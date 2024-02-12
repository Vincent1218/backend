import openai
import os
from openai import OpenAI
client = OpenAI()
openai.api_key = os.environ.get('OPENAI_API_KEY')
# 2 types of data:
# 1. Miro notes
# 2. Essay


# 4 Score Dimensions (Miro notes): 
# 1. Cognitive Advancement : ft:gpt-3.5-turbo-1106:personal::8Pup1gFD
# 2. Number of disciplines (Diversity) : ft:gpt-3.5-turbo-0613:personal::8GVMf2Ro
# 3. Disciplinary grounding : ft:gpt-3.5-turbo-0613:personal::8GXMriL2
# 4. Integration : ft:gpt-3.5-turbo-1106:personal::8K18Y2ny

# 4 Score Dimensions (Essay):
# 1. Cognitive Advancement : ft:gpt-3.5-turbo-0613:personal::8EWHfPCF
# 2. Number of disciplines (Diversity) : ft:gpt-3.5-turbo-0613:personal::8KRhSwLi
# 3. Disciplinary grounding : ft:gpt-3.5-turbo-0613:personal::8KdPJAzW
# 4. Integration : ft:gpt-3.5-turbo-1106:personal::8K18Y2ny (This is missing, so we use the same model as Miro notes)
 

system_message = '''
You are an advanced researcher that can precisely follow user's instructions.
Your mission is to evaluate the disciplinary diversity levels of students' notes.
Here are the 11 DISCIPLINE LIST: 'Arts & humanities'; 'Business & economics'; 'Clinical, pre-clinical & health'; 'Computer science'; 'Education'; 'Engineering & technology'; 'Law'; 'Life sciences'; 'Physical sciences'; 'Psychology'; 'Social sciences'.
'''
diversity_message = '''
Please evaluate the integration level of students notes, and then return ONLY numerical values "0", "1" and "2".
First,please check how many disciplines in the DISCIPLINE LIST can be found in students notes?
For example, if students talk about "COVID, hospital...", they cover "Clinical, pre-clinical & health";
if students talk about "learning, teachers, students, schooling...", they cover "Education";
if students talk about "arts, music, movies...", they cover "Arts & humanities";
if students talk about "AI technologies, cybersecurity, algrithms, chatgpt...", they cover "Computer science";
if students talk about "industry, technology, machine, robot...", they cover "Engineering & technology";
if students talk about "ip, law, legal...", they cover "Law";
if students talk about "biology...", they cover "Life sciences";
if students talk about "Mathematics and statistics, phyics and astronomy, chemistry, geology, environmental sciences, and earth and marine sciences...", they cover "Physical sciences";
if students talk about "mental health, attention...", they cover "Psychology";
if students talk about "social, goverment, communication, culture, privacy...", they cover "Social sciences";
if students talk about "economy, cost, money, income, productivity, business, market..", they cover "Business & economics",

Second, Return "2" if the content provides terminologies or knowledge or perspectives from more than 1 disciplines in the DISCIPLINE LIST.
Return "1" if the content provides terminologies or knowledge or perspectives from only 1 disciplines in the DISCIPLINE LIST.
Return "0" on all other situations (no terminologies nor knowledge nor perspectives in the DISCIPLINE LIST).
Here is the note you need to evaluate:
'''




model = ""
dimensions = ["advancement", "diversity", "grounding", "integration"]
miro_model = ["ft:gpt-3.5-turbo-1106:personal::8Pup1gFD", "ft:gpt-3.5-turbo-0613:personal::8GVMf2Ro", "ft:gpt-3.5-turbo-0613:personal::8GXMriL2", "ft:gpt-3.5-turbo-1106:personal::8K18Y2ny"]
essay_model = ["ft:gpt-3.5-turbo-0613:personal::8EWHfPCF", "ft:gpt-3.5-turbo-0613:personal::8KRhSwLi", "ft:gpt-3.5-turbo-0613:personal::8KdPJAzW", "ft:gpt-3.5-turbo-1106:personal::8K18Y2ny"]

def evaluate_annotation(context, dimensions, data_type):
    
    
    # Get model
    if data_type == "miro":
        model = miro_model
    elif data_type == "essay":
        model = essay_model
    else:
        return "Error: Invalid data type"

    # Get dimensions
    if dimensions == "advancement":
        model = model[0]
    elif dimensions == "diversity":
        model = model[1]
    elif dimensions == "grounding":
        model = model[2]
    elif dimensions == "integration":
        model = model[3]
    else:
        return "Error: Invalid dimension"


    response = client.chat.completions.create(
        model = "ft:gpt-3.5-turbo-1106:personal::8PwIJq90",
        # model = model,
        messages = context,
        max_tokens = 1,
        temperature = 0)
    return response.choices[0].message.content

def evaluate_row(row, data_type):
    # Construct context for this row
          # {"role": "system", "content": "You are an advanced researcher that can precisely follow user's instructions."},
          # {"role": "user", "content": 'Please evaluate the cognitive advancement level of students notes, and then return ONLY numerical values "0", "1" and "2".Return "2" if the content provides extended reasoning with details, mechanisms, and examples. The explanations tend to be longer than average and contain logical words such as "thus", "because", "however", and "but". Only a few annotations that meet the above-mentioned criteria can be labeled as "2". Return "1" if the content has explanations, reasons, relationships, or mechanisms mentioned without explanation in detail; or elaborations of terms, phenomena. Return "0" on all other situations. Here is the note you need to evaluate:' + str(row['note'])},
          # {"role": "assistant", "content": str(row['advancement'])}
    context = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": diversity_message + str(row)},
          ]

    # json
    score = {
      "advancement": 0,
      "diversity": 0,
      "grounding": 0,
      "integration": 0
    }

    # change name
    for dimension in dimensions:
      score.update({dimension: int(evaluate_annotation(context, dimension, data_type))})

    print("score:", score)

    return score

