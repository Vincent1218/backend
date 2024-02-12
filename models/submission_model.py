from database.db import db

class DGISubtype(db.EmbeddedDocument):
    finalScore = db.FloatField(min_value=0, max_value=1)
    numPara = db.IntField(min_value=0, max_value=1000)
    numDisciplines = db.IntField(min_value=0, max_value=1000)

class DIISubtype(db.EmbeddedDocument):
    finalScore = db.FloatField(min_value=0, max_value=1)
    numPara = db.IntField(min_value=0, max_value=1000)
    selectedPara = db.IntField(min_value=0, max_value=1000)

class DEISubtype(db.EmbeddedDocument):
    finalScore = db.FloatField(min_value=0, max_value=1)
    paraBusiness = db.IntField(min_value=0, max_value=1000)
    paraHumanities = db.IntField(min_value=0, max_value=1000)
    paraSciences = db.IntField(min_value=0, max_value=1000)
    paraSum = db.IntField(min_value=0, max_value=1000)
    paraTechnology = db.IntField(min_value=0, max_value=1000)
    summationVal = db.FloatField(min_value=0, max_value=1)

# class Submission(db.Document):
#     submissionDate = db.fields.StringField(required=True)
#     author = db.fields.StringField(required=True)
#     fileName = db.fields.StringField(required=True)
#     content = db.fields.StringField(required=True)
#     submissionName = db.fields.StringField(required=True)
#     disciplines = db.fields.ListField(db.fields.StringField())
#     DGIscore = db.fields.EmbeddedDocumentField(DGISubtype)
#     DIIscore = db.fields.EmbeddedDocumentField(DIISubtype)
#     DEIscore = db.fields.EmbeddedDocumentField(DEISubtype)

class score(db.EmbeddedDocument):
    advancement = db.fields.DecimalField(min_value=0, max_value=2)
    diversity = db.fields.DecimalField(min_value=0, max_value=2)
    grounding = db.fields.DecimalField(min_value=0, max_value=2)
    integration = db.fields.DecimalField(min_value=0, max_value=2)


class Submission(db.Document):
    submissionDate = db.fields.StringField(required=True)
    author = db.fields.StringField(required=True)
    fileName = db.fields.StringField(required=True)
    content = db.fields.StringField(required=True)
    submissionName = db.fields.StringField(required=True)
    score = db.fields.EmbeddedDocumentField(score)



