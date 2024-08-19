#OneDrive\Desktop\Projects\science\pages>streamlit run molgenics.py


import streamlit as st
import json
import os

def load_data():
    # Get the directory where the current script is located
    current_dir = os.path.dirname(__file__)
    
    # Construct the full path to the JSON file
    json_path = os.path.join(current_dir, 'scrapers', 'molgenics.json')  # Update to use the correct JSON file
    
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_unique_products(data):
    # Extract unique products from the loaded data
    products = {item['product'] for item in data}
    return sorted(products)

# Load the data
data = load_data()

# Extract unique products from the data
products = extract_unique_products(data)

st.title("Molgenics")

# Search by product using a dropdown menu
product_search = st.selectbox("Select a Product", options=["All"] + products)

# Apply Filters button
if st.button("Apply Filters"):
    st.subheader("Filtered Products")
    for item in data:
        product = item["product"]
        link = item.get("link")  # Get the link from the item

        # Filter by product name
        if product_search == "All" or product_search == product:
            st.write(f"**Product:** {product}")
            if link:
                st.markdown(f"[View Product]({link})", unsafe_allow_html=True)  # Make the link clickable
