import uvicorn
from fastapi import FastAPI, Response, APIRouter, Request
import os
from parsers import Uniprot
from drivers import Neo4jConnector


NEO4J_URI = "neo4j://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "adminneo4j"


app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "Uniprot"}


@app.post("/protein")
async def protein(request: Request):

    body = await request.body()
    protein = Uniprot(body)

    app = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    app.create_protein(
        protein.accession,
        protein.full_name, 
        protein.gene_primary_name, 
        protein.gene_synonym
    )
    app.close()


if __name__ == '__main__':
    uvicorn.run(app, host='app', port=8080)
