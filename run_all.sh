#!/usr/bin/env bash
# Builds the QuickBite database from scratch and saves every query's
# output to outputs/. Usage:  ./run_all.sh   (needs psql on PATH)
set -euo pipefail

DB="${DB:-quickbite}"
cd "$(dirname "$0")"
mkdir -p outputs

PSQL=(psql -X -q -v ON_ERROR_STOP=1 -d "$DB" -P pager=off)

echo "==> Recreating database '$DB'"
dropdb --if-exists "$DB"
createdb "$DB"

echo "==> 01 schema";          "${PSQL[@]}" -f sql/01_schema.sql
echo "==> 02 indexes";         "${PSQL[@]}" -f sql/02_indexes.sql
echo "==> 03 seed data";       "${PSQL[@]}" -f sql/03_seed_data.sql > /dev/null

echo "==> Row counts"
"${PSQL[@]}" -c "
SELECT 'restaurant' AS table_name, COUNT(*) AS rows FROM restaurant
UNION ALL SELECT 'menu_item',      COUNT(*) FROM menu_item
UNION ALL SELECT 'customer',       COUNT(*) FROM customer
UNION ALL SELECT 'delivery_agent', COUNT(*) FROM delivery_agent
UNION ALL SELECT 'food_order',     COUNT(*) FROM food_order
UNION ALL SELECT 'order_item',     COUNT(*) FROM order_item
UNION ALL SELECT 'payment',        COUNT(*) FROM payment;" | tee outputs/00_row_counts.txt

echo "==> 04 queries      -> outputs/04_queries_output.txt"
"${PSQL[@]}" -f sql/04_queries.sql         > outputs/04_queries_output.txt 2>&1
echo "==> 05 index demo   -> outputs/05_index_demo_output.txt"
"${PSQL[@]}" -f sql/05_index_demo.sql      > outputs/05_index_demo_output.txt 2>&1
echo "==> 06 integrity    -> outputs/06_integrity_tests_output.txt"
"${PSQL[@]}" -f sql/06_integrity_tests.sql > outputs/06_integrity_tests_output.txt 2>&1

echo "Done."
