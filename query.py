from owlready2 import *
import json
#comment about this code regarding the ontology.

step_count = 0

def sanitize_uri(text):
    return text.replace(" ", "_")

# Load the JSON data line by line, treating each line as a separate JSON object
response_json = []
with open('Skills.json', 'r') as file:
    for line in file:
        try:
            response_json.append(json.loads(line))  # Load each line as a JSON object
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

# Create the ontology
onto = get_ontology("http://example.org/ifixit.owl")

with onto:
    # Define classes
    class Item(Thing): pass
    class Procedure(Thing): pass
    class Step(Thing): pass
    class Tool(Item): pass
    class Part(Item): pass
    class Image(Thing): pass  # Define the Image class

    # Define properties
    class has_procedure(ObjectProperty): pass
    class has_tool(ObjectProperty): pass
    class has_step(ObjectProperty): pass
    class part_of(Item >> Item, TransitiveProperty): pass
    class has_image(ObjectProperty): pass
    class issubProcedure(Procedure >> Procedure, TransitiveProperty): pass
        

# Dictionary to store procedure instances
procedure_instances = {}

# Store step information for each procedure to compare later
procedure_steps = {}

# Iterate over each procedure in the loaded JSON data
for data in response_json:
    # Check if necessary keys exist
    if 'Guidid' not in data or 'Title' not in data:
        print(f"Skipping entry with missing 'Guidid' or 'Title': {data}")
        continue
    
    item = Item(sanitize_uri(data['Category']))
    # Create a Procedure instance
    procedure = Procedure(sanitize_uri(f"Procedure_{data['Guidid']}"))  # Ensuring unique IRI by prefixing "Procedure_"
    item.has_procedure.append(procedure)

     # Store the procedure instance and steps
    procedure_instances[data['Guidid']] = procedure
    steps_list = []

    # Set properties for the procedure
    procedure.title = data['Title']
    procedure.category = data['Category']
    procedure.url = data['Url']

    #dictionary for all tools in toolbox
    tools_in_procedure = {}
    # Create Tool instances and link to the procedure
    if 'Toolbox' in data:
        for tool in data['Toolbox']:
            if 'Name' not in tool:
                print(f"Skipping tool with missing 'Name': {tool}")
                continue
            tool_instance = Tool(sanitize_uri(f"Tool_{tool['Name']}"))  # Ensure unique IRI
            tool_instance.url = tool['Url']
            # Store tool in a dictionary for easy access when linking to steps
            tools_in_procedure[tool['Name']] = tool_instance
            # Link tools to the procedure
            procedure.has_tool.append(tool_instance)

    # Create Step instances and link to the procedure
    if 'Steps' in data:
        for step_data in data['Steps']:
            if 'StepId' not in step_data:
                print(f"Skipping step with missing 'StepId': {step_data}")
                continue
            step = Step(sanitize_uri(f"Step_{step_data['StepId']}"))  # Ensure unique IRI
            step.text_raw = step_data['Text_raw']
            step.order = step_data['Order']

            # Check if "tools_extracted" exists and if tools are in the procedure's toolbox
            if 'Tools_extracted' in step_data:
                
                for extracted_tool in step_data['Tools_extracted']:
                    
                    if extracted_tool in tools_in_procedure:
                        # Link the tool to the step
                        step.has_tool.append(tools_in_procedure[extracted_tool])
                        
                    else:
                        print(f"Tool '{extracted_tool}' extracted in step not found in procedure toolbox.")

            steps_list.append(step_data['StepId'])

            step_count += 1

            # Create Image instances for each image associated with the step
            if 'Images' in step_data:
                for image_url in step_data['Images']:
                    if not image_url:
                        print(f"Skipping image with missing URL: {step_data}")
                        continue
                    image_instance = Image(image_url)  # Create an Image instance
                    step.has_image.append(image_instance)

            # Link the step to the procedure
            procedure.has_step.append(step)
    
    procedure_steps[data['Guidid']] = set(steps_list)

for guid1, steps1 in procedure_steps.items():
    for guid2, steps2 in procedure_steps.items():
        if guid1 != guid2 and steps1.issubset(steps2):
            # If steps1 is a subset of steps2, guid1 is a sub-procedure of guid2
            procedure_instances[guid1].issubProcedure.append(procedure_instances[guid2])

# Save the ontology to an OWL file
try:
    onto.save(file="ifixit_ontology.owl", format="rdfxml")
    print("Ontology saved as ifixit_ontology.owl")
except Exception as e:
    print(f"Error saving ontology: {e}")

print(f"number of steps: {step_count}")


