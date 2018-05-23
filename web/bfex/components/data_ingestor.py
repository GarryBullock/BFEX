from collections.abc import Sequence

from marshmallow.exceptions import ValidationError
from bfex.models import Faculty, Document
from bfex.common.schema import *
from bfex.common.exceptions import DataIngestionException
from bfex.components.data_pipeline.tasks import FacultyPageScrape, UpdateFacultyFromScrape, ResearchIdPageScrape, GoogleScholarPageScrape, GetKeywordsFromScrape, UpdateKeywordsFromGenerator
from bfex.tasks import run_workflow
from bfex.components.data_pipeline.workflow import Workflow

class DataIngester(object):
    INITIAL_PAGE_SCRAPE = [FacultyPageScrape, UpdateFacultyFromScrape, ResearchIdPageScrape, GoogleScholarPageScrape, GetKeywordsFromScrape, UpdateKeywordsFromGenerator]

    @staticmethod
    def create_faculty(json_data, write=True):
        """Creates an instance of Faculty from a JSON representation.

        :param dict json_data: Dictionary representation of the JSON data.
        :param bool write: Boolean switch that will enable writing to elastic.
        """
        schema = FacultySchema()

        try:
            faculty = schema.load(json_data)
        except ValidationError as err:
            raise DataIngestionException("Missing one of the required fields of the schema. {}"
                                         .format(err.messages))

        if write:
            faculty.save()

        workflow = Workflow(DataIngester.INITIAL_PAGE_SCRAPE, faculty.name)
        run_workflow.apply_async((workflow,), countdown=5)

    @staticmethod
    def bulk_create_lexicon(json_data, write=True):
        """Takes in a list of JSON objects, and loads them into elasticsearch.

        :exception TypeError: If the json_data is not a sequence object. The expected type is a List.
        """
        if not isinstance(json_data, Sequence):
            raise TypeError("Expected a Sequence, but got a {}", type(json_data))

        if write:
            lex = Lexicon()
            lex.keywords = json_data
            lex.save()
            
        print("Ingested lexicon words")

    @staticmethod
    def bulk_create_faculty(json_data, write=True):
        """Takes in a list of JSON objects, and loads them into elasticsearch.

        :exception TypeError: If the json_data is not a sequence object. The expected type is a List.
        """
        if not isinstance(json_data, Sequence):
            raise TypeError("Expected a Sequence, but got a {}", type(json_data))

        count = 0
        for faculty_member in json_data:
            count += 1
            DataIngester.create_faculty(faculty_member, write)

        print("Ingested {} faculty members".format(count))

    @staticmethod
    def create_grant(json_data, write=True):
        """Creates an instance of Faculty from a JSON representation.

        :param dict json_data: Dictionary representation of the JSON data.
        :param bool write: Boolean switch that will enable writing to elastic.
        """
        schema = GrantSchema()

        try:
            grant = schema.load(json_data)
        except ValidationError as err:
            raise DataIngestionException("Missing one of the required fields of the schema. {}"
                                         .format(err.messages))

        # Need to find a faculty with matching name so we can build a new document
        search_results = Faculty.search().query('match', full_name=grant["faculty_name"]).execute()
        if len(search_results) < 1:
            return
        faculty = search_results[0]

        # TODO: There is no spot for titles in the document...
        grant_doc = Document(faculty_id=faculty.faculty_id, source=grant["source"], text=grant["text"])
        grant = Grant(faculty_id=faculty.faculty_id, **grant)
        if write:
            grant_doc.save()
            grant.save()
        

    @staticmethod
    def bulk_create_grants(json_data, write=True):
        """Takes in a list of JSON objects, and loads them into elasticsearch.

        :exception TypeError: If the json_data is not a sequence object. The expected type is a List.
        """
        if not isinstance(json_data, Sequence):
            raise TypeError("Expected a Sequence, but got a {}", type(json_data))

        count = 0
        for grant in json_data:
            count += 1
            DataIngester.create_grant(grant, write)

        print("Ingested {} grants".format(count))


    @staticmethod
    def create_publication(json_data, write=True):
        pass

    @staticmethod
    def bulk_create_publications(json_data, write=True):
        pass
