{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "nOOPLCHF7hLB"
      },
      "source": [
        "**Task 07: Querying RDF(s)**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 211
        },
        "id": "Yl9npCt8n6m-",
        "outputId": "096014c0-f1ad-4bd6-bada-ab3561ff1367"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Requirement already satisfied: rdflib in c:\\users\\usuario\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages (7.0.0)\n",
            "Requirement already satisfied: isodate<0.7.0,>=0.6.0 in c:\\users\\usuario\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages (from rdflib) (0.6.1)\n",
            "Requirement already satisfied: pyparsing<4,>=2.1.0 in c:\\users\\usuario\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages (from rdflib) (3.0.9)\n",
            "Requirement already satisfied: six in c:\\users\\usuario\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages (from isodate<0.7.0,>=0.6.0->rdflib) (1.16.0)\n"
          ]
        }
      ],
      "source": [
        "!pip install rdflib\n",
        "github_storage = \"https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2023-2024/master/Assignment4/course_materials\""
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "XY7aPc86Bqoo"
      },
      "source": [
        "First let's read the RDF file"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 35
        },
        "id": "9ERh415on7kF",
        "outputId": "395dc571-ef76-4330-cf4b-0b9db3aa5277"
      },
      "outputs": [
        {
          "data": {
            "text/plain": [
              "<Graph identifier=N533c5a2962be49e48ef596326b7e6a0c (<class 'rdflib.graph.Graph'>)>"
            ]
          },
          "execution_count": 2,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "from rdflib import Graph, Namespace, Literal\n",
        "from rdflib.namespace import RDF, RDFS\n",
        "g = Graph()\n",
        "g.namespace_manager.bind('ns', Namespace(\"http://somewhere#\"), override=False)\n",
        "g.namespace_manager.bind('vcard', Namespace(\"http://www.w3.org/2001/vcard-rdf/3.0#\"), override=False)\n",
        "g.parse(github_storage+\"/rdf/example6.rdf\", format=\"xml\")"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "qp1oe2Eddsvo"
      },
      "source": [
        "**TASK 7.1: List all subclasses of \"LivingThing\" with RDFLib and SPARQL**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 7,
      "metadata": {
        "id": "tRcSWuMHOXBl"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "http://somewhere#Person\n",
            "http://somewhere#Animal\n"
          ]
        }
      ],
      "source": [
        "from rdflib.plugins.sparql import prepareQuery\n",
        "#print(g.serialize(format=\"ttl\"))   #para saber un poco como se definen\n",
        "# TO DO\n",
        "q1 = prepareQuery('''\n",
        "  PREFIX rdf:<http://www.w3.org/2000/01/rdf-schema#>\n",
        "  PREFIX ns:<http://somewhere#>               \n",
        "  SELECT ?Subject WHERE { \n",
        "    ?Subject rdf:subClassOf ns:LivingThing. \n",
        "  }\n",
        "  '''\n",
        ")\n",
        "# Visualize the results\n",
        "for r in g.query(q1):\n",
        "  print(r.Subject)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "gM3DASkTQQ5Y"
      },
      "source": [
        "**TASK 7.2: List all individuals of \"Person\" with RDFLib and SPARQL (remember the subClasses)**\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 30,
      "metadata": {
        "id": "LiKSPHRzS-XJ"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "http://somewhere#SaraJones\n",
            "http://somewhere#JohnSmith\n",
            "http://somewhere#JaneSmith\n",
            "http://somewhere#JimGonzalez\n"
          ]
        }
      ],
      "source": [
        "# TO DO\n",
        "q1 = prepareQuery('''\n",
        "  PREFIX rdf:<http://www.w3.org/2000/01/rdf-schema#>\n",
        "  PREFIX ns:<http://somewhere#>               \n",
        "  SELECT DISTINCT ?Subject WHERE { \n",
        "    {?Subject a ns:Person.} UNION {?SubClass rdf:subClassOf ns:Person. ?Subject a ?SubClass}\n",
        "  }\n",
        "  '''\n",
        ")\n",
        "# Visualize the results\n",
        "for r in g.query(q1):\n",
        "  print(r.Subject)\n"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "MXBqtBkJd22I"
      },
      "source": [
        "**TASK 7.3: List all individuals of \"Person\" or \"Animal\" and all their properties including their class with RDFLib and SPARQL. You do not need to list the individuals of the subclasses of person**\n"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 28,
      "metadata": {
        "id": "APQGv3NHX8Tf"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "http://somewhere#SaraJones http://www.w3.org/1999/02/22-rdf-syntax-ns#type\n",
            "http://somewhere#SaraJones http://www.w3.org/2001/vcard-rdf/3.0/Given\n",
            "http://somewhere#SaraJones http://www.w3.org/2001/vcard-rdf/3.0/FN\n",
            "http://somewhere#SaraJones http://www.w3.org/2001/vcard-rdf/3.0/Family\n",
            "http://somewhere#SaraJones http://xmlns.com/foaf/0.1/knows\n",
            "http://somewhere#JohnSmith http://www.w3.org/1999/02/22-rdf-syntax-ns#type\n",
            "http://somewhere#JohnSmith http://www.w3.org/2001/vcard-rdf/3.0/Given\n",
            "http://somewhere#JohnSmith http://www.w3.org/2001/vcard-rdf/3.0/FN\n",
            "http://somewhere#JohnSmith http://www.w3.org/2001/vcard-rdf/3.0/Family\n",
            "http://somewhere#RockySmith http://www.w3.org/1999/02/22-rdf-syntax-ns#type\n",
            "http://somewhere#RockySmith http://www.w3.org/2001/vcard-rdf/3.0/Given\n",
            "http://somewhere#RockySmith http://www.w3.org/2001/vcard-rdf/3.0/FN\n",
            "http://somewhere#RockySmith http://www.w3.org/2001/vcard-rdf/3.0/Family\n",
            "http://somewhere#RockySmith http://xmlns.com/foaf/0.1/knows\n"
          ]
        }
      ],
      "source": [
        "# TO DO\n",
        "q1 = prepareQuery('''\n",
        "  PREFIX ns:<http://somewhere#>               \n",
        "  SELECT DISTINCT ?Subject ?Predicade WHERE { \n",
        "    {?Subject a ns:Person.\n",
        "     ?Subject ?Predicade []. } \n",
        "    UNION \n",
        "    {?Subject a ns:Animal.\n",
        "     ?Subject ?Predicade [].}\n",
        "  }\n",
        "  '''\n",
        ")\n",
        "# Visualize the results\n",
        "for r in g.query(q1):\n",
        "  print(r.Subject, r.Predicade)\n",
        "  #print(r.Subject +\"  \"+ r.Predicade)      #Asi me sale de una forma extranna"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "3NyI7M2VNr9R"
      },
      "source": [
        "**TASK 7.4:  List the name of the persons who know Rocky**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 26,
      "metadata": {
        "id": "I_CNoIKdNpbx"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "Sara Jones\n",
            "Jane Smith\n"
          ]
        }
      ],
      "source": [
        "# TO DO\n",
        "q1 = prepareQuery('''\n",
        "  PREFIX vcard-rdf:<http://www.w3.org/2001/vcard-rdf/3.0/>\n",
        "  PREFIX foaf:<http://xmlns.com/foaf/0.1/>\n",
        "  PREFIX ns:<http://somewhere#>               \n",
        "  SELECT ?Name WHERE { \n",
        "    ?Subject foaf:knows ns:RockySmith.\n",
        "    ?Subject vcard-rdf:FN ?Name\n",
        "  }\n",
        "  '''\n",
        ")\n",
        "# Visualize the results\n",
        "for r in g.query(q1):\n",
        "  print(r.Name)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "kyjGsyxDPa2C"
      },
      "source": [
        "**Task 7.5: List the entities who know at least two other entities in the graph**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 32,
      "metadata": {
        "id": "yoVwVZUAPaLm"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "http://somewhere#RockySmith\n",
            "http://somewhere#SaraJones\n",
            "http://somewhere#JaneSmith\n"
          ]
        }
      ],
      "source": [
        "#revisar!!!!\n",
        "# TO DO\n",
        "q1 = prepareQuery('''\n",
        "  PREFIX vcard-rdf:<http://www.w3.org/2001/vcard-rdf/3.0/>\n",
        "  PREFIX foaf:<http://xmlns.com/foaf/0.1/>\n",
        "  PREFIX ns:<http://somewhere#>               \n",
        "  SELECT DISTINCT ?Subject WHERE { \n",
        "    ?Subject foaf:knows ?Person1, ?Person2.\n",
        "  }\n",
        "  '''\n",
        ")\n",
        "# Visualize the results\n",
        "for r in g.query(q1):\n",
        "  print(r.Subject)"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.9.5"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
