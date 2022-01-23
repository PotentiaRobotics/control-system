# Create priority queue
# In main create three threads
# 1 for managing actions (stores priority queue)
# 1 for reading sensor data
# Updates sensor data through wifi and propiosense system
# 1 for executing the first action in the priority queue
import threading
import socket
import heapq
import time

class Receiver:
  def __init__(self, host, port):
    self.actions = ["Password L"]
    self.timer = 0
    self.HOST = host
    self.PORT = port

  def priorityQueue(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    #managing error exception
    try:
      s.bind((self.HOST, self.PORT))
    except socket.error:
        print ('Bind failed ')

    s.listen(5)
    print ('Socket awaiting messages')
    (conn, addr) = s.accept()
    print ('Connected')

    # awaiting for message
    while True:
      instruction = conn.recv(1024)
      action = instruction.decode('UTF-8')
      print("Action received:", action)
      if "Password" in action:
        heapq.heappush(self.actions,action)
        print(self.actions)
      else:
        print("Incorrect Command")

      # Sending reply
      conn.send(action.encode()+bytes(" works",'utf-8'))

  def execute(self):
    while len(self.actions) > 0:
      if self.timer == 0:
        print("Executed: ", heapq.heappop(self.actions))
        time.sleep(5)
        heapq.heappush(self.actions, "Password Balancing")
      print("Inside execute",self.actions)

  def sensorData(self):
    print("Test")

  def runSimul(self):
    threading.Thread(target=self.priorityQueue).start()
    threading.Thread(target=self.execute()).start()
    threading.Thread(target=self.sensorData()).start()

def main():
  simulation = Receiver('10.235.1.127',12345)
  simulation.runSimul()

if __name__ == "__main__":
  main()