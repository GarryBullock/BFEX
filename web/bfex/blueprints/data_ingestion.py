from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.models import *
from bfex.components.data_ingestor import DataIngester
from bfex.common.exceptions import DataIngestionException

MB = 1024 * 1024

# Setup the blueprint and add to the api.
data_ingestion_bp = Blueprint("data_ingestion", __name__)
api = Api(data_ingestion_bp)


class FacultyAPI(Resource):
    """Contains methods for performing basic CRUD operations on Faculty members"""

    def get(self, faculty_id):
        """ HTTP Get for the faculty resource.

        Currently returns an HTML page, but should instead return the Faculty object as JSON
        """
        faculty = Faculty.safe_get(faculty_id)

        if faculty is None:
            abort(404)

        return make_response(render_template("faculty.html", faculty=faculty), 200, {'content-type': 'text/html'})


class FacultyListAPI(Resource):

    def post(self):
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


api.add_resource(FacultyAPI, '/faculty/<int:faculty_id>')
api.add_resource(FacultyListAPI, '/faculty')

