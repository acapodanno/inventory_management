Project Python for course AI Solution Architect

At the level of functional and non-functional requirements, the project must provide the following main features:

Main Functionalities (Functional Requirements)
1. New Order Registration

Entry of orders containing: customer identifier, list of products (product code, requested quantity), date, and priority.

Verification of availability status at the time of registration (available / partially available / unavailable).

2. Inventory Update

Reduction of stock levels upon order fulfillment.

Management of negative stock or partial orders as separate states (e.g. “partial”, “pending”).

3. Real-Time Inventory Status Consultation

Display of product list with current stock level, reorder point, and unit of measure.

Search filters by product code, category, or stock threshold.

4. Daily Report Generation

Daily summary report containing: number of orders received, fulfilled orders, pending orders, best-selling products, stock level variations.

Export of the report in a readable format (e.g. text file or CSV) for internal sharing.

5. Data Persistence (High-Level Requirement)

Ability to load and save inventory status and order lists to data files (standard formats such as CSV or JSON), so that the system can be restarted while preserving its state.

6. Traceability and Logging

Tracking of main operations (e.g. order registration, fulfillment, inventory changes) with timestamp and operator information.

---------------------------------------------------------------------------------------------------------------------------------

Create a Virtual Enviroment:

- python -m venv venv  

Active Virtual Enviroment:

- venv\Scripts\Activate

Install dependency:

- pip install -r .\requirements.txt

Start software:

- python app.py



