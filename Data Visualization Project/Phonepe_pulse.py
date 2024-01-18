
import json
import streamlit as st
import pandas as pd
import requests #To get the url of geojson file
import plotly.express as px
from PIL import Image #To decode images
import mysql.connector



st.set_page_config(page_title='PhonePe Pulse', page_icon=':bar_chart:', layout="wide")

# Load your image
image_path = "C:/Users/Hp/Documents/project/Projects/Phonepe project/pngwing.com.png"
image = Image.open(image_path)



st.image(image,width=200)
#CREATE DATAFRAMES FROM SQL
   


st.header(":violet[Phonepe Data Visualization]")

phonepe_description = """PhonePe has launched PhonePe Pulse, a data analytics platform that provides insights into
                        how Indians are using digital payments. With over 30 crore registered users and 2000 crore 
                        transactions, PhonePe, India's largest digital payments platform with 46% UPI market share,
                        has a unique ring-side view into the Indian digital payments story. Through this app, you 
                        can now easily access and visualize the data provided by PhonePe Pulse, gaining deep 
                        insights and interesting trends into how India transacts with digital payments."""

st.write(phonepe_description)


tab1, tab2 = st.tabs(["**:violet[Overview]**","**:violet[Top Charts]**"])


with st.sidebar:
        
        st.header(":violet[About]")
        
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown(" :violet[Phonepe is an Indian digital payments and financial technology company]")
        st.write("****FEATURES****")
        st.write("**-> :violet[One App For All Your Payments]**")
        st.write("**-> :violet[Multiple Payment Modes]**")
        st.write("**-> :violet[Earn Great Rewards]**")
        st.write("**-> :violet[No Wallet Top-Up Required]**")
        st.write("**-> :violet[Pay Directly From Any Bank To Any Bank A/C]**")
        st.write("**-> :violet[Instantly & Free]**")
        st.download_button("Download PhonePe App", "https://www.phonepe.com/app-download/")

#sql connection
mydb = mysql.connector.connect(host="localhost",
                            user="root",
                            password="",
                            #database='joins'
                            )
mycursor = mydb.cursor(buffered=True)

#Aggregated_transaction

mycursor.execute("select * from phonepe_datas.agg_transaction_table")
mydb.commit()
At = mycursor.fetchall()
Agg_txn = pd.DataFrame(At,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
mycursor.execute("select * from phonepe_datas.agg_users_table")
mydb.commit()
Au= mycursor.fetchall()
Agg_user = pd.DataFrame(Au,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_transaction
mycursor.execute("select * from phonepe_datas.map_transaction_table")
mydb.commit()
Mt = mycursor.fetchall()
Map_txn = pd.DataFrame(Mt,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
mycursor.execute("select * from phonepe_datas.map_users_table")
mydb.commit()
Mu = mycursor.fetchall()
Map_user = pd.DataFrame(Mu,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))


#Top_transaction
mycursor.execute("select * from phonepe_datas.top_transactions_table")
mydb.commit()
Tt = mycursor.fetchall()
Top_txn = pd.DataFrame(Tt,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
mycursor.execute("select * from phonepe_datas.top_users_table")
mydb.commit()
Tu = mycursor.fetchall()
Top_user = pd.DataFrame(Tu, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

def txn_amount_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atay= Agg_txn[["States","Years","Transaction_amount"]]
    atay1= atay.loc[(Agg_txn["Years"]==year)]
    atay2= atay1.groupby("States")["Transaction_amount"].sum()
    atay3= pd.DataFrame(atay2).reset_index()

    fig_atay= px.choropleth(atay3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "Transaction_amount",color_continuous_scale=px.colors.sequential.ice,
                            title="Transaction Amount & States", hover_name= "States",template="plotly_dark")

    fig_atay.update_geos(fitbounds= "locations", visible= False)
    fig_atay.update_layout(width=600,height=700)
    fig_atay.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_atay, use_container_width=True)

def txn_count(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atay= Agg_txn[["States","Years","Transaction_count"]]
    atay1= atay.loc[(Agg_txn["Years"]==year)]
    atay2= atay1.groupby("States")["Transaction_count"].sum()
    atay3= pd.DataFrame(atay2).reset_index()

    fig_atay= px.choropleth(atay3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "Transaction_count",color_continuous_scale=px.colors.sequential.Darkmint,
                            title="Transaction Count & States", hover_name= "States",template="plotly_dark")

    fig_atay.update_geos(fitbounds= "locations", visible= False)
    fig_atay.update_layout(width=600,height=700)
    fig_atay.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_atay, use_container_width=True)


def district_year(sel_year):
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    state_names_tra= [feature["properties"]['ST_NM']for feature in data1["features"]]
    state_names_tra.sort()

    year= int(sel_year)
    atay= Map_user[["States","Years","RegisteredUser","Districts"]]
    atay1= atay.loc[(Map_user["Years"]==year)]
    atay2= atay1.groupby("States")["RegisteredUser"].sum()
    atay3= pd.DataFrame(atay2).reset_index()

    fig_atay= px.choropleth(atay3, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                            color= "RegisteredUser",color_continuous_scale=px.colors.sequential.solar,
                            title="RegisteredUser & States", hover_name= "States",template="plotly_dark")

    fig_atay.update_geos(fitbounds= "locations", visible= False)
    fig_atay.update_layout(width=600,height=700)
    fig_atay.update_layout(title_font= {"size":25})
    return st.plotly_chart(fig_atay, use_container_width=True)


with tab1:

    sel_year = st.selectbox("select the Year",("2018", "2019", "2020", "2021", "2022", "2023"),index=None)

    if sel_year==None:
        st.empty()
    else:
        txn_amount_year(sel_year)
        txn_count(sel_year)
        district_year(sel_year)

      
                       
with tab2: 



    cmnd=st.selectbox("",("1.Total transactions of districts.",
                            "2.Mobile phone brands used for transactions.",
                            "3.Most used transaction types.",
                            "4.Most users registered districts.",
                            "5.Distrcts with appopens.",
                            "6.Top 10 States of highest amount transaction",
                            "7.Top 10 States of highest users registered",
                            "8.Top 10 States of highest Appopens registered",
                            "9.Top 10 States of lowest amount transaction",
                            "10.Top 10 Districts of lowest transaction count"),index=None,placeholder="Select Commands")
    
    if cmnd=="6.Top 10 States of highest amount transaction" or cmnd=="7.Top 10 States of highest users registered" or cmnd=="8.Top 10 States of highest Appopens registered" or cmnd=="9.Top 10 States of lowest amount transaction" or cmnd=="10.Top 10 Districts of lowest transaction count" :
        g=True
    else:
        g=False
    
    state=st.selectbox("",('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh',
                "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand",
                "Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry",
                "Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"),index=None,disabled=g,placeholder="Select states")

    

    if cmnd=="1.Total transactions of districts.":

        Bon = st.radio("Based On",[":rainbow[Transactions Amounts]", ":rainbow[Transanctions Counts]"],horizontal=True)

        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)
 
        if Bon==":rainbow[Transactions Amounts]":
    
            E1 = Map_txn[["States","Years","Districts","Transaction_amount"]]
            ef1 = E1[(E1["States"] == state) & (E1["Years"] == year)]
        
            df1 = ef1.groupby("Districts")["Transaction_amount"].sum().reset_index()
            df1['Formatted_amount'] = df1['Transaction_amount'].apply(lambda x: '{:,.2f}'.format(x))
            sort_df1=df1.sort_values(by="Transaction_amount", ascending=False)

            fig1 = px.bar(sort_df1,
                        y='Transaction_amount',
                        x='Districts',
                        text="Transaction_amount",
                        color="Transaction_amount",
                        color_continuous_scale=px.colors.sequential.Reds)
            fig1.update_traces(texttemplate="%{text:.2s}",textposition="outside")
            st.plotly_chart(fig1, use_container_width=True)

        elif Bon==":rainbow[Transanctions Counts]":
        
            E2 = Map_txn[["States","Years","Districts","Transaction_count"]]
            ef2 = E2[(E2["States"] == state) & (E2["Years"] == year)]
            df2 = ef2.groupby("Districts")["Transaction_count"].sum().reset_index()
            sort_df2=df2.sort_values(by="Transaction_count", ascending=False)
            fig2 = px.bar(sort_df2,
                        y='Transaction_count',
                        x='Districts',
                        text="Transaction_count",
                        color="Transaction_count",
                        color_continuous_scale=px.colors.sequential.Blues)
            fig2.update_traces(texttemplate="%{text:.2s}",textposition="outside")
            st.plotly_chart(fig2, use_container_width=True)

    elif cmnd=="2.Mobile phone brands used for transactions.":
        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022"],horizontal=True)
        year = int(sel_year)

        E3 = Agg_user[["States","Years","Brands","Transaction_count"]]
        ef3 = E3[(E3["States"] == state) & (E3["Years"] == year)]
        df3=ef3.groupby('Brands')['Transaction_count'].sum().reset_index()
        fig3=px.pie(df3,
                    values='Transaction_count',
                    names='Brands',
                    color_discrete_sequence=px.colors.sequential.PuBu_r)
        fig3.update_traces(text=df3["Brands"],textfont_size=10)
        st.plotly_chart(fig3, use_container_width=True)

    elif cmnd=="3.Most used transaction types.":

        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022","2023"],horizontal=True)
        year = int(sel_year)
        
        Bon = st.radio("Based On",[":rainbow[Transactions Amounts]", ":rainbow[Transanctions Counts]"],horizontal=True)

        if Bon==":rainbow[Transanctions Counts]":

            E4 = Agg_txn[["States","Years","Transaction_type","Transaction_count"]]
            ef4 = E4[(E4["States"] == state) & (E4["Years"] == year)]
            df4 = ef4.groupby("Transaction_type")["Transaction_count"].sum().reset_index()
            sort_df4=df4.sort_values(by="Transaction_count", ascending=False)
            fig4 = px.bar(sort_df4,
                        y='Transaction_count',
                        x='Transaction_type',
                        text="Transaction_count",
                        color="Transaction_count",
                        color_continuous_scale=px.colors.sequential.Greens)
            fig4.update_traces(texttemplate="%{text:.2s}",textposition="outside")
            st.plotly_chart(fig4, use_container_width=True)


        elif Bon==":rainbow[Transactions Amounts]": 

            E5 = Agg_txn[["States","Years","Transaction_type","Transaction_amount"]]
            ef5 = E5[(E5["States"] == state) & (E5["Years"] == year)]
            df5 = ef5.groupby("Transaction_type")["Transaction_amount"].sum().reset_index()
            sort_df5=df5.sort_values(by="Transaction_amount", ascending=False)
            fig5 = px.bar(sort_df5,
                        y='Transaction_amount',
                        x='Transaction_type',
                        text="Transaction_amount",
                        color="Transaction_amount",
                        color_continuous_scale=px.colors.sequential.Purples)
            
            fig5.update_traces(texttemplate="%{text:.3s}",textposition="outside")
            st.plotly_chart(fig5, use_container_width=True) 

    elif cmnd=="4.Most users registered districts.":

        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)
        
        E6 = Map_user[["States","Years","Districts","RegisteredUser"]]
        ef6 = E6[(E6["States"] == state) & (E6["Years"] == year)]
        df6 = ef6.groupby("Districts")["RegisteredUser"].sum().reset_index()
        sort_df6=df6.sort_values(by="RegisteredUser", ascending=False)
        fig6 = px.bar(sort_df6,
                    y='RegisteredUser',
                    x='Districts',
                    color="RegisteredUser",
                    color_continuous_scale=px.colors.sequential.Mint)
        st.plotly_chart(fig6, use_container_width=True)
    
    elif cmnd=="5.Distrcts with appopens.":
        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)
        
        E7 = Map_user[["States","Years","Districts","AppOpens"]]
        ef7 = E7[(E7["States"] == state) & (E7["Years"] == year)]
        df7 = ef7.groupby("Districts")["AppOpens"].sum().reset_index()
        sort_df7=df7.sort_values(by="AppOpens", ascending=False)
        fig7 = px.bar(sort_df7,
                    y='AppOpens',
                    x='Districts',
                    color="AppOpens",
                    color_continuous_scale=px.colors.sequential.solar)
        st.plotly_chart(fig7, use_container_width=True)

    elif cmnd=="6.Top 10 States of highest amount transaction":

        
        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)

        E8 = Top_txn[["States","Years","Transaction_amount"]]
        ef8=E8[E8["Years"] == year]
        df8 = ef8.groupby(["States"])["Transaction_amount"].sum().reset_index()
        sort_df8=df8.sort_values(by="Transaction_amount", ascending=False).head(10)
        fig8 = px.bar(sort_df8,
                    y='States',
                    x='Transaction_amount',
                    color="Transaction_amount",
                    color_continuous_scale=px.colors.sequential.Oranges,
                    orientation='h')
        st.plotly_chart(fig8, use_container_width=True) 

    elif cmnd=="7.Top 10 States of highest users registered":
        
        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)

        E9 = Top_user[["States","Years","RegisteredUser"]]
        ef9=E9[E9["Years"] == year]
        df9 = ef9.groupby(["States"])["RegisteredUser"].sum().reset_index()
        sort_df9=df9.sort_values(by="RegisteredUser", ascending=False).head(10)
        fig9 = px.bar(sort_df9,
                    y='States',
                    x='RegisteredUser',
                    color="RegisteredUser",
                    color_continuous_scale=px.colors.sequential.BuPu,
                    orientation='h')
        st.plotly_chart(fig9, use_container_width=True) 

    elif cmnd=="8.Top 10 States of highest Appopens registered":
        
        sel_year = st.radio("",["2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)

        E10 = Map_user[["States","Years","AppOpens"]]
        ef10=E10[E10["Years"] == year]
        df10 = ef10.groupby(["States"])["AppOpens"].sum().reset_index()
        sort_df10=df10.sort_values(by="AppOpens", ascending=False).head(10)
        fig10 = px.bar(sort_df10,
                    y='States',
                    x='AppOpens',
                    color="AppOpens",
                    color_continuous_scale=px.colors.sequential.ice_r,
                    orientation='h')
        st.plotly_chart(fig10, use_container_width=True) 

    elif cmnd=="9.Top 10 States of lowest amount transaction":
        
        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)

        E11 = Top_txn[["States","Years","Transaction_amount"]]
        ef11=E11[E11["Years"] == year]
        df11 = ef11.groupby(["States"])["Transaction_amount"].sum().reset_index()
        sort_df11=df11.sort_values(by="Transaction_amount", ascending=True).head(10)
        fig11 = px.bar(sort_df11,
                    y='States',
                    x='Transaction_amount',
                    color="Transaction_amount",
                    color_continuous_scale=px.colors.sequential.algae,
                    orientation='h')
        st.plotly_chart(fig11, use_container_width=True)

    elif cmnd=="10.Top 10 Districts of lowest transaction count":

        sel_year = st.radio("",["2018", "2019", "2020", "2021", "2022", "2023"],horizontal=True)
        year = int(sel_year)
        
        E12 = Map_txn[["States","Years","Districts","Transaction_count"]]
        ef12 = E12[(E12["Years"] == year)]
        df12 = ef12.groupby(["States","Districts"])["Transaction_count"].sum().reset_index()
        sort_df12=df12.sort_values(by="Transaction_count", ascending=True).head(10)
        fig6 = px.bar(sort_df12,
                    y='Districts',
                    x='Transaction_count',
                    color="Transaction_count",
                    color_continuous_scale=px.colors.sequential.Redor,
                    hover_data=["States", "Transaction_count"],
                    orientation='h')
        st.plotly_chart(fig6, use_container_width=True)




        


    

    
         

    




   





        



    











































    
