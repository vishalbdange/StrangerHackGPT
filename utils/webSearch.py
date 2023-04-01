# import OS for environment variables
import json
import os

# import requests
import requests


def google_search(query_text):
    faultyText = "No results found! Please check your input once again!"
    print('>>>> Query text', query_text)
    if query_text == '':
        return faultyText
    
    url='https://customsearch.googleapis.com/customsearch/v1'
    cx='21f70c2b29d284393'
    search_key = os.environ['WEB_API_KEY']
    parameters = {
        "q" : query_text,
        "cx" : cx,
        'key' : search_key,
    }
    
    
    page=requests.request("GET",url,params=parameters)
    print('status', page.status_code)
    # Vishal made changes
    if page.status_code == 500 or page.status_code == 502 or page.status_code == 404 or page.status_code == '500' or page.status_code == '502' or page.status_code == '404':
        
        return faultyText

    if page.status_code == 429 or page.status_code == '429':
        return 'Seems that you have tried too many requests! Please try after searching after sometime!'
        
    results = json.loads(page.text)
    print('results', results)
    if len(results) == 0 or results is None or 'items' not in results:
        
        return faultyText
    # return [results['items'][3],results['items'][2],results['items'][1],results['items'][0]]
    
    top_output =  [results['items'][3],results['items'][2],results['items'][1],results['items'][0]]
    output = top_output[0]['snippet'] + '\n' + top_output[0]['link'] + '\n\n' + top_output[1]['snippet'] + '\n' + top_output[1]['link']
    return output
