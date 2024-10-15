from flask import Flask, render_template, abort, redirect,request,url_for
from owlready2 import *

# Load the ontology and enable reasoning
onto = get_ontology("repair_ontology.owl").load()

# Run reasoning to compute inferred classes and relations
# with onto:
#     sync_reasoner()

app = Flask(__name__)

@app.route('/')
def index():

    items_info = []

    # Collect information about items, excluding subclasses like Tool and Part
    for item in onto.Item.instances():
        if not isinstance(item, onto.Tool) and not isinstance(item, onto.Part):
            item_data = {
                "name": item.name,
                "has_procedure": [procedure for procedure in item.has_procedure],
                "part_of": [part.name for part in item.part_of] if item.part_of else [],
                "errors": []  # To track any errors found
            }

            # Error: Check if procedure is missing steps or tools
            for procedure in item_data['has_procedure']:
                if not procedure.has_step:
                    item_data['errors'].append(f"Procedure '{procedure.has_title[0]}' has no steps.")
                if not procedure.has_tool:
                    item_data['errors'].append(f"Procedure '{procedure.has_title[0]}' has no tools.")

            items_info.append(item_data)

    return render_template('index.html', items=items_info)


@app.route('/procedure/<string:procedure_title>')
def procedure_detail(procedure_title):
    # Get the procedure instance by its title
    procedures = [proc for proc in onto.Procedure.instances() if procedure_title in proc.has_title]
    
    if not procedures:
        abort(404)  # Procedure not found

    procedure = procedures[0]  # Assuming titles are unique, take the first match

    return render_template('procedure_detail.html', procedure=procedure)

@app.route('/add_procedure', methods=['POST'])
def add_procedure():
    item_name = request.form.get('item_name')
    procedure_title = request.form.get('procedure_title')
    step_titles = request.form.getlist('step_titles')  # Use getlist for multiple entries
    tool_titles = request.form.getlist('tool_titles')  # Use getlist for multiple entries

    # Find the item instance
    item = next((i for i in onto.Item.instances() if i.name == item_name), None)

    # Find or create the procedure instance
    procedure = next((p for p in onto.Procedure.instances() if p.has_title and p.has_title[0] == procedure_title), None)

    if procedure is None:  # If the procedure does not exist, create it
        procedure = onto.Procedure(sanitize_uri(f"Procedure_{procedure_title}"))
        procedure.has_title.append(procedure_title)

    # Add steps to the procedure
    for step_title in step_titles:
        step_title = step_title.strip()  # Remove any extra whitespace
        if step_title:  # Check if the title is not empty
            existing_step = next((s for s in onto.Step.instances() if s.has_title and s.has_title[0] == step_title), None)
            if existing_step is None:
                step = onto.Step(sanitize_uri(f"Step_{step_title}"))
                step.has_title.append(step_title)
                procedure.has_step.append(step)  # Link step to the procedure

    # Add tools to the procedure
    for tool_title in tool_titles:
        tool_title = tool_title.strip()  # Remove any extra whitespace
        if tool_title:  # Check if the title is not empty
            existing_tool = next((t for t in onto.Tool.instances() if t.has_title and t.has_title[0] == tool_title), None)
            if existing_tool is None:
                tool = onto.Tool(sanitize_uri(f"Tool_{tool_title}"))
                tool.has_title.append(tool_title)
                procedure.has_tool.append(tool)  # Link tool to the procedure

    # Link the procedure to the item
    if item:
        item.has_procedure.append(procedure)

    # Save the changes to the ontology
    onto.save(file="repair_ontology.owl", format="rdfxml")

    return redirect(url_for('index'))




def sanitize_uri(text):
    return text.replace(" ", "_")

if __name__ == '__main__':
    app.run(debug=True)
