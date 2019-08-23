import _thread as thread,time
stdoutmutex = thread.allocate_lock()
numthreads = 5
exitmutexes = [thread.allocate_lock() for i in range(numthreads)]

def counter(myId,count,mutex):
  # pass
  for i in range(count):
    time.sleep(1/(myId+1))
    with mutex:
      print("[%s] => %s" % (myId, i))
    # stdoutmutex.acquire()
    # print("[%s] => %s" % (myId, i))
    # stdoutmutex.release()

  exitmutexes[myId].acquire()


for i in range(numthreads):
  thread.start_new_thread(counter,(i,5,stdoutmutex))


for mutex in exitmutexes:
  while not mutex.locked():pass

print("Main thread exiting")
