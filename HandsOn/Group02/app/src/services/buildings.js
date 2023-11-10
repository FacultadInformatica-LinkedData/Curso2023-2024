import { runSparqlQuery } from "./sparql.js";

const getAllNames = async () => {
  const query = `
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/energyConsumption#>
  SELECT DISTINCT ?name WHERE {
    ?sub a ns:Building .
    ?sub ns:buildingName ?name
  }
  `;
  const response = await runSparqlQuery(query);
  return response.results.bindings.map((b) => b.name.value);
};

export { getAllNames };
