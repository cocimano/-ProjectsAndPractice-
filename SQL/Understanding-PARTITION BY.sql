SELECT TOP 50 nombre, pais, calificacion_CREDITO, COUNT(calificacion_CREDITO) OVER (PARTITION BY calificacion_CREDITO) AS totalCalificacion
FROM clientes

SELECT TOP 50 nombre, pais, calificacion_CREDITO, COUNT(calificacion_CREDITO)
FROM clientes
GROUP BY nombre, pais, calificacion_CREDITO

SELECT DISTINCT calificacion_CREDITO, COUNT(calificacion_CREDITO)
FROM clientes
GROUP BY calificacion_CREDITO

SELECT pais,
CASE
	WHEN calificacion_CREDITO = 'BUENA' THEN 'buena'
END
FROM clientes
