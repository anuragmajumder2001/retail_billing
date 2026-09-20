import streamlit as st


# -----------------------------
# Manager function
# -----------------------------
def manager(offer=0):
    return lambda total_mrp: total_mrp * (100 - offer) / 100


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Billing System",
    page_icon="🧾",
    layout="centered"
)

st.title("🧾 Billing Management System")


# -----------------------------
# Manager Login
# -----------------------------
st.header("👨‍💼 Manager Login")

userid_m = "manager123"
password_m = "manager@123"

userid_login_m = st.text_input(
    "Dear Manager, Enter your User ID",
    key="manager_userid"
)

password_login_m = st.text_input(
    "Enter your Password",
    type="password",
    key="manager_password"
)

manager_login = st.button("Manager Login")


# Default offer
if "offer" not in st.session_state:
    st.session_state.offer = 0


if manager_login:

    if userid_m == userid_login_m and password_m == password_login_m:

        st.success("Manager login successful!")

        offer = st.number_input(
            "Enter your offer (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=1.0
        )

        if st.button("Set Offer"):
            st.session_state.offer = offer
            st.success(f"{offer}% offer has been applied.")

    else:
        st.error("User ID or password is wrong... Try again.")

        st.session_state.offer = 0


# -----------------------------
# Current Offer
# -----------------------------
st.divider()

st.info(
    f"Current Manager Offer: {st.session_state.offer}%"
)


# -----------------------------
# Cashier Login
# -----------------------------
st.header("👨‍💼 Cashier Login")

userid_cashier = "cashier123"
password_cashier = "cashier@123"

userid_login_cashier = st.text_input(
    "Dear Cashier, Enter your User ID",
    key="cashier_userid"
)

password_login_cashier = st.text_input(
    "Enter your Password",
    type="password",
    key="cashier_password"
)

cashier_login = st.button("Cashier Login")


# -----------------------------
# Cashier Billing
# -----------------------------
if cashier_login:

    if (
        userid_cashier == userid_login_cashier
        and password_cashier == password_login_cashier
    ):

        st.success("Billing can be started now!")

        # Store billing items
        st.session_state.billing_items = []

    else:
        st.error("User ID or password is wrong... Try again.")


# -----------------------------
# Billing Section
# -----------------------------
if "billing_items" in st.session_state:

    st.divider()

    st.header("🛒 Customer Billing")

    # Item price
    price = st.number_input(
        "Enter price of the item",
        min_value=0.0,
        step=1.0,
        key="item_price"
    )

    # Item quantity
    quantity = st.number_input(
        "Enter quantity of the item",
        min_value=1,
        step=1,
        key="item_quantity"
    )

    if st.button("Add Item"):

        total_for_product = price * quantity

        st.session_state.billing_items.append({
            "Price": price,
            "Quantity": quantity,
            "Total": total_for_product
        })

        st.success("Item added successfully!")


    # -----------------------------
    # Display Items
    # -----------------------------
    if st.session_state.billing_items:

        st.subheader("📋 Billing Items")

        total_mrp = 0

        for i, item in enumerate(st.session_state.billing_items):

            total_mrp += item["Total"]

            st.write(
                f"**Item {i + 1}:** "
                f"₹{item['Price']:.2f} × {item['Quantity']} "
                f"= ₹{item['Total']:.2f}"
            )

        st.divider()

        st.write(f"### Total MRP: ₹{total_mrp:.2f}")


        # -----------------------------
        # Calculate Final Amount
        # -----------------------------
        if st.button("Generate Bill"):

            billing_formula = manager(
                st.session_state.offer
            )

            total_amount_payable = billing_formula(total_mrp)

            discount_amount = total_mrp - total_amount_payable

            st.success(
                f"### Total Amount Payable: ₹{total_amount_payable:.2f}"
            )

            st.write(
                f"**Discount:** ₹{discount_amount:.2f}"
            )


        # -----------------------------
        # Clear Billing
        # -----------------------------
        if st.button("Clear Bill"):

            st.session_state.billing_items = []

            st.rerun()