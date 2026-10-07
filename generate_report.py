import base64
import os
import subprocess

def main():
    with open('docs/itm_logo.png', 'rb') as f:
        logo_b64 = base64.b64encode(f.read()).decode('utf-8')

    with open('docs/er_diagram.png', 'rb') as f:
        er_b64 = base64.b64encode(f.read()).decode('utf-8')

    html_path = 'docs/case_study_report.html'
    pdf_path = 'docs/CASE_STUDY_REPORT.pdf'
    root_pdf_path = 'CASE_STUDY_REPORT.pdf'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>QuickBite - DBMS Case Study Report</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 20mm 16mm 20mm 16mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1f2937;
    line-height: 1.5;
    font-size: 9.5pt;
    margin: 0;
    padding: 0;
  }}
  .cover-page {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    page-break-after: always;
    break-after: page;
    padding: 40mm 20mm 30mm 20mm;
  }}
  .cover-top {{
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .cover-logo {{
    width: 280px;
    height: auto;
    margin-bottom: 25px;
  }}
  .cover-school {{
    font-size: 20pt;
    font-weight: 700;
    color: #111827;
    margin-bottom: 50px;
    letter-spacing: -0.5px;
  }}
  .cover-title-box {{
    margin: 30px 0;
  }}
  .cover-report-label {{
    font-size: 22pt;
    font-weight: 800;
    color: #111827;
    margin: 0 0 15px 0;
  }}
  .cover-on {{
    font-size: 14pt;
    color: #4b5563;
    margin: 0 0 15px 0;
    font-style: italic;
  }}
  .cover-title {{
    font-size: 20pt;
    font-weight: 800;
    color: #1e3a8a;
    line-height: 1.3;
    margin: 0 0 12px 0;
  }}
  .cover-subtitle {{
    font-size: 12pt;
    font-weight: 600;
    color: #4b5563;
  }}
  .cover-by {{
    font-size: 13pt;
    color: #4b5563;
    margin-bottom: 8px;
  }}
  .cover-author {{
    font-size: 16pt;
    font-weight: 700;
    color: #111827;
    margin: 0 0 4px 0;
  }}
  .cover-roll {{
    font-size: 14pt;
    font-weight: 600;
    color: #374151;
    margin: 0 0 4px 0;
  }}
  .cover-dept {{
    font-size: 11pt;
    color: #6b7280;
    margin: 0;
  }}
  .index-page {{
    page-break-after: always;
    break-after: page;
    padding-top: 20mm;
  }}
  .index-title {{
    font-size: 20pt;
    font-weight: 700;
    margin-bottom: 25px;
    color: #111827;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 10px;
  }}
  .index-list {{
    list-style: none;
    padding: 0;
    margin: 0;
    font-size: 11pt;
    line-height: 2.3;
  }}
  .index-item {{
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dotted #cbd5e1;
    padding-bottom: 4px;
    margin-bottom: 12px;
    font-weight: 600;
    color: #1f2937;
  }}
  .section {{
    margin-bottom: 20px;
  }}
  h1.section-heading {{
    font-size: 13.5pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h2.sub-heading {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  h3.sub-sub-heading {{
    font-size: 10pt;
    font-weight: 700;
    color: #334155;
    margin-top: 10px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
  }}
  p {{
    margin: 0 0 8px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 9px 0;
    padding-left: 18px;
  }}
  li {{
    margin-bottom: 3px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 4px 7px;
    text-align: left;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  pre, code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 7.5pt;
  }}
  pre {{
    background-color: #0f172a;
    color: #f8fafc;
    padding: 7px 10px;
    border-radius: 4px;
    overflow-x: auto;
    line-height: 1.3;
    margin: 8px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .diagram-container {{
    text-align: center;
    margin: 12px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .diagram-img {{
    max-width: 90%;
    height: auto;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}
  .caption {{
    font-size: 7.5pt;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }}
  .callout {{
    background-color: #eff6ff;
    border-left: 3.5px solid #2563eb;
    padding: 7px 10px;
    margin: 8px 0;
    border-radius: 0 4px 4px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  .callout-title {{
    font-weight: 700;
    color: #1e40af;
    margin-bottom: 2px;
  }}
</style>
</head>
<body>

<!-- PAGE 1: COVER PAGE -->
<div class="cover-page">
  <div class="cover-top">
    <img src="data:image/png;base64,{logo_b64}" class="cover-logo" alt="ITM Skills University Logo">
    <div class="cover-school">School of Future Tech</div>
  </div>

  <div class="cover-title-box">
    <div class="cover-report-label">Case Study Report</div>
    <div class="cover-on">on</div>
    <div class="cover-title">QuickBite: Food Delivery Order &amp; Restaurant Management System</div>
    <div class="cover-subtitle">DBMS Case Study #83 &middot; B.Tech Computer Science Engineering</div>
  </div>

  <div class="cover-bottom">
    <div class="cover-by">by</div>
    <div class="cover-author">Aditya Sunil Chouksey</div>
    <div class="cover-roll">Roll Number: 150096725070</div>
    <div class="cover-dept">Semester III &middot; Academic Year 2025&ndash;2029</div>
  </div>
</div>

<!-- PAGE 2: INDEX -->
<div class="index-page">
  <div class="index-title">Index</div>
  <ul class="index-list">
    <li class="index-item"><span>1. Introduction to the Case Study.</span> <span>3</span></li>
    <li class="index-item"><span>2. Problem Statement / Case Background (Abstract).</span> <span>4</span></li>
    <li class="index-item"><span>3. Problem Statement / Case Study Design.</span> <span>5</span></li>
    <li class="index-item"><span>4. Methods &amp; Algorithms Technology Applied in the Problem Statement / Case Study.</span> <span>7</span></li>
    <li class="index-item"><span>5. Problem Statement / Case Study Implementation Details and Snapshots.</span> <span>8</span></li>
    <li class="index-item"><span>6. Problem Statement / Case Study Results and Conclusion.</span> <span>11</span></li>
    <li class="index-item"><span>7. References</span> <span>12</span></li>
  </ul>
</div>

<!-- SECTION 1 -->
<div class="section">
  <h1 class="section-heading">1. Introduction to the Case Study</h1>
  <p>
    Online food delivery aggregators and restaurant platforms are central to urban commerce and daily consumer life, handling millions of transactional events across restaurants, dynamic menus, customer requests, and delivery logistics. Modern food delivery platforms such as Zomato, Swiggy, and DoorDash operate as high-throughput, multi-sided digital marketplaces. They continuously orchestrate real-time interactions across four key stakeholders: end consumers searching menus and submitting digital orders, partner restaurants managing dish availability and processing culinary preparation, freelance delivery riders fulfilling dispatch across dynamic geographical transit zones, and platform administrators tracking financial settlements, commissions, and marketing campaigns.
  </p>
  <p>
    Underlying this high-frequency user ecosystem is a demanding database engineering requirement. A production food-delivery database cannot merely act as a passive data store; it must guarantee absolute transactional and financial consistency, enforce rigorous domain integrity across distributed entities, execute complex business intelligence aggregations, and sustain sub-millisecond query search response times under catalogs spanning hundreds of thousands of restaurants.
  </p>
  <p>
    This case study focuses on designing, architecting, and implementing <strong>QuickBite</strong> &mdash; a relational database management system for a food delivery order and restaurant aggregator platform. Engineered and benchmarked using <strong>PostgreSQL 18</strong>, QuickBite demonstrates how foundational database theory &mdash; spanning conceptual Entity-Relationship (ER) modeling, mathematical dependency decomposition up to Boyce-Codd Normal Form (BCNF), procedural PL/pgSQL triggers, non-materialized views, composite B-Tree indexing, and advanced SQL analytical queries &mdash; solves the operational bottlenecks inherent in large-scale online food commerce.
  </p>
</div>

<!-- SECTION 2 -->
<div class="section">
  <h1 class="section-heading">2. Problem Statement / Case Background (Abstract)</h1>
  
  <h2 class="sub-heading">Background</h2>
  <p>
    In early-stage platform development or poorly architected architectures, delivery applications frequently record restaurant menus, customer accounts, and order transactions in flat, unnormalized tables or disjointed spreadsheets. In an unnormalized schema, every dish listed copies the complete restaurant profile (merchant name, cuisine category, city locality, street address, and contact number). Similarly, every order line duplicates consumer and courier details.
  </p>
  <p>
    This architectural denormalization induces severe structural database anomalies:
  </p>
  <ul>
    <li><strong>Update Anomalies:</strong> If a partner restaurant relocates to a new address or updates its telephone number, every single menu item row associated with that restaurant must be independently altered. If an update misses even one row, the database suffers contradictory records, disrupting order fulfillment.</li>
    <li><strong>Insertion Anomalies:</strong> A newly onboarded restaurant (such as <em>Malvani Tadka</em>) cannot be registered in the system until it publishes at least one active dish, because naive composite keys of <code>(RestaurantID, ItemID)</code> prohibit null key components.</li>
    <li><strong>Deletion Anomalies:</strong> If a restaurant temporarily purges all seasonal dishes from its catalog, deleting those dish rows inadvertently wipes out the entire operational footprint, address, and rating of the restaurant itself.</li>
    <li><strong>Referential Gaps:</strong> Without foreign key constraints and procedural checks, customers can place orders containing dishes belonging to multiple disparate restaurants, creating an impossible physical dispatch assignment.</li>
    <li><strong>Scalability Degradation:</strong> As directories grow to hundreds of thousands of listings, full table sequential scans (<code>Seq Scan</code>) cause search response times to degrade severely, creating intolerable user latency.</li>
  </ul>

  <h2 class="sub-heading">Abstract</h2>
  <p>
    This case study presents the comprehensive design, implementation, and empirical evaluation of <strong>QuickBite</strong>, an enterprise-grade relational database system built on PostgreSQL 18. The database schema resolves the flat delivery model by decomposing into <strong>7 strictly normalized entities</strong> meeting <strong>Boyce-Codd Normal Form (BCNF)</strong>: <code>restaurant</code>, <code>menu_item</code>, <code>customer</code>, <code>delivery_agent</code>, <code>food_order</code>, <code>order_item</code>, and <code>payment</code>. This decomposition systematically eliminates all partial and transitive functional dependencies while guaranteeing lossless join decomposition.
  </p>
  <p>
    To enforce complex multi-table operational rules without introducing denormalized columns, QuickBite incorporates a procedural PL/pgSQL event trigger (<code>trg_order_item_same_restaurant</code>) that strictly prevents orders from including dishes from foreign kitchens. Financial totals are dynamically computed via the view <code>v_order_total</code>, permanently eliminating the risk of stored order sums drifting from itemized line totals. For search acceleration, a composite B-Tree index on <code>restaurant(cuisine, location)</code> is implemented; empirical scalability benchmarking on a <strong>200,000-restaurant dataset</strong> reveals a reduction in query execution time from <strong>13.42 ms to 1.05 ms (~13&times; speedup)</strong>. A suite of 10 analytical SQL queries extracts actionable operational insights, and the system is formally validated against a 9-point referential integrity test suite achieving 100% rejection of illegal transactions.
  </p>
</div>

<!-- SECTION 3 -->
<div class="section">
  <h1 class="section-heading">3. Problem Statement / Case Study Design</h1>
  <p>
    The QuickBite database system is engineered through an end-to-end, multi-stage relational lifecycle comprising eight foundational phases:
  </p>

  <h2 class="sub-heading">3.1 Stage 1: Conceptual Design &amp; Entity-Relationship Modeling</h2>
  <p>
    The system models the food delivery ecosystem through seven core entities, capturing complete business lifecycles:
  </p>
  <ul>
    <li><strong>Restaurant:</strong> Encapsulates merchant identity, cuisine classification, locality, physical street address, contact phone, consumer rating, and operational activation flag.</li>
    <li><strong>MenuItem:</strong> Stores individual dishes, course category (Starter, Main Course, Dessert, etc.), selling price, vegetarian indicator (<code>is_veg</code>), and inventory availability.</li>
    <li><strong>Customer:</strong> Holds user profile data, verified email, phone number, physical address, locality, and registration date.</li>
    <li><strong>DeliveryAgent:</strong> Details logistics personnel, verified contact phone, vehicle classification (Bicycle, Scooter, Motorbike, EV Scooter), license plate number, and assigned home zone.</li>
    <li><strong>FoodOrder:</strong> Tracks individual order transactions, linking the purchasing customer, preparing restaurant, and assigned courier. Captures timestamp, delivery destination snapshot, and fulfillment status.</li>
    <li><strong>OrderItem:</strong> Resolves the many-to-many (M : N) relationship between orders and menu items, recording ordered quantities and the frozen historical unit price charged at checkout.</li>
    <li><strong>Payment:</strong> Establishes a 1:1 relationship with each food order, recording transaction method (UPI, Card, Cash, Wallet), settlement status, transaction reference IDs, and timestamps.</li>
  </ul>

  <table>
    <thead>
      <tr>
        <th>Relationship</th>
        <th>Cardinality</th>
        <th>Foreign Key Constraint</th>
        <th>Deletion Behavior</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Restaurant &rarr; MenuItem</td>
        <td>1 : M</td>
        <td><code>menu_item.restaurant_id &rarr; restaurant.restaurant_id</code></td>
        <td><code>ON DELETE RESTRICT</code></td>
      </tr>
      <tr>
        <td>Restaurant &rarr; FoodOrder</td>
        <td>1 : M</td>
        <td><code>food_order.restaurant_id &rarr; restaurant.restaurant_id</code></td>
        <td><code>ON DELETE RESTRICT</code></td>
      </tr>
      <tr>
        <td>Customer &rarr; FoodOrder</td>
        <td>1 : M</td>
        <td><code>food_order.customer_id &rarr; customer.customer_id</code></td>
        <td><code>ON DELETE RESTRICT</code></td>
      </tr>
      <tr>
        <td>DeliveryAgent &rarr; FoodOrder</td>
        <td>1 : M</td>
        <td><code>food_order.delivery_agent_id &rarr; delivery_agent.delivery_agent_id</code></td>
        <td><code>ON DELETE RESTRICT</code></td>
      </tr>
      <tr>
        <td>FoodOrder &harr; MenuItem (via OrderItem)</td>
        <td>M : N</td>
        <td><code>order_item.order_id</code> (CASCADE), <code>order_item.menu_item_id</code> (RESTRICT)</td>
        <td>Composite PK <code>(order_id, menu_item_id)</code></td>
      </tr>
      <tr>
        <td>FoodOrder &rarr; Payment</td>
        <td>1 : 1</td>
        <td><code>payment.order_id &rarr; food_order.order_id</code> (UNIQUE)</td>
        <td><code>ON DELETE CASCADE</code></td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-heading">3.2 Stage 2: Logical Schema Design &amp; Normalization (1NF &rarr; BCNF)</h2>
  <p>
    Normalization eliminates redundancy and ensures structural anomalies cannot occur:
  </p>
  <ul>
    <li><strong>First Normal Form (1NF):</strong> All attributes contain atomic, indivisible values. No repeating groups or arrays exist. Primary keys are formally declared for every entity.</li>
    <li><strong>Second Normal Form (2NF):</strong> In the flat menu listing, attributes <code>Cuisine</code>, <code>Location</code>, and <code>Address</code> depend on <code>RestaurantID</code> alone, which is only part of the composite key <code>(RestaurantID, ItemID)</code>. This partial dependency is resolved by splitting into <code>restaurant</code> and <code>menu_item</code>. Similarly, order lines are isolated in <code>order_item</code> where quantity and unit price depend on the complete key <code>(order_id, menu_item_id)</code>.</li>
    <li><strong>Third Normal Form (3NF):</strong> No non-key attribute transitively depends on another non-key attribute. Specifically, total order amount is deliberately excluded from <code>food_order</code> and computed dynamically via view <code>v_order_total</code>, preventing data drift. Historical pricing (<code>unit_price</code> at order time) and snapshot delivery addresses are preserved as legitimate historical facts.</li>
    <li><strong>Boyce-Codd Normal Form (BCNF):</strong> For every non-trivial functional dependency X &rarr; Y, determinant X is a superkey. All 7 tables in QuickBite satisfy BCNF.</li>
  </ul>

  <h2 class="sub-heading">3.3 Stage 3: Physical Schema Design &amp; Integrity Constraints</h2>
  <p>
    Domain and data integrity are enforced at the database kernel level through check constraints, unique keys, and strict nullability rules:
  </p>
  <ul>
    <li><code>restaurant.rating CHECK (rating BETWEEN 0 AND 5)</code> and <code>UNIQUE (name, location)</code>.</li>
    <li><code>menu_item.price CHECK (price &gt; 0)</code> and <code>category CHECK (category IN ('Starter', 'Main Course', ...))</code>.</li>
    <li><code>food_order</code> mandates <code>NOT NULL</code> on <code>customer_id</code>, <code>restaurant_id</code>, and <code>delivery_agent_id</code>. Status is restricted to valid lifecycle states, and <code>CHECK (delivered_time IS NULL OR delivered_time &gt; order_time)</code> ensures temporal consistency.</li>
    <li><code>order_item.quantity CHECK (quantity BETWEEN 1 AND 50)</code> and <code>unit_price CHECK (unit_price &gt; 0)</code>.</li>
  </ul>

  <h2 class="sub-heading">3.4 Stage 4: Procedural Enforcement via Triggers</h2>
  <p>
    Standard foreign key constraints can verify that an order ID exists and a menu item ID exists, but cannot check that the dish ordered originates from the specific restaurant fulfilling the order. Rather than copying <code>restaurant_id</code> into <code>order_item</code> (which would violate 2NF), QuickBite deploys a PL/pgSQL trigger (<code>trg_order_item_same_restaurant</code>) executing before insertion or update to reject cross-restaurant cart contamination.
  </p>

  <h2 class="sub-heading">3.5 Stage 5: Dynamic Views for Single Source of Truth</h2>
  <p>
    The dynamic view <code>v_order_total</code> joins <code>food_order</code> to <code>order_item</code>, computing order totals on demand. This architecture eliminates update anomalies while serving as the authoritative financial ledger for all billing and analytical queries.
  </p>

  <h2 class="sub-heading">3.6 Stage 6: Composite Indexing Architecture</h2>
  <p>
    A multi-column B-Tree index <code>idx_restaurant_cuisine_location</code> on <code>(cuisine, location)</code> is deployed. Under the leftmost-prefix rule, it supports multi-column filtering and cuisine-only browsing. Supporting B-Tree indexes are created on all foreign key columns to optimize relational join performance.
  </p>

  <h2 class="sub-heading">3.7 Stage 7: Analytical Business Intelligence Suite</h2>
  <p>
    A set of 10 analytical queries provides core metrics: most popular dish per restaurant (with ties), single-dish promotional tie-breaking, total restaurant revenue, delivery fleet efficiency, top customers by spend, and 7-table itemized invoicing.
  </p>

  <h2 class="sub-heading">3.8 Stage 8: Scalability Benchmarking &amp; Integrity Testing</h2>
  <p>
    Empirical validation is conducted via a 200,000-row synthetic benchmark comparing unindexed sequential scans against indexed seeks, followed by a 9-vector negative test suite validating constraint rejection.
  </p>
</div>

<!-- SECTION 4 -->
<div class="section">
  <h1 class="section-heading">4. Methods &amp; Algorithms Technology Applied in the Problem Statement / Case Study</h1>
  
  <h2 class="sub-heading">Key Methods and Algorithms</h2>
  
  <h3 class="sub-sub-heading">1. Relational Decomposition &amp; Functional Dependency Theory</h3>
  <ul>
    <li><strong>Attribute Closure Algorithm:</strong> Used to identify candidate keys and eliminate redundancy across relations.</li>
    <li><strong>Lossless Join Decomposition:</strong> Proves that joining decomposed tables R1 and R2 on common attributes recreates the exact original relation without spurious tuples.</li>
    <li><strong>BCNF Verification:</strong> Ensures that for every non-trivial dependency X &rarr; Y, X contains a candidate key.</li>
  </ul>

  <h3 class="sub-sub-heading">2. Indexing Algorithms &amp; Search Tree Traversal</h3>
  <ul>
    <li><strong>B-Tree Multi-Level Search:</strong> Balanced search tree structure enabling O(log N) point seek and range scan complexity across large data blocks.</li>
    <li><strong>Leftmost-Prefix Principle:</strong> Index navigation utilizing leading key columns for direct tree probes.</li>
    <li><strong>Bitmap Index Scan Mechanics:</strong> Builds an in-memory page bitmap of matching tuple offsets, batching physical disk block visits.</li>
    <li><strong>B-Tree Skip Scan:</strong> Leverages PostgreSQL 18 capability to probe non-leading indexed attributes across distinct values of the leading column.</li>
  </ul>

  <h3 class="sub-sub-heading">3. Analytical Query Optimization &amp; Ranking Algorithms</h3>
  <ul>
    <li><strong>Correlated Subquery Evaluation:</strong> Aggregates maximum dish frequencies dynamically partitioned per restaurant.</li>
    <li><strong>Window Functions &amp; Deterministic Tie-Breaking:</strong>
      <ul>
        <li><code>RANK() OVER (PARTITION BY restaurant_id ORDER BY COUNT(*) DESC)</code> to identify tied popularity leaders.</li>
        <li><code>ROW_NUMBER() OVER (PARTITION BY restaurant_id ORDER BY COUNT(*) DESC, SUM(quantity) DESC)</code> to break ties deterministically by total volume of units sold.</li>
      </ul>
    </li>
    <li><strong>Multi-Table Relational Equi-Joins:</strong> Query trees connecting up to 7 relations simultaneously for comprehensive invoicing.</li>
  </ul>

  <h3 class="sub-sub-heading">4. Procedural Exception Handling &amp; Transaction Boundaries</h3>
  <ul>
    <li><strong>PL/pgSQL Trigger Pipeline:</strong> Intercepts tuple state before disk write, executing relational subqueries and raising fatal exceptions on business rule violations.</li>
    <li><strong>ACID Transaction Isolation:</strong> Comprehensive <code>BEGIN ... ROLLBACK</code> transaction blocks for isolated scalability benchmarking without catalog mutation.</li>
  </ul>

  <h2 class="sub-heading">Technology Stack Used for the Case</h2>
  <table>
    <thead>
      <tr>
        <th>Component</th>
        <th>Technology</th>
        <th>Description &amp; Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Database Engine</strong></td>
        <td>PostgreSQL 18.x</td>
        <td>Advanced open-source object-relational database management system.</td>
      </tr>
      <tr>
        <td><strong>Query Languages</strong></td>
        <td>SQL:2016, PL/pgSQL</td>
        <td>Declarative data definition, data manipulation, and procedural server-side logic.</td>
      </tr>
      <tr>
        <td><strong>Client &amp; Execution Tools</strong></td>
        <td><code>psql</code> CLI, <code>createdb</code>, <code>dropdb</code></td>
        <td>Native command-line interface for batch database creation, seeding, and execution.</td>
      </tr>
      <tr>
        <td><strong>Orchestration &amp; Automation</strong></td>
        <td>Bash / POSIX Shell (<code>run_all.sh</code>)</td>
        <td>Automated end-to-end script building database, running queries, and capturing outputs.</td>
      </tr>
      <tr>
        <td><strong>Environment</strong></td>
        <td>macOS, Antigravity IDE, VS Code</td>
        <td>Local development, debugging, and terminal automation environment.</td>
      </tr>
      <tr>
        <td><strong>Diagramming &amp; Modeling</strong></td>
        <td>Draw.io, SVG, PNG</td>
        <td>Crow's Foot and Chen notation entity-relationship architectural models.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- SECTION 5 -->
<div class="section">
  <h1 class="section-heading">5. Problem Statement / Case Study Implementation Details and Snapshots</h1>
  
  <p>
    The implementation is organized into six modular SQL scripts and an automated runner:
  </p>
  <ul>
    <li><code>01_schema.sql</code>: Table creation, constraints, procedural trigger, and views.</li>
    <li><code>02_indexes.sql</code>: Composite search index and foreign key indexes.</li>
    <li><code>03_seed_data.sql</code>: Realistic Mumbai/Navi Mumbai delivery ecosystem seed data.</li>
    <li><code>04_queries.sql</code>: 10 comprehensive business intelligence and operational queries.</li>
    <li><code>05_index_demo.sql</code>: 200,000-row scalability benchmark executed inside a transaction.</li>
    <li><code>06_integrity_tests.sql</code>: 9-point negative referential integrity test suite.</li>
    <li><code>run_all.sh</code>: Automated build, execution, and output capture pipeline.</li>
  </ul>

  <h2 class="sub-heading">Snapshot 1: Entity-Relationship Diagram (Crow's Foot Notation)</h2>
  <div class="diagram-container">
    <img src="data:image/png;base64,{er_b64}" class="diagram-img" alt="Crow's Foot ER Diagram">
    <div class="caption">Figure 1: QuickBite Entity-Relationship Model (Crow's Foot Notation)</div>
  </div>

  <h2 class="sub-heading">Snapshot 2: Database Schema &amp; Baseline Table Row Counts</h2>
  <pre>
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
  </pre>

  <h2 class="sub-heading">Snapshot 3: Procedural Trigger Implementation</h2>
  <pre>
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
  </pre>

  <h2 class="sub-heading">Snapshot 4: Query 1 &mdash; Most Frequently Ordered Dish per Restaurant (With Ties)</h2>
  <pre>
SELECT r.restaurant_id, r.name AS restaurant, m.name AS most_popular_dish,
       COUNT(*) AS times_ordered, SUM(oi.quantity) AS units_sold
FROM   order_item oi
JOIN   menu_item  m  ON m.menu_item_id  = oi.menu_item_id
JOIN   food_order fo ON fo.order_id     = oi.order_id
JOIN   restaurant r  ON r.restaurant_id = m.restaurant_id
WHERE  fo.status &lt;&gt; 'Cancelled'
GROUP  BY r.restaurant_id, r.name, m.menu_item_id, m.name
HAVING COUNT(*) = (SELECT MAX(dish_count)
                   FROM (SELECT COUNT(*) AS dish_count
                         FROM   order_item oi2
                         JOIN   menu_item  m2  ON m2.menu_item_id = oi2.menu_item_id
                         JOIN   food_order fo2 ON fo2.order_id    = oi2.order_id
                         WHERE  m2.restaurant_id = r.restaurant_id
                           AND  fo2.status &lt;&gt; 'Cancelled'
                         GROUP  BY oi2.menu_item_id) AS per_dish);
  </pre>
  <pre>
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
  </pre>

  <h2 class="sub-heading">Snapshot 5: Query 2 &mdash; Total Revenue Generated per Restaurant</h2>
  <pre>
SELECT r.restaurant_id, r.name AS restaurant, r.cuisine,
       COUNT(t.order_id) AS delivered_orders,
       COALESCE(SUM(t.order_total), 0) AS total_revenue,
       ROUND(COALESCE(AVG(t.order_total), 0), 2) AS avg_order_value
FROM   restaurant r
LEFT   JOIN v_order_total t ON t.restaurant_id = r.restaurant_id
                           AND t.status = 'Delivered'
GROUP  BY r.restaurant_id, r.name, r.cuisine
ORDER  BY total_revenue DESC;
  </pre>
  <pre>
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
  </pre>

  <h2 class="sub-heading">Snapshot 6: Query 3 &mdash; High-Speed Search by Cuisine &amp; Locality</h2>
  <pre>
SELECT restaurant_id, name, cuisine, location, rating
FROM   restaurant
WHERE  cuisine = 'North Indian' AND location = 'Kharghar'
ORDER  BY rating DESC;
  </pre>
  <pre>
 restaurant_id |          name          |   cuisine    | location | rating 
---------------+------------------------+--------------+----------+--------
             7 | Amritsari Kulcha House | North Indian | Kharghar |    4.5
             1 | Punjab Da Dhaba        | North Indian | Kharghar |    4.4
(2 rows)
  </pre>

  <h2 class="sub-heading">Snapshot 7: Query 9 &mdash; Full Itemized Order Invoice via 7-Table JOIN</h2>
  <pre>
 order_id |    ordered_at     |  customer  |   restaurant   | delivery_agent |        item         | quantity | unit_price | line_total | paid_via 
----------+-------------------+------------+----------------+----------------+---------------------+----------+------------+------------+----------
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Chicken Dum Biryani |        3 |     320.00 |     960.00 | UPI
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Chicken Seekh Kebab |        2 |     280.00 |     560.00 | UPI
       26 | 21-Sep-2026 20:45 | Aditya Rao | Biryani Darbar | Deepak Chauhan | Phirni              |        3 |     110.00 |     330.00 | UPI
(3 rows)
  </pre>

  <h2 class="sub-heading">Snapshot 8: Advanced Concept &mdash; Index Scalability Benchmark on 200,000 Rows</h2>
  <div class="callout">
    <div class="callout-title">Performance Benchmark Summary: 200,000 Synthetic Restaurants</div>
    Predicate: <code>WHERE cuisine = 'North Indian' AND location = 'Kharghar'</code>
  </div>
  <pre>
==== 1) WITHOUT INDEX: Parallel Seq Scan (Full Table Scan) ====
Gather (actual time=0.475..13.349 rows=835.00 loops=1)
  Workers Planned: 1, Workers Launched: 1
  Buffers: shared hit=2879
  -> Parallel Seq Scan on restaurant (actual time=0.036..9.085 rows=417.50 loops=2)
       Filter: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
       Rows Removed by Filter: 99588
Execution Time: 13.418 ms

==== 2) WITH COMPOSITE INDEX: Bitmap Index Scan ====
Bitmap Heap Scan on restaurant (actual time=0.182..1.010 rows=835.00 loops=1)
  Recheck Cond: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
  Heap Blocks: exact=834
  Buffers: shared hit=834 read=3
  -> Bitmap Index Scan on idx_restaurant_cuisine_location (actual time=0.098..0.098 rows=835.00 loops=1)
       Index Cond: (((cuisine)::text = 'North Indian'::text) AND ((location)::text = 'Kharghar'::text))
       Index Searches: 1
Execution Time: 1.058 ms (~13x FASTER)
  </pre>

  <h2 class="sub-heading">Snapshot 9: Referential Integrity Suite Execution (9/9 Passed)</h2>
  <pre>
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
  </pre>
</div>

<!-- SECTION 6 -->
<div class="section">
  <h1 class="section-heading">6. Problem Statement / Case Study Results and Conclusion</h1>
  
  <h2 class="sub-heading">Key Findings</h2>
  <ul>
    <li><strong>Normalized Relational Architecture (BCNF):</strong> Decomposing the unnormalized data into 7 normalized tables eliminated all partial and transitive dependencies. An address update modifies exactly one row, and onboarding new restaurants does not depend on immediate dish entry.</li>
    <li><strong>Empirical Index Acceleration:</strong> In our 200,000-restaurant dataset benchmark, the composite B-Tree index on <code>(cuisine, location)</code> accelerated query response time by <strong>~13&times; (from 13.42 ms to 1.05 ms)</strong> while reducing buffer reads by 71%, proving scalability under production workloads.</li>
    <li><strong>Preservation of 2NF via Triggers:</strong> Implementing procedural trigger logic in PL/pgSQL enabled enforcement of complex cross-restaurant integrity constraints without introducing redundant foreign keys into <code>order_item</code>.</li>
    <li><strong>Financial Reliability via Dynamic Views:</strong> Calculating order totals on the fly via <code>v_order_total</code> eliminated data drift and synchronization errors between line items and billing summaries.</li>
    <li><strong>Total Referential Integrity:</strong> All 9 deliberate corrupt write attempts were successfully rejected by PostgreSQL constraints and triggers, demonstrating 100% defense against orphan records and data anomalies.</li>
  </ul>

  <h2 class="sub-heading">Empirical Performance Comparison</h2>
  <table>
    <thead>
      <tr>
        <th>Execution Metric</th>
        <th>Without Index (Seq Scan)</th>
        <th>With Composite Index (Bitmap Index Scan)</th>
        <th>Performance Advantage</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Access Method</strong></td>
        <td>Parallel Sequential Scan across heap</td>
        <td>Bitmap Index Scan + Bitmap Heap Scan</td>
        <td>Targeted block lookup</td>
      </tr>
      <tr>
        <td><strong>Candidate Rows Scanned</strong></td>
        <td>200,011 rows (199,176 filtered out)</td>
        <td>835 rows (exact candidate matches)</td>
        <td>~240&times; reduction in examined rows</td>
      </tr>
      <tr>
        <td><strong>Shared Buffers Read</strong></td>
        <td>2,879 blocks</td>
        <td>837 blocks</td>
        <td>3.4&times; reduction in I/O demand</td>
      </tr>
      <tr>
        <td><strong>Query Execution Time</strong></td>
        <td><strong>13.418 ms</strong></td>
        <td><strong>1.058 ms</strong></td>
        <td><strong>~12.7&times; (~13&times; speedup)</strong></td>
      </tr>
    </tbody>
  </table>

  <h2 class="sub-heading">Conclusion</h2>
  <p>
    This case study successfully engineered, implemented, and validated the <strong>QuickBite Food Delivery Order &amp; Restaurant Management System</strong> on PostgreSQL 18. All core project deliverables for Case Study #83 were accomplished with zero compromises in relational purity, referential integrity, or analytical capability.
  </p>
  <p>
    The system proves that sound relational theory &mdash; when combined with modern database indexing and procedural logic &mdash; provides an ultra-reliable foundation capable of powering modern high-velocity delivery applications.
  </p>

  <h2 class="sub-heading">Future Enhancements</h2>
  <ul>
    <li><strong>Geospatial Distance Routing (PostGIS):</strong> Integrating spatial extensions (<code>ST_DWithin</code>, <code>ST_Distance</code>) to calculate real-time delivery radiuses and rider-to-restaurant dispatch routes.</li>
    <li><strong>Declarative Range Partitioning:</strong> Implementing PostgreSQL declarative partitioning on <code>food_order</code> by monthly ranges to maintain query speed over years of transaction history.</li>
    <li><strong>Materialized Reporting Views &amp; Redis Caching:</strong> Using concurrently refreshed materialized views for heavy executive analytics, combined with Redis in-memory caches for top-level menu browsing.</li>
  </ul>
</div>

<!-- SECTION 7 -->
<div class="section">
  <h1 class="section-heading">7. References</h1>
  <ol>
    <li><strong>Silberschatz, A., Korth, H. F., &amp; Sudarshan, S.</strong> (2020). <em>Database System Concepts</em> (7th ed.). McGraw-Hill Education.</li>
    <li><strong>Elmasri, R., &amp; Navathe, S. B.</strong> (2016). <em>Fundamentals of Database Systems</em> (7th ed.). Pearson.</li>
    <li><strong>Date, C. J.</strong> (2004). <em>An Introduction to Database Systems</em> (8th ed.). Addison-Wesley.</li>
    <li><strong>PostgreSQL Global Development Group.</strong> (2024). <em>PostgreSQL 18 Documentation: B-Tree Indexing, Concurrency Control, and Triggers</em>. Available online: https://www.postgresql.org/docs/</li>
    <li><strong>Codd, E. F.</strong> (1970). <em>A Relational Model of Data for Large Shared Data Banks</em>. Communications of the ACM, 13(6), 377&ndash;387.</li>
    <li><strong>Codd, E. F.</strong> (1974). <em>Recent Investigations in Relational Data Base Systems</em>. IFIP Congress, 1017&ndash;1021.</li>
    <li><strong>School of Future Tech, ITM Skills University.</strong> (2025). <em>Database Management Systems Course Curriculum &amp; Case Study Specifications (Case Study #83)</em>.</li>
  </ol>
</div>

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Wrote {html_path}")

    cmd = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"Generated {pdf_path} ({size} bytes)")
        with open(pdf_path, 'rb') as f_in, open(root_pdf_path, 'wb') as f_out:
            f_out.write(f_in.read())
        print(f"Copied to {root_pdf_path}")
    else:
        print("Failed to generate PDF:", res.stderr)

if __name__ == '__main__':
    main()
