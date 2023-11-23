# %% [markdown]
# **Task 07: Querying RDF(s)**

# %%
%pip install rdflib
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



ns =Namespace("http://somewhere#")

# %% [markdown]
# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# %%
# TO DO
# Visualize the results

for s,p,o in g.triples((None,RDFS.subClassOf,ns.LivingThing)):
    print(s)


# %%
from rdflib.plugins.sparql import prepareQuery


q1 = prepareQuery('''
  SELECT ?subclass WHERE { 
    ?subclass rdfs:subClassOf ns:LivingThing. 
  }
  ''',initNs = { "ns": Namespace("http://somewhere#"),"rdfs": RDFS}
)


for r in g.query(q1):
  print(r.subclass)

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
# TO DO
# Visualize the results

def list_elems_recursive(elem):
    results =[]
    classes=[elem]
    while classes:
        elem = classes.pop()
        for s,p,o in g.triples((None,RDF.type,elem)):
            results.append((s,p,o))
        for s,p,o in g.triples((None,RDFS.subClassOf,elem)):
            classes.append(s)
    return results



for elem in list_elems_recursive(ns.Person):
    print(elem[0])
    
    
    
for s, p, o in g:
    print(s,p,o)

       

# %%
q1 = prepareQuery('''
  SELECT ?individual  WHERE { 
    
    {
      ?individual rdf:type ?subclass.
      optional{?subclass rdfs:subClassOf ?subclass.}
      ?subclass rdfs:subClassOf ns:Person
    }
    UNION
    {
      ?individual rdf:type ns:Person.
    }
    
  }
  ''',initNs = { "ns": Namespace("http://somewhere#"),"rdfs": RDFS,"rdf":RDF}
)


for r in g.query(q1):
  print(r.individual)



# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %%
# TO DO
# Visualize the results

for elem,p,o in g.triples((None,RDF.type,ns.Person)):
    print("Element:",elem)
    for s,p,o in g.triples((elem,None,None)):
        print("Propertie:",p,o)
for elem,p,o in g.triples((None,RDF.type,ns.Animal)):
    print("Element:",elem)
    for s,p,o in g.triples((elem,None,None)):
        print("Propertie:",p,o)

# %%
q1 = prepareQuery('''
  SELECT distinct ?individual ?property ?value WHERE {   
    {
      ?individual rdf:type ns:Person.
      ?individual ?property ?value
    }
    UNION
    {
      ?individual rdf:type ns:Animal.
      ?individual ?property ?value
    }
      
  }
  ''',initNs = { "ns": Namespace("http://somewhere#"),"rdfs": RDFS,"rdf":RDF}
)


for r in g.query(q1):
  print(r.individual,r.property,r.value)

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %%
# TO DO
# Visualize the results
from rdflib import FOAF
#con el # no funciona si imprimes todo el grafo esta con / no con #
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
rocky =ns.RockySmith
for person,p,o in g.triples((None,FOAF.knows,rocky)):
    print(g.value(subject=person, predicate=VCARD.Given, object=None))
    


# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %%
# TO DO
# Visualize the results
for person,p,o in g.triples((None,FOAF.knows,None)):
  list=[]
  for elem in g.triples((person,FOAF.knows,None)):
    list.append(elem[2])
  if len(list)>=2 :
    for elem in list:
      print(person,"knows",elem)
  print("")




