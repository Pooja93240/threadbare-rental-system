# Billing module created by Arpita
from datetime import datetime
import streamlit as st
from pymongo import MongoClient
# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Threadbare | Billing & Payments",
    page_icon="🌿",
    layout="wide"
)

# --- BACKEND CONNECTION ---
# --- BACKEND CONNECTION ---
@st.cache_resource

def get_db():
    mongo_uri = "mongodb://localhost:27017"
    client = MongoClient(mongo_uri)
    return client["threadbare_db"]

db = get_db()
# You can now reference collections using db, e.g.:
# billing_col = db["billing"]
rentals_col = db["rentals"]      
inventory_col = db["inventory"]  
billing_col = db["billing"]      

def apply_custom_css():
    st.markdown("""
        <style>
            /* Import Luxury Serif Font */
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;600&display=swap');

            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', sans-serif;
            }

            /* Main Background */
            .main {
                background-color: #F4F7F5;
            }

            /* Hero Header */
            .hero-header {
                background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #10B981 100%);
                padding: 2.5rem 2rem;
                border-radius: 16px;
                color: #FFFFFF;
                box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
                margin-bottom: 2rem;
            }
            .hero-title {
                font-family: 'Playfair Display', serif;
                font-size: 2.5rem;
                font-weight: 700;
                letter-spacing: -0.5px;
                margin-bottom: 0.3rem;
            }
            .hero-subtitle {
                font-size: 1.05rem;
                color: #A7F3D0;
                font-weight: 300;
            }

            /* Perks Floating Bar */
            .perks-bar {
                background-color: #ECFDF5;
                border: 1px solid #A7F3D0;
                padding: 10px 20px;
                border-radius: 30px;
                text-align: center;
                font-size: 0.85rem;
                font-weight: 600;
                color: #065F46;
                margin-top: 1rem;
            }

            /* Custom Emerald Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 12px;
                background-color: transparent;
            }
            .stTabs [data-baseweb="tab"] {
                height: 48px;
                border-radius: 8px;
                background-color: #FFFFFF;
                color: #064E3B;
                font-weight: 600;
                border: 1px solid #E2E8F0;
                padding: 0px 20px;
            }
            .stTabs [aria-selected="true"] {
                background-color: #064E3B !important;
                color: #FFFFFF !important;
                border-color: #064E3B !important;
            }

            /* Metric Cards */
            [data-testid="stMetricValue"] {
                color: #064E3B !important;
                font-family: 'Playfair Display', serif;
                font-size: 2.2rem !important;
            }

            /* Status Badges */
            .badge {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                display: inline-block;
            }
            .badge-paid { background-color: #D1FAE5; color: #065F46; }
            .badge-pending { background-color: #FEF3C7; color: #92400E; }

            /* Primary Emerald Buttons */
            .stButton > button[kind="primary"] {
                background-color: #064E3B !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.5rem !important;
                transition: all 0.2s ease;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #047857 !important;
                box-shadow: 0 4px 12px rgba(4, 120, 87, 0.3);
            }

            /* Invoice Summary Card */
            .invoice-card {
                background-color: #FFFFFF;
                border: 1px solid #A7F3D0;
                border-radius: 12px;
                padding: 24px;
                margin-top: 1rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 12px rgba(6, 78, 59, 0.05);
            }
            .invoice-amount {
                font-family: 'Playfair Display', serif;
                font-size: 1.8rem;
                font-weight: 700;
                color: #064E3B;
            }
        </style>
    """, unsafe_allow_html=True)

def show_billing_app():
    apply_custom_css()

    # --- HERO HEADER SECTION ---
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">Threadbare Financials</div>
            <div class="hero-subtitle">Billing, Checkout & Payment Concierge</div>
            <div class="perks-bar">
                💳 AUTOMATED INVOICING &nbsp;|&nbsp; 🔄 INSTANT INVENTORY REPLACEMENT &nbsp;|&nbsp; 🛡️ SECURE TRANSACTION LOGS
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- METRICS OVERVIEW ---
    total_bills = billing_col.count_documents({})
    all_bills = list(billing_col.find())
    total_revenue = sum(b.get("total_amount", 0.0) for b in all_bills)

    m1, m2 = st.columns(2)
    m1.metric("Invoices Settled", total_bills)
    m2.metric("Total Revenue Generated", f"${total_revenue:,.2f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- NAVIGATION TABS ---
    tab_checkout, tab_history = st.tabs([
        "💳 Generate Invoice & Return Asset",
        "🧾 Transaction History"
    ])

    # --- TAB 1: INVOICE GENERATION & RETURN ---
    with tab_checkout:
        st.subheader("Process Return & Settlement")
        st.caption("Select an active customer lease to preview billing details, process payment, and restock the item.")

        # Fetch active rentals from rentals collection
        active_rentals = list(rentals_col.find({"rental_status": "Active"}))

        if not active_rentals:
            st.info("No active leases currently require settlement.")
        else:
            # Dropdown options formatted cleanly
            rental_options = {f"{r['rental_id']} — {r['customer_name']}": r for r in active_rentals}
            selected_option = st.selectbox("Select Active Lease Agreement", list(rental_options.keys()))
            selected_rental = rental_options[selected_option]

            # Fetch linked item details from inventory collection
            item_id = selected_rental.get("item_id")
            item = inventory_col.find_one({"_id": item_id})

            if item:
                daily_rate = item.get("daily_rate", 0.0)
                rental_days = selected_rental.get("rental_days", 1)
                total_amount = daily_rate * rental_days

                # --- DISPLAY INVOICE CARD ---
                st.markdown(f"""
                    <div class="invoice-card">
                        <h4 style="margin-top:0; color:#064E3B; font-family:'Playfair Display', serif;">Invoice Preview — INV-{selected_rental.get('rental_id')}</h4>
                        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 12px 0;">
                        <p><strong>Customer Name:</strong> {selected_rental.get('customer_name')}</p>
                        <p><strong>Apparel Item:</strong> {item.get('item_name')}</p>
                        <p><strong>Daily Rental Rate:</strong> ${daily_rate:.2f} / day</p>
                        <p><strong>Lease Duration:</strong> {rental_days} day(s)</p>
                        <div class="invoice-amount" style="margin-top: 15px;">
                            Total Due: ${total_amount:.2f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                # --- PROCESS PAYMENT & RETURN ---
                if st.button("✨ Process Payment & Restock Item", type="primary"):
                    # 1. Create billing record
                    bill_record = {
                        "bill_id": f"INV-{selected_rental.get('rental_id')}",
                        "rental_id": selected_rental.get("rental_id"),
                        "customer_name": selected_rental.get("customer_name"),
                        "item_name": item.get("item_name"),
                        "total_amount": total_amount,
                        "payment_status": "Paid"
                    }
                    billing_col.insert_one(bill_record)

                    # 2. Update rental status
                    rentals_col.update_one(
                        {"_id": selected_rental["_id"]},
                        {"$set": {"rental_status": "Returned"}}
                    )

                    # 3. Revert inventory item status back to 'Available'
                    inventory_col.update_one(
                        {"_id": item_id},
                        {"$set": {"status": "Available"}}
                    )

                    st.success("Payment settled! Invoice recorded and apparel returned to catalog.")
                    st.rerun()

    # --- TAB 2: TRANSACTION HISTORY ---
    with tab_history:
        st.subheader("Completed Transactions")
        bills = list(billing_col.find())

        if not bills:
            st.info("No transaction history available.")
        else:
            st.caption(f"Showing **{len(bills)}** completed transaction(s)")
            for bill in bills:
                with st.expander(f"🧾 {bill.get('bill_id')} — Client: {bill.get('customer_name')}"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**Apparel Piece:** {bill.get('item_name')}")
                        st.markdown(f"**Lease Reference:** `{bill.get('rental_id')}`")
                        st.markdown(f"**Amount Paid:** `${bill.get('total_amount', 0.0):.2f}`")
                    with col_b:
                        st.markdown("**Payment Status:** <span class='badge badge-paid'>Paid</span>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_billing_app()
