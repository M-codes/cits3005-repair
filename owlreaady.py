import json

counter = 0

# Load a local JSON file line by line
response_json = []
steps = []
with open('Vehicle.json', 'r') as file:
    for line in file:
        try:
            response_json.append(json.loads(line))  # Load each line as a JSON object
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
for lines in response_json:
    print(f"This is toolbox: {lines['Steps']}")
    for data in lines['Steps']:
        #print(f"this is tools: {data['Tools_extracted']}")
        steps.append(data['StepId'])
        counter += 1

# function to get unique values
def unique(list1):

    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

unique_step = unique(steps)


    
print(len(steps))
print(len(unique_step))