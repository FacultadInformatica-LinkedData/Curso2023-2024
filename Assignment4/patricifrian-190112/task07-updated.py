# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zZUeTCp-VpsiVugt0e6UXlnV26GOvBAb

**Task 07: Querying RDF(s)**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"

"""First let's read the RDF file"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**"""

# TO DO
from rdflib.plugins.sparql import prepareQuery
ns = Namespace("http://somewhere#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")

# Using RDFLib
print("Print results using RDFLib")
for s, p, o in g.triples((None, rdfs.subClassOf, ns.LivingThing)):
    print(s)
    for q, p, o in g.triples((None, rdfs.subClassOf, s)):
      print("Subclass:"+q)

# Using SPARQL
q1 = prepareQuery('''
  SELECT ?Subject ?Subclass WHERE {
    ?Subject rdfs:subClassOf ns:LivingThing .
    OPTIONAL {?Subclass rdfs:subClassOf ?Subject .}
  }
  ''',
  initNs={"vcard": vcard, "rdfs": rdfs, "ns": ns}
)
print("\nPrint results using SPARQL:")
for row in g.query(q1):
    print(row.Subject)
    if row.Subclass:
        print("Subclass:" + row.Subclass)
    else:
        print()

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
# Using RDFLib
print("Print results using RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for sub, p, o in g.triples((None,RDFS.subClassOf,ns.Person)):
  for s, p, o in g.triples((None,RDF.type,sub)):
    print(s)

# Using SPARQL
q1 = prepareQuery('''
  SELECT ?individual WHERE {
    ?individual rdf:type/rdfs:subClassOf* ns:Person
  }
  ''',
  initNs={"rdfs": rdfs, "rdf": RDF, "ns": ns}
)

print("\nPrint results using SPARQL:")
for r in g.query(q1):
    print(r.individual)

"""**TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**

"""

# TO DO
# Using RDFLib
print("Print results using RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
    print(f"Individual: {s}")
    for s2, p2, o2 in g.triples((s, None, None)):
        print(f"  Property: {p2} - Value: {o2}")

for s, p, o in g.triples((None, RDF.type, ns.Animal)):
    print(f"Individual: {s}")
    for s2, p2, o2 in g.triples((s, None, None)):
        print(f"  Property: {p2} - Value: {o2}")

# Using SPARQL
q1 = prepareQuery('''
  SELECT ?individual ?property ?value WHERE {
    {
      ?individual rdf:type ns:Person .
      ?individual ?property ?value .
    }
    UNION
    {
      ?individual rdf:type ns:Animal .
      ?individual ?property ?value .
    }
  }
  ''',
  initNs={"rdf": RDF, "ns": ns}
)

print("\nPrint results using SPARQL:")
for r in g.query(q1):
    print(f"Individual: {r.individual}")
    print(f"  Property: {r.property} - Value: {r.value}")

"""**TASK 7.4:  List the name of the persons who know Rocky**"""

# TO DO
# Using RDFLib
print("Print results using RDFLib:")
print("Persons who know Rocky:")
for s,p,o in g.triples((None, FOAF.knows, ns.RockySmith)):
    for s, p, o in g.triples((s, vcard.FN, None)):
        print(o)

# Using SPARQL
from rdflib import FOAF
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")

q1 = prepareQuery('''
  SELECT ?Subject WHERE {
    ?Person foaf:knows ns:RockySmith .
    ?Person vcard:FN ?Subject.
  }
  ''',
  initNs={"foaf": FOAF, "vcard": vcard, "ns": ns}
)
# Visualize the results
print("\nPrint results using SPARQL:")
print("Persons who know Rocky:")
for r in g.query(q1):
    print(r.Subject)

"""**Task 7.5: List the entities who know at least two other entities in the graph**"""

# TO DO
# Using RDFLib
print("Print results using RDFLib")
print("Entities who know at least two others:")
known = {}
for subject, predicate, object in g.triples((None, foaf.knows, None)):
    if subject not in known:
        known[subject] = 1
    else:
        known[subject] += 1
# Filter and print entities who know at least two others
for entity, count in known.items():
    if count >= 2:
        print(entity)

# Using SPARQL
q1 = prepareQuery('''
  SELECT ?entity WHERE {
    {
      ?entity foaf:knows ?known1 .
      ?entity foaf:knows ?known2 .
      FILTER (?known1 != ?known2)
    }
  }
  GROUP BY ?entity
  ''',
  initNs={"foaf": foaf, "ns": ns}
)
# Visualize the results

print("\nPrint results using SPARQL:")
print("Entities who know at least two others:")
for r in g.query(q1):
    print(r.entity)