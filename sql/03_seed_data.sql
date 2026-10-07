-- =====================================================================
-- QuickBite — 03_seed_data.sql : DML (realistic sample records)
-- 11 restaurants · 53 menu items · 15 customers · 8 delivery agents
-- 49 orders · 110 order lines · 49 payments      (September 2026)
-- =====================================================================

BEGIN;

-- ---------------------------------------------------------------------
-- RESTAURANTS  (note R1 & R7 share cuisine + location, R2/R6/R9/R11 all
-- in Vashi — useful for testing the (cuisine, location) search)
-- ---------------------------------------------------------------------
INSERT INTO restaurant (restaurant_id, name, cuisine, location, address, phone, rating) VALUES
 (1,  'Punjab Da Dhaba',        'North Indian', 'Kharghar',    'Shop 4, Sector 7, Kharghar, Navi Mumbai 410210',        '02227741001', 4.4),
 (2,  'Udupi Sagar',            'South Indian', 'Vashi',       'Plot 12, Sector 17, Vashi, Navi Mumbai 400703',          '02227891002', 4.2),
 (3,  'Dragon Wok',             'Chinese',      'Powai',       'Galleria Mall, Hiranandani Gardens, Powai 400076',       '02225701003', 4.0),
 (4,  'La Pizzeria Napoli',     'Italian',      'Bandra West', '22 Hill Road, Bandra West, Mumbai 400050',               '02226401004', 4.6),
 (5,  'Biryani Darbar',         'Mughlai',      'Andheri West','Shop 9, Lokhandwala Market, Andheri West 400053',        '02226311005', 4.3),
 (6,  'Mumbai Chaat Corner',    'Street Food',  'Vashi',       'Stall 3, Sector 9A, Vashi, Navi Mumbai 400703',          '02227821006', 4.1),
 (7,  'Amritsari Kulcha House', 'North Indian', 'Kharghar',    'Shop 18, Utsav Chowk, Sector 20, Kharghar 410210',       '02227741007', 4.5),
 (8,  'Madras Filter Cafe',     'South Indian', 'Thane West',  'Ground Floor, Viviana Mall, Thane West 400606',          '02225881008', 4.3),
 (9,  'Wok Express',            'Chinese',      'Vashi',       'Inorbit Mall Food Court, Sector 30A, Vashi 400703',      '02227811009', 3.9),
 (10, 'The Green Bowl',         'Continental',  'Powai',       'Shop 2, Supreme Business Park, Powai 400076',            '02225701010', 4.4),
 (11, 'Malvani Tadka',          'Malvani',      'Vashi',       'Shop 6, Sector 15, Vashi, Navi Mumbai 400703',           '02227891011', 4.0);

-- ---------------------------------------------------------------------
-- MENU ITEMS  (restaurant r owns items 5r-4 .. 5r; R11 owns 51-53)
-- ---------------------------------------------------------------------
INSERT INTO menu_item (menu_item_id, restaurant_id, name, category, price, is_veg) VALUES
 -- 1 Punjab Da Dhaba
 (1,  1, 'Butter Chicken',          'Main Course', 340, FALSE),
 (2,  1, 'Dal Makhani',             'Main Course', 260, TRUE),
 (3,  1, 'Paneer Tikka',            'Starter',     290, TRUE),
 (4,  1, 'Butter Naan',             'Bread',        60, TRUE),
 (5,  1, 'Sweet Lassi',             'Beverage',     90, TRUE),
 -- 2 Udupi Sagar
 (6,  2, 'Masala Dosa',             'Main Course', 120, TRUE),
 (7,  2, 'Idli Sambar',             'Snack',        80, TRUE),
 (8,  2, 'Medu Vada',               'Snack',        90, TRUE),
 (9,  2, 'Rava Uttapam',            'Main Course', 130, TRUE),
 (10, 2, 'Filter Coffee',           'Beverage',     50, TRUE),
 -- 3 Dragon Wok
 (11, 3, 'Veg Hakka Noodles',       'Main Course', 210, TRUE),
 (12, 3, 'Chicken Manchurian',      'Starter',     260, FALSE),
 (13, 3, 'Schezwan Fried Rice',     'Rice',        230, TRUE),
 (14, 3, 'Chilli Paneer',           'Starter',     250, TRUE),
 (15, 3, 'Veg Spring Rolls',        'Starter',     180, TRUE),
 -- 4 La Pizzeria Napoli
 (16, 4, 'Margherita Pizza',        'Main Course', 399, TRUE),
 (17, 4, 'Pepperoni Pizza',         'Main Course', 499, FALSE),
 (18, 4, 'Penne Arrabbiata',        'Main Course', 349, TRUE),
 (19, 4, 'Garlic Bread',            'Snack',       179, TRUE),
 (20, 4, 'Tiramisu',                'Dessert',     249, TRUE),
 -- 5 Biryani Darbar
 (21, 5, 'Chicken Dum Biryani',     'Rice',        320, FALSE),
 (22, 5, 'Mutton Biryani',          'Rice',        420, FALSE),
 (23, 5, 'Veg Biryani',             'Rice',        240, TRUE),
 (24, 5, 'Chicken Seekh Kebab',     'Starter',     280, FALSE),
 (25, 5, 'Phirni',                  'Dessert',     110, TRUE),
 -- 6 Mumbai Chaat Corner
 (26, 6, 'Pani Puri',               'Snack',        60, TRUE),
 (27, 6, 'Pav Bhaji',               'Main Course', 140, TRUE),
 (28, 6, 'Vada Pav',                'Snack',        30, TRUE),
 (29, 6, 'Sev Puri',                'Snack',        70, TRUE),
 (30, 6, 'Masala Chaas',            'Beverage',     40, TRUE),
 -- 7 Amritsari Kulcha House
 (31, 7, 'Amritsari Kulcha',        'Bread',       150, TRUE),
 (32, 7, 'Pindi Chole',             'Main Course', 180, TRUE),
 (33, 7, 'Paneer Butter Masala',    'Main Course', 280, TRUE),
 (34, 7, 'Aloo Paratha',            'Bread',       120, TRUE),
 (35, 7, 'Mango Lassi',             'Beverage',    110, TRUE),
 -- 8 Madras Filter Cafe
 (36, 8, 'Ghee Roast Dosa',         'Main Course', 160, TRUE),
 (37, 8, 'Mini Ghee Idli',          'Snack',       110, TRUE),
 (38, 8, 'Ven Pongal',              'Main Course', 130, TRUE),
 (39, 8, 'Curd Rice',               'Rice',        120, TRUE),
 (40, 8, 'Madras Filter Coffee',    'Beverage',     60, TRUE),
 -- 9 Wok Express
 (41, 9, 'Chicken Hakka Noodles',   'Main Course', 240, FALSE),
 (42, 9, 'Veg Manchurian',          'Starter',     200, TRUE),
 (43, 9, 'Chicken Fried Rice',      'Rice',        250, FALSE),
 (44, 9, 'Hot and Sour Soup',       'Starter',     150, TRUE),
 (45, 9, 'Honey Chilli Potato',     'Starter',     190, TRUE),
 -- 10 The Green Bowl
 (46, 10, 'Classic Caesar Salad',   'Starter',     320, TRUE),
 (47, 10, 'Grilled Chicken Steak',  'Main Course', 450, FALSE),
 (48, 10, 'Quinoa Buddha Bowl',     'Main Course', 380, TRUE),
 (49, 10, 'Cream of Mushroom Soup', 'Starter',     220, TRUE),
 (50, 10, 'Cold Coffee',            'Beverage',    180, TRUE),
 -- 11 Malvani Tadka (newly listed, no orders yet)
 (51, 11, 'Surmai Fry',             'Starter',     380, FALSE),
 (52, 11, 'Prawn Malvani Curry',    'Main Course', 420, FALSE),
 (53, 11, 'Sol Kadhi',              'Beverage',     80, TRUE);

-- ---------------------------------------------------------------------
-- CUSTOMERS
-- ---------------------------------------------------------------------
INSERT INTO customer (customer_id, full_name, email, phone, address, location, joined_on) VALUES
 (1,  'Aarav Sharma',     'aarav.sharma@example.com',     '9820011001', 'B-204, Sai Heights, Sector 12, Kharghar',     'Kharghar',    '2025-11-14'),
 (2,  'Priya Nair',       'priya.nair@example.com',       '9820011002', 'Flat 7, Palm Beach Residency, Sector 17, Vashi','Vashi',     '2025-12-02'),
 (3,  'Rohan Mehta',      'rohan.mehta@example.com',      '9820011003', 'A-1102, Hiranandani Gardens, Powai',          'Powai',       '2026-01-09'),
 (4,  'Sneha Kulkarni',   'sneha.kulkarni@example.com',   '9820011004', '12, Shanti Nagar, Sector 9, Vashi',           'Vashi',       '2026-01-21'),
 (5,  'Karan Malhotra',   'karan.malhotra@example.com',   '9820011005', '301, Lokhandwala Complex, Andheri West',      'Andheri West','2026-02-03'),
 (6,  'Ananya Iyer',      'ananya.iyer@example.com',      '9820011006', '15, Pali Hill Road, Bandra West',             'Bandra West', '2026-02-18'),
 (7,  'Vikram Singh',     'vikram.singh@example.com',     '9820011007', 'C-45, Raheja Vihar, Powai',                   'Powai',       '2026-03-05'),
 (8,  'Neha Gupta',       'neha.gupta@example.com',       '9820011008', '9, Kharghar Hills CHS, Sector 35, Kharghar',  'Kharghar',    '2026-03-22'),
 (9,  'Arjun Reddy',      'arjun.reddy@example.com',      '9820011009', '502, Vasant Vihar, Thane West',               'Thane West',  '2026-04-10'),
 (10, 'Isha Desai',       'isha.desai@example.com',       '9820011010', 'Flat 3, Sector 28, Vashi',                    'Vashi',       '2026-04-27'),
 (11, 'Siddharth Joshi',  'siddharth.joshi@example.com',  '9820011011', '18, Hiranandani Estate, Thane West',          'Thane West',  '2026-05-15'),
 (12, 'Meera Pillai',     'meera.pillai@example.com',     '9820011012', 'D-9, Sector 20, Kharghar',                    'Kharghar',    '2026-06-01'),
 (13, 'Aditya Rao',       'aditya.rao@example.com',       '9820011013', '706, Oberoi Springs, Andheri West',           'Andheri West','2026-06-19'),
 (14, 'Tanvi Kapoor',     'tanvi.kapoor@example.com',     '9820011014', '11, Carter Road, Bandra West',                'Bandra West', '2026-07-08'),
 (15, 'Rahul Verma',      'rahul.verma@example.com',      '9820011015', '404, Lake Homes, Powai',                      'Powai',       '2026-08-12');

-- ---------------------------------------------------------------------
-- DELIVERY AGENTS
-- ---------------------------------------------------------------------
INSERT INTO delivery_agent (delivery_agent_id, full_name, phone, vehicle_type, vehicle_no, home_zone) VALUES
 (1, 'Ramesh Yadav',   '9004400101', 'Motorbike',  'MH46AB1021', 'Kharghar'),
 (2, 'Suresh Patil',   '9004400102', 'Scooter',    'MH43CD2210', 'Vashi'),
 (3, 'Imran Shaikh',   '9004400103', 'EV Scooter', 'MH03EV3345', 'Powai'),
 (4, 'Deepak Chauhan', '9004400104', 'Motorbike',  'MH02GH4410', 'Andheri West'),
 (5, 'Joseph D''Souza','9004400105', 'Scooter',    'MH02JK5521', 'Bandra West'),
 (6, 'Ganesh More',    '9004400106', 'Motorbike',  'MH04LM6632', 'Thane West'),
 (7, 'Anil Kamble',    '9004400107', 'Bicycle',    NULL,         'Vashi'),
 (8, 'Manoj Tiwari',   '9004400108', 'EV Scooter', 'MH46EV7743', 'Kharghar');

-- ---------------------------------------------------------------------
-- FOOD ORDERS
-- delivery_address is copied from the customer's current address at
-- order time (a historical snapshot — the customer may move later).
-- delivered_time = order_time + delivery minutes (NULL if not delivered)
-- ---------------------------------------------------------------------
INSERT INTO food_order (order_id, customer_id, restaurant_id, delivery_agent_id,
                        order_time, delivery_address, status, delivered_time)
SELECT v.oid, v.cid, v.rid, v.aid,
       v.t::TIMESTAMP,
       c.address,
       v.st,
       CASE WHEN v.mins IS NULL THEN NULL
            ELSE v.t::TIMESTAMP + make_interval(mins => v.mins) END
FROM (VALUES
 -- oid cust rest agent  order_time             status              minutes
 ( 1,  1,  1, 1, '2026-09-02 13:05', 'Delivered',        34),
 ( 2,  3,  1, 8, '2026-09-03 20:40', 'Delivered',        41),
 ( 3,  5,  1, 1, '2026-09-06 12:50', 'Delivered',        29),
 ( 4,  8,  1, 1, '2026-09-10 21:15', 'Delivered',        38),
 ( 5, 12,  1, 8, '2026-09-15 19:30', 'Delivered',        45),
 ( 6,  1,  1, 1, '2026-09-22 13:20', 'Delivered',        31),
 ( 7,  2,  2, 2, '2026-09-01 08:45', 'Delivered',        26),
 ( 8,  4,  2, 7, '2026-09-04 09:10', 'Delivered',        28),
 ( 9,  6,  2, 2, '2026-09-09 18:05', 'Delivered',        33),
 (10,  2,  2, 7, '2026-09-17 08:30', 'Delivered',        25),
 (11, 10,  2, 2, '2026-09-24 19:50', 'Delivered',        36),
 (12,  7,  3, 3, '2026-09-02 20:15', 'Delivered',        39),
 (13,  9,  3, 3, '2026-09-07 21:30', 'Delivered',        42),
 (14, 11,  3, 3, '2026-09-12 20:00', 'Delivered',        35),
 (15,  7,  3, 3, '2026-09-19 13:45', 'Delivered',        30),
 (16, 13,  3, 3, '2026-09-25 22:10', 'Cancelled',        NULL),
 (17, 14,  4, 5, '2026-09-03 19:25', 'Delivered',        44),
 (18,  3,  4, 5, '2026-09-08 20:50', 'Delivered',        40),
 (19, 15,  4, 5, '2026-09-14 21:05', 'Delivered',        37),
 (20,  6,  4, 5, '2026-09-20 19:40', 'Delivered',        43),
 (21, 14,  4, 5, '2026-09-26 20:30', 'Delivered',        39),
 (22,  5,  5, 4, '2026-09-01 13:30', 'Delivered',        32),
 (23,  8,  5, 4, '2026-09-05 20:10', 'Delivered',        36),
 (24,  1,  5, 4, '2026-09-11 21:00', 'Delivered',        47),
 (25, 11,  5, 4, '2026-09-16 14:15', 'Delivered',        30),
 (26, 13,  5, 4, '2026-09-21 20:45', 'Delivered',        41),
 (27,  4,  5, 4, '2026-09-27 13:10', 'Delivered',        35),
 (28,  2,  6, 2, '2026-09-02 17:30', 'Delivered',        22),
 (29, 10,  6, 7, '2026-09-08 18:20', 'Delivered',        24),
 (30,  6,  6, 2, '2026-09-13 17:55', 'Delivered',        27),
 (31, 12,  6, 7, '2026-09-18 18:40', 'Delivered',        29),
 (32, 15,  6, 2, '2026-09-23 19:05', 'Delivered',        31),
 (33,  1,  7, 1, '2026-09-04 13:35', 'Delivered',        33),
 (34,  5,  7, 8, '2026-09-10 20:25', 'Delivered',        37),
 (35,  9,  7, 8, '2026-09-16 09:40', 'Delivered',        28),
 (36,  3,  7, 1, '2026-09-24 21:10', 'Delivered',        40),
 (37,  7,  8, 6, '2026-09-03 08:20', 'Delivered',        27),
 (38, 11,  8, 6, '2026-09-11 09:05', 'Delivered',        30),
 (39,  4,  8, 6, '2026-09-18 13:00', 'Delivered',        34),
 (40, 13,  8, 6, '2026-09-25 08:50', 'Delivered',        29),
 (41,  8,  9, 7, '2026-09-06 20:35', 'Delivered',        31),
 (42, 12,  9, 2, '2026-09-13 21:20', 'Delivered',        38),
 (43, 14,  9, 7, '2026-09-19 20:05', 'Delivered',        35),
 (44,  9,  9, 2, '2026-09-27 21:45', 'Delivered',        33),
 (45, 10, 10, 3, '2026-09-07 13:15', 'Delivered',        38),
 (46, 15, 10, 3, '2026-09-17 20:55', 'Delivered',        42),
 (47,  6, 10, 3, '2026-09-23 12:30', 'Cancelled',        NULL),
 (48,  3,  1, 1, '2026-09-29 10:40', 'Out for Delivery', NULL),
 (49,  2,  6, 7, '2026-09-29 10:55', 'Preparing',        NULL)
) AS v(oid, cid, rid, aid, t, st, mins)
JOIN customer c ON c.customer_id = v.cid;

-- ---------------------------------------------------------------------
-- ORDER LINES  (unit_price captured from the menu at order time)
-- ---------------------------------------------------------------------
INSERT INTO order_item (order_id, menu_item_id, quantity, unit_price)
SELECT v.oid, v.mid, v.qty, m.price
FROM (VALUES
 -- Punjab Da Dhaba
 ( 1, 1,1),( 1, 4,4),( 1, 5,2),
 ( 2, 1,2),( 2, 2,1),( 2, 4,3),
 ( 3, 1,1),( 3, 3,1),
 ( 4, 2,1),( 4, 4,2),
 ( 5, 1,1),( 5, 2,1),( 5, 4,2),( 5, 5,1),
 ( 6, 1,1),( 6, 3,1),
 (48, 1,1),(48, 4,2),
 -- Udupi Sagar
 ( 7, 6,2),( 7,10,2),
 ( 8, 6,1),( 8, 7,1),( 8, 8,1),
 ( 9, 7,2),( 9,10,1),
 (10, 6,1),(10, 9,1),(10,10,2),
 (11, 6,2),(11, 8,2),
 -- Dragon Wok  (Veg Hakka Noodles and Chilli Paneer tie on purpose)
 (12,11,1),(12,14,1),
 (13,11,2),(13,12,1),
 (14,14,1),(14,13,1),(14,15,1),
 (15,11,1),(15,14,1),(15,13,1),
 (16,12,1),(16,15,1),
 -- La Pizzeria Napoli
 (17,16,1),(17,19,1),
 (18,16,2),(18,20,1),
 (19,17,1),(19,19,1),
 (20,16,1),(20,18,1),(20,20,2),
 (21,16,1),(21,17,1),
 -- Biryani Darbar
 (22,21,2),(22,25,2),
 (23,21,1),(23,24,1),
 (24,22,1),(24,21,1),
 (25,23,2),
 (26,21,3),(26,24,2),(26,25,3),
 (27,21,1),(27,22,1),
 -- Mumbai Chaat Corner
 (28,27,2),(28,28,4),
 (29,26,2),(29,27,1),
 (30,27,1),(30,29,1),(30,30,2),
 (31,28,6),(31,30,2),
 (32,26,1),(32,27,2),
 (49,26,1),(49,28,2),
 -- Amritsari Kulcha House
 (33,31,2),(33,32,1),(33,35,1),
 (34,31,1),(34,33,1),
 (35,34,2),(35,35,2),
 (36,31,3),(36,32,1),
 -- Madras Filter Cafe
 (37,36,1),(37,40,1),
 (38,36,2),(38,37,1),
 (39,38,1),(39,39,1),(39,40,1),
 (40,36,1),(40,37,1),
 -- Wok Express
 (41,41,1),(41,42,1),
 (42,41,2),(42,44,2),
 (43,43,1),(43,45,1),
 (44,41,1),(44,45,1),
 -- The Green Bowl
 (45,48,1),(45,50,1),
 (46,47,1),(46,48,1),
 (47,46,1),(47,49,1)
) AS v(oid, mid, qty)
JOIN menu_item m ON m.menu_item_id = v.mid;

-- ---------------------------------------------------------------------
-- PAYMENTS  (exactly one per order — 1:1)
-- ---------------------------------------------------------------------
INSERT INTO payment (order_id, method, status, transaction_ref, paid_at)
SELECT fo.order_id,
       v.method,
       CASE
         WHEN fo.status = 'Cancelled'                  THEN 'Refunded'
         WHEN v.method = 'Cash' AND fo.status <> 'Delivered' THEN 'Pending'
         ELSE 'Paid'
       END,
       CASE WHEN v.method = 'Cash' THEN NULL
            ELSE 'QB' || to_char(fo.order_time, 'YYYYMMDD') || lpad(fo.order_id::TEXT, 5, '0')
       END,
       CASE
         WHEN v.method = 'Cash' THEN fo.delivered_time          -- paid on delivery
         ELSE fo.order_time + INTERVAL '1 minute'               -- prepaid
       END
FROM (VALUES
 ( 1,'UPI'),( 2,'Card'),( 3,'Cash'),( 4,'UPI'),( 5,'Wallet'),( 6,'UPI'),
 ( 7,'UPI'),( 8,'Cash'),( 9,'UPI'),(10,'Card'),(11,'UPI'),
 (12,'Card'),(13,'UPI'),(14,'Wallet'),(15,'UPI'),(16,'UPI'),
 (17,'Card'),(18,'UPI'),(19,'Card'),(20,'UPI'),(21,'Wallet'),
 (22,'UPI'),(23,'Cash'),(24,'UPI'),(25,'Card'),(26,'UPI'),(27,'Cash'),
 (28,'Cash'),(29,'UPI'),(30,'UPI'),(31,'Wallet'),(32,'UPI'),
 (33,'UPI'),(34,'Card'),(35,'Cash'),(36,'UPI'),
 (37,'UPI'),(38,'Card'),(39,'Cash'),(40,'UPI'),
 (41,'UPI'),(42,'Card'),(43,'UPI'),(44,'Wallet'),
 (45,'Card'),(46,'UPI'),(47,'Card'),
 (48,'UPI'),(49,'Cash')
) AS v(oid, method)
JOIN food_order fo ON fo.order_id = v.oid;

-- ---------------------------------------------------------------------
-- Explicit IDs were supplied above, so move each identity sequence past
-- the highest ID; otherwise the next app-generated insert would collide.
-- ---------------------------------------------------------------------
SELECT setval(pg_get_serial_sequence('restaurant',     'restaurant_id'),     (SELECT MAX(restaurant_id)     FROM restaurant));
SELECT setval(pg_get_serial_sequence('menu_item',      'menu_item_id'),      (SELECT MAX(menu_item_id)      FROM menu_item));
SELECT setval(pg_get_serial_sequence('customer',       'customer_id'),       (SELECT MAX(customer_id)       FROM customer));
SELECT setval(pg_get_serial_sequence('delivery_agent', 'delivery_agent_id'), (SELECT MAX(delivery_agent_id) FROM delivery_agent));
SELECT setval(pg_get_serial_sequence('food_order',     'order_id'),          (SELECT MAX(order_id)          FROM food_order));
SELECT setval(pg_get_serial_sequence('payment',        'payment_id'),        (SELECT MAX(payment_id)        FROM payment));

COMMIT;
