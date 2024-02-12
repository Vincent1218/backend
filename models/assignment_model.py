from decimal import Decimal
from database.db import db


class Assignment(db.Document):
    assignmentName = db.fields.StringField(required=True, unique=True)
    question = db.fields.StringField(required=True)
    startDate = db.fields.StringField(required=True)
    dueDate = db.fields.StringField(required=True)
    tries = db.IntField(min_value=1, max_value=10)
    revealResults = db.BooleanField(default=False)
    averageDGI = db.fields.DecimalField(min_value=Decimal("0"), max_value=Decimal("1"))
    averageDII = db.fields.DecimalField(min_value=Decimal("0"), max_value=Decimal("1"))
    averageDEI = db.fields.DecimalField(min_value=Decimal("0"), max_value=Decimal("1"))


