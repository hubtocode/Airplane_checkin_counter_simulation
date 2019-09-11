#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Queue(object):
    '''Implementation of the queue abstract data structure using Python lists'''
    
    def __init__(self):
        self.items = []
        
    #helps in adding elements to the queue  
    def enqueue(self, item):
        self.items.insert(0,item)
        
    #remove elements from the queue    
    def dequeue(self):
        return self.items.pop()
    def size(self):
        return len(self.items)
    
    #check if the queue has any items
    def isEmpty(self):
        return self.items == []
    
    #prints the values in the queue
    def __str__(self):
        return str(self.items)
    def __repr__(self):
        return str(self.items)


def Simulation(nb,ne,pb,pe):
    
    '''
    nb : Number of business customers
    ne : Number of economy customers
    pb: Time to process check-in for business customers
    pe: Time to process check-in for economy customers
    Function runs the simulation for a check in counter and return the average wait time for business and 
    economy class passengers and return the closing time for last counter'''
    
    #import libraries 
    import numpy as np
    from datetime import datetime
    from datetime import timedelta

    #inititaiize the variables
    bcust_interval = np.linspace(0,120,nb,dtype=int)
    ecust_interval = np.linspace(0,120,ne,dtype=int)
    e_wait = Queue() #to track economy customers 
    b_wait = Queue() #to track business customers
    i=0
    e_busy = 0 #server flag for economy queue
    b_busy = 0 #server flag for business queue
    e_avg = [] #list for wait times for economy passengers
    b_avg = [] #list for wait times for business passengers
    x=0
    y=0
    
    while not(e_wait.isEmpty() and b_wait.isEmpty() and i>120): #iterating over the simulation
        #enqueue 2 queues with respective passengers
        if i in ecust_interval: 
            e_wait.enqueue(i)
        if i in bcust_interval:
            b_wait.enqueue(i)
        
        #process eco passenger if server is free and queue is not empty
        if e_busy==0:
            if(e_wait.isEmpty() == False):
                a = e_wait.dequeue()
                e_busy = pe
                e_avg.append(i-a)
        else:
            e_busy-=1
            
        #process business passenger if server is free and queue is not empty
        if b_busy==0:
            if (b_wait.isEmpty() == False):
                b = b_wait.dequeue()
                b_busy = pb
                b_avg.append(i-b)
                
            #check if economy queue is not empty and utilise empty business server    
            elif(e_wait.isEmpty() == False):
                c = e_wait.dequeue()
                b_busy = pe
                e_avg.append(i-c)           
        else:
            b_busy-=1
        i = i+1
    
    #average the time and add a processing time to get actual average (waiting+processing)
    averWaitEconomy = sum(e_avg)/ne + pe
    averWaitBusiness = sum(b_avg)/nb + pb
    counter = i-1 + max(b_busy,e_busy)
    
    #convert time to 24 hour format save in a variable
    d = datetime.strptime("16:00", "%H:%M")
    d = d + timedelta(minutes=counter)
    
    closingTime=d.strftime("%I:%M %p")
        
    return averWaitBusiness,averWaitEconomy,closingTime

