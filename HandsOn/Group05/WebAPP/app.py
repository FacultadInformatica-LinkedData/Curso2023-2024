from flask import Flask, render_template, request
from rdflib import Graph, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery

app = Flask(__name__)

g = Graph()
g.parse('../rdf/data-with-links.ttl', format="ttl")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['GET'])
def quers():
    cons = request.args.get("textbox")

    query = prepareQuery(cons)
    result = g.query(query)

    field_values = result.vars
    field_names = [str(value) for value in field_values]

    results_lists = []
    for row in result:
        row_from_list = []
        for value in row: 
            row_from_list.append(str(value))
        results_lists.append(row_from_list)
    
    return render_template('result.html', results_lists= results_lists, field_names= field_names)

@app.route('/ontology')
def onto():
    return render_template('ontology.html')

if __name__ == '__main__':
    app.run(debug=True)
