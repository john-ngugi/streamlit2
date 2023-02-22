import streamlit as st 
import plotly.express as px 
import pandas as pd
import leafmap.kepler as leafmap
import json 
from ipyleaflet import GeoJSON 
import geemap.foliumap as geemap
import ee 
import time
from shapely.geometry import shape
import geopandas as gpd
from datetime import date
import datetime


############ add google earth engigne to our app ######################


# login Data from the downloaded JSON file super secrety do not share with anyone 


json_data = '''
{
  "type": "service_account",
  "project_id": "ee-muthamijohn",
  "private_key_id": "ba887a502e5b94d1c484429fb58de81fda8bf013",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCnBlXhl3LS4NDO\nO/32iManSz+kH+YFYfjqTIutkj+JUJ2CVywYIB85cJVGbQ0k23SVS1kx0wrhlA+b\nBzDwtsVBFev4/w6NeZ/YeqL4U/Ky9SP7t6wAmdDkijP9/EtP5IonxuVLYC5trGtw\nL5z6nWgfub0O+A6oTee1bdc3VSlgjt/wKcJwsHFMIr/Brg0lf3chwkBRh0+X1Ntd\np1l1hQVQCshLs32PoDds6ep3cEOpIf/X7diTT1uvprEPUQlNsQf4RzxPBvvqyRZb\nPo1Zv1JO+BAHntC8Z2L3aPmqot9Bq94BqLZm+pRzusoCRJ/Pe+V8J66rM1gR3jup\nEwI3K6abAgMBAAECggEABp5+DmY9sXtU8XdeXyplRQGUahRH8PREmw4H7KVpFmLQ\nrl1DoBXvZtiK8eZZQpnePhrLh0/0lG/7r/C4ncsaEhqksvkL28tzUqIf9A6cbAv1\nYYDFgXIwqkq+OLu9q4YRFSmqsjJp/jd6ooPtVd+hd4n/otvUKOAj5WrCJq03UJFu\n8NEP2aVF4OiVjYLhN5DaN1I+b7lsAA88ZcAYDYxOKiRvkIEyD2S3lJg46+cfIRKz\nbuNV65tWDsDWQL9djB8bRgmUnXjFmEfjiBxWyqv4JF2Xs4/bEuPmX3u06Zfy9UqE\nt/lhvXQ/s0Ou6ayrbDN7jd8yJuIl8EBDQAF6BWGSwQKBgQDWaroZc75ETtBEU401\nU8iBBSKI4YLY4RTvbCeaKBcmNGLzqk0nIdX4NxOwMm8P1LiDYJeOcKkxNTB05lNz\n526MomJ7rHx+vFjpi2a068+FuxczmVeEIbgDM8e2jttBjh6PauUxHEbcOsd7k2Je\nunDCHDUjjaCdRaMrWRT7m+qXywKBgQDHarRQ1pdNxmTjeAVyw1s8br6coVrL94Za\nPfBo6eFDcfsrPOdx7iq1NFuoOCWwZm1hBqhWJYWNqwbVS+G4ESaqnTY5LZTzR67X\n2LobeV/ZegpU7KWBt8Pes4ksMQZedNXuQmtZuKpNEXdAV5WKDgPeSIhdLNdevFJf\n99cv/8sycQKBgQCHy3wlVnpwBII+Y7QQzAk2PSxMCJa4CIUbxSGnrjBLD+6DZ54J\nZJKA61DazHYuToi1G92gZpWhBpCz2JON2krXYpiAvxLxqROehZz8hEQf7AebtEgK\n9Nf3nzmi0wLll76fEhIpckEmhUuFZihs2iNDrF2zMKVCNbJLZ9W0LGD81QKBgGEC\nzdmNq2mQnD/0gWIFG3tYvK3h6RPUxK1d+HhxXr660l+Eb2uDW49vey9osR0RlyBe\nZsIR2tjCXL6i/ZnX7iGN/XTvcciwFKS4sEDxWOmpbyFFRnbGeSj72j1/VAPbfr87\n3JF3PpHjb0oD0aGpk8QtMPly+QsDPmelYC/flnBhAoGBALqZ13BjABwBTKimTcmC\nQiI7LvdsAAdO9k4LjSKKSmCyUTAN4hCc5gqKPVxv62ao+rxbHzRqGNvouXePVb8z\nZbXzfXrWLJxci43wkq3UOoB3t5DTkTGQQveD1tFiVFwLrVZUahoDCerMSQRo449s\n1hx46+u8FvPA57M640V7arV8\n-----END PRIVATE KEY-----\n",
  "client_email": "kenya-environmental-dashboard@ee-muthamijohn.iam.gserviceaccount.com",
  "client_id": "101824526217381631179",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kenya-environmental-dashboard%40ee-muthamijohn.iam.gserviceaccount.com"
}
'''

# Preparing values
json_object = json.loads(json_data, strict=False)
service_account = json_object['client_email']
json_object = json.dumps(json_object)
#Authorising the app
credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
ee.Initialize(credentials)

# service_account =  "kenya-environmental-dashboard@ee-muthamijohn.iam.gserviceaccount.com"
# #credentials = ee.ServiceAccountCredentials(service_account, key_data=json_object)
# credentials = compute_engine.Credentials(scopes=['https://www.googleapis.com/auth/earthengine'])
# ee.Initialize(credentials)


ROI1=ee.FeatureCollection('users/muthamijohn/kwanza_constituency')
lc = ee.ImageCollection('MODIS/006/MCD12Q1')
S2CH4=ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4").filterDate('2019-01-01', '2021-12-30').select('CH4_column_volume_mixing_ratio_dry_air_bias_corrected').mean()





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
with st.spinner(' building application....'):
    time.sleep(5)
    #st.success('Done!')
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
    totalkilotonsofCo2=df["  TotalKilotonsofCo2"]

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

    Date=st.sidebar.multiselect("Select carbon Date: ",
    options=df["date"].unique(),
    )

    tempSelection=st.sidebar.multiselect(
        "select temperature date",
        options=df_temp["Variable"].unique()
    )

    # Selection1=st.sidebar.multiselect(
    #      "select temperature date",
    #     options=df_temp["Variable"].unique()
    #  )

    precipSelection=st.sidebar.multiselect(
        "select precipitation date",
        options=df_precip["Variable"].unique()
    )


    st.markdown("##")
    st.markdown("##")
    st.header("Carbon Emissions ")
    st.subheader("carbon emission in Kenya 1990-2019")
    #st.dataframe(df)


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

    fig_transactions = px.line(
        df_temp_ts,
        x="Variable",
        y= "Kenya",
        orientation="v",
        title="<b> Annual Temperature In kenya 1901-2021 </b>",
        color_discrete_sequence = ["#2AAA8A"],
        template="plotly_white",
    )
    fig_transactions.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
    # xaxis=(dict(showgrid=False)),
        yaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_transactions,use_container_width=True)

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
# st.subheader("map showing internet cable lines in the ocean")
# m = leafmap.Map(center=[20, 0], zoom=1)
# lines = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/cable_geo.geojson'
# m.add_geojson(lines, layer_name="Cable lines")
# m.to_streamlit()
# st.write(ROI1)

########################## google earth engine #################################

dateCol1,dateCol2= st.columns(2)

with dateCol1:
    startDate = st.date_input("enter start date", datetime.date(2018,5,1))
    startDate = startDate.strftime("%Y-%m-%d")

with dateCol2:
    endDate = st.date_input("enter end date",datetime.date(2018,8,31))
    endDate = endDate.strftime("%Y-%m-%d")
 



with st.spinner("fuelling the earth engine...."):
    # Define the region of interest
    #roi = ee.Geometry.Rectangle([-122.5, 37.5, -122, 38])

    # Define the Sentinel-2 image collection
    s2 = ee.ImageCollection('COPERNICUS/S2') \
        .filterBounds(ROI1) \
        .filterDate(startDate, endDate) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))

    # Define a function to compute the NDVI statistics for an image
    def compute_ndvi_stats(image):
        ndvi = image.normalizedDifference(['B8', 'B4'])
        stats = ndvi.reduceRegion(
            reducer=ee.Reducer.minMax().combine(reducer2=ee.Reducer.mean(), sharedInputs=True),
            geometry=ROI1,
            scale=10,
            bestEffort=True
        )
        return ee.Feature(None, {
        'date': image.date().format('YYYY-MM-dd'),
        'mean_ndvi': stats.get('nd_mean'),
        'min_ndvi': stats.get('nd_min'),
        'max_ndvi': stats.get('nd_max')
    })

    # Map the function over the image collection and convert the resulting feature collection to a pandas dataframe
    features = s2.map(compute_ndvi_stats).getInfo()['features']
    data = []
    for feature in features:
        properties = feature['properties']
        data.append({
            'date': properties['date'],
            'mean_ndvi': properties['mean_ndvi'],
            'min_ndvi': properties['min_ndvi'],
            'max_ndvi': properties['max_ndvi']
        })
    df_all = pd.DataFrame(data).set_index('date')
   

    #cloud mask function
    def maskS2clouds(image):
        return image.updateMask(image.select('QA60').eq(0))

    #importing the image collection and filtering the date and cloud percentage and mapping the cloud filter function 
    S2=ee.ImageCollection('COPERNICUS/S2').filterDate(startDate,endDate).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1)).map(maskS2clouds).filterBounds(ROI1)
    #creating a single image from the sentinel 2 image collection 
    image=S2.median().clip(ROI1)

    #S2=ee.ImageCollection("COPERNICUS/S2_HARMONIZED").filterDate('2019-01-01', '2021-12-30').filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1)).map(maskS2clouds).filterBounds(ROI1)
    S2CH4=ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CH4").filterDate(startDate,endDate ).select('CH4_column_volume_mixing_ratio_dry_air_bias_corrected').filterBounds(ROI1).mean().clip(ROI1)

    #calculating the ndvi and assining the image to a variable i.e NDVI 
    NDVI=image.normalizedDifference(['B8','B4'])

    mean=S2.mean()

    # calculate SARVI 
    SARVI = mean.expression('((NIR-(Red-1*(Blue-Red)))/(NIR+(Red-1*(Blue-Red))))*(1+0.5)', {
                                'NIR' : mean.select('B8'),
                                'Red' : mean.select('B4'),
                                'Blue' : mean.select('B2')
                            })


    meanSARVI= SARVI.reduceRegion(ee.Reducer.mean(),ROI1,10,1e10)

    # getting the min max and mean values of our indeces

    def addNDVI(S2):
        nir = S2.select('B8')
        red = S2.select('B4')
        ndvi1 = S2.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return S2.addBands(ndvi1)


    withNDVI = S2.map(addNDVI);
    ndvi = withNDVI.select('NDVI');

    def extractMinMaxMean(image):
        return image.reduceRegions(**{
        'collection': ROI1,
        'reducer':ee.Reducer.minMax().combine(ee.Reducer.mean(), '', True), 
    })
        
    ndviMaxMin= withNDVI.map(extractMinMaxMean)

    sampleResult= ndviMaxMin.first().getInfo()

    columnsNDVI=sampleResult['features']
    NDVIValues=columnsNDVI[0]
    vals=NDVIValues['properties']
    NDVININMAX=vals['NDVI_max']
    ndvimin=vals['NDVI_min']
    ndvimean=vals['NDVI_mean']


    #creating the map instance i.e geemap 
    Map=geemap.Map(center=(1.1641,35.0),zoom=12)
#defining the visualization parametters of different images 
    st.markdown("###")
# create custom visualization colors

    st.subheader("pick visualization colors")

# for ndvi    
    st.markdown("###### NDVI: ")
#create 3 columns for high medium and low ranges 
    
    colorCol1,colorCol2,colorCol3=st.columns(3)

    with st.spinner('painting map....'):
        with colorCol1:
            ndvism=st.color_picker("pick low values colors",value="#FC2D00")    
        with colorCol2:    
            ndvimd=st.color_picker("pick medium value colors",value="#FFFFFF")
        with colorCol3:     
            ndvilg=st.color_picker("pick high value colors",value="#228b22")

    S2Vis = {
    'min': 0,
    'max': 3000,
    'bands':['B4','B3','B2']
    }
    ndviVis={
        'min':-1,
        'max':1,
        #'palette':['#1e90ff','#ff6347','red','#ff4500','#f0e68c','#fcf75e','#ffff66','yellow','yellow','#32cd32','green','green','#228b22']
        'palette':[ndvism,ndvimd,ndvilg]
    }


    methVis={
    'min': 1750,
    'max': 1900,
    'palette':['black','blue','purple','cyan','green','yellow','red']
    }
    s2Vis={
        'min':0,
        'max':3000,
        'bands':['B4','B3','B2']
        }


with st.spinner(' getting the catographers....'):
    #time.sleep(5)
    Map.addLayer(S2CH4,methVis,'methane concentration')
    Map.addLayer(S2,s2Vis,'sentinel 2 imagery');
    #adding the map layers to the map instance     
    Map.addLayer(S2,S2Vis,'map1')
    Map.addLayer(NDVI,ndviVis,'ndvi')
    
#Map.addLayer(S2,s2Vis,'sentinel 2 imagery')
#st.success('Done!')

Map.to_streamlit()

st.subheader('quick analysis:')
st.write(f"MAX NDVI: {NDVININMAX} " )
st.write(f"MIN NDVI: {ndvimin} " )
st.write(f"MEAN NDVI: {ndvimean} " )

st.dataframe(df_all, use_container_width=True)
fig_ndvitrend = px.line(
        df_all,
        x=df_all.index,
        y= "mean_ndvi",
        orientation="v",
        title="<b> mean ndvi trend </b>",
        color_discrete_sequence = ["#2AAA8A"],
        template="plotly_white",
    )
fig_ndvitrend.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
# xaxis=(dict(showgrid=False)),
    yaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_ndvitrend,use_container_width=True)




