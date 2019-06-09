#!/usr/bin/python3
import sys
sys.path.append("../")
import python_client
import time
import random
import threading
import json

WORKER_THREADS = 10

def isPrime(n) :   
    # Corner cases 
    if (n <= 1) : 
        return False
    if (n <= 3) : 
        return True  
    # This is checked so that we can skip  
    # middle five numbers in below loop 
    if (n % 2 == 0 or n % 3 == 0) : 
        return False
  
    i = 5
    while(i * i <= n) : 
        if (n % i == 0 or n % (i + 2) == 0) : 
            return False
        i = i + 6
  
    return True


### this feller is where your code gets the job data if you want to use the threaded worker pattern
def myWorker(j,jec):    
    time.sleep(random.randint(2,6)) # simulate time taken to run
    payload = json.loads(j['payload'])    
    n = payload['n']    
    prime = isPrime(n)    
    result = {}
    result['isPrime'] = prime
    jec.completeJob(j['_id'], json.dumps(result))    
########

def spawnme(workerid):
    ## define the API basepoint and a worker for worker example
    jec = python_client.GpcJobEngineClient("http://localhost:8007/", userWorker= myWorker, terminateOnNoJobs= True, workerId=workerid)
    #### maybe you just want to call your function only if there's a job and not deal with that check/wait yourself:    
    jec.start()

def main():
    workers = []
    for i in range(WORKER_THREADS):
        t = threading.Thread(target=spawnme(i))
        workers.append(t)
    
    for w in workers:
        w.start()

    for w in workers:
        w.join()
    
    print(f"spawned {WORKER_THREADS} threads")

if __name__ == "__main__":
    main()
