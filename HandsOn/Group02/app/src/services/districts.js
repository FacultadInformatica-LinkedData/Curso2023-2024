import { runSparqlQuery } from "./sparql.js";
import { parsePoint } from "../utils/pointParser.js";

const endpoint = "http://localhost:9000/api/sparql";
const wikidataEndpoint = "https://query.wikidata.org/sparql";

const getAllNames = async () => {
  const query = `
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/energyConsumption#>
  SELECT DISTINCT ?name WHERE {
    ?sub a ns:District .
    ?sub ns:districtName ?name
  } ORDER BY ASC(?name)`;

  try {
    const response = await runSparqlQuery(endpoint, query);
    return response.results.bindings.map((b) => b.name.value);
  } catch (err) {
    console.error(err);
  }
};

const getWikiDataEntityFromName = async (name) => {
  const query = `
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/energyConsumption#>
  PREFIX owl: <http://www.w3.org/2002/07/owl#>
  SELECT DISTINCT ?wikidataUri WHERE {
    ?district ns:districtName "${name}" .
    ?district owl:sameAs ?wikidataUri .
  }`;

  try {
    const response = await runSparqlQuery(endpoint, query);
    return response.results.bindings[0].wikidataUri.value.split("/").pop();
  } catch (err) {
    console.error(err);
  }
};

const getWikiDataProperties = async (name) => {
  try {
    const entity = await getWikiDataEntityFromName(name);

    const query = `
      PREFIX wd: <http://www.wikidata.org/entity/>
      PREFIX wdt: <http://www.wikidata.org/prop/direct/>
      PREFIX wikibase: <http://wikiba.se/ontology#>
      PREFIX bd: <http://www.bigdata.com/rdf#>

      SELECT ?map ?population ?location WHERE {
        wd:${entity} wdt:P242 ?map .
        wd:${entity} wdt:P1082 ?population .
        wd:${entity} wdt:P625 ?location .
      }`;

    try {
      const { results } = await runSparqlQuery(wikidataEndpoint, query);
      return {
        location: parsePoint(results.bindings[0].location.value),
        map: results.bindings[0].map.value,
        population: results.bindings[0].population.value,
      };
    } catch (err) {
      console.error(err);
      return;
    }
  } catch (err) {
    console.error(err);
  }
};

export { getAllNames, getWikiDataProperties };
