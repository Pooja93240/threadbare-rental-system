#Module updated by Juhi
# Rental module created by Juhi
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Threadbare | Leases & Bookings",
    page_icon="🌿",
    layout="wide"
)

# --- BACKEND CONNECTION ---
@st.cache_resource
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["rental_system"]

db = get_db()
rentals_col = db["rentals"]      
inventory_col = db["inventory"]  

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
            .badge-active { background-color: #D1FAE5; color: #065F46; }
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
        </style>
    """, unsafe_allow_html=True)

def show_rentals_app():
    apply_custom_css()

    # --- HERO HEADER SECTION ---
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">Threadbare Reservations</div>
            <div class="hero-subtitle">Customer Concierge & Active Rental Tracking Portal</div>
            <div class="perks-bar">
                ✨ INSTANT LEASING &nbsp;|&nbsp; 🔄 EASY EXTENSIONS &nbsp;|&nbsp; 🛡️ VERIFIED CLIENT DIRECTORY
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- METRICS DASHBOARD ---
    total_leases = rentals_col.count_documents({})
    active_leases = rentals_col.count_documents({"rental_status": "Active"})

    m1, m2 = st.columns(2)
    m1.metric("Total Executed Leases", total_leases)
    m2.metric("Currently Out on Lease", active_leases)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- NAVIGATION TABS ---
    tab_issue, tab_directory = st.tabs([
        "➕ Issue New Lease",
        "📋 Active Leases Directory"
    ])

    # --- TAB 1: ISSUE RENTAL FORM ---
    with tab_issue:
        st.subheader("Issue New Apparel Lease")
        st.caption("Assign a wardrobe piece to a verified customer and track rental duration.")

        with st.form("issue_rental_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                rental_id = st.text_input("Lease Reference ID", value="RNT-501")
                customer_name = st.text_input("Customer Name", placeholder="e.g. Sophia Montgomery")
                customer_phone = st.text_input("Customer Phone", placeholder="+1 (555) 019-2834")
            with col2:
                item_id_str = st.text_input("Inventory MongoDB ID", placeholder="Paste 24-character hex ID...")
                rental_days = st.number_input("Lease Duration (Days)", min_value=1, value=3, step=1)

            submit_btn = st.form_submit_button("✨ Confirm & Issue Lease", type="primary")

        # --- BACKEND LOGIC: ISSUE RENTAL & FLIP STATUS ---
        if submit_btn:
            if not item_id_str.strip() or not customer_name.strip():
                st.error("Please complete all required details before issuing.")
            else:
                try:
                    item_obj_id = ObjectId(item_id_str.strip())
                    # Check if item exists in Inventory
                    item = inventory_col.find_one({"_id": item_obj_id})

                    if not item:
                        st.error("Item ID not found in the inventory collection!")
                    elif item.get("status") == "Rented":
                        st.warning(f"'{item.get('item_name', 'This item')}' is currently rented out to another client!")
                    else:
                        start_date = datetime.now()
                        due_date = start_date + timedelta(days=int(rental_days))

                        # 1. Create Rental Document in 'rentals' collection
                        new_rental = {
                            "rental_id": rental_id.strip(),
                            "customer_name": customer_name.strip(),
                            "customer_phone": customer_phone.strip(),
                            "item_id": item_obj_id,
                            "rental_days": int(rental_days),
                            "start_date": start_date,
                            "return_due_date": due_date,
                            "rental_status": "Active"
                        }
                        rentals_col.insert_one(new_rental)

                        # 2. Trigger Status Change in 'inventory' collection
                        inventory_col.update_one(
                            {"_id": item_obj_id},
                            {"$set": {"status": "Rented"}}
                        )

                        st.success(f"Lease {rental_id} executed successfully! Inventory status changed to 'Rented'.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Invalid ObjectId format or error occurred: {e}")

    # --- TAB 2: ACTIVE RENTALS DIRECTORY ---
    with tab_directory:
        st.subheader("Current Active Leases")
        active_rentals = list(rentals_col.find())

        if not active_rentals:
            st.info("No active customer leases found.")
        else:
            st.caption(f"Managing **{len(active_rentals)}** active lease agreement(s)")
            for rental in active_rentals:
                r_id = rental["_id"]
                due_date_str = rental.get('return_due_date').strftime('%B %d, %Y') if rental.get('return_due_date') else 'N/A'
                
                with st.expander(f"✨ {rental.get('rental_id')} — Client: {rental.get('customer_name')}"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**Customer Phone:** {rental.get('customer_phone', 'N/A')}")
                        st.markdown(f"**Duration:** {rental.get('rental_days')} Days")
                        st.markdown(f"**Return Due Date:** `{due_date_str}`")
                        st.markdown(f"**Lease Status:** <span class='badge badge-active'>{rental.get('rental_status', 'Active')}</span>", unsafe_allow_html=True)
                    with col_b:
                        st.caption("Linked Inventory Item ID:")
                        st.code(str(rental.get('item_id')), language="text")

                    st.divider()

                    col_ext, col_can = st.columns(2)
                    
                    # BACKEND UPDATE: Extend rental
                    with col_ext:
                        if st.button("➕ Extend Lease (+1 Day)", key=f"ext_{r_id}"):
                            new_due = rental.get("return_due_date") + timedelta(days=1)
                            rentals_col.update_one(
                                {"_id": r_id},
                                {"$set": {
                                    "rental_days": rental.get("rental_days", 0) + 1,
                                    "return_due_date": new_due
                                }}
                            )
                            st.success("Lease extended by 1 day!")
                            st.rerun()

                    # BACKEND DELETE: Cancel rental & revert inventory status
                    with col_can:
                        if st.button("🔴 Cancel & Return Asset", key=f"del_{r_id}", type="primary"):
                            inventory_col.update_one(
                                {"_id": rental.get("item_id")},
                                {"$set": {"status": "Available"}}
                            )
                            rentals_col.delete_one({"_id": r_id})
                            st.warning("Booking closed & item marked as 'Available' in catalog!")
                            st.rerun()

if __name__ == "__main__":
    show_rentals_app()
