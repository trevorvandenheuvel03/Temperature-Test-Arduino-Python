#!/usr/bin/env python
# coding: utf-8

# In[1]:


#imports and Author Trevor van den Heuvel
import numpy as np
import pyfirmata as pf
from jupyterplot import ProgressPlot
from time import sleep


# In[2]:


#connects to Arduino through COM3 and allows it to communicate
board = pf.Arduino("COM3")
it = pf.util.Iterator(board)
it.start()


# In[3]:


#collects reading from analogue pin A0
a0 = board.get_pin('a:0:i')
a1 = board.get_pin('a:1:i')


# In[6]:


#outputs the current voltage read through A0
voltage0 = a0.read()*5
print(voltage0)

voltage1 = a1.read()*5
print(voltage1)


# In[12]:


#creates text file and graph that shows temperature values in real time
with open('temperature.text', 'w') as f:
    tempPlot = ProgressPlot(plot_names=['Temperature vs Time'], line_names=['Temperature']) #creates plot
    i = 0
    T = -20
    T2 = -20
    T3 = -20
    while T>-30 and (T<24 or T2<24 or T3<24):      #T2 and T3 are included to prevent spikes in data to end loop
        i += 0.5
        voltage0 = a0.read()*5            #finds voltage at pin a0
        voltage1 = a1.read()*5            #finds voltage at pin a1
        I = (voltage1 - voltage0)/3846    #finds current
        R = voltage0/I                    #finds resistance
        T = (R/1000 - 1)/0.00383          #finds temperature
        tempPlot.update(T)                #adds temperature to graph
        sleep(15)                         #waits before adding another reading
        
        voltage0 = a0.read()*5            #finds voltage at pin a0
        voltage1 = a1.read()*5            #finds voltage at pin a1
        I = (voltage1 - voltage0)/3846    #finds current
        R = voltage0/I                    #finds resistance
        T2 = (R/1000 - 1)/0.00383         #finds temperature
        sleep(15)                         #waits before calculating T3
        
        voltage0 = a0.read()*5            #finds voltage at pin a0
        voltage1 = a1.read()*5            #finds voltage at pin a1
        I = (voltage1 - voltage0)/3846    #finds current
        R = voltage0/I                    #finds resistance
        T3 = (R/1000 - 1)/0.00383         #finds temperature

        f.write(str(i) + '\t' + str(T) + '\n') #adds time and temperature values to text file
    tempPlot.finalize()
    print(T)    #prints final temperature

