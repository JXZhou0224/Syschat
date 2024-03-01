# SysChat: a LLM-based multiagent group chat simluation
---
## 
## Running
---

to download:
```
$ git clone https://github.com/JXZhou0224/GPT-GroupChat.git
$ cd SysChat
$ pip install -r requirements.txt
```

set your openai api key:
```
In Bash:
$ export OPENAI_API_KEY=<your openai api key>

In PowerShell:
$ env:OPENAI_API_KEY=<your openai api key>
```

To test if installation succeeded:
```
$ python run.py
>>>Please Enter template name:
sim0
>>>['Alex', 'Bob', 'Charlotte', 'Dylan', 'Emma']
>>>Loading finished!
>>>Enter option:
run 1
```
If it run successfully then the installation is successful!

Here are the possible options:

`run <number>`: proceed `<number>`of chat

`save`: save all the chat history and agent state

`exit`: exit the chat without saving



## Customization
---
follow the template in `sim_5agents_template`
to customize your own Group Chat

For further customization:
You can modifiy all the prompt in `templates` to better serve your need!