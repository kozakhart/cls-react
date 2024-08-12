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
    s_counter = 0


    ih_insight_counters = defaultdict(int)
    al_insight_counters = defaultdict(int)
    am_insight_counters = defaultdict(int)
    ah_insight_counters = defaultdict(int)

    ih_categorized_insight_counters = {}
    al_categorized_insight_counters = {}
    am_categorized_insight_counters = {}
    ah_categorized_insight_counters = {}
    #match language
    #with open("output.txt", "w") as file:

    for grid in data:

        if grid['language'] == language or language == 'All':
            total_results += 1
            #print(grid)
            #file.write(str(grid) + "\n")

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
                            'Content: Pronunciation': {key: ah_insight_counters[key] for key in superior_pronunciation},
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
                            'Content: Pronunciation': {key: am_insight_counters[key] for key in superior_pronunciation},
                            'Content: Sociolinguistic Competency': {key: am_insight_counters[key] for key in sociolinguistic_competency},
                            'Text Type': {key: am_insight_counters[key] for key in superior_text_type}
                        }

                    if rating == "AL":
                        for index, function_dict in enumerate(advanced_functions):
                            for key, value in function_dict.items():
                                for val in value:
                                    if val in function and grid_title == "OPIc ADVANCED DIAGNOSTIC FORM":
                                        #if val == "Grammar: Prepositions" or val == "Grammar: Agreement":

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
                            # index 0
                            # function_dict =['Description in present time', 'Description in past time', 'Description in future time', 'Clarity', 'Detail']
                            for key, value in function_dict.items():
                                # key = 'Function: Description'
                                # value = 'Description in present time'
                                for val in value:
                                    # Detail
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

    ah_counts = [d["Total Function Count"] for d in ah_data]
    am_counts = [d["Total Function Count"] for d in am_data]
    # might need to be a dictionary and assign label to values
    al_counts = [d["Total Function Count"] for d in al_data]
    ih_counts = [d["Total Function Count"] for d in ih_data]

    # Apply Min-Max Normalization
    #print('Superior Start AH')
    if ah_counts:
        ah_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in ah_data]
        ah_normalized_count_dict = {d["Function Name"]: ah_normalized_counts[i] for i, d in enumerate(ah_data)}
        ah_normalized_count_dict['Total People'] = ah_data[0]['Total People']
        ah_normalized_count_dict['Score Type'] = ah_data[0]['Score Type']
        # ah_normalized_count_dict['Number of Function Topics'] = ah_data[0]['Number of Function Topics']
        ah_normalized_count_dict['Total Function Count'] = ah_data[0]['Total Function Count']
        #print(ah_normalized_count_dict)
    else:
        ah_normalized_count_dict = {}
    #print('Superior Start AM')
    if am_counts:
        am_normalized_counts = [function_data['Total Function Count'] / (function_data['Total People'] * function_data['Number of Function Topics']) for function_data in am_data]
        am_normalized_count_dict = {d["Function Name"]: am_normalized_counts[i] for i, d in enumerate(am_data)}
        am_normalized_count_dict['Total People'] = am_data[0]['Total People']
        am_normalized_count_dict['Score Type'] = am_data[0]['Score Type']
        #am_normalized_count_dict['Number of Function Topics'] = am_data[0]['Number of Function Topics']
        am_normalized_count_dict['Total Function Count'] = am_data[0]['Total Function Count']
        #print(am_normalized_count_dict)
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
    return (ih_normalized_count_dict, al_normalized_count_dict, am_normalized_count_dict, ah_normalized_count_dict, 
            total_results, s_counter, ih_categorized_insight_counters, al_categorized_insight_counters, 
            am_categorized_insight_counters, ah_categorized_insight_counters)

# next steps- need to delve into each function particulars, consultations with other departments
# same thing for OPI comments as separate tabs
# click on something (word order) and see the other details

if __name__ == "__main__":
    get_opic_diagnostic_grids('08/09/2023', "08/09/2024", 'Spanish', [])
