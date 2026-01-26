import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Anti-Corruption System", layout="wide")
st.title("🛡️ AI-Powered Anti-Corruption Auditor")
st.markdown("### MCA Final Year Project: Transparency Framework")

# 2. Session State (Memory)
if 'df' not in st.session_state:
    st.session_state.df = None

# 3. Sidebar Settings
st.sidebar.header("Audit Settings")
sensitivity = st.sidebar.slider("Anomaly Sensitivity (Price %)", 100, 500, 200)

# 4. Data Input
uploaded_file = st.file_uploader("Upload government spending file (CSV)", type="csv")

if st.button("Show Demo Data") or uploaded_file is not None:
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
    else:
        data = {
            'Item': ['Laptops', 'Pencils', 'Office Chairs', 'Pencils', 'Laptops'],
            'Vendor': ['Tech Corp', 'Global Supplies', 'Family First Ltd', 'Global Supplies', 'Tech Corp'],
            'Price_Paid': [50000, 10, 15000, 10, 50000],
            'Standard_Price': [50000, 10, 2000, 10, 50000]
        }
        st.session_state.df = pd.DataFrame(data)

# 5. The Audit Logic & Visualization
if st.session_state.df is not None:
    df = st.session_state.df.copy()
    
    # Calculate Price Difference
    df['Price_Diff_%'] = (df['Price_Paid'] / df['Standard_Price']) * 100
    
    # Flagging Logic
    limit = sensitivity
    df['Status'] = df['Price_Diff_%'].apply(lambda x: '🚨 CORRUPTION RISK' if x > limit else '✅ CLEAR')
    
    # Show Visuals
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔍 Audit Results")
        st.dataframe(df.style.highlight_max(axis=0, subset=['Price_Diff_%'], color='#ffcccc'))
    
    with col2:
        st.subheader("📊 Risk Visualization")
        st.bar_chart(data=df, x='Item', y='Price_Diff_%')

    # Summary Stats
    risks = len(df[df['Status'] == '🚨 CORRUPTION RISK'])
    st.metric("Risk Items Found", risks)
    
    # 6. Download Feature
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Report (CSV)",
        data=csv,
        file_name='audit_report.csv',
        mime='text/csv',
    )
else:
    st.info("Upload a file or click 'Show Demo Data' to see the AI in action.")