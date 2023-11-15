# React.js and SPARQL app

## Starting the app

```bash
npm install
npm run dev
```

_Note: The application expects a SPARQL endpoint at `http:localhost:9000/api/sparql` and a KG with the same structure as our. Also, due to the data and the app being running at the same host at the same time, CORS policy will make the app to crash. We cannot deactivate or configure Allowed-Origins in Helio Publisher so we run the app in a Chrome instance with CORS policiy deactivated (not recommended)._

Authors:
- Ramiro Lopez Cento
- Guillermo Izquierdo Cabo
- Marco Ciccalè Baztán
