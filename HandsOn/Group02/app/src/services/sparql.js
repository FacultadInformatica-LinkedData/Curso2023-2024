const runSparqlQuery = async (endpoint, query) => {
  const fullUrl = `${endpoint}?query=${encodeURIComponent(query)}`;
  const headers = { Accept: "application/sparql-results+json" };

  try {
    const res = await fetch(fullUrl, { headers });
    if (!res.ok) {
      console.error(`SPARQL query failed with status: ${res.status}`);
      return;
    }
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(`SPARQL query network error: ${err}`);
  }
};

export { runSparqlQuery };
