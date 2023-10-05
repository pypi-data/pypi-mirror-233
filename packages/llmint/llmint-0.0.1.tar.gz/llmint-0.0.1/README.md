# Mint
Fast, modular data integration powered by LLM.

Given sample data:
```yaml
source: { "status": "on", "brightness": 90 }
target: { "power": "active", "luminosity": 0.9 }
```
We want to generate the dataflow operators that convert from the source schema to the target schema. Mint splits the process in to the following steps:
1. Discovery. Identifying the data sources that are relevant to a data consumer. 
1. Identification. This step preprocesses all schemas and generates a unique schema fingerprint which is invariant to field ordering, captitalization etc. Extracts the schema from the data. Each schema is of form:
```yaml
schema_source:
- Name: "status"
- Type: string
- Default: None
- Description: "status of the lamp"
```
3. Matching. Identify the correspondences between fields in the schemas. This step generates the correspondence between fields. Each correspondence contains a language-neutral transformation between the values. Each correspondence can be seen as a row of a match-action table.
4. Mapping. Generates dataflow that coverts fields from source schema to the target schema, given the match-action table.

