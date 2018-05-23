from bfex.components.data_pipeline.tasks import Task
from bfex.components.scraper.scrapp import Scrapp
from bfex.models import *
from bfex.common.exceptions import WorkflowException
from bfex.components.key_generation.rake_approach import *
from bfex.components.key_generation.generic_approach import *
from bfex.components.key_generation.textrank_approach import *
from bfex.components.key_generation.key_generator import KeyGenerator
import time

class GetKeywordsFromScrape(Task):
    """
    Updates Keywords of a Faculty Members data in elastic.
    """
    def __init__(self):
        self.task_name = "Update Keywords From Scrape"

    def is_requirement_satisfied(self, faculty):
        """Verifies that the data is acceptable and has the faculty_id.

        :param faculty: Expected to be a faculty object with an id.
        :returns True if the data is of the form above, else False.
        """
        satisfied = True

        if (not isinstance(faculty.faculty_id, int)):
            satisfied = False

        return satisfied


    def run(self,faculty):
        """ Updates keywords of a prof

        :param faculty is a faculty object
        :return: list of keyword objects
        """
        key_objects= []
        faculty_id = faculty.faculty_id
        time.sleep(1)
        search_results = Document.search().query('match', faculty_id=faculty_id).execute()
        for document in search_results:
            #Approaches will be registered somewhere else                  
            key_generator  = KeyGenerator.instance()

            keys = key_generator.generate_keywords(document.text)

            for approach in keys:
                if len(keys[approach]) == 0:
                    continue
                keywords = Keywords()
                keywords.faculty_id = document.faculty_id
                keywords.datasource = document.source
                keywords.approach_id = approach
                keywords.keywords = keys[approach]

                key_objects.append(keywords)

        return key_objects


if __name__ == "__main__":
    from elasticsearch_dsl import connections
    connections.create_connection()
    Keywords.init()

    #search = Document.search()
    #allDocument = [document for document in search.scan()]
    #task = GetKeywordsFromScrape()
    #task.run(allDocument)
