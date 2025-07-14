import streamlit as st
import uuid

# ---------- PAGE SETUP ----------
st.set_page_config(page_title="🛒 Grocery Manager", layout="wide")
st.markdown(
    """
    <style>
    .row-widget.stButton > button {
        width: 100%;
    }
    .number-input input {
        text-align: center;
    }
    .stNumberInput, .stTextInput {
        padding-top: 2px !important;
        padding-bottom: 2px !important;
    }
    .stMarkdown {
        padding-top: 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛒 Grocery Manager")
st.markdown("Add items now, and update prices & quantities later while shopping!")

# ---------- SESSION STATE ----------
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

# ---------- ADD ITEM FORM ----------
with st.form("add_form", clear_on_submit=True):
    st.markdown("#### ➕ Add New Item")

    col1, col2, col3 = st.columns([5, 2, 1.5])
    with col1:
        item_name = st.text_input("Item Name", label_visibility="collapsed", placeholder="Enter item name")
    with col2:
        item_unit = st.selectbox("Unit", ["kg", "liters", "pcs", "packets", "dozen"], label_visibility="collapsed")
    with col3:
        submitted = st.form_submit_button("➕ Add")

    if submitted:
        if item_name.strip():
            st.session_state.grocery_list.append({
                "id": str(uuid.uuid4()),
                "name": item_name.strip(),
                "price": 0.0,
                "qty": 1.0,
                "unit": item_unit,
                "purchased": False
            })
            st.success(f"✅ Added: {item_name.strip()} ({item_unit})")
        else:
            st.warning("⚠️ Please enter a valid item name.")

# ---------- SHOW LIST ----------
st.markdown("---")
st.subheader("📋 Grocery List")

if st.session_state.grocery_list:
    total = 0.0
    purchased_total = 0.0

    # Headers
    headers = st.columns([0.5, 2.5, 2, 2, 1.5, 2, 1.2, 1])
    headers[0].markdown("**#**")
    headers[1].markdown("**Item**")
    headers[2].markdown("**Price (₹)**")
    headers[3].markdown("**Quantity**")
    headers[4].markdown("**Unit**")
    headers[5].markdown("**Subtotal (₹)**")
    headers[6].markdown("**Purchased**")
    headers[7].markdown("**Remove**")

    item_to_remove = None

    for idx, item in enumerate(st.session_state.grocery_list):
        cols = st.columns([0.5, 2.5, 2, 2, 1.5, 2, 1.2, 1])

        cols[0].markdown(f"**{idx + 1}**")
        cols[1].markdown(f"**{item['name']}**")

        item["price"] = cols[2].number_input(
            label="", key=f"price_{item['id']}",
            value=float(item["price"]), min_value=0.0, step=0.5,
            format="%.2f", label_visibility="collapsed"
        )

        item["qty"] = cols[3].number_input(
            label="", key=f"qty_{item['id']}",
            value=float(item["qty"]), min_value=0.0, step=0.1,
            label_visibility="collapsed"
        )

        cols[4].markdown(f"<div style='text-align:center;'>{item['unit']}</div>", unsafe_allow_html=True)

        subtotal = item["price"] * item["qty"]
        cols[5].markdown(f"<div style='text-align:center;'>₹ {subtotal:.2f}</div>", unsafe_allow_html=True)
        total += subtotal

        item["purchased"] = cols[6].checkbox("", value=item["purchased"], key=f"purchased_{item['id']}", label_visibility="collapsed")
        if item["purchased"]:
            purchased_total += subtotal

        with cols[7]:
            if st.button("❌", key=f"remove_{item['id']}"):
                item_to_remove = item["id"]

    # Remove item after loop
    if item_to_remove:
        st.session_state.grocery_list = [item for item in st.session_state.grocery_list if item["id"] != item_to_remove]
        st.experimental_rerun()

    # Summary
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.success(f"🧾 **Total Cost:** ₹ {total:.2f}")
    c2.info(f"🛍 **Purchased Total:** ₹ {purchased_total:.2f}")
    c3.warning(f"📦 **Items Count:** {len(st.session_state.grocery_list)}")

    if st.button("🧹 Clear All"):
        st.session_state.grocery_list.clear()
        st.experimental_rerun()
else:
    st.info("📝 No items yet. Start by adding items above.")
