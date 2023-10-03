# Lifecycle state broadcast SDK

Python SDK version for the Lifecycle state broadcast Restful API

## Lineamientos estructura y propiedades en archivos de configuración

- Los archivos de configuración deben tener un formato JSON válido.
- Incluir en el nivel más alto (root) la propiedad "id" / "Id", y como valor un string que identifique de forma única al componente.
  - Este valor servira de referencia cuando algún otro componente dependa de dicho artefacto.   
- Incluir de forma opcional la palabra "context" / "Context" en el nombre de las propiedades que incluyan información de dependencia con (conexión a):
  - Bases de datos
  - Servicios de mensajería
  - Servidores SMTP, FTP, etc.
  - APIs, Web services, y endpoints en general
- Incluir en cada propiedad tipo "Context" o dependencia un "id" / "Id" que permita identificar de forma única a cada una de ellas y asi poder relacionar más adelante la conexión con sus dependientes.
  - Este valor debe ser consistente entre componentes, es decir si la instancia de SQL Server cuya ip privada es 10.142.0.11 la identifican como pls-online, ese "id" / "Id" debe estar en todos los settings de los componentes que dependan de dicha instancia.
- Incluir en cada propiedad tipo "Context" o dependencia las palabras claves:
  - port (TCP / HTTP services, bases de datos)
  - portNumber (TCP / HTTP services, bases de datos)
  - host (TCP / HTTP services, bases de datos)
  - hostName (TCP / HTTP services, bases de datos)
  - url (HTTP services)
  - endpoint (TCP / HTTP services)
  - servers (TCP / HTTP services, bases de datos)
  - address (TCP / HTTP services)
  - topicId (Pubsub)
  - dataset (Bigquery)
  - connectionString (Bases de datos relacionales)

### Opcional

- Incluir en el nivel más alto (root) las propiedades "name" / "Name" y "description" / "Description" para ayudar a identificar mejor a cada componente.
- Incluir en el archivo de configuración una sección que permita itentificar si el componente expone alguna especie de mecanismo o endpoint de Health check, que puede ser tipo TCP o HTTP, acompañado de su respectivo puerto, ejemplos:

```json
{
  "httpHealthCheck": {
    "endpoint": "http://localhost",
    "portNumber": 8081
  }
}
```

```json
{
  "tcpHealthCheck": {
    "hostName": "10.142.0.11",
    "portNumber": 1433
  }
}
```

### Lineamientos en funcionamiento

```json
{
  "id": "my-cool-component",
  "httpHealthCheck": {
    "endpoint": "http://localhost",
    "portNumber": 8082
  },
  "masterDbContext": {
    "id": "pls-online",
    "connectionString": "MSSQL;databse=xyz;..."
  },
  "cacheDbContext": {
    "id": "elastic-cache-1",
    "endpoint": "http://10.143.1.2:9200"
  }
}
```
## Resultados obtenidos al intentar utilizar el parser con los archivos modelos

- En algunos archivos no se puede identificar la propiedad "id".
- En algunos archivos no se puede identificar la propiedad "id", pues dicha configuración aparentemente incluye este valor en la propiedad "name", la cual se utiliza en el parser para el nombre del servicio.
- En algunos archivos no se puede identificar la propiedad "name" de la aplicación.
- En algunos archivos no se puede identificar la propiedad "description" de la aplicación.
- Se identifican las dependencias, pero estas no poseen la propiedad "id".

Recomendaciones:

- Agregar la propiedad "id" a nivel aplicación.
- Agregar la propiedad "id" para cada dependencia.
- Hay casos en los que la información de los websockets no se puede identificar, pues los endpoints o url se almacenan en propiedades con nombres que no reflejan ningún patrón aparente, como por ejemplo en el schema-8.json propiedad websockets.

### schema-3.json

Conflicto en la identificación de dependencia en la propiedad zookeeperEndPoint, no es recomendable colocar endpoints a nivel aplicación.

### schema-15.json (NA - No aplica)

Imposible identificar información alguna. Este archivo es en realidad un archivo de configuración de entorno de desarrollo de Salesforce, por lo cual no aplica la ejecución del parser sobre el mismo.

## Building package

```bash
python setup.py sdist bdist_wheel
```

## Publishing package

```bash
python -m twine upload dist/*
```

This will ask for credentials:

username: __token__
password: Your PyPi API Token
