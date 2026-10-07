-- QuickBite — 04_queries.sql : Query set (JOINs, subqueries, aggregates)


-- Q1. Most frequently ordered dish for each restaurant
-- JOIN order-lines + MenuItem, GROUP BY, COUNT, per-restaurant
SELECT r.restaurant_id,
       r.name                AS restaurant,
       m.name                AS most_popular_dish,
       COUNT(*)              AS times_ordered,      
       SUM(oi.quantity)      AS units_sold
FROM   order_item oi
JOIN   menu_item  m  ON m.menu_item_id  = oi.menu_item_id
JOIN   food_order fo ON fo.order_id     = oi.order_id
JOIN   restaurant r  ON r.restaurant_id = m.restaurant_id
WHERE  fo.status <> 'Cancelled'
GROUP  BY r.restaurant_id, r.name, m.menu_item_id, m.name
HAVING COUNT(*) = (
        -- ranking subquery: the highest order-count of any dish
        -- belonging to THIS restaurant (correlated on r.restaurant_id)
        SELECT MAX(dish_count)
        FROM  (SELECT COUNT(*) AS dish_count
               FROM   order_item oi2
               JOIN   menu_item  m2  ON m2.menu_item_id = oi2.menu_item_id
               JOIN   food_order fo2 ON fo2.order_id    = oi2.order_id
               WHERE  m2.restaurant_id = r.restaurant_id
                 AND  fo2.status <> 'Cancelled'
               GROUP  BY oi2.menu_item_id) AS per_dish
       )
ORDER  BY r.restaurant_id, m.name;




-- Q2. Revenue generated per restaurant — GROUP BY + SUM on order totals
-- (LEFT JOIN keeps restaurants with no delivered orders at 0)
SELECT r.restaurant_id,
       r.name AS restaurant,
       r.cuisine,
       COUNT(t.order_id) AS delivered_orders,
       COALESCE(SUM(t.order_total), 0) AS total_revenue,
       COALESCE(ROUND(AVG(t.order_total), 2), 0) AS avg_order_value
FROM   restaurant r
LEFT   JOIN v_order_total t
       ON  t.restaurant_id = r.restaurant_id
       AND t.status        = 'Delivered'
GROUP  BY r.restaurant_id, r.name, r.cuisine
ORDER  BY total_revenue DESC;



-- Q3. Browse restaurants by cuisine + area (served by
-- idx_restaurant_cuisine_location — see 05_index_demo.sql)
SELECT restaurant_id, name, cuisine, location, rating
FROM   restaurant
WHERE  cuisine  = 'North Indian'
  AND  location = 'Kharghar'
  AND  is_active
ORDER  BY rating DESC;


-- Q4. Restaurants earning above the average restaurant revenue
-- (subquery in HAVING)
SELECT r.name AS restaurant, SUM(t.order_total) AS total_revenue
FROM   restaurant r
JOIN   v_order_total t ON t.restaurant_id = r.restaurant_id
WHERE  t.status = 'Delivered'
GROUP  BY r.restaurant_id, r.name
HAVING SUM(t.order_total) > (
        SELECT AVG(rest_rev)
        FROM  (SELECT SUM(order_total) AS rest_rev
               FROM   v_order_total
               WHERE  status = 'Delivered'
               GROUP  BY restaurant_id) AS x)
ORDER  BY total_revenue DESC;


-- Q5. Menu items never ordered (NOT EXISTS subquery) — candidates to
-- promote or delist
SELECT r.name AS restaurant, m.name AS dish, m.price
FROM   menu_item m
JOIN   restaurant r ON r.restaurant_id = m.restaurant_id
WHERE  NOT EXISTS (
         SELECT 1
         FROM   order_item oi
         JOIN   food_order fo ON fo.order_id = oi.order_id
         WHERE  oi.menu_item_id = m.menu_item_id
           AND  fo.status <> 'Cancelled')
ORDER  BY r.restaurant_id, m.name;


-- Q6. Delivery agent performance — orders delivered and average
-- delivery time in minutes
SELECT da.delivery_agent_id,
       da.full_name AS agent,
       da.vehicle_type,
       COUNT(fo.order_id) AS delivered_orders,
       ROUND(AVG(EXTRACT(EPOCH FROM (fo.delivered_time - fo.order_time)) / 60), 1) AS avg_delivery_mins
FROM   delivery_agent da
LEFT   JOIN food_order fo
       ON  fo.delivery_agent_id = da.delivery_agent_id
       AND fo.status = 'Delivered'
GROUP  BY da.delivery_agent_id, da.full_name, da.vehicle_type
ORDER  BY delivered_orders DESC, avg_delivery_mins;


-- Q7. Top 5 customers by total spend
SELECT c.customer_id,
       c.full_name AS customer,
       c.location,
       COUNT(t.order_id) AS orders,
       SUM(t.order_total) AS total_spent
FROM   customer c
JOIN   v_order_total t ON t.customer_id = c.customer_id
WHERE  t.status = 'Delivered'
GROUP  BY c.customer_id, c.full_name, c.location
ORDER  BY total_spent DESC
LIMIT  5;


-- Q8. Revenue by cuisine
SELECT r.cuisine,
       COUNT(DISTINCT r.restaurant_id) AS restaurants,
       COUNT(t.order_id) AS delivered_orders,
       COALESCE(SUM(t.order_total), 0) AS revenue
FROM   restaurant r
LEFT   JOIN v_order_total t
       ON t.restaurant_id = r.restaurant_id AND t.status = 'Delivered'
GROUP  BY r.cuisine
ORDER  BY revenue DESC;


-- Q9. Full invoice for order #26 — 7-table JOIN
SELECT fo.order_id,
       to_char(fo.order_time, 'DD-Mon-YYYY HH24:MI') AS ordered_at,
       c.full_name AS customer,
       r.name AS restaurant,
       da.full_name AS delivery_agent,
       m.name AS item,
       oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price AS line_total,
       p.method AS paid_via
FROM   food_order     fo
JOIN   customer       c  ON c.customer_id        = fo.customer_id
JOIN   restaurant     r  ON r.restaurant_id      = fo.restaurant_id
JOIN   delivery_agent da ON da.delivery_agent_id = fo.delivery_agent_id
JOIN   order_item     oi ON oi.order_id          = fo.order_id
JOIN   menu_item      m  ON m.menu_item_id       = oi.menu_item_id
JOIN   payment        p  ON p.order_id           = fo.order_id
WHERE  fo.order_id = 26
ORDER  BY line_total DESC;


-- Q10. Payment method split for delivered orders
SELECT p.method,
       COUNT(*) AS orders,
       SUM(t.order_total) AS amount,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders
FROM   payment p
JOIN   v_order_total t ON t.order_id = p.order_id
WHERE  t.status = 'Delivered'
GROUP  BY p.method
ORDER  BY orders DESC;


CREATE TABLE employees,
