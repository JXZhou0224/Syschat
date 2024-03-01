import openai
import Chat
import json

class Agent():
    '''
    a template for agents
    speak()  talk from history
    reflect()  reflect base on history
    get_will() reply agent's will to speak
    '''
    def __init__(self,file,agents):
        '''
        initialize the agent from a dict
        config: dict initial settings for an agent
        agents: list of agents
        '''
        self.directory=file
        with open(f"{file}/meta.json") as f:
            self.config=json.load(f)
        self.agents=[i for i in agents]
        self.agents.remove(self.config["name"])
        '''
        initalize opinion and knowledge according to agent list
        '''
        if self.config["opinion"] == {}:
            for agent in self.agents:
                if not(agent in self.config["opinion"]):
                    self.config["opinion"][agent]="Not familiar"

        if self.config["knowledge"] == {}:
            for agent in self.agents:
                if not(agent in self.config["knowledge"]):
                    self.config["knowledge"][agent]="Not familiar"
    
    def name(self):
        return self.config["name"]
    
    def speak(self,History):
        
        with open("templates/speak.json") as f:
            template=json.load(f)
        template["message"]["content"]=template["message"]["content"].format(self.config["name"],
                                                                             self.config["inner"],
                                                                             self.config["emo_state"],
                                                                             self.config["knowledge"],
                                                                             self.config["opinion"],
                                                                             History)
        rep=Chat.gpt_request(template)
        return rep
    
    def format_out(self,sp_token):
        output_format='{'
        for agent in self.agents:
            output_format+=f"\"{agent}\": {sp_token},"
        output_format=output_format[0:-1]+"}"
        return output_format
    
    def get_will(self,History):
        with open("templates/will.json") as f:
            template=json.load(f)
        template['message']['content']=template['message']['content'].format(self.config["name"],
                                                                            self.config["inner"],
                                                                            self.config["knowledge"],
                                                                            self.config["opinion"],
                                                                            History,
                                                                            self.config["emo_state"])
        return int(Chat.gpt_request(template))
        
    
    def reflect(self,History):
        sp_token="<string object: knowledge about the person>"
        output_format=self.format_out(sp_token)
        with open("templates/reflect_know.json") as f:
            template=json.load(f)
        template['message']['content']=template['message']['content'].format(self.config["name"],
                                                                            self.config["inner"],
                                                                            self.config["emo_state"],
                                                                            self.config["knowledge"],
                                                                            self.config["opinion"],
                                                                            History,
                                                                            output_format)
        
        self.config["knowledge"]=json.loads(Chat.gpt_request(template))
        
        
        
        output_format=self.format_out("<string object: opinion about the person>")
        with open("templates/reflect_opinion.json") as f:
            template=json.load(f)
        template['message']['content']=template['message']['content'].format(self.config["name"],
                                                                            self.config["inner"],
                                                                            self.config["emo_state"],
                                                                            self.config["knowledge"],
                                                                            self.config["opinion"],
                                                                            History,
                                                                            output_format)
        self.config["opinion"]=json.loads(Chat.gpt_request(template))

        
        with open("templates/reflect_emo.json") as f:
            template=json.load(f)
        emo_temp="{\"emo_state\": <a str description your current emotional state>}"
        template['message']['content']=template['message']['content'].format(self.config["name"],
                                                                            self.config["inner"],
                                                                            self.config["emo_state"],
                                                                            self.config["knowledge"],
                                                                            self.config["opinion"],
                                                                            History,
                                                                            emo_temp)
        self.config["emo_state"]=json.loads(Chat.gpt_request(template))["emo_state"]
        
        print(self.config)

        
    def save_state(self):
        with open(f"{self.directory}/meta.json","w+") as f:
            f.write(json.dumps(self.config,indent=2))
    
            
          
          
# alex=Agent("D:/SysChat/simulation/agents/Alex",["Alex","Bob","Charlotte"])
# print(alex.config)
# History=[{"speaker":"Bob","message":"I really don't like alex, she is so boring and weird."},
#             {"speaker":"Charlotte","message":"I agree, she is the worst"}]

# temp=alex.speak(History)
# print(temp)

# History.append({"speaker": "Alex","message":alex.speak(History)})
# alex.reflect(History)
# print(alex.config)