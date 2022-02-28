import tkinter as tk
from FlappyBirdGym.GameLogic import *

from threading import Thread, Event

import numpy as np

import time

class FlappyBirdGym:
    def __init__(self, windowMode = "none"):
        
        self.windowMode = windowMode

        if windowMode == "none":
            self.gameLogic = GameLogic(windowMode=self.windowMode)

        else:
            self.e = Event()
    
            self.windowThread = Thread(target = self.windowLoop)
            self.windowThread.start() 

            self.e.wait()
            time.sleep(0.5)

        self.done = False
      

    def step(self, action):

        if self.done:
            print("Error: Call step() on a finished game")
            return None 

        done, reward = self.gameLogic.nextGameStep(action)
        self.done = done
        
        state = self.gameLogic.getState()
      
        return state, reward, done
    
    def getState(self):
        return self.gameLogic.getState()

    
    def reset(self):
        self.done = False
        self.gameLogic.reset()

    def windowLoop(self):
        root = tk.Tk()
        self.gameLogic = GameLogic(windowMode=self.windowMode, master=root)

        self.e.set()
        self.gameLogic.mainloop()
   
    def close(self):
        self.gameLogic.quit()