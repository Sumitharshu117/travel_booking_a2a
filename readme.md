Create an virtual env through 
*python -m venv venv*
**bin/Scripts/activate**

<!--  --> for installing the dependencies:
**pip install -m requirements.txt**

*Inside the .env file put gemini llm api key* 

**uvicorn payment_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8005**



**uvicorn transport_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8003**

**uvicorn flight_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8001**

**uvicorn hotel_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8002**

**uvicorn activities_agent.a2a_server:a2a_app --host 127.0.0.1 --port 8004**


<!-- if you want to test particular agent  -->
**adk run**

gut 
**adk web**