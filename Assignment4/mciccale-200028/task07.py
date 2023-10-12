#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[ ]:


get_ipython().system("pip install rdflib")
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[ ]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

g = Graph()
g.namespace_manager.bind("ns", Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind(
    "vcard", Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False
)
g.parse(github_storage + "/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[ ]:


ns = Namespace("http://somewhere#")
# RDFLib
print("RDFLib Query:")
for s, _, _ in g.triples((None, RDFS.subClassOf, ns.LivingThing)):
    print(s)

# SPARQL
from rdflib.plugins.sparql import prepareQuery

q1 = prepareQuery(
    """
    SELECT ?Subclass
    WHERE {
        ?Subclass RDFS:subClassOf ns:LivingThing .
    }
    """,
    initNs={"RDFS": RDFS, "ns": ns},
)
print("\nSPARQL Query:")
for r in g.query(q1):
    print(r.Subclass)


#

# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
#

# In[ ]:


# RDFLib
print("RDFLib Query:")
for subclass, _, _ in g.triples((None, RDFS.subClassOf, ns.Person)):
    for s, _, _ in g.triples((None, RDF.type, subclass)):
        print(s)

# SPARQL
q2 = prepareQuery(
    """
    SELECT DISTINCT ?Individual
    WHERE {
        ?Subclass RDFS:subClassOf ns:Person .
        ?Individual a ?Subclass .
    }
    """,
    initNs={"RDFS": RDFS, "RDF": RDF, "ns": ns},
)
print("\nSPARQL Query:")
for r in g.query(q2):
    print(r.Individual)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
#

# In[ ]:


# RDFLib
print("RDFLib Query:")
for individual, _, o in g.triples((None, RDF.type, None)):
    if o == ns.Animal or o == ns.Person:
        for _, p, _ in g.triples((individual, None, None)):
            print(f"{individual} {p}")
# SPARQL
q3 = prepareQuery(
    """
    SELECT ?Individual ?Property
    WHERE {
        ?Individual a ?Type .
        ?Individual ?Property ?Value .
    }
    VALUES (?Type) {(ns:Person) (ns:Animal)}
    """,
    initNs={"ns": ns},
)
print("\nSPARQL Query:")
for r in g.query(q3):
    print(r.Individual, r.Property)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[ ]:


foaf = Namespace("http://xmlns.com/foaf/0.1/")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
# RDFLib
print("RDFLib Query:")
for s, _, _ in g.triples((None, foaf.knows, ns.RockySmith)):
    for _, _, name in g.triples((s, vcard.Given, None)):
        print(name)
# SPARQL
q4 = prepareQuery(
    """
    SELECT ?Name
    WHERE {
        ?Individual foaf:knows ns:RockySmith .
        ?Individual vcard:Given ?Name .
    }
    """,
    initNs={"ns": ns, "vcard": vcard, "foaf": foaf},
)
print("\nSPARQL Query:")
for r in g.query(q4):
    print(r.Name)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[ ]:


# RDFLib
print("RDFLib Query:")
found = set()
for i, _, e1 in g.triples((None, foaf.knows, None)):
    for _, _, e2 in g.triples((i, foaf.knows, None)):
        if e1 != e2 and i not in found:
            print(i)
            found.add(i)
# SPARQL
q5 = prepareQuery(
    """
    SELECT ?Individual
    WHERE {
        ?Individual foaf:knows ?Entity1 .
        ?Individual foaf:knows ?Entity2 .
        FILTER (?Entity1 != ?Entity2) .
    }
    GROUP BY ?Individual
    """,
    initNs={"foaf": foaf},
)
print("\nSPARQL Query:")
for r in g.query(q5):
    print(r.Individual)


# In[ ]:
