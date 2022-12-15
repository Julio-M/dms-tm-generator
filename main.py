#!/usr/bin/env python3

# Import modules
import json, os, readline
from bullet import Bullet
import uuid

# importing the random module
import random

# Make uuid json serializable
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)

unique_id = uuid.uuid4() 
random_ids = []
# Initialize empty dictionary `data` and set `rules` key to an empty list
data = {}
data['rules'] = []

# User prompt to enter path of table list file and check if file exists
print('\n')
readline.set_completer_delims(' \t\n=')
readline.parse_and_bind("tab: complete")
table_list_input = input("Enter the path of your table list file: ")     
assert os.path.exists(table_list_input), "Can't find the table list file at, " + table_list_input

# Function that reads table list file
def readTableList():
    file = open(table_list_input, "r")
    file_lines = file.read()
    list_of_lines = file_lines.split("\n")
    list_of_lines_after_quotes = [w.strip('\"') for w in list_of_lines]
    return list_of_lines_after_quotes if '"' in list_of_lines[0] else list_of_lines

# Prompt user to enter schema name and/or the prefix_value
print('\n')
schema_list_input = input("Enter the schema name \n(Default value is %) : ") or "%"
prefix_value = input("Enter the prefix value if there are any prefix rules added (Leave blank if not) \n(Default value is None) : ") or None

# Choose from the list of rule-actions
def ruleAction():
    rule_action = ["include","exclude","explicit"]
    prompt = Bullet(
            prompt = "\nSelect a action for your rules : ",
            choices = rule_action, 
            indent = 0,
            align = 5, 
            margin = 2,
            shift = 0,
            bullet = "",
            pad_right = 5,
            return_index = False
        )
    selected_profiles = prompt.launch()
    return selected_profiles

# Invoke ruleAction function assign value
rule_action=ruleAction()

# Function to present a list of table types and return the selected
def tableType():
    table_types = ["table","view","all"]
    prompt = Bullet(
            prompt = "\nSelect whether to migrate tables, views or all : ",
            choices = table_types, 
            indent = 0,
            align = 5, 
            margin = 2,
            shift = 0,
            bullet = "",
            pad_right = 5,
            return_index = False
        )
    selected_type = prompt.launch()
    return selected_type

# Invoke tableType function assign value
table_type=tableType()

# General rules object
def general_rules(i,random_id): 
    return {
                "rule-type":"selection",
                "rule-id":f"{random_id}",
                "rule-name":unique_id,
                "object-locator":{
                    "schema-name":schema_list_input,
                    "table-name":readTableList()[i] if "add-prefix" not in readTableList()[i] else  readTableList()[i].replace(' add-prefix',"")
                },
                "rule-action":rule_action,
                "filters":[]
            }

# Prefix rules object
def prefix_rules(i,random_id):
    return {
                "rule-type":"transformation",
                "rule-id":f"{random_id}",
                "rule-name":unique_id,
                "rule-target":"table",
                "object-locator":{
                    "schema-name":schema_list_input,
                    "table-name":readTableList()[i] if "add-prefix" not in readTableList()[i] else  readTableList()[i].replace(' add-prefix',"")
                },
                "rule-action":"add-prefix",
                "value":prefix_value
            }
                
# Loop through the list of table names, create dictionary, and add it to the list
def createJSON():
        for i in range(0,len(readTableList())):
            random_id = random.randint(0,1000)
            if random_id in random_ids: random_id = random.randint(0,1000)
            if "add-prefix" in readTableList()[i]:
                if prefix_value==None:
                    print('You forgot to add a value for prefix rule-actions\n Either delete the "add-prefix" from list of tables or run the script again and add value')
                    return
                data['rules'].append(prefix_rules(i,random_id))
                data['rules'].append(general_rules(i,random_id))
                print('This table has a prefix value', '\033[1m' + readTableList()[i])
            else:
                data['rules'].append(general_rules(i,random_id))
            random_ids.append(random_id)

        with open('table_mapping.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=True, indent=2, cls=UUIDEncoder)
        print('\n')
        print("Check your table_mapping.json file.")

# Invoke CreateJSON()
createJSON()
