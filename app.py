import streamlit as st

def intro():
    st.sidebar.success("Select a dashboard above.")

    st.markdown(
        """
        # Tailnode Assessment - 09-12-2025

        **👈 Select a dashboard from the dropdown on the left**

        ### Charts in Dashboard

        - Correlation Matrix
        - Time Series Analysis
        - Top producing Districts
        - Yield
        - Yield vs Production Area
        - Crop Wise Production

        ### Charts in Map View

        - tbd
    """
    )

def dashboardView():
    st.write("Dashboard View")

def mapView():
    st.write("Map View")

page_names_to_funcs = {
    "—": intro,
    "Dashboard View": dashboardView,
    "Map View": mapView,
}

demo_name = st.sidebar.selectbox("Choose a view", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()