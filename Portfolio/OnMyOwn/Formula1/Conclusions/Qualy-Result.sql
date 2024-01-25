/*
SELECT r.driverId, r.raceId, r.grid, r.position
FROM results r
ORDER BY r.raceId

SELECT driverId, raceId, position
FROM qualifying
ORDER BY raceId
*/

/*
SELECT r.driverId, r.raceId, r.grid, r.position, (r.grid - r.position) AS gap,
CASE
	WHEN gap = 0 THEN 'STILL'
	WHEN gap > 0 THEN 'UP'
	WHEN gap < 0 THEN 'DOWN'
END AS DIFF
FROM results r JOIN qualifying q ON r.raceId = q.raceId
WHERE r.grid = q.position
*/

SELECT r.driverId, r.raceId, r.grid, r.position,
    CASE
		WHEN (r.grid - r.position) IS NULL THEN 'INVALID'
        WHEN r.grid - r.position = 0 THEN 'STILL'
        WHEN r.grid - r.position > 0 THEN 'UP'
        ELSE 'DOWN'
    END AS gap
FROM 
    results r 
JOIN 
    qualifying q ON r.raceId = q.raceId AND r.driverId = q.driverId
WHERE 
    r.grid = q.position;

