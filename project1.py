
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
            user_height = input("Height (in): ")

            if not None == re.search('\D', user_height):
                raise ValueError
            else:
                break
        except ValueError:
            print("\n\tPlease enter your height in inches.")
        
    while True:
        try:
            user_weight = input("Weight (lbs): ")

            if not None == re.search('\D', user_weight):
                raise ValueError
            else:
                p1 = profile.Profile(user_first, user_last, user_height, user_weight)
                return p1
        except ValueError:
            print("\n\tPlease enter your weight in pounds.")

#Option to add#

def add_new_entry(p1):

    while True:
        try:
            print("\nWhat would you like to do?")
            print("\nEnter 'add' to update weight")
            print("Enter 'delete' to clear your history")
            print("Enter 'done' to exit")

            option = input("~").strip()

            if option.upper() =="DELETE":
                collection.delete_many({})
                break
            elif option.upper() == "ADD":
                new_weight = input("\nenter weight (lbs): ")
                p1.add_entry(new_weight)
            elif option.upper() == "DONE":
                load_weight()
                break
            else:
                raise ValueError('Invalid Input')
        except ValueError:
            print("\n\tPlease enter 'add' to continue. Otherwise enter 'delete' or 'done'.")

header_lst = ["\nWeight (lbs) ", "Gain or Loss (lbs) ", "BMI ", "Date "]

def weight_track(p1):
    with open("fitness_track.csv", "a", newline = '') as fitness_log:
        writer = csv.writer(fitness_log)
        writer.writerow(p1.log_output())
    
def load_weight():
    with open("fitness_track.csv", "r") as fitness_log:
        csvFile = csv.reader(fitness_log)
        for line in csvFile:
            first = True
            print(line)
            if line ==[]:
                continue 
            for weight in line[0].strip('][').split(', '):
                if first:
                    first = False
                    continue
                print(weight)
                dict_val = {
                    "Weight" : int(weight.strip("'")),
                    "Gain or Loss" : line[1],
                    "BMI" : line[2],
                    "Date" : line[3]
                }
                collection.insert_one(dict_val)

p1 = user_profile()
add_new_entry(p1)
weight_track(p1)




