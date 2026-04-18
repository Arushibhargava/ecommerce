import streamlit as st
import requests
import uuid
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/products"

st.set_page_config(page_title="Product CRUD App", layout="wide")
st.title("🛒 Product Management System")

menu = ["Search Products", "Search by ID", "Add Product", "Update Product", "Delete Product"]
choice = st.sidebar.selectbox("Menu", menu)

# -------------------- SEARCH BY NAME --------------------
if choice == "Search Products":
    st.subheader("🔍 Search Products by Name")

    name = st.text_input("Enter Product Name (Required)")
    sort = st.checkbox("Sort Results")
    order = st.selectbox("Order", ["asc", "desc"])
    limit = st.number_input("Limit", 1, 100, 10)
    offset = st.number_input("Offset", 0, 100, 0)

    if st.button("Search"):
        if not name:
            st.error("Name is required")
        else:
            params = {
                "name": name,
                "sort": sort,
                "order": order,
                "limit": limit,
                "offset": offset
            }

            res = requests.get(BASE_URL, params=params)

            if res.status_code == 200:
                data = res.json()
                st.success(f"Total Found: {data['total']}")

                for p in data["data"]:
                    with st.expander(p["name"]):
                        st.json(p)
            else:
                st.error(res.text)

# -------------------- SEARCH BY ID --------------------
elif choice == "Search by ID":
    st.subheader("🔍 Search Product by ID")

    product_id = st.text_input("Enter Product ID")

    if st.button("Get Product"):
        res = requests.get(f"{BASE_URL}/{product_id}")

        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error(res.text)

# -------------------- ADD PRODUCT --------------------
elif choice == "Add Product":
    st.subheader("➕ Add Product")

    name = st.text_input("Name")
    sku = st.text_input("SKU")
    description = st.text_area("Description")
    category = st.text_input("Category")
    brand = st.text_input("Brand")
    price = st.number_input("Price", min_value=0.0)
    discount = st.number_input("Discount %", 0, 90)
    stock = st.number_input("Stock", 0)
    rating = st.number_input("Rating", 0.0, 5.0)
    is_active = st.checkbox("Is Active")

    st.write("### Dimensions")
    length = st.number_input("Length")
    width = st.number_input("Width")
    height = st.number_input("Height")

    st.write("### Seller")
    seller_name = st.text_input("Seller Name")
    seller_email = st.text_input("Seller Email")
    seller_website = st.text_input("Seller Website")

    if st.button("Add Product"):
        product = {
            "id": str(uuid.uuid4()),
            "sku": sku,
            "name": name,
            "description": description,
            "category": category,
            "brand": brand,
            "price": price,
            "currency": "INR",
            "discount_percent": discount,
            "stock": stock,
            "is_active": is_active,
            "rating": rating,
            "tags": [],
            "image_urls": ["https://example.com/image.png"],
            "dimensions_cm": {
                "length": length,
                "width": width,
                "height": height
            },
            "seller": {
                "id": str(uuid.uuid4()),
                "name": seller_name,
                "email": seller_email,
                "website": seller_website
            },
            "created_at": datetime.utcnow().isoformat()
        }

        res = requests.post(BASE_URL, json=product)

        if res.status_code in [200, 201]:
            st.success("Product Added Successfully")
        else:
            st.error(res.text)

# -------------------- UPDATE PRODUCT --------------------
elif choice == "Update Product":
    st.subheader("✏️ Update Product")

    product_id = st.text_input("Product ID (Required)")

    st.write("### Optional Fields (fill what you want to update)")

    name = st.text_input("Name")
    description = st.text_area("Description")
    category = st.text_input("Category")
    brand = st.text_input("Brand")
    price = st.number_input("Price", min_value=0.0)
    discount = st.number_input("Discount %", 0, 90)
    stock = st.number_input("Stock", 0)
    rating = st.number_input("Rating", 0.0, 5.0)
    is_active = st.checkbox("Is Active")

    st.write("### Dimensions (Optional)")
    length = st.number_input("Length")
    width = st.number_input("Width")
    height = st.number_input("Height")

    st.write("### Seller (Optional)")
    seller_name = st.text_input("Seller Name")
    seller_email = st.text_input("Seller Email")
    seller_website = st.text_input("Seller Website")

    if st.button("Update"):
        if not product_id:
            st.error("Product ID is required")
        else:
            update_data = {}

            if name: update_data["name"] = name
            if description: update_data["description"] = description
            if category: update_data["category"] = category
            if brand: update_data["brand"] = brand
            if price: update_data["price"] = price
            if discount: update_data["discount_percent"] = discount
            if stock: update_data["stock"] = stock
            if rating: update_data["rating"] = rating
            if is_active: update_data["is_active"] = is_active

            # Dimensions
            dim = {}
            if length: dim["length"] = length
            if width: dim["width"] = width
            if height: dim["height"] = height
            if dim:
                update_data["dimensions_cm"] = dim

            # Seller
            seller = {}
            if seller_name: seller["name"] = seller_name
            if seller_email: seller["email"] = seller_email
            if seller_website: seller["website"] = seller_website
            if seller:
                update_data["seller"] = seller

            res = requests.put(f"{BASE_URL}/{product_id}", json=update_data)

            if res.status_code == 200:
                st.success("Product Updated Successfully")
            else:
                st.error(res.text)

# -------------------- DELETE PRODUCT --------------------
elif choice == "Delete Product":
    st.subheader("🗑️ Delete Product")

    product_id = st.text_input("Enter Product ID")

    if st.button("Delete"):
        res = requests.delete(f"{BASE_URL}/{product_id}")

        if res.status_code == 200:
            st.success("Deleted Successfully")
        else:
            st.error(res.text)