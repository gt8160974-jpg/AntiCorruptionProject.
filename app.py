import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Anti-Corruption System", layout="wide", page_icon="🛡️")
st.title("🛡️ Universal Anti-Corruption Auditor")
st.markdown("### MCA Final Year Project: Adaptive Transparency Framework")

# 2. Sidebar Settings
st.sidebar.header("1. Audit Settings")
st.sidebar.write("Adjust the sensitivity to flag suspicious price markups.")
sensitivity = st.sidebar.slider("Anomaly Sensitivity (Price %)", 100, 500, 200)

# 3. Data Input - Accepts CSV and Excel
uploaded_file = st.file_uploader("Upload any procurement file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read data based on extension
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            # Requires 'openpyxl' in requirements.txt
            df_raw = pd.read_excel(uploaded_file)
        
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
        
        # 4. Dynamic Column Mapping
        st.subheader("⚙️ Step 2: Map Your Data Columns")
        st.write("Match your file's columns to the Auditor's required fields:")
        
        col_options = df_raw.columns.tolist()
        
        # Creating a 4-column layout for the mapping dropdowns
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            item_col = st.selectbox("Item/Product Column", col_options)
        with c2:
            vendor_col = st.selectbox("Vendor/Supplier Column", col_options)
        with c3:
            paid_col = st.selectbox("Price Paid Column", col_options)
        with c4:
            std_col = st.selectbox("Market Standard Price Column", col_options)

        if st.button("🚀 Run Audit with Selected Mapping"):
            # Create a standardized dataframe for logic
            # pd.to_numeric ensures the math works even if there are currency symbols
            df = pd.DataFrame({
                'Item': df_raw[item_col],
                'Vendor': df_raw[vendor_col],
                'Price_Paid': pd.to_numeric(df_raw[paid_col], errors='coerce'),
                'Standard_Price': pd.to_numeric(df_raw[std_col], errors='coerce')
            }).dropna()

            # 5. The Audit Logic
            # Calculate the percentage difference
            df['Price_Diff_%'] = (df['Price_Paid'] / df['Standard_Price']) * 100
            
            # Flagging based on the slider value
            df['Status'] = df['Price_Diff_%'].apply(
                lambda x: '🚨 CORRUPTION RISK' if x > sensitivity else '✅ CLEAR'
            )
            
            # 6. Dashboard Visuals
            st.divider()
            res_col, chart_col = st.columns([2, 1])
            
            with res_col:
                st.subheader("🔍 Detailed Audit Results")
                # Highlights cells that exceed the sensitivity threshold
                st.dataframe(df.style.highlight_between(
                    left=sensitivity, 
                    subset=['Price_Diff_%'], 
                    color='#ffcccc'
                ), use_container_width=True)
            
            with chart_col:
                st.subheader("📊 Risk Visualization")
                st.bar_chart(data=df, x='Item', y='Price_Diff_%')

            # Summary Metrics
            st.divider()
            m1, m2, m3 = st.columns(3)
            risks = len(df[df['Status'] == '🚨 CORRUPTION RISK'])
            m1.metric("Total Items Audited", len(df))
            m2.metric("High-Risk Anomalies", risks, delta=risks, delta_color="inverse")
            m3.metric("Maximum Variance Found", f"{int(df['Price_Diff_%'].max())}%")

            # 7. Export Standardized Report
            st.subheader("📥 Export Evidence")
            csv_output = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Standardized Audit Report (CSV)",
                data=csv_output,
                file_name='final_audit_report.csv',
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"⚠️ An error occurred while processing the file: {e}")

else:
    # Initial state screen
    st.info("👋 Welcome! Please upload a CSV or Excel file to begin the audit process.")
    st.markdown("""
    **To use this tool:**
    1. Upload your expenditure data.
    2. Map the columns (Item, Vendor, Price Paid, and Standard Price).
    3. Adjust the sensitivity slider in the sidebar.
    4. Review flagged risks and download your report.
    """)
