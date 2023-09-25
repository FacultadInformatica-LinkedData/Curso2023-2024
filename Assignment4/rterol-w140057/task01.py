# -*- coding: utf-8 -*-
"""Task01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13Z4_g4h0x8kZtU_yDdb-Bc7K-ht39mkb

**Task 01: Reading and writing RDF files**

Leer y escribir ficheros que contienen tripletas es muy sencillo en RDFlib, para ello vamos a emplear dos métodos de la librería: parse y serialize.
"""

!pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

from rdflib import Graph, Namespace, Literal
g = Graph()

"""Podemos añadir tripletas a nuestro grafo empleando serialize, que leerá el recurso proporcionado. Debemos además indicarle el formato si este no puede ser inferido."""

g.parse(github_storage+"/rdf/example1.rdf", format="xml")

"""El recurso puede ser local o remoto, como en nuestro caso. El resultado es el mismo. Podemos añadir todos los datos que queramos a nuestro grafo, los datos simplemente se irán fusionando.

"""

g.parse(github_storage+"/rdf/example2.rdf", format="xml")

"""Ahora podemos comprobar el resultado volcando las tripletas de forma sencilla."""

for subj, pred, obj in g:
  print(subj,pred,obj)

"""Ahora podemos ver la operación inversa, serializando estos datos a algún formato que nos lo permita. Este proceso también nos permite una conversión sencilla entre formatos."""

print(g.serialize(format="ttl"))

print(g.serialize(format="xml"))

"""También podemos guardar el resultado serializado en un fichero, puedes ver este fichero resultante en el panel izquierdo.

"""

g.serialize("example1.ttl", format="ttl")

g.parse(github_storage+"/rdf/example2.rdf", format="xml")
g.parse(github_storage+"/rdf/example1.rdf", format="xml")

