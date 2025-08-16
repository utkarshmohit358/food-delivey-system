import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
from PIL import Image
import random
from datetime import datetime
from decimal import Decimal


st.set_page_config(page_title="BiteBuddy", page_icon="🍽️", layout="wide")

# Custom CSS for enhanced design with hover effects, fonts, animations
st.markdown("""
    <style>
    body {
        background-color: #fff;
        color: #333;
        font-family: 'Segoe UI', sans-serif;
    }
    .css-1d391kg, .css-1v3fvcr {
        background-color: #fff0f0;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.2s ease-in-out;
    }
    .css-1d391kg:hover, .css-1v3fvcr:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    h1, h2, h3, h4 {
        color: #FF6347;
    }
    .stButton > button {
        background-color: #FF6347;
        color: white;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #e5533d;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Database Connection
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='fooddelivery'
    )

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="BiteBuddy",
       options=["Home", "Restaurants", "Menu", "Search", "Orders", "Track Order", "Place Order", "Feedback", "Wishlist", "Profile"],
       icons=["house", "building", "book", "search", "cart", "geo-alt", "chat", "heart", "person-circle"],
        menu_icon="globe",
        default_index=0,
    )

# --- Pages ---
if selected == "Home":
    st.markdown("""
    <h1 style='text-align: center; color: #FF6347;'>Welcome to BiteBuddy</h1>
    <h3 style='text-align: center;'>Discover the best food & drinks in your city</h3>
    
   <span style='text-align: left;'>
        <img src='https://images.unsplash.com/photo-1600891964599-f61ba0e24092?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cmVzdGF1cmFudCUyMGZvb2R8ZW58MHx8MHx8fDA%3D' 
             style='width:30%; border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'/>
        </span>
    <span style='text-align: center;'>           
        <img src='https://img.freepik.com/premium-photo/table-full-delicious-food-top-view_79782-601.jpg' 
             style='width:30%; border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'/>
    </span>
    <span style='text-align: right;'>
        <img src='https://www.papirmass.com/wp-content/uploads/2024/06/fast-food-restaurant-names2.jpg' 
             style='width:30%; border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'/>
    </span>            
    """, unsafe_allow_html=True)


elif selected == "Restaurants":
    st.markdown("<h2 style='color:#FF6347;'>Popular Restaurants</h2>", unsafe_allow_html=True)
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM Restaurant")
    data = c.fetchall()
    for row in data:
        with st.container():
            cols = st.columns([2, 5])
            with cols[0]:
                image_url = {
                    "Spice Kitchen": "https://images.unsplash.com/photo-1600891964599-f61ba0e24092",
                    "South Spice": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8xPTwPISF91b5k4PQVgvp8Jgr2fGSvdhEcg&s",
                    "Tandoori Flame": "https://tandooriflame.com/wp-content/uploads/2022/08/Edit-1-scaled.jpg",
                    "Pasta Paradise": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/restaurant/cover/c955e64e-7086-4f66-b6b4-2ce00789142a.png",
                    "BBQ Nation": "https://i0.wp.com/www.drsdeals.in/wp-content/uploads/2022/04/Restaurants-Bars.webp?fit=1200%2C675&ssl=1",
                    "The Office Cafe": "https://en.idei.club/uploads/posts/2023-06/1685627296_en-idei-club-p-cafe-office-dizain-pinterest-1.jpg",
                }.get(row[1], f"https://source.unsplash.com/300x200/?restaurant,food,{random.randint(1,1000)}")
                st.image(image_url, use_container_width=True)
            with cols[1]:
                st.subheader(row[1])
                st.write(f"📞 {row[2]} | 📍 {row[6]}, {row[4]} - {row[7]}")
    conn.close()

elif selected == "Menu":
    st.markdown("<h2 style='color:#FF6347;'>Explore Menu Items</h2>", unsafe_allow_html=True)
    cuisine_filter = st.selectbox("Filter by Cuisine", ["All"])
    conn = get_connection()
    c = conn.cursor()
    if cuisine_filter == "All":
        c.execute("SELECT item_name, price FROM Menu_Item")
    else:
        c.execute("SELECT item_name, price FROM Menu_Item WHERE cuisine = %s", (cuisine_filter,))
    menu_items = c.fetchall()
    for item in menu_items:
        with st.container():
            cols = st.columns([2, 5])
            with cols[0]:
                item_images = {
                    "Paneer Butter Masala": "https://www.indianhealthyrecipes.com/wp-content/uploads/2014/11/paneer-butter-masala-recipe-2.jpg",
                    "Margherita Pizza": "https://uk.ooni.com/cdn/shop/articles/20220211142645-margherita-9920_e41233d5-dcec-461c-b07e-03245f031dfe.jpg?v=1737105431&width=1080",
                    "Chicken Biryani": "https://ministryofcurry.com/wp-content/uploads/2024/06/chicken-biryani-5.jpg",
                    "Tandoori Chicken": "https://sinfullyspicy.com/wp-content/uploads/2014/07/1200-by-1200-images-2.jpg",
                    "Chocolate Lava Cake": "https://www.melskitchencafe.com/wp-content/uploads/2023/01/updated-lava-cakes7.jpg",
                    "Beetroot Burger": "https://images.immediate.co.uk/production/volatile/sites/30/2020/08/cant-believe-its-vegan-burger-76fdd67.jpg",
                    "Veg Manchurian": "https://www.yummytummyaarthi.com/wp-content/uploads/2022/08/veg-manchurian-1.jpeg",
                }
                img_url = item_images.get(item[0], f"https://source.unsplash.com/300x200/?dish,food,{random.randint(1,1000)}")
                st.image(img_url, use_container_width=True)
            with cols[1]:
                st.write(f"🍽️ {item[0]} - ₹{item[1]}")
    conn.close()

elif selected == "Search":
    st.markdown("<h2 style='color:#FF6347;'>Search Menu or Restaurants</h2>", unsafe_allow_html=True)
    search_term = st.text_input("Search")
    if search_term:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT rest_name FROM Restaurant WHERE rest_name LIKE %s", ('%' + search_term + '%',))
        rest_results = c.fetchall()
        c.execute("SELECT item_name FROM Menu_Item WHERE item_name LIKE %s", ('%' + search_term + '%',))
        item_results = c.fetchall()
        st.subheader("Restaurants:")
        for r in rest_results:
            st.write(f"🏢 {r[0]}")
        st.subheader("Menu Items:")
        for i in item_results:
            st.write(f"🍽️ {i[0]}")
        conn.close()

elif selected == "Orders":
    st.markdown("<h2 style='color:#FF6347;'>Your Orders</h2>", unsafe_allow_html=True)
    cust_id = st.number_input("Enter Your Customer ID", min_value=1, step=1)
    if cust_id:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Orders WHERE cust_id = %s", (cust_id,))
        orders = c.fetchall()
        for order in orders:
            st.write(f"Order ID: {order[0]} | Status: {order[6]} | Total: ₹{order[5]}")
        conn.close()

elif selected == "Place Order":
    st.markdown("<h2 style='color:#FF6347;'>Place Your Order</h2>", unsafe_allow_html=True)
    
    cust_id = st.number_input("Customer ID", min_value=1, step=1, key="place_order")
    
    conn = get_connection()
    c = conn.cursor()

    # Fetch menu items
    c.execute("SELECT item_id, item_name, price FROM Menu_Item")
    menu_items = c.fetchall()
    item_dict = {f"{name} - ₹{price}": (item_id, price) for item_id, name, price in menu_items}

    selected_item = st.selectbox("Select Item", list(item_dict.keys()))
    quantity = st.number_input("Quantity", min_value=1, step=1)

    if st.button("Confirm Order"):
        item_id, base_price = item_dict[selected_item]

        # Convert base_price to Decimal if needed
        base_price = Decimal(base_price)

        subtotal = base_price * quantity
        tip = round(Decimal("0.10") * subtotal, 2)
        gst = round(Decimal("0.08") * subtotal, 2)
        total_price = subtotal + tip + gst

        order_date = datetime.now().strftime("%Y-%m-%d")
        status = "Pending"

        # Insert into Orders table
        c.execute("""
            INSERT INTO Orders (cust_id, order_date, tip_price, gst_price, total_price, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (cust_id, order_date, tip, gst, total_price, status))

        order_id = c.lastrowid

        # Insert into Order_Tracking table
        c.execute("INSERT INTO Order_Tracking (order_id, status) VALUES (%s, %s)", (order_id, 'Preparing'))

        conn.commit()
        conn.close()

        st.success(f"Order placed successfully! Order ID: {order_id}")


elif selected == "Track Order":
    st.markdown("<h2 style='color:#FF6347;'>Track Your Order</h2>", unsafe_allow_html=True)
    order_id = st.number_input("Enter Your Order ID", min_value=1, step=1)
    
    if order_id:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT status FROM Order_Tracking WHERE order_id = %s", (order_id,))
        status = c.fetchone()
        conn.close()
        
        if status:
            st.success(f"Order Status: {status[0]}")
        else:
            st.error("Order not found")

elif selected == "Feedback":
    st.markdown("<h2 style='color:#FF6347;'>Give Feedback</h2>", unsafe_allow_html=True)
    cust_id = st.number_input("Customer ID", min_value=1, step=1)
    comments = st.text_area("Your Feedback")

    if st.button("Submit"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Feedback (cust_id, comment) VALUES (%s, %s)", (cust_id, comments))
        conn.commit()
        conn.close()
        st.success("Feedback submitted!")

elif selected == "Wishlist":
    st.markdown("<h2 style='color:#FF6347;'>Your Wishlist</h2>", unsafe_allow_html=True)
    
    cust_id = st.number_input("Enter Your Customer ID", min_value=1, step=1)
    
    conn = get_connection()
    c = conn.cursor()

    # Fetch available menu items
    c.execute("SELECT item_id, item_name FROM Menu_Item")
    menu_items = c.fetchall()
    
    if menu_items:
        item_dict = {f"{name} (ID: {item_id})": (item_id, name) for item_id, name in menu_items}
        selected_item = st.selectbox("Select Item to Add", list(item_dict.keys()))

        if st.button("Add to Wishlist"):
            item_id, item_name = item_dict[selected_item]
            c.execute("INSERT INTO Wishlist (wishlist_id, cust_id, item_id, name) VALUES (NULL, %s, %s, %s)", 
                      (cust_id, item_id, item_name))
            conn.commit()
            st.success(f"'{item_name}' added to your wishlist!")

    # Show existing wishlist
    st.markdown("### Your Current Wishlist")
    c.execute("SELECT name FROM Wishlist WHERE cust_id = %s", (cust_id,))
    wishlist_items = c.fetchall()

    if wishlist_items:
        for item in wishlist_items:
            st.write(f"🍽️ {item[0]}")
    else:
        st.info("Your wishlist is empty.")
    
    conn.close()

elif selected == "Profile":
    st.markdown("<h2 style='color:#FF6347;'>Your Membership Profile</h2>", unsafe_allow_html=True)
    cust_id = st.number_input("Enter Your Customer ID", min_value=1, step=1, key="mem")
    if cust_id:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM Membership WHERE cust_id = %s", (cust_id,))
        profile = c.fetchone()
        if profile:
            st.write(f"Membership ID: {profile[0]} | Joined on: {profile[2]} | Offer: {profile[3]}")
        else:
            st.warning("No membership found.")
        conn.close()
