from flask import Flask, render_template, abort, redirect, request, url_for
from owlready2 import *

# Load the ontology
onto = get_ontology("repair_ontology.owl").load()

app = Flask(__name__)

@app.route('/')
def index():
    items_info = []
    for item in onto.Item.instances():
        if not isinstance(item, onto.Tool) and not isinstance(item, onto.Part):
            item_data = {
                "name": item.name,
                "has_procedure": [procedure for procedure in item.has_procedure],
                "part_of": [part.name for part in item.part_of] if item.part_of else [],
                "errors": []
            }
            for procedure in item_data['has_procedure']:
                if not procedure.has_step:
                    item_data['errors'].append(f"Procedure '{procedure.has_title[0]}' has no steps.")
                if not procedure.has_tool:
                    item_data['errors'].append(f"Procedure '{procedure.has_title[0]}' has no tools.")
            items_info.append(item_data)
    return render_template('index.html', items=items_info)

@app.route('/procedure/<string:procedure_title>')
def procedure_detail(procedure_title):
    procedures = [proc for proc in onto.Procedure.instances() if procedure_title in proc.has_title]
    if not procedures:
        abort(404)
    procedure = procedures[0]
    return render_template('procedure_detail.html', procedure=procedure)

@app.route('/add_procedure', methods=['POST'])
def add_procedure():
    item_name = request.form.get('item_name')
    procedure_title = request.form.get('procedure_title')
    step_titles = request.form.getlist('step_titles')
    step_images = request.form.getlist('step_images')
    tool_titles = request.form.getlist('tool_titles')

    item = next((i for i in onto.Item.instances() if i.name == item_name), None)
    procedure = next((p for p in onto.Procedure.instances() if p.has_title and p.has_title[0] == procedure_title), None)

    if procedure is None:
        procedure = onto.Procedure(sanitize_uri(f"Procedure_{procedure_title}"))
        procedure.has_title.append(procedure_title)

    for i, step_title in enumerate(step_titles):
        step_title = step_title.strip()
        if step_title:
            existing_step = next((s for s in onto.Step.instances() if s.has_title and s.has_title[0] == step_title), None)
            if existing_step is None:
                step = onto.Step(sanitize_uri(f"Step_{step_title}"))
                step.has_title.append(step_title)
                procedure.has_step.append(step)

                # Add images to the step if provided
                if i < len(step_images):
                    image_urls = step_images[i].split(',')  # Assuming multiple URLs can be provided, comma-separated
                    for image_url in image_urls:
                        image_url = image_url.strip()
                        if image_url:
                            image_instance = onto.Image(image_url)
                            step.has_image.append(image_instance)

    for tool_title in tool_titles:
        tool_title = tool_title.strip()
        if tool_title:
            existing_tool = next((t for t in onto.Tool.instances() if t.has_title and t.has_title[0] == tool_title), None)
            if existing_tool is None:
                tool = onto.Tool(sanitize_uri(f"Tool_{tool_title}"))
                tool.has_title.append(tool_title)
                procedure.has_tool.append(tool)

    if item:
        item.has_procedure.append(procedure)

    onto.save(file="repair_ontology.owl", format="rdfxml")
    return redirect(url_for('index'))


@app.route('/remove_procedure', methods=['POST'])
def remove_procedure():
    item_name = request.form.get('item_name')
    procedure_title = request.form.get('procedure_title')

    item = next((i for i in onto.Item.instances() if i.name == item_name), None)
    if item:
        procedure = next((p for p in item.has_procedure if p.has_title and p.has_title[0] == procedure_title), None)
        if procedure:
            item.has_procedure.remove(procedure)
            onto.save(file="repair_ontology.owl", format="rdfxml")

    return redirect(url_for('index'))



def sanitize_uri(text):
    return text.replace(" ", "_")

if __name__ == '__main__':
    app.run(debug=True)
