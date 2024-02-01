-- RECURSIVE SQL QUERIES in PostgreSQL, Oracle, MSSQL & MySQL
/* Recursive Query Structure/Syntax
WITH [RECURSIVE] CTE_name AS
	(
     SELECT query (Non Recursive query or the Base query)
	    UNION [ALL]
	 SELECT query (Recursive query using CTE_name [with a termination condition])
	)
SELECT * FROM CTE_name;
*/

/* Difference in Recursive Query syntax for PostgreSQL, Oracle, MySQL, MSSQL.
- Syntax for PostgreSQL and MySQL is the same.
- In MSSQL, RECURSIVE keyword is not required and we should use UNION ALL instead of UNION.
- In Oracle, RECURSIVE keyword is not required and we should use UNION ALL instead of UNION. Additionally, we need to provide column alias in WITH clause itself
*/

-- Queries:
-- Q1: Display number from 1 to 10 without using any in built functions.
-- Q2: Find the hierarchy of employees under a given manager "Asha".
-- Q3: Find the hierarchy of managers for a given employee "David".

-- Q1: Display number from 1 to 10 without using any in built functions.
WITH numbers AS
(
	SELECT 1 AS n
	UNION ALL
	SELECT n + 1
	FROM numbers --mandatory to use de CTE_NAME in the recursive part
	WHERE n <10
)
SELECT * FROM numbers;

-- Q2: Find the hierarchy of employees under a given manager "Asha".
WITH employees_of_Asha AS (
	SELECT id, name, manager_id, designation, 1 AS lvl FROM emp_details WHERE name = 'Asha'
	UNION ALL
	SELECT e.id, e.name, e.manager_id, e.designation, a.lvl+1 as lvl
	FROM employees_of_Asha a
	JOIN emp_details e ON a.id = e.manager_id
)
SELECT a2.id AS emp_id, a2.name AS emp_name, e2.name AS manager_name, a2.lvl AS level 
FROM employees_of_Asha a2
JOIN emp_details e2 ON e2.id = a2.manager_id;

-- Q3: Find the hierarchy of managers for a given employee "David".
WITH managers_of_David AS (
	SELECT id, name, manager_id, designation, 1 AS lvl FROM emp_details WHERE name = 'David'
	UNION ALL
	SELECT e.id, e.name, e.manager_id, e.designation, d.lvl+1 as lvl
	FROM managers_of_David d
	JOIN emp_details e ON d.manager_id = e.id
)
SELECT a2.id AS emp_id, a2.name AS emp_name, e2.name AS manager_name, a2.lvl AS level 
FROM managers_of_David a2
JOIN emp_details e2 ON e2.id = a2.manager_id;
