from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable


class Neo4jConnector:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_protein(self, protein, full_name, gene_primary, gene_synonym):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_protein, protein, full_name, gene_primary, gene_synonym
            )
            for row in result:
                print(f'Created protein: {row["p"]}, {row["f"]}, {row["gp"]}, {row["gs"]}')

    @staticmethod
    def _create_and_return_protein(tx, protein, full_name, gene_primary, gene_synonym):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p:Protein { id: $protein }) "
            "CREATE (f:FullName { name: $full_name }) "
            "CREATE (gp:Gene { name: $gene_primary }) "
            "CREATE (gs:Gene { name: $gene_synonym }) "
            "CREATE (p)-[:HAS_FULL_NAME]->(f) "
            "CREATE (p)-[:FROM_GENE { status: 'primary' }]->(gp) "
            "CREATE (p)-[:FROM_GENE { status: 'synonym' }]->(gs) "
            "RETURN p, f, gp, gs"
        )
        result = tx.run(query, protein=protein, full_name=full_name, gene_primary=gene_primary, gene_synonym=gene_synonym)
        try:
            return [{"p": row["p"]["id"], "f": row["f"]["name"], "gp": row["gp"]["name"], "gs": row["gs"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]
