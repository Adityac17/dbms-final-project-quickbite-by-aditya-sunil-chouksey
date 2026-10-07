# School of Future Tech, ITM Skills University
## Case Study Report on
# QuickBite: Food Delivery Order & Restaurant Management System
### DBMS Case Study #83 · B.Tech Computer Science Engineering (2025–29)

**Author:** Aditya Sunil Chouksey  
**Roll Number:** 150096725070  
**Program:** B.Tech Computer Science & Engineering (Semester III)  
**Institution:** School of Future Tech, ITM Skills University  
**Date:** October 2026  

---

## Index

1. **Introduction to the Case Study**
2. **Problem Statement / Case Background (Abstract)**
   - 2.1 Background
   - 2.2 Abstract
3. **Problem Statement / Case Study Design**
   - 3.1 Stage 1: Conceptual Design & Entity-Relationship (ER) Architecture
   - 3.2 Stage 2: Logical Schema Design & Normalization (1NF → BCNF)
   - 3.3 Stage 3: Physical Database Schema & Constraint Engineering
   - 3.4 Stage 4: Procedural Enforcement via Triggers
   - 3.5 Stage 5: Dynamic Views for Financial Consistency
   - 3.6 Stage 6: High-Performance Composite Indexing Strategy
   - 3.7 Stage 7: Analytical Business Intelligence Pipeline
   - 3.8 Stage 8: Scalability Benchmarking & Integrity Verification
4. **Methods & Algorithms Technology Applied in the Problem Statement / Case Study**
   - 4.1 Relational Normalization & Functional Dependency Decomposition
   - 4.2 Indexing Algorithms & Search Tree Traversal
   - 4.3 Analytical SQL Querying, Correlated Subqueries & Window Ranking
   - 4.4 Declarative & Procedural Integrity Enforcement
   - 4.5 Technology Stack Used for the Case
5. **Problem Statement / Case Study Implementation Details and Snapshots**
   - 5.1 Project Directory & Module Architecture
   - 5.2 Snapshot 1: Entity-Relationship Diagram (Crow's Foot & Chen Notation)
   - 5.3 Snapshot 2: Database Schema & Baseline Row Counts
   - 5.4 Snapshot 3: Procedural Trigger Implementation (`order_item_same_restaurant`)
   - 5.5 Snapshot 4: Query 1 — Most Frequently Ordered Dish per Restaurant (With Ties)
   - 5.6 Snapshot 5: Query 1b — Single Promo Recommendation with Tie-Breaking
   - 5.7 Snapshot 6: Query 2 — Total Revenue Generated per Restaurant
   - 5.8 Snapshot 7: Query 3 — High-Speed Search by Cuisine & Locality
   - 5.9 Snapshot 8: Query 6 — Delivery Agent Performance & Average Transit Time
   - 5.10 Snapshot 9: Query 9 — Itemized Order Invoice via 7-Table JOIN
   - 5.11 Snapshot 10: Advanced Concept — Index Scalability Benchmark on 200,000 Rows
   - 5.12 Snapshot 11: Referential Integrity Suite Execution (9/9 Rejected)
6. **Problem Statement / Case Study Results and Conclusion**
   - 6.1 Key Findings
   - 6.2 Comparison of Query Performance (Indexed vs. Unindexed)
   - 6.3 Conclusion & Future Enhancements
7. **References**

---

## 1. Introduction to the Case Study

Digital food delivery aggregators (such as Zomato, Swiggy, and Uber Eats) have fundamentally transformed modern urban food commerce. These platforms serve as hyper-local two-sided marketplaces orchestrating real-time interactions between four primary stakeholders: consumers browsing menus and placing orders, partner restaurants updating dish catalogues and managing fulfillment, freelance delivery riders navigating urban transit zones, and the platform operators managing financial settlements and promotions.

Underneath these high-velocity consumer applications lies an intricate data engineering challenge. The underlying database must simultaneously guarantee:
1. **Uncompromised Financial & Inventory Integrity:** Preventing phantom totals, duplicate billing, and orphaned records during order spikes.
2. **Strict Multi-Tenant Relational Consistency:** Ensuring order items strictly correspond to the merchant fulfilling the order, avoiding cross-restaurant dispatch errors.
3. **Ultra-Low-Latency Search & Retrieval:** Enabling instant filtering across hundreds of thousands of restaurants by multi-dimensional facets (such as cuisine type and geographical locality).
4. **Actionable Business Intelligence:** Surfacing real-time operational insights, such as top-selling promotional dishes, accurate net revenue per partner, customer lifetime value, and delivery agent turnaround times.

This case study documents the design, architecture, implementation, and empirical evaluation of **QuickBite**, a specialized relational database management system designed to serve as the transaction engine for an urban food-delivery aggregator. Developed and benchmarked on **PostgreSQL 18**, QuickBite demonstrates how formal database theory—spanning conceptual ER modeling, Boyce-Codd Normalization (BCNF), declarative constraint systems, procedural event triggers, composite B-Tree indexing, and complex analytical SQL—is applied to solve real-world industry challenges.

---

## 2. Problem Statement / Case Background (Abstract)

### 2.1 Background
Nascent digital delivery startups often begin by tracking listings, menus, and orders within spreadsheet sheets or flat, denormalized database tables. In such naive schemas, every dish row redundantly duplicates restaurant attributes (such as name, cuisine category, locality, street address, and phone number). Similarly, every order line duplicates customer and delivery personnel contact information.

This structural denormalization introduces critical database anomalies:
* **Update Anomalies:** If a restaurant changes its contact telephone number or relocates within a sector, every individual menu item row must be updated. Missing a single row causes internal database contradictions and failed delivery routing.
* **Insertion Anomalies:** A newly partnered restaurant (such as an onboarding kitchen like *Malvani Tadka*) cannot be inserted into the system until it creates its first menu item if the table relies on a composite key of `(RestaurantID, ItemID)`.
* **Deletion Anomalies:** If a specialty restaurant temporarily removes all seasonal dishes from its menu, deleting those dish rows inadvertently deletes the restaurant's operational registration, contact details, and historical footprint.
* **Referential Inconsistencies:** Without foreign key constraints and procedural checks, customers can place orders containing dishes belonging to multiple disparate restaurants, creating an impossible physical dispatch assignment.
* **Scalability Bottlenecks:** As restaurant directories expand to hundreds of thousands of listings, naive sequential scans (`Seq Scan`) cause user catalog browsing to degrade severely, resulting in unacceptable search latencies.

### 2.2 Abstract
This case study presents the end-to-end design, implementation, and optimization of **QuickBite**, a robust relational database system built on PostgreSQL 18. QuickBite deconstructs the flat delivery model into **7 strictly normalized entities** meeting **Boyce-Codd Normal Form (BCNF)**: `restaurant`, `menu_item`, `customer`, `delivery_agent`, `food_order`, `order_item`, and `payment`. This architecture eliminates all partial and transitive functional dependencies while preserving lossless join capability.

To enforce relational integrity beyond standard declarative foreign keys, QuickBite integrates a PL/pgSQL procedural trigger (`trg_order_item_same_restaurant`) that blocks orders from incorporating dishes from foreign kitchens without requiring 2NF-violating duplicate columns. Financial consistency is maintained through a dynamic view (`v_order_total`), eliminating the risks of precalculated stored order totals drifting out of sync with itemized lines.

For search optimization, a composite B-Tree index on `restaurant(cuisine, location)` is designed according to the leftmost-prefix rule. In empirical scalability benchmarking against a **200,000-restaurant catalogue**, the composite index transforms full sequential table scans into selective Bitmap Index Scans, reducing execution time from **13.42 ms to 1.05 ms** (an approximate **13× performance improvement**). Furthermore, a comprehensive analytical suite of 10 SQL queries demonstrates multi-table relational joins, correlated ranking subqueries, window partition tie-breaking, and aggregations. The system is validated via a 9-vector negative testing suite, achieving a 100% rejection rate for invalid data mutations.

---

## 3. Problem Statement / Case Study Design

The QuickBite database architecture was engineered following a structured 8-stage relational design lifecycle:

```
┌────────────────────────────────────────────────────────────────────────┐
│               QUICKBITE SYSTEM DESIGN & EXECUTION PIPELINE             │
└────────────────────────────────────────────────────────────────────────┘
  [Stage 1: Conceptual Modeling]
       └─► Entity-Relationship Diagramming (7 Entities, Crow's Foot & Chen)
  [Stage 2: Logical Schema & Normalization]
       └─► Functional Dependency Analysis (1NF → 2NF → 3NF → BCNF)
  [Stage 3: Physical Schema & Constraints]
       └─► PostgreSQL DDL, Identity PKs, Restrict/Cascade FKs, Domain CHECKs
  [Stage 4: Procedural Business Logic]
       └─► PL/pgSQL Event Trigger (Cross-Restaurant Validation)
  [Stage 5: Dynamic Financial View]
       └─► Non-Materialized View (`v_order_total`) for Single Source of Truth
  [Stage 6: Index Architecture]
       └─► Composite B-Tree Index on (Cuisine, Location) + FK Indexes
  [Stage 7: Analytical Query Suite]
       └─► 10 Business Intelligence Queries (Window Functions, Aggregations)
  [Stage 8: Empirical Validation & Testing]
       └─► 200,000-Row Index Benchmark + 9 Negative Integrity Test Vectors
```

### 3.1 Stage 1: Conceptual Design & Entity-Relationship (ER) Architecture
The system models the operational ecosystem through seven distinct entities:
1. **`Restaurant`**: Stores core merchant registration, culinary category, geographical locality, physical street address, contact phone, and consumer rating.
2. **`MenuItem`**: Captures individual catalog dishes, course category (Starter, Main Course, Dessert, etc.), base selling price, dietary flag (`is_veg`), and live inventory availability.
3. **`Customer`**: Holds registered user profile, verified email, phone number, default locality, and platform registration date.
4. **`DeliveryAgent`**: Details logistics personnel, verified contact phone, vehicle category (Bicycle, Scooter, Motorbike, EV Scooter), registration license plate, and assigned home operational zone.
5. **`FoodOrder`**: Represents order transactions, tracking order timestamp, delivery address snapshot, fulfillment status, and delivery completion timestamp.
6. **`OrderItem`**: Resolves the many-to-many ($M:N$) cardinality between `FoodOrder` and `MenuItem`, recording ordered quantities and the frozen historical unit price charged at the moment of checkout.
7. **`Payment`**: Establishes a 1:1 relationship with `FoodOrder`, recording transaction method (UPI, Card, Cash, Wallet), settlement status, gateway transaction references, and completion timestamps.

#### Entity Cardinality Matrix
| Parent Entity | Child Entity | Cardinality | Implementation Mechanism |
|---|---|---|---|
| `Restaurant` | `MenuItem` | $1 : M$ | `menu_item.restaurant_id` FK (NOT NULL, RESTRICT) |
| `Restaurant` | `FoodOrder` | $1 : M$ | `food_order.restaurant_id` FK (NOT NULL, RESTRICT) |
| `Customer` | `FoodOrder` | $1 : M$ | `food_order.customer_id` FK (NOT NULL, RESTRICT) |
| `DeliveryAgent` | `FoodOrder` | $1 : M$ | `food_order.delivery_agent_id` FK (NOT NULL, RESTRICT) |
| `FoodOrder` | `MenuItem` | $M : N$ | Junction table `order_item` with composite PK `(order_id, menu_item_id)` |
| `FoodOrder` | `Payment` | $1 : 1$ | `payment.order_id` FK + UNIQUE constraint |

### 3.2 Stage 2: Logical Schema Design & Normalization (1NF → BCNF)

#### 1. Unnormalized Starting Point
Initial unnormalized schemas store menus and orders in flat tabular records:
* `Menu_Flat = (RestaurantID, RestaurantName, Cuisine, Location, Address, ItemID, ItemName, Price)`
* Candidate Key: `(RestaurantID, ItemID)`
* Functional Dependencies:
  * $FD_1: \text{RestaurantID} \to \text{RestaurantName, Cuisine, Location, Address}$
  * $FD_2: (\text{RestaurantID, ItemID}) \to \text{ItemName, Price}$

#### 2. First Normal Form (1NF)
All attributes contain strictly atomic, non-divisible values. No repeating multi-valued arrays exist in columns.

#### 3. Second Normal Form (2NF)
In the unnormalized menu relation, $\text{RestaurantID} \to \text{Cuisine, Location, Address}$ represents a **partial functional dependency**, because attributes depend only on a subset of the composite candidate key `(RestaurantID, ItemID)`.
* **2NF Decomposition:** Decompose into `restaurant` and `menu_item`. Restaurant metadata is isolated into `restaurant` keyed by `restaurant_id`, and `menu_item` references it via foreign key `restaurant_id`.
* Similarly, `food_order` is isolated from customer, rider, and restaurant metadata, while `order_item` retains only attributes functionally dependent on the entire composite key `(order_id, menu_item_id)`.

#### 4. Third Normal Form (3NF)
A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on any candidate key ($X \to Y$ and $Y \to Z$).
* **Order Total Elimination:** Total bill amounts are derived values ($\sum (\text{quantity} \times \text{unit\_price})$). Storing total bill in `food_order` creates a transitive dependency (`order_id` $\to$ line items $\to$ `order_total`), creating data synchronization anomalies. QuickBite removes stored order totals and calculates them dynamically via view `v_order_total`.
* **Deliberate Historical Snapshotting:**
  * `order_item.unit_price`: Records the exact price at checkout time. It does not represent a redundant copy of `menu_item.price` because menu prices fluctuate over time, whereas historical financial ledgers must remain immutably fixed.
  * `food_order.delivery_address`: Captures the destination at order time, remaining immune to subsequent customer profile address edits.

#### 5. Boyce-Codd Normal Form (BCNF)
A relation is in BCNF if for every non-trivial functional dependency $X \to Y$, $X$ is a superkey.
* `restaurant`: Determinants are `restaurant_id`, `phone`, and `(name, location)`. All are superkeys (enforced by PK and UNIQUE constraints).
* `menu_item`: Determinants are `menu_item_id` and `(restaurant_id, name)`. All are superkeys.
* `customer`: Determinants are `customer_id`, `email`, and `phone`. All are superkeys.
* `delivery_agent`: Determinants are `delivery_agent_id`, `phone`, and `vehicle_no`. All are superkeys.
* `food_order`: Determinant is `order_id` (PK). All are superkeys.
* `order_item`: Determinant is `(order_id, menu_item_id)` (composite PK). Superkey.
* `payment`: Determinants are `payment_id`, `order_id` (UNIQUE), and `transaction_ref` (UNIQUE). All are superkeys.
* **Result:** Every table in QuickBite strictly satisfies BCNF.

### 3.3 Stage 3: Physical Database Schema & Constraint Engineering
Physical implementation enforces bulletproof domain integrity:
* `restaurant`: Rating bounded between 0.0 and 5.0 via `CHECK (rating BETWEEN 0 AND 5)`. Unique composite constraint on `(name, location)`.
* `menu_item`: Price bounded to positive values via `CHECK (price > 0)`. Category constrained to an enumeration check (`'Starter'`, `'Main Course'`, `'Bread'`, `'Rice'`, `'Dessert'`, `'Beverage'`, `'Snack'`, `'Combo'`).
* `delivery_agent`: Vehicle type restricted to `'Bicycle'`, `'Scooter'`, `'Motorbike'`, `'EV Scooter'`.
* `food_order`: Mandatory foreign keys (`NOT NULL`) for `customer_id`, `restaurant_id`, and `delivery_agent_id`. Status constrained to `'Placed'`, `'Preparing'`, `'Out for Delivery'`, `'Delivered'`, `'Cancelled'`. Temporal integrity verified via `CHECK (delivered_time IS NULL OR delivered_time > order_time)`.
* `order_item`: Quantity restricted via `CHECK (quantity BETWEEN 1 AND 50)`. Unit price verified via `CHECK (unit_price > 0)`.

### 3.4 Stage 4: Procedural Enforcement via Triggers
Standard foreign keys can guarantee that `order_item.order_id` references a valid order and `order_item.menu_item_id` references a valid menu item. However, they cannot natively guarantee that the selected dish belongs to the **same restaurant** referenced by the order.

Denormalizing `restaurant_id` into `order_item` would violate 2NF (as `restaurant_id` would partially depend on `order_id`). QuickBite resolves this cleanly in the procedural layer using a `BEFORE INSERT OR UPDATE` PL/pgSQL trigger (`trg_order_item_same_restaurant`):
```sql
CREATE OR REPLACE FUNCTION trg_order_item_same_restaurant()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT restaurant_id FROM menu_item  WHERE menu_item_id = NEW.menu_item_id)
       IS DISTINCT FROM
       (SELECT restaurant_id FROM food_order WHERE order_id     = NEW.order_id) THEN
        RAISE EXCEPTION
            'Menu item % does not belong to the restaurant of order %',
            NEW.menu_item_id, NEW.order_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 3.5 Stage 5: Dynamic Views for Financial Consistency
To uphold 3NF and guarantee mathematical accuracy, the platform provides `v_order_total`:
```sql
CREATE VIEW v_order_total AS
SELECT fo.order_id,
       fo.restaurant_id,
       fo.customer_id,
       fo.status,
       fo.order_time,
       SUM(oi.quantity * oi.unit_price)::NUMERIC(10,2) AS order_total
FROM   food_order fo
JOIN   order_item oi ON oi.order_id = fo.order_id
GROUP  BY fo.order_id;
```
This view serves as the authoritative single source of truth for all downstream billing and revenue analytics.

### 3.6 Stage 6: High-Performance Composite Indexing Strategy
Food delivery search workloads are heavily dominated by consumer queries filtering by cuisine and geographical locality (e.g., *Find all North Indian restaurants in Kharghar*).
QuickBite implements a composite B-Tree index:
```sql
CREATE INDEX idx_restaurant_cuisine_location ON restaurant (cuisine, location);
```
* **Leftmost-Prefix Optimization:** Because `cuisine` occupies the leading position, this single index accelerates both combined `(cuisine, location)` queries and `cuisine`-only queries.
* **Skip-Scan Mechanics:** For queries filtering on `location` alone, PostgreSQL 18's B-Tree skip scan probes the index across distinct cuisines rather than falling back to an unindexed sequential scan.
* **Foreign Key Support Indexes:** Indexes are created across all foreign key columns (`menu_item.restaurant_id`, `food_order.restaurant_id`, `food_order.customer_id`, `food_order.delivery_agent_id`, `order_item.menu_item_id`) to accelerate relational join execution and optimize `ON DELETE RESTRICT` cascade validation.

---

## 4. Methods & Algorithms Technology Applied in the Problem Statement / Case Study

### 4.1 Relational Normalization & Functional Dependency Decomposition
* **Functional Dependency Closure:** Calculation of attribute closures $X^+$ under set $F$ to determine candidate keys.
* **Lossless Join Decomposition:** Ensuring that for every decomposition $R \to (R_1, R_2)$, $(R_1 \cap R_2) \to R_1$ or $(R_1 \cap R_2) \to R_2$.
* **Dependency Preservation:** Ensuring all functional dependencies can be checked within individual target relations without requiring cross-table joins.

### 4.2 Indexing Algorithms & Search Tree Traversal
* **B-Tree Search Mechanics:** Multilevel balanced search trees maintaining $O(\log N)$ point lookups and range scans.
* **Bitmap Index Scan vs. Parallel Sequential Scan:** For selective queries, PostgreSQL constructs an in-memory bitmap of matching heap physical block pointers, visiting only disk pages containing relevant records.
* **Leftmost-Prefix Evaluation:** Demonstrating algorithmic index utility based on search predicate alignment with composite index leading keys.

### 4.3 Analytical SQL Querying, Correlated Subqueries & Window Ranking
* **Correlated Subquery Aggregation:** Used in Query 1 to compute the maximum dish order count within each restaurant group and filter outer rows dynamically.
* **Window Partitioning & Tie-Breaking:**
  * `RANK() OVER (PARTITION BY restaurant_id ORDER BY COUNT(*) DESC)` to surface tied popularity leaders.
  * `ROW_NUMBER() OVER (PARTITION BY restaurant_id ORDER BY COUNT(*) DESC, SUM(quantity) DESC)` to break ties deterministically by total volume of units sold.
* **Multi-Table Relational Equi-Joins:** Itemized receipt generation traversing 7 interrelated tables in a single relational join tree.

### 4.4 Declarative & Procedural Integrity Enforcement
* **ACID Transactions:** Full transaction boundaries (`BEGIN ... ROLLBACK`) applied during synthetic scale testing to preserve baseline data isolation.
* **Procedural Exception Trapping:** Execution of PL/pgSQL procedural event listeners intercepting tuple mutation events before disk persistence.

### 4.5 Technology Stack Used for the Case
* **Database Management System:** PostgreSQL 18.x (compatible with PostgreSQL 14+).
* **Procedural & Query Languages:** SQL:2016, PL/pgSQL.
* **Administrative & Execution CLI:** `psql`, `createdb`, `dropdb`.
* **Automation & Scripting:** POSIX Shell / Bash (`run_all.sh`).
* **Environment:** macOS / Antigravity IDE / VS Code.
* **Benchmarking & Inspection:** PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`.

---

## 5. Problem Statement / Case Study Implementation Details and Snapshots

### 5.1 Project Directory & Module Architecture
The implementation is organized into modular SQL scripts executed through an automated orchestration pipeline:

```
final project/
├── sql/
│   ├── 01_schema.sql           # Table DDL, PK/FK, CHECKs, PL/pgSQL Trigger, View
│   ├── 02_indexes.sql          # Composite search index and foreign key indexes
│   ├── 03_seed_data.sql        # Realistic Mumbai/Navi Mumbai seed dataset
│   ├── 04_queries.sql          # Analytical query suite (Q1 through Q10)
│   ├── 05_index_demo.sql       # 200k-row synthetic index benchmark
│   └── 06_integrity_tests.sql  # 9-point negative referential integrity suite
├── outputs/
│   ├── 00_row_counts.txt       # Verified baseline entity counts
│   ├── 04_queries_output.txt   # Complete analytical query results
│   ├── 05_index_demo_output.txt# Query execution plans (with vs without index)
│   └── 06_integrity_tests_output.txt # Integrity violation notices
├── docs/
│   ├── er_diagram.png          # Visual Crow's Foot ER Diagram
│   ├── er_diagram_chen.png     # Visual Chen Notation ER Diagram
│   ├── normalization.md        # Mathematical 1NF to BCNF derivations
│   └── CODE_WALKTHROUGH.md     # Detailed code commentary
├── README.md                   # Repository overview and instructions
└── run_all.sh                  # One-click execution and validation script
```

### 5.2 Snapshot 1: Entity-Relationship Diagram (Crow's Foot & Chen Notation)

The relational schema coordinates 7 entities, modeling real-world food aggregation workflows:

```
 ┌──────────────────────┐             1:M             ┌──────────────────────┐
 │      RESTAURANT      │────────────────────────────►│      MENU_ITEM       │
 │──────────────────────│                             │──────────────────────│
 │ PK restaurant_id     │                             │ PK menu_item_id      │
 │    name, cuisine     │                             │ FK restaurant_id     │
 │    location, address │                             │    name, price, etc. │
 └──────────┬───────────┘                             └──────────┬───────────┘
            │                                                    │
            │ 1:M                                                │ 1:M
            ▼                                                    ▼
 ┌──────────────────────┐             1:M             ┌──────────────────────┐
 │      FOOD_ORDER      │────────────────────────────►│      ORDER_ITEM      │
 │──────────────────────│                             │──────────────────────│
 │ PK order_id          │                             │ PK (order_id,        │
 │ FK customer_id       │                             │     menu_item_id)    │
 │ FK restaurant_id     │                             │    quantity          │
 │ FK delivery_agent_id │                             │    unit_price        │
 └───────┬──────────▲───┘                             └──────────────────────┘
         │          │
     1:1 │          │ 1:M
         ▼          │
 ┌───────────────┐  │  ┌──────────────────────┐
 │    PAYMENT    │  └──│    DELIVERY_AGENT    │
 │───────────────│     │──────────────────────│
 │ PK payment_id │     │ PK delivery_agent_id │
 │ FK order_id   │     │    full_name, phone  │
 │    method     │     │    vehicle_type      │
 └───────────────┘     └──────────────────────┘
         ▲
         │ 1:M
 ┌───────┴──────────────┐
 │       CUSTOMER       │
 │──────────────────────│
 │ PK customer_id       │
 │    full_name, email  │
 └──────────────────────┘
```

### 5.3 Snapshot 2: Database Schema & Baseline Row Counts
Baseline seed data captures a realistic delivery operations cluster situated across Mumbai and Navi Mumbai (Kharghar, Vashi, CBD Belapur, Powai, Andheri West, Bandra West):

```
   table_name   | rows 
----------------+------
 restaurant     |   11
 menu_item      |   53
 customer       |   15
 delivery_agent |    8
 food_order     |   49
 order_item     |  110
 payment        |   49
(7 rows)
```

### 5.4 Snapshot 3: Procedural Trigger Implementation (`order_item_same_restaurant`)
```sql
CREATE OR REPLACE FUNCTION trg_order_item_same_restaurant()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT restaurant_id FROM menu_item  WHERE menu_item_id = NEW.menu_item_id)
       IS DISTINCT FROM
       (SELECT restaurant_id FROM food_order WHERE order_id     = NEW.order_id) THEN
        RAISE EXCEPTION
            'Menu item % does not belong to the restaurant of order %',
            NEW.menu_item_id, NEW.order_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_item_same_restaurant
BEFORE INSERT OR UPDATE ON order_item
FOR EACH ROW EXECUTE FUNCTION trg_order_item_same_restaurant();
```

### 5.5 Snapshot 4: Query 1 — Most Frequently Ordered Dish per Restaurant (With Ties)
Surfaces each merchant's top culinary offering for promotional placement using correlated ranking aggregation. Note that ties are cleanly retained (e.g., Dragon Wok ties on Chilli Paneer and Veg Hakka Noodles):

```sql
SELECT r.restaurant_id, r.name AS restaurant, m.name AS most_popular_dish,
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

#### Execution Output:
```
 restaurant_id |       restaurant       |   most_popular_dish   | times_ordered | units_sold 
---------------+------------------------+-----------------------+---------------+------------
             1 | Punjab Da Dhaba        | Butter Chicken        |             6 |          7
             2 | Udupi Sagar            | Masala Dosa           |             4 |          6
             3 | Dragon Wok             | Chilli Paneer         |             3 |          3
             3 | Dragon Wok             | Veg Hakka Noodles     |             3 |          4
             4 | La Pizzeria Napoli     | Margherita Pizza      |             4 |          5
             5 | Biryani Darbar         | Chicken Dum Biryani   |             5 |          8
             6 | Mumbai Chaat Corner    | Pav Bhaji             |             4 |          6
             7 | Amritsari Kulcha House | Amritsari Kulcha      |             3 |          6
             8 | Madras Filter Cafe     | Ghee Roast Dosa       |             3 |          4
             9 | Wok Express            | Chicken Hakka Noodles |             3 |          4
            10 | The Green Bowl         | Quinoa Buddha Bowl    |             2 |          2
(11 rows)
```

### 5.6 Snapshot 5: Query 1b — Single Promo Recommendation with Tie-Breaking
When the frontend banner UI requires exactly **one** promotional dish per restaurant, `ROW_NUMBER()` breaks ties by secondary volume of units sold (giving Veg Hakka Noodles the edge over Chilli Paneer):

```sql
WITH dish_stats AS (
    SELECT r.name AS restaurant, m.name AS dish,
           COUNT(*) AS times_ordered, SUM(oi.quantity) AS units_sold,
           RANK() OVER (PARTITION BY r.restaurant_id ORDER BY COUNT(*) DESC) AS pop_rank,
           ROW_NUMBER() OVER (PARTITION BY r.restaurant_id 
                              ORDER BY COUNT(*) DESC, SUM(oi.quantity) DESC) AS promo_rank
    FROM   order_item oi
    JOIN   menu_item  m  ON m.menu_item_id  = oi.menu_item_id
    JOIN   food_order fo ON fo.order_id     = oi.order_id
    JOIN   restaurant r  ON r.restaurant_id = m.restaurant_id
    WHERE  fo.status <> 'Cancelled'
    GROUP  BY r.restaurant_id, r.name, m.menu_item_id, m.name
)
SELECT restaurant, dish, times_ordered, units_sold, pop_rank,
       CASE WHEN promo_rank = 1 THEN 'YES' ELSE '' END AS promote
FROM   dish_stats
WHERE  pop_rank = 1
ORDER  BY restaurant;
```

#### Execution Output:
```
       restaurant       |         dish          | times_ordered | units_sold | popularity_rank | promote 
------------------------+-----------------------+---------------+------------+-----------------+---------
 Amritsari Kulcha House | Amritsari Kulcha      |             3 |          6 |               1 | YES
 Biryani Darbar         | Chicken Dum Biryani   |             5 |          8 |               1 | YES
 Dragon Wok             | Veg Hakka Noodles     |             3 |          4 |               1 | YES
 Dragon Wok             | Chilli Paneer         |             3 |          3 |               1 | 
 La Pizzeria Napoli     | Margherita Pizza      |             4 |          5 |               1 | YES
 Madras Filter Cafe     | Ghee Roast Dosa       |             3 |          4 |               1 | YES
 Mumbai Chaat Corner    | Pav Bhaji             |             4 |          6 |               1 | YES
 Punjab Da Dhaba        | Butter Chicken        |             6 |          7 |               1 | YES
 The Green Bowl         | Quinoa Buddha Bowl    |             2 |          2 |               1 | YES
 Udupi Sagar            | Masala Dosa           |             4 |          6 |               1 | YES
 Wok Express            | Chicken Hakka Noodles |             3 |          4 |               1 | YES
(11 rows)
```

### 5.7 Snapshot 6: Query 2 — Total Revenue Generated per Restaurant
Aggregates settled revenue per partner restaurant using a `LEFT JOIN` on `v_order_total`, cleanly preserving newly onboarded merchants (*Malvani Tadka*) with 0 orders and ₹0 revenue:

```sql
SELECT r.restaurant_id, r.name AS restaurant, r.cuisine,
       COUNT(t.order_id) AS delivered_orders,
       COALESCE(SUM(t.order_total), 0) AS total_revenue,
       ROUND(COALESCE(AVG(t.order_total), 0), 2) AS avg_order_value
FROM   restaurant r
LEFT   JOIN v_order_total t ON t.restaurant_id = r.restaurant_id
                           AND t.status = 'Delivered'
GROUP  BY r.restaurant_id, r.name, r.cuisine
ORDER  BY total_revenue DESC;
```

#### Execution Output:
```
 restaurant_id |       restaurant       |   cuisine    | delivered_orders | total_revenue | avg_order_value 
---------------+------------------------+--------------+------------------+---------------+-----------------
             5 | Biryani Darbar         | Mughlai      |                6 |       5270.00 |          878.33
             4 | La Pizzeria Napoli     | Italian      |                5 |       4447.00 |          889.40
             1 | Punjab Da Dhaba        | North Indian |                6 |       4330.00 |          721.67
             3 | Dragon Wok             | Chinese      |                4 |       2490.00 |          622.50
             7 | Amritsari Kulcha House | North Indian |                4 |       2110.00 |          527.50
             9 | Wok Express            | Chinese      |                4 |       2090.00 |          522.50
             2 | Udupi Sagar            | South Indian |                5 |       1610.00 |          322.00
             6 | Mumbai Chaat Corner    | Street Food  |                5 |       1550.00 |          310.00
            10 | The Green Bowl         | Continental  |                2 |       1390.00 |          695.00
             8 | Madras Filter Cafe     | South Indian |                4 |       1230.00 |          307.50
            11 | Malvani Tadka          | Malvani      |                0 |             0 |               0
(11 rows)
```

### 5.8 Snapshot 7: Query 3 — High-Speed Search by Cuisine & Locality
Demonstrates multi-attribute customer catalogue filtering serviced directly by the composite B-Tree index:

```sql
SELECT restaurant_id, name, cuisine, location, rating
FROM   restaurant
WHERE  cuisine = 'North Indian' AND location = 'Kharghar'
ORDER  BY rating DESC;
```

#### Execution Output:
```
 restaurant_id |          name          |   cuisine    | location | rating 
---------------+------------------------+--------------+----------+--------
             7 | Amritsari Kulcha House | North Indian | Kharghar |    4.5
             1 | Punjab Da Dhaba        | North Indian | Kharghar |    4.4
(2 rows)
```

### 5.9 Snapshot 8: Query 6 — Delivery Agent Performance & Average Transit Time
Tracks logistics fleet efficiency by extracting delivery turnaround durations in minutes:

```sql
SELECT da.delivery_agent_id, da.full_name AS agent, da.vehicle_type,
       COUNT(fo.order_id) AS delivered_orders,
       ROUND(AVG(EXTRACT(EPOCH FROM (fo.delivered_time - fo.order_time)) / 60)::numeric, 1) AS avg_delivery_mins
FROM   delivery_agent da
LEFT   JOIN food_order fo ON fo.delivery_agent_id = da.delivery_agent_id
                         AND fo.status = 'Delivered'
GROUP  BY da.delivery_agent_id, da.full_name, da.vehicle_type
ORDER  BY delivered_orders DESC, avg_delivery_mins ASC;
```

#### Execution Output:
```
 delivery_agent_id |     agent      | vehicle_type | delivered_orders | avg_delivery_mins 
-------------------+----------------+--------------+------------------+-------------------
                 2 | Suresh Patil   | Scooter      |                8 |              30.8
                 7 | Anil Kamble    | Bicycle      |                6 |              28.7
                 1 | Ramesh Yadav   | Motorbike    |                6 |              34.2
                 4 | Deepak Chauhan | Motorbike    |                6 |              36.8
                 3 | Imran Shaikh   | EV Scooter   |                6 |              37.7
                 5 | Joseph D'Souza | Scooter      |                5 |              40.6
                 6 | Ganesh More    | Motorbike    |                4 |              30.0
                 8 | Manoj Tiwari   | EV Scooter   |                4 |              37.8
(8 rows)
```

### 5.10 Snapshot 9: Query 9 — Itemized Order Invoice via 7-Table JOIN
Generates a complete billing ledger traversing all 7 tables in the database for order #26:

```
 order_id |    ordered_at     |  customer  |   restaurant   | delivery_agent |        item         | quantity | unit_price | line_total | paid_via 
----------+-------------------+------------+----------------+----------------+---------------------+----------+------------+------------+----------
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Chicken Dum Biryani |        3 |     320.00 |     960.00 | UPI
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Chicken Seekh Kebab |        2 |     280.00 |     560.00 | UPI
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Phirni              |        3 |     110.00 |     330.00 | UPI
(3 rows)
```

### 5.11 Snapshot 10: Advanced Concept — Index Scalability Benchmark on 200,000 Rows
To evaluate index performance under industrial scale, `05_index_demo.sql` populates **200,000 synthetic restaurant records** within an isolated transaction. The query `WHERE cuisine = 'North Indian' AND location = 'Kharghar'` is analyzed using `EXPLAIN (ANALYZE, BUFFERS)` both with and without `idx_restaurant_cuisine_location`:

#### Unindexed Execution Plan (Sequential Scan):
```
Gather (actual time=0.475..13.349 rows=835.00 loops=1)
  Workers Planned: 1, Workers Launched: 1
  Buffers: shared hit=2879
  -> Parallel Seq Scan on restaurant (actual time=0.036..9.085 rows=417.50 loops=2)
       Filter: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
       Rows Removed by Filter: 99588
Execution Time: 13.418 ms
```

#### Indexed Execution Plan (Bitmap Index Scan):
```
Bitmap Heap Scan on restaurant (actual time=0.182..1.010 rows=835.00 loops=1)
  Recheck Cond: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
  Heap Blocks: exact=834
  Buffers: shared hit=834 read=3
  -> Bitmap Index Scan on idx_restaurant_cuisine_location (actual time=0.098..0.098 rows=835.00 loops=1)
       Index Cond: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
       Index Searches: 1
Execution Time: 1.058 ms
```

The composite index reduces query latency from **13.42 ms to 1.05 ms**—yielding a **12.7× (~13×) speedup** while reducing disk block reads from 2,879 to 837 buffers.

### 5.12 Snapshot 11: Referential Integrity Suite Execution (9/9 Rejected)
To prove that the database reject corrupt, orphaned, or unauthorized data, `06_integrity_tests.sql` submits 9 intentionally malformed transactions within isolated savepoints:

```
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Order for a customer that does not exist (FK)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: violates foreign key constraint "food_order_customer_id_fkey"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Order for a restaurant that does not exist (FK)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: violates foreign key constraint "food_order_restaurant_id_fkey"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Order with no delivery agent (NOT NULL)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: null value in column "delivery_agent_id" violates not-null constraint
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Order line for a dish from ANOTHER restaurant (trigger)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: Menu item 21 does not belong to the restaurant of order 1
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Deleting a restaurant that still has orders (ON DELETE RESTRICT)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: violates RESTRICT setting of foreign key constraint "menu_item_restaurant_id_fkey"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Second payment for an already-paid order (1:1 UNIQUE)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: duplicate key value violates unique constraint "payment_order_id_key"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Menu item with a negative price (CHECK)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: violates check constraint "menu_item_price_check"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Unknown order status (CHECK)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: violates check constraint "food_order_status_check"
psql:sql/06_integrity_tests.sql:46: NOTICE:  OK    Duplicate customer e-mail (UNIQUE)
psql:sql/06_integrity_tests.sql:46: NOTICE:        rejected: duplicate key value violates unique constraint "customer_email_key"
```
**Result:** 100% of illegal operations (9/9) were safely intercepted and rejected.

---

## 6. Problem Statement / Case Study Results and Conclusion

### 6.1 Key Findings
1. **Elimination of Structural Anomalies via BCNF:** Decomposing the unnormalized catalog into 7 distinct entities eliminated all partial and transitive functional dependencies. Modifying a restaurant's locality now requires exactly one row update, and newly onboarded restaurants (*Malvani Tadka*) can exist independently of menu creation.
2. **Empirical Index Acceleration:** Testing against 200,000 synthetic records confirmed the theoretical advantages of B-Tree indexing. Search execution times dropped from **13.42 ms to 1.05 ms (~13× speedup)**, transforming an expensive parallel table scan into an exact point seek.
3. **Trigger-Based Domain Invariants:** By leveraging a PL/pgSQL procedural trigger (`trg_order_item_same_restaurant`), the system guarantees that orders cannot cross-contaminate menu items across different restaurants, preserving database purity while keeping `order_item` strictly in 2NF.
4. **Calculated Consistency via Dynamic Views:** Eliminating stored order totals in favor of `v_order_total` guaranteed 100% mathematical precision across all billing and revenue aggregations, permanently avoiding ledger drift.
5. **Airtight Relational Defense:** All 9 deliberate constraint violations were cleanly blocked by the database engine without side effects.

### 6.2 Comparison of Query Performance (Indexed vs. Unindexed)
| Metric | Without Index (`Parallel Seq Scan`) | With Composite Index (`Bitmap Index Scan`) | Optimization Factor |
|---|---|---|---|
| **Query Mechanism** | Full table scan across 200,011 rows | B-Tree index traversal + exact block heap scan | Direct Seek |
| **Rows Examined** | 200,011 rows (199,176 filtered out) | 835 rows (only matching candidate rows) | ~240× reduction |
| **Shared Buffers Hit** | 2,879 pages | 837 pages | 3.4× less I/O |
| **Planning Time** | 0.134 ms | 0.143 ms | Comparable |
| **Execution Time** | **13.418 ms** | **1.058 ms** | **~12.7× (~13× faster)** |

### 6.3 Conclusion & Future Enhancements
This case study successfully designed, implemented, and empirically validated the **QuickBite Food Delivery Order & Restaurant Management System** on PostgreSQL 18. All four primary project outcomes were accomplished:
* Scalable multi-attribute restaurant browsing via composite B-Tree indexing.
* Dynamic surfacing of each restaurant's most popular dish (with full tie-handling).
* Real-time aggregation of net restaurant revenue via computed views.
* Airtight multi-entity referential integrity guaranteed through relational constraints and procedural triggers.

#### Future Architectural Roadmap
* **Geospatial Proximity Routing:** Integrating the **PostGIS** extension (`ST_DWithin`, `ST_Distance`) to compute customer-restaurant-agent routing and dynamic delivery fees based on real-time GPS coordinates.
* **Declarative Table Partitioning:** Implementing PostgreSQL declarative range partitioning on `food_order` by `order_time` (e.g., monthly partitions) to ensure high throughput as transaction volumes scale into millions of orders.
* **Materialized Caching:** Deploying materialized views refreshed concurrently on schedule for heavy analytical reporting dashboards, paired with Redis caching for top-level menu browsing.

---

## 7. References

1. **Silberschatz, A., Korth, H. F., & Sudarshan, S.** (2020). *Database System Concepts* (7th ed.). McGraw-Hill Education.
2. **Elmasri, R., & Navathe, S. B.** (2016). *Fundamentals of Database Systems* (7th ed.). Pearson.
3. **Date, C. J.** (2004). *An Introduction to Database Systems* (8th ed.). Addison-Wesley.
4. **PostgreSQL Global Development Group.** (2024). *PostgreSQL 18 Documentation: B-Tree Indexing, Concurrency Control, and Triggers*. Available online: https://www.postgresql.org/docs/
5. **Codd, E. F.** (1970). *A Relational Model of Data for Large Shared Data Banks*. Communications of the ACM, 13(6), 377–387.
6. **Codd, E. F.** (1974). *Recent Investigations in Relational Data Base Systems*. IFIP Congress, 1017–1021.
7. **School of Future Tech, ITM Skills University.** (2025). *Database Management Systems Course Curriculum & Case Study Specifications (Case Study #83)*.
