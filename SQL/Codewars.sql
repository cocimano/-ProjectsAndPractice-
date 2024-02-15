/*
SQL Bug Fixing: Fix the QUERY - Totaling

Oh no! Timmys been moved into the database divison of his software company but as we know Timmy loves making mistakes. Help Timmy keep his job by fixing his query...

Timmy works for a statistical analysis company and has been given a task of totaling the number of sales on a given day grouped by each department name and then each day.

Resultant table:
day (type: date) {group by} [order by asc]
department (type: text) {group by} [In a real world situation it is bad practice to name a column after a table]
sale_count (type: int)
Tables and relationship below:
 
Solution:
*/

SELECT DISTINCT DATE (s.transaction_date) AS day, d.name AS department, COUNT(s.id) AS sale_count
FROM department d
INNER JOIN sale s ON d.id = s.department_id
GROUP BY d.name, day
ORDER BY day ASC

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
Calculating Batting Average
In baseball, the batting average is a simple and most common way to measure a hitter's performace. Batting average is calculated by taking all the players hits and dividing it by their number of at_bats, and it is usually displayed as a 3 digit decimal (i.e. 0.300).
Given a yankees table with the following schema,
-player_id STRING
-player_name STRING
-primary_position STRING
-games INTEGER
-at_bats INTEGER
-hits INTEGER
return a table with player_name, games, and batting_average.
We want batting_average to be rounded to the nearest thousandth, since that is how baseball fans are used to seeing it. Format it as text and make sure it has 3 digits to the right of the decimal (pad with zeroes if neccesary).
Next, order our resulting table by batting_average, with the highest average in the first row.
Finally, since batting_average is a rate statistic, a small number of at_bats can change the average dramatically. To correct for this, exclude any player who doesn't have at least 100 at bats.

Expected Output Table
-player_name STRING
-games INTEGER
-batting_average STRING

Solution:
*/
SELECT player_name, games, CAST(ROUND(hits::NUMERIC / at_bats, 3) AS DECIMAL(10,3))::TEXT AS batting_average
FROM yankees
WHERE at_bats >= 100
ORDER BY batting_average DESC

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
SQL: Disorder
You are given a table numbers with just one column, number. It holds some numbers that are already ordered.
You need to write a query that makes them un-ordered, as in, every possible ordering should appear equally often.

Solution:
*/
SELECT *
FROM numbers
ORDER BY RANDOM()

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
SQL with Pokemon: Damage Multipliers
You have arrived at the Celadon Gym to battle Erika for the Rainbow Badge.
She will be using Grass-type Pokemon. Any fire pokemon you have will be strong against grass, but your water types will be weakened. The multipliers table within your Pokedex will take care of that.
Using the following tables, return the pokemon_name, modifiedStrength and element of the Pokemon whose strength, after taking these changes into account, is greater than or equal to 40, ordered from strongest to weakest.
pokemon schema
id
pokemon_name
element_id
str

multipliers schema
id
element
multiplier

Solution:
*/
SELECT p.pokemon_name, (p.str * m.multiplier) AS modifiedStrength, m.element
FROM pokemon p
LEFT JOIN multipliers m ON p.element_id = m.id
WHERE modifiedStrength >= 40
ORDER BY modifiedStrength DESC

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
SQL Basics: Simple table totaling
For this challenge you need to create a simple query to display each unique clan with their total points and ranked by their total points.
people table schema
name
points
clan
You should then return a table that resembles below
select on
rank
clan
total_points
total_people
The query must rank each clan by their total_points, you must return each unqiue clan and if there is no clan name (i.e. it's an empty string) you must replace it with [no clan specified], you must sum the total_points for each clan and the total_people within that clan.
Note The data is loaded from the live leaderboard, this means values will change but also could cause the kata to time out retreiving the information.

Solution:
*/
SELECT DISTINCT ROW_NUMBER() OVER (ORDER BY SUM(points) DESC) AS rank, 
COALESCE(NULLIF(clan,''), '[no clan specified]') AS clan, 
SUM(points) AS total_points, 
COUNT(name) AS total_people
FROM people
GROUP BY clan
ORDER BY SUM(points) DESC

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
SQL Basics - Monsters using CASE
You have access to two tables named top_half and bottom_half, as follows:

top_half schema
id
heads
arms

bottom_half schema
id
legs
tails

You must return a table with the format as follows:

output schema

id
heads
legs
arms
tails
species

The IDs on the tables match to make a full monster. For heads, arms, legs and tails you need to draw in the data from each table.

For the species, if the monster has more heads than arms, more tails than legs, or both, it is a 'BEAST' else it is a 'WEIRDO'. This needs to be captured in the species column.

All rows should be returned (10).

Tests require the use of CASE. Order by species.

Solution:
*/
SELECT t.id, t.heads, t.arms, b.legs, b.tails, 
(CASE
  WHEN t.heads > t.arms OR b.tails > b.legs THEN 'BEAST'
  ELSE 'WEIRDO'
END) AS species
FROM top_half t JOIN bottom_half b ON t.id = b.id
ORDER BY species

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/

/*
SQL Bug Fixing: Fix the JOIN
Oh no! Timmys been moved into the database divison of his software company but as we know Timmy loves making mistakes. Help Timmy keep his job by fixing his query...

Timmy works for a statistical analysis company and has been given a task of calculating the highest average salary for a given job, the sample is compiled of 100 applicants each with a job and a salary. Timmy must display each unique job, the total average salary, the total people and the total salary and order by highest average salary. Timmy has some bugs in his query, help Timmy fix his query so he can keep his job!


people table schema
id
name

job table schema
id
people_id
job_title
salary

resultant table schema
job_title (unique)
average_salary (float, 2 dp)
total_people (int)
total_salary (float, 2 dp)

Solution:
*/
SELECT DISTINCT j.job_title
	,CAST(ROUND((SUM(j.salary) / COUNT(p)), 2) AS FLOAT) AS average_salary
	,COUNT(p.id) AS total_people
	,CAST(ROUND(SUM(j.salary), 2) AS FLOAT) AS total_salary
FROM people p
INNER JOIN job j ON p.id = j.people_id
GROUP BY j.job_title
ORDER BY average_salary DESC

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
SQL Basics: Simple PIVOTING data WITHOUT CROSSTAB
This kata is inspired by SQL Basics: Simple PIVOTING data by matt c.
You need to build a pivot table WITHOUT using CROSSTAB function. Having two tables products and details you need to select a pivot table of products with counts of details occurrences (possible details values are ['good', 'ok', 'bad'].
Results should be ordered by product's name.
Model schema for the kata is:

your query should return table with next columns
name
good
ok
bad
Compare your table to the expected table to view the expected results.

Solution:
*/
SELECT p.name,
(SELECT COUNT(d.detail) FROM details d WHERE detail = 'good' AND p.id = d.product_id ) as good,
(SELECT COUNT(d.detail) FROM details d WHERE detail = 'ok' AND p.id = d.product_id) as ok,
(SELECT COUNT(d.detail) FROM details d WHERE detail = 'bad' AND p.id = d.product_id) as bad
FROM products p INNER JOIN details d ON p.id = d.product_id
GROUP BY p.name, p.id
ORDER BY p.name

/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
SQL Basics: Simple Hierarchical structure
NOTE: Most difficult query at the moment, required further investigation.
For this challenge you need to create a RECURSIVE Hierarchical query. You have a table employees of employees, you must order each employee by level. You must use a WITH statement and name it employee_levels after that has been defined you must select from it.
A Level is in correlation what manager managers the employee. e.g. an employee with a manager_id of NULL is at level 1 and then direct employees with the employee at level 1 will be level 2.
employees table schema
id
first_name
last_name
manager_id (can be NULL)

resultant schema
level
id
first_name
last_name
manager_id (can be NULL)

Solution:
*/
WITH RECURSIVE employee_levels AS (
  SELECT 1 AS level, id, first_name, last_name, manager_id
  FROM employees
  WHERE manager_id IS NULL
  UNION ALL
  SELECT (el.level + 1) AS level, e.id, e.first_name, e.last_name, e.manager_id
  FROM employees e
  INNER JOIN employee_levels el ON e.manager_id = el.id
)
SELECT *
FROM employee_levels
ORDER BY level, id;
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
SQL Basics: Group By Day
There is an events table used to track different key activities taken on a website. For this task you need to:
find the entries whose name equals "trained"
group them by the day the activity happened (the date part of the created_at timestamp) and their description's
the 2 aforementioned fields should be returned together with the number of grouped entries in a column called count
the result should also be sorted by day
"events" table schema
id (bigint)
name (text)
created_at (timestamp)
description (text)
expected result schema
day (date)
description (text)
count (numeric)
Solution:
*/
SELECT DATE(created_at) AS day, description, COUNT(description) AS count
FROM events
WHERE name = 'trained'
GROUP BY DATE(created_at), description
ORDER BY DATE(created_at)
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
SQL Basics: Simple HAVING
For this challenge you need to create a simple HAVING statement, you want to count how many people have the same age and return the groups with 10 or more people who have that age.
people table schema
id
name
age
return table schema
age
total_people
Solution:
*/
SELECT age, COUNT(age) AS total_people
FROM people
GROUP BY age
HAVING COUNT(age) >= 10
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
Youngest Team Members
You are working with a database that stores information about employees in a tech firm. The database includes a table named employees with the following columns:
employee_id: A unique integer identifier for each employee.
full_name: A string representing the employee's full name.
team: A string that specifies which team the employee is part of. The team can be one of the following four: "backend", "frontend", "devops", or "design".
birth_date: A date that represents the employee's birthdate.
The company is planning an event where the youngest employee from each team will be given a chance to share their vision of future technology trends.
Your task is to write an SQL query that retrieves the complete record for the youngest member of each team. You should consider the person with the latest birthdate as the youngest. Let's assume for this task that the are no youngest employees who share the same birthdate.
The classical solution of using aggregate function and group by is forbidden. Can you come up with something more witty?
The result should be ordered by team in asc alphabetical order.
Good luck!
Desired Output
The desired output should look like this:
employee_id	full_name	team	birth_date
11	John Doe	backend	1980-12-01
7	Jane Smith	design	1985-05-03
24	Bob Jones	devops	1990-04-15
54	Dana Smith	frontend	1995-05-03
Solution:
*/
SELECT DISTINCT e.employee_id, e.full_name, e.team, e.birth_date
FROM employees e
WHERE e.birth_date >= ALL (
  SELECT b.birth_date 
  FROM employees b 
  WHERE b.team = e.team)
ORDER BY e.team, e.birth_date
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
Dealing With Messy Data
Your company has an internal policy to determine your customers' credit limit, but this procedure has been questioned recently by the board as being too conservative.
Your CEO wants to increase the current customer base credit limits in order to upsell a new line of products. In order to do that, the company hired several external consultancies to produce new credit limit estimates.
The problem is that each agency has produced the report in its own format. Some use the format "First-name Last-name" to identify a person, others use the format "Last-name, First-name". There is also no consensus on how to capitalize each word, so some used all uppercase, others used all lowercase, and some used mixed-case.
Also, some names are titled, for example: "Dr. Hannibal Lecter", "Robert Downey Jr." etc, so you will need to pay attention to any such or similar cases.
Internally, the data is structured as follows:
Table: customers
================
id: INT
first_name: TEXT
last_name: TEXT
credit_limit: FLOAT

The data you've received from all agencies was consolidated in the following table:

Table: prospects
================
full_name: TEXT
credit_limit: FLOAT
Keep in mind that the agencies had access only to a partial customer base. There is also the possibility of more than one agency prospecting the same customer, so it's highly likely that there will be duplicates. Finally, they've prospected customers that were not in your customer base as well.
For this task you are interested in the prospected customers that are already in your customer base and the prospected credit limit is higher than your internal estimate. When more than one agency prospected the same customer, chose the highest estimate.
You have to produce a report with the following fields:
first_name
last_name
old_limit [the current credit_limit]
new_limit [the highest credit_limit found]
Good luck!
Notes:
•	only list the customers that a higher credit limit was found.
Solution:
*/
CREATE INDEX ON customers (lower(first_name || ' ' || last_name), lower(first_name || ',' || last_name));
CREATE INDEX ON prospects (lower(full_name));

SELECT a.first_name,
       a.last_name,
       a.credit_limit AS old_limit,
       max(b.credit_limit) AS new_limit
FROM customers a JOIN prospects b
  ON lower(full_name) IN (
    lower(a.first_name || ' ' || a.last_name),
    lower(a.last_name || ', ' || a.first_name)
  )
GROUP BY a.id 
  HAVING max(b.credit_limit) > a.credit_limit
ORDER BY first_name, last_name
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/
/*
SQL Basics: Simple PIVOTING data
For this challenge you need to PIVOT data. You have two tables, products and details. Your task is to pivot the rows in products to produce a table of products which have rows of their detail. Group and Order by the name of the Product.
Tables and relationship below:
 
products table schema
- id   - integer
- name - text
details table schema
- id          - integer
- product_id  - integer
- detail      - text
You must use the CROSSTAB statement to create a table that has the schema as below:
CROSSTAB table schema
- name  - text
- bad   - bigint
- good  - bigint
- ok    - bigint
If the values aren't assigned to the last three columns within the query directly, it's assumed they will be presented in the lexicographical order (i.e. if we have three values, a, b and c, then bad, good and ok will have these values respectively).
Compare your table to the expected table to view the expected results.
Solution:
*/
CREATE EXTENSION tablefunc;

SELECT *
FROM CROSSTAB (
  'SELECT p.name, d.detail, COUNT(*)
  FROM products p
  JOIN details d ON p.id = d.product_id
  GROUP BY 1, 2
  ORDER BY 1, 2',
  'VALUES (''bad''::text), (''good''::text), (''ok''::text)'
) AS product_pivot (name text, bad bigint, good bigint, ok bigint);
/*
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
*/





