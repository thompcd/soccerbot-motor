import queue
import time

def process_moves(q, n_cycles=2):
    while True:
        try:
            queued = q.get(timeout=4)
            print("Executing command id " + queued[0] + " for other thread...")
            motor_output(queued[0], queued[1], queued[2])
            
        except queue.Empty:
            print("Queue was empty, nothing to do...")
            time.sleep(0) # So app doesn't bog down, relinquish control
                          # when idle to let other threads have more time.

def motor_output(id, degrees, magnitude):
    try:
        print("moving " + str(magnitude) + " units in direction of " + str(degrees) + " bearing")
        #send result back to main thread
        # client_queue.put(0, "")
    except:
        # client_queue.put(-1, "unrecognized command")
        print("error moving")
