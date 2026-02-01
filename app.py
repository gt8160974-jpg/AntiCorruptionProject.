        if st.button("🚀 Run Audit with Selected Mapping"):
            # Create a standardized dataframe
            # .strip() removes hidden spaces, and 'coerce' handles non-numeric text
            df = pd.DataFrame({
                'Item': df_raw[item_col].astype(str),
                'Vendor': df_raw[vendor_col].astype(str),
                'Price_Paid': pd.to_numeric(df_raw[paid_col], errors='coerce'),
                'Standard_Price': pd.to_numeric(df_raw[std_col], errors='coerce')
            })

            # FIX: Remove any rows that have empty (NaN) price values
            df = df.dropna(subset=['Price_Paid', 'Standard_Price'])

            # 5. The Audit Logic
            if not df.empty:
                df['Price_Diff_%'] = (df['Price_Paid'] / df['Standard_Price']) * 100
                
                # Flagging logic
                df['Status'] = df['Price_Diff_%'].apply(
                    lambda x: '🚨 CORRUPTION RISK' if x > sensitivity else '✅ CLEAR'
                )
                
                # ... (rest of your visualization code)
            else:
                st.error("❌ No valid numeric data found in the selected price columns. Please check your file.")
                
