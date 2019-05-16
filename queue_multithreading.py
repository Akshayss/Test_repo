# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:58:48 2019

@author: akshay
"""


from queue import Queue
import threading
import time




class Person():
    def __init__(self, firstName, lastName):
        self.firstName = firstName
        self.lastName = lastName

def printName(q):
    while True:
        person = q.get()
        print ("Getting Name: " + person.firstName + " " + person.lastName)
        q.task_done()
        
def putPersonQueue(q, firstName, lastName):
    name = threading.currentThread().getName()
    print ("Thread: " + name)
    person = Person(firstName, lastName)
    print ("Adding Name: " + person.firstName + " " + person.lastName)
    q.put(person)
    
    
if __name__ == "__main__":
    namesList = [('Akshay', 'Sawant'),\
            ('Ameya', 'Sawant')]
    q = Queue()
    
    for names in namesList:
        firstName = names[0]
        lastName = names[1]
        
        t = threading.Thread(name="Producer Thread - "+firstName+lastName, target=putPersonQueue, args=(q, firstName, lastName), daemon=True)
        t.start()
        
    t = threading.Thread(name="Consumer Thread", target=printName, args=(q,), daemon=True)
    t.start()
    
    q.join()
