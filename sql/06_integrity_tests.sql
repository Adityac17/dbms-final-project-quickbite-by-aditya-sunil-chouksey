-- =====================================================================
-- QuickBite — 06_integrity_tests.sql
-- Each block attempts an INVALID write and shows the constraint that
-- rejects it. Nothing is changed in the database.
-- =====================================================================

DO $$
DECLARE
    tests TEXT[][] := ARRAY[
      ['Order for a customer that does not exist (FK)',
       $q$INSERT INTO food_order (customer_id, restaurant_id, delivery_agent_id, delivery_address)
          VALUES (999, 1, 1, 'Nowhere')$q$],
      ['Order for a restaurant that does not exist (FK)',
       $q$INSERT INTO food_order (customer_id, restaurant_id, delivery_agent_id, delivery_address)
          VALUES (1, 999, 1, 'Nowhere')$q$],
      ['Order with no delivery agent (NOT NULL)',
       $q$INSERT INTO food_order (customer_id, restaurant_id, delivery_agent_id, delivery_address)
          VALUES (1, 1, NULL, 'B-204, Sai Heights')$q$],
      ['Order line for a dish from ANOTHER restaurant (trigger)',
       $q$INSERT INTO order_item (order_id, menu_item_id, quantity, unit_price)
          VALUES (1, 21, 1, 320)$q$],
      ['Deleting a restaurant that still has orders (ON DELETE RESTRICT)',
       $q$DELETE FROM restaurant WHERE restaurant_id = 1$q$],
      ['Second payment for an already-paid order (1:1 UNIQUE)',
       $q$INSERT INTO payment (order_id, method, status) VALUES (1, 'Cash', 'Paid')$q$],
      ['Menu item with a negative price (CHECK)',
       $q$INSERT INTO menu_item (restaurant_id, name, category, price, is_veg)
          VALUES (1, 'Free Lunch', 'Main Course', -10, TRUE)$q$],
      ['Unknown order status (CHECK)',
       $q$UPDATE food_order SET status = 'Lost' WHERE order_id = 1$q$],
      ['Duplicate customer e-mail (UNIQUE)',
       $q$INSERT INTO customer (full_name, email, phone, address, location)
          VALUES ('Copy Cat', 'aarav.sharma@example.com', '9999999999', 'x', 'Vashi')$q$]
    ];
    i INT;
BEGIN
    FOR i IN 1 .. array_length(tests, 1) LOOP
        BEGIN
            EXECUTE tests[i][2];
            RAISE NOTICE 'FAIL  % -> was accepted!', tests[i][1];
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE 'OK    %', tests[i][1];
            RAISE NOTICE '      rejected: %', SQLERRM;
        END;
    END LOOP;
END $$;
