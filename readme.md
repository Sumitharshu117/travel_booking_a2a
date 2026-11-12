this is an agent to agent communication project work
where few agent are communicating to each other and an orchestrator agent is handling all the workflow 
user ask his query and it will divide the query into different sub problem then pass through all the agent
and after collection  output then genrate  a final report for the user query  response 



Create an virtual env through 
*python -m venv venv*
**bin/Scripts/activate**

<!--  --> for installing the dependencies:
**pip install -m requirements.txt**

*Inside the .env file put gemini llm api key* 

*for running the instance of flight agent *
**uvicorn flight_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8001**

*for running the instance of hotel agent *
**uvicorn hotel_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8002**

*for running the instance of transport agent *
**uvicorn transport_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8003**

*for running the instance of activity  agent *
**uvicorn activities_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8004**

*for running the instance of payment agent *
**uvicorn payment_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8005**


<!-- if you want to test particular agent  -->
**adk run <agent_name>**

for user interaction through user interface run this command  
**adk web**
