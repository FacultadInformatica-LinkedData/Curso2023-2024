#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# First let's read the RDF file

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")


# **TASK 7.1: List all subclasses of "LivingThing" with RDFLib and SPARQL**

# In[3]:


ns = Namespace("http://somewhere#")
q1 = """
    SELECT ?subClass
    WHERE {
        ?subClass rdfs:subClassOf ns:LivingThing .
    }
"""

# Visualize the results
for row in g.query(q1):
    print(row.subClass)


# **TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**
# 

# In[4]:


q2 = """
    SELECT ?individual
    WHERE {
        ?individual rdf:type/rdfs:subClassOf* ns:Person.
    }
"""

# Visualize the results
for row in g.query(q2):
    print(row.individual)


# **TASK 7.3: List all individuals of "Person" or "Animal" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**
# 

# In[5]:


q3 = """
    SELECT ?individual ?property ?value
    WHERE {
        {
        ?individual a ns:Person .
        }
        UNION
        {
        ?individual a ns:Animal .
        }
        ?individual ?property ?value .
    }
"""

# Visualize the results
for row in g.query(q3):
    print(row.individual, row.property, row.value)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[6]:


q4 = """
    SELECT ?name
    WHERE {
      ?person rdf:type ns:Person.
      ?person ns:knows ?known.
      ?person ns:fullName ?name.
      ?known ns:fullName "Rocky".
    }
"""

# Visualize the results
for row in g.query(q4):
    print(row.personName)


# **Task 7.5: List the entities who know at least two other entities in the graph**

# In[7]:


q5 = """
    SELECT ?entity ?count
    WHERE {
    {
        SELECT ?entity (COUNT(?known) AS ?count)
        WHERE {
            ?entity ns:knows ?known.
        }   GROUP BY ?entity
    }
    FILTER (?count >= 2)
    }
"""

# Visualize the results
for row in g.query(q5):
    print(row.entity)

