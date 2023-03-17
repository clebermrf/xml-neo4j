# xml-neo4j
This microservice can ingest Uniprot XML files into a neo4j instance. You may use HTTP requests from external tools like Airflow to run jobs. 

1. Start the containers by starting the instances
```
$ docker-compose up
```

2. Open the neo4j interface at http://localhost:7474/browser/ with user neo4j and password neo4j, then set the password to adminneo4j.


3. You will be able to send data by running
```
curl -X POST localhost:8080/protein \
  -H "Content-Type: application/xml" \
  -H "Accept: application/xml" \
  -d "<xml>....</xml>"
```
