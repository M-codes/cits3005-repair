# student 1 : Michael Hii Rong Mee (23237074)
# student 2 : Rishwanth Katherapalle (23463452)

from owlready2 import *
from rdflib import Graph

# Load the ontology
g = Graph()
g.parse("repair_ontology.owl", format="xml")


# SPARQL Query 1: Procedures with more than 6 steps - Michael
query_1 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://example.org/repair_ontology.owl#>

SELECT ?procedure (COUNT(?step) AS ?stepCount)
WHERE {
    ?procedure rdf:type ex:Procedure .
    ?procedure ex:has_step ?step .
}
GROUP BY ?procedure
HAVING (COUNT(?step) > 6)
"""

# SPARQL Query 2: Items with more than 10 procedures - Rishwanth
query_2 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://example.org/repair_ontology.owl#>

SELECT ?item (COUNT(?procedure) AS ?procedureCount)
WHERE {
    ?item rdf:type ex:Item .
    ?item ex:has_procedure ?procedure .
}
GROUP BY ?item
HAVING (COUNT(?procedure) > 10)
"""

# SPARQL Query 3: Procedures with tools not mentioned in steps - Michael
query_3 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://example.org/repair_ontology.owl#>

SELECT DISTINCT ?procedure ?tool
WHERE {
    ?procedure ex:has_tool ?tool .
    ?procedure ex:has_step ?step .
    FILTER NOT EXISTS {
        ?step ex:has_tool ?tool .
    }
}
"""

# SPARQL Query 4: Steps with potential hazards - Rishwanth
query_4 = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX ex: <http://example.org/repair_ontology.owl#>

SELECT ?step ?title
WHERE {
    ?step rdf:type ex:Step .
    ?step ex:has_title ?title .
    FILTER(REGEX(?title, "careful|dangerous|Careful|Dangerous|CAREFUL|DANGEROUS", "i"))  # Case-insensitive matching
}
"""

# Step 4: Run queries on the RDFLib graph and display results


# Helper function to execute a query and print results - Rishwanth
def execute_query(query, description):
    print(f"\n{description}")
    for row in g.query(query):
        print(row)

# Execute each SPARQL query
# Query 1: Procedures with more than 6 steps
execute_query(query_1, "Procedures with more than 6 steps:")

# Query 2: Items with more than 10 procedures
execute_query(query_2, "Items with more than 10 procedures:")

# Query 3: Procedures with tools not mentioned in steps
execute_query(query_3, "Procedures with tools not mentioned in steps:")

# Query 4: Steps with potential hazards
execute_query(query_4, "Steps with potential hazards (careful/dangerous):")
