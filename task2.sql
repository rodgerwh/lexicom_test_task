-- Mocking up data:
-- Create short_names and full_names tables
CREATE TABLE short_names
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

CREATE TABLE full_names
(
    name   VARCHAR(64) UNIQUE,
    status BOOLEAN
);

-- Populate short_names with series of 1..700000 names
INSERT INTO short_names (name, status)
SELECT 'name.anothername' || GENERATE_SERIES(1, 700000), RANDOM() < 0.5;

-- Populate full_names with series of 1..400000 names and random extensions
INSERT INTO full_names (name)
SELECT 'name.anothername' || GENERATE_SERIES(1, 400000) || CASE WHEN RANDOM() < 0.5 THEN '.mp3' ELSE '.jpeg' END;

-- Add series of 700001-800000 unique entries with no match in short_names and different extensions just in case
INSERT INTO full_names (name)
SELECT 'name.anothername' || GENERATE_SERIES(700001, 800000) || CASE WHEN RANDOM() < 0.5 THEN '.wav' ELSE '.xlsx' END;

-- Copy short_names and full_names in random order so it won't be a best case scenario
CREATE TABLE short_names_random AS
SELECT name, status
FROM short_names
ORDER BY RANDOM();

CREATE TABLE full_names_random AS
SELECT name, status
FROM full_names
ORDER BY RANDOM();

-- Solutions:
-- Solution 1: truncate extensions using regexp, removing everything after the last dot (including the dot itself)
-- ~3-6 seconds of execution time on my machine
UPDATE full_names_random
SET status = short_names_random.status
FROM short_names_random
WHERE short_names_random.name = REGEXP_REPLACE(full_names_random.name, '\.[^.]*$', '');

-- Solution 2: get length of a reversed string, split it by dot, then extract first (length - extension length) chars
-- ~2 seconds of execution time on my machine
UPDATE full_names_random
SET status = short_names_random.status
FROM short_names_random
WHERE short_names_random.name = LEFT(full_names_random.name, LENGTH(full_names_random.name) -
                                                             LENGTH(SPLIT_PART(REVERSE(full_names_random.name), '.', 1)) -
                                                             1);
