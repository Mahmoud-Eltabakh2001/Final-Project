
import joblib
import lightgbm as ltb
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.style.use("bmh")
plt.rc("figure",autolayout=True)
plt.rc("axes",labelweight="bold",labelsize="large",titleweight="bold",titlesize=14,titlepad=10)

database=pd.read_csv("database.csv")
database.drop(columns=["Unnamed: 0"],inplace=True)

visualize_data=pd.read_csv("/content/visualize_data.csv")

model=joblib.load("Uber.pkl")

def predict_trip_price(source, destination, cab_type, name, surge_multiplier,distance):
    prediction =model.predict( pd.DataFrame({"source":[source],
                                             "destination":[destination],
                                             "cab_type":[cab_type],
                                             "name":[name],
                                             "surge_multiplier":[surge_multiplier],
                                             "distance":[distance] },index=[1] ) )
    return prediction    

def main():
    
    st.set_page_config(layout="wide")
    st.sidebar.title("Graduation Project")
    st.sidebar.title("")
    page=st.sidebar.radio("Navigation",["Home","Dashboard","Predict","Append","Evaluate"])  
    st.sidebar.title("") 
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.title("")
    st.sidebar.subheader("Created By: Mahmoud Eltabakh")
    
    if page=="Home":

       html_temp = """
            <div style="background-color:tomato;padding:10px">
            <h2 style="color:white;">About This Project.</h2>
            </div>
                   """
       st.markdown(html_temp,unsafe_allow_html=True)

       st.markdown("""""")
       st.markdown("One of problems facing transport companies is the Dynamic price problem")
       st.markdown("Where the company is required to determine the best and most appropriate price for a trip, taking into account the increase in its revenue and profit")
       st.markdown("""""")
       st.subheader("User can: ")
       st.markdown(" 1) Know price of the trip ")
       st.markdown(" 2) Evaluate the App in arabic")
       st.subheader(" There are 3 evaluation cases")
       st.code(" ( 1)  > > Positive")
       st.code(" ( 0)  > > Natural")
       st.code(" (-1)  > > Negative")

    if page=="Append":
       html_temp = """
                      <div style="background-color:tomato;padding:10px">
                      <h2 style="color:white;text-align:center;">Contribute to database</h2>
                      </div>
                   """
       st.markdown(html_temp,unsafe_allow_html=True)
       st.title("")
       df=database.tail()
       if st.checkbox("Show data",value=False) :
          st.dataframe(df)
      
       source=st.selectbox("Mark your place.",['Haymarket Square','Back Bay','North End','North Station','Beacon Hill',
                                               'Boston University','Fenway','South Station','Theatre District','West End',
                                               'Financial District','Northeastern University'] )
       destination=st.selectbox("Select your destination.",['North Station', 'Northeastern University', 'West End','Haymarket Square',
                                                            'South Station', 'Fenway','Theatre District','Beacon Hill', 'Back Bay', 
                                                            'North End', 'Financial District','Boston University'])
       cab_type=st.selectbox("Choose company name",['Lyft', 'Uber'])
       name=st.selectbox("Choose type of car",['Shared','Lux','Lyft','Lux Black XL','Lyft XL','Lux Black','UberXL','Black',
                                               'UberX','WAV','Black SUV','UberPool','Taxi'])
       distance=st.number_input("Estimated distance",min_value=0.0,max_value=10.0,step=0.1)  
       surge_multiplier=st.slider("Value added",min_value=1.0,max_value=3.0,step=0.1) 
       price=st.number_input("Enter price of trip.",min_value=1.0,max_value=100.0,step=0.1)


       if st.button("Submit"):
          to_add={
                  "source":source,
                  "destination":destination,
                  "cab_type":cab_type,
                  "name":name,
                  "surge_multiplier":surge_multiplier,
                  "distance":distance,
                  "price":price
                 }
        
          to_add=pd.DataFrame(to_add,index= [len(database)] )
          to_add.to_csv("database.csv",mode="a",header=False)
          st.success("Submited Successfully")

       if st.checkbox("Show updated data",value=False) :
          st.dataframe(database.tail())

    if page=="Predict":
       html_temp = """
                        <div style="background-color:tomato;padding:10px">
                        <h2 style="color:white;text-align:center;">Find out price of trip</h2>
                        </div>
                   """
       st.markdown(html_temp,unsafe_allow_html=True)
     
       st.title("")
       source=st.selectbox("Mark your place.",['Haymarket Square','Back Bay','North End','North Station','Beacon Hill',
                                               'Boston University','Fenway','South Station','Theatre District','West End',
                                               'Financial District','Northeastern University'] )
       destination=st.selectbox("Select your destination.",['North Station', 'Northeastern University', 'West End','Haymarket Square',
                                                            'South Station', 'Fenway','Theatre District','Beacon Hill', 'Back Bay', 
                                                            'North End', 'Financial District','Boston University'])
       cab_type=st.selectbox("Choose company name",['Lyft', 'Uber'])
       name=st.selectbox("Choose type of car",['Shared','Lux','Lyft','Lux Black XL','Lyft XL','Lux Black','UberXL','Black',
                                               'UberX','WAV','Black SUV','UberPool','Taxi'])
       distance=st.number_input("Estimated distance",min_value=0.0,max_value=10.0,step=0.1)  
       surge_multiplier=st.slider("Value added",min_value=1.0,max_value=3.0,step=0.1) 

       result=""
       if st.button("Predict"):
          result=predict_trip_price(source,destination,cab_type,name,surge_multiplier,distance)
          st.success("Expected trip price : {} $".format(result)) 

    if page=="Dashboard":
       html_temp = """
            <div style="background-color:tomato;padding:10px">
            <h2 style="color:white;text-align:center;">Insights from data.</h2>
            </div>
                   """
       st.markdown(html_temp,unsafe_allow_html=True)
       st.title("")
 
       df=visualize_data.tail()
       if st.checkbox("Show data",value=False) :
          st.dataframe(df)

       kind=st.selectbox("What kind of Graph?",["Non-Interactive","Interactive"])
       st.title("")
       if kind=="Non-Interactive":
          col1,col2=st.columns(2)
          with col1:

               sns.countplot(x="day",data=visualize_data,hue="cab_type")
               st.subheader("The number of trips for each company during the days of month")
               st.pyplot()

               st.subheader("Distribution of weather conditions on number of trips")
               s=visualize_data["icon"].value_counts().reset_index(name="count").rename(columns={"index":"icon"})
               plt.pie(s["count"],labels=s["icon"],autopct="%0.1f%%",explode=[0.1,0,0,0,0,0,0])
               st.pyplot()
               st.title("")
               st.title("")

               st.subheader("Average distance traveled for each company")
               sns.barplot(x='cab_type',y="distance",data=visualize_data)
               st.pyplot()
 
               st.subheader("The number of trips made by each each type of each company")
               plt.xticks(rotation=45)
               n=visualize_data.groupby(["name","cab_type"])[["id"]].count().rename(columns={"id":"count"}).stack().reset_index(name="count").drop("level_2",axis=1).sort_values(by="count")
               sns.barplot(x="name",y="count",data=n,hue="cab_type")           
               st.pyplot() 
             
               st.subheader("The number of trips for each company over the month")
               sns.countplot(x="month",data=visualize_data,hue="cab_type")
               st.pyplot()

               st.subheader("The number of trips for each company over weather conditions")
               sns.countplot(x="icon",data=visualize_data,hue="cab_type")
               plt.xticks(rotation=45)
               st.pyplot()

               st.subheader("The relationship between the time period and price of the trip")
               sns.barplot(x="period",y="price",data=visualize_data)
               st.pyplot()


          with col2:
            
               sns.countplot(x="hour",data=visualize_data,hue="cab_type")
               st.subheader("The number of trips for each company during the hours of day")
               st.pyplot()

               c=visualize_data.groupby("cab_type")["id"].size().reset_index(name="count")
               st.subheader("Most requested company")
               plt.pie(c["count"],labels=c["cab_type"],autopct="%1.1f%%")
               st.pyplot()

               st.subheader("The average trip price for each company.")
               st.title("")
               sns.barplot(x="cab_type",y="price",estimator=np.mean,data=visualize_data)
               st.pyplot()

               st.subheader("Average prices of trips carried out by each type of each company")
               plt.xticks(rotation=45)
               sns.barplot(x="name",y="price",hue="cab_type",data=visualize_data) 
               st.pyplot()

               st.subheader("Average trips prices for each month")
               st.title("")
               sns.barplot(x="month",y="price",data=visualize_data)
               st.pyplot()

               st.subheader("The relationship between weather conditions and trip prices")
               s=visualize_data.groupby("icon")[["price"]].mean().sort_values(by="price",ascending=False)
               sns.barplot(x=s.index,y="price",data=s)
               plt.xticks(rotation=45)
               st.pyplot()

               st.subheader("Trip prices throughout the week for both companies")
               sns.barplot(x="day_name",y="price",hue="cab_type",data=visualize_data)
               st.pyplot() 


          on,tw,thr=st.columns(3)
          with on:
               m=visualize_data["month"].value_counts().reset_index(name="count").rename(columns={"index":"month"})
               st.subheader("Trips every month")
               st.title("")
               plt.pie(m["count"],labels=m["month"],autopct="%1.1f%%")
               st.pyplot()

          with tw:
               st.subheader("Distribution of number of trips on the days of the week")
               v=visualize_data["day_name"].value_counts().reset_index(name="count").rename(columns={"index":"day_name"})
               plt.pie(v["count"],labels=v.day_name,autopct="%0.1f%%",explode=[0.1,0.1,0,0,0,0,0])  
               st.pyplot() 
          with thr:
               st.subheader("Distribution of number of trips to the periods of the day")
               v=visualize_data["period"].value_counts().reset_index(name="count").rename(columns={"index":"period"})
               plt.pie(v["count"],labels=v.period,autopct="%0.1f%%",explode=[0.1,0,0])
               st.pyplot()


          one,two=st.columns(2)
          with one :
               s=visualize_data.groupby("source")[["id"]].count().rename(columns={"id":"Number of Trips"}).sort_values(by="Number of Trips",ascending=False)
               st.subheader("The number of trips originating from each source")
               sns.barplot(x=s["Number of Trips"],y=s.index)
               st.pyplot()
               st.title("")

          with two :
               s=visualize_data.groupby("destination")[["id"]].count().rename(columns={"id":"Number of Trips"}).sort_values(by="Number of Trips",ascending=False)
               st.subheader("The number of trips originating from each destination")
               sns.barplot(x=s["Number of Trips"],y=s.index)
               st.pyplot()
            
          t=visualize_data.groupby(["source","destination"])[["id"]].count().sort_values(by="id",ascending=False).rename(columns={"id":"count"})
          t=t.stack().reset_index(name="count").drop("level_2",axis=1).head(15)
          def trip (x):
              x["trip"]=x["source"] + " --> "+ x["destination"]
              return x
          t=t.apply(trip,axis=1)
          st.subheader("Most popular trips")
          sns.barplot(y="trip",x="count",data=t)
          st.pyplot()


       if kind=="Interactive":

          col1,col2=st.columns(2)

          with col1:

               st.subheader("The number of trips for each company during the days of month")
               fig = px.histogram(visualize_data, x="day", color="cab_type",barmode="group", nbins=len(visualize_data["day"].unique()),template="plotly_dark")
               fig.update_layout(title="Count per Day and Cab Type",xaxis_title="Day",yaxis_title="Count")
               st.plotly_chart(fig)

               st.subheader("Distribution of weather conditions on number of trips")
               s=visualize_data["icon"].value_counts().reset_index(name="count").rename(columns={"index":"icon"})
               fig = px.pie(s, values='count', names='icon',title='Distribution of cab rides by weather icon',hole=0.5,labels={'count': 'Number of Rides'}) 
               st.plotly_chart(fig)
  

               st.subheader("Average distance traveled for each company")
               fig = px.bar(visualize_data, x='cab_type', y='distance', color='cab_type', title='Distance by Cab Type')
               st.plotly_chart(fig)
 
               st.subheader("The number of trips made by each each type of each company")
               plt.xticks(rotation=45)
               n=visualize_data.groupby(["name","cab_type"])[["id"]].count().rename(columns={"id":"count"}).stack().reset_index(name="count").drop("level_2",axis=1).sort_values(by="count")
               fig = px.bar(n, x="name", y="count", color="cab_type", color_discrete_sequence=["#fdaa48", "#2a75bb"])
               st.plotly_chart(fig)

               st.subheader("The number of trips for each company over the month")
               fig = px.histogram(visualize_data, x="month", color="cab_type")
               fig.update_layout(barmode="group")
               st.plotly_chart(fig)

               st.subheader("The number of trips for each company over weather conditions")
               fig = px.histogram(visualize_data, x="icon", color="cab_type")
               st.plotly_chart(fig)

               st.subheader("The relationship between the time period and price of the trip")
               dd=visualize_data.groupby("period")[["price"]].mean()
               fig = px.bar(dd, x=dd.index, y=dd.price, color_discrete_sequence=['blue'], barmode='group')
               fig.update_layout(title='Price vs Period')
               st.plotly_chart(fig)


          with col2:

               st.subheader("The number of trips for each company during the hours of day")
               fig = px.histogram(visualize_data, x="hour", color="cab_type",barmode="group", nbins=len(visualize_data["day"].unique()),template="plotly_dark")
               fig.update_layout(title="Distribution of Cab Rides by Hour",xaxis_title="hour",yaxis_title="Count")
               st.plotly_chart(fig)

               c=visualize_data.groupby("cab_type")["id"].size().reset_index(name="count")
               st.subheader("Most requested company")
               fig = go.Figure(data=[go.Pie(labels=c["cab_type"], values=c["count"], hole=0.3)])
               fig.update_layout(title="Percentage of Cab Type Usage")
               st.plotly_chart(fig)


               st.subheader("The average trip price for each company.")
               fig = px.bar(visualize_data, x="cab_type", y="price",color="cab_type", title="Average Price per Cab Type")
               st.plotly_chart(fig)
             
               st.subheader("Average prices of trips carried out by each type of each company")
               fig = px.bar(visualize_data, x="name", y="price", color="cab_type",title="Price by Cab Type and Name")
               st.plotly_chart(fig)

               st.subheader("Average trips prices for each month")
               fig = go.Figure()
               fig.add_trace(go.Bar(x=visualize_data['month'], y=visualize_data['price']))
               fig.update_layout(title="Average Trip Price by Month",xaxis_title="Month",yaxis_title="Price")
               st.plotly_chart(fig)

               st.subheader("The relationship between weather conditions and trip prices")
               s=visualize_data.groupby("icon")[["price"]].mean().sort_values(by="price",ascending=False)
               fig = px.bar(x=s.index, y="price", data_frame=s)
               fig.update_layout(title='Bar Plot', xaxis_title='Index', yaxis_title='Price')
               st.plotly_chart(fig)

               st.subheader("Trip prices throughout the week for both companies")
               fig = px.bar(visualize_data, x='day_name', y='price', color='cab_type', barmode='group')
               fig.update_layout(title='Price by Day and Cab Type', xaxis_title='Day of Week', yaxis_title='Price')
               st.plotly_chart(fig)
    

          on,tw,thr=st.columns(3)
          with on:
               m=visualize_data["month"].value_counts().reset_index(name="count").rename(columns={"index":"month"})
               st.subheader("Trips every month")
               fig = go.Figure(data=[go.Pie(labels=m["month"], values=m["count"])])
               fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,marker=dict(colors=px.colors.qualitative.Plotly))
               st.plotly_chart(fig)

          with tw:
               st.subheader("Distribution of number of trips on the days of the week")
               v=visualize_data["day_name"].value_counts().reset_index(name="count").rename(columns={"index":"day_name"})
               fig = px.pie(v, values='count', names='day_name',title='Distribution of Rides by Day',labels={'count': 'Number of Rides'})
               st.plotly_chart(fig)
               
          with thr:
               st.subheader("Distribution of number of trips to the periods of the day")
               v=visualize_data["period"].value_counts().reset_index(name="count").rename(columns={"index":"period"})
               fig = px.pie(v, values='count', names='period',title='Distribution of Rides by Period',labels={'count': 'Number of Rides'})
               st.plotly_chart(fig)

          one,two=st.columns(2)
          with one :
               s=visualize_data.groupby("source")[["id"]].count().rename(columns={"id":"Number of Trips"}).sort_values(by="Number of Trips",ascending=False)
               st.subheader("The number of trips originating from each source")
               data = go.Bar(x=s["Number of Trips"], y=s.index, orientation="h")
               layout = go.Layout(title="Number of Trips per Hour", xaxis_title="Number of Trips", yaxis_title="Hour of the Day")
               fig = go.Figure(data=data, layout=layout)
               st.plotly_chart(fig)

          with two :
               s=visualize_data.groupby("destination")[["id"]].count().rename(columns={"id":"Number of Trips"}).sort_values(by="Number of Trips",ascending=False)
               st.subheader("The number of trips originating from each destination")
               fig = go.Figure()
               fig.add_trace(go.Bar(x=s["Number of Trips"],y=s.index,orientation='h'))
               fig.update_layout(title='Number of Trips by Weekday',xaxis_title='Number of Trips',yaxis_title='Weekday')
               st.plotly_chart(fig)

          t=visualize_data.groupby(["source","destination"])[["id"]].count().sort_values(by="id",ascending=False).rename(columns={"id":"count"})
          t=t.stack().reset_index(name="count").drop("level_2",axis=1).head(15)
          def trip (x):
              x["trip"]=x["source"] + " --> "+ x["destination"]
              return x
          t=t.apply(trip,axis=1)
          st.subheader("Most popular trips")
          fig = go.Figure(go.Bar(x=t["count"],y=t["trip"],orientation='h'))
          fig.update_layout(title="Trips per category",xaxis_title="Count",yaxis_title="Trip category")
          st.plotly_chart(fig)


main()
