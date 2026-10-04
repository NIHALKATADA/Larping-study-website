import os
from bs4 import BeautifulSoup

html_file = "subjects/dbms/comprehensive-report.html"
with open(html_file, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find the article card that contains "Architecture" (which is Introduction to DBMS & Architecture)
intro_card = soup.find(lambda tag: tag.name == 'h4' and 'Architecture' in tag.text)
if intro_card:
    intro_card = intro_card.parent
    intro_card.clear()
    intro_card.append(BeautifulSoup("""<h4 id="sub_I_0">Introduction to DBMS & Architecture</h4>
<p>A <strong>Database Management System (DBMS)</strong> is a powerful software system that allows users to create, maintain, and manage databases efficiently. It serves as a secure interface between the end-user and the raw data, ensuring that data is consistently organized and easily accessible.</p>
<p>Before the invention of DBMS, organizations relied on <strong>File-Based Systems</strong> where data was stored in flat files (like CSVs or text files). This older approach suffered from severe limitations.</p>

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">DBMS vs File System</h5>
<p>The transition from file systems to DBMS was driven by the need to handle large, complex datasets securely. Here is a detailed comparison of the two approaches:</p>
<table border="1">
    <tr>
        <th>Feature</th>
        <th>File-Processing System</th>
        <th>Database Management System (DBMS)</th>
    </tr>
    <tr>
        <td><strong>Data Redundancy</strong></td>
        <td>High. The same data is often duplicated across multiple files.</td>
        <td>Minimal. Data is centralized and normalized.</td>
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

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">Data Abstraction (3-Schema Architecture)</h5>
<p>One of the primary advantages of a DBMS is <strong>Data Abstraction</strong>. Databases are incredibly complex internally, involving trees, hash tables, and pointers. However, end-users do not need to understand this complexity to use the database.</p>
<p>To achieve this, the ANSI-SPARC architecture divides the database into three levels of abstraction:</p>
<ul>
    <li><strong>Physical Level (Internal Schema):</strong> The lowest level of abstraction. It describes exactly <em>how</em> the data is stored on the physical hardware.</li>
    <li><strong>Logical Level (Conceptual Schema):</strong> The middle level. It describes <em>what</em> data is stored in the database and the relationships among that data.</li>
    <li><strong>View Level (External Schema):</strong> The highest level. It describes only a specific portion of the database relevant to a particular user.</li>
</ul>
<div class="pro-tip"><strong>Data Independence:</strong> This 3-schema architecture provides Data Independence. Logical Data Independence means you can change the logical schema without breaking the external views. Physical Data Independence means you can change the physical storage without breaking the logical schema!</div>

<h5 style="margin-top:2rem; font-size:1.2rem; color:var(--subject-color);">Schema and Instance</h5>
<p>It is critical to understand the distinction between a database's structure and its data.</p>
<p>A <strong>Schema</strong> is the overall logical blueprint or structural design of the database. It defines the tables, the columns, the data types, and the constraints (like Primary Keys). A schema is established when the database is first created and changes very rarely. Think of the schema as the architectural blueprint of a house.</p>
<p>An <strong>Instance</strong> (or State) is the actual collection of data stored in the database at a specific moment in time. Every time you insert a new row, update a value, or delete a record, the instance changes. While the schema is static, the instance is highly dynamic. Think of the instance as the furniture and people currently inside the house.</p>
""", 'html.parser'))

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Restored DBMS Unit 1 fixes.")
