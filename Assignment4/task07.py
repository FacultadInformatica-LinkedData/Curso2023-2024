# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
# %pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

# %% [markdown]
# First let's read the RDF file

# %%
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
# TO DO
# Visualize the results

ns = Namespace("http://somewhere#")
q1 = """SELECT ?s
WHERE {
  ?s rdfs:subClassOf/rdfs:subClassOf* ns:LivingThing.
}"""

for r in g.query(q1):
 print(r)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO
# Visualize the results

q2 = """SELECT ?s
WHERE {
  ?s rdf:type/rdfs:subClassOf* ns:Person.
}"""

for r in g.query(q2):
 print(r)

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %%
# TO DO
# Visualize the results

q3 = """SELECT ?s ?p ?o
WHERE {
  ?s rdf:type/rdfs:subClassOf* ns:Person.
  ?s ?p ?o.
}"""

for r in g.query(q3):
 print(r)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %%
# TO DO
# Visualize the results

q4 = """SELECT ?s
WHERE {
  ?s rdf:type/rdfs:subClassOf* ns:Person.
  ?s ns:knows ns:Rocky.
}"""

for r in g.query(q4):
    print(r)

# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %%
# TO DO
# Visualize the results

q5 = """SELECT ?s
WHERE {
  ?s rdf:type/rdfs:subClassOf* ns:Person.
  ?s ns:knows ?o.
  ?s ns:knows ?p.
  FILTER(?o != ?p).
}"""

for r in g.query(q5):
    print(r)


