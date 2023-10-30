# **Task 07: Querying RDF(s)**

# %%
!pip install rdflib
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
ns = Namespace("http://somewhere#")
# RDFlib
for s,p,o in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
  print(s)

# SPARQL
# Used asterisk to capture all subclass levels, only Person and Animal were showing
q1 = """
SELECT ?s
WHERE {
  ?s rdfs:subClassOf/rdfs:subClassOf* ns:LivingThing.
}
"""
for r in g.query(q1):
  print(r[0])

# %% [markdown]
# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# %%
#RDFlib
for s, _, o in g.triples((None, RDFS.subClassOf, ns.Person)):
     for s1, _, _ in g.triples((None, RDF.type, s)):
         print(s1)


# %%
# SPARQL
q2 = """
 PREFIX ns: <http://somewhere#>
 SELECT DISTINCT ?s1
 WHERE {
   ?s rdfs:subClassOf ns:Person .
   ?s1 a ?s .
 }
 """
for r in g.query(q2):
  print(r[0])

# %% [markdown]
# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# %%
# RDFlib
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDF.type, None)):
  if o == ns.Person or o == ns.Animal:
    print(s,p)


# %%
# SPARQL
q3 = """
 PREFIX ns: <http://somewhere#>
 SELECT ?s ?p ?o
 WHERE {
   { 
    ?s ?p ns:Person.
    ?s ?p ?o.
   }
   UNION
   { 
    ?s ?p ns:Animal.
    ?s ?p ?o.
   }
 }
 """
# Can´t solve this one 
for r in g.query(q3):
  print(r[0],r[1],r[2])

# %% [markdown]
# **TASK 7.4:  List the name of the persons who know Rocky**

# %%
# RDFlib
ns = Namespace("http://somewhere#")
from rdflib import FOAF
for s,p,o in g.triples((None, FOAF.knows,ns.RockySmith)):
    only_name = s.split('#')[1]
    print(only_name)
 
# Only printed Names without ns prefix

# %%
# SPARQL
q4 = """
  PREFIX ns: <http://somewhere#>
  PREFIX foaf: <http://xmlns.com/foaf/0.1/>
  PREFIX vcard: <http://www.w3.org/2001/vcard-rdf/3.0/>
  PREFIX ns: <http://somewhere#>
 SELECT ?s ?name
 WHERE {
   ?s foaf:knows ns:RockySmith.
    ?s vcard:Given ?name .
 }
  """
for r in g.query(q4):
  print(r[1]) # Printing only name 

# %% [markdown]
# **Task 7.5: List the entities who know at least two other entities in the graph**

# %%
# RDFlib
ns = Namespace("http://somewhere#")
from rdflib import FOAF
entities = set()
for s,p,o in g.triples((None, FOAF.knows, None)):
  for s1,p1,o1 in g.triples((o, FOAF.knows, None)):
        if s1 not in entities:
            print(s1)
            entities.add(s1)
    
# How to avoid entity repetition? 

# %%
# SPARQL
q5 = """
 PREFIX ns: <http://somewhere#>
 SELECT  distinct ?s
 WHERE {
   ?s foaf:knows ?o.
   ?o foaf:knows ?s.
 }
 """
for r in g.query(q5):
  print(r[0])


