from marshmallow import Schema, fields, post_load

from bfex.models import *


class KeywordSchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.
    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", required=True, dump_to="id")
    datasource = fields.String()
    approach_id = fields.Integer(dump_to="approachId")
    keywords = fields.List(fields.String)

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Keywords(meta={}, **data)


class FacultySchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.

    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", required=True)
    name = fields.String(required=True)
    full_name = fields.String(load_from="fullName", required=True)
    email = fields.Email(required=True)
    department = fields.String(allow_none=True, missing="Unknown")

    google_scholar = fields.String(load_from="googleScholarId")
    orc_id = fields.String(load_from="orcId")
    sciverse_id = fields.String(load_from="sciverseId")
    research_id = fields.String(load_from="researchId", missing="")

    generated_keywords = fields.Nested(KeywordSchema, exclude=('faculty_id',), many=True)

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Faculty(meta={'id': data["faculty_id"]}, **data)

    class Meta:
        ordered = True


class GrantSchema(Schema):
    faculty_name = fields.String(load_from="faculty_name", required=True)
    title = fields.String(missing="", required=True)
    text = fields.String(load_from="summary", required=True)
    source = fields.String(missing="nserc")

    application_group = fields.String(dump_to="applicationGroup")
    application_group_fr = fields.String(dump_to="applicationGroupFR")
    application_area = fields.String(dump_to="applicationArea")
    application_area_fr = fields.String(dump_to="applicationAreaFR")


class FacultyForumSchema(Schema):
    """Marshmallow schema used for validating Faculty JSON objects.

    A marshmallow schema allows us to easily extract information from JSON input, while at the same time, performing
    basic validation of that data.
    """
    faculty_id = fields.Integer(load_from="id", dump_to="id", required=True)
    # id = fields.Integer(attribute="faculty_id", dump_only=True)

    name = fields.String(required=True)

    full_name = fields.String(load_from="fullName", dump_to="fullName", required=True)
    # fullName = fields.String(attribute="full_name", dump_only=True)

    email = fields.Email(required=True)
    department = fields.String(allow_none=True, missing="Unknown")

    google_scholar = fields.String(load_from="googleScholarId", dump_to="googleScholarId")
    # googleScholarId = fields.String(attribute="google_scholar", dump_only=True)

    orc_id = fields.String(load_from="orcId", dump_to="orcId")
    # orcId = fields.String(attribute="orc_id", dump_only=True)

    sciverse_id = fields.String(load_from="sciverseId", dump_to="sciverseId")
    # sciverseId = fields.String(attribute="sciverse_id", dump_only=True)

    research_id = fields.String(load_from="researchId", dump_to="researchId", missing="")
    # researchId = fields.String(load_from="research_id", dump_only=True)

    scraped_keywords = fields.Nested(KeywordSchema, exclude=('faculty_id',), many=True, dump_to="scrapedKeywords")
    generated_keywords = fields.Nested(KeywordSchema, exclude=('faculty_id',), many=True, dump_to="generatedKeywords")
    grants = fields.Nested(GrantSchema, exclude=('faculty_name',), many=True)

    @post_load
    def _create_faculty(self, data):
        """Turns the extracted json data into an instance of Faculty"""
        return Faculty(meta={'id': data["faculty_id"]}, **data)

    class Meta:
        ordered = True


class DocumentSchema(Schema):
    faculty_id = fields.String(required=True)
    source = fields.String(required=True)

    title = fields.String()
    text = fields.String()
    date = fields.Date()
    keywords = fields.String()

class LexiconSchema(Schema):
    keywords = fields.List(fields.String)