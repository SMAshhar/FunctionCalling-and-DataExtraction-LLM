import inspect

def raven_post(payload):
    """
    Sends a payload to TGI endpoint.
    """
    
    API_URL = "http://nexusraven.nexusflow.ai"
    headers={
        "Content-Type": "application/json"
    }
    import requests
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()

def call_functioncalling_llm(prompt, api_to_call):
    """
    This finction sends a request to TGI endpoint to get Raven's function call.
    This will not generate Raven'sjustification and reasoning for the call, to save on latency.
    """
    
    signature=inspect.signature(api_to_call)
    docstring=api_to_call.__doc__
    prompt=f'''Function:\n{api_to_call.__name__}{signature}\n"""{clean_docstring(docstring)}"""\n\nUser Query:{prompt}<human_end>'''
    import requests
    output=raven_post(
        {"inputs":prompt,
         "parameters":{
             "temperature":0.001, 
             "stop":["<bot_end>"], 
             "do_simple":False, 
             "max_new_tokens":2048, 
             "return_full_text":False
             }
         }
    )
    call = output[0]["generated_text"].replace("Call:", "").strip()
    return call

def query_raven(prompt:str):
    """
    This function sends a request to TGI endpoint to get Raven's function call.
    This will not generate Raven's justification and reasoning for te call, to save on latency.
    """
    import requests
    output = raven_post({
        "inputs":prompt,
        # "parameters":{
        #     "temperature":0.001,
        #     "stop":["<bot_end>"],
        #     "do_simple":False,
        #     "max_new_tokens":2048,
        #     "return_full_text":False
        #     }
        }
    )
    
def clean_docstring(docstring):
    """
    This function removes trailing white spaces
    """
    if docstring is not None:
        docstring=docstring.strip()
        return docstring
    
def build_raven_prompt(function_list, user_query):
    import inspect
    raven_prompts=""
    for function in function_list:
        signature=inspect.signature(function)
        docstring=function.__doc__
        prompt =\
f'''
Function:
def {function.__name__}{signature}
    """
    {clean_docstring(docstring)}
    """                
'''
        raven_prompts+=prompt
    raven_prompts+=f"User Query:{user_query}<human_end>"
    return raven_prompts

