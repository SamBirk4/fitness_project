
from datetime import datetime
from email import header
import re
import profile
import csv
from pymongo import MongoClient

client = MongoClient()
db = client.project1
collection = db.fitness
    
#creating a profile#

def user_profile() -> profile.Profile:

    '''
    user_profile -> None :

    This function asks the user for input on name, height, weight.  The height and weight are used to calculate variables
    in the output of the program i.e. gain/loss.

    Return: None 
    '''

    while True:    
        try: 
            print("\nPlease enter your information.")
            user_first = input("\nFirst Name: ").strip()
            user_last = input("Last Name: ").strip()

            if not None == re.search('\W', user_first):
                raise ValueError("Non letter used")
            elif not None == re.search('\W', user_last):
                raise ValueError("Non letter used")
            else: 
                break
        except ValueError:
            print("\n\tNo special characters,please try again.")
    
    while True:
        try:
            user_height = input("Height (in): ") # Used to calculate BMI

            if not None == re.search('\D', user_height):
                raise ValueError
            else:
                break
        except ValueError:
            print("\n\tPlease enter your height in inches.")
        
    while True:
        try:
            user_weight = input("Weight (lbs): ") # Used to calculate gain/loss

            if not None == re.search('\D', user_weight):
                raise ValueError
            else:
                p1 = profile.Profile(user_first, user_last, user_height, user_weight)
                return p1
        except ValueError:
            print("\n\tPlease enter your weight in pounds.")

# Option to add delete or quit #

def add_new_entry(p1):

    '''
    add_new_entry 

    This function takes in put on a new weight and thats used to calculate gain/loss and BMI.  This function calls on two other
    functions, weight_track and load_weight (see below for functionality). This returns the desired output of new weight, gain/loss, BMI, date.

    Argunents: p1 - this is the object created from the class in profile.py

    Returns: None  
    '''

    while True:
        try:
            print("\nWhat would you like to do?")
            print("\nEnter 'add' to update weight")
            print("Enter 'delete' to clear your history")
            print("Enter 'done' to exit")

            option = input("~").strip()

            if option.upper() =="DELETE":
                collection.delete_many({}) # Will delete information in database 
                break
            elif option.upper() == "ADD":
                new_weight = input("\nenter weight (lbs): ")
                p1.add_entry(new_weight) # Will append new weight to list of weights in order to calculate BMI and gain/loss
            elif option.upper() == "DONE":
                weight_track(p1)
                load_weight() # Will run load function to print CSV to console if 'done' is selected 
                break
            else:
                raise ValueError('Invalid Input')
        except ValueError:
            print("\n\tPlease enter 'add' to continue. Otherwise enter 'delete' or 'done'.") 

def weight_track(p1): # Writes output to csv file

    '''
    weight_track()

    This function prints the output to the CSV file 'fitness_track.csv'.

    Arguments: p1 - this is the object created from the class in profile.py

    Returns: None
    '''

    with open("fitness_track.csv", "a", newline = '') as fitness_log:
        writer = csv.writer(fitness_log)
        writer.writerow(p1.log_output())
    
def load_weight():

    '''
    load_weight()

    This function prints all entries in 'fitness_track.csv' to the console while also printing it to the mongodb database.
    The out put is formated and given headers when printed to the database. 

    Return: None
    '''
    
    with open("fitness_track.csv", "r") as fitness_log:
        csvFile = csv.reader(fitness_log) # Prints all entries in Fitness_trac.csv to the console
        for line in csvFile: # Prints lines to the database 
            first = True
            print(line)
            if line ==[]:
                continue 
            for weight in line[0].strip('][').split(', '):
                if first:
                    first = False
                    continue
                print(weight)
                dict_val = { # Headers for the information output from program
                    "Weight (lbs)" : int(weight.strip("'")),
                    "Gain or Loss (lbs)" : line[1],
                    "BMI" : line[2],
                    "Date" : line[3]
                }
                collection.insert_one(dict_val)

p1 = user_profile()
add_new_entry(p1)





