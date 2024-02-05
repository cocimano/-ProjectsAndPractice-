/*
SQL for Data Analysis: Advanced Techniques for Transforming Data into Insights
--https://github.com/cathytanimura/sql_book/tree/master
*/
 
--Chapter 2: Preparing Data for Analysis
SELECT *
FROM emp_details

--This will tell you whether there are any cases of duplicates. If the query returns 0, you’re good to go.
SELECT count(*)
FROM
(
 SELECT id, name, manager_id, salary, designation
 , count(*) as records
 FROM emp_details
 GROUP BY id, name,manager_id, salary, designation
) a
WHERE records > 1
;--Alternative with HAVING
SELECT id, name, manager_id, salary, designation, COUNT(*) as records
FROM emp_details
GROUP BY id, name,manager_id, salary, designation
HAVING COUNT(*) > 1
;
