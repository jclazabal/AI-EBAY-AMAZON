import streamlit as st
import pandas as pd
import io
from io import BytesIO

st.title("AI Bot for Amazon/eBay Listings")
st.write("Upload your Excel file to generate optimized listing data, and export it to CSV or Excel.")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel file with product data", type=["xlsx"])

if uploaded_file:
    input_df = pd.read_excel(uploaded_file)
    data = []

    for _, row in input_df.iterrows():
        asin = row.get("ASIN", "")
        title = f"{row.get('Product Type', 'Clutch Kit')} for {row.get('Fitment', 'Unknown Vehicle')} – {row.get('Brand', 'Brand')} {asin}"
        bullets = [
            f"Fits {row.get('Fitment', 'N/A')}",
            f"Includes: {row.get('Components', 'Full kit')}",
            f"Made by {row.get('Brand', 'Brand')} in {row.get('Country', 'USA')}",
            row.get('Review Summary', 'Customer approved')
        ]
        description = f"""
<p><strong>Vehicle Fitment:</strong> {row.get('Fitment', 'N/A')}</p>
<ul>
  <li>{row.get('Components', 'Full kit')}</li>
  <li>Brand: {row.get('Brand', 'Brand')}, made in {row.get('Country', 'USA')}</li>
  <li>{row.get('Review Summary', 'Customer approved')}</li>
</ul>
"""
        data.append({
            "ASIN": asin,
            "Suggested Title": title,
            "Bullets": bullets,
            "HTML Description": description
        })

    for item in data:
        st.subheader(f"ASIN: {item['ASIN']}")
        st.markdown(f"**Suggested Title:** {item['Suggested Title']}")
        st.markdown("**Bullet Points:**")
        for bullet in item["Bullets"]:
            st.markdown(f"- {bullet}")
        st.markdown("**HTML Description:**")
        st.code(item["HTML Description"], language='html')

    # Flatten bullets for export
    export_data = []
    for item in data:
        export_data.append({
            "ASIN": item["ASIN"],
            "Suggested Title": item["Suggested Title"],
            "Bullets": " | ".join(item["Bullets"]),
            "HTML Description": item["HTML Description"]
        })
    df = pd.DataFrame(export_data)

    # Export to CSV
    if st.button("Export to CSV"):
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="amazon_ebay_listings.csv",
            mime="text/csv"
        )

    # Export to Excel
    if st.button("Export to Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Listings')
        st.download_button(
            label="Download Excel",
            data=output.getvalue(),
            file_name="amazon_ebay_listings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info("Please upload an Excel file with columns: ASIN, Product Type, Fitment, Brand, Components, Country, Review Summary.")
