from rdflib.plugins.sparql import prepareQuery
from rdflib import Graph

g = Graph()

g.parse("soluc.nt", format="ttl")

q1 = prepareQuery('''
    SELECT ?counter
WHERE {
  ?counter <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://smart.city.linkeddata.es/lcc/ontology/G5O#Counter> .
}
''')

q2 = prepareQuery('''
      select ?prop ?value where{
        SERVICE <https://query.wikidata.org/sparql> {
        <http://www.wikidata.org/entity/Q106421316> ?prop ?value.
        }
      }
                  limit 10
''')

q3 = prepareQuery('''
      select ?subj where{
        SERVICE <http://localhost:9000/api/sparql> {
        ?subj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://smart.city.linkeddata.es/lcc/ontology/G5O#Counter>.
        }
      }
                  limit 3
''')

q33 = prepareQuery(
    '''
SELECT ?subj ?prop
WHERE {
  ?suj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://smart.city.linkeddata.es/lcc/ontology/G5O#Counter>.
  ?suj <http://smart.city.linkeddata.es/lcc/ontology/G5O#locatedIn> ?other.
  ?other <http://www.w3.org/2002/07/owl#sameAs> ?subj.
  SERVICE <https://query.wikidata.org/sparql> {
        ?subj ?prop ?obj.
  }
}
limit 10
'''
)

#print(g.serialize("txt"))

for i in g.query(q33):
    print(i.subj, i.prop)