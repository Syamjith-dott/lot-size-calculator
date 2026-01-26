import streamlit as st

# App title
st.title("Lot Size Calculator for XAUUSD")

# Session state initialization
if "account_history" not in st.session_state:
    st.session_state.account_history = [1000, 5000, 10000]

if "risk_history" not in st.session_state:
    st.session_state.risk_history = [0.5, 1.0, 2.0]

# Account Size Dropdown + Custom Entry
account_choice = st.selectbox("Select Account Size", st.session_state.account_history)
account_custom = st.number_input("Or Enter Custom Account Size ($)", min_value=0.0, step=10.0)

account_size = account_custom if account_custom not in st.session_state.account_history and account_custom > 0 else account_choice
if account_custom and account_custom not in st.session_state.account_history:
    st.session_state.account_history.insert(0, account_custom)

# Risk Percentage Dropdown + Custom Entry
risk_choice = st.selectbox("Select Risk Percentage (%)", st.session_state.risk_history)
risk_custom = st.number_input("Or Enter Custom Risk %", min_value=0.0, step=0.1)

risk_percent = risk_custom if risk_custom not in st.session_state.risk_history and risk_custom > 0 else risk_choice
if risk_custom and risk_custom not in st.session_state.risk_history:
    st.session_state.risk_history.insert(0, risk_custom)

# Other User Inputs
entry_price = st.number_input("Entry Price", min_value=0.0)
stop_loss_price = st.number_input("Stop Loss Price", min_value=0.0)
target_price = st.number_input("Target Price", min_value=0.0)

# Ensure all inputs are provided
if all([account_size, risk_percent, entry_price, stop_loss_price, target_price]):

    # Calculations
    risk_amount = (risk_percent / 100) * account_size
    sl_pips = abs(entry_price - stop_loss_price) * 100  # XAUUSD = 1 pip = 0.01
    tp_pips = abs(target_price - entry_price) * 100
    lot_size = risk_amount / sl_pips if sl_pips != 0 else 0
    loss = sl_pips * lot_size
    profit = tp_pips * lot_size
    rr_ratio = profit / loss if loss != 0 else 0

    # Output
    st.write("###  Results")
    st.write(f" Stop Loss (Pips): {int(sl_pips)}")
    st.markdown(f"<span style='color:red;'> Potential Loss: ${int(loss)}</span>", unsafe_allow_html=True)
    st.markdown(f"<span style='color:blue;'> Potential Profit: ${int(profit)}</span>", unsafe_allow_html=True)
    st.write(f" Risk-to-Reward Ratio: {rr_ratio:.2f}")
    st.success(f"✅ Recommended Lot Size: {lot_size:.2f}")

else:
    st.warning("⚠️ Please fill in all the input fields to see the results.")