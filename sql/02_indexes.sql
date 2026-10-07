-- =====================================================================
-- QuickBite — 02_indexes.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- ADVANCED CONCEPT: composite search index
-- The app's most common search is "restaurants of cuisine X in area Y".
-- A B-tree on (cuisine, location) lets the planner jump straight to the
-- matching keys instead of scanning the whole restaurant table.
-- Column order matters: cuisine first, so the index ALSO serves
-- "cuisine only" searches (leftmost-prefix rule). A search on location
-- alone cannot seek on it (PostgreSQL 18+ can "skip scan" it, one probe
-- per distinct cuisine, but that is still costlier than a direct seek).
-- ---------------------------------------------------------------------
CREATE INDEX idx_restaurant_cuisine_location
    ON restaurant (cuisine, location);

-- ---------------------------------------------------------------------
-- Supporting indexes on foreign keys. PostgreSQL does not index FK
-- columns automatically; these speed up the JOINs in 04_queries.sql
-- and the RESTRICT checks when a parent row is deleted.
-- (order_item.order_id is already covered by its composite PK.)
-- ---------------------------------------------------------------------
CREATE INDEX idx_menu_item_restaurant   ON menu_item  (restaurant_id);
CREATE INDEX idx_food_order_restaurant  ON food_order (restaurant_id);
CREATE INDEX idx_food_order_customer    ON food_order (customer_id);
CREATE INDEX idx_food_order_agent       ON food_order (delivery_agent_id);
CREATE INDEX idx_order_item_menu_item   ON order_item (menu_item_id);
