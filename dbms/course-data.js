/*
  course-data.js — AUTHORITATIVE course metadata for Database Management Systems
  Source: official course syllabus document (Karnavati University, B.Tech, Sem 3).

  IMPORTANT: This file uses a plain global object, NOT ES module import/export.
  Pages are opened directly via file:// (not through a local server), and
  file:// blocks ES module imports due to CORS. Include this with a classic
  (non-module) <script src="course-data.js"></script> tag, and every
  other script that needs it can just reference the global COURSE_DATA
  object directly (no import statement needed).
*/

const COURSE_DATA = {

  meta: {
    universityCode: "26UITU030001",
    courseName: "Database Management Systems",
    program: "B.Tech (CSE / AIML / DS / CYBER)",
    semester: 3,
    hoursPerWeek: { lecture: 3, tutorial: 0, practical: 1 },
    credits: 4,
    totalMarks: 100,
    totalTheoryHours: 45,
    courseDescription:
      "Database Management Systems (DBMS) is a course that teaches how to store, " +
      "organize, and manage data efficiently using databases. It covers SQL, " +
      "relational models, normalization, and transaction management. It also " +
      "introduces modern databases like MongoDB and NoSQL for real-world applications."
  },

  prerequisites: [
    "Basic programming skills",
    "Fundamental knowledge of computer systems and data handling",
    "Understanding of basic logic and problem-solving concepts"
  ],

  bloomLevelNames: {
    L1: "Remember",
    L2: "Understand",
    L3: "Apply",
    L4: "Analyze",
    L5: "Evaluate",
    L6: "Create"
  },

  // Lower Order Thinking Skills vs Higher Order Thinking Skills, per Bloom's taxonomy
  bloomOrder: {
    L1: "LOTS", L2: "LOTS", L3: "LOTS",
    L4: "HOTS", L5: "HOTS", L6: "HOTS"
  },

  courseOutcomes: [
    {
      id: "CO1",
      bloomLevel: "L2",
      statement:
        "Understand fundamental concepts of DBMS, data models, database architecture, " +
        "ER modeling and normalization techniques."
    },
    {
      id: "CO2",
      bloomLevel: "L3",
      statement:
        "Apply RDBMS concepts, relational algebra and SQL commands for database " +
        "querying and management."
    },
    {
      id: "CO3",
      bloomLevel: "L3",
      statement:
        "Design and implement database operations using SQL functions, constraints, " +
        "triggers and stored procedures."
    },
    {
      id: "CO4",
      bloomLevel: "L4",
      statement:
        "Analyze transaction processing, concurrency control, recovery mechanisms " +
        "and database security techniques."
    },
    {
      id: "CO5",
      bloomLevel: "L5",
      statement:
        "Evaluate advanced database systems, NoSQL databases and MongoDB techniques " +
        "for modern data management and real-world applications."
    }
  ],

  // CO-PO matrix. Values are 1-3 (strength of mapping) or null (no mapping, "–" in syllabus).
  coPoMatrix: {
    CO1: { PO1: 3, PO2: 2, PO3: 1, PO4: null, PO5: 1,    PO6: null, PO7: null, PO8: null, PO9: null,    PO10: null, PO11: null, PO12: 2 },
    CO2: { PO1: 3, PO2: 3, PO3: 2, PO4: 1,    PO5: 3,    PO6: null, PO7: null, PO8: null, PO9: null,    PO10: 1,    PO11: null, PO12: 2 },
    CO3: { PO1: 3, PO2: 3, PO3: 3, PO4: 2,    PO5: 3,    PO6: null, PO7: null, PO8: null, PO9: 1,       PO10: 1,    PO11: null, PO12: 2 },
    CO4: { PO1: 3, PO2: 3, PO3: 2, PO4: 3,    PO5: 2,    PO6: 1,    PO7: null, PO8: 2,    PO9: null,    PO10: 1,    PO11: null, PO12: 2 },
    CO5: { PO1: 3, PO2: 3, PO3: 3, PO4: 2,    PO5: 3,    PO6: 1,    PO7: 1,    PO8: null, PO9: 1,       PO10: 1,    PO11: null, PO12: 3 }
  },

  units: [
    {
      unit: "I",
      title: "Introduction to DBMS",
      hours: 9,
      mappedCOs: ["CO1"],
      topics: [
        "Introduction to DBMS, its characteristics, advantages and applications",
        "DBMS vs file system",
        "3-level (ANSI-SPARC) database architecture",
        "Data abstraction, schema and instance",
        "Data models: relational, hierarchical, network, object-oriented, NoSQL",
        "Relational model, keys and constraints",
        "ER modeling and cardinality constraints",
        "Normalization: 1NF, 2NF, 3NF, 4NF, BCNF, 5NF"
      ]
    },
    {
      unit: "II",
      title: "Relational Database Concepts",
      hours: 9,
      mappedCOs: ["CO2"],
      topics: [
        "Introduction to RDBMS, entities and relationships",
        "Relational algebra and relational calculus",
        "SQL basics: DDL, DML, DCL, TCL",
        "Relational operations and query writing",
        "Aggregate functions, nested queries",
        "GROUP BY and ORDER BY clauses",
        "Joins and views",
        "Extended ER model: generalization, specialization, aggregation",
        "Decomposition concepts"
      ]
    },
    {
      unit: "III",
      title: "Structured Query Language - SQL",
      hours: 8,
      mappedCOs: ["CO3"],
      topics: [
        "Table creation and alteration",
        "Constraints: primary key, foreign key, unique, not null, check",
        "SQL functions: numeric, date, string",
        "Set operations",
        "Transaction control commands: COMMIT, ROLLBACK, SAVEPOINT",
        "Control flow commands, cursors and sequences",
        "Triggers and stored procedures",
        "Exception handling in DBMS"
      ]
    },
    {
      unit: "IV",
      title: "Transaction Processing and Database Management",
      hours: 10,
      mappedCOs: ["CO4"],
      topics: [
        "Transactions: ACID properties, state diagram",
        "Serializability of schedules, consistent/inconsistent state",
        "Serial & non-serial schedules; recoverable & non-recoverable schedules",
        "Cascading rollback and cascade-less schedules",
        "Recovery from transaction failures: log-based recovery, checkpoints",
        "Concurrency control: lock-based techniques, shared/exclusive locks",
        "Two-phase locking protocol, concurrency control manager, lock manager",
        "Indexing and hashing: file organization, primary/secondary indexing",
        "Clustered/non-clustered indexes, B-tree and B+ tree indexing",
        "Static and dynamic hashing techniques",
        "Recoverability: types of recovery, failures and their types",
        "Deadlocks: detection using wait-for-graph, recovery schemes",
        "Introduction to data warehouse, data marts and ETL process"
      ]
    },
    {
      unit: "V",
      title: "Advanced Databases and MongoDB",
      hours: 9,
      mappedCOs: ["CO5"],
      topics: [
        "Advanced database systems, distributed and cloud databases",
        "NoSQL databases and types, Big Data databases",
        "MongoDB architecture, collections and documents",
        "CRUD operations, indexing, aggregation framework",
        "Replication concepts",
        "Comparison of RDBMS and NoSQL databases",
        "Real-world applications of MongoDB"
      ]
    }
  ],

  examScheme: {
    endSemester: { hours: 2, marks: 50, scopeUnits: ["I", "II", "III", "IV", "V"] },
    midterm: {
      theoryMarks: 25,
      practicalMarks: 25,
      scopeUnits: ["I", "II", "III"],
      note: "Midterm covers Units I, II and III only. Units IV and V are end-semester scope."
    },
    internalTheory: {
      midterm: 25,
      ciaAssignmentQuizCertification: 20,
      attendance: 5
    },
    internalPractical: {
      midtermPractical: 25,
      ciaLabOrMiniProject: 20,
      attendance: 5
    }
  }
};
