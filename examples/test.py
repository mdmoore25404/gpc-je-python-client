#/usr/bin/python3
import python_client
import time
import random

### this feller is where your code gets the job data if you want to use the threaded worker pattern
def myWorker(j,jec):
    print(f"WORKER THREAD I have the job: {j}")    
    time.sleep(random.randint(2,6)) # simulate time taken to run
    jec.completeJob(j['_id'], f"WORKER! job {j['_id']}")
    print("Worker finished a job!")
########

## define the API basepoint and a worker for worker example
jec = python_client.GpcJobEngineClient("http://localhost:8008/", userWorker= myWorker)

#example jobs
for i in range(20):
    jec.addJob(f"example job {i}", f"Friendly Name {i}")

#the jobs added
for j in jec.getJobs():
    print(f"Job Added: {j}")

#checkout a job
job = jec.checkoutJob()
id = job['_id']
print(f"checked out job {job}")

#mark it completed
if jec.completeJob(id, f"PROCEDURAL! jobid {id}"):    
    j = jec.getJobById(id)
    print(f"Job we completed: {j}")

#### maybe you just want to call your function only if there's a job and not deal with that check/wait yourself:
print("starting worker thread")
jec.start()

## normally when using the worker you would jec.start() and then jec.end() when the python script is terminating, or have it but we're going to watch
## this would be like having a status dashboard showing what's being worked on etc with multiple workers chewing data.
while jec.processing == True:    
    for j in jec.getRunningJobs():
        print(f"running job: {j}")
    time.sleep(1) #sleep so we don't pound the API in a loop

print("all done! no jobs left in queue! lets look at the results")

for j in jec.getCompletedJobs():
    print(f"Completed Job: {j}")

#cleanup jobs
jec.deleteAllJobs()