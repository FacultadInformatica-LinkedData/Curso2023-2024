from flask import Flask, render_template, request
from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

g = Graph()
g.parse('../data/result-with-links.ttl', format="turtle")


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Directions')
def directions():
    return render_template('directions.html', data ="")

@app.route('/Directions/Request')
def directions_request():
    if request.method == 'GET':
        n_places = request.args.get('plazas')
        n_places = str(n_places)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Direction WHERE {
                ?Station ns:places ''' + n_places + '''.                 
                ?Station ns:hasDirection ?Directions. 
                ?Directions rdfs:label ?Direction.
            } LIMIT 10'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(r.Direction)

        if len(string) == 0:
            string.append("No se han encontrado Bases con dicho numero de plazas")

        datos = {'resultados': string}
        return render_template('directions.html', data=datos)

    

@app.route('/Streets')
def streets():
    return render_template('streets.html', data="")

@app.route('/Streets/Request')
def streets_request():
    if request.method == 'GET':
        calle = request.args.get('street')
        calle = str(calle)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?ID WHERE {
                ?Street rdfs:label "''' + calle + '''". 
                ?Direction ns:hasStreet ?Street.                
                ?Bases ns:hasDirection ?Direction. 
                ?Bases ns:id ?ID.
            } LIMIT 10'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(str(r.ID))

        if len(string) == 0:
            string.append("Dicha calle no tienen ninguna base de bicicletas")

        datos = {'resultados': string}
        return render_template('streets.html', data=datos)

@app.route('/Districts')
def districts():
    return render_template('districts.html', data="")

@app.route('/Districts/Request')
def districts_request():
    if request.method == 'GET':
        distrito = request.args.get('district')
        distrito = str(distrito)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Nombre WHERE {
                ?District rdfs:label "''' + distrito + '''". 
                ?Hood ns:neighbourhoodBelongsDistrict ?District.                
                ?Direction ns:directionBelongsNeighbourhood ?Hood. 
                ?Direction ns:hasStreet ?Street.
                ?Street rdfs:label ?Nombre
            } LIMIT 25'''
        )
        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(r.Nombre)

        if len(string) == 0:
            string.append("Dicho distrito no alberga ninguna calle con bases de bicicletas")

        datos = {'resultados': string}
        return render_template('districts.html', data=datos)

@app.route('/Companies')
def companys():
    return render_template('companys.html', data="")

@app.route('/Companies/Request')
def companys_request():
      if request.method == 'GET':
        calle = request.args.get('street')
        calle = str(calle)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT DISTINCT ?Company WHERE {
                ?Street rdfs:label "''' + calle + '''". 
                ?Direction ns:hasStreet ?Street.                
                ?BicycleStation ns:hasDirection ?Direction.
                ?BicycleStation ns:isManageBy ?Company.
            } LIMIT 10'''
        )

        ##ADAPTER##
        string = []
        for r in g.query(q):
            string.append(r.Company)

        if len(string) == 0:
            string.append("Dicha calle no alberga ninguna bases de bicicletas")

        datos = {'resultados': string}
        return render_template('companys.html', data=datos)
        
## CONSULTAS LINKEADAS ##

@app.route('/StreetsLinked')
def streetsLinked():
    return render_template('streets-linked.html', data={})

@app.route('/StreetsLinked/Request')
def streetsLinked_request():
    if request.method == 'GET':
        calle = request.args.get('street')
        calle = str(calle)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#>   
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Key WHERE {
                ?Street rdfs:label "''' + calle + '''". 
                ?Street owl:sameAs ?Key
            } LIMIT 1'''
        )


        ##ADAPTER##
        valores = {}
        clave = ''
        for r in g.query(q):
            clave= r.Key.split('/')

        if clave != '':
        #DESCARGAMOS LA PAGINA DE WIKIDATA QUE NOS INTERESA
            grafo = Graph()
            grafo.parse("https://www.wikidata.org/wiki/Special:EntityData/"+clave[-1]+".ttl")

            #CONSULTAMOS A ESA PAGINA DESCARGADA, CON prepareQuery ESTO NO FUNCIONA
            q = grafo.query("""SELECT ?p ?label_objeto
                        WHERE 
                        {
                            wd:"""+clave[-1]+""" ?p ?objeto.
                            ?objeto rdfs:label ?label_objeto.
                        }LIMIT 5""")
            
            #HACEMOS UN ADAPTER PARA RETENER LOS VALORES
            for p, label_objeto in q:
                valores[p] = label_objeto

        else:
            valores['resultado'] = "No tiene ningun link con datos de WIKIDATA"

        return render_template('streets-linked.html', data=valores)
    

@app.route('/NeighbourhoodLinked')
def neighbourhoodLinked():
    return render_template('neighbourhood-linked.html',data={})

@app.route('/NeighbourhoodLinked/Request')
def neighbourhoodLinked_request():
    if request.method == 'GET':
        hood = request.args.get('hood')
        hood = str(hood)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/>  
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Key WHERE {
                ?Neighbourhood rdfs:label "''' + hood + '''". 
                ?Neighbourhood owl:sameAs ?Key
            } LIMIT 1'''
        ) 
        
        ##ADAPTER##
        valores = {}
        clave = ''
        for r in g.query(q):
            clave= r.Key.split('/')

        if clave != '':
            #DESCARGAMOS LA PAGINA DE WIKIDATA QUE NOS INTERESA
            grafo = Graph()
            grafo.parse("https://www.wikidata.org/wiki/Special:EntityData/"+clave[-1]+".ttl")

            #CONSULTAMOS A ESA PAGINA DESCARGADA, CON prepareQuery ESTO NO FUNCIONA
            q = grafo.query("""SELECT ?p ?label_objeto
                        WHERE 
                        {
                            wd:"""+clave[-1]+""" ?p ?objeto.
                            ?objeto rdfs:label ?label_objeto.
                        }LIMIT 5""")
            
            #HACEMOS UN ADAPTER PARA RETENER LOS VALORES
            for p, label_objeto in q:
                valores[p] = label_objeto

        else:
            valores['resultado'] = "No tiene ningun link con datos de WIKIDATA"

        return render_template('neighbourhood-linked.html', data=valores)

@app.route('/DistrictLinked')
def DistrictLinked():
    return render_template('districts-linked.html', data={})

@app.route('/DistrictLinked/Request')
def DistricLinked_request():
    if request.method == 'GET':
        distrito = request.args.get('district')
        distrito = str(distrito)
        q = prepareQuery('''
            PREFIX ns: <http://smartcity.linkeddata.es/lcc/ontology/BicicletasElectricas#> 
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   
            PREFIX data: <http://smartcity.linkeddata.es/lcc/resource/> 
            PREFIX owl: <http://www.w3.org/2002/07/owl#>   
            PREFIX bicycle: <data:BicycleStation> 
            PREFIX district: <data:District> 
            PREFIX direction: <data:Direction>  
            PREFIX hood: <data:Neighbourhood>  
            PREFIX street: <data:Street>           

            SELECT ?Key WHERE {
                ?Distric rdfs:label "''' + distrito + '''". 
                ?Distric owl:sameAs ?Key
            } LIMIT 1'''
        )

        ##ADAPTER##
        valores = {}
        clave = ''
        for r in g.query(q):
            clave= r.Key.split('/')

        if clave != '':
            #DESCARGAMOS LA PAGINA DE WIKIDATA QUE NOS INTERESA
            grafo = Graph()
            grafo.parse("https://www.wikidata.org/wiki/Special:EntityData/"+clave[-1]+".ttl")

            #CONSULTAMOS A ESA PAGINA DESCARGADA, CON prepareQuery ESTO NO FUNCIONA
            q = grafo.query("""SELECT ?p ?label_objeto
                        WHERE 
                        {
                            wd:"""+clave[-1]+""" ?p ?objeto.
                            ?objeto rdfs:label ?label_objeto.
                        }LIMIT 5""")
            
            #HACEMOS UN ADAPTER PARA RETENER LOS VALORES
            for p, label_objeto in q:
                valores[p] = label_objeto

        else:
            valores['resultado'] = "No tiene ningun link con datos de WIKIDATA"

        return render_template('districts-linked.html', data=valores)

if __name__ == '__main__':
    app.run(debug=True, port=5000)         ##Indicamos que cada vez que cambiemos algo  se reinicie el servidor, y en que puerto lanzarse