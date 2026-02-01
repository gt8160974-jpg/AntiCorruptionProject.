import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Anti-Corruption System", layout="wide", page_icon="🛡️")
st.title("🛡️ Universal Anti-Corruption Auditor")
st.markdown("### MCA Final Year Project: Adaptive Transparency Framework")

# 2. Sidebar Settings
st.sidebar.header("1. Audit Settings")
sensitivity = st.sidebar.slider("Anomaly Sensitivity (Price %)", 100, 500, 200)

# 3. Data Input
uploaded_file = st.file_uploader("Upload any procurement file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read data based on extension
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File uploaded successfully!")
        
        # 4. Dynamic Column Mapping
        st.subheader("⚙️ Step 2: Map Your Data Columns")
        col_options = df_raw.columns.tolist()
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            item_col = st.selectbox("Item Column", col_options)
        with c2:
            vendor_col = st.selectbox("Vendor Column", col_options)
        with c3:
            paid_col = st.selectbox("Price Paid", col_options)
        with c4:
            std_col = st.selectbox("Standard Price", col_options)

        if st.button("🚀 Run Audit"):
            # Create a standardized dataframe and handle data cleaning
            df = pd.DataFrame({
                'Item': df_raw[item_col].astype(str),
                'Vendor': df_raw[vendor_col].astype(str),
                'Price_Paid': pd.to_numeric(df_raw[paid_col], errors='coerce'),
                'Standard_Price': pd.to_numeric(df_raw[std_col], errors='coerce')
            })

            # Remove rows with empty prices to prevent math errors
            df = df.dropna(subset=['Price_Paid', 'Standard_Price'])

            if not df.empty:
                # 5. The Audit Logic
                df['Price_Diff_%'] = (df['Price_Paid'] / df['Standard_Price']) * 100
                df['Status'] = df['Price_Diff_%'].apply(
                    lambda x: '🚨 CORRUPTION RISK' if x > sensitivity else '✅ CLEAR'
                )
                
                # 6. Dashboard Visuals
                res_col, chart_col = st.columns([2, 1])
                with res_col:
                    st.subheader("🔍 Audit Results")
                    st.dataframe(df.style.highlight_between(left=sensitivity, subset=['Price_Diff_%'], color='#ffcccc'))
                
                with chart_col:
                    st.subheader("📊 Risk Visualization")
                    st.bar_chart(data=df, x='Item', y='Price_Diff_%')

                # Metrics
                st.divider()
                m1, m2, m3 = st.columns(3)
                risks = len(df[df['Status'] == '🚨 CORRUPTION RISK'])
                m1.metric("Items Audited", len(df))
                m2.metric("Risks Found", risks, delta=risks, delta_color="inverse")
                m3.metric("Max Variance", f"{int(df['Price_Diff_%'].max())}%")
            else:
                st.warning("⚠️ No valid numeric data found. Check your column mapping.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
else:
    st.info("👋 Please upload a CSV or Excel file to begin.")
