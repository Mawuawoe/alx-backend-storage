-- SQL script that lists all bands with Glam rock as their main style, ranked by their longevity
-- sql statement 
SELECT band_name,
CASE
WHEN split IS NOT NULL THEN LEAST(split, 2022) - formed
ELSE 2022 - formed
END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
