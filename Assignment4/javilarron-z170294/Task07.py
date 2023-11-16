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
        ?subClass rdfs:subClassOf* ns:LivingThing .
    }
"""

living_thing_subclasses = list(g.transitive_subjects(RDFS.subClassOf, ns.LivingThing))

# Visualize the results
print("\nTASK 7.1 Results with RDFLib:")
for subclass in living_thing_subclasses:
    print(subclass)

print("\nTASK 7.1 Results with SPARQL:")
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

person_individuals = list(g.subjects(RDF.type, ns.Person))
person_subclasses = list(g.subjects(RDFS.subClassOf, ns.Person))
for subclass in person_subclasses:
    person_individuals.extend(list(g.subjects(RDF.type, subclass)))

# Visualize the results
print("\nTASK 7.2 Results with RDFLib:")
for individual in person_individuals:
    print(individual)

print("\nTASK 7.2 Results with SPARQL:")
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

person_animal_individuals = set()
for person in g.subjects(RDF.type, ns.Person):
    person_animal_individuals.add(person)

for animal in g.subjects(RDF.type, ns.Animal):
    person_animal_individuals.add(animal)

# Visualize the results
print("\nTASK 7.3 Results with RDFLib:")
for individual in person_animal_individuals:
    properties = g.predicate_objects(individual)
    for prop, value in properties:
        print(individual, prop, value)
        
print("\nTASK 7.3 Results with SPARQL:")

for row in g.query(q3):
    print(row.individual, row.property, row.value)


# **TASK 7.4:  List the name of the persons who know Rocky**

# In[6]:


q4 = """
    SELECT ?personName
    WHERE {
      ?person rdf:type ns:Person.
      ?person <http://xmlns.com/foaf/0.1/knows> <http://somewhere#RockySmith>.
      ?person <http://www.w3.org/2001/vcard-rdf/3.0/FN> ?personName.
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
            ?entity <http://xmlns.com/foaf/0.1/knows> ?known.
        }   GROUP BY ?entity
    }
    FILTER (?count >= 2)
    }
"""

# Visualize the results
for row in g.query(q5):
    print(row.entity)

