# Create priority queue
# In main create three threads
# 1 for managing actions (stores priority queue)
# 1 for reading sensor data
# Updates sensor data through wifi and propiosense system
# 1 for executing the first action in the priority queue

from Propioception import *
from commands import *

import threading
import socket
import heapq
import time
import serial

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
        conn.send(action.encode()+bytes(" works",'utf-8'))
      else:
        print("Incorrect Command")
        conn.send(bytes("Incorrect Commandc",'utf-8'))

      # Sending reply
      

  def execute(self):
    while len(self.actions) > 0:
      if self.timer == 0:
        command = heapq.heappop(self.actions)
        if command == "Password A_on_LED":
          if onAndOfffLed():
            print("Executed: ", command)
          else:
            print("Did not execute correctly ", command)
        
        time.sleep(5)
        if "Password Balancing" not in self.actions:
          heapq.heappush(self.actions, "Password Balancing")
      print("Inside execute",self.actions)

  def sensorData(self):
    # Test
    print("Inside")
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.reset_input_buffer()
    while True:
      print("Inside data")
      # Read from Arduinos to know what motors and sensors there are
      ser.write("Send ****s plz\n".encode('utf-8'))
      line = ser.readline().decode('utf-8').rstrip()
      print(line)

  def runSimul(self):
    threading.Thread(target=self.priorityQueue).start()
    threading.Thread(target=self.execute).start()
    threading.Thread(target=self.sensorData).start()

def startBoot():
  simulation = Receiver('10.235.1.148',12345)
  simulation.runSimul()
