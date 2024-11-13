import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from datetime import datetime
import plotly.express as px
from pathlib import Path

# Configure Streamlit page settings
st.set_page_config(
    page_title="Sales Convert",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
DB_PATH = Path('sales_convert.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create users table with enhanced security
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create sales data table
    c.execute('''CREATE TABLE IF NOT EXISTS sales_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  date DATE,
                  revenue FLOAT,
                  platform TEXT,
                  campaign TEXT,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# Security functions
def hash_password(password):
    """Create a secure hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    """Verify the password against its hash"""
    return hash_password(password) == hash_value

# Database operations
def create_user(name, email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, password_hash FROM users WHERE email = ?', (email,))
    result = c.fetchone()
    conn.close()
    
    if result and verify_password(password, result[1]):
        return result[0]
    return None

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Initialize database
init_db()

# Sidebar navigation
def sidebar_nav():
    with st.sidebar:
        st.title("Sales Convert")
        if st.session_state.user_id:
            if st.button("Dashboard"):
                st.session_state.page = 'dashboard'
            if st.button("Add Sales Data"):
                st.session_state.page = 'add_sales'
            if st.button("Analytics"):
                st.session_state.page = 'analytics'
            if st.button("Profile"):
                st.session_state.page = 'profile'
            if st.button("Logout"):
                st.session_state.user_id = None
                st.session_state.page = 'login'
        else:
            if st.button("Login"):
                st.session_state.page = 'login'
            if st.button("Register"):
                st.session_state.page = 'register'

# Page functions
def login_page():
    st.title("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user_id = verify_user(email, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.page = 'dashboard'
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")

def register_page():
    st.title("Register")
    
    with st.form("register_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if create_user(name, email, password):
                st.success("Registration successful! Please login.")
                st.session_state.page = 'login'
                st.experimental_rerun()
            else:
                st.error("Email already exists!")

def add_sales_data(user_id, date, revenue, platform, campaign):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO sales_data (user_id, date, revenue, platform, campaign) VALUES (?, ?, ?, ?, ?)',
        (user_id, date, revenue, platform, campaign)
    )
    conn.commit()
    conn.close()

def get_user_sales_data(user_id):
    conn = sqlite3.connect(DB_PATH)
    query = '''
    SELECT date, revenue, platform, campaign 
    FROM sales_data 
    WHERE user_id = ? 
    ORDER BY date DESC
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

def dashboard_page():
    st.title("Dashboard")
    
    # Get user's sales data
    df = get_user_sales_data(st.session_state.user_id)
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue Overview")
            fig = px.line(df, x='date', y='revenue', title='Revenue Trend')
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("Platform Distribution")
            fig = px.pie(df, values='revenue', names='platform', title='Revenue by Platform')
            st.plotly_chart(fig)
        
        st.subheader("Recent Sales Data")
        st.dataframe(df.head())
    else:
        st.info("No sales data available. Add some data to see your dashboard!")

def add_sales_page():
    st.title("Add Sales Data")
    
    with st.form("add_sales_form"):
        date = st.date_input("Date")
        revenue = st.number_input("Revenue", min_value=0.0)
        platform = st.selectbox("Platform", ["Facebook", "Instagram", "LinkedIn", "Twitter", "Other"])
        campaign = st.text_input("Campaign Name")
        submit = st.form_submit_button("Add Sales Data")
        
        if submit:
            add_sales_data(st.session_state.user_id, date, revenue, platform, campaign)
            st.success("Sales data added successfully!")

def analytics_page():
    st.title("Analytics")
    
    df = get_user_sales_data(st.session_state.user_id)
    
    if not df.empty:
        # Time period selection
        time_period = st.selectbox(
            "Select Time Period",
            ["Last 7 days", "Last 30 days", "Last 90 days", "All time"]
        )
        
        # Filter data based on selected time period
        today = pd.Timestamp.now().date()
        if time_period == "Last 7 days":
            df = df[df['date'] >= str(today - pd.Timedelta(days=7))]
        elif time_period == "Last 30 days":
            df = df[df['date'] >= str(today - pd.Timedelta(days=30))]
        elif time_period == "Last 90 days":
            df = df[df['date'] >= str(today - pd.Timedelta(days=90))]
        
        # Display analytics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
        with col2:
            st.metric("Average Revenue", f"${df['revenue'].mean():,.2f}")
        with col3:
            st.metric("Total Campaigns", len(df['campaign'].unique()))
        
        # Advanced visualizations
        st.subheader("Campaign Performance")
        campaign_data = df.groupby('campaign')['revenue'].sum().reset_index()
        fig = px.bar(campaign_data, x='campaign', y='revenue', title='Revenue by Campaign')
        st.plotly_chart(fig)
        
        st.subheader("Platform Analysis")
        platform_data = df.groupby('platform').agg({
            'revenue': ['sum', 'mean', 'count']
        }).reset_index()
        platform_data.columns = ['Platform', 'Total Revenue', 'Average Revenue', 'Number of Sales']
        st.dataframe(platform_data)
    else:
        st.info("No data available for analysis. Please add some sales data first!")

# Main app logic
def main():
    sidebar_nav()
    
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'register':
        register_page()
    elif st.session_state.user_id:
        if st.session_state.page == 'dashboard':
            dashboard_page()
        elif st.session_state.page == 'add_sales':
            add_sales_page()
        elif st.session_state.page == 'analytics':
            analytics_page()
    else:
        st.session_state.page = 'login'
        st.experimental_rerun()

if __name__ == "__main__":
    main()
