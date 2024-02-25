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





