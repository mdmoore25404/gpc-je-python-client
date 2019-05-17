#/usr/bin/python3
import sys
sys.path.append("../")
import python_client
import json

# define the API basepoint and a worker for worker example
jec = python_client.GpcJobEngineClient("http://localhost:30000/")

#example jobs
for i in range(1,101):
    payload = {}
    payload['n'] = i
    jec.addJob(json.dumps(payload), f"IsPrime {i}")


