import os
import shutil
import sys
import tkinter as tk
import webbrowser
import socket
from subprocess import Popen
from tkinter import *
from tkinter import filedialog
import re

class fileShare:
    def __init__(self, obj):
        self.obj = obj
        self.currentWrokingDir = os.getcwd()
        if os.name == 'nt':
            self.fileCacheDir = os.path.join(self.currentWrokingDir, 'fileCache')
        else:
            self.fileCacheDir = os.path.join(self.currentWrokingDir, 'fileCache')
        self.subProcessId = ''
        self.homeFrame()

    def ipAddr(self):
        regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
                    25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
        listOfNetworks = socket.getaddrinfo(socket.gethostname(), None)
        validIp = []
        for network in listOfNetworks:
            if re.search(regex, network[4][0]):
                validIp.append(network[4][0])
        return validIp

    def all_children(self, window):
        _list = window.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        return _list

    def clear_window(self, window):
        widget_list = self.all_children(window)
        for widget in widget_list:
            widget.destroy()

    def change_frame(self, which_frame, from_which_frame):
        from_which_frame.destroy()
        which_frame()

    def go(self, textBox):
        inputValue = textBox.get("1.0", "end-1c")
        inputValue = 'http://' + inputValue
        print(inputValue)
        webbrowser.open(inputValue)

    def selectFiles(self, frame):
        os.makedirs(self.fileCacheDir, exist_ok=True)
        frame.filename = filedialog.askopenfilename(initialdir=self.currentWrokingDir, title="Choose your file", filetypes=(("All files", "*.*"), ("All files", "*.*")))
        if frame.filename:
            label = Label(frame, text=frame.filename, height='1', width='100', relief=RAISED)
            shutil.copy2(frame.filename, self.fileCacheDir)
            print(f"Copied file to {self.fileCacheDir}")  # Debugging statement
            label.pack()

        # List files in the directory for debugging
            print("Files in fileCache directory:", os.listdir(self.fileCacheDir))

    def closeConnection(self):
        if self.subProcessId:
            self.subProcessId.kill()
        if os.path.exists(self.fileCacheDir):
            shutil.rmtree(self.fileCacheDir)
        quit()

    def establishConnection(self, frame): 
        os.makedirs(self.fileCacheDir, exist_ok=True)  # Ensure directory exists
        python_path = r"C:\Users\student\AppData\Local\Programs\Python\Python312\python.exe"  # Full path to Python
        cmd = f"cd {self.fileCacheDir} && {python_path} -m http.server 8001"
        print(cmd)  # For debugging
        try:
            self.subProcessId = Popen(cmd, shell=True)  # Use shell=True
            label = Label(frame, text='Connection Established to ' + ' #'.join(self.ipAddr()) + '!!!')
        except Exception as e:
            print("Error starting HTTP server:", e)
            label = Label(frame, text='Error starting server: ' + str(e))
        label.pack()

    def homeFrame(self):
        frame = Frame(self.obj, width=500, height=500)
        frame.pack(pady=80)

        b1 = Button(frame, width=20, bd=5, text="Send", command=lambda: self.change_frame(lambda: self.sendFrame(self.obj), frame))
        b1.pack(pady=20)

        b2 = Button(frame, width=20, bd=5, text="Receive", command=lambda: self.change_frame(lambda: self.receiveFrame(self.obj), frame))
        b2.pack(pady=20)

        b3 = Button(frame, width=20, bd=5, text="Quit", command=quit)
        b3.pack(pady=20)

    def sendFrame(self, obj):
        print(self.ipAddr())
        frame = Frame(obj, width=500, height=500)
        frame.pack(pady=80)

        b1 = Button(frame, width=20, bd=5, text="Select File", command=lambda: self.selectFiles(frame))
        b1.pack(pady=5)

        b2 = Button(frame, width=20, bd=5, text="Establish Connection", command=lambda: self.establishConnection(frame))
        b2.pack(pady=15)

        b3 = Button(frame, width=20, bd=5, text="Quit", command=self.closeConnection)
        b3.pack(pady=15)

    def receiveFrame(self, obj):
        frame = Frame(obj, width=500, height=500)
        frame.pack(pady=80)

        l = Label(frame, text='Enter URL shared by Sender (ex. 127.0.0.101:8001)')
        l.pack(pady=20)

        textBox = Text(frame, height=1, width=20)
        textBox.pack()

        b1 = Button(frame, width=20, bd=5, text='Go', command=lambda: self.go(textBox))
        b1.pack(pady=10)

        b2 = Button(frame, width=20, bd=5, text='Back', command=lambda: self.change_frame(lambda: self.homeFrame(), frame))
        b2.pack(pady=10)
