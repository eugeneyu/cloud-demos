import random
import os
import requests
import json
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No"])

def llama_response(message, history):
    url = f'http://34.171.17.189:8080/generate'
    headers = {'Content-Type': 'application/json'}
    prompt = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    
    history_text = ""
    for human, ai in history:
        history_text = history_text + human + "[/INST]" + ai + "</s><s> [INST]"
    #print(history_text)

    data_str = f"""
    {{
        "inputs": "<s>[INST] <<SYS>>{prompt}<</SYS>>{history_text}{message}[/INST]",
        "parameters": {{
            "max_new_tokens": 128
        }}
    }}
    """

    print("data_str*****="+data_str)
    r = requests.post(url, headers=headers, data=data_str)
    print("r.content*****="+r.content.decode("utf-8"))

    response_json = json.loads(r.text)
    response_text = response_json["generated_text"] if response_json["generated_text"] else "No Response :("
    return response_text

demo = gr.ChatInterface(llama_response)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))
