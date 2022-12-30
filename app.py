import streamlit as st 
import folium 
import plotly.express as px 
import pandas as pd


st.set_page_config(
page_title="climatology and environmental dashboard",
page_icon=":earth_africa:",
layout="wide"
)
st.title("Climatology And Environmental Dashboard")
st.subheader("A Data Oriented And reliable Source of Climatology And environmental Data and Visualizations ")
st.caption("Powered by Taita Taveta University")
st.markdown("---")
df = pd.read_excel(
    io="./kenya-carbon-co2-emissions.xlsx",
    engine="openpyxl",
    sheet_name="kenya-carbon-co2-emissions",
    usecols="A:C"
)
st.subheader("Major Climate Change Indicators")
col1,col2,col3 = st.columns(3)

with col1:
    st.metric(label="temperature",
    value="30 °c",
    delta="2.5°c"
    )

with col2:
    st.metric(label="precipitation",
    value="1023 mm",
    delta="-50 mm"
    )


with col3:
    st.metric(label="Carbon Emissions",
    value="13000 m²",
    delta="-1200 m²"
    )        



st.sidebar.header("Make filters Here: ")

Date=st.sidebar.multiselect("Select Date: ",
options=df["date"].unique(),
)

st.markdown("##")
st.markdown("##")
st.subheader("carbon emission in Kenya 1990-2019")
st.dataframe(df)
fig_co2 = px.bar(
    df,
    x="date",
    y=' Per Capita Metric Tons Per Capita',
    title="<b> total carbon emissions over the years </b>",
    template="plotly_white",
)

st.plotly_chart(fig_co2)