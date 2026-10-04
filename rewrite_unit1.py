import json

with open('data/dbms/dbms_exhaustive_report.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find "Introduction to DBMS & Architecture"
for u in data:
    for t in u['topics']:
        if t['title'] == 'Introduction to DBMS & Architecture':
            # Rewrite it completely
            t['content_html'] = """
<p>A <strong>Database Management System (DBMS)</strong> is a powerful software system that allows users to create, maintain, and manage databases efficiently. It serves as a secure interface between the end-user and the raw data, ensuring that data is consistently organized and easily accessible.</p>

<p>Before the invention of DBMS, organizations relied on <strong>File-Based Systems</strong> where data was stored in flat files (like CSVs or text files). This older approach suffered from severe limitations, which modern DBMS architecture solves.</p>

<h4 style="margin-top:2rem;">DBMS vs File System</h4>
<p>The transition from file systems to DBMS was driven by the need to handle large, complex datasets securely. Here is a detailed comparison of the two approaches:</p>
<table border="1">
    <tr>
        <th>Feature</th>
        <th>File-Processing System</th>
        <th>Database Management System (DBMS)</th>
    </tr>
    <tr>
        <td><strong>Data Redundancy</strong></td>
        <td>High. The same data is often duplicated across multiple files, wasting storage.</td>
        <td>Minimal. Data is centralized and normalized, eliminating unnecessary duplication.</td>
    </tr>
    <tr>
        <td><strong>Data Inconsistency</strong></td>
        <td>High. If data is updated in one file but not another, inconsistencies arise.</td>
        <td>Low. Updates automatically propagate throughout the centralized database.</td>
    </tr>
    <tr>
        <td><strong>Data Access</strong></td>
        <td>Difficult. Requires writing custom application code for every new query.</td>
        <td>Easy. Uses declarative query languages like SQL to retrieve data instantly.</td>
    </tr>
    <tr>
        <td><strong>Data Independence</strong></td>
        <td>None. Applications are tightly coupled to the physical structure of the file.</td>
        <td>High. Applications are isolated from how the data is physically stored on disk.</td>
    </tr>
    <tr>
        <td><strong>Concurrent Access</strong></td>
        <td>Poor. Multiple users trying to edit a file simultaneously can corrupt it.</td>
        <td>Excellent. Uses locks and transactions to allow safe simultaneous edits.</td>
    </tr>
</table>

<h4 style="margin-top:2rem;">Data Abstraction (The 3-Schema Architecture)</h4>
<p>One of the primary advantages of a DBMS is <strong>Data Abstraction</strong>. Databases are incredibly complex internally, involving trees, hash tables, and pointers. However, end-users do not need to understand this complexity to use the database.</p>
<p>To achieve this, the ANSI-SPARC architecture divides the database into three levels of abstraction:</p>
<ul>
    <li><strong>Physical Level (Internal Schema):</strong> The lowest level of abstraction. It describes exactly <em>how</em> the data is stored on the physical hardware (e.g., contiguous blocks, B+ trees). This level is managed by the Database Administrator (DBA).</li>
    <li><strong>Logical Level (Conceptual Schema):</strong> The middle level. It describes <em>what</em> data is stored in the database and the relationships among that data. Programmers and developers operate at this level, viewing the data as tables and relationships without worrying about disk sectors.</li>
    <li><strong>View Level (External Schema):</strong> The highest level. It describes only a specific portion of the database relevant to a particular user. For example, a university clerk might only have a view of the student names, while the payroll department has a view of the salary data. This hides unnecessary data and enforces security.</li>
</ul>
<div class="pro-tip"><strong>Data Independence:</strong> This 3-schema architecture provides Data Independence. <strong>Logical Data Independence</strong> means you can change the logical schema (e.g., add a new column) without breaking the external views or applications. <strong>Physical Data Independence</strong> means you can change the physical storage (e.g., move data to a faster hard drive) without breaking the logical schema!</div>

<h4 style="margin-top:2rem;">Schema vs Instance</h4>
<p>It is critical to understand the distinction between a database's structure and its data. These are formally known as the Schema and the Instance.</p>
<p>A <strong>Schema</strong> is the overall logical blueprint or structural design of the database. It defines the tables, the columns, the data types, and the constraints (like Primary Keys). A schema is established when the database is first created and changes very rarely. Think of the schema as the architectural blueprint of a house.</p>
<p>An <strong>Instance</strong> (or State) is the actual collection of data stored in the database at a specific moment in time. Every time you insert a new row, update a value, or delete a record, the instance changes. While the schema is static, the instance is highly dynamic. Think of the instance as the furniture and people currently inside the house.</p>

<h4 style="margin-top:2rem;">Database Users and the DBA</h4>
<p>Databases are used by various people with different technical skills:</p>
<ul>
    <li><strong>Naive Users:</strong> End-users who interact with the system through GUI applications (e.g., bank tellers). They do not know SQL.</li>
    <li><strong>Application Programmers:</strong> Developers who write the backend code and queries to interact with the database.</li>
    <li><strong>Sophisticated Users:</strong> Analysts who write complex SQL queries directly to generate reports without writing application code.</li>
</ul>
<p>The <strong>Database Administrator (DBA)</strong> is the supreme controller of the database. Their responsibilities include designing the schema, managing storage, granting security permissions, taking backups, and monitoring performance.</p>
"""
            break

with open('data/dbms/dbms_exhaustive_report.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
print("Rewrote Unit I manually.")
