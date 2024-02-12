from flask import Response, request, jsonify
from models.analysis_model import Analysis
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, AnalysisAlreadyExistsError, InternalServerError, \
    UpdatingAnalysisError, DeletingAnalysisError, AnalysisNotExistsError



class AnalysisApi(Resource):
    @jwt_required()
    def post(self):
        try:
            # To be used in the future
            pass

        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise AnalysisAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class TargetAnalysisApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            Analysis.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingAnalysisError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            analysis = Analysis.objects().filter(submissionID=id)
            analysis.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingAnalysisError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def get(self, id):
        try:
            analysis = Analysis.objects().filter(submissionID=id)
            analysis_obj = analysis.to_json()
            return Response(analysis_obj, mimetype="application/json", status=200)
        except DoesNotExist:
            raise AnalysisNotExistsError
        except Exception:
            raise InternalServerError
