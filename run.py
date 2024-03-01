import sys
import openai
from agent_template import Agent
import json
import os
REFLECTION_INTERVAL=5
HISTORY_FOR_CHAT=5

def update_will(agents,History,will):
    print("updating will\n"+"-"*15)
    for agent in agents:
        print("generating will for "+agent)
        will[agent]+=agents[agent].get_will(History)
    return will
        
        
        
def step(agents: list,History, will):
    '''
    take one time step
    '''
    if(History != []):
        will[History[-1]["speaker"]]-=4
    if(len(History)%REFLECTION_INTERVAL==0):
        will=update_will(agents,History,will)
    speaker=max(will.items(),key=lambda tup: tup[1])[0]
    print(will)
    print(f"speaker: {speaker}")
    if(History==[]):
        feed_History=[]
    else:
        feed_History=History[-(len(History)%5)-1:]
    rep=agents[speaker].speak(feed_History)
    print(agents[speaker].name()+": "+rep)
    History.append({"speaker":agents[speaker].name(),"message":rep})
    feed_History.append(History[-1])
    
    
    if((len(History)+1)%REFLECTION_INTERVAL==0):
        print("starting reflection!\n"+"-"*15)
        for agent in agents:
            agents[agent].reflect(feed_History)
    print(History)
    return History,will


    
'''
Loading simulation

agents:[Agent] list of agents
History:[<name,content>] chat history
will:List[<agent_id,will>] How much do each agent want to chat
'''

simulation_name=input("Please Enter template name:")
main_dir=simulation_name
curr_step=0
with open(f"{main_dir}/global.json") as f:
    gbl=json.load(f)
    curr_step=gbl["step"]
    agent_list=gbl["agents"]
    
    will=gbl["will"]
    if(will== None):
        will={}
        for agent in agent_list:
            will[agent]=0



History=[]

with open(f"{main_dir}/history.json") as f:
    his=json.load(f)
    for id in his:
        History.append(his[id])

agents={}
for agent in agent_list:
    agents[agent]=Agent(f"{main_dir}/agents/{agent}",agent_list)
print(agent_list)
print("Loading finished!")

'''
running phase
command:
run <run_num>: proceed <run_num>step of chat
exit: exit the program
'''
while True:
    command=input("Enter option:")
    if(command=='exit'):
        sys.exit()
    elif(command.split(" ")[0]=='run'):
        run_num=int(command.split(" ")[1])
        for i in range(run_num):
            curr_step+=1
            History,will=step(agents,History,will)
            with open(f"{main_dir}/log/{curr_step}.txt","w") as f:
                speaker=History[-1]["speaker"]
                f.write(f"log for time step{curr_step}\n speaker for this round: {speaker}\n")
                for item in History:
                    f.write(json.dumps(item,indent=2))
                    f.write("\n")
                f.write("-"*20+"\n")
                for agent in agents:
                    f.write(json.dumps(agents[agent].config,indent=2))
                    f.write("\n")
                
                
    elif(command=='save'):
        '''
        Saving all the data
        '''
        with open(f"{main_dir}/global.json","w") as f:
            gbl["step"]=curr_step
            gbl["will"]=will
            f.write(json.dumps(gbl,indent=2))
        with open(f"{simulation_name}/history.json","w") as f:
            load={}
            for n,v in enumerate(History):
                load[n]=v
            f.write(json.dumps(load,indent=2))
        for agent in agents:
            agents[agent].save_state()
        print("saved successfully!")
    else:
        print("Invalid input")
