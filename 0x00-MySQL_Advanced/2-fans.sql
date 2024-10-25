-- import a table and group by origin, sum fans from each origin and order dsec;
-- sql statement group by / order by
SELECT origin, SUM(fans) AS nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
