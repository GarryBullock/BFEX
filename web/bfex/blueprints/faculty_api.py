from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import Faculty, Keywords, Document, Grant
from bfex.components.data_ingestor import DataIngester
from bfex.common.exceptions import DataIngestionException
from bfex.common.schema import FacultySchema, KeywordSchema, GrantSchema, FacultyForumSchema
from bfex.blueprints.api_utils import paginate_query

MB = 1024 * 1024

# Setup the blueprint and add to the api.
faculty_bp = Blueprint("faculty_api", __name__)
api = Api(faculty_bp)


class FacultyAPI(Resource):
    """Contains methods for performing basic CRUD operations on Faculty members"""

    def get(self, faculty_id):
        """ HTTP Get for the faculty resource.

        Currently returns an HTML page, but should instead return the Faculty object as JSON.

        :param faculty_id: The id as is in elasticsearch. This id is defined by the forum data dump.
        :return:HTTP 404 if the given ID does not exist.
                HTTP 200 if the id exists and the GET operation succeeds.
        """
        faculty = Faculty.safe_get(faculty_id)

        if faculty is None:
            abort(404)

        return make_response(render_template("faculty.html", faculty=faculty), 200, {'content-type': 'text/html'})


class FacultyListAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def get(self):
        """HTTP Get for the faculty list resource.

        Returns a list of faculty members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :return:
        """
        search = Faculty.search()
        query, pagination_info = paginate_query(request, search)
        response = query.execute()

        schema = FacultySchema()
        results = [schema.dump(faculty) for faculty in response]

        return {
            "pagination": pagination_info,
            "data": results
        }

    def post(self):
        """HTTP Post for the faculty list resource.

        Ingests a lists of faculty members, and saves the information into elasticsearch. Currently does not do any
        checks if there already exists a faculty member with the same id that will be overridden.
        TODO: Decide if this should check for existing faculty and return which faculty were not inserted, and add PUT.

        :return:HTTP 400 if the request is not JSON.
                HTTP 413 if the given JSON is more than 16MB in size or there was an error ingesting the given data.
                HTTP 200 if the ingestion succeeded.
        """
        if not request.is_json:
            abort(400)

        # Data larger than 16MB should be broken up.
        if request.content_length > 16*MB:
            abort(413)

        json_data = request.get_json()

        try:
            DataIngester.bulk_create_faculty(json_data["data"])
        except DataIngestionException:
            abort(413)

        return 200


class DataDumpAPI(Resource):
    """Methods for performing some operations on lists of Faculty members."""

    def get(self):
        """HTTP Get for the faculty list resource.

        Returns a list of faculty members from elasticsearch.
        :param page: URL Parameter for the page to fetch. Default - 0.
        :param results: URL Parameter for the number of results to return per page. Default - 20.
        :return:
        """
        search = Faculty.search()
        # query = search
        # query, pagination_info = paginate_query(request, search)
        response = search.scan()

        schema = FacultyForumSchema()
        results = []
        for faculty in response:
            key_search = Keywords.search().query('match', faculty_id=faculty.faculty_id) \
                .query('match', approach_id=4) \
                .execute()
            generated_key_search = Keywords.search().query('match', faculty_id=faculty.faculty_id) \
                .query('match', approach_id=5)
            grant_search = Grant.search().query('match', faculty_id=faculty.faculty_id) \
                .execute()  

            faculty.scraped_keywords = key_search
            faculty.generated_keywords = generated_key_search
            faculty.grants = grant_search

            results.append(schema.dump(faculty))

        return {
            # "pagination": pagination_info,
            "data": results
        }


api.add_resource(FacultyAPI, '/faculty/<int:faculty_id>')
api.add_resource(FacultyListAPI, '/faculty')
api.add_resource(DataDumpAPI, '/faculty/dump')
