#/usr/bin/python3
import sys
sys.path.append("../")
import python_client

# define the API basepoint and a worker for worker example
jec = python_client.GpcJobEngineClient("http://localhost:30000/")

jec.deleteAllJobs()
 