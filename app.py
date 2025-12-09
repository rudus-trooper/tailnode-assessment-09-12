import streamlit as st
import pandas as pd

from dashboard.utils import (
    getCorrelationMatrix,
    getTimeSeries,
    getTopProducingDistricts,
    getYieldByDistrict,
    getYieldVsArea,
    getCropWiseProduction,
)

# load dataset
@st.cache_data
def load_data():
    return pd.read_csv("crop_data.csv")

def intro():
    st.sidebar.success("Select a dashboard above.")

    st.markdown(
        """
        # Tailnode Assessment - 09-12-2025

        ** Select a dashboard from the dropdown on the left**

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
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Crop Production & Yield Dashboard</h1>", unsafe_allow_html=True)
    df = load_data()
    
    # FILTERS
    filterContainer = st.container(border=True)
    with filterContainer:
        st.subheader("Filters")
        colLeft, colRight = st.columns([3, 1])
        with colLeft:
            col1, col2 = st.columns(2)
            
            # State filter
            selectedStates = col1.multiselect("State", df["State"].unique().tolist())
            
            # District filter - filtered by selected states
            if selectedStates:
                district_options = df[df["State"].isin(selectedStates)]["District"].unique().tolist()
                default_district = [district_options[0]] if district_options else []
            else:
                district_options = []
                default_district = []
            selectedDistricts = col2.multiselect("District", district_options, default=default_district, disabled=not selectedStates)
            
            col3, col4 = st.columns(2)
            
            # Crop filter - filtered by selected states and districts
            if selectedDistricts:
                filtered_df = df[df["State"].isin(selectedStates) & df["District"].isin(selectedDistricts)]
                crop_options = filtered_df["Crop"].unique().tolist()
                default_crop = [crop_options[0]] if crop_options else []
            else:
                crop_options = []
                default_crop = []
            selectedCrops = col3.multiselect("Crop", crop_options, default=default_crop, disabled=not selectedDistricts)
            
            # Season filter - filtered by all previous selections
            if selectedCrops:
                filtered_df = df[
                    df["State"].isin(selectedStates) & 
                    df["District"].isin(selectedDistricts) & 
                    df["Crop"].isin(selectedCrops)
                ]
                season_options = filtered_df["Season"].unique().tolist()
                default_season = [season_options[0]] if season_options else []
            else:
                season_options = []
                default_season = []
            selectedSeasons = col4.multiselect("Season", season_options, default=default_season, disabled=not selectedCrops)
        
        with colRight:
            # Year filter - filtered by all previous selections
            if selectedSeasons:
                filtered_df = df[
                    df["State"].isin(selectedStates) & 
                    df["District"].isin(selectedDistricts) & 
                    df["Crop"].isin(selectedCrops) & 
                    df["Season"].isin(selectedSeasons)
                ]
                year_options = filtered_df["Year"].unique().tolist()
                default_year = [year_options[0]] if year_options else []
            else:
                year_options = []
                default_year = []
            selectedYears = st.multiselect("Year", year_options, default=default_year, disabled=not selectedSeasons)
    
    # Compute KPI DataFrames
    corrDf = getCorrelationMatrix(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    tsDf = getTimeSeries(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    topDistDf = getTopProducingDistricts(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    yieldDf = getYieldByDistrict(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    scatterDf = getYieldVsArea(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    cropProdDf = getCropWiseProduction(df, selectedStates, selectedDistricts, selectedCrops, selectedSeasons, selectedYears)
    st.markdown("---")
    kpiContainer = st.container()

    with kpiContainer:
        col0, col00 = st.columns(2)
        with col0:
            st.subheader("Correlation Matrix")
            st.dataframe(corrDf, use_container_width=True)

        with col00:
            st.subheader("Time Series Analysis")
            if not tsDf.empty:
                st.line_chart(tsDf.set_index("Year"))
            else:
                st.write("No data")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top Producing Districts")
            if not topDistDf.empty:
                st.bar_chart(topDistDf.set_index("District"))
            else:
                st.write("No data")

        with col2:
            st.subheader("Yield (District Level)")
            st.dataframe(yieldDf, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Yield vs Production Area")
            if not scatterDf.empty:
                st.scatter_chart(scatterDf)
            else:
                st.write("No data")

        with col4:
            st.subheader("Crop-wise Production")
            if not cropProdDf.empty:
                st.line_chart(cropProdDf.set_index("Year"))
            else:
                st.write("No data")


def mapView():
    st.write("Map View")

page_names_to_funcs = {
    "—": intro,
    "Dashboard View": dashboardView,
    "Map View": mapView,
}

demo_name = st.sidebar.selectbox("Choose a view", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()