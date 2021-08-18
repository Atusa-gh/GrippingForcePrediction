from matplotlib import pyplot as plt
from collections import deque
from threading import Lock, Thread

import myo
import numpy as np

import serial
import csv
import re

import time
from datetime import datetime

## serial port and rate for reading F/T sensor data
SERIAL_PORT = 'COM1'
SERIAL_RATE = 115200

## initializing Myo armband
class EmgCollector(myo.DeviceListener):

  def __init__(self, n):
    self.n = n
    self.lock = Lock()
    self.emg_data_queue = deque(maxlen=n)

  def get_emg_data(self):
    with self.lock:
      return list(self.emg_data_queue)

  def on_connected(self, event):
    event.device.stream_emg(True)

  def on_emg(self, event):
    with self.lock:
      self.emg_data_queue.append((event.timestamp, event.emg))


def main():
    myo.init(sdk_path='E:\\sensors\\myo-sdk-win-0.9.0\\')  ## type the path to myo-sdk 
    hub = myo.Hub()
    listener = EmgCollector(1)
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    ser.write(b'CV 4\r')
    with open('01.csv', 'w', newline='') as csvfile:
        fieldnames = ['Fz', 'emg0', 'emg1', 'emg2', 'emg3', 'emg4', 'emg5', 'emg6', 'emg7']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
  
        with hub.run_in_background(listener.on_event):
            timeout = time.time() + 50    ##  setting the recording time for 50 seconds
            
            starttime = datetime.now()
            while True:
                if listener.get_emg_data() != []:
                    ser.write(b'QR\r') ##this command asks to receive Z-axis force data
                    a = ser.inWaiting() ## this command recieves Z-axis force data
                    time.sleep(0.003)
                    r = ser.read(a).decode('ascii')
                    p = re.sub(r'[-\n,QR, CV, >, , \r]', "", r)
                    if p != "":  
                        emg = listener.get_emg_data()[0][1]
                        writer.writerow({'Fz': p, 'emg0': emg[0],'emg1': emg[1],'emg2': emg[2],'emg3': emg[3],'emg4': emg[4],'emg5': emg[5],'emg6': emg[6], 'emg7': emg[7]})
                if time.time() > timeout:
                    break
          
            endtime = datetime.now()
            print('test time: {}'.format(endtime - starttime))



if __name__ == '__main__':
  main()

