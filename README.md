## 💻 System Configuration & Technical Specifications

## Software & Environment Setup
- **Programming Language:** Python 3.13
- **IDE / Text Editor:** Python IDLE
- **Database Engine:** MongoDB Community Server (for Local) / MongoDB Atlas (Cloud)
- **Database Management Tool:** MongoDB Compass
- **Web App Framework:** Streamlit
- **Database Driver:** PyMongo
- **Version Control:** Git & GitHub (Collaborative Remote Repository)

## 🛠️ Complete Tech Stack

| Layer | Technology | Usage |
| :--- | :--- | :--- |
| *Frontend UI* | *Streamlit + CSS3* | Custom responsive dashboard, navigation tabs, metrics widgets, and luxury styling |
| *Backend & Logic* | *Python* | Cross-module data fetching, fee calculations, and transaction orchestration |
| *Database* | *MongoDB (NoSQL)* | Dynamic BSON document storage across 3 interconnected collections |
| *DB Driver* | *PyMongo* | Establishing connection strings, executing queries, updates, and inserts |


## 👥 Team Workload Division & Member Contributions

### 📦 Pooja_467 Member 1: Inventory & Asset Manager
- **Collection Handled:** `inventory`
- **Frontend Responsibilities:** Built the **Inventory Catalog & Management Screen** allowing staff to input, view, and organize physical fashion assets.
- **Backend Responsibilities:**
  - Designed the document schema for clothing items (Title, Category, Size, Color, Daily Rate, and Availability Status).
  - Implemented core CRUD operations to **Add** new stock, **Update** apparel pricing/sizing, and **Delete** damaged/retired garments.
  - Managed stock status transitions (`Available`and `Rented`).

### 📋 Juhi_458 Member 2: Rentals & Active Leases Tracker
- **Collection Handled:** `rentals`
- **Frontend Responsibilities:** Created the **Lease Agreement Booking Interface** and active rentals directory for tracking dispatched items.
- **Backend Responsibilities:**
  - Designed the document schema for rental orders (`rental_id`, `customer_name`, `item_id`, `rental_days`, `rental_status`).
  - Executed **Transaction #1 (Lease Issuance):** Programmed logic to create a new rental agreement while automatically triggering an update in Member 1's    `inventory` collection to switch item status from `"Available"` to `"Rented"`.
  - Maintained records for active customer leases and return timelines.

### 💳 Arpita_462 Member 3: Billing, Payments & Checkout Manager
- **Collection Handled:** `billing`
- **Frontend Responsibilities:** Designed the **Financial Dashboard**, dynamic invoice preview cards, live metric summary boxes (Invoices Settled & Total Revenue), and the completed transaction history tab.
- **Backend Responsibilities:**
  - Designed the invoice document schema (`bill_id`, `rental_id`, `customer_name`, `item_name`, `total_amount`, `payment_status`).
  - Executed **Transaction #2 (Settlement & Restock):** Calculated total amount due ($Total = Daily\ Rate \times Days$), generated invoice records in `billing`, updated lease status in `rentals` to `"Returned"`, and reverted item status in `inventory` back to `"Available"`.
 
## 📸 Application Screenshots
Dashboard for Register
<img width="1917" height="1015" alt="image" src="https://github.com/user-attachments/assets/327f9022-6d00-4a9c-8b12-f0d802f3e166" />
Login page
<img width="1907" height="1011" alt="image" src="https://github.com/user-attachments/assets/8a0440f6-b162-460a-b549-06ec9206fdf2" />
Staff Page
<img width="1915" height="1018" alt="image" src="https://github.com/user-attachments/assets/d38ac60b-7b59-449c-8311-73c740d32a32" />
<img width="1917" height="993" alt="image" src="https://github.com/user-attachments/assets/14c767b6-f2b7-4bc1-aa6c-e3ecbac724ff" />
<img width="1912" height="927" alt="image" src="https://github.com/user-attachments/assets/84b52563-666e-4ad6-bd54-b101d93ba054" />
Customer page
<img width="1917" height="970" alt="image" src="https://github.com/user-attachments/assets/4690b449-4d31-4a10-8c0c-8c9226be7fae" />
<img width="1917" height="975" alt="image" src="https://github.com/user-attachments/assets/3e89ac43-223e-4352-87d2-375398e5acc3" />
