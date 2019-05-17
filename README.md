This is a python API wrapper for [https://github.com/mdmoore25404/gpc-je]

# Quickstart

For a quick example we will show creating jobs to calculate if a number is prime and then farmingthat work out. The full code is located under the `examples` directory of this project.


Create an instance and load some jobs

    # define the API basepoint and a worker for worker example
    jec = python_client.GpcJobEngineClient("http://localhost:30000/")

    #example jobs
    for i in range(1,101):
        payload = {}
        payload['n'] = i
        jec.addJob(json.dumps(payload), f"IsPrime {i}")


Now we have the jobs loaded, lets work on them

required imports (note we are appending the parent directory `../` to path so that we can import python_client )

    #/usr/bin/python3
    import sys
    sys.path.append("../")
    import python_client
    import time
    import random
    import threading
    import json

    WORKER_THREADS = 10


simple function to determine if a number is prime or not

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

This function is called once for each job and passes the job `j` and the job engine client `jec`

    def myWorker(j,jec):    
        time.sleep(random.randint(2,6)) # simulate time taken to run
        payload = json.loads(j['payload'])    
        n = payload['n']    
        prime = isPrime(n)    
        result = {}
        result['isPrime'] = prime
        jec.completeJob(j['_id'], json.dumps(result))    
    ########

This is the multithreadded entrypoint. Worker threads will start here. The URL to the API endpoint, `myWorker`, which we defined above will be used for each job found, we will `terminateOnNoJobs` so the thread will exit when no more jobs remain in the queue, and we provide a `workerId` 

    def spawnme(workerid):
        ## define the API basepoint and a worker for worker example
        jec = python_client.GpcJobEngineClient("http://localhost:30000/", userWorker= myWorker, terminateOnNoJobs= True, workerId=workerid)
        #### maybe you just want to call your function only if there's a job and not deal with that check/wait yourself:    
        jec.start()

Here we create `WORKER_THREADS` number of worker threads, which start in `spawnme` and pass the thread number as `workerId`

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


The worker threads will compute in parallel until there are no more jobs left in the queue and then the `main` process will exit.

