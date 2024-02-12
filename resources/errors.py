class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class AssignmentAlreadyExistsError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class SubmissionAlreadyExistsError(Exception):
    pass

class AnalysisAlreadyExistsError(Exception):
    pass

class UpdatingAssignmentError(Exception):
    pass

class UpdatingUserError(Exception):
    pass

class UpdatingSubmissionError(Exception):
    pass

class UpdatingAnalysisError(Exception):
    pass

class DeletingAssignmentError(Exception):
    pass

class DeletingUserError(Exception):
    pass

class DeletingSubmissionError(Exception):
    pass

class DeletingAnalysisError(Exception):
    pass

class AssignmentNotExistsError(Exception):
    pass

class UserNotExistsError(Exception):
    pass

class SubmissionNotExistsError(Exception):
    pass

class AnalysisNotExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UnauthorizedError(Exception):
    pass

class EmailDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
     "AssignmentAlreadyExistsError": {
         "message": "Assignment with given name already exists",
         "status": 400
     },
    "UserAlreadyExistsError": {
         "message": "User with given username already exists",
         "status": 400
     },
    "SubmissionAlreadyExistsError": {
         "message": "Submission with given author already exists",
         "status": 400
     },
    "AnalysisAlreadyExistsError": {
         "message": "Analysis with given submission already exists",
         "status": 400
     },
     "UpdatingAssignmentError": {
         "message": "Updating assignment added by other is forbidden",
         "status": 403
     },
    "UpdatingUserError": {
         "message": "Updating user added by other is forbidden",
         "status": 403
     },
    "UpdatingSubmissionError": {
         "message": "Updating submission added by other is forbidden",
         "status": 403
     },
    "UpdatingAnalysisError": {
         "message": "Updating analysis added by other is forbidden",
         "status": 403
     },
     "DeletingAssignmentError": {
         "message": "Deleting assignment added by other is forbidden",
         "status": 403
     },
    "DeletingUserError": {
         "message": "Deleting user added by other is forbidden",
         "status": 403
     },
    "DeletingSubmissionError": {
         "message": "Deleting submission added by other is forbidden",
         "status": 403
     },
    "DeletingAnalysisError": {
         "message": "Deleting analysis added by other is forbidden",
         "status": 403
     },
     "AssignmentNotExistsError": {
         "message": "Assignment with given id doesn't exists",
         "status": 400
     },
    "UserNotExistsError": {
         "message": "User with given id doesn't exists",
         "status": 400
     },
    "SubmissionNotExistsError": {
         "message": "Submission with given id doesn't exists",
         "status": 400
     },
    "AnalysisNotExistsError": {
         "message": "Analysis with given id doesn't exists",
         "status": 400
     },
     "EmailAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },
     "EmailDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
     }
}