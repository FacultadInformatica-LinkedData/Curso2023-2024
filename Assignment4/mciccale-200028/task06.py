#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[ ]:


get_ipython().system("pip install rdflib")
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials"


# Read the RDF file as shown in class

# In[ ]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS

g = Graph()
g.namespace_manager.bind("ns", Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind(
    "vcard", Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False
)
g.parse(github_storage + "/rdf/example5.rdf", format="xml")


# Create a new class named Researcher

# In[ ]:


ns = Namespace("http://somewhere#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
    print(s, p, o)


# **TASK 6.1: Create a new class named "University"**
#

# In[ ]:


# TO DO
g.add((ns.University, RDF.type, RDFS.Class))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **TASK 6.2: Add "Researcher" as a subclass of "Person"**

# In[ ]:


# TO DO
g.add((ns.Researcher, RDFS.subClassOf, ns.Person))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **TASK 6.3: Create a new individual of Researcher named "Jane Smith"**

# In[ ]:


# TO DO
g.add((ns.JaneSmith, RDF.type, ns.Researcher))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **TASK 6.4: Add to the individual JaneSmith the email address, fullName, given and family names**

# In[ ]:


# TO DO
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
g.add((ns.JaneSmith, vcard.Email, Literal("jsmith@example.org")))
g.add((ns.JaneSmith, vcard.FN, Literal("Jane Smith")))
g.add((ns.JaneSmith, vcard.Given, Literal("Jane")))
g.add((ns.JaneSmith, vcard.Family, Literal("Smith")))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **TASK 6.5: Add UPM as the university where John Smith works**

# In[ ]:


# TO DO
g.add((ns.UPM, RDF.type, ns.University))
g.add((ns.JohnSmith, vcard.Works, ns.UPM))
# Visualize the results
for s, p, o in g:
    print(s, p, o)


# **Task 6.6: Add that John knows Jane using the FOAF vocabulary**

# In[ ]:


# TO DO
foaf = Namespace("http://xmlns.com/foaf/0.1/")
g.add((ns.JohnSmith, foaf.knows, ns.JaneSmith))
# Visualize the results
for s, p, o in g:
    print(s, p, o)
