import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from collections import defaultdict
import csv

def get_opic_scores(firstname, lastname):
    todays_date = datetime.now()
    fromDate = todays_date.replace(year=todays_date.year - 2)
    toDate = todays_date.strftime('%m/%d/%Y')
    fromDate = fromDate.strftime('%m/%d/%Y')

    url = f'https://tms2.languagetesting.com/byuapi/opic/requestgrid'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    json_object = {

    "clientId":"394",

    "appointment":"0",

    "authCode":"BYU-787dc-ONLINE",

    "fromDate":"",

    "toDate":"",

    "firstName":"",

    "lastName":""
    }
    json_object['fromDate'] = fromDate
    json_object['toDate'] = toDate
    json_object['firstName'] = firstname
    json_object['lastName'] = lastname

    #return None
    record_response = requests.post(url, headers=headers, json=json_object)
    print(record_response.status_code)
    record_response = record_response.json()
    try:
        if record_response['Data']['errorCode'] == "103":
            return "No OPIc Scores Found"
    except:
        opic_scores = []
        for score in record_response['Data']['gridResults']:
            short_score = score['rating']
            long_score = score['ratingName']
            test_date = score['testDate']
            score_type = 'OPIc'
            opic_scores.append([score_type, short_score, long_score, test_date])
        #print(record_response)
        return opic_scores

def get_opi_scores(firstname, lastname, fromDate):
    todays_date = datetime.now()
    # fromDate = todays_date.replace(year=todays_date.year - 2)
    toDate = todays_date.strftime('%m/%d/%Y')
    # fromDate = fromDate.strftime('%m/%d/%Y')

    url = f'https://tms2.languagetesting.com/byuapi/opi/requestgrid'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    json_object = {

    "clientId":"394",

    "appointment":"0",

    "authCode":"BYU-787dc-ONLINE",

    "fromDate":"",

    "toDate":"",

    "firstName":"",

    "lastName":""
    }
    json_object['fromDate'] = fromDate
    json_object['toDate'] = toDate
    json_object['firstName'] = firstname
    json_object['lastName'] = lastname

    #return None
    record_response = requests.post(url, headers=headers, json=json_object)
    print(record_response.status_code)
    record_response = record_response.json()
    try:
        if record_response['Data']['errorCode'] == "103":
            return "No OPI Scores Found"
    except:
        opi_scores = []
        for score in record_response['Data']['gridResults']:
            short_score = score['rating']
            long_score = score['ratingName']
            test_date = score['testDate']
            score_type = 'OPI'
            opi_scores.append([score_type, short_score, long_score, test_date])
        #print(record_response)
        return short_score, opi_scores

def get_wpt_scores(firstname, lastname):
    todays_date = datetime.now()
    fromDate = todays_date.replace(year=todays_date.year - 2)
    toDate = todays_date.strftime('%m/%d/%Y')
    fromDate = fromDate.strftime('%m/%d/%Y')
    print(toDate, fromDate)

    url = f'https://tms2.languagetesting.com/byuapi/wpt/requestgrid'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    json_object = {

    "clientId":"394",

    "appointment":"0",

    "authCode":"BYU-787dc-ONLINE",

    "fromDate":"",

    "toDate":"",

    "firstName":"",

    "lastName":""
    }
    json_object['fromDate'] = fromDate
    json_object['toDate'] = toDate
    json_object['firstName'] = firstname
    json_object['lastName'] = lastname

    #return None
    record_response = requests.post(url, headers=headers, json=json_object)
    print(record_response.status_code)
    record_response = record_response.json()
    print(record_response)
    try:
        if record_response['Data']['errorCode'] == "103":
            return "No WPT Scores Found"
    except:
        wpt_scores = []
        for score in record_response['Data']['gridResults']:
            short_score = score['rating']
            long_score = score['ratingName']
            test_date = score['testDate']
            score_type = 'WPT'
            wpt_scores.append([score_type, short_score, long_score, test_date])
        #print(record_response)
        return wpt_scores

def get_opi_grid(firstname, lastname, fromDate):
    todays_date = datetime.now()
    toDate = todays_date.strftime('%m/%d/%Y')

    url = f'https://tms2.languagetesting.com/byuapi/opi/requestgrid'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    json_object = {

    "clientId":"394",

    "appointment":"0",

    "authCode":"BYU-787dc-ONLINE",

    "fromDate":"",

    "toDate":"",

    "firstName":"",

    "lastName":""
    }
    json_object['fromDate'] = fromDate
    json_object['toDate'] = toDate
    json_object['firstName'] = firstname
    json_object['lastName'] = lastname

    #return None
    record_response = requests.post(url, headers=headers, json=json_object, verify=False)
    print(record_response.status_code)
    print('hello')
    record_response = record_response.json()
    return record_response

# print(get_opi_grid('Rachel', '', '01/01/2023'))

def get_opic_diagnostic_grids(fromDate, toDate, language, csv_file):
    #nh, nm, nl
    intermediate_create_w_language = ["Increase vocabulary to be able to provide personal information", "Improve listening comprehension in order to respond to requests for information", "Produce sentence level discourse and not just lists and phrases"]
    intermediate_ask_and_answer_questions = ["Formulate questions correctly", "Produce enough questions and responses to complete the transaction"]
    intermediate_text_type = ["Words, lists of words and memorized phrases", "Some sentences, memorized phrases and words", "Mostly sentences, but sometimes just memorized phrases and lists of words"]
    intermediate_fluency = ["Rate of speech", "Fluidity (reduce pauses)", """Reduce "dead ending"(incomplete statements)""", "Reduce false-starts", 
                            "Reduce repetition"]
    intermediate_pronunciation = ["Rate of Speech", "Fluidity (reduce pauses)", "Reduce 'dead ending' (incomplete statements)",
            "Reduce false-starts", "Reduce repetition"]
    intermediate_structure = ["Needs control of simple sentence level grammar",
            "Needs to create complete sentences", "Needs to improve sentence level word order"]

    intermediate_functions=[
        {"Function: Create with Language":intermediate_create_w_language},
        {"Function: Ask and Answer Questions":intermediate_ask_and_answer_questions},
        {"Accuracy: Fluency":intermediate_fluency},
        {"Accuracy: Pronunciation":intermediate_pronunciation},
        {"Accuracy: Structure":intermediate_structure},
        {"Text Type":intermediate_text_type},
    ]

    #add im and 
    description = ["Description in present time", "Description in past time", "Description in future time", "Clarity", "Detail"]
    narration = ["Narration in present time", "Narration in past time", "Narration in future time", "Logical sequencing", "Verb forms", "Person markers"]
    situation_with_a_complication = ["Struggles,but succeeds in addressing the situation", 
                                     "Attempts to address, but is unable to successfully resolve the situation", 
                                     "Demonstrates no linguistic ability to address the situations", 
                                     "Knowledge and use of communicative devices"]
    # for whatever reason "Struggles,but succeeds in addressing the situation" should not have a space after the comma
    advanced_grammar = ["Grammar: Morphology", "Grammar: Syntax", "Grammar: Cases", "Grammar: Prepositions", "Grammar: Agreement"]
    advanced_other = ["Rate of speech", "Fluidity", "Connectedness", "Lacks strategies to compensate for weaknesses"]
    advanced_pronunciation = ["Articulation", "Pitch", "Stress", "Intonation"]
    word_order = ["Phrases", "Sentences", "Paragraphs"]
    cohesive_devices = ["Not used", "Used inaccurately", "Repetitive"]
    advanced_content = ["Lacks breadth of vocabulary", "Uses words from other languages", "Uses false cognates"]
    # Anything from content has a placeholder on physical grid, but nothing is ever recorded there. I checked years of data from the api and nothing shows for content. I believe they do not record that data.
    advanced_text_type = ["Words and phrases", "Sentences", "Strings of sentences", "Connected sentences", "Skeletal paragraphs"]
    advanced_functions = [
        {"Function: Description":description}, 
        {"Function: Narration":narration}, 
        {"Function: Situation With a Complication":situation_with_a_complication}, 
        {"Accuracy: Grammar":advanced_grammar}, 
        {"Accuracy: Pronunciation":advanced_pronunciation}, 
        {"Accuracy: Other":advanced_other}, 
        {"Content":advanced_content}, 
        {"Text Type: Word Order":word_order}, 
        {"Text Type: Cohesive Devices":cohesive_devices}, 
        {"Text Type":advanced_text_type}
        ]

    support_an_opinion = ["Present point of view clearly", "Present well organized supporting arguments", "Elaborate on arguments", 
                          "Handle the topic at the issue level (to speak outside the self)"]
    speculate_and_present_hypothesis = ["Speculate and present hypotheses", "Use grammatical constructs that signal hypothetical discourse", 
                                        "Elaborate in the hypothetical mode"]
    discussion_in_extended_discourse = ["Broaden range and precision of vocabulary", "Correctly formulate high frequency compound/complex structures", 
                                        "Employ a variety of cohesive devises and discourse strategies", 
                                        "Increase discourse from a paragraph to extended treatment of the topic"]
    linguistically_unfamiliar_topics_or_situations = ["Broaden range and depth of precise vocabulary", "Reduce L1 or L2 interference", 
                                                      "Develop discourse strategies"]
    superior_grammar_accuracy = ["Agreement", "Verb formulations", "Case", "Prepositions and Prepositional phrases", 
                                "Word order (Complex/Compound Sentence)", "Dependent and Subordinate clauses"]
    other_accuracy = ["Rate of speech", "Fluidity", "Connectedness of expression", 
                    "Increase range of sophisticated discourse strategies to compensate for weaknesses or shortcomings"]

    superior_pronunciation = ["Articulation", "Pitch", "Stress features", "Intonation"]
    sociolinguistic_competency = ["Size of vocabulary", "Range of topic areas", "Precision of vocabulary", "Appropriate forms for formal and informal situations"]
    superior_text_type = []
    # not present on grids
    superior_functions = [
        {"Function: Support an Opinion":support_an_opinion}, 
        {"Function: Speculate and Present Hypothesis":speculate_and_present_hypothesis}, 
        {"Function: Discussion in Extended Discourse":discussion_in_extended_discourse}, 
        {"Function: Linguistically Unfamiliar Topics or Situations":linguistically_unfamiliar_topics_or_situations}, 
        {"Accuracy: Grammar":superior_grammar_accuracy}, 
        {"Accuracy: Pronunciation":superior_pronunciation}, 
        {"Accuracy: Other":other_accuracy}, 
        {"Content: Sociolinguistic Competency":sociolinguistic_competency}, 
        {"Text Type":superior_text_type}
        ]

    total_results = 0

    fromDate = datetime.strptime(fromDate, '%m/%d/%Y')
    toDate = datetime.strptime(toDate, '%m/%d/%Y')
    fromDate_str = fromDate.strftime('%m/%d/%Y')
    toDate_str = toDate.strftime('%m/%d/%Y')

    # for row in csv file, first column = first name, last column = last name
    url = f'https://tms2.languagetesting.com/byuapi/opic/requestgrid'
    headers= CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    json_object = {

    "clientId":"394",

    "appointment":"0",

    "authCode":"BYU-787dc-ONLINE",

    "fromDate":"",

    "toDate":"",

    "firstName":"",

    "lastName":""
    }
    json_object['fromDate'] = fromDate_str
    json_object['toDate'] = toDate_str

    #return None
    record_response = requests.post(url, headers=headers, json=json_object, verify=False)
    print(record_response.status_code)
    record_response = record_response.json()

    data = record_response['Data']['gridResults']
    csv_candidate_names = set()

    if csv_file:
        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())

        next(reader) 
        for row in reader:
            if row:
                firstName = row[0]
                lastName = row[-1]
                candidateName = f"{firstName} {lastName}"
                csv_candidate_names.add(candidateName) 
        print(len(csv_candidate_names))  
        data = [record for record in data if record['candidateName'] in csv_candidate_names]
    

    ah_superior_topic_counters = {index: defaultdict(int) for index, _ in enumerate(superior_functions)}
    ah_counter = 0
    am_superior_topic_counters = {index: defaultdict(int) for index, _ in enumerate(superior_functions)}
    am_counter  = 0
    al_advanced_topic_counters = {index: defaultdict(int) for index, _ in enumerate(advanced_functions)}
    al_counter = 0
    ih_advanced_topic_counters = {index: defaultdict(int) for index, _ in enumerate(advanced_functions)}
    ih_counter = 0
    im_advanced_topic_counters = {index: defaultdict(int) for index, _ in enumerate(advanced_functions)}
    im_counter = 0
    il_advanced_topic_counters = {index: defaultdict(int) for index, _ in enumerate(advanced_functions)}
    il_counter = 0
    nh_intermediate_topic_counters = {index: defaultdict(int) for index, _ in enumerate(intermediate_functions)}
    nh_counter = 0
    nm_intermediate_topic_counters = {index: defaultdict(int) for index, _ in enumerate(intermediate_functions)}
    nm_counter = 0
    nl_intermediate_topic_counters = {index: defaultdict(int) for index, _ in enumerate(intermediate_functions)}
    nl_counter = 0
    s_counter = 0

    nl_insight_counters = defaultdict(int)
    nm_insight_counters = defaultdict(int)
    nh_insight_counters = defaultdict(int)
    il_insight_counters = defaultdict(int)
    im_insight_counters = defaultdict(int)
    ih_insight_counters = defaultdict(int)
    al_insight_counters = defaultdict(int)
    am_insight_counters = defaultdict(int)
    ah_insight_counters = defaultdict(int)

    nl_categorized_insight_counters = {}
    nm_categorized_insight_counters = {}
    nh_categorized_insight_counters = {}
    il_categorized_insight_counters = {}
    im_categorized_insight_counters = {}
    ih_categorized_insight_counters = {}
    al_categorized_insight_counters = {}
    am_categorized_insight_counters = {}
    ah_categorized_insight_counters = {}
    #match language
    with open("output.txt", "w") as file:

        for grid in data:

            if grid['language'] == language or language == 'All':
                total_results += 1
                #print(grid)
                file.write(str(grid) + "\n")

                rating = grid['rating']

                if rating == "S":
                    s_counter += 1
                if rating == "AH":
                    ah_counter += 1
                if rating == "AM":
                    am_counter += 1
                if rating == "AL":
                    al_counter += 1
                if rating == "IH":
                    ih_counter += 1
                if rating == "IM":
                    im_counter += 1
                if rating == "IL":
                    il_counter += 1
                if rating == "NH":
                    nh_counter += 1
                if rating == "NM":
                    nm_counter += 1
                if rating == "NL":
                    nl_counter += 1

                for i in grid['grid']:
                    for comment in i['gridComments']:
                        function = comment['details']
                        grid_title = comment['title']
                        if rating == "AH":
                            for index, function_dict in enumerate(superior_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc SUPERIOR DIAGNOSTIC GRID":
                                            ah_superior_topic_counters[index][key] += 1
                                            ah_insight_counters[val] += 1
                        
                            ah_categorized_insight_counters = {
                                'Function: Support an Opinion': {key: ah_insight_counters[key] for key in support_an_opinion},
                                'Function: Speculate and Present Hypothesis': {key: ah_insight_counters[key] for key in speculate_and_present_hypothesis},
                                'Function: Discussion in Extended Discourse': {key: ah_insight_counters[key] for key in discussion_in_extended_discourse},
                                'Function: Linguistically Unfamiliar Topics or Situations': {key: ah_insight_counters[key] for key in linguistically_unfamiliar_topics_or_situations},
                                'Accuracy: Grammar': {key: ah_insight_counters[key] for key in superior_grammar_accuracy},
                                'Accuracy: Other': {key: ah_insight_counters[key] for key in other_accuracy},
                                'Accuracy: Pronunciation': {key: ah_insight_counters[key] for key in superior_pronunciation},
                                'Content: Sociolinguistic Competency': {key: ah_insight_counters[key] for key in sociolinguistic_competency},
                                'Text Type': {key: ah_insight_counters[key] for key in superior_text_type}
                            }
                        if rating == "AM":
                            for index, function_dict in enumerate(superior_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc SUPERIOR DIAGNOSTIC GRID":
                                            am_superior_topic_counters[index][key] += 1
                                            am_insight_counters[val] += 1
                    
                            am_categorized_insight_counters = {
                                'Function: Support an Opinion': {key: am_insight_counters[key] for key in support_an_opinion},
                                'Function: Speculate and Present Hypothesis': {key: am_insight_counters[key] for key in speculate_and_present_hypothesis},
                                'Function: Discussion in Extended Discourse': {key: am_insight_counters[key] for key in discussion_in_extended_discourse},
                                'Function: Linguistically Unfamiliar Topics or Situations': {key: am_insight_counters[key] for key in linguistically_unfamiliar_topics_or_situations},
                                'Accuracy: Grammar': {key: am_insight_counters[key] for key in superior_grammar_accuracy},
                                'Accuracy: Other': {key: am_insight_counters[key] for key in other_accuracy},
                                'Accuracy: Pronunciation': {key: am_insight_counters[key] for key in superior_pronunciation},
                                'Content: Sociolinguistic Competency': {key: am_insight_counters[key] for key in sociolinguistic_competency},
                                'Text Type': {key: am_insight_counters[key] for key in superior_text_type}
                            }

                        if rating == "AL":
                            for index, function_dict in enumerate(advanced_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc ADVANCED DIAGNOSTIC FORM":
                                            al_advanced_topic_counters[index][key] += 1
                                            al_insight_counters[val] += 1
                    
                            al_categorized_insight_counters = {
                                'Accuracy: Other': {key: al_insight_counters[key] for key in advanced_other},
                                'Accuracy: Pronunciation': {key: al_insight_counters[key] for key in advanced_pronunciation},
                                'Text Type: Word Order': {key: al_insight_counters[key] for key in word_order},
                                'Text Type: Cohesive Devices': {key: al_insight_counters[key] for key in cohesive_devices},
                                'Content': {key: al_insight_counters[key] for key in advanced_content},
                                'Text Type': {key: al_insight_counters[key] for key in advanced_text_type},
                                'Accuracy: Grammar': {key: al_insight_counters[key] for key in advanced_grammar},
                                'Function: Situation With a Complication': {key: al_insight_counters[key] for key in situation_with_a_complication},
                                'Function: Narration': {key: al_insight_counters[key] for key in narration},
                                'Function: Description': {key: al_insight_counters[key] for key in description}
                            }
                        if rating == "IH":
                            for index, function_dict in enumerate(advanced_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc ADVANCED DIAGNOSTIC FORM": 
                                            ih_advanced_topic_counters[index][key] += 1
                                            ih_insight_counters[val] += 1
            

                            ih_categorized_insight_counters = {
                                'Accuracy: Other': {key: ih_insight_counters[key] for key in advanced_other},
                                'Accuracy: Pronunciation': {key: ih_insight_counters[key] for key in advanced_pronunciation},
                                'Text Type: Word Order': {key: ih_insight_counters[key] for key in word_order},
                                'Text Type: Cohesive Devices': {key: ih_insight_counters[key] for key in cohesive_devices},
                                'Content': {key: ih_insight_counters[key] for key in advanced_content},
                                'Text Type': {key: ih_insight_counters[key] for key in advanced_text_type},
                                'Accuracy: Grammar': {key: ih_insight_counters[key] for key in advanced_grammar},
                                'Function: Situation With a Complication': {key: ih_insight_counters[key] for key in situation_with_a_complication},
                                'Function: Narration': {key: ih_insight_counters[key] for key in narration},
                                'Function: Description': {key: ih_insight_counters[key] for key in description}
                            }
                        if rating == "IM":
                            for index, function_dict in enumerate(advanced_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc ADVANCED DIAGNOSTIC FORM":
                                            im_advanced_topic_counters[index][key] += 1
                                            im_insight_counters[val] += 1
                            im_categorized_insight_counters = {
                                'Accuracy: Other': {key: im_insight_counters[key] for key in advanced_other},
                                'Accuracy: Pronunciation': {key: im_insight_counters[key] for key in advanced_pronunciation},
                                'Text Type: Word Order': {key: im_insight_counters[key] for key in word_order},
                                'Text Type: Cohesive Devices': {key: im_insight_counters[key] for key in cohesive_devices},
                                'Content': {key: im_insight_counters[key] for key in advanced_content},
                                'Text Type': {key: im_insight_counters[key] for key in advanced_text_type},
                                'Accuracy: Grammar': {key: im_insight_counters[key] for key in advanced_grammar},
                                'Function: Situation With a Complication': {key: im_insight_counters[key] for key in situation_with_a_complication},
                                'Function: Narration': {key: im_insight_counters[key] for key in narration},
                                'Function: Description': {key: im_insight_counters[key] for key in description}
                            }
                        if rating == "IL":
                            for index, function_dict in enumerate(advanced_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc ADVANCED DIAGNOSTIC FORM":
                                            il_advanced_topic_counters[index][key] += 1
                                            il_insight_counters[val] += 1
                            il_categorized_insight_counters = {
                                'Accuracy: Other': {key: il_insight_counters[key] for key in advanced_other},
                                'Accuracy: Pronunciation': {key: il_insight_counters[key] for key in advanced_pronunciation},
                                'Text Type: Word Order': {key: il_insight_counters[key] for key in word_order},
                                'Text Type: Cohesive Devices': {key: il_insight_counters[key] for key in cohesive_devices},
                                'Content': {key: il_insight_counters[key] for key in advanced_content},
                                'Text Type': {key: il_insight_counters[key] for key in advanced_text_type},
                                'Accuracy: Grammar': {key: il_insight_counters[key] for key in advanced_grammar},
                                'Function: Situation With a Complication': {key: il_insight_counters[key] for key in situation_with_a_complication},
                                'Function: Narration': {key: il_insight_counters[key] for key in narration},
                                'Function: Description': {key: il_insight_counters[key] for key in description}
                            }
                        if rating == "NH":
                            for index, function_dict in enumerate(intermediate_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc INTERMEDIATE DIAGNOSTIC GRID":
                                            nh_intermediate_topic_counters[index][key] += 1
                                            nh_insight_counters[val] += 1
                            nh_categorized_insight_counters = {
                                'Function: Create with Language': {key: nh_insight_counters[key] for key in intermediate_create_w_language},
                                'Function: Ask and Answer Questions': {key: nh_insight_counters[key] for key in intermediate_ask_and_answer_questions},
                                'Accuracy: Fluency': {key: nh_insight_counters[key] for key in intermediate_fluency},
                                'Accuracy: Pronunciation': {key: nh_insight_counters[key] for key in intermediate_pronunciation},
                                'Accuracy: Structure': {key: nh_insight_counters[key] for key in intermediate_structure},
                                'Text Type': {key: nh_insight_counters[key] for key in intermediate_text_type}
                            }
                        if rating == "NM":
                            for index, function_dict in enumerate(intermediate_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc INTERMEDIATE DIAGNOSTIC GRID":
                                            nm_intermediate_topic_counters[index][key] += 1
                                            nm_insight_counters[val] += 1
                            nm_categorized_insight_counters = {
                                'Function: Create with Language': {key: nm_insight_counters[key] for key in intermediate_create_w_language},
                                'Function: Ask and Answer Questions': {key: nm_insight_counters[key] for key in intermediate_ask_and_answer_questions},
                                'Accuracy: Fluency': {key: nm_insight_counters[key] for key in intermediate_fluency},
                                'Accuracy: Pronunciation': {key: nm_insight_counters[key] for key in intermediate_pronunciation},
                                'Accuracy: Structure': {key: nm_insight_counters[key] for key in intermediate_structure},
                                'Text Type': {key: nm_insight_counters[key] for key in intermediate_text_type}
                            }
                        if rating == "NL":
                            for index, function_dict in enumerate(intermediate_functions):
                                for key, value in function_dict.items():
                                    for val in value:
                                        if val in function and grid_title == "OPIc INTERMEDIATE DIAGNOSTIC GRID":
                                            nl_intermediate_topic_counters[index][key] += 1
                                            nl_insight_counters[val] += 1
                            nl_categorized_insight_counters = {
                                'Function: Create with Language': {key: nl_insight_counters[key] for key in intermediate_create_w_language},
                                'Function: Ask and Answer Questions': {key: nl_insight_counters[key] for key in intermediate_ask_and_answer_questions},
                                'Accuracy: Fluency': {key: nl_insight_counters[key] for key in intermediate_fluency},
                                'Accuracy: Pronunciation': {key: nl_insight_counters[key] for key in intermediate_pronunciation},
                                'Accuracy: Structure': {key: nl_insight_counters[key] for key in intermediate_structure},
                                'Text Type': {key: nl_insight_counters[key] for key in intermediate_text_type}
                            }
        
        ah_data = []
        for index, counter in ah_superior_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            #print(f"{function_list_name}:")
            for func, count in counter.items():
                topics_dict = next((d for d in superior_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    #print(f"Total people= {ah_counter}, Total Function Count= {count}, Function Name= {func}, Number of Function Topics= {num_topics}")
                    ah_data.append({"Score Type": "AH", "Function Name": func, "Total People": ah_counter, "Total Function Count": count, "Number of Function Topics": num_topics})

        am_data = []
        for index, counter in am_superior_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            #print(f"{function_list_name}:")
            for func, count in counter.items():
                topics_dict = next((d for d in superior_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    #print(f"Total people= {am_counter}, Total Function Count= {count}, Function Name= {func}, Number of Function Topics= {num_topics}")
                    am_data.append({"Score Type": "AM", "Function Name": func,  "Total People": am_counter, "Total Function Count": count, "Number of Function Topics": num_topics})
        print('hello')
        al_data = []
        for index, counter in al_advanced_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            #print(f"{function_list_name}:")
            for func, count in counter.items():
                topics_dict = next((d for d in advanced_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    #print(f"Total people= {al_counter}, Total Function Count= {count}, Function Name= {func}, Number of Function Topics= {num_topics}")
                    al_data.append({"Score Type": "AL", "Function Name": func,  "Total People": al_counter, "Total Function Count": count, "Number of Function Topics": num_topics})
        # it is appending to al_data
        ih_data = []
        for index, counter in ih_advanced_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            #print(f"{function_list_name}:")
            for func, count in counter.items():
                topics_dict = next((d for d in advanced_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    #print(f"Total people= {ih_counter}, Total Function Count= {count}, Function Name= {func}, Number of Function Topics= {num_topics}")
                    ih_data.append({"Score Type": "IH", "Function Name": func,  "Total People": ih_counter, "Total Function Count": count, "Number of Function Topics": num_topics})
                # print(f"  {func}: {count}")

        im_data = []
        for index, counter in im_advanced_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            for func, count in counter.items():
                topics_dict = next((d for d in advanced_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    im_data.append({"Score Type": "IM", "Function Name": func,  "Total People": im_counter, "Total Function Count": count, "Number of Function Topics": num_topics})
        
        il_data = []
        for index, counter in il_advanced_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            for func, count in counter.items():
                topics_dict = next((d for d in advanced_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    il_data.append({"Score Type": "IL", "Function Name": func,  "Total People": il_counter, "Total Function Count": count, "Number of Function Topics": num_topics})

        nh_data = []
        for index, counter in nh_intermediate_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            for func, count in counter.items():
                topics_dict = next((d for d in intermediate_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    nh_data.append({"Score Type": "NH", "Function Name": func,  "Total People": nh_counter, "Total Function Count": count, "Number of Function Topics": num_topics})

        nm_data = []
        for index, counter in nm_intermediate_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            for func, count in counter.items():
                topics_dict = next((d for d in intermediate_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    nm_data.append({"Score Type": "NM", "Function Name": func,  "Total People": nm_counter, "Total Function Count": count, "Number of Function Topics": num_topics})

        nl_data = []
        for index, counter in nl_intermediate_topic_counters.items():
            function_list_name = "Function List {}".format(index + 1)
            for func, count in counter.items():
                topics_dict = next((d for d in intermediate_functions if func in d), None)
                if topics_dict:
                    num_topics = len(topics_dict[func])
                    nl_data.append({"Score Type": "NL", "Function Name": func,  "Total People": nl_counter, "Total Function Count": count, "Number of Function Topics": num_topics})

        ah_counts = [d["Total Function Count"] for d in ah_data]
        am_counts = [d["Total Function Count"] for d in am_data]
        # might need to be a dictionary and assign label to values
        al_counts = [d["Total Function Count"] for d in al_data]
        ih_counts = [d["Total Function Count"] for d in ih_data]
        im_counts = [d["Total Function Count"] for d in im_data]
        il_counts = [d["Total Function Count"] for d in il_data]
        nh_counts = [d["Total Function Count"] for d in nh_data]
        nm_counts = [d["Total Function Count"] for d in nm_data]
        nl_counts = [d["Total Function Count"] for d in nl_data]

        # the equation is total functions found / (total people * number of function topics)
        # the denominator is the max total functions that could be found
        # the numerator is the total functions actually found
        if ah_counts:
            ah_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in ah_data]
            ah_normalized_count_dict = {d["Function Name"]: ah_normalized_counts[i] for i, d in enumerate(ah_data)}
            ah_normalized_count_dict['Total People'] = ah_data[0]['Total People']
            ah_normalized_count_dict['Score Type'] = ah_data[0]['Score Type']
            ah_normalized_count_dict['Total Function Count'] = ah_data[0]['Total Function Count']
        else:
            ah_normalized_count_dict = {}
        if am_counts:
            am_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in am_data]
            am_normalized_count_dict = {d["Function Name"]: am_normalized_counts[i] for i, d in enumerate(am_data)}
            am_normalized_count_dict['Total People'] = am_data[0]['Total People']
            am_normalized_count_dict['Score Type'] = am_data[0]['Score Type']
            am_normalized_count_dict['Total Function Count'] = am_data[0]['Total Function Count']
        else:
            am_normalized_count_dict = {}

        print('Advanced Start AL')
        if al_counts:
            al_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in al_data]

            al_normalized_count_dict = {d["Function Name"]: al_normalized_counts[i] for i, d in enumerate(al_data)}
            al_normalized_count_dict['Total People'] = al_data[0]['Total People']
            al_normalized_count_dict['Score Type'] = al_data[0]['Score Type']
            # al_normalized_count_dict['Number of Function Topics'] = al_data[0]['Number of Function Topics']
            al_normalized_count_dict['Total Function Count'] = al_data[0]['Total Function Count']
            print(al_normalized_count_dict)
        else:
            al_normalized_count_dict = {}

        #print('Advanced Start IH')
        if ih_counts:
            ih_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in ih_data]
            ih_normalized_count_dict = {d["Function Name"]: ih_normalized_counts[i] for i, d in enumerate(ih_data)}
            ih_normalized_count_dict['Total People'] = ih_data[0]['Total People']
            ih_normalized_count_dict['Score Type'] = ih_data[0]['Score Type']
            # ih_normalized_count_dict['Number of Function Topics'] = ih_data[0]['Number of Function Topics']
            ih_normalized_count_dict['Total Function Count'] = ih_data[0]['Total Function Count']
            #print(ih_normalized_count_dict)
        else:
            ih_normalized_count_dict = {}

        if im_counts:
            im_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in im_data]
            im_normalized_count_dict = {d["Function Name"]: im_normalized_counts[i] for i, d in enumerate(im_data)}
            im_normalized_count_dict['Total People'] = im_data[0]['Total People']
            im_normalized_count_dict['Score Type'] = im_data[0]['Score Type']
            im_normalized_count_dict['Total Function Count'] = im_data[0]['Total Function Count']
        else:
            im_normalized_count_dict = {}

        if il_counts:
            il_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in il_data]
            il_normalized_count_dict = {d["Function Name"]: il_normalized_counts[i] for i, d in enumerate(il_data)}
            il_normalized_count_dict['Total People'] = il_data[0]['Total People']
            il_normalized_count_dict['Score Type'] = il_data[0]['Score Type']
            il_normalized_count_dict['Total Function Count'] = il_data[0]['Total Function Count']
        else:
            il_normalized_count_dict = {}
        
        if nh_counts:
            nh_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in nh_data]
            nh_normalized_count_dict = {d["Function Name"]: nh_normalized_counts[i] for i, d in enumerate(nh_data)}
            nh_normalized_count_dict['Total People'] = nh_data[0]['Total People']
            nh_normalized_count_dict['Score Type'] = nh_data[0]['Score Type']
            nh_normalized_count_dict['Total Function Count'] = nh_data[0]['Total Function Count']
        else:
            nh_normalized_count_dict = {}

        if nm_counts:
            nm_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in nm_data]
            nm_normalized_count_dict = {d["Function Name"]: nm_normalized_counts[i] for i, d in enumerate(nm_data)}
            nm_normalized_count_dict['Total People'] = nm_data[0]['Total People']
            nm_normalized_count_dict['Score Type'] = nm_data[0]['Score Type']
            nm_normalized_count_dict['Total Function Count'] = nm_data[0]['Total Function Count']
        else:
            nm_normalized_count_dict = {}

        if nl_counts:
            nl_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in nl_data]
            nl_normalized_count_dict = {d["Function Name"]: nl_normalized_counts[i] for i, d in enumerate(nl_data)}
            nl_normalized_count_dict['Total People'] = nl_data[0]['Total People']
            nl_normalized_count_dict['Score Type'] = nl_data[0]['Score Type']
            nl_normalized_count_dict['Total Function Count'] = nl_data[0]['Total Function Count']
        else:
            nl_normalized_count_dict = {}

    return (
            nl_normalized_count_dict, nm_normalized_count_dict, nh_normalized_count_dict,
            il_normalized_count_dict, im_normalized_count_dict, ih_normalized_count_dict,
            al_normalized_count_dict, am_normalized_count_dict, ah_normalized_count_dict, 
            nl_categorized_insight_counters, nm_categorized_insight_counters, nh_categorized_insight_counters,
            il_categorized_insight_counters, im_categorized_insight_counters, ih_categorized_insight_counters,
            al_categorized_insight_counters, am_categorized_insight_counters, ah_categorized_insight_counters,
            total_results, s_counter
            )

# next steps- need to delve into each function particulars, consultations with other departments
# same thing for OPI comments as separate tabs
# click on something (word order) and see the other details

if __name__ == "__main__":
    get_opic_diagnostic_grids('05/01/2024', "09/01/2024", 'All', [])
