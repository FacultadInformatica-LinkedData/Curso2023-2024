# -*- coding: utf-8 -*-
"""Task04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xABnoS2LqlHJCG-fdP0o0KCF6mHoOuH2

**Task 04: Graph querying**
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal
g = Graph()
g.parse(github_storage+"/rdf/example3.rdf", format="xml")

"""Listamos todos los recursos que contienen la propiedad VCARD:FN"""

from rdflib.plugins.sparql import prepareQuery


VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0#")


q1 = prepareQuery('''
  SELECT ?Subject ?FullName WHERE {
    ?Subject vcard:FN ?FullName.
  }
  ''',
  initNs = { "vcard": VCARD}
)


for r in g.query(q1):
  print(r.FullName)

"""Repetimos la anterior consulta, pero pidiendo ahora además los nombres completos de los sujetos"""

q2 = prepareQuery('''
  SELECT ?Subject ?FullName WHERE {
    ?Subject vcard:FN ?FullName.
  }
  ''',
  initNs = { "vcard": VCARD}
)

for r in g.query(q2):
  print(r.Subject, r.FullName)

"""Obtenemos todos los recursos que contienen "Smith" como nombre de familia"""

from rdflib import XSD

q3 = prepareQuery('''
 SELECT ?Subject WHERE {
   ?Subject vcard:Family ?Family.
  }
  ''',
#q3 = prepareQuery('''
#  SELECT ?Subject WHERE {
#    prefix xsd: <http://www.w3.org/2001/XMLSchema>
#    ?Subject vcard:Family "Smith"^^xsd:String.
#  }
#  ''',


  initNs = { "vcard": VCARD}
)

#for r in g.query(q3):
for r in g.query(q3, initBindings = {'?Family' : Literal('Smith', datatype=XSD.string)}):
  print(r)

"""Obtenemos todos los elementos que contienen un email asociado"""

from rdflib import FOAF

q4 = prepareQuery('''
  SELECT ?Subject ?Email WHERE {
    ?Subject foaf:email ?Email.
  }
  ''',
  initNs = { "foaf": FOAF}
)

for r in g.query(q4):
  print(r.Subject,r.Email)

"""Consultamos todos los que conocen (FOAF:knows) a "Jane Smith" y obtenemos sus nombres de pila (VCARD:Given)"""

q5 = prepareQuery('''
  SELECT  ?Subject ?Given  WHERE {
    ?Subject foaf:knows ?JaneSmith.
	?JaneSmith vcard:FN ?JaneSmithFullName.
	?Subject vcard:Given ?Given.
  }
  ''',
  initNs = { "foaf": FOAF, "vcard": VCARD, "xsd":XSD}
)

for r in g.query(q5, initBindings = {'?JaneSmithFullName' : Literal('Jane Smith', datatype=XSD.string)}):
  print(r.Subject, r.Given)
