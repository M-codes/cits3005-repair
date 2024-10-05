from flask import Flask, render_template, abort
from owlready2 import *

# Load the ontology
onto = get_ontology("ifixit_ontology.owl").load()

app = Flask(__name__)

@app.route('/')
def index():
    items_info = []

    # Collect information about items, excluding subclasses like Tool and Part
    for item in onto.Item.instances():
        if not isinstance(item, onto.Tool) and not isinstance(item, onto.Part):
            item_data = {
                "name": item.name,
                "has_procedure": [procedure for procedure in item.has_procedure],  # Changed here
                "part_of": [part.name for part in item.part_of] if item.part_of else []
            }
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

if __name__ == '__main__':
    app.run(debug=True)
