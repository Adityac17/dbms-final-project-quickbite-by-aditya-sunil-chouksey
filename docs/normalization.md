# QuickBite — Schema Design & Normalization

## 1. Starting point: the unnormalized listing

Today QuickBite keeps menus in one flat sheet. Every menu-item row repeats its restaurant's details:

| RestaurantID | RestaurantName  | Cuisine      | Location | Address          | ItemID | ItemName       | Price |
|---|---|---|---|---|---|---|---|
| 1 | Punjab Da Dhaba | North Indian | Kharghar | Shop 4, Sector 7 | 1 | Butter Chicken | 340 |
| 1 | Punjab Da Dhaba | North Indian | Kharghar | Shop 4, Sector 7 | 2 | Dal Makhani    | 260 |
| 1 | Punjab Da Dhaba | North Indian | Kharghar | Shop 4, Sector 7 | 3 | Paneer Tikka   | 290 |
| 2 | Udupi Sagar     | South Indian | Vashi    | Plot 12, Sec 17  | 6 | Masala Dosa    | 120 |

Orders are kept the same way: one row per dish ordered, with customer, restaurant and agent details copied onto each row.

**Candidate key:** `(RestaurantID, ItemID)`

**Functional dependencies:**

- `RestaurantID → RestaurantName, Cuisine, Location, Address`
- `(RestaurantID, ItemID) → ItemName, Price`

### Anomalies this causes

| Anomaly | Example |
|---|---|
| **Update** | Punjab Da Dhaba moves. Its address must change on every menu row. If one row is missed, the data contradicts itself. |
| **Insert** | Malvani Tadka can't be listed until it has at least one dish, because `ItemID` is part of the key. |
| **Delete** | Deleting a restaurant's last dish also deletes the only record of the restaurant. |
| **Storage** | Cuisine and address are stored once per dish instead of once per restaurant. |

## 2. First Normal Form (1NF)

1NF needs atomic values, no repeating groups, and a primary key. The flat sheet already meets this: there is one dish per row, and no cell holds a list of items. The problem is redundancy, which 1NF doesn't address.

## 3. Second Normal Form (2NF): removing partial dependencies

`Cuisine`, `Location` and `Address` depend on `RestaurantID` alone, which is only **part** of the composite key `(RestaurantID, ItemID)`. That is a partial dependency, so the table breaks 2NF.

**Fix (the case study's requirement):** move the restaurant attributes into their own table and link menu items to it by `RestaurantID`.

```
RESTAURANT (restaurant_id PK, name, cuisine, location, address, phone, rating, is_active)
MENU_ITEM  (menu_item_id PK, restaurant_id FK → RESTAURANT, name, category, price, is_veg, is_available)
```

Each restaurant's cuisine and address are now stored exactly once.

The flat order sheet is split the same way:

```
CUSTOMER       (customer_id PK, ...)
DELIVERY_AGENT (delivery_agent_id PK, ...)
FOOD_ORDER     (order_id PK, customer_id FK, restaurant_id FK, delivery_agent_id FK, order_time, ...)
ORDER_ITEM     (order_id PK/FK, menu_item_id PK/FK, quantity, unit_price)
```

`ORDER_ITEM` has the composite key `(order_id, menu_item_id)`. Both `quantity` and `unit_price` depend on the **whole** key, so there's no partial dependency.

> **Design note: no `restaurant_id` in ORDER_ITEM.** Copying `restaurant_id` into order lines would let a composite foreign key check that each dish belongs to the order's restaurant. But `restaurant_id` depends on `order_id` alone, which would bring back a partial dependency and break 2NF. The rule is enforced with a trigger instead (`trg_order_item_same_restaurant`).

## 4. Third Normal Form (3NF): removing transitive dependencies

3NF means no non-key attribute depends on another non-key attribute.

| Table | Check |
|---|---|
| RESTAURANT | Every attribute depends only on `restaurant_id`. `phone` is also a candidate key (UNIQUE). `location` is the area, `address` is the street line. Neither determines the other. |
| MENU_ITEM | `name`, `price` and `category` depend on `menu_item_id`. `(restaurant_id, name)` is a second candidate key. |
| CUSTOMER | `email` and `phone` are candidate keys (UNIQUE). No other attribute determines anything. |
| DELIVERY_AGENT | `phone` and `vehicle_no` are candidate keys. |
| FOOD_ORDER | Customer, restaurant and agent details are **not** copied here, only their FKs. |
| PAYMENT | `order_id` is UNIQUE, so it's a candidate key (1 : 1). `method` and `status` depend on the payment. |

**Derived data isn't stored.** The order total is `SUM(quantity × unit_price)`. Storing it in `FOOD_ORDER` would create a transitive dependency (order → lines → total) and risk it drifting out of sync. It's computed by the view `v_order_total` instead.

**Two copies that are deliberate and stay in 3NF:**

- `order_item.unit_price`: the price **at the moment of the order**. The menu price can change later, and past orders must still add up. It's a separate fact about the order line, not a copy of `menu_item.price`.
- `food_order.delivery_address`: where **this** order was delivered. The customer may move later, and the order's history must not change.

## 5. Boyce–Codd Normal Form (BCNF)

BCNF means the determinant of every non-trivial FD is a superkey.

| Table | Determinants | All superkeys? |
|---|---|---|
| restaurant | `restaurant_id`, `phone`, `(name, location)` | ✅ |
| menu_item | `menu_item_id`, `(restaurant_id, name)` | ✅ |
| customer | `customer_id`, `email`, `phone` | ✅ |
| delivery_agent | `delivery_agent_id`, `phone`, `vehicle_no` | ✅ |
| food_order | `order_id` | ✅ |
| order_item | `(order_id, menu_item_id)` | ✅ |
| payment | `payment_id`, `order_id`, `transaction_ref` | ✅ |

**Every table is in BCNF.**

## 6. Relationship summary

| Relationship | Cardinality | Implemented by |
|---|---|---|
| Restaurant offers MenuItem | 1 : M | `menu_item.restaurant_id` FK, NOT NULL |
| Restaurant receives FoodOrder | 1 : M | `food_order.restaurant_id` FK, NOT NULL |
| Customer places FoodOrder | 1 : M | `food_order.customer_id` FK, NOT NULL |
| DeliveryAgent delivers FoodOrder | 1 : M | `food_order.delivery_agent_id` FK, NOT NULL |
| FoodOrder contains MenuItem | **M : N** | junction table `order_item` with composite PK |
| FoodOrder is paid by Payment | **1 : 1** | `payment.order_id` FK + UNIQUE |
