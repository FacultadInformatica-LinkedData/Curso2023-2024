import re
from re import U
import rdflib
from rdflib.plugins.sparql import prepareQuery
from SPARQLWrapper import SPARQLWrapper, JSON
import time

def query1():
    #QUERY DE Devuelve las direcciones de los parques en cuyos distritos no hay ese tipo de árbol
    arbol = "Ligustrum japonicum"

    # Definir la URL de tus datos RDF en GitHub
    data_url = "https://raw.githubusercontent.com/aom20021/Curso2023-2024/master/HandsOn/Group10/rdf/result-with-links.ttl"

    # Crear un objeto Graph y cargar los datos desde la URL
    g = rdflib.Graph()
    g.parse(data_url, format="turtle")

    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
    PREFIX base: <http://base.itree.com/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?numDistrito ?direccion ?wikidataBarrio ?nomBarrio WHERE {{

    ?parques a base:Parque_Canino.
    ?parques base:hasDireccion ?direccion.
    ?parques base:hasDistrito ?numDistrito.
    ?barrio a base:Barrio.
    ?barrio base:hasDistrito ?numDistrito.
    ?barrio owl:sameAs ?wikidataBarrio.
    ?barrio rdfs:label ?nomBarrio.
    #?parques owl:sameAs ?wikidataDireccion.
    ?parques base:hasBarrio ?numBarrio.
    ?barrio base:numBarrio ?numBarrio.
    
    FILTER NOT EXISTS {{
        ?arbol2 a base:Arbol.
        ?arbol2 rdfs:label "{arbol}".
        ?arbol2 base:hasDistrito ?numDistrito.
        ?arbol2 owl:sameAs ?wikidataArbol.
    }}
    }}
    ORDER BY ?numDistrito
    """


    # Preparar la consulta SPARQL
    query = prepareQuery(sparql_query)

    # Ejecutar la consulta SPARQL en tus datos
    results = g.query(query)

    for row in results:
        # row es un diccionario que mapea las variables a sus valores
        numDistrito = row['numDistrito']
        direccion = row['direccion']
        wikidataBarrio = row['wikidataBarrio']
        nomBarrio = row['nomBarrio']
        
        # Hacer algo con los valores, por ejemplo, imprimirlos
        #print(f"Número Distrito: {numDistrito}, Dirección: {direccion}, Wikidata Barrio: {wikidataBarrio}, Nombre Barrio: {nomBarrio}")

    #Obtener las instancias de wikidata
    results_list = [row.wikidataBarrio for row in results]

    # Inicializar una lista para almacenar los códigos Q del barrio
    codigos_Q_lista = []

    # Iterar sobre la lista y obtener los códigos Q
    for wikidata_link in results_list:
        partes_enlace = wikidata_link.split('/')
        codigo_Q = partes_enlace[-1]
        codigos_Q_lista.append(codigo_Q)

    #print(codigos_Q_lista)

    # Imprimir la lista de códigos Q --> Imprime los Q
    #print(codigos_Q_lista)

    sparql_query2 = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
    PREFIX base: <http://base.itree.com/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?wikidataArbol WHERE {{
        ?arbol2 a base:Arbol.
        ?arbol2 rdfs:label "{arbol}".
        ?arbol2 base:hasDistrito ?numDistrito.
        ?arbol2 owl:sameAs ?wikidataArbol.
    }}
    """

    # Preparar la consulta SPARQL
    query2 = prepareQuery(sparql_query2)

    # Ejecutar la consulta SPARQL en tus datos
    results2 = g.query(query2)

    # Inicializar una lista para almacenar los valores de wikidataArbol
    wikidata_arboles = []

    # Iterar sobre los resultados de la consulta
    for row in results2:
        wikidata_arbol = row['wikidataArbol']
        wikidata_arboles.append(wikidata_arbol)

    # Imprimir la lista de valores de wikidataArbol
    #print(wikidata_arboles)


    codigoQarbol = []
    # Iterar sobre la lista y obtener los códigos Q
    for wikidata_link in wikidata_arboles:
        partes_enlace = wikidata_link.split('/')
        codigo_Q = partes_enlace[-1]
        codigoQarbol.append(codigo_Q)

    #print(codigoQarbol)

    #---------------------------------------------------------
    # Definir la URL del servicio SPARQL de Wikidata
    wikidata_sparql_url = "https://query.wikidata.org/sparql"


    short_names = []

    # Iterar sobre la lista de códigos Q y ejecutar la consulta SPARQL para cada uno
    for codigo_Q in codigoQarbol:
        # Crear un objeto SPARQLWrapper para el servicio de Wikidata
        wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)

        # Construir la consulta SPARQL con el código Q actual
        sparql_query_wikidata = f"""
        PREFIX wiki: <http://en.wikipedia.org/wiki/>
        PREFIX wi: <http://purl.org/ontology/wi/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
        PREFIX base: <http://base.itree.com/>
        PREFIX baseDistrito: <http://base.itree.com/distrito/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?o ?value WHERE {{
            wd:{codigo_Q} p:P1813 ?o.
            ?o ps:P1813 ?value.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es". }}
        }}
        """
        # Establecer la consulta SPARQL que deseas ejecutar en Wikidata
        wikidata_sparql.setQuery(sparql_query_wikidata)

        # Establecer el formato de los resultados a JSON
        wikidata_sparql.setReturnFormat(JSON)

        # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
        wikidata_results = wikidata_sparql.query().convert()

        for result in wikidata_results["results"]["bindings"]:
            value = result["value"]["value"]
            short_names.append(value)

    time.sleep(10)
    #print(short_names)

    ubicaciones = []
    for codigo_Q in codigos_Q_lista:
        wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)
        sparql_query_wikidata = f"""
        PREFIX wiki: <http://en.wikipedia.org/wiki/>
        PREFIX wi: <http://purl.org/ontology/wi/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
        PREFIX base: <http://base.itree.com/>
        PREFIX baseDistrito: <http://base.itree.com/distrito/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?o ?value WHERE {{
            wd:{codigo_Q} p:P625 ?o.
            ?o ps:P625 ?value.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es". }}
        }}
        """
        # Establecer la consulta SPARQL que deseas ejecutar en Wikidata
        wikidata_sparql.setQuery(sparql_query_wikidata)

        # Establecer el formato de los resultados a JSON
        wikidata_sparql.setReturnFormat(JSON)

        # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
        wikidata_results = wikidata_sparql.query().convert()

        for result in wikidata_results["results"]["bindings"]:
            value = result["value"]["value"]
            ubicaciones.append(value)
        
        #time.sleep(10)

    #print(ubicaciones)


    print("Arbol a evitar es {short_names}")

    for row, ubicacion in zip(results, ubicaciones):
        # row es un diccionario que mapea las variables a sus valores
        numDistrito = row['numDistrito']
        direccion = row['direccion']
        wikidataBarrio = row['wikidataBarrio']
        nomBarrio = row['nomBarrio']
        #ubi = ubicacion['ubicaciones']

        
        # Hacer algo con los valores, por ejemplo, imprimirlos
        print(f"Número Distrito: {numDistrito}, Dirección: {direccion}, Wikidata Barrio: {wikidataBarrio}, Nombre Barrio: {nomBarrio}, Ubicación; {ubicacion}")


def query2():
    distrito = "Centro"

    # Definir la URL de tus datos RDF en GitHub
    data_url = "https://raw.githubusercontent.com/aom20021/Curso2023-2024/master/HandsOn/Group10/rdf/result-with-links.ttl"

    # Crear un objeto Graph y cargar los datos desde la URL
    g = rdflib.Graph()
    g.parse(data_url, format="turtle")

    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
    PREFIX base: <http://base.itree.com/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT DISTINCT ?numBarrio ?nombreBarrio ?direccion ?wikidataBarrio WHERE {{
    ?parque a base:Parque_Canino.
    ?distrito a base:Distrito.
    ?parque base:hasDistrito ?numDistrito.
    ?distrito base:numDistrito ?numDistrito.
    ?parque base:hasDireccion ?direccion.
    ?distrito rdfs:label "{distrito}".
    ?barrio a base:Barrio.
    ?barrio base:numBarrio ?numBarrio.
    ?parque base:hasBarrio ?numBarrio.
    ?barrio rdfs:label ?nombreBarrio.
    ?barrio owl:sameAs ?wikidataBarrio.
    
    }}
    ORDER BY ?numDistrito
    """


    # Preparar la consulta SPARQL
    query = prepareQuery(sparql_query)

    # Ejecutar la consulta SPARQL en tus datos
    results = g.query(query)

    for row in results:
        # row es un diccionario que mapea las variables a sus valores
        numBarrio = row['numBarrio']
        wikidataBarrio = row['wikidataBarrio']
        nomBarrio = row['nombreBarrio']
        direccion = row['direccion']
        
        # Hacer algo con los valores, por ejemplo, imprimirlos
        #print(f"Distrito: {distrito}, Número Barrio: {numBarrio}, Dirección: {direccion}, Wikidata Barrio: {wikidataBarrio}, Nombre Barrio: {nomBarrio}")

    #Obtener las instancias de wikidata
    results_list = [row.wikidataBarrio for row in results]

    # Inicializar una lista para almacenar los códigos Q del barrio
    codigos_Q_lista = []

    # Iterar sobre la lista y obtener los códigos Q
    for wikidata_link in results_list:
        partes_enlace = wikidata_link.split('/')
        codigo_Q = partes_enlace[-1]
        codigos_Q_lista.append(codigo_Q)

    #print(codigos_Q_lista)

    #---------------------------------------------------------
    # Definir la URL del servicio SPARQL de Wikidata
    wikidata_sparql_url = "https://query.wikidata.org/sparql"


    # Iterar sobre la lista de códigos Q y ejecutar la consulta SPARQL para ca

    ubicaciones = []
    for codigo_Q in codigos_Q_lista:
        wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)
        sparql_query_wikidata = f"""
        PREFIX wiki: <http://en.wikipedia.org/wiki/>
        PREFIX wi: <http://purl.org/ontology/wi/core#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
        PREFIX base: <http://base.itree.com/>
        PREFIX baseDistrito: <http://base.itree.com/distrito/>
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX wikibase: <http://wikiba.se/ontology#>
        PREFIX p: <http://www.wikidata.org/prop/>
        PREFIX ps: <http://www.wikidata.org/prop/statement/>
        PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
        PREFIX bd: <http://www.bigdata.com/rdf#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>

        SELECT DISTINCT ?o ?value WHERE {{
            wd:{codigo_Q} p:P625 ?o.
            ?o ps:P625 ?value.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "es". }}
        }}
        """
        # Establecer la consulta SPARQL que deseas ejecutar en Wikidata
        wikidata_sparql.setQuery(sparql_query_wikidata)

        # Establecer el formato de los resultados a JSON
        wikidata_sparql.setReturnFormat(JSON)

        # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
        wikidata_results = wikidata_sparql.query().convert()

        for result in wikidata_results["results"]["bindings"]:
            value = result["value"]["value"]
            ubicaciones.append(value)
        
        #time.sleep(10)

    #print(ubicaciones)

    for row, ubicacion in zip(results, ubicaciones):
        # row es un diccionario que mapea las variables a sus valores
        numBarrio = row['numBarrio']
        wikidataBarrio = row['wikidataBarrio']
        nomBarrio = row['nombreBarrio']
        direccion = row['direccion']
        
        # Hacer algo con los valores, por ejemplo, imprimirlos
        print(f"Distrito: {distrito}, Número Barrio: {numBarrio}, Dirección: {direccion}, Wikidata Barrio: {wikidataBarrio}, Nombre Barrio: {nomBarrio}, Ubicación: {ubicacion}")
    

def query3():
    # Definir la URL de tus datos RDF en GitHub
    data_url = "https://raw.githubusercontent.com/aom20021/Curso2023-2024/master/HandsOn/Group10/rdf/result-with-links.ttl"

    # Crear un objeto Graph y cargar los datos desde la URL
    g = rdflib.Graph()
    g.parse(data_url, format="turtle")
    distrito = "Barajas"

    # Define the SPARQL query with a variable for the tree name
    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
    PREFIX base: <http://base.itree.com/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#> 


    SELECT DISTINCT ?nombreDistrito ?nombreArbol ?maxUnidades ?wikidataArbol WHERE {{
    {{
        SELECT ?nombreDistrito (MAX(?unidades) as ?maxUnidades) ?numDistrito WHERE {{
        ?distrito a base:Distrito.
        ?arbol a base:Arbol.
        ?arbol base:hasDistrito ?numDistrito.
        ?distrito base:numDistrito ?numDistrito.
        ?distrito rdfs:label "{distrito}".
        ?distrito rdfs:label ?nombreDistrito.
        ?arbol base:hasUnidades ?unidades.
        }}
        GROUP BY ?nombreDistrito ?numDistrito
    }}
    ?arbol a base:Arbol.
    ?arbol base:hasDistrito ?numDistrito.
    ?arbol rdfs:label ?nombreArbol.
    ?distrito rdfs:label ?nombreDistrito.
    ?distrito rdfs:label "{distrito}".
    ?arbol base:hasUnidades ?maxUnidades.
    ?arbol owl:sameAs ?wikidataArbol.
    }}
    ORDER BY ?nombreDistrito
    """

    # Prepare the SPARQL query
    query = prepareQuery(sparql_query)

    # Execute the query
    results = g.query(query)

    # Print the results
    codigo_Q = ""
    numero_Uds = 0
    for row in results:
        codigo_Q = row.wikidataArbol.split('/')[-1]
        numero_Uds = row.maxUnidades

    # URL del punto de consulta de Wikidata
    wikidata_sparql_url = "https://query.wikidata.org/sparql"

    # Consulta SPARQL para obtener la propiedad P1813 del objeto con Qnode especificado
    sparql_query_wikidata = f"""
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT DISTINCT ?shortName WHERE {{
            wd:{codigo_Q} wdt:P1813 ?shortName.
        }}
    """

    # Configurar el objeto SPARQLWrapper
    wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)
    wikidata_sparql.setQuery(sparql_query_wikidata)
    wikidata_sparql.setReturnFormat(JSON)

    # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
    wikidata_results = wikidata_sparql.query().convert()

    # Imprimir los resultados
    for result in wikidata_results["results"]["bindings"]:
        short_name = result["shortName"]["value"]
        print(f"Arbol: {short_name}")
        print(f"Número de unidades: {numero_Uds}")


def query4():
    data_url = "https://raw.githubusercontent.com/aom20021/Curso2023-2024/master/HandsOn/Group10/rdf/result-with-links.ttl"

    # Crear un objeto Graph y cargar los datos desde la URL
    g = rdflib.Graph()
    g.parse(data_url, format="turtle")
    arbol = "Aesculus hippocastanum"

    # Define the SPARQL query with a variable for the tree name
    sparql_query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema>
    PREFIX base: <http://base.itree.com/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?direccion ?arbol ?nombre ?wikidataArbol ?wikidataDireccion WHERE {{
    ?arbol a base:Arbol.
    ?parques a base:Parque_Canino.
    ?parques base:hasDireccion ?direccion.
    ?parques base:hasDistrito ?numDistrito.
    ?parques owl:sameAs ?wikidataDireccion.
    ?arbol base:hasDistrito ?numDistrito.
    ?arbol owl:sameAs ?wikidataArbol.
    ?arbol rdfs:label "{arbol}".
    }}
    """

    # Prepare the SPARQL query
    query = prepareQuery(sparql_query)

    # Execute the query
    results = g.query(query)

    # Print the results
    codigo_Q = ""
    for row in results:
        codigo_Q = row.wikidataArbol.split('/')[-1]
    codigos_direccion = []
    for row in results:
        codigos_direccion.append(row.wikidataDireccion.split('/')[-1])

    # URL del punto de consulta de Wikidata
    wikidata_sparql_url = "https://query.wikidata.org/sparql"

    # Consulta SPARQL para obtener la propiedad P1813 del objeto con Qnode especificado
    sparql_query_wikidata = f"""
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        SELECT DISTINCT ?shortName WHERE {{
            wd:{codigo_Q} wdt:P1813 ?shortName.
        }}
    """

    # Configurar el objeto SPARQLWrapper
    wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)
    wikidata_sparql.setQuery(sparql_query_wikidata)
    wikidata_sparql.setReturnFormat(JSON)

    # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
    wikidata_results = wikidata_sparql.query().convert()

    # Imprimir los resultados
    for result in wikidata_results["results"]["bindings"]:
        short_name = result["shortName"]["value"]
        print(f"En estas calles hay {short_name}:")
    for string in codigos_direccion:
        sparql_query_wikidata = f"""
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            SELECT DISTINCT ?coords ?label WHERE {{
                wd:{string} wdt:P625 ?coords.
                wd:{string} rdfs:label ?label.
                FILTER(LANG(?label) = 'es').
            }}
        """
        # Configurar el objeto SPARQLWrapper
        wikidata_sparql = SPARQLWrapper(wikidata_sparql_url)
        wikidata_sparql.setQuery(sparql_query_wikidata)
        wikidata_sparql.setReturnFormat(JSON)

        # Ejecutar la consulta en el servicio de Wikidata y obtener los resultados
        wikidata_results = wikidata_sparql.query().convert()
        for result in wikidata_results["results"]["bindings"]:
            coords = result["coords"]["value"]
            label = result["label"]["value"]

            # Print or use the coordinates and street name as needed
            # Use regular expression to extract the two numbers
            match = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", coords)

            # Check if the match is successful
            if match:
                # Extract the two numbers
                number1 = float(match.group(1))
                number2 = float(match.group(2))

                # Print or use the extracted numbers as needed
                print(f"Coordenadas: {number2} {number1}, Nombre de la calle: {label}")
            else:
                print("No match found.")


def main():
    while True:
        print("Selecciona una opción:")
        print("1. Consultar datos de parques en distritos sin cierto tipo de árbol:")
        print("2. Consultar parques de perros en el distrito seleccionado:")
        print("3. Árbol con más unidades en un distrito:")
        print("4. Calle en la que hay un cierto tipo de árbol:")
        print("-1. Salir")

        opcion = int(input("Ingresa el número de la opción (o -1 para salir): "))

        if opcion == 1:
            query1()
        elif opcion == 2:
            query2()
        elif opcion == 3:
            query3()
        elif opcion == 4:
            query4()
        elif opcion == -1:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")
        
        print("")
        print("")
        print("")

if __name__ == "__main__":
    main()