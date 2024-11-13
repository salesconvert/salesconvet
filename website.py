import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="Sales Convert", page_icon="📈", layout="wide")

# Sidebar navigation
def sidebar_nav():
    with st.sidebar:
        st.title("Sales Convert")
        st.markdown("### Social Media Management Services")
        if st.button("Home"):
            st.session_state.page = 'home'
        elif st.button("Services"):
            st.session_state.page = 'services'
        elif st.button("Case Studies"):
            st.session_state.page = 'portfolio'
        elif st.button("Blog"):
            st.session_state.page = 'blog'
        elif st.button("Contact Us"):
            st.session_state.page = 'contact'
        else:
            st.session_state.page = 'home'

# Home Page
def home_page():
    st.title("Welcome to Sales Convert")
    st.markdown("""
    ## Your Partner in Digital Marketing
    We specialize in **Social Media Management** to help your business grow online. Our services are designed to engage your audience, drive traffic, and increase conversions. Let's work together to build your brand presence on platforms like **Facebook**, **Instagram**, **LinkedIn**, and **Twitter**.
    """)

    st.image("https://via.placeholder.com/1500x500.png", use_column_width=True)
    st.write("### Why Choose Us?")
    st.markdown("""
    - Proven results with ROI-driven campaigns.
    - Expertise in various social media platforms.
    - Data-driven strategies for targeted marketing.
    - Dedicated customer support to ensure smooth communication.
    """)

# Services Page
def services_page():
    st.title("Our Services")
    
    st.markdown("""
    ### Social Media Management Services
    We offer a range of services tailored to your business needs:
    
    1. **Social Media Strategy**: Tailored strategies to grow your brand.
    2. **Content Creation**: Engaging posts and videos designed for your target audience.
    3. **Community Engagement**: Direct engagement with your followers to drive loyalty.
    4. **Advertising Campaigns**: Facebook, Instagram, LinkedIn Ads.
    5. **Analytics & Reporting**: Track the success of campaigns and optimize.

    For more information or to get started, reach out to us on our [contact page](#Contact-Us).
    """)

# Portfolio/Case Studies Page
def portfolio_page():
    st.title("Case Studies")

    st.markdown("""
    ### Success Stories
    Take a look at how we’ve helped businesses like yours grow their online presence.
    """)

    # Sample case study (You can dynamically load this from a database or file)
    df = pd.DataFrame({
        'Campaign': ['Campaign A', 'Campaign B', 'Campaign C'],
        'Platform': ['Instagram', 'Facebook', 'LinkedIn'],
        'ROI': [150, 200, 180],
    })

    st.dataframe(df)

# Blog Page
def blog_page():
    st.title("Blog")
    st.markdown("""
    ### Latest Articles
    Stay up-to-date with the latest trends in social media marketing:
    - **How to Build a Successful Social Media Strategy in 2024** [Read more]
    - **Top 10 Social Media Mistakes to Avoid** [Read more]
    - **The Power of Facebook Ads for Small Businesses** [Read more]
    """)

# Contact Page
def contact_page():
    st.title("Contact Us")
    st.markdown("""
    If you're ready to take your social media to the next level, get in touch with us today!
    """)
    
    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit = st.form_submit_button("Send Message")
        
        if submit:
            st.success(f"Thank you {name}! We'll get back to you soon.")
        else:
            st.warning("Please fill out all fields.")

# Analytics Page (Dashboard for Clients)
def analytics_page():
    st.title("Analytics Dashboard")
    st.markdown("""
    ### Campaign Overview
    Here you can view the performance of your social media campaigns.

    - **Total Engagements**
    - **Impressions & Reach**
    - **Revenue Generated**
    """)

    # Sample Analytics Data
    data = pd.DataFrame({
        'Platform': ['Facebook', 'Instagram', 'LinkedIn'],
        'Total Engagements': [1200, 3000, 1500],
        'Revenue': [5000, 6000, 4000],
    })
    
    st.dataframe(data)

    # Visualizing Data
    fig = px.bar(data, x='Platform', y='Revenue', title="Revenue by Platform")
    st.plotly_chart(fig)

# Main App Logic
def main():
    # Initialize session state if not set
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    sidebar_nav()
    
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'services':
        services_page()
    elif st.session_state.page == 'portfolio':
        portfolio_page()
    elif st.session_state.page == 'blog':
        blog_page()
    elif st.session_state.page == 'contact':
        contact_page()
    elif st.session_state.page == 'analytics':
        analytics_page()

if __name__ == "__main__":
    main()
