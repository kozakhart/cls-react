import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from collections import defaultdict
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

def get_opic_diagnostic_grids(fromDate, toDate, language):
    description = ["Description in present time", "Description in past time", "Description in future tense", "Clarity", "Detail"]
    narration = ["Narration in present time", "Narration in past time", "Narration in future time", "Logical sequencing", "Verb forms", "Person markers"]
    situation_with_a_complication = ["Struggles, but succeeds in addressing the situation", "Attempts to address, but is unable to successfully resolve the situation", "Demonstrates no linguistic ability to address the situation", "Knowledge and use of communicative devices" ]
    advanced_grammar = ["Morphology", "Syntax", "Cases", "Prepositions", "Agreement"]
    advanced_other = ["Rate of speech", "Fluidity", "Connectedness", "Lacks strategies to compensate for weaknesses"]
    pronunciation = ["Articulation", "Pitch", "Stress", "Intonation"]
    word_order = ["Phrases", "Sentences", "Paragraphs"]
    cohesive_devices = ["Not used", "Used inaccurately", "Repetitive"]
    advanced_content = ["Lacks breadth of vocabulary", "Uses words from other languages", "Uses false cognates"]
    advanced_functions = [{'Word Order':word_order,'Cohesive Devices':cohesive_devices ,'Description':description, 'Narration':narration, 'Situation With a Complication':situation_with_a_complication, 'Advanced Grammar':advanced_grammar, 'Advanced Other':advanced_other, 'Advanced Content':advanced_content}]


    support_an_opinion = ["Present point of view clearly", "Present well organized supporting arguments", "Elaborate on arguments", "Handle the topic at the issue level (to speak outside the self)"]
    speculate_and_present_hypothesis = ["Speculate and present hypotheses", "Use grammatical constructs that signal hypothetical discourse", "Elaborate in the hypothetical mode"]
    discussion_in_extended_discourse = ["Broaden range and precision of vocabulary", "Correctly formulate high frequency compound/complex structures", "Employ a variety of cohesive devises and discourse strategies", "Increase discourse from a paragraph to extended treatment of the topic"]
    linguistically_unfamiliar_topics_or_situations = ["Broaden range and depth of precise vocabulary", "Reduce L1 or L2 interference", "Develop discourse strategies."]
    superior_grammar_accuracy = ["Agreement", "Verb formulations", "Case", "Prepositions and Prepositional phrases", "Word order (Complex/Compound Sentence)", "Dependent and Subordinate clauses"]
    other_accuracy = ["Rate", "Fluidity", "Connectedness of expression", "Increase range of sophisticated discourse strategies to compensate for weaknesses or shortcomings"]
    pronunciation = ["Articulation", "Pitch", "Stress Features", "Intonation"]
    sociolinguistic_competency = ["Size of vocabulary", "Range of topic areas", "Precision of vocabulary", "Appropriate forms for formal and informal situations"]
    superior_functions = [{'Support an Opinion':support_an_opinion}, {'Speculate and Present Hypothesis':speculate_and_present_hypothesis}, {'Discussion in Extended Discourse':discussion_in_extended_discourse}, {'Linguistically Unfamiliar Topics or Situations':linguistically_unfamiliar_topics_or_situations}, {'Superior Grammar Accuracy':superior_grammar_accuracy}, {'Other Accuracy':other_accuracy}, {'Sociolinguistic Competency':sociolinguistic_competency}, {'Pronunciation':pronunciation}]

    total_results = 0

    fromDate = datetime.strptime(fromDate, '%m/%d/%Y')
    toDate = datetime.strptime(toDate, '%m/%d/%Y')

    fromDate_str = fromDate.strftime('%m/%d/%Y')
    toDate_str = toDate.strftime('%m/%d/%Y')

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

    superior_topic_counters = {index: defaultdict(int) for index, _ in enumerate(superior_functions)}
    advanced_topic_counters = {index: defaultdict(int) for index, _ in enumerate(advanced_functions)}
    #match language
    for grid in data:

        if grid['language'] == language or language == 'All':
            total_results += 1
            for i in grid['grid']:
                
                for comment in i['gridComments']:
                    function = comment['details']
                    for index, function_dict in enumerate(superior_functions):
                        for key, value in function_dict.items():
                            if function in value:
                                superior_topic_counters[index][key] += 1
                            else:
                                superior_topic_counters[index][key] += 0

                    for index, function_dict in enumerate(advanced_functions):
                        for key, value in function_dict.items():
                            if function in value:
                                advanced_topic_counters[index][key] += 1
                            else:
                                advanced_topic_counters[index][key] += 0



    for index, counter in superior_topic_counters.items():
        function_list_name = "Function List {}".format(index + 1)
        print(f"{function_list_name}:")
        for func, count in counter.items():
            print(total_results, count)

            count = count / total_results
            counter[func] = count
            print(f"  {func}: {count}")
    for index, counter in advanced_topic_counters.items():
        function_list_name = "Function List {}".format(index + 1)
        print(f"{function_list_name}:")
        for func, count in counter.items():
            print(total_results, count)

            count = count / total_results
            counter[func] = count
            print(f"  {func}: {count}")
            
    return advanced_topic_counters, superior_topic_counters, total_results

#add main languages to the model spanish, german, 
# separate by each score, one table for AM and one for AH, give the count for each at the top
# calculation- the scale is based off of how many students there are

# next steps- need to delve into each function particulars, consultations with other departments
# fix spacing 
# same thing for OPI comments as separate tabs
# instead of program, attach csv file with netids or byuids
get_opic_diagnostic_grids('02/01/2023', "02/28/2023", 'Spanish')

