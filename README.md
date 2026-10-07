# QuickBite: Food Delivery Order & Restaurant Management System

This is the DBMS case study #83 for B.Tech CSE (2025–29), Semester III, School of Future Tech, ITM Skills University.

**Submitted by:** Aditya Sunil Chouksey · Roll No. 150096725070 · B.Tech CSE (2025–29)

QuickBite is a food-delivery aggregator. It lists restaurant menus and processes customer orders. The database tracks **revenue per restaurant**, surfaces each restaurant's **most popular dish** for promotion, and makes restaurant browsing **by cuisine and area** fast.

It's built and tested on **PostgreSQL 18**. The SQL works on PostgreSQL 14 and later.

---

## Deliverables

| Deliverable | File |
|---|---|
| **Case Study Report (PDF)** | [`CASE_STUDY_REPORT.pdf`](CASE_STUDY_REPORT.pdf) · [`docs/CASE_STUDY_REPORT.pdf`](docs/CASE_STUDY_REPORT.pdf) |
| **Case Study Report (Markdown)** | [`CASE_STUDY_REPORT.md`](CASE_STUDY_REPORT.md) · [`docs/CASE_STUDY_REPORT.md`](docs/CASE_STUDY_REPORT.md) |
| ER diagram | [`docs/er_diagram.png`](docs/er_diagram.png) · Chen vector: [`er_diagram_chen.svg`](er_diagram_chen.svg) |
| ER diagram, Chen notation (entities, relationships, attributes) | [`docs/er_diagram_chen.png`](docs/er_diagram_chen.png) · editable in draw.io: [`docs/er_diagram_chen.drawio`](docs/er_diagram_chen.drawio) |
| Schema design & normalization (1NF → BCNF) | [`docs/normalization.md`](docs/normalization.md) |
| DDL: tables, PK/FK, NOT NULL, CHECK, UNIQUE, trigger, view | [`sql/01_schema.sql`](sql/01_schema.sql) |
| Indexing: `Restaurant(cuisine, location)` plus FK indexes | [`sql/02_indexes.sql`](sql/02_indexes.sql) |
| DML: sample data | [`sql/03_seed_data.sql`](sql/03_seed_data.sql) |
| Query set: JOINs, subqueries, aggregates | [`sql/04_queries.sql`](sql/04_queries.sql) |
| Index proof on a 200k-restaurant catalogue | [`sql/05_index_demo.sql`](sql/05_index_demo.sql) |
| Referential-integrity tests | [`sql/06_integrity_tests.sql`](sql/06_integrity_tests.sql) |
| Documented query outputs from a real run | [`outputs/`](outputs/) |

### Guides

| Guide | File |
|---|---|
| Line-by-line explanation of every code file | [`docs/CODE_WALKTHROUGH.md`](docs/CODE_WALKTHROUGH.md) |
| 34 practice exercises, basic → advanced, with verified solutions | [`docs/QUERY_PRACTICE.md`](docs/QUERY_PRACTICE.md) |
| Viva preparation: design decisions + likely questions | [`docs/VIVA_NOTES.md`](docs/VIVA_NOTES.md) |
| Uploading this project to GitHub | [`docs/GITHUB_UPLOAD_GUIDE.md`](docs/GITHUB_UPLOAD_GUIDE.md) |
| Presentation script (7 slides, ~6½ min) | [`docs/PRESENTATION_SCRIPT.md`](docs/PRESENTATION_SCRIPT.md) |

## How to run

```bash
./run_all.sh            # creates DB "quickbite", loads everything, writes outputs/
```

To use a different database name:

```bash
DB=mydb ./run_all.sh
```

To run the files by hand:

```bash
createdb quickbite
psql -d quickbite -f sql/01_schema.sql
psql -d quickbite -f sql/02_indexes.sql
psql -d quickbite -f sql/03_seed_data.sql
psql -d quickbite -f sql/04_queries.sql
```

---

## 1. ER Diagram

! refer the image uploaded in github repo under chen_notation.svg (since uploading here is causing issues) 

**Entities:** Restaurant, MenuItem, Customer, FoodOrder, DeliveryAgent, plus two supporting tables:

- **OrderItem**: the order lines. It resolves the M : N between FoodOrder and MenuItem.
- **Payment**: gives a 1 : 1 with FoodOrder.

| Relationship | Type |
|---|---|
| Restaurant → MenuItem | 1 : M |
| Restaurant → FoodOrder | 1 : M |
| Customer → FoodOrder | 1 : M |
| DeliveryAgent → FoodOrder | 1 : M |
| FoodOrder ↔ MenuItem (via OrderItem) | **M : N** |
| FoodOrder → Payment | **1 : 1** |

## 2. Schema & normalization

The original listing repeated each restaurant's cuisine and address on **every menu-item row**. That was a partial dependency on the composite key `(RestaurantID, ItemID)`. Moving those attributes into a separate `restaurant` table, linked by `restaurant_id`, removes it (**2NF**). The design then goes on through 3NF to **BCNF**. The full derivation, FD analysis and anomaly examples are in [`docs/normalization.md`](docs/normalization.md).

| Table | Primary key | Foreign keys | Other constraints |
|---|---|---|---|
| `restaurant` | restaurant_id | — | UNIQUE phone, UNIQUE (name, location), CHECK rating 0–5 |
| `menu_item` | menu_item_id | restaurant_id → restaurant | UNIQUE (restaurant_id, name), CHECK price > 0, CHECK category |
| `customer` | customer_id | — | UNIQUE email, UNIQUE phone |
| `delivery_agent` | delivery_agent_id | — | UNIQUE phone, UNIQUE vehicle_no, CHECK vehicle_type |
| `food_order` | order_id | customer_id, restaurant_id, delivery_agent_id (**all NOT NULL**) | CHECK status, CHECK delivered_time > order_time |
| `order_item` | (order_id, menu_item_id) | order_id → food_order, menu_item_id → menu_item | CHECK quantity 1–50; **trigger:** dish must belong to the order's restaurant |
| `payment` | payment_id | order_id → food_order (**UNIQUE → 1 : 1**) | CHECK method, CHECK status |

`food_order` includes **OrderID, CustomerID, RestaurantID, OrderTime and DeliveryAgentID**, as the brief requires. Order totals are **computed** by the view `v_order_total`, not stored, so they can't drift out of sync.

**Sample data:**

| Table | Rows |
|---|---|
| Restaurants | 11 |
| Menu items | 53 |
| Customers | 15 |
| Delivery agents | 8 |
| Orders | 49 |
| Order lines | 110 |
| Payments | 49 |

- Everything is set in Mumbai and Navi Mumbai during September 2026.
- 45 orders are delivered, 2 are cancelled and 2 are still in progress.
- One restaurant, Malvani Tadka, is newly listed and has no orders yet.

## 3. Key queries & outputs

Full output for all 10 queries is in [`outputs/04_queries_output.txt`](outputs/04_queries_output.txt). In every query, cancelled orders don't count as demand, and revenue counts only delivered orders.

### Q1. Most frequently ordered dish per restaurant

This query JOINs order lines to MenuItem, then uses GROUP BY and COUNT. A correlated ranking subquery in HAVING keeps only each restaurant's highest count.

```sql
SELECT r.name AS restaurant, m.name AS most_popular_dish,
       COUNT(*) AS times_ordered, SUM(oi.quantity) AS units_sold
FROM   order_item oi
JOIN   menu_item  m  ON m.menu_item_id  = oi.menu_item_id
JOIN   food_order fo ON fo.order_id     = oi.order_id
JOIN   restaurant r  ON r.restaurant_id = m.restaurant_id
WHERE  fo.status <> 'Cancelled'
GROUP  BY r.restaurant_id, r.name, m.menu_item_id, m.name
HAVING COUNT(*) = (SELECT MAX(dish_count)
                   FROM (SELECT COUNT(*) AS dish_count
                         FROM   order_item oi2
                         JOIN   menu_item  m2  ON m2.menu_item_id = oi2.menu_item_id
                         JOIN   food_order fo2 ON fo2.order_id    = oi2.order_id
                         WHERE  m2.restaurant_id = r.restaurant_id
                           AND  fo2.status <> 'Cancelled'
                         GROUP  BY oi2.menu_item_id) AS per_dish);
```

```
       restaurant       |   most_popular_dish   | times_ordered | units_sold
------------------------+-----------------------+---------------+------------
 Punjab Da Dhaba        | Butter Chicken        |             6 |          7
 Udupi Sagar            | Masala Dosa           |             4 |          6
 Dragon Wok             | Chilli Paneer         |             3 |          3   <- tie
 Dragon Wok             | Veg Hakka Noodles     |             3 |          4   <- tie
 La Pizzeria Napoli     | Margherita Pizza      |             4 |          5
 Biryani Darbar         | Chicken Dum Biryani   |             5 |          8
 Mumbai Chaat Corner    | Pav Bhaji             |             4 |          6
 Amritsari Kulcha House | Amritsari Kulcha      |             3 |          6
 Madras Filter Cafe     | Ghee Roast Dosa       |             3 |          4
 Wok Express            | Chicken Hakka Noodles |             3 |          4
 The Green Bowl         | Quinoa Buddha Bowl    |             2 |          2
```

The ranking subquery keeps **ties**, as Dragon Wok shows. Q1b gives the same answer using `RANK() OVER (PARTITION BY restaurant_id …)`. It then uses `ROW_NUMBER()` to pick **one** promoted dish per restaurant, breaking ties by units sold (Veg Hakka Noodles wins).

### Q2. Revenue per restaurant: GROUP BY with SUM of order totals

```sql
SELECT r.name AS restaurant, COUNT(t.order_id) AS delivered_orders,
       COALESCE(SUM(t.order_total), 0) AS total_revenue
FROM   restaurant r
LEFT   JOIN v_order_total t ON t.restaurant_id = r.restaurant_id
                           AND t.status = 'Delivered'
GROUP  BY r.restaurant_id, r.name
ORDER  BY total_revenue DESC;
```

```
       restaurant       | delivered_orders | total_revenue | avg_order_value
------------------------+------------------+---------------+-----------------
 Biryani Darbar         |                6 |       5270.00 |          878.33
 La Pizzeria Napoli     |                5 |       4447.00 |          889.40
 Punjab Da Dhaba        |                6 |       4330.00 |          721.67
 Dragon Wok             |                4 |       2490.00 |          622.50
 Amritsari Kulcha House |                4 |       2110.00 |          527.50
 Wok Express            |                4 |       2090.00 |          522.50
 Udupi Sagar            |                5 |       1610.00 |          322.00
 Mumbai Chaat Corner    |                5 |       1550.00 |          310.00
 The Green Bowl         |                2 |       1390.00 |          695.00
 Madras Filter Cafe     |                4 |       1230.00 |          307.50
 Malvani Tadka          |                0 |             0 |               0
```

### Other queries in the set

| # | Query | Technique |
|---|---|---|
| Q3 | Browse by cuisine and area | Uses the composite index |
| Q4 | Restaurants above average revenue | Subquery in HAVING |
| Q5 | Dishes never ordered | NOT EXISTS |
| Q6 | Delivery-agent performance and average delivery minutes | LEFT JOIN, EXTRACT |
| Q7 | Top 5 customers by spend | JOIN, GROUP BY, LIMIT |
| Q8 | Revenue by cuisine | COUNT DISTINCT |
| Q9 | Full invoice | 7-table JOIN |
| Q10 | Payment-method split | Window SUM |

## 4. Advanced concept: indexing

```sql
CREATE INDEX idx_restaurant_cuisine_location ON restaurant (cuisine, location);
```

`05_index_demo.sql` loads **200,000 synthetic restaurants** inside a transaction and runs the app's most common search with and without the index. It then rolls back, so the sample data is untouched.

The search:

```sql
WHERE cuisine = 'North Indian' AND location = 'Kharghar'
```

| | Plan | Rows examined | Execution time |
|---|---|---|---|
| Without index | **Parallel Seq Scan** (full table scan) | ~200,000 (199,176 filtered out) | **13.42 ms** |
| With index | **Bitmap Index Scan** on `idx_restaurant_cuisine_location` | 835 (matches only) | **1.05 ms** (~13× faster) |

**Why the column order is (cuisine, location):**

- By the leftmost-prefix rule, the same index also serves searches on **cuisine alone**.
- A search on **location alone** can't seek directly. PostgreSQL 18's B-tree *skip scan* still uses the index, but it needs one probe per distinct cuisine ("Index Searches: 25" in the plan).

Full plans are in [`outputs/05_index_demo_output.txt`](outputs/05_index_demo_output.txt). Exact timings vary from machine to machine.

PostgreSQL does **not** index foreign keys automatically, so `02_indexes.sql` also indexes every FK column. This speeds up the JOINs and the `ON DELETE RESTRICT` checks.

## 5. Referential integrity

`06_integrity_tests.sql` attempts 9 invalid writes. **All 9 are rejected**, and nothing in the database changes:

| Attempt | Rejected by |
|---|---|
| Order for a customer that doesn't exist | FK `food_order_customer_id_fkey` |
| Order for a restaurant that doesn't exist | FK `food_order_restaurant_id_fkey` |
| Order with no delivery agent | NOT NULL |
| Order line for a dish from **another** restaurant | trigger `order_item_same_restaurant` |
| Deleting a restaurant that still has data | ON DELETE RESTRICT |
| Second payment for the same order | UNIQUE (1 : 1) |
| Negative price, or an unknown order status | CHECK |
| Duplicate customer e-mail | UNIQUE |

## Outcomes vs. the brief

| Outcome required | How it's met |
|---|---|
| Restaurant search stays fast even with a large catalogue | Composite index. Seq Scan becomes Bitmap Index Scan at 200k rows, ~13× faster. |
| Each restaurant's most popular dish surfaced instantly | Q1 and Q1b |
| Revenue per restaurant via GROUP BY SUM on order totals | Q2, using `v_order_total` |
| Every order tied to a valid restaurant, customer and agent | NOT NULL FKs with RESTRICT, a trigger, and the tests in §5 |
