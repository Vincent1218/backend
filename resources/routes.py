from services.user import UsersApi, UserApi
# from services.assignment import AssignmentsApi, AssignmentApi
# from services.analysis import AnalysisApi, TargetAnalysisApi
from services.analysis import TargetAnalysisApi
from services.submission import SubmissionsApi, SubmissionApi
from .auth import SignupApi, LoginApi, RefreshApi

def initialize_routes(api):
    # User routes
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/user/<id>')

    # Assignment routes
    # api.add_resource(AssignmentsApi, '/api/assignments')
    # api.add_resource(AssignmentApi, '/api/assignment/<id>')

    # Submission routes
    api.add_resource(SubmissionsApi, '/api/submissions/<uid>')
    api.add_resource(SubmissionApi, '/api/submission/<id>')

    # Analysis routes
    # api.add_resource(AnalysisApi, '/api/analysis')
    api.add_resource(TargetAnalysisApi, '/api/targetAnalysis/<id>')

    # Authentication routes
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    api.add_resource(RefreshApi, '/api/auth/refresh')
