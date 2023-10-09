#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[1]:


get_ipython().system('pip install rdflib')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[2]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example5.rdf", format="xml")


# Create a new class named Researcher

# In[3]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)


# **TASK 6.1: Create a new class named "University"**
# 

# In[4]:


ns = Namespace("http://somewhere#")
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[5]:


g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**

# In[6]:


jane_smith_uri = ns.JaneSmith
g.add((jane_smith_uri, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
  print(s,p,o)


# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**

# In[7]:


g.add((jane_smith_uri, ns.email, Literal("jane.smith@example.com")))
g.add((jane_smith_uri, ns.fullName, Literal("Jane Smith")))
g.add((jane_smith_uri, ns.givenName, Literal("Jane")))
g.add((jane_smith_uri, ns.familyName, Literal("Smith")))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **TASK 6.5: Add UPM as the university where John Smith works**

# In[8]:


john_smith_uri = ns.JohnSmith
g.add((john_smith_uri, ns.worksAt, ns.UPM))

# Visualize the results
for s, p, o in g:
  print(s, p, o)


# **Task 6.6: Add that Jown knows Jane using the FOAF vocabulary**

# In[9]:


foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.add((john_smith_uri, foaf.knows, jane_smith_uri))

# Visualize the results
for s, p, o in g:
  print(s, p, o)

