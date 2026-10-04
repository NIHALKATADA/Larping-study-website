import json

data = [
  {
    "unit": "I",
    "unit_title": "Unit I: Introduction to DBMS, E-R Modeling, and Normalization",
    "topics": [
      {
        "title": "Introduction to DBMS",
        "content_html": """
        <p>A <strong>Database Management System (DBMS)</strong> is a software system designed to store, retrieve, and manage data efficiently and securely. It serves as an interface between the user and the database, ensuring that data is consistently organized and easily accessible.</p>
        <div class="example"><strong>Example:</strong> MySQL, PostgreSQL, Oracle, and Microsoft SQL Server are popular DBMS software.</div>
        
        <h3>DBMS vs File System</h3>
        <p>Before DBMS, data was stored in traditional file-processing systems (like flat files or CSVs). This led to issues like <strong>data redundancy</strong> (duplication of data) and <strong>data inconsistency</strong> (different copies having different values).</p>
        <table border="1">
          <tr><th>Feature</th><th>DBMS</th><th>File-Based System</th></tr>
          <tr><td>Data Redundancy</td><td>Minimal redundancy due to normalization.</td><td>High redundancy as files are isolated.</td></tr>
          <tr><td>Data Consistency</td><td>High consistency. Updates reflect everywhere.</td><td>Inconsistent if multiple copies exist.</td></tr>
          <tr><td>Data Access</td><td>Provides query languages (e.g., SQL) for easy access.</td><td>Requires writing custom application programs.</td></tr>
          <tr><td>Security</td><td>High security with user access controls.</td><td>Very little security mechanism.</td></tr>
        </table>

        <h3>Three-Level ANSI-SPARC Architecture</h3>
        <p>The DBMS architecture is divided into three levels to separate the user applications from the physical database:</p>
        <ul>
          <li><strong>Internal/Physical Level:</strong> Describes how the data is actually stored on the storage devices.</li>
          <li><strong>Conceptual/Logical Level:</strong> Describes what data is stored and the relationships between them.</li>
          <li><strong>External/View Level:</strong> Describes only a part of the entire database that a specific user needs to see.</li>
        </ul>
        <div class="exam-trap"><strong>Exam Trap:</strong> Don't confuse logical data independence with physical data independence. Physical data independence is the ability to modify the internal schema without altering the conceptual schema. Logical data independence is the ability to modify the conceptual schema without altering the external schemas.</div>
        
        <h3>Schema and Instance</h3>
        <p>A <strong>Schema</strong> is the overall design or structure of the database (rarely changes). An <strong>Instance</strong> is the actual data stored in the database at a particular moment in time (changes frequently).</p>
        """
      },
      {
        "title": "Database Users and DBA",
        "content_html": """
        <p>Database systems are used by various classes of users:</p>
        <ul>
          <li><strong>Naive Users:</strong> Interact with the system by invoking one of the application programs (e.g., banking clerks).</li>
          <li><strong>Application Programmers:</strong> Computer professionals who write application programs.</li>
          <li><strong>Sophisticated Users:</strong> Interact without writing programs, typically using query languages (e.g., Data Analysts).</li>
          <li><strong>Database Administrator (DBA):</strong> The central authority managing the database.</li>
        </ul>
        <div class="pro-tip"><strong>Pro-Tip:</strong> The DBA is responsible for schema definition, storage structure and access-method definition, granting authorizations, and routine maintenance (backups).</div>
        """
      },
      {
        "title": "Data Models",
        "content_html": """
        <p>A data model is a collection of conceptual tools for describing data, data relationships, data semantics, and consistency constraints.</p>
        <table border="1">
          <tr><th>Model</th><th>Structure</th><th>Pros/Cons</th></tr>
          <tr><td>Hierarchical</td><td>Tree-like structure (Parent-Child).</td><td>Fast navigation, but lacks flexibility (no N:M relationships easily).</td></tr>
          <tr><td>Network</td><td>Graph structure.</td><td>Handles many-to-many relationships, but complex to design.</td></tr>
          <tr><td>Relational</td><td>Tables (Rows and Columns).</td><td>Highly flexible, uses SQL. Most widely used today.</td></tr>
          <tr><td>Object-Oriented</td><td>Objects, classes, inheritance.</td><td>Good for complex data, steep learning curve.</td></tr>
        </table>
        """
      },
      {
        "title": "Relational Model & Keys",
        "content_html": """
        <p>The relational model represents data as a collection of tables (relations).</p>
        <ul>
          <li><strong>Super Key:</strong> A set of one or more attributes that uniquely identifies a row.</li>
          <li><strong>Candidate Key:</strong> A minimal super key.</li>
          <li><strong>Primary Key:</strong> A candidate key chosen by the database designer as the principal means of identifying rows.</li>
          <li><strong>Foreign Key:</strong> An attribute in one table that refers to the primary key in another table.</li>
        </ul>
        <div class="example"><strong>Example:</strong> In a Student table, (RollNo, Email) is a super key. RollNo is a candidate key and could be chosen as the Primary Key.</div>
        
        <h3>Integrity Constraints</h3>
        <p>Integrity constraints ensure data accuracy and consistency.</p>
        <ul>
          <li><strong>Domain Integrity:</strong> Ensures columns contain valid values (e.g., Age > 0).</li>
          <li><strong>Entity Integrity:</strong> Ensures the Primary Key is not NULL.</li>
          <li><strong>Referential Integrity:</strong> Ensures a Foreign Key value must match a valid Primary Key value in the referenced table.</li>
        </ul>
        """
      },
      {
        "title": "E-R Modeling",
        "content_html": """
        <p>The <strong>Entity-Relationship (E-R) Model</strong> is a conceptual data model that views the real world as a set of basic objects (entities) and relationships among them.</p>
        <ul>
          <li><strong>Entity:</strong> A "thing" or "object" in the real world (e.g., Student).</li>
          <li><strong>Attribute:</strong> Properties of an entity (e.g., Name, Age).</li>
          <li><strong>Relationship:</strong> An association among several entities.</li>
        </ul>
        
        <h3>Types of Attributes</h3>
        <ul>
          <li><strong>Simple vs Composite:</strong> Simple cannot be divided (e.g., Age), Composite can be divided (e.g., Name -> First, Last).</li>
          <li><strong>Single-valued vs Multivalued:</strong> Multivalued can have multiple values (e.g., Phone Numbers).</li>
          <li><strong>Derived:</strong> Value can be calculated from other attributes (e.g., Age derived from Date of Birth).</li>
        </ul>
        
        <h3>Generalization, Specialization, and Aggregation</h3>
        <p><strong>Generalization</strong> is a bottom-up approach combining lower-level entities into a higher-level entity. <strong>Specialization</strong> is top-down, breaking an entity into sub-entities. <strong>Aggregation</strong> treats a relationship as an entity itself to associate it with other entities.</p>
        """
      },
      {
        "title": "Normalization",
        "content_html": """
        <p><strong>Normalization</strong> is the process of organizing data to minimize redundancy and eliminate insertion, update, and deletion anomalies.</p>
        <ul>
          <li><strong>1NF (First Normal Form):</strong> Domain of each attribute contains only atomic (indivisible) values.</li>
          <li><strong>2NF (Second Normal Form):</strong> In 1NF and no partial dependencies (non-prime attributes must depend on the FULL primary key).</li>
          <li><strong>3NF (Third Normal Form):</strong> In 2NF and no transitive dependencies (non-prime attributes must not depend on other non-prime attributes).</li>
          <li><strong>BCNF (Boyce-Codd Normal Form):</strong> A stricter version of 3NF. For every functional dependency X -> Y, X must be a super key.</li>
        </ul>
        <div class="exam-trap"><strong>Exam Trap:</strong> Remember that BCNF is stricter than 3NF. A relation in BCNF is always in 3NF, but a relation in 3NF might not be in BCNF.</div>
        """
      }
    ]
  },
  {
    "unit": "II",
    "unit_title": "Unit II: Relational Algebra & SQL",
    "topics": [
      {
        "title": "Relational Algebra",
        "content_html": """
        <p><strong>Relational Algebra</strong> is a procedural query language. It consists of a set of operations that take one or two relations as input and produce a new relation as their result.</p>
        <p>Derived operations include Join, Intersection, and Division.</p>
        <div class="example"><strong>Example:</strong> Division is useful for queries like "Find students who have taken ALL courses."</div>
        
        <table border="1">
          <tr><th>Feature</th><th>Relational Algebra</th><th>Relational Calculus</th></tr>
          <tr><td>Nature</td><td>Procedural (How to get data).</td><td>Declarative (What data to get).</td></tr>
          <tr><td>Complexity</td><td>Easier to construct step-by-step.</td><td>Uses logical predicates.</td></tr>
        </table>
        """
      },
      {
        "title": "Introduction to SQL",
        "content_html": """
        <p>SQL (Structured Query Language) is the standard language for relational databases. It consists of several sub-languages:</p>
        <ul>
          <li><strong>DDL (Data Definition Language):</strong> CREATE, ALTER, DROP, TRUNCATE.</li>
          <li><strong>DML (Data Manipulation Language):</strong> INSERT, UPDATE, DELETE, SELECT.</li>
          <li><strong>DCL (Data Control Language):</strong> GRANT, REVOKE.</li>
          <li><strong>TCL (Transaction Control Language):</strong> COMMIT, ROLLBACK, SAVEPOINT.</li>
        </ul>
        """
      },
      {
        "title": "SQL Queries and Joins",
        "content_html": """
        <p><strong>Joins</strong> combine rows from two or more tables based on a related column between them.</p>
        <table border="1">
          <tr><th>Join Type</th><th>Description</th></tr>
          <tr><td>Inner Join</td><td>Returns records that have matching values in both tables.</td></tr>
          <tr><td>Left Outer Join</td><td>Returns all records from the left table, and matched records from the right table.</td></tr>
          <tr><td>Right Outer Join</td><td>Returns all records from the right table, and matched records from the left table.</td></tr>
          <tr><td>Full Outer Join</td><td>Returns all records when there is a match in either left or right table.</td></tr>
        </table>
        
        <h3>GROUP BY and HAVING</h3>
        <p>The <code>GROUP BY</code> statement groups rows that have the same values into summary rows. The <code>HAVING</code> clause was added to SQL because the <code>WHERE</code> keyword cannot be used with aggregate functions.</p>
        <div class="pro-tip"><strong>Pro-Tip:</strong> WHERE filters rows before grouping, whereas HAVING filters groups after grouping.</div>
        """
      },
      {
        "title": "Views",
        "content_html": """
        <p>A <strong>View</strong> is a virtual table based on the result-set of an SQL statement. It simplifies complex queries and enhances security by restricting access to underlying tables.</p>
        <table border="1">
          <tr><th>Simple View</th><th>Materialized View</th></tr>
          <tr><td>Virtual table. Re-evaluates query every time.</td><td>Physical copy of the data. Updated periodically.</td></tr>
          <tr><td>Performance can be slow for complex queries.</td><td>Faster performance as data is pre-computed.</td></tr>
        </table>
        """
      }
    ]
  },
  {
    "unit": "III",
    "unit_title": "Unit III: Advanced SQL & Transaction Management",
    "topics": [
      {
        "title": "Table Creation & Constraints",
        "content_html": """
        <p>SQL constraints are used to specify rules for the data in a table.</p>
        <ul>
          <li><strong>NOT NULL:</strong> Ensures that a column cannot have a NULL value.</li>
          <li><strong>UNIQUE:</strong> Ensures that all values in a column are different.</li>
          <li><strong>PRIMARY KEY:</strong> A combination of a NOT NULL and UNIQUE. Uniquely identifies each row.</li>
          <li><strong>FOREIGN KEY:</strong> Prevents actions that would destroy links between tables.</li>
          <li><strong>CHECK:</strong> Ensures that the values in a column satisfy a specific condition.</li>
        </ul>
        <div class="example"><strong>Example:</strong> A table can have multiple UNIQUE constraints (e.g., Email, Phone), but only ONE PRIMARY KEY to uniquely identify the row fundamentally.</div>
        """
      },
      {
        "title": "SQL Functions",
        "content_html": """
        <p>Functions in SQL provide powerful ways to manipulate strings, numbers, and dates.</p>
        <h3>Numeric Functions</h3>
        <p>ROUND rounds a number to a specified number of decimal places, while TRUNCATE simply chops off the decimals without rounding.</p>
        
        <h3>Date Functions</h3>
        <p>DATEDIFF returns the number of days between two dates. DATE_ADD adds a time/date interval to a date.</p>
        """
      },
      {
        "title": "Set Operations",
        "content_html": """
        <p>Set operators combine the results of two or more query blocks into a single result.</p>
        <table border="1">
          <tr><th>Operator</th><th>Function</th></tr>
          <tr><td>UNION</td><td>Combines results, removing duplicates.</td></tr>
          <tr><td>UNION ALL</td><td>Combines results, keeping duplicates.</td></tr>
          <tr><td>INTERSECT</td><td>Returns only rows found in both queries.</td></tr>
          <tr><td>MINUS / EXCEPT</td><td>Returns rows from the first query that are not in the second.</td></tr>
        </table>
        <div class="pro-tip"><strong>Pro-Tip:</strong> Both SELECT statements must have the same number of columns in the result sets with similar data types.</div>
        """
      },
      {
        "title": "Transaction Management",
        "content_html": """
        <p>A <strong>Transaction</strong> is a logical unit of work that contains one or more SQL statements.</p>
        <p>Transactions must follow the <strong>ACID properties</strong>:</p>
        <ul>
          <li><strong>Atomicity:</strong> "All or nothing" rule. Either all operations execute or none.</li>
          <li><strong>Consistency:</strong> Ensures the database moves from one consistent state to another.</li>
          <li><strong>Isolation:</strong> Concurrent transactions execute independently of one another.</li>
          <li><strong>Durability:</strong> Once a transaction is committed, changes are permanent, even after a system failure.</li>
        </ul>
        <div class="example"><strong>Example:</strong> In a bank transfer, deducting money from Account A and adding to Account B must be Atomic. If the system crashes after deduction but before addition, the transaction rolls back.</div>
        """
      },
      {
        "title": "Advanced Constructs",
        "content_html": """
        <p>Advanced constructs like CASE, COALESCE, and Stored Procedures provide programming capabilities within SQL.</p>
        <ul>
          <li><strong>CASE:</strong> Returns a value when the first condition is met (like an IF-THEN-ELSE statement).</li>
          <li><strong>COALESCE:</strong> Returns the first non-null value in a list.</li>
          <li><strong>Stored Procedure:</strong> Prepared SQL code that you can save, so the code can be reused over and over again.</li>
          <li><strong>Trigger:</strong> SQL code that automatically executes in response to certain events on a particular table.</li>
        </ul>
        <table border="1">
          <tr><th>BEFORE Trigger</th><th>AFTER Trigger</th></tr>
          <tr><td>Fires before the triggering event (INSERT/UPDATE/DELETE) completes.</td><td>Fires after the triggering event completes.</td></tr>
        </table>
        """
      }
    ]
  }
]

with open(r'c:\Users\nihal\OneDrive\Desktop\revision-hub\data\dbms\dbms_exhaustive_report.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("JSON generation complete.")
