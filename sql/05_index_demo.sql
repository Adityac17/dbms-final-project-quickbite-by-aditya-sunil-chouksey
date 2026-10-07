-- =====================================================================
-- QuickBite — 05_index_demo.sql
-- Proves idx_restaurant_cuisine_location removes the full table scan.
-- Loads 200,000 synthetic restaurants (a "large catalogue"), compares
-- the query plan WITHOUT and WITH the index, then ROLLS BACK so the
-- real sample data is untouched.
-- =====================================================================

BEGIN;

INSERT INTO restaurant (name, cuisine, location, address, phone, rating)
SELECT 'Test Kitchen ' || g,
       (ARRAY['North Indian','South Indian','Chinese','Italian','Mughlai',
              'Street Food','Continental','Malvani','Bengali','Gujarati',
              'Mexican','Thai'])[1 + g % 12],
       (ARRAY['Kharghar','Vashi','Powai','Andheri West','Bandra West',
              'Thane West','Nerul','Panvel','Belapur','Airoli','Dadar',
              'Colaba','Borivali','Malad','Goregaon','Chembur','Ghatkopar',
              'Mulund','Worli','Juhu'])[1 + (g / 12) % 20],
       'Synthetic address ' || g,
       'T' || lpad(g::TEXT, 10, '0'),
       round((3 + random() * 2)::NUMERIC, 1)
FROM generate_series(1, 200000) AS g;

ANALYZE restaurant;

\echo
\echo '---- Catalogue size ----'
SELECT COUNT(*) AS restaurants FROM restaurant;

-- ---------------------------------------------------------------------
\echo
\echo '==== 1) WITHOUT the index  -> expect Seq Scan (full table scan) ===='
DROP INDEX idx_restaurant_cuisine_location;

EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT restaurant_id, name, rating
FROM   restaurant
WHERE  cuisine = 'North Indian' AND location = 'Kharghar';

-- ---------------------------------------------------------------------
\echo
\echo '==== 2) WITH the index     -> expect Index / Bitmap Index Scan ===='
CREATE INDEX idx_restaurant_cuisine_location ON restaurant (cuisine, location);
ANALYZE restaurant;

EXPLAIN (ANALYZE, COSTS OFF, SUMMARY ON)
SELECT restaurant_id, name, rating
FROM   restaurant
WHERE  cuisine = 'North Indian' AND location = 'Kharghar';

-- ---------------------------------------------------------------------
\echo
\echo '==== 3) Leftmost-prefix: cuisine-only search also uses the index ===='
EXPLAIN (COSTS OFF)
SELECT restaurant_id, name FROM restaurant WHERE cuisine = 'Italian';

\echo
\echo '==== 4) Location-only search (2nd column only) ===='
\echo 'PostgreSQL <= 17: cannot seek -> Seq Scan.'
\echo 'PostgreSQL 18+ : B-tree "skip scan" probes ~once per distinct cuisine'
\echo '                 (see "Index Searches") - works, but costlier than a'
\echo '                 leading-column seek. Order columns by search pattern.'
EXPLAIN (ANALYZE, COSTS OFF, SUMMARY OFF)
SELECT restaurant_id, name FROM restaurant WHERE location = 'Powai';

ROLLBACK;   -- discard synthetic rows; original index definition restored
