from flask import Blueprint, abort, render_template, make_response, request
from flask_restful import Resource, Api

from bfex.components.search_engine import parser, builder
from bfex.components.data_pipeline.tasks import *
from bfex.components.data_pipeline.workflow import Workflow
from bfex.models import Faculty
from bfex.tasks import run_workflow

# Setup the blueprint and add to the api.
workflow_bp = Blueprint("workflow", __name__)
api = Api(workflow_bp)

TASKLIST = {
    "tfidf": [GetKeywordsFromScrape, UpdateKeywordsFromGenerator]
}


class WorkflowAPI(Resource):
    """Contains methods for performing search over keywords."""

    def post(self):
        """HTTP Get that enables boolean query processing and search."""
        to_run = request.args.get('run')
        faculty = request.args.get('faculty')

        if not to_run or not faculty:
            abort(400)

        try:
            task_list = TASKLIST[to_run]
        except:
            abort(400)

        workflow = Workflow(task_list, Faculty.safe_get(faculty))
        run_workflow.apply_async((workflow,), countdown=1)

        return 200
        
class BatchWorkflowAPI(Resource):
    def post(self):
        to_run = request.args.get('run')

        if not to_run:
            abort(400)

        try:
            task_list = TASKLIST[to_run]
        except:
            abort(400)

        faculty = Faculty.search().scan()

        for f in faculty:
            workflow = Workflow(task_list, f)
            run_workflow.apply_async((workflow,), countdown=1)

        return 200


api.add_resource(WorkflowAPI, '/workflow')
api.add_resource(BatchWorkflowAPI, '/workflow/batch')
