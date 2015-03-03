// sessions
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/sessions.csv" AS row
MERGE (session:Session {id: row.sessionId, title: row.talkTitle});

// tracks
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/sessions.csv" AS row
WITH row WHERE row.trackHref <> ""
MERGE (track:Track {id: row.trackHref})
ON CREATE SET track.title = row.trackTitle;

// sessions -> tracks
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/sessions.csv" AS row
WITH row WHERE row.trackHref <> ""
MATCH (track:Track {id: row.trackHref})
MATCH (session:Session {id: row.sessionId})
MERGE (session)-[:PART_OF_TRACK]->(track);

// topics
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/topics.csv" AS row
MERGE (topic:Topic {id: row.topicId});

// words
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/topics.csv" AS row
MERGE (word:Word {value: row.word});

// topic -> words
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/topics.csv" AS row
MATCH (topic:Topic {id: row.topicId})
MATCH (word:Word {value: row.word})
MERGE (topic)-[:HAS_WORD]->(word);

// sessions -> topics
LOAD CSV WITH HEADERS FROM "file:/Users/markneedham/projects/neo4j-qcon/data/sessions-topics.csv" AS row
MATCH (session:Session {id: row.sessionId})
MATCH (topic:Topic {id: row.topicId})
MERGE (topic)-[:TOPIC]->(topic);
