from decimal import Decimal
from database.db import db


class DimensionsSubtype(db.EmbeddedDocument):
    advancement = db.fields.IntField(min_value=0, max_value=2)
    diversity = db.fields.IntField(min_value=0, max_value=2)
    grounding = db.fields.IntField(min_value=0, max_value=2)
    integration = db.fields.IntField(min_value=0, max_value=2)


class InstancesSubtype(db.EmbeddedDocument):
    content = db.fields.StringField(required=True)
    dimensions = db.fields.EmbeddedDocumentField(DimensionsSubtype)

class Analysis(db.Document):
    submissionID = db.fields.StringField(required=True)
    paragraphs = db.fields.ListField(db.fields.EmbeddedDocumentField(InstancesSubtype))






