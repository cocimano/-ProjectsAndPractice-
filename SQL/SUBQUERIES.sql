-- TYPES OF SUBQUERY
--------------------------------------------------------------------------------
/* < SCALAR SUBQUERY > */
/* QUESTION: Find the employees who earn more than the average salary earned by all employees. */
-- Scalar subquery return exactly 1 row and 1 column
SELECT AVG(salary) FROM employee; --5791.6666666666666667

SELECT *
FROM employee
WHERE salary > (
	SELECT AVG(salary)
	FROM employee
);

--------------------------------------------------------------------------------
/* < MULTIPLE ROW SUBQUERY > */
-- Multiple column, multiple row subquery
/* QUESTION: Find the employees who earn the highest salary in each department. */
--1) find the highest salary in each department.
--2) filter the employees based on above result.
SELECT *
FROM employee e
WHERE e.salary >= ( 
	SELECT MAX(e2.salary)
	FROM employee e2
	WHERE e2.dept_name = e.dept_name
);

--VIDEO SOLUTION (Same Result). Multiple columns and rows
SELECT *
FROM employee
WHERE (dept_name,salary) IN (
	SELECT dept_name, MAX(salary)
	FROM employee
	GROUP BY dept_name
);
-- Single column, multiple row subquery
/* QUESTION: Find department who do not have any employees */
--1) find the departments where employees are present.
--2) from the department table filter out the above results.
SELECT *
FROM department
WHERE dept_name NOT IN (
	SELECT dept_name
	FROM employee
	INNER JOIN department USING (dept_name)
);
--Easier solution
SELECT *
FROM department
WHERE dept_name NOT IN (
	SELECT DISTINCT dept_name
	FROM employee
);


--------------------------------------------------------------------------------
/* < CORRELATED SUBQUERY >
-- A subquery which is related to the Outer query
/* QUESTION: Find the employees in each department who earn more than the average salary in that department. */
1) find the avg salary per department
2) filter data from employee tables based on avg salary from above result.
*/
SELECT *
FROM employee e
WHERE e.salary > ( 
	SELECT AVG(e2.salary)
	FROM employee e2
	WHERE e2.dept_name = e.dept_name
);
--QUESTION: Find department who do not have any employees */
SELECT *
FROM department d
WHERE NOT EXISTS (
	SELECT 1
	FROM employee e2
	WHERE e2.dept_name = d.dept_name
);

--------------------------------------------------------------------------------
/* < NESTED SUBQUERY >
-- A subquery inside n subqueries
QUESTION: Find stores who's sales where better than the average sales accross all stores.
1) find the total sales for each store
2) find avg sales for all the stores
3) compare 1 and 2
*/

SELECT store_name
FROM sales
GROUP BY store_name
HAVING SUM(price) > (
	SELECT AVG(total)
	FROM (
		SELECT store_name, SUM(price) as total
		FROM sales
		GROUP BY store_name
	)
);

-- CLAUSES WHERE SUBQUERY CAN BE USED
--------------------------------------------------------------------------------
/* < Using Subquery in WHERE clause > */
/* QUESTION:  Find the employees who earn more than the average salary earned by all employees. */
select *
from employee e
where salary > (select avg(salary) from employee)
order by e.salary;


--------------------------------------------------------------------------------
/* < Using Subquery in FROM clause > */
/* QUESTION: Find stores who's sales where better than the average sales accross all stores */
-- Using WITH clause
with sales as
	(select store_name, sum(price) as total_sales
	 from sales
	 group by store_name)
select *
from sales
join (select avg(total_sales) as avg_sales from sales) avg_sales
	on sales.total_sales > avg_sales.avg_sales;


--------------------------------------------------------------------------------
/* < USING SUBQUERY IN SELECT CLAUSE > */
-- Only subqueries which return 1 row and 1 column is allowed (scalar or correlated)
/* QUESTION: Fetch all employee details and add remarks to those employees who earn more than the average pay. */
select e.*
, case when e.salary > (select avg(salary) from employee)
			then 'Above average Salary'
	   else null
  end remarks
from employee e;

-- Alternative approach
select e.*
, case when e.salary > avg_sal.sal
			then 'Above average Salary'
	   else null
  end remarks
from employee e
cross join (select avg(salary) sal from employee) avg_sal;



--------------------------------------------------------------------------------
/* < Using Subquery in HAVING clause > */
/* QUESTION: Find the stores who have sold more units than the average units sold by all stores. */
select store_name, sum(quantity) Items_sold
from sales
group by store_name
having sum(quantity) > (select avg(quantity) from sales);




-- SQL COMMANDS WHICH ALLOW A SUBQUERY
--------------------------------------------------------------------------------
/* < Using Subquery with INSERT statement > */
/* QUESTION: Insert data to employee history table. Make sure not insert duplicate records. */
insert into employee_history
select e.emp_id, e.emp_name, d.dept_name, e.salary, d.location
from employee e
join department d on d.dept_name = e.dept_name
where not exists (select 1
				  from employee_history eh
				  where eh.emp_id = e.emp_id);


--------------------------------------------------------------------------------
/* < Using Subquery with UPDATE statement > */
/* QUESTION: Give 10% increment to all employees in Bangalore location based on the maximum
salary earned by an emp in each dept. Only consider employees in employee_history table. */
update employee e
set salary = (select max(salary) + (max(salary) * 0.1)
			  from employee_history eh
			  where eh.dept_name = e.dept_name)
where dept_name in (select dept_name
				   from department
				   where location = 'Bangalore')
and e.emp_id in (select emp_id from employee_history);


--------------------------------------------------------------------------------
/* < Using Subquery with DELETE statement > */
/* QUESTION: Delete all departments who do not have any employees. */
delete from department d1
where dept_name in (select dept_name from department d2
				    where not exists (select 1 from employee e
									  where e.dept_name = d2.dept_name));


