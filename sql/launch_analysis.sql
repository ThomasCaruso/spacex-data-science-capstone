-- Falcon 9 launch analysis queries
-- Import the launch data into a table named SPACEXTBL before running.

-- 1. Unique launch sites
SELECT DISTINCT Launch_Site
FROM SPACEXTBL
ORDER BY Launch_Site;

-- 2. Records launched from CCAFS
SELECT *
FROM SPACEXTBL
WHERE Launch_Site LIKE 'CCAFS%';

-- 3. Total payload carried for NASA customers
SELECT SUM(PAYLOAD_MASS__KG_) AS total_nasa_payload_kg
FROM SPACEXTBL
WHERE Customer LIKE '%NASA%';

-- 4. Average payload for Falcon 9 version 1.1
SELECT AVG(PAYLOAD_MASS__KG_) AS average_payload_kg
FROM SPACEXTBL
WHERE Booster_Version LIKE 'F9 v1.1%';

-- 5. First successful ground-pad landing date
SELECT MIN(Date) AS first_successful_ground_landing
FROM SPACEXTBL
WHERE Landing_Outcome LIKE 'Success%ground pad%';

-- 6. Boosters with successful drone-ship landings in a payload range
SELECT Booster_Version, PAYLOAD_MASS__KG_, Date
FROM SPACEXTBL
WHERE Landing_Outcome LIKE 'Success%drone ship%'
  AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000
ORDER BY PAYLOAD_MASS__KG_;

-- 7. Landing outcome counts
SELECT Landing_Outcome, COUNT(*) AS outcome_count
FROM SPACEXTBL
GROUP BY Landing_Outcome
ORDER BY outcome_count DESC;

-- 8. Highest payload missions
SELECT Date, Booster_Version, Launch_Site, PAYLOAD_MASS__KG_
FROM SPACEXTBL
WHERE PAYLOAD_MASS__KG_ = (
    SELECT MAX(PAYLOAD_MASS__KG_)
    FROM SPACEXTBL
);

-- 9. Failed drone-ship landings in 2015
SELECT Date, Booster_Version, Launch_Site, Landing_Outcome
FROM SPACEXTBL
WHERE Landing_Outcome LIKE 'Failure%drone ship%'
  AND SUBSTR(Date, 1, 4) = '2015'
ORDER BY Date;

-- 10. Landing outcomes during a date interval
SELECT Landing_Outcome, COUNT(*) AS outcome_count
FROM SPACEXTBL
WHERE Date BETWEEN '2010-06-04' AND '2017-03-20'
GROUP BY Landing_Outcome
ORDER BY outcome_count DESC;
