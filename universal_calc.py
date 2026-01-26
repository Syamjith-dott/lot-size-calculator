import streamlit as st

st.set_page_config(page_title="Universal Lot Size Calc", layout="centered")
st.title("Universal Lot Size Calculator")

# 1. Asset Settings
ASSET_CONFIG = {
    "Forex Majors (EURUSD, etc.)": {"multiplier": 10000, "pip_val": 10},
    "Yen Pairs (USDJPY, etc.)": {"multiplier": 100, "pip_val": 10},
    "Gold (XAUUSD)": {"multiplier": 100, "pip_val": 1},
    "Crypto (BTCUSD)": {"multiplier": 1, "pip_val": 1}
}

# 2. UI Inputs
asset_type = st.selectbox("Select Asset Class", list(ASSET_CONFIG.keys()))
config = ASSET_CONFIG[asset_type]

col1, col2 = st.columns(2)
with col1:
    account_size = st.number_input("Account Size ($)", min_value=0.0, value=1000.0, step=100.0)
with col2:
    risk_percent = st.number_input("Risk Percentage (%)", min_value=0.0, value=1.0, step=0.1)

st.divider()
entry_price = st.number_input("Entry Price", min_value=0.0, format="%.5f", value=0.0)
stop_loss_price = st.number_input("Stop Loss Price", min_value=0.0, format="%.5f", value=0.0)
target_price = st.number_input("Target Price", min_value=0.0, format="%.5f", value=0.0)

# 3. Calculations
if all([account_size > 0, risk_percent > 0, entry_price > 0, stop_loss_price > 0]):
    # Calculate Pips
    sl_pips = abs(entry_price - stop_loss_price) * config["multiplier"]
    tp_pips = abs(target_price - entry_price) * config["multiplier"]
    
    # Calculate Risk in Dollars
    risk_dollars = (risk_percent / 100) * account_size
    
    if sl_pips > 0:
        # Standard Formula: Lot Size = Risk / (Pips * Pip Value)
        lot_size = risk_dollars / (sl_pips * config["pip_val"])
        
        st.write("### 📊 Results")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.write(f"**Stop Loss:** {sl_pips:.1f} Pips")
            st.markdown(f"<span style='color:red;'>**Risk Amount:** ${risk_dollars:.2f}</span>", unsafe_allow_html=True)
        with res_col2:
            st.write(f"**Target Profit:** {tp_pips:.1f} Pips")
            reward_dollars = tp_pips * lot_size * config["pip_val"]
            st.markdown(f"<span style='color:green;'>**Potential Profit:** ${reward_dollars:.2f}</span>", unsafe_allow_html=True)
            
        st.divider()
        # Handle decimal precision for small lot sizes
        if lot_size < 0.01:
            st.success(f"✅ **Recommended Lot Size: {lot_size:.4f}**")
        else:
            st.success(f"✅ **Recommended Lot Size: {lot_size:.2f}**")
    else:
        st.error("Stop Loss cannot be at the same price as Entry.")
else:
    st.info("👋 Enter your trade details above to see the recommended lot size.")