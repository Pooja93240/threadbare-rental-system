import certifi
import os
import streamlit as st
from pymongo import MongoClient




# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Threadbare | Luxury Fashion Portal",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MASTER STAFF CREDENTIALS (HIDDEN / UNKNOWN TO CUSTOMERS) ---
STAFF_USERNAME = "admin"
STAFF_PASSWORD = "threadbare2026"

# --- BACKEND CONNECTION ---
# --- BACKEND CONNECTION ---
@st.cache_resource
@st.cache_resource
def get_db():
    if "MONGO_URI" in st.secrets:
        mongo_uri = st.secrets["MONGO_URI"]
    elif "MONGO_URI" in os.environ:
        mongo_uri = os.environ["MONGO_URI"]
    else:
        mongo_uri = "mongodb+srv://Pooja:db_Poojapihu2912@cluster0.z9x64ww.mongodb.net/?retryWrites=true&w=majority"

    # Explicitly pass tls=True along with certifi CA bundle
    client = MongoClient(
        mongo_uri, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000
    )
    return client["rental_system"]

db = get_db()
inventory_col = db["inventory"]
rentals_col = db["rentals"]
billing_col = db["billing"]
users_col = db["users"]  # Customer accounts database

# --- GLOBAL STYLING & THEMING ---
def apply_custom_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', sans-serif;
            }

            .main {
                background-color: #F4F7F5;
            }

            .hero-header {
                background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #10B981 100%);
                padding: 2.5rem 2rem;
                border-radius: 18px;
                color: #FFFFFF;
                box-shadow: 0 12px 28px -5px rgba(6, 78, 59, 0.25);
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

            .badge {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-transform: uppercase;
                display: inline-block;
            }
            .badge-available, .badge-active, .badge-paid { 
                background-color: #D1FAE5; color: #065F46; 
            }
            .badge-rented, .badge-pending { 
                background-color: #FEF3C7; color: #92400E; 
            }
            .badge-maintenance { 
                background-color: #FEE2E2; color: #991B1B; 
            }

            .stButton > button[kind="primary"] {
                background-color: #064E3B !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                padding: 0.5rem 1.5rem !important;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #047857 !important;
                box-shadow: 0 4px 12px rgba(4, 120, 87, 0.3);
            }

            .dress-card {
                background-color: #FFFFFF;
                border: 1px solid #A7F3D0;
                border-radius: 14px;
                padding: 20px;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 12px rgba(6, 78, 59, 0.05);
            }

            section[data-testid="stSidebar"] {
                background-color: #064E3B;
            }
            section[data-testid="stSidebar"] * {
                color: #FFFFFF !important;
            }
        </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "is_staff" not in st.session_state:
    st.session_state["is_staff"] = False

# --- UNIFIED AUTHENTICATION LANDING PAGE ---
def show_auth_page():
    st.markdown("""
        <div class="hero-header" style="text-align: center;">
            <div class="hero-title">Threadbare Luxury Wardrobes</div>
            <div class="hero-subtitle">High-End Fashion & Designer Dress Rental Platform</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        auth_tab1, auth_tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])

        # --- SINGLE UNIFIED SIGN IN ---
        with auth_tab1:
            st.subheader("Member Sign In")
            with st.form("unified_login_form"):
                user_input = st.text_input("Username", placeholder="e.g. sophia_m")
                pass_input = st.text_input("Password", type="password")
                login_btn = st.form_submit_button("Sign In to Portal", type="primary")

            if login_btn:
                u_str = user_input.strip()
                p_str = pass_input.strip()

                if not u_str or not p_str:
                    st.error("Please fill in all fields.")
                # 1. SECRET STAFF CHECK (AUTOMATIC REDIRECT TO ADMIN PANEL)
                elif u_str == STAFF_USERNAME and p_str == STAFF_PASSWORD:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = "System Admin (Staff)"
                    st.session_state["is_staff"] = True
                    st.success("Welcome back!")
                    st.rerun()
                # 2. STANDARD CUSTOMER CHECK
                else:
                    found_user = users_col.find_one({"username": u_str, "password": p_str})
                    if found_user:
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = u_str
                        st.session_state["is_staff"] = False
                        st.success(f"Welcome back, {u_str}!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        # --- CUSTOMER REGISTRATION ---
        with auth_tab2:
            st.subheader("Register Account")
            with st.form("unified_reg_form"):
                new_user = st.text_input("Choose Username")
                new_pass = st.text_input("Choose Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                reg_btn = st.form_submit_button("Register Account", type="primary")

            if reg_btn:
                if not new_user.strip() or not new_pass.strip():
                    st.error("All fields are required.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    if users_col.find_one({"username": new_user.strip()}):
                        st.warning("Username already taken.")
                    else:
                        users_col.insert_one({"username": new_user.strip(), "password": new_pass.strip()})
                        st.success("Account successfully created! Please sign in.")

# --- CUSTOMER INTERFACE (BROWSE, PAY & RENT) ---
def show_customer_dashboard():
    st.markdown(f"""
        <div class="hero-header">
            <div class="hero-title">Designer Dress Collection</div>
            <div class="hero-subtitle">Welcome, {st.session_state['username']} — Select, Rent & Reserve Your Outfit</div>
        </div>
    """, unsafe_allow_html=True)

    c_tab1, c_tab2 = st.tabs(["👗 Select & Rent Outfits", "📜 My Active Rentals"])

    with c_tab1:
        search = st.text_input("🔍 Search Outfits", placeholder="Search by dress name or style...")
        query = {"status": "Available"}
        if search.strip():
            query["$or"] = [
                {"item_name": {"$regex": search.strip(), "$options": "i"}},
                {"category": {"$regex": search.strip(), "$options": "i"}}
            ]

        available_dresses = list(inventory_col.find(query))

        if not available_dresses:
            st.info("No outfits currently available for rental.")
        else:
            for dress in available_dresses:
                d_id = dress["_id"]
                rate = dress.get("daily_rate", 0.0)

                st.markdown(f"""
                    <div class="dress-card">
                        <h3 style="margin:0; color:#064E3B; font-family:'Playfair Display', serif;">{dress.get('item_name')}</h3>
                        <p style="color:#047857; margin-top:2px; font-weight:600;">Category: {dress.get('category', 'Evening Wear')}</p>
                        <p style="font-size:1.2rem; font-weight:700; color:#064E3B;">Rate: ${rate:.2f} / day</p>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander(f"✨ Reserve '{dress.get('item_name')}'"):
                    with st.form(key=f"rent_form_{d_id}"):
                        days = st.number_input("How many days do you want to rent?", min_value=1, value=3, key=f"days_{d_id}")
                        phone = st.text_input("Contact Phone Number", placeholder="+1 (555) 000-1122", key=f"phone_{d_id}")
                        
                        total_cost = days * rate
                        st.markdown(f"#### **Total Payment Due: ${total_cost:.2f}**")
                        
                        confirm_rent = st.form_submit_button("💳 Pay & Rent Outfit", type="primary")

                    if confirm_rent:
                        if not phone.strip():
                            st.error("Please enter a valid contact phone number.")
                        else:
                            start_date = datetime.now()
                            due_date = start_date + timedelta(days=int(days))
                            r_ref = f"RNT-{datetime.now().strftime('%M%S')}"

                            # 1. Add record to rentals collection
                            rentals_col.insert_one({
                                "rental_id": r_ref,
                                "customer_name": st.session_state["username"],
                                "customer_phone": phone.strip(),
                                "item_id": d_id,
                                "rental_days": int(days),
                                "start_date": start_date,
                                "return_due_date": due_date,
                                "rental_status": "Active"
                            })

                            # 2. Update status in inventory collection
                            inventory_col.update_one({"_id": d_id}, {"$set": {"status": "Rented"}})

                            # 3. Add paid transaction to billing collection
                            billing_col.insert_one({
                                "bill_id": f"INV-{r_ref}",
                                "rental_id": r_ref,
                                "customer_name": st.session_state["username"],
                                "item_name": dress.get("item_name"),
                                "total_amount": total_cost,
                                "payment_status": "Paid"
                            })

                            st.success(f"Payment successful! Outfit reserved under Reference #{r_ref}")
                            st.rerun()

    with c_tab2:
        st.subheader("Your Rental History & Reservations")
        my_rentals = list(rentals_col.find({"customer_name": st.session_state["username"]}))
        if not my_rentals:
            st.info("You haven't rented any dresses yet.")
        else:
            for r in my_rentals:
                item = inventory_col.find_one({"_id": r.get("item_id")})
                item_name = item.get("item_name") if item else "Luxury Dress"
                st.write(f"🧾 **Lease #{r.get('rental_id')}** | Dress: **{item_name}** | Duration: {r.get('rental_days')} Days | Status: `{r.get('rental_status')}`")

# --- SECRET STAFF INTERFACE (FULL CONTROLS) ---
def show_staff_dashboard():
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">Staff Administration Control</div>
            <div class="hero-subtitle">Inventory Management, Add/Delete Outfits & Active Lease Control</div>
        </div>
    """, unsafe_allow_html=True)

    s_tab1, s_tab2, s_tab3 = st.tabs(["👗 Add/Delete/Edit Dresses", "📋 All Active Leases", "💳 Revenue & Invoices"])

    # --- STAFF TAB 1: ADD / DELETE DRESSES ---
    with s_tab1:
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("➕ Add New Dress to Store")
            with st.form("add_dress_form", clear_on_submit=True):
                d_name = st.text_input("Dress Name / Title", placeholder="e.g. Silk Emerald Gown")
                d_cat = st.text_input("Style / Category", placeholder="e.g. Formal Gowns")
                d_rate = st.number_input("Daily Rental Rate ($)", min_value=1.0, value=85.0)
                submit_add = st.form_submit_button("Add Outfit to Store", type="primary")

            if submit_add and d_name.strip():
                inventory_col.insert_one({
                    "item_name": d_name.strip(),
                    "category": d_cat.strip(),
                    "daily_rate": float(d_rate),
                    "status": "Available"
                })
                st.success(f"'{d_name}' added to inventory!")
                st.rerun()

        with col_right:
            st.subheader("🗑️ Delete Outfit from Inventory")
            all_items = list(inventory_col.find())
            if all_items:
                item_map = {f"{i['item_name']} (Status: {i.get('status')})": i["_id"] for i in all_items}
                selected_del = st.selectbox("Select Outfit to Remove", list(item_map.keys()))
                if st.button("Delete Dress Permanently", type="primary"):
                    inventory_col.delete_one({"_id": item_map[selected_del]})
                    st.success("Dress removed from inventory.")
                    st.rerun()
            else:
                st.info("No items in inventory to delete.")

        st.divider()
        st.subheader("Current Full Store Inventory")
        items = list(inventory_col.find())
        for i in items:
            st.write(f"✨ **{i.get('item_name')}** | Category: {i.get('category')} | Rate: **${i.get('daily_rate'):.2f}/day** | Status: `{i.get('status')}`")

    # --- STAFF TAB 2: ACTIVE LEASES ---
    with s_tab2:
        st.subheader("Master Lease Directory")
        active = list(rentals_col.find({"rental_status": "Active"}))
        if not active:
            st.info("No active leases currently outstanding.")
        else:
            for rental in active:
                rec_id = rental["_id"]
                with st.expander(f"✨ Lease #{rental.get('rental_id')} — Client: {rental.get('customer_name')}"):
                    st.write(f"**Contact Phone:** {rental.get('customer_phone')}")
                    st.write(f"**Lease Duration:** {rental.get('rental_days')} Days")
                    if st.button("Mark Item as Returned / Restock", key=f"ret_{rec_id}", type="primary"):
                        inventory_col.update_one({"_id": rental.get("item_id")}, {"$set": {"status": "Available"}})
                        rentals_col.update_one({"_id": rec_id}, {"$set": {"rental_status": "Returned"}})
                        st.success("Item restocked and available for rent!")
                        st.rerun()

    # --- STAFF TAB 3: INVOICES ---
    with s_tab3:
        st.subheader("Completed Payment Records")
        bills = list(billing_col.find())
        if not bills:
            st.info("No payment history.")
        else:
            for b in bills:
                st.write(f"🧾 **Invoice #{b.get('bill_id')}** | Client: {b.get('customer_name')} | Outfit: {b.get('item_name')} | **Amount Settled: ${b.get('total_amount', 0.0):.2f}**")

# --- MAIN CONTROLLER ---
def main():
    apply_custom_css()

    if not st.session_state["authenticated"]:
        show_auth_page()
    else:
        with st.sidebar:
            st.markdown("## 🌿 Threadbare Portal")
            st.caption(f"User: **{st.session_state['username']}**")
            
            if st.session_state["is_staff"]:
                st.markdown("<span class='badge badge-pending'>STAFF ADMIN MODE</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='badge badge-available'>CUSTOMER ACCOUNT</span>", unsafe_allow_html=True)

            st.divider()
            if st.button("🚪 Sign Out"):
                st.session_state["authenticated"] = False
                st.session_state["username"] = ""
                st.session_state["is_staff"] = False
                st.rerun()

        if st.session_state["is_staff"]:
            show_staff_dashboard()
        else:
            show_customer_dashboard()

if __name__ == "__main__":
    main()
