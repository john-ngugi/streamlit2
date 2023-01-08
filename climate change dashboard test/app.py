import streamlit as st 
import folium 
import plotly.express as px 
import pandas as pd
import pdb 


st.set_page_config(
page_title="Climatology And Environmental Dashboard",
page_icon=":earth_africa:",
layout="wide"
)
st.title("CLIMATOLOGY AND ENVIRONMENTAL DASHBOARD")
st.subheader("A Data Oriented And reliable Source of Climatology And environmental Data and Visualizations ")
st.caption("Powered by Taita Taveta University")
st.markdown("---")

#add data 

df = pd.read_excel(
    io="./kenya-carbon-co2-emissions.xlsx",
    engine="openpyxl",
    sheet_name="kenya-carbon-co2-emissions",
    usecols="A:C"
)
cell_hover = {  # for row hover use <tr> instead of <td>
    'selector': 'td:hover',
    'props': [('background-color', '#ffffb3')]
}
# temperature timeseries
df_temp_ts=pd.read_csv(
    "./tas_timeseries_annual_cru_1901-2021_KEN.csv",
    skiprows=1
)

#precipitation data 

df_precip = pd.read_csv(
    "./pr_climatology_annual-monthly_cru_1991-2020_KEN.csv",
    skiprows=1
)

#annual precipitation 

df_annual_precip = pd.read_excel(
    io="./kenya precipitation anual.xlsx",
    engine="openpyxl",
    sheet_name="Sheet1",
   
)

#precipitation

df_temp = pd.read_csv(
   "./tas_climatology_annual-monthly_cru_1991-2020_KEN.csv",
   skiprows=1,
)

#select the total kilotons of co2
df_co2_minmax=df["  TotalKilotonsofCo2"]

#calculate change in co2

maxCo2=df_co2_minmax.max()
minCo2=df_co2_minmax.min()

change_in_tktco2=maxCo2-minCo2

#select temperature annual max and min 

df_temp_minmax=df_temp_ts["Kenya"]
maxTemp=df_temp_minmax.max()
minTemp=df_temp_minmax.min()

change_in_temp = maxTemp-minTemp

# select precipitation 


df_annual_precip_minmax=df_annual_precip["value"]
maxPrecip=df_annual_precip_minmax.max()
minPrecip=df_annual_precip_minmax.min()

change_in_precip = maxPrecip-minPrecip


st.header("Major Climate Change Indicators")
col1,col2,col3 = st.columns(3)

with col1:
    st.metric(label="Temperature",
    value="25.2 °c",
    delta=str(round(change_in_temp,0)) + "°c",
    delta_color="inverse"
    )

with col2:
    st.metric(label="Precipitation",
    value="726.1 mm",
    delta= str(round(change_in_precip,1)) + "mm",
    )


with col3:
    st.metric(label="Carbon Emissions",
    value=str(round(maxCo2,1)) +"KT",
    delta= str(round(change_in_tktco2,1)) + "KT",
    delta_color="inverse"

    )    


st.markdown("##")
st.markdown("---")


st.sidebar.header("Make filters Here: ")

Date=st.sidebar.multiselect("Select Date: ",
options=df["date"].unique(),
)

st.markdown("##")
st.markdown("##")
st.header("Carbon Emissions ")
st.subheader("carbon emission in Kenya 1990-2019")
st.dataframe(df)

column1,column2 = st.columns(2)

fig_co2 = px.bar(
    df,
    x='  TotalKilotonsofCo2',
    y="date",
    title="<b> total carbon emissions over the years </b>",
    template="plotly_white",
)

fig_co2.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

fig_co2Metric= px.bar(
    df,
    x='    Per Capita Metric Tons Per Capita',
    y="date",
    title="<b> Per Capita Metric Tons carbon emissions over the years </b>",
    template="plotly_white",
    color_discrete_sequence = ["#FF4B4B"] 
)
fig_co2Metric.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
column1.plotly_chart(fig_co2)
column2.plotly_chart(fig_co2Metric)

st.markdown("---")

st.header("Temperature")
st.dataframe(df_temp_ts.style.highlight_max(axis=0))

fig_temp = px.line(
    df_temp_ts,
    x="Variable",
    y= "Kenya",
    orientation="v",
    title="<b> Annual Temperature In kenya 1901-2021 </b>",
    color_discrete_sequence = ["#2AAA8A"],
    template="plotly_white",
)


st.plotly_chart(fig_temp,use_container_width=True)

st.markdown("---")

df_trees= pd.read_excel(
    io="./cartodb-query.xlsx",
    engine="openpyxl",
    sheet_name="cartodb-query",
    usecols="D:H"
)

st.header("Forest cover in kenya")
st.subheader("map showing the map points")

st.markdown("##")
column1,column2 = st.columns(2)
column1.dataframe(df_trees,height=500)
column2.map(df_trees,use_container_width=True)
#st.dataframe(df_trees)

st.markdown("##")
st.markdown("---")

st.header("precipitation")
st.subheader(" Analysis on annual and monthly precipitation in different regions of kenya")

#monthly precipitation 1991-2020


st.dataframe(df_precip)
col1,col2=st.columns(2)

fig_precip = px.bar(
    df_precip,
    x="Variable",
    y="Annual",
    title="<b> annual precipitation for different kenyan regions  </b>"
)

#st.dataframe(df_annual_precip)

fig_precip_annual = px.bar(
    df_annual_precip,
    x="year",
    y="value",
    title="<b> annual precipitation per 30 year period </b>",
    color= "year",
)
fig_precip_annual.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

col2.plotly_chart(fig_precip_annual)
col1.plotly_chart(fig_precip)
st.write(""" In the precipitation category we see not much change as the annual rainfall over the years has pretty much remained at 
almost the same level,However since 1931 the change has been positive and at 2020 we can see it has suppersed all the other years. 
This is not thretening but monitoring of anuual rainfall patterns is important. """)

st.markdown("##")



