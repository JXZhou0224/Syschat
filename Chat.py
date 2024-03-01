from openai import OpenAI
import time
import os
import json
client=OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
with open("templates/system.json") as f:
    sys_prompt=json.load(f)
def sleep(sleep_time=0.1):
    time.sleep(sleep_time)

def gpt_request(gpt_call):
    sleep(2)
    try:
        completion=client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
               
                gpt_call["message"]
            ],
            temperature=0.85,
            frequency_penalty=1,
            max_tokens=gpt_call["max_tokens"]
        )
        return completion.choices[0].message.content
    except:
        print("GPT request error, retrying in 10 seconds")
        sleep(10)
        return gpt_request(gpt_call)