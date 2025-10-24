-- Combines daily COVID case data with static population data,
-- filtering by date to create the base dataset for analysis.
SELECT
    r.date,
    r.region,
    r.subregion,
    r.cases,
    p.population
FROM
    covid AS r
JOIN
    population AS p ON r.region = p.region AND r.subregion = p.subregion
WHERE
    r.date >= :start_date AND r.date <= :end_date
ORDER BY
    r.region, r.subregion, r.date;
