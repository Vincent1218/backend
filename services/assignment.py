

# from flask import Response, request
# from models.assignment_model import Assignment
# from models.analysis_model import Analysis
# from models.submission_model import Submission
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from flask_restful import Resource
# from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
# from resources.errors import SchemaValidationError, AssignmentAlreadyExistsError, InternalServerError, \
#     UpdatingAssignmentError, DeletingAssignmentError, AssignmentNotExistsError


# class AssignmentsApi(Resource):
#     @jwt_required()
#     def get(self):
#         assignments = Assignment.objects().to_json()
#         print(assignments)
#         return Response(assignments, mimetype="application/json", status=200)

#     @jwt_required()
#     def post(self):
#         try:
#             body = request.get_json()
#             assignment = Assignment(**body)
#             assignment.save()
#             id = assignment.id
#             return {'id': str(id)}, 200
#         except (FieldDoesNotExist, ValidationError):
#             raise SchemaValidationError
#         except NotUniqueError:
#             raise AssignmentAlreadyExistsError
#         except Exception as e:
#             raise InternalServerError


# class AssignmentApi(Resource):
#     @jwt_required()
#     def put(self, id):
#         try:
#             body = request.get_json()
#             Assignment.objects.get(id=id).update(**body)
#             return '', 200
#         except InvalidQueryError:
#             raise SchemaValidationError
#         except DoesNotExist:
#             raise UpdatingAssignmentError
#         except Exception:
#             raise InternalServerError

#     @jwt_required()
#     def delete(self, id):
#         try:
#             submissions = Submission.objects(assignmentID__exact=id)
#             submissions.delete()
#             analysis = Analysis.objects(assignmentID__exact=id)
#             analysis.delete()
#             assignment = Assignment.objects.get(id=id)
#             assignment.delete()
#             return 'Deletion successful', 200
#         except DoesNotExist:
#             raise DeletingAssignmentError
#         except Exception:
#             raise InternalServerError

#     @jwt_required()
#     def get(self, id):
#         try:
#             assignment = Assignment.objects.get(id=id).to_json()
#             return Response(assignment, mimetype="application/json", status=200)
#         except DoesNotExist:
#             raise AssignmentNotExistsError
#         except Exception:
#             raise InternalServerError
