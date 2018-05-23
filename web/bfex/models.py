from elasticsearch_dsl import DocType, Integer, Text, Date
from elasticsearch import NotFoundError


class Model(object):
    """Basic class that provides utility methods to our elasticsearch models."""

    @classmethod
    def safe_get(cls, id):
        """Performs a safe get of an elasticsearch object by id, avoiding 404 exception from elasticsearch.

        :param id: The id of the object in elastic to get.
        :return The object if found, otherwise None."""
        try:
            obj = cls.get(id=id)
        except NotFoundError:
            obj = None
        return obj


class Faculty(DocType, Model):
    """Definition of the basic Faculty doctype.

    Contains any information related to a Faculty member instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index faculty.
    """
    faculty_id = Integer(required=True)
    name = Text(required=True)
    full_name = Text()
    email = Text(required=True)
    department = Text()

    google_scholar = Text()
    orc_id = Text()
    sciverse_id = Text()
    research_id = Text()

    user_keywords = Text()

    class Meta:
        index = "faculty"

    def __str__(self):
        return "<Faculty ID:{} Name: {} Email: {}".format(self.faculty_id, self.name, self.email)
        

class Keywords(DocType,Model):
    """Definition of the basic Keywords doctype.

    Contains any information related to a keywords instance generated from the keyword generation approaches.
    Data is saved in the elasticsearch index keywords.
    """
    faculty_id = Integer(required=True)
    datasource = Text(required=True)
    approach_id = Integer(required=True)
    keywords = Text()

    class Meta: 
        index = "keywords"

    def __str__(self):
        return "<Faculty ID:{} Keywords:{}>".format(self.faculty_id,self.keywords)


class Grant(DocType):
    """Definition of the basic Grant doctype.

    Contains any information related to a Grant instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index grants.
    """
    faculty_id = Integer(required=True)
    source = Text(required=True)
    title = Text()
    text = Text()

    application_group = Text()
    application_group_fr = Text()
    application_area = Text()
    application_area_fr = Text()

    class Meta:
        index = "grants"


class Publication(DocType):
    """Definition of the basic Publication doctype.

    Contains any information related to a Publication instance pulled from the Forum data dump, or page scrapes.
    Data is saved in the elaticsearch index grants.
    """
    publication_id = Integer(required=True)
    authors = Integer(required=True)
    title = Text()
    type = Text()
    url = Text()
    data = Text()
    
    class Meta:
        index = "publications"


class Document(DocType, Model):
    """Definition of the basic Document doctype.

    Contains any information related to a Document member instance
    pulled from scrapes.
    Data is saved in the elaticsearch index document.
    """
    faculty_id = Integer(required=True)
    source = Text(required=True)

    user_keywords = Text()
    text = Text()
    date = Date()

    class Meta:
        index = "document"

    def __str__(self):
        return "<Faculty ID:{} Source: {} Text: {}".format(self.faculty_id, self.source, self.text)


class Lexicon(DocType, Model):
    """Definition of the basic Lexicon doctype.

    Contains all keywords to be pulled from text.
    Data is saved in the elaticsearch index lexicon.
    """
    keywords = Text(required=True)

    class Meta:
        index = "lexicon"

    def __str__(self):
        return "<Keywords:{}".format(self.keywords)

def initialize_models():
    """Initializes the mappings of all models in ElasticSearch. Expects that a connection to elastic has already been
    initialized.
    """
    models = [Faculty, Keywords, Grant, Publication, Document, Lexicon]
    for model in models:
        try:
            model.init()
        except:
            continue


# if __name__ == "__main__":
#     from elasticsearch_dsl.connections import connections
#     connections.create_connection(hosts=["localhost"])

#     Faculty.init()

#     prof = Faculty(meta={'id': 42}, name="Garry Bullock", email="gbullock@ualberta.ca", faculty_id=42)
#     prof.save()

#     saved_prof = Faculty.get(id=42)
#     print(saved_prof.name)

#     print(connections.get_connection().cluster.health())