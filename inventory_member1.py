import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Threadbare | Emerald Vault",
    page_icon="🌿",
    layout="wide"
)

# --- BACKEND CONNECTION ---
@st.cache_resource
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    return client["rental_system"]

db = get_db()
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

            /* Hero Banner */
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
            .badge-available { background-color: #D1FAE5; color: #065F46; }
            .badge-rented { background-color: #FEF3C7; color: #92400E; }
            .badge-maintenance { background-color: #FEE2E2; color: #991B1B; }

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

def show_inventory_app():
    apply_custom_css()

    # --- HERO HEADER SECTION ---
    st.markdown("""
        <div class="hero-header">
            <div class="hero-title">Threadbare Wardrobe</div>
            <div class="hero-subtitle">Experience the Best of Sustainable Luxury Rentals</div>
            <div class="perks-bar">
                ✨ FREE DRY CLEANING &nbsp;|&nbsp; 🔄 CANCEL ANYTIME &nbsp;|&nbsp; 🛡️ INSURED LUXURY ASSETS
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- ANALYTICS OVERVIEW ---
    total_items = inventory_col.count_documents({})
    available_items = inventory_col.count_documents({"status": "Available"})
    rented_items = inventory_col.count_documents({"status": "Rented"})
    maintenance_items = inventory_col.count_documents({"status": "Maintenance"})

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Collection", total_items)
    m2.metric("Ready to Rent", available_items)
    m3.metric("Out on Rent", rented_items)
    m4.metric("In Care / Service", maintenance_items)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- NAVIGATION TABS ---
    tab_list, tab_add, tab_update, tab_delete = st.tabs([
        "🌿 Wardrobe Catalog", 
        "➕ Add New Apparel", 
        "✏️ Edit Details", 
        "🗑️ Remove Item"
    ])

    # --- TAB 1: CATALOG & SEARCH ---
    with tab_list:
        col_search1, col_search2 = st.columns([3, 1])
        with col_search1:
            search_query = st.text_input("🔍 Search Catalog", placeholder="Search designer dresses, tuxedos, categories, or IDs...")
        with col_search2:
            status_filter = st.selectbox("Availability", ["All Collection", "Available", "Rented", "Maintenance"])

        query = {}
        if status_filter != "All Collection":
            query["status"] = status_filter

        if search_query.strip():
            if ObjectId.is_valid(search_query.strip()):
                query["_id"] = ObjectId(search_query.strip())
            else:
                query["$or"] = [
                    {"item_name": {"$regex": search_query.strip(), "$options": "i"}},
                    {"category": {"$regex": search_query.strip(), "$options": "i"}}
                ]

        items = list(inventory_col.find(query))

        if not items:
            st.info("No luxury items found matching your criteria.")
        else:
            st.caption(f"Showing **{len(items)}** piece(s) in collection")
            for item in items:
                status = item.get('status', 'Available')
                badge_class = f"badge-{status.lower()}"
                
                with st.expander(f"✨ {item.get('item_name', 'Unnamed Piece')} — ${item.get('daily_rate', 0.0):.2f} / day"):
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        st.markdown(f"**Category:** {item.get('category', 'Designer Wear')}")
                        st.markdown(f"**Rental Price:** `${item.get('daily_rate', 0.0):.2f}` per day")
                        st.markdown(f"**Status:** <span class='badge {badge_class}'>{status}</span>", unsafe_allow_html=True)
                    with col_b:
                        st.caption("Inventory Object ID:")
                        st.code(str(item['_id']), language="text")

    # --- TAB 2: ADD NEW ITEM ---
    with tab_add:
        st.subheader("Add New Piece to Wardrobe")
        st.caption("Expand the Threadbare catalog with authentic designer attire.")
        
        with st.form("add_item_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                item_name = st.text_input("Item Name", placeholder="e.g. Emerald Silk Evening Gown")
                category = st.text_input("Category", placeholder="e.g. Gowns, Blazers, Jewelry")
            with col2:
                daily_rate = st.number_input("Daily Rental Rate ($)", min_value=1.0, value=85.0, step=5.0)
                status = st.selectbox("Initial Status", ["Available", "Rented", "Maintenance"])

            submit_btn = st.form_submit_button("✨ Add to Wardrobe", type="primary")

        if submit_btn:
            if not item_name.strip():
                st.error("Please provide an apparel name!")
            else:
                new_item = {
                    "item_name": item_name.strip(),
                    "category": category.strip(),
                    "daily_rate": float(daily_rate),
                    "status": status
                }
                res = inventory_col.insert_one(new_item)
                st.success(f"Successfully added to collection! Asset ID: `{res.inserted_id}`")
                st.rerun()

    # --- TAB 3: UPDATE ITEM ---
    with tab_update:
        st.subheader("Edit Wardrobe Piece")
        target_id_str = st.text_input("Enter Item ID to Edit:", key="update_id_input", placeholder="Paste 24-character Mongo ID...")

        if target_id_str.strip():
            if not ObjectId.is_valid(target_id_str.strip()):
                st.error("Invalid ObjectId format!")
            else:
                target_id = ObjectId(target_id_str.strip())
                existing_item = inventory_col.find_one({"_id": target_id})

                if not existing_item:
                    st.warning("No piece found with this ID.")
                else:
                    st.info(f"Editing: **{existing_item.get('item_name')}**")
                    
                    with st.form("update_item_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            up_name = st.text_input("Item Name", value=existing_item.get("item_name", ""))
                            up_cat = st.text_input("Category", value=existing_item.get("category", ""))
                        with col2:
                            up_rate = st.number_input(
                                "Daily Rental Rate ($)", 
                                min_value=1.0, 
                                value=float(existing_item.get("daily_rate", 50.0)),
                                step=5.0
                            )
                            status_options = ["Available", "Rented", "Maintenance"]
                            curr_status_idx = status_options.index(existing_item.get("status", "Available")) if existing_item.get("status") in status_options else 0
                            up_status = st.selectbox("Status", status_options, index=curr_status_idx)

                        update_btn = st.form_submit_button("Save Changes", type="primary")

                    if update_btn:
                        inventory_col.update_one(
                            {"_id": target_id},
                            {"$set": {
                                "item_name": up_name.strip(),
                                "category": up_cat.strip(),
                                "daily_rate": float(up_rate),
                                "status": up_status
                            }}
                        )
                        st.success("Details updated successfully!")
                        st.rerun()

    # --- TAB 4: DELETE ITEM ---
    with tab_delete:
        st.subheader("Decommission Asset")
        delete_id_str = st.text_input("Enter Item ID to Remove:", key="delete_id_input", placeholder="Paste 24-character Mongo ID...")

        if delete_id_str.strip():
            if not ObjectId.is_valid(delete_id_str.strip()):
                st.error("Invalid ObjectId format!")
            else:
                target_id = ObjectId(delete_id_str.strip())
                item_to_del = inventory_col.find_one({"_id": target_id})

                if not item_to_del:
                    st.warning("No item found with this ID.")
                else:
                    st.error(f"⚠️ Are you sure you want to permanently delete **{item_to_del.get('item_name')}**?")
                    if st.button("🔴 Confirm Removal", type="primary"):
                        inventory_col.delete_one({"_id": target_id})
                        st.success("Item removed from wardrobe collection.")
                        st.rerun()

if __name__ == "__main__":
    show_inventory_app()
