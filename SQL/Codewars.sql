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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*
SQL: Disorder
You are given a table numbers with just one column, number. It holds some numbers that are already ordered.
You need to write a query that makes them un-ordered, as in, every possible ordering should appear equally often.

Solution:
*/
SELECT *
FROM numbers
ORDER BY RANDOM()

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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







