import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components
import pickle
import requests
import pandas as pd
from datetime import datetime
from email.message import EmailMessage
import ssl 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
from database_service import db_connection,insert_subscribers,check_subscribers
import time
import re


#Setting Page Configuration 
st.set_page_config(page_title="HeatIndex Prediction", page_icon="♨️", layout="wide", initial_sidebar_state="expanded", menu_items=None)

# Title
st.title("HeatIndex Prediction")

# Contents
st.subheader("Contents")

# Adding Page elements anchors
st.markdown("- [What Are Heatwaves?](#what-are-heatwaves)")
st.markdown("- [Information On The Factors That Contribute To Heatwave](#information-on-the-factors-that-contribute-to-heatwave)")
st.markdown("- [Prediction Methods](#prediction-methods)")
st.markdown("- [Heatwave Impacts](#heatwave-impacts)")
st.markdown("- [Heatwave Preparation and Response](#heatwave-preparation-and-response)")
st.markdown("- [Heatwave Dashboard](#heatwave-dashboard)")
st.markdown("- [Heatwave Forcasting](#heatwave-forcasting)")
st.markdown("- [Heatwave Alert Service](#for-getting-heatwave-alerts-please-subscribe-to-our-mail-service)")

# Calculation Result Container
calci_result=st.container()

# Data Container
data_container=st.container()

# Defining Calculator in Sidebar Section
st.sidebar.header("Heat Index Calculator")

# Air Temperature
st.sidebar.markdown("Air Temperature :thermometer:")
air_temp_radio=st.sidebar.radio("Air Temperature",["Degree","Ferenheit"],label_visibility="collapsed")

# Default values and limit changer for air temperature box
if air_temp_radio=="Ferenheit":
    air_temp=st.sidebar.number_input("Air Temperature",0.0,200.0,75.2,label_visibility="collapsed")
else:
    air_temp=st.sidebar.number_input("Air Temperature",-60.0,80.0,24.0,label_visibility="collapsed")

# Dew Point
st.sidebar.markdown("Dew Point Temperature :thermometer:")
dew_temp_radio=st.sidebar.radio("Dew Temperature",["Degree","Ferenheit"],label_visibility="collapsed")

# Default values and limit changer for dew point box
if dew_temp_radio=="Ferenheit":
     dew_temp=st.sidebar.number_input("Dew Temperature",0.0,200.0,75.2,label_visibility="collapsed")
else:
    dew_temp=st.sidebar.number_input("Dew Temperature",-60.0,80.0,24.0,label_visibility="collapsed")

#Function to convert temperature in degree celcius for further calculation
def convert(air_temp_radio,air_temp,dew_temp_radio,dew_temp):
    if(air_temp_radio=="Ferenheit"):
       air_temp1=(air_temp-32)*5/9
    else:
        air_temp1=air_temp

    if(dew_temp_radio=="Ferenheit"):
       dew_temp1=(dew_temp-32)*5/9
    else:
        dew_temp1=dew_temp

    return air_temp1,dew_temp1


container=st.sidebar.container()
btn=st.sidebar.button("Submit")

if btn:
    air_temp1,dew_temp1=convert(air_temp_radio,air_temp,dew_temp_radio,dew_temp)
    
#Caching Model
@st.cache_data()
def load_model():
    model=pickle.load(open("model.pkl","rb"))
    return model

if btn:
    model=load_model()
    HI=model.predict([[0,air_temp1,dew_temp1,5]])


if btn:
    container.subheader("Heat Index is:")
    container.text(round(HI[0]))

# Unit changer for parameters
if air_temp_radio=="Degree":
    Unit1="C"
else:
    Unit1="F"

if dew_temp_radio=="Degree":
    Unit2="C"
else:
    Unit2="F"


# Showing Calculator Results 
if btn:
    calci_result.write("---")
    str1=f"- ###### Air Temperature: {str(air_temp)} {Unit1}"
    calci_result.markdown(str1) 
    str2=f"- ###### Dew Point Temperature: {str(dew_temp)} {Unit2}"
    calci_result.markdown(str2)
    str3=f"- ###### Heat Index: {str(round(HI[0]))} F"
    calci_result.markdown(str3)
   

# Showing Heatwave Intensity message based on calculated heat index
if btn and ( HI <80 ):
    calci_result.markdown('<style>bold{color: SpringGreen;}</style>', unsafe_allow_html=True)
    calci_result.markdown("<strong><bold>Normal Temperature: You are Safe!</strong></bold>",unsafe_allow_html=True)
elif btn and (HI>=80 and HI<90):
    calci_result.markdown('<style>bold{color: yellow;}</style>', unsafe_allow_html=True)
    calci_result.markdown("<strong><bold>Caution: Fatigue possible with prolonged exposure and/or physical activity !</strong></bold>",unsafe_allow_html=True)
elif btn and (HI>=90 and HI<103):
    calci_result.markdown('<style>bold{color: gold;}</style>', unsafe_allow_html=True)
    calci_result.markdown("<strong><bold>Extreme Caution: Heat stroke, heat cramps, or heat exhaustion possible with prolonged exposure and/or physical activity !</bold></strong>",unsafe_allow_html=True)
elif btn and (HI>=103 and HI<124):
    calci_result.markdown('<style>bold{color: orange;}</style>', unsafe_allow_html=True)
    calci_result.markdown("<strong><bold>Danger: Heat cramps or heat exhaustion likely, and heat stroke possible with prolonged exposure and/or physical activity !</bold></strong>",unsafe_allow_html=True)
elif btn and (HI>=124):
    calci_result.markdown('<style>bold{color: red;}</style>', unsafe_allow_html=True)
    calci_result.markdown("<strong><bold>Extreme Danger: Heat stroke highly likely !</bold></strong>",unsafe_allow_html=True)
calci_result.write("---")



# Information Section of Page
data_container.markdown(''' ####  What Are Heatwaves ? ''')
data_container.markdown('''<p style="text-align:start;"><img src="https://images.herzindagi.info/image/2022/May/tips-to-beat-heat-wave.jpg" width="650" height="300" ></p>''',unsafe_allow_html=True)
data_container.markdown(''' <p align="justify"> Heatwaves are prolonged periods of abnormally high temperatures that
                            occur in a specific geographical area, typically during the summer months. 
                            They are characterized by a sustained increase in temperature that can last 
                            for several days or even weeks. Heatwaves are caused by various meteorological factors, 
                            including the presence of high-pressure systems, the location of the jet stream, and the amount 
                            of moisture in the atmosphere.Climate change is expected to increase the frequency and 
                            severity of heatwaves around the world. As global temperatures continue to rise, 
                            heatwaves are likely to become more frequent, longer-lasting, and more intense. 
                            This underscores the importance of taking proactive steps to mitigate climate change,
                            such as reducing greenhouse gas emissions and adapting to a changing climate.</p> ''',unsafe_allow_html=True)

data_container.markdown('#### Information On The Factors That Contribute To Heatwave')

data_container.markdown('''* <p align="justify"> <strong> Atmospheric conditions:</strong> Atmospheric conditions, such as high-pressure systems,
                        can contribute to the development and intensity of heatwaves. High-pressure systems can lead to 
                        sinking air and clear skies, allowing for heat to build up near the surface.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"> <strong>Temperature anomalies:</strong> Temperature anomalies, which occur when temperatures are significantly higher than normal for a given location 
                        and time of year, can lead to heatwaves. Temperature anomalies can be caused by a variety of factors,
                        including changes in atmospheric circulation patterns, land use changes, and climate change.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"> <strong>Humidity:</strong> Humidity levels can also affect the intensity of heatwaves.
                         When humidity is high, it can make it feel much hotter than the actual temperature, as 
                        sweat cannot evaporate from the skin as easily.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"> <strong>Heat index:</strong> The heat index is a measure of how hot it feels outside,
                         taking into account both temperature and humidity. When the humidity is high, 
                        the heat index can be significantly higher than the actual temperature, making it feel much hotter outside.</p>''',unsafe_allow_html=True)

data_container.markdown('''<p style="text-align:center;"><img src="https://www.weather.gov/images/safety/heatindexchart-650.jpg" width="600" height="400" ></p>''',unsafe_allow_html=True)
data_container.text("     ")
data_container.text("     ")
data_container.markdown('''<p style="text-align:center;"><img src="https://drive.google.com/uc?export=view&id=1TlKYi7UKqhohdr5mJO_gsSeCOB3IX-l1" width="800" height="200" ></p>''',unsafe_allow_html=True)




data_container.markdown('''* <p align="justify"> <strong>Land surface conditions:</strong> Land surface conditions, such as soil moisture and 
                            vegetation cover, can affect the intensity of heatwaves.
                            Dry soil can absorb more heat from the sun, leading to hotter temperatures at the surface.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"> <strong>Urban heat island effect:</strong> The urban heat island effect occurs when urban areas are
                         significantly warmer than surrounding rural areas due to the concentration of buildings, 
                         pavement, and other infrastructure that can trap heat.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"> <strong>Climate change:</strong> Climate change is expected to contribute to 
                        an increase in the frequency, intensity, and duration of heatwaves. As global temperatures continue to rise, heatwaves are
                          expected to become more frequent and more severe.</p>''',unsafe_allow_html=True)

data_container.markdown(" #### Prediction Methods")
data_container.markdown('''<p align="justify">Predicting heat waves has been one of the major challenges for the climatologist due to their complex non-linear interaction with the large-scale atmospheric variables.
The prediction of the heat waves can be carried out broadly using two approaches i.e., statistical and dynamical. The statistical approach of forecasting is conducted by using the empirical models developed by
relating the largescale atmospheric variable with heatwaves. On the other hand, dynamical models depend on the physical interactions of ocean, atmosphere, and land for the development of the prediction model, which
makes the development of the model computationally intensive. Therefore, statistical models are broadly used for the development of the heat- wave prediction model. The capability of conventional statistical methods 
often found limited to solve intricate non-linear prediction problems. Considering the ability of ML algorithms in apprehending multidimensional complex processes, various types of ML models have been employed in
recent years for robust prediction of different natural phenomena.
The main objective of this study is to develop a climate change resilient robust heatwave prediction model to predict heatwave Index through that we are going to predict the heatwave intensity.
</p>''',unsafe_allow_html=True)

data_container.markdown("#### Heatwave Impacts")
data_container.markdown('''* <p align="justify"><strong> Heat-related illness and death: </strong>Heatwaves can cause a range of heat-related illnesses, 
                        from heat exhaustion to heat stroke, and can even be deadly. Older adults, young children, and people with certain medical 
                        conditions are especially vulnerable.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Wildfires: </strong> Heatwaves can increase the risk of wildfires by drying 
                        out vegetation and increasing the likelihood of ignition.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Reduced crop yields: </strong> High temperatures and drought conditions associated with heatwaves 
                        can lead to reduced crop yields and economic losses for farmers and food producers.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Infrastructure damage: </strong> High temperatures can cause roads, railways, and other
                         infrastructure to buckle and warp, leading to safety hazards and expensive repairs.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Increased energy demand:  </strong> During heatwaves, energy demand for
                         cooling can increase, putting a strain on power grids and leading to power outages.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Increased energy demand:  </strong> During heatwaves, energy demand for
                         cooling can increase, putting a strain on power grids and leading to power outages.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Water shortages: </strong> Heatwaves can increase demand for water for 
                        irrigation, cooling, and other purposes, leading to water shortages in some areas.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Negative impacts on wildlife: </strong> Heatwaves can affect wildlife by 
                        changing habitat conditions, reducing water availability, and increasing the risk of disease and predation.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong> Reduced air quality: </strong> Heatwaves can exacerbate air pollution by increasing the formation
                         of ground-level ozone and other pollutants.</p>''',unsafe_allow_html=True)

data_container.markdown("#### Heatwave Preparation and Response")

data_container.markdown('''* <p align="justify"><strong>Stay informed: </strong>Stay up to date on weather forecasts and heatwave alerts. Monitor local news 
                        and weather reports and sign up for emergency alerts from your local government or weather service.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Stay hydrated: </strong>Drink plenty of water, even if you don't feel thirsty. Avoid alcohol 
                        and caffeine, as these can dehydrate you.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Stay cool: </strong>Stay indoors in air-conditioned spaces when possible, and use fans or air 
                        conditioning to stay cool. Wear loose-fitting, light-coloured clothing and avoid strenuous activity during the hottest parts of 
                        the day. </p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Check on vulnerable individuals: </strong>Check on older adults, young children, and people with
                         medical conditions to ensure they are staying cool and hydrated.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Reduce energy use: </strong> Reduce energy use during heatwaves to avoid power outages and reduce
                         greenhouse gas emissions. Turn off non-essential lights and appliances, and avoid using ovens and other heat-producing
                         appliances.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Prepare your home: </strong> Prepare your home for heatwaves by installing window coverings or shades, 
                        sealing air leaks, and insulating your home. Consider installing a cool roof or using reflective roofing materials.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Be prepared for emergencies: </strong> Have a plan for what to do in case of a power outage or other emergency.
                        Stock up on food, water, and other supplies in case of an emergency.</p>''',unsafe_allow_html=True)

data_container.markdown('''* <p align="justify"><strong>Know the signs of heat-related illness: </strong> Know the signs of heat exhaustion and heat stroke, and seek
                         medical attention if you or someone you know shows signs of heat-related illness.</p>''',unsafe_allow_html=True)

# Heatwave Dashboard
data_container.header("Heatwave Dashboard")
data_container.markdown("""The tableau dashboard for the data used for this project is displayed below.
 This dashboard displays a variety of visualizations based on data parameters such as temperature, dew point and condition, among others.
The data used for this project is based on five districts in Telangana state: Adilabad, Warangal, Karimnagar, Mancherial, and Nizamabad.""")
# Accessing Tableau Dashboard Through API
html_temp="""<div class='tableauPlaceholder' id='viz1683884877659' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;He&#47;Heatwave_Intensity_Dashboard&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Heatwave_Intensity_Dashboard&#47;Dashboard1' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;He&#47;Heatwave_Intensity_Dashboard&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1683884877659');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.minWidth='1250px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='750px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.minWidth='1250px';vizElement.style.maxWidth='100%';vizElement.style.minHeight='750px';vizElement.style.maxHeight=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.minHeight='1050px';vizElement.style.maxHeight=(divElement.offsetWidth*1.77)+'px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
components.html(html_temp, width=1300, height=750)

# Creating New Data Container
new_container=st.container()
new_container.header("Heatwave Forcasting")

# Getting City Input From User 
city=new_container.text_input("Enter Your City Name:-","Nagpur")
Search_Button=new_container.button("Search")

# Creating API url based on city input
if Search_Button and (pd.notna(city)): 
    url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next7days?unitGroup=metric&include=days&key=5ELNAQ4SLUYNV9QFEV8EH373S&contentType=json'
else:
    url='https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/nagpur/next7days?unitGroup=metric&include=days&key=5ELNAQ4SLUYNV9QFEV8EH373S&contentType=json'

#Requesting data from API
r=requests.get(url)
excep_counter=0
if str(r)!='<Response [200]>':
    e=ValueError("Please Enter Correct City Name!")
    new_container.exception(e)
    excep_counter=1 
if excep_counter==0:
    json_data=r.json()
    data=pd.DataFrame(json_data['days'])
    forcast_data=data.iloc[:,[0,2,8]].reset_index(drop=True)
    forcast_data["HI"]=0
    forcast_data["condition"]=" "
    forcast_data.rename({"datetime":"date"},axis=1,inplace=True)

def calculation(air_temp1,dew_temp1):
    model=load_model()
    HI=model.predict([[0,air_temp1,dew_temp1,5]])
    return HI

def condition(HI):
    if (HI <80 ):
        output="Normal Temperature"
    elif (HI>=80 and HI<90):
        output="Caution"
    elif (HI>=90 and HI<103):
        output="Extreme Caution"
    elif (HI>=103 and HI<124):
        output="Danger"
    elif (HI>=124):
        output="Extreme Danger"
    return output


for i in range(0,len(forcast_data)):
    temp=forcast_data.loc[i,"tempmax"]
    dew=forcast_data.loc[i,"dew"]
    result=calculation(temp,dew)
    forcast_data["HI"][i] =round(result[0],2)
    forcast_data["condition"][i]=condition(forcast_data["HI"][i])
    forcast_data["date"][i]= datetime.strptime(forcast_data["date"][i],'%Y-%m-%d')
    #forcast_data["date"][i]=forcast_data["date"][i].strftime("%d %b")

    # new_container.dataframe(forcast_data.loc[:,["date","HI","condition"]])


# Creating Columns for showing heatwave forcasting data   
col1,col2,col3,col4=new_container.columns(4)
col1.markdown('''<h4>Date</h4>''',unsafe_allow_html=True)
col2.markdown('''<h4>Temperature</h4>''',unsafe_allow_html=True)
col3.markdown('''<h4>Heat Intensity</h4>''',unsafe_allow_html=True)
col4.markdown('''<h4>Condition</h4>
<style>
div[data-testid="stMetricValue"] > div {
    font-size: 20px;
}
</style>
''', unsafe_allow_html=True)

for i in range(len(forcast_data)):
    col1.metric(forcast_data["date"][i].strftime("%b"),forcast_data["date"][i].strftime("%d"))
    col2.metric("Temperature",forcast_data.loc[i,"tempmax"],label_visibility="hidden")
    col3.metric("Heat Index",forcast_data["HI"][i])
    col4.metric("Condition",forcast_data["condition"][i],label_visibility="hidden")


# New user subscription form
mail_form=new_container.form("user_form")
mail_form.subheader("For Getting Heatwave Alerts Please Subscribe To Our Mail Service ! :sun_with_face: :city_sunrise: " )
user_mail=mail_form.text_input("Enter Your Mail:-")
user_city=mail_form.text_input("Enter Your City:-")
mail_submit=mail_form.form_submit_button("Subscribe")

#email validator
def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False  
  
if mail_submit:
    user_mail=user_mail.lower().strip()
    user_city=user_city.lower().strip()
    db=db_connection()
    if(user_city=="" and user_mail==""):
        mail_form.exception(ValueError("Please Enter Your City and Mail!"))
        pass
    elif(user_mail==""):
        mail_form.exception(ValueError("Please Enter Your Mail!"))
        pass
    elif(user_city==""):
        mail_form.exception(ValueError("Please Enter Your City!"))
        pass
    elif(not validate_email(user_mail)):
        mail_form.exception(ValueError("Please Enter Proper Mail!"))
    elif(not user_city.isalpha()):
        mail_form.exception(ValueError("Please Enter Proper City Name!"))
        pass
    elif(check_subscribers(db,user_mail,user_city)):
        mail_form.success("You Are Already Subscribed !:smile:")
        pass
    else:
        if(user_city.isalpha()):
            insert_subscribers(db,user_mail,user_city)
            with st.spinner("please wait !"):
                time.sleep(3)
            mail_form.success("Your Subscription is Successful, Thank You For Subscribing !:partying_face:")

    

# Function for sending mail to users
def mail_sender(email_receiver,city,info):
        email_sender='heatwavealert@gmail.com'
        email_password='hgereewbwgagrxii'
        #email_receiver='aniruddhamane940@gmail.com'

        subject="Heatwave Alert"
        text_body=f"""Dear Citizen of {city} you will likely have high temperature in your city today ! Today's possible max temperature {str(info.loc[0,"tempmax"])} ℃ 
    Heat cramps or heat exhaustion likely, and heat stroke possible with prolonged exposure and/or physical activity. 
    Drink plenty of water, stay indoors in air-conditioned spaces when possible, 
    and use fans or air conditioning to stay cool. Wear loose-fitting, light-coloured clothing and avoid strenuous activity during the hottest parts of the day.
    Know the signs of heat exhaustion and heat stroke, and seek medical attention if you or someone you know shows signs of heat-related illness."""

        html_body=f"""\
    <html>
    <body>
        <div style="padding-left: 30px; background-image: url(https://wallpaperaccess.com/full/862227.png);
        background-size: cover; background-attachment: fixed;max-width:100%; height: auto;">
        <br><br>
        <h1 style="color: crimson; font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif; font-weight: bolder;">
            Heatwave Alert
        </h1>
        <p style="color: whitesmoke;font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;font-size: larger;font-weight: 500;">
        <span style="font-size: medium;font-weight: bolder"> Dear Citizen of {city} you will likely have high temperature in your city today ! <br>
            Today's possible max temperature is: {str(info.loc[0,"tempmax"])} ℃</span> <br><br>
        <span style="color: darkorange;font-weight: bolder;"> 
            Heat cramps or heat exhaustion is likely, and there is a risk of heat stroke with prolonged exposure and/or physical activity.</span><br>
            <br><span style="font-size: large;font-weight: bolder;">Precautions To Take</span><br>
        <div style="font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;font-size:medium;font-weight: 600;color: whitesmoke;">
            <ul>   
        <li>Drink plenty of water.</li> 
        <li>Stay indoors in air-conditioned spaces when possible and use fans or air conditioning to stay cool.</li> 
        <li> Wear loose-fitting, light-coloured clothing and avoid strenuous activity during the hottest parts of the day.</li>
        <li>Know the signs of heat exhaustion and heat stroke, and seek medical attention if you or someone you know shows <br>
        signs of heat-related illness.</li><br><br>
        </ul>
        </div>
    </p>
    </div>
    </body>
    </html>
        """
        em=MIMEMultipart("alternative")

        em['From']=email_sender
        em['To']=email_receiver
        em['Subject']=subject

        #em.set_content(body)

        part1 = MIMEText(text_body, "plain")
        part2 = MIMEText(html_body, "html")

        em.attach(part1)
        em.attach(part2)



        context=ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())

# Function for making dataframe of user city's heatwave condition
def dfmaker(City):
                    url=f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{City}/next7days?unitGroup=metric&include=days&key=5ELNAQ4SLUYNV9QFEV8EH373S&contentType=json'
                    r=requests.get(url)
                    excep_counter=0
                    if str(r)!='<Response [200]>':
                        excep_counter=1
                        return 0 
                    if excep_counter==0:
                        json_data=r.json()
                        data=pd.DataFrame(json_data['days'])
                        forcast_data=data.iloc[:,[0,2,8]].reset_index(drop=True)
                        forcast_data["HI"]=0
                        forcast_data["condition"]=" "
                        forcast_data.rename({"datetime":"date"},axis=1,inplace=True)

                    for i in range(0,len(forcast_data)):
                        temp=forcast_data.loc[i,"tempmax"]
                        dew=forcast_data.loc[i,"dew"]
                        result=calculation(temp,dew)
                        forcast_data["HI"][i] =round(result,2)
                        forcast_data["condition"][i]=condition(forcast_data["HI"][i])
                        forcast_data["date"][i]= datetime.strptime(forcast_data["date"][i],'%Y-%m-%d')

                    return forcast_data

# Function for iterating through each user for sending alert mails
def mail_iterator():    
    # reader=pd.read_excel("subscribers.xlsx")
    db=db_connection()
    query=db.sql("select City,Mail from heatwave_repo.subscribers")
    reader=pd.DataFrame(query,columns=["Mail","City"])
    for i in range(0,len(reader)):
        Mail=reader.loc[i,"Mail"]
        City=reader.loc[i,"City"]
        info=dfmaker(City)
        if info.loc[0,"condition"]=="Danger":
                mail_sender(Mail,City,info)

datetime_in_india = datetime.now(pytz.timezone('Asia/Kolkata'))

# function for invoking mail function on specific time
if(datetime_in_india.hour>=5 and datetime_in_india.hour<=7 ):
    mail_iterator()

#AutoRefresh Page Every 30 Minutes 
st_autorefresh(interval=30 * 60 * 1000, key="dataframerefresh")
# new_container.dataframe(forcast_data)

