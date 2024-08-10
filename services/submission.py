from flask import Response, request
import json
from models.analysis_model import Analysis
from models.submission_model import Submission
from services.analyzer import *
from services.chatgptAnalyzer import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, SubmissionAlreadyExistsError, InternalServerError, \
    UpdatingSubmissionError, DeletingSubmissionError, SubmissionNotExistsError

from PyPDF2 import PdfReader
from docx import Document


class SubmissionsApi(Resource):
    @jwt_required()
    def get(self, uid):
        submissions = Submission.objects().filter(author=uid)
        submissions_obj = submissions.to_json()
        submissions_dic = json.loads(submissions_obj)  # converting string into json object
        temp_array = []
        for i in range(len(submissions_dic)):
            temp_dict = {"id": submissions_dic[i]["_id"]["$oid"]}
            month = ""
            if submissions_dic[i]["submissionDate"][5:7] == "01":
                month = "Jan"
            elif submissions_dic[i]["submissionDate"][5:7] == "02":
                month = "Feb"
            elif submissions_dic[i]["submissionDate"][5:7] == "03":
                month = "Mar"
            elif submissions_dic[i]["submissionDate"][5:7] == "04":
                month = "Apr"
            elif submissions_dic[i]["submissionDate"][5:7] == "05":
                month = "May"
            elif submissions_dic[i]["submissionDate"][5:7] == "06":
                month = "Jun"
            elif submissions_dic[i]["submissionDate"][5:7] == "07":
                month = "Jul"
            elif submissions_dic[i]["submissionDate"][5:7] == "08":
                month = "Aug"
            elif submissions_dic[i]["submissionDate"][5:7] == "09":
                month = "Sep"
            elif submissions_dic[i]["submissionDate"][5:7] == "10":
                month = "Oct"
            elif submissions_dic[i]["submissionDate"][5:7] == "11":
                month = "Nov"
            elif submissions_dic[i]["submissionDate"][5:7] == "12":
                month = "Dec"
            temp_dict["date"] = submissions_dic[i]["submissionDate"][8:10] + " " + month + " " + submissions_dic[i][
                                                                                                     "submissionDate"][
                                                                                                 0:4] + ", " + \
                                submissions_dic[i]["submissionDate"][11:13] + " " + submissions_dic[i][
                                                                                        "submissionDate"][14:] + " HRS"
            temp_dict["title"] = submissions_dic[i]["submissionName"]

            # temp_dict["dgi"] = round(submissions_dic[i]["DGIscore"]["finalScore"] * 100)
            # temp_dict["dii"] = round(submissions_dic[i]["DIIscore"]["finalScore"] * 100)
            # temp_dict["dei"] = round(submissions_dic[i]["DEIscore"]["finalScore"] * 100)
            # temp_dict["disciplines"] = len(submissions_dic[i]["disciplines"])

            temp_dict["score"] = submissions_dic[i]["score"]
            temp_array.append(temp_dict)

        # reverse array
        temp_array.reverse()
        
        return_array = json.dumps(temp_array)
        
        

        return Response(return_array, mimetype="application/json", status=200)

    # def post(self, uid):
    #     try:

    #         body = request.get_json()
    #         body['author'] = uid

    #         ml_results = generate_results(body['content'])
    #         submission_body = calculate_scores(body, ml_results)

    #         submission = Submission(**submission_body)
    #         submission.save()
    #         submission_id = submission.id

    #         business_count = 0
    #         humanities_count = 0
    #         sciences_count = 0
    #         technology_count = 0

    #         for i in range(len(ml_results)):
    #             keys_list = list(ml_results[i]['disciplines'].keys())
    #             if 'business' in keys_list:
    #                 business_count = business_count + 1
    #             if 'humanities' in keys_list:
    #                 humanities_count = humanities_count + 1
    #             if 'sciences' in keys_list:
    #                 sciences_count = sciences_count + 1
    #             if 'technology' in keys_list:
    #                 technology_count = technology_count + 1

    #         disciplines_proportion = []
    #         sum_count = business_count + humanities_count + sciences_count + technology_count
    #         if humanities_count != 0:
    #             disciplines_proportion.append(
    #                 {'discipline': 'Humanities', 'proportion': str(round(humanities_count / sum_count * 100))})
    #         if sciences_count != 0:
    #             disciplines_proportion.append(
    #                 {'discipline': 'Sciences', 'proportion': str(round(sciences_count / sum_count * 100))})
    #         if technology_count != 0:
    #             disciplines_proportion.append(
    #                 {'discipline': 'Technology', 'proportion': str(round(technology_count / sum_count * 100))})
    #         if business_count != 0:
    #             disciplines_proportion.append(
    #                 {'discipline': 'Business', 'proportion': str(round(business_count / sum_count * 100))})

    #         analysis_body = {'submissionID': str(submission_id), 'paragraphs': ml_results,
    #                          'disciplinesProportion': disciplines_proportion}
    #         analysis = Analysis(**analysis_body)
    #         analysis.save()

    #         """

    #         body = request.get_json()
    #         submission = Submission(**body)
    #         submission.save()
    #         submission_id = submission.id

    #         #User.objects.get(id="63db0fa34eba1dda0a70dd0a").update({'$push': {'submissions': '63e1a26bce0f25e013a7d187'}})

    #         #submission_json_obj = json.loads(body)  # converting string into json object
    #         #temp_dic_submission = dict(submission_json_obj)  # converting json object into python dictionary
    #         authors_array = body['authors']

    #         for id in authors_array:
    #             user = User.objects.get(id=id)
    #             user_string = user.to_json()
    #             user_json_obj = json.loads(user_string)  # converting string into json object
    #             temp_dic = dict(user_json_obj)  # converting json object into python dictionary
    #             #del temp_dic['_id']
    #             temp_array = temp_dic['submissions']
    #             temp_array.append(str(submission_id))

    #             #temp_str = "{'submissions': " + str(temp_array) + "}"
    #             #temp_dic.update(eval(temp_str))
    #             #output_json = json.loads(json.dumps(temp_dic))

    #             user.update(submissions=temp_array)

    #         return {'id': str(submission_id)}, 200
    #         """
    #         return {'id': str(submission_id)}, 200

    #     except (FieldDoesNotExist, ValidationError):
    #         raise SchemaValidationError
    #     except NotUniqueError:
    #         raise SubmissionAlreadyExistsError
    #     except Exception as e:
    #         raise InternalServerError

    def post(self, uid):
        try:

            body = {
                'author': "",
                'fileName': "",
                'submissionName': "",
                'submissionDate': "",
                'content': "",
            }

            if 'file' not in request.files:
                return 'No file part', 400  

            file = request.files['file']
            if file.filename == '':
                return 'No selected file', 400

            # extract passed data
            submission_date = request.form.get('submissionDate')
            submission_name = request.form.get('submissionName')

            # assign data to body
            body['author'] = uid
            body['fileName'] = file.filename
            body['submissionName'] = submission_name
            body['submissionDate'] = submission_date


            # Check file type
            # pdf
            if file.filename.endswith('.pdf'):
                reader = PdfReader(file)
                pagesNo = len(reader.pages)
            
                final_text = ""
                # getting all pages from the pdf file 
                for i in range(pagesNo):
                    page = reader.pages[i] 
                    # extracting text from page 
                    text = page.extract_text()  
                    final_text += text
                    
                # Split by paragraphs
                paragraphs = final_text.split("\n \n")              
                # Remove \n
                for i in range(len(paragraphs)):
                    paragraphs[i] = paragraphs[i].replace("\n", "")
                    
                # Remove empty paragraphs
                paragraphs = [x for x in paragraphs if x != '']
                
                print("Paragraph length")
                print(len(paragraphs))
                print(paragraphs)  
                
                # Join paragraphs
                final_text = "\n\n".join(paragraphs)
                    
                body['content'] = final_text            
                print(final_text)

            # docs
            elif file.filename.endswith('.docx'):
                document = Document(file)
                final_text = ""
                for para in document.paragraphs:
                    ## para.text already has \n
                    final_text += para.text + "\n"
                    
                body['content'] = final_text
                print(final_text)
            
            # txt
            elif file.filename.endswith('.txt'):
                final_text = file.read()
                final_text = final_text.decode("utf-8")

                body['content'] = final_text
                print(final_text)

            else:
                return 'Invalid file type', 400

            # split paragraphs
            paragraphs_content = body['content'].split("\n")
            
            # remove empty paragraphs
            paragraphs_content = [x for x in paragraphs_content if ((x != '') and (x != ' ') and (x != '\n'))]

            # evaluate each paragraph
            chatgpt_results = []
            for paragraph in paragraphs_content:
                print("Para: ", paragraph)
                # if paragraph length is less, eg(Title, Name, etc)
                if len(paragraph) < 50:
                    chatgpt_results.append({
                        "advancement": 0,
                        "diversity": 0,
                        "grounding": 0,
                        "integration": 0,
                    })
                else:
                    chatgpt_results.append(evaluate_row(paragraph, "essay"))

            overall_results = {
                "advancement": 0,
                "diversity": 0,
                "grounding": 0,
                "integration": 0,
            }

            for result in chatgpt_results:
                overall_results["advancement"] += result["advancement"]
                overall_results["diversity"] += result["diversity"]
                overall_results["grounding"] += result["grounding"]
                overall_results["integration"] += result["integration"]

            overall_results["advancement"] = overall_results["advancement"] / len(chatgpt_results)
            overall_results["diversity"] = overall_results["diversity"] / len(chatgpt_results)
            overall_results["grounding"] = overall_results["grounding"] / len(chatgpt_results)
            overall_results["integration"] = overall_results["integration"] / len(chatgpt_results)

            # combine body and chatgpt_results
            body['score'] = overall_results

            print("body:" , body)

            submission = Submission(**body)
            submission.save()
            submission_id = submission.id

            analysis_result = []

            for i in range(len(chatgpt_results)):
                temp_dict = {"content": paragraphs_content[i], "dimensions": chatgpt_results[i]}
                analysis_result.append(temp_dict)



            analysis_body = {'submissionID': str(submission_id), 'paragraphs': analysis_result}
            analysis = Analysis(**analysis_body)
            analysis.save()
            return {'id': str(submission_id)}, 200

        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise SubmissionAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class SubmissionApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            Submission.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingSubmissionError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            submission = Submission.objects.get(id=id)
            submission.delete()

            analysis = Analysis.objects().filter(submissionID=id)
            analysis.delete()

            return 'success', 200
        except DoesNotExist:
            raise DeletingSubmissionError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def get(self, id):
        try:
            submission = Submission.objects.get(id=id).to_json()
            return Response(submission, mimetype="application/json", status=200)
        except DoesNotExist:
            raise SubmissionNotExistsError
        except Exception:
            raise InternalServerError

