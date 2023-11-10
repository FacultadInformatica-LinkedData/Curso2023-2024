import json

from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint

sparql = SPARQLWrapper("http://localhost:9000/api/sparql" "https://query.wikidata.org/sparql")

query = '''
      select ?prop ?obj where{
        <http://www.wikidata.org/entity/Q106421316> ?prop ?obj.
      }
      limit 20
'''

query2 = '''
      select ?subj where{
        ?suj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://smart.city.linkeddata.es/lcc/ontology/G5O#Counter>.
        ?suj <http://smart.city.linkeddata.es/lcc/ontology/G5O#locatedIn> ?other.
        ?other <http://www.w3.org/2002/07/owl#sameAs> ?subj.
      }
      limit 13
'''

query33 = '''
SELECT ?subj ?prop
WHERE {
  ?suj <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://smart.city.linkeddata.es/lcc/ontology/G5O#Counter>.
  ?suj <http://smart.city.linkeddata.es/lcc/ontology/G5O#locatedIn> ?other.
  ?other <http://www.w3.org/2002/07/owl#sameAs> ?subj.
  ?subj ?prop ?obj.
}
limit 10
'''

sparql.setQuery(query2)
sparql.setReturnFormat(JSON)

results = sparql.queryAndConvert()

pprint(results)

print("-------------------------")

json_string = results.decode('utf-8')
json_obj = json.loads(json_string)

pprint(json_obj)

for r in json_obj["results"]["bindings"]:
  print(f"Subj: {r['subj']['value']}")
  #print(f"Prop: {r['prop']['value']} | Value: {r['obj']['value']}")