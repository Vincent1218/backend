# from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
# from resources.errors import SchemaValidationError, AnalysisAlreadyExistsError, InternalServerError, \
#     UpdatingAnalysisError, DeletingAnalysisError, AnalysisNotExistsError

# import numpy as np
# import re
# import spacy
# import nltk
# from nltk.corpus import stopwords
# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('stopwords')
# nlp=spacy.load('en_core_web_sm')

# import tensorflow as tf
# import pandas as pd
# from ast import literal_eval

# from sklearn.model_selection import train_test_split

# def calculate_scores(json_body, results):
#     # Compute total number of disciplines
#     total_disciplines_array = []
#     for i in range(len(results)):
#         total_disciplines_array = total_disciplines_array + list(results[i]["disciplines"].keys())
#     total_disciplines_array = [*set(total_disciplines_array)]
#     total_num_disciplines = len(total_disciplines_array)

#     # Compute DGI Score
#     num_sections = len(results)
#     dgi_score = round(total_num_disciplines / num_sections, 3)

#     # Compute DII Score
#     sections_gt_one_manual = 0
#     for i in range(len(results)):
#         if len(results[i]["disciplines"]) > 1:
#             sections_gt_one_manual = sections_gt_one_manual + 1
#     dii_score = round(sections_gt_one_manual / num_sections, 3)

#     # Compute DEI Score
#     humanities_section_manual = 0
#     business_section_manual = 0
#     sciences_section_manual = 0
#     technology_section_manual = 0
#     for i in range(len(results)):
#         paragraph_disciplines = list(results[i]["disciplines"].keys())
#         if "humanities" in paragraph_disciplines:
#             humanities_section_manual = humanities_section_manual + 1
#         if "business" in paragraph_disciplines:
#             business_section_manual = business_section_manual + 1
#         if "sciences" in paragraph_disciplines:
#             sciences_section_manual = sciences_section_manual + 1
#         if "technology" in paragraph_disciplines:
#             technology_section_manual = technology_section_manual + 1
#     sum_sections_labeled_by_discipline = humanities_section_manual + business_section_manual + sciences_section_manual + technology_section_manual
#     summation_squared_values = (humanities_section_manual / sum_sections_labeled_by_discipline) ** 2 + (business_section_manual / sum_sections_labeled_by_discipline) ** 2 + (sciences_section_manual / sum_sections_labeled_by_discipline) ** 2 + (technology_section_manual / sum_sections_labeled_by_discipline) ** 2
#     dei_score = round(1 - summation_squared_values, 3)

#     # Adding results to json body
#     json_body['disciplines'] = total_disciplines_array

#     dgi_dict = {'finalScore': dgi_score, 'numPara': num_sections, 'numDisciplines':total_num_disciplines}
#     json_body['DGIscore'] = dgi_dict

#     dii_dict = {'finalScore': dii_score, 'numPara': num_sections, 'selectedPara': sections_gt_one_manual}
#     json_body['DIIscore'] = dii_dict

#     dei_dict = {'finalScore': dei_score, 'paraBusiness': business_section_manual, 'paraHumanities': humanities_section_manual, 'paraSciences': sciences_section_manual, 'paraTechnology': technology_section_manual, 'paraSum': sum_sections_labeled_by_discipline, 'summationVal': round(summation_squared_values, 3)}
#     json_body['DEIscore'] = dei_dict

#     return json_body


# def generate_results(input_content):
#     try:
#         # Retrieve content
#         essay_content = input_content

#         # Machine learning pipeline start ------------------------------------------------------------
#         # Prepare vectorizer ------------------------------------------------------------
#         df = pd.read_csv("resources/final_output_broad_cleaned.csv")
#         df['terms'] = df['terms'].astype(str)
#         df.drop(['ABSTRACT'], axis=1, inplace=True)
#         df.rename(columns={'ABSTRACT_CLEANED': 'ABSTRACT'}, inplace=True)

#         df = df[df['ABSTRACT'].notnull()]

#         def convertToArray(content):
#             if ',' not in content:
#                 temp_array = [content]
#                 return str(temp_array)
#             else:
#                 return str(content.split(","))

#         df['terms'] = df['terms'].apply(convertToArray)

#         # Filtering the rare terms.
#         df_shortened = df.groupby("terms").filter(lambda x: len(x) > 1)

#         # Using AST tree function to convert the strings into list structure
#         df_shortened["terms"] = df_shortened["terms"].apply(
#             lambda x: literal_eval(x))

#         # Initial train and test split.
#         extract_df, excess_df = train_test_split(
#             df_shortened,
#             test_size=0.1,
#             stratify=df_shortened["terms"].values,
#         )

#         terms = tf.ragged.constant(extract_df["terms"].values)
#         lookup = tf.keras.layers.StringLookup(output_mode="multi_hot")
#         lookup.adapt(terms) 

#         batch_size = 32

#         def create_format_df(dataframe, is_train=True):
#             labels = tf.ragged.constant(dataframe["terms"].values)
#             binary_labels = lookup(labels).numpy()
#             dataset = tf.data.Dataset.from_tensor_slices(
#                 (dataframe["ABSTRACT"].values, binary_labels)
#             )

#             if is_train:
#                 dataset = dataset.shuffle(batch_size * 10)

#             return dataset.batch(batch_size)


#         vocabulary = set()
#         extract_df["ABSTRACT"].str.lower().str.split().apply(vocabulary.update)
#         target_directory = "resources/model"
#         testing_model = tf.keras.models.load_model(target_directory)

#         # Essay paragraphs ---------------------------------------------------------------------------
#         temp_essay = essay_content.split("\n")
#         essay_paragraphs = []
#         for item in temp_essay:
#             if item != '':
#                 if len(item.split(' ')) > 10:
#                     essay_paragraphs.append(item)

#         # Essay sections ---------------------------------------------------------------------------
#         essay_sections = []
#         essay_sections.append(essay_paragraphs[0])
#         sections_index = 0

#         for para in essay_paragraphs[1:]:
#             if len(para.split()) < 50 and len(essay_sections[sections_index].split()) < 250:
#                 essay_sections[sections_index] = essay_sections[sections_index] + ' ' + para
#             else:
#                 essay_sections.append(para)
#                 sections_index = sections_index + 1

#         original_sections = essay_sections[:]

#         # Data cleaning ---------------------------------------------------------------------------
#         contraction_dict = {"can't": "cannot", "won't": "will not", "where's": "where is", "what's": "what is",
#                             "that's": "that is", "he's": "he is", "she's": "she is", "i'm": "i am",
#                             "aren't": "are not", "can't": "can not", "couldn't": "could not", "didn't": "did not",
#                             "didn’t": "did not",
#                             "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not",
#                             "haven't": "have not", "he'd": "he had", "he'll": "he will", "he's": "he is",
#                             "i'd": "i had", "i'll": "i will", "i'm": "i am", "i've": "i have",
#                             "isn't": "is not", "let's": "let us", "mightn't": "might not", "mustn't": "must not",
#                             "shan't": "shall not", "she'd": "she had", "she'll": "she will", "she's": "she is",
#                             "shouldn't": "should not", "that's": "that is", "there's": "there is",
#                             "they'd": "they had",
#                             "they'll": "they will", "they're": "they are", "they've": "they have", "we'd": "we had",
#                             "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
#                             "what're": "what are", "what's": "what is", "what've": "what have",
#                             "where's": "where is",
#                             "who'd": "who had", "who'll": "who will", "who're": "who are", "who's": "who is",
#                             "who've": "who have", "won't": "will not", "wouldn't": "would not", "you'd": "you had",
#                             "you'll": "you will", "you're": "you are", "you've": "you have", "aaaa": "bbbb",
#                             "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
#                             "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have",
#                             "it's": "it is",
#                             "ma'am": "madam", "mayn't": "may not", "aaaa": "bbbb", "aaaa": "bbbb",
#                             "needn't": "need not", "needn't've": "need not have", "o'clock": "of the clock",
#                             "oughtn't": "ought not", "oughtn't've": "ought not have", "where'd": "where did",
#                             "e.g.": "", "eg": "", "i.e.": "", "ie": "", "e.t.c.": "", "etc": ""}

#         def removeStopwords(text, stopList):
#             string = ""

#             specificStopwords = ['a', 'the']

#             for word in text.split():
#                 if word not in stopList and word not in specificStopwords:
#                     string += word + " "

#             return string

#         def cleanData(review):
#             review = str(review)
#             # case folding
#             review = review.lower()

#             # remove general contractions
#             review = re.sub(r"\'d", " would", review)
#             review = re.sub(r"\'ll", " will", review)
#             review = re.sub("\'s", " ", review)
#             review = re.sub(r"\'re", " are", review)
#             review = re.sub(r"\'ve", " have", review)

#             # remove common contractions using stored contraction dictionary
#             review = ' '.join([contraction_dict[t] if t in contraction_dict else t for t in review.split(" ")])

#             # remove characters and symbols
#             review = re.sub(r"[^a-zA-Z0-9]", " ", review)  # remove special characters
#             review = re.sub(r"[0-9]+", "", review)  # remove numbers
#             review = re.sub("(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)", "", review)  # remove single letters
#             review = review.replace('   ', ' ')  # change triple spaces to single space
#             review = review.replace('  ', ' ')  # change double spaces to single space

#             # remove stopwords
#             # stopwords of spacy
#             stoplist1 = nlp.Defaults.stop_words
#             # stopwords of NLTK
#             stoplist2 = stopwords.words('english')
#             # combining the stopword list
#             combinedStopwords = set((set(stoplist1) | set(stoplist2)))
#             review = removeStopwords(review, combinedStopwords)

#             # lemmatization
#             review = nlp(review)
#             review = " ".join([token.lemma_ for token in review])
#             review = review.replace('-PRON-', '')

#             return review

#         for i in range(len(essay_sections)):
#             essay_sections[i] = cleanData(essay_sections[i])

#         # Generating results ---------------------------------------------------------------------------
#         # For producing top 5 with probability
#         testing_essay = pd.DataFrame(columns=['ABSTRACT', 'terms'])

#         export_para = []
#         export_topics = []
#         export_proba = []

#         for i in range(len(essay_sections)):
#             testing_essay.loc[i] = [essay_sections[i]] + [str([' '])]

#         # Filtering the rare terms.
#         df_sample_filtered = testing_essay.groupby("terms").filter(lambda x: len(x) > 1)

#         df_sample_filtered["terms"] = df_sample_filtered["terms"].apply(
#             lambda x: literal_eval(x)
#         )

#         testing_dataset = create_format_df(df_sample_filtered, is_train=False)
#         content_batch, label_batch = next(iter(testing_dataset))
#         predicted_probabilities = testing_model.predict(content_batch)

#         for i, text in enumerate(content_batch):
#             export_para.append(str(text))
#             predicted_proba = [proba for proba in predicted_probabilities[i]]
#             export_proba.append(sorted(predicted_proba, reverse=True)[:5])
#             final_result = [
#                                x
#                                for _, x in sorted(
#                     zip(predicted_probabilities[i], lookup.get_vocabulary()),
#                     key=lambda pair: pair[0],
#                     reverse=True,
#                 )
#                            ][:5]

#             predicted_labels = ', '.join([label for label in final_result])
#             if len(predicted_labels) > 0:
#                 export_topics.append('(' + str(predicted_labels) + ')')
#             else:
#                 export_topics.append('()')

#         # Preparing for output data ---------------------------------------------------------------------------
#         for i in range(len(export_para)):
#             export_para[i] = export_para[i].replace("tf.Tensor(b'", '')
#             export_para[i] = export_para[i].replace("tf.Tensor(b\"", '')
#             export_para[i] = export_para[i].replace("', shape=(), dtype=string)", '')
#             export_para[i] = export_para[i].replace("\", shape=(), dtype=string)", '')

#         essay_labelled = pd.DataFrame(columns=['Paragraphs', 'Predicted Topics'])
#         for i in range(len(export_para)):
#             essay_labelled.loc[i] = [export_para[i]] + [export_topics[i]]

#         final_discipline_prob = []
#         for ind in essay_labelled.index:
#             topic_prob_tuple_array = []
#             topics_list = export_topics[ind].replace(' ', '')
#             topics_array_temp = topics_list[1:-1].split(',')
#             for i in range(len(topics_array_temp)):
#                 topic_prob_tuple_array.append((topics_array_temp[i], export_proba[ind][i]))
#             essay_labelled['Predicted Topics'][ind] = topic_prob_tuple_array
#             final_discipline_prob.append(topic_prob_tuple_array)

#         # Machine learning pipeline end -------------------------------------------------------------------------

#         output_array = []
#         for i in range(len(original_sections)):
#             temp_dict = {}
#             temp_dict["content"] = original_sections[i]
#             second_temp_dict = {}
#             for j in range(5):
#                 if final_discipline_prob[i][j][1] >= 0.3:
#                     second_temp_dict[final_discipline_prob[i][j][0]] = final_discipline_prob[i][j][1]
#             temp_dict["disciplines"] = second_temp_dict
#             output_array.append(temp_dict)

#         return output_array

#     except (FieldDoesNotExist, ValidationError):
#         raise SchemaValidationError
#     except NotUniqueError:
#         raise AnalysisAlreadyExistsError
#     except Exception as e:
#         raise InternalServerError