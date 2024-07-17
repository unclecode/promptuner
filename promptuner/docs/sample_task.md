Given a passage of text, generate a knowledge graph by extracting named entities and the relations between them. Your task involves:

1. Carefully analyzing the given passage.
2. Identifying and extracting named entities (e.g., people, organizations, locations, concepts).
3. Determining the relationships between these entities based on the context provided in the passage.
4. Generating a JSON output that represents the knowledge graph, containing two main sections: "entities" and "relations".

The JSON output should follow this structure, and it must be wrapped in a <result> tag:

<result>
{
  "entities": [
    {
      "id": "E1",
      "name": "Entity name",
      "type": "Entity type (e.g., Person, Organization, Location, Concept)",
    }
  ],
  "relations": [
    {
      "id": "R1",
      "type": "Relation type (e.g., worksFor, locatedIn, partOf)",
      "source": "ID of the source entity",
      "target": "ID of the target entity",
    }
  ]
}
</result>

Guidelines:
- Assign a unique ID to each entity and relation (e.g., E1, E2, E3 for entities; R1, R2, R3 for relations).
- Include common attributes for entities such as name, type, and mentions.
- For relations, specify the type, source entity, target entity, and supporting evidence from the text.
- Ensure the JSON is well-formed, parsable, and error-free.
- Ensure the JSON result is wrapped in the <result> tag.
- Extract as many relevant entities and relations as possible from the given passage.

Your goal is to create a comprehensive knowledge graph that accurately represents the information and relationships described in the input text. This process requires careful analysis of the passage, identification of key entities and their relationships, and the ability to structure this information in a clear and organized JSON format.