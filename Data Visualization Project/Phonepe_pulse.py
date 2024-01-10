import requests
import pandas as pd
import numpy as np
import json
import mysql.connector
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu


#sql connection
mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               #database='joins'
                               )
mycursor = mydb.cursor(buffered=True)



st.set_page_config(layout="wide")

selected = option_menu(None,
                       options = ["About","Home","Analysis","Insights",],
                       icons = ["bar-chart","house","toggles","at"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "white", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-4px" ,"--hover-color": "#800080"},
                               "nav-link-selected": {"background-color": "#800080"},
                               "nav": {"background-color": "#E6E6FA"}})


# ABOUT PAGE
if selected == "About":
    col1, col2, = st.columns(2)
    col1.image("https://tse3.mm.bing.net/th?id=OIP.eCSo2z86EagDx42Ie9-9RQHaDt&pid=Api&P=0&h=180", width=500)
    with col1:
        st.subheader(
            "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.markdown("[DOWNLOAD APP](https://www.phonepe.com/app-download/)")

    with col2:
        st.image("https://www.techgenyz.com/wp-content/uploads/2021/09/PhonePe.jpg")


# HOME PAGE
if selected == "Home":
    col1,col2 = st.columns(2)
    with col1:
        st.video("https://youtu.be/c_1H6vivsiA")
    with col2:
        st.title(':violet[PHONEPE PULSE DATA VISUALISATION]')
        st.subheader(':violet[Phonepe Pulse]:')
        st.write('PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.')
        st.subheader(':violet[Phonepe Pulse Data Visualisation]:')
        st.write('Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.'
                 'The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.')

    st.write("---")


# ANALYSIS PAGE
if selected == "Analysis":
    st.title(':violet[ANALYSIS]')
    st.subheader('Analysis done on the basis of All India ,States, Districts and Top categories between 2018 and 2023')
    select = option_menu(None,
                         options=["INDIA", "STATES", "TOP CATEGORIES" ],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                   "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})
    if select == "INDIA":
        tab1, tab2 = st.tabs(["TRANSACTION","USER"])

        # TRANSACTION TAB
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                in_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='in_tr_yr')
            with col2:
                in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')
            with col3:
                in_tr_tr_typ = st.selectbox('**Select Transaction type**',
                                            ('Recharge & bill payments', 'Peer-to-peer payments',
                                             'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')
            try:
                # Transaction Analysis bar chart query
                cursor.execute(
                    f"SELECT States, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
                in_tr_tab_qry_rslt = cursor.fetchall()
                df_in_tr_tab_qry_rslt = pd.DataFrame(np.array(in_tr_tab_qry_rslt), columns=['State', 'Transaction_amount'])
                df_in_tr_tab_qry_rslt1 = df_in_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_tab_qry_rslt) + 1)))

                # Transaction Analysis table query
                cursor.execute(
                    f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
                in_tr_anly_tab_qry_rslt = cursor.fetchall()
                df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt),
                                                        columns=['State', 'Transaction_count', 'Transaction_amount'])
                df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(
                    pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt) + 1)))

                # Total Transaction Amount table query
                cursor.execute(
                    f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
                in_tr_am_qry_rslt = cursor.fetchall()
                df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total', 'Average'])
                df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])

                # Total Transaction Count table query
                cursor.execute(
                    f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Years = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
                in_tr_co_qry_rslt = cursor.fetchall()
                df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total', 'Average'])
                df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])
                col,cols=st.columns([2,2])
                with col:
                    # GEO VISUALISATION
                    # Drop a State column from df_in_tr_tab_qry_rslt
                    df_in_tr_tab_qry_rslt.drop(columns=['State'], inplace=True)
                    # Clone the gio data
                    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                    response = requests.get(url)
                    data1 = json.loads(response.content)
                    # Extract state names and sort them in alphabetical order
                    state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
                    state_names_tra.sort()
                    # Create a DataFrame with the state names column
                    df_state_names_tra = pd.DataFrame({'State': state_names_tra})
                    # Combine the Gio State name with df_in_tr_tab_qry_rslt
                    df_state_names_tra['Transaction_amount'] = df_in_tr_tab_qry_rslt
                    # convert dataframe to csv file
                    df_state_names_tra.to_csv('State_trans.csv', index=False)
                    # Read csv
                    df_tra = pd.read_csv('State_trans.csv')
                    # Geo plot
                    fig_tra = px.choropleth(
                        df_tra,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
                        color_continuous_scale='thermal', title='Transaction Analysis')
                    fig_tra.update_geos(fitbounds="locations", visible=False)
                    fig_tra.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
                    st.plotly_chart(fig_tra, use_container_width=True)

                    # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
                    df_in_tr_tab_qry_rslt1['State'] = df_in_tr_tab_qry_rslt1['State'].astype(str)
                    df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
                    df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1, x='State', y='Transaction_amount',
                                                        color='Transaction_amount', color_continuous_scale='thermal',
                                                        title='Transaction Analysis Chart', height=700, )
                    df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
                    st.plotly_chart(df_in_tr_tab_qry_rslt1_fig, use_container_width=True)

                # -------  /  All India Total Transaction calculation Table   /   ----  #
                with cols:
                    col4, col5 = st.columns(2)
                    with col4:
                        st.subheader(':violet[Transaction Analysis]')
                        st.dataframe(df_in_tr_anly_tab_qry_rslt1)
                    with col5:
                        st.subheader(':violet[Transaction Amount]')
                        st.dataframe(df_in_tr_am_qry_rslt1)
                        st.subheader(':violet[Transaction Count]')
                        st.dataframe(df_in_tr_co_qry_rslt1)
            except:
                pass

        # USER TAB
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='in_us_yr')
            with col2:
                in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')

            # SQL Query
            try:
                # User Analysis Bar chart query
                cursor.execute(f"SELECT States, SUM(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY States;")
                in_us_tab_qry_rslt = cursor.fetchall()
                df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['State', 'User Count'])
                df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

                # Total User Count table query
                cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_user WHERE Years = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
                in_us_co_qry_rslt = cursor.fetchall()
                df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total', 'Average'])
                df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])



                # GEO VISUALIZATION FOR USER

                # Drop a State column from df_in_us_tab_qry_rslt
                df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
                # Clone the gio data
                url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
                response = requests.get(url)
                data2 = json.loads(response.content)
                # Extract state names and sort them in alphabetical order
                state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
                state_names_use.sort()
                # Create a DataFrame with the state names column
                df_state_names_use = pd.DataFrame({'State': state_names_use})
                # Combine the Gio State name with df_in_tr_tab_qry_rslt
                df_state_names_use['User Count'] = df_in_us_tab_qry_rslt
                # convert dataframe to csv file
                df_state_names_use.to_csv('State_user.csv', index=False)
                # Read csv
                df_use = pd.read_csv('State_user.csv')
                # Geo plot
                fig_use = px.choropleth(
                    df_use,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM', locations='State', color='User Count',
                    color_continuous_scale='thermal', title='User Analysis')
                fig_use.update_geos(fitbounds="locations", visible=False)
                fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
                st.plotly_chart(fig_use, use_container_width=True)

                # ----   /   All India User Analysis Bar chart   /     -------- #
                df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
                df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
                df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='State', y='User Count', color='User Count',
                                                    color_continuous_scale='thermal', title='User Analysis Chart',
                                                    height=700, )
                df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
                st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)

                # -----   /   All India Total User calculation Table   /   ----- #
                st.header(':violet[Total calculation]')

                col3, col4 = st.columns(2)
                with col3:
                    st.subheader(':violet[User Analysis]')
                    st.dataframe(df_in_us_tab_qry_rslt1)
                with col4:
                    st.subheader(':violet[User Count]')
                    st.dataframe(df_in_us_co_qry_rslt1)
            except:
                pass

    # STATE TAB
    if select == "STATES":
        tab3 ,tab4 = st.tabs(["TRANSACTION","USER"])
        #TRANSACTION TAB FOR STATE
        with tab3:
            col1, col2, col3 = st.columns(3)
            with col1:
                st_tr_st = st.selectbox('**Select State**', (
                'Andaman & Nicobar', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar',
                'chandigarh', 'chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal pradesh',
                'jammu & kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh',
                'maharashtra', 'manipur',
                'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                'tamil nadu', 'telangana',
                'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal'), key='st_tr_st')
            with col2:
                st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='st_tr_yr')
            with col3:
                st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')
            

            # SQL QUERY
            try:
                #Transaction Analysis bar chart query
                cursor.execute(f"SELECT District,Transaction_amount FROM map_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
                st_tr_tab_bar_qry_rslt = cursor.fetchall()
                df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt),
                                                        columns=['Districts','Transaction_amount'])
                df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(
                    pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt) + 1)))

                # Transaction Analysis table query
                cursor.execute(f"SELECT District, Transaction_count, Transaction_amount FROM map_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
                st_tr_anly_tab_qry_rslt = cursor.fetchall()
                df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt),
                                                        columns=['Districts', 'Transaction_count',
                                                                'Transaction_amount'])
                df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(
                    pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt) + 1)))

                # Total Transaction Amount table query
                cursor.execute(f"SELECT District,SUM(Transaction_amount), AVG(Transaction_amount) FROM map_transaction WHERE States = '{st_tr_st}' AND Years = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}'  group by District;")
                st_tr_am_qry_rslt = cursor.fetchall()
                df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Districts', 'Total', 'Average'])
                df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])

                # Total Transaction Count table query
                cursor.execute(f"SELECT District,SUM(Transaction_count), AVG(Transaction_count) FROM map_transaction WHERE States = '{st_tr_st}' AND Years ='{st_tr_yr}' AND Quarter = '{st_tr_qtr}' group by District;")
                st_tr_co_qry_rslt = cursor.fetchall()
                df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Districts','Total', 'Average'])
                df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])



                # -----    /   State wise Transaction Analysis bar chart   /   ------ #

                df_st_tr_tab_bar_qry_rslt1['Districts'] = df_st_tr_tab_bar_qry_rslt1['Districts'].astype(str)
                df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(
                    float)
                df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1, x='Districts',
                                                        y='Transaction_amount', color='Transaction_amount',
                                                        color_continuous_scale='thermal',
                                                        title='Transaction Analysis Chart', height=500, )
                df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
                st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig, use_container_width=True)

                # ------  /  State wise Total Transaction calculation Table  /  ---- #
                st.header(':violet[Total calculation]')

                col4, col5 = st.columns(2)
                with col4:
                    st.subheader(':violet[Transaction Analysis]')
                    st.dataframe(df_st_tr_anly_tab_qry_rslt1)
                with col5:
                    st.subheader(':violet[Transaction Amount]')
                    st.dataframe(df_st_tr_am_qry_rslt1)
                    st.subheader(':violet[Transaction Count]')
                    st.dataframe(df_st_tr_co_qry_rslt1)
            except:
                pass

        # USER TAB FOR STATE
        with tab4:
            col5, col6,col7 = st.columns(3)
            try:
                with col5:
                    st_us_st = st.selectbox('**Select State**', (
                    'Andaman & Nicobar', 'andhra pradesh', 'arunachal pradesh', 'assam', 'bihar',
                    'chandigarh', 'chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'delhi', 'goa', 'gujarat',
                    'haryana', 'himachal pradesh',
                    'jammu & kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya pradesh',
                    'maharashtra', 'manipur',
                    'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                    'tamil nadu', 'telangana',
                    'tripura', 'uttar pradesh', 'uttarakhand', 'west bengal'), key='st_us_st')
                with col6:
                    st_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='st_us_yr')
                with col7:
                    st_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_us_qtr')
                
                column1,column2 = st.columns(2)
                # SQL QUERY
                try:
                    # User Analysis Bar chart query
                    
                    cursor.execute(f"SELECT Districts, SUM(registeredUser) FROM map_user WHERE States = '{st_us_st}' AND Years = '{st_us_yr}' AND Quarter = '{st_us_qtr}' GROUP BY Districts;")
                    st_us_tab_qry_rslt = cursor.fetchall()
                    df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['District', 'User Count'])
                    df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt) + 1)))

                    # Total User Count table query
                    cursor.execute(f"SELECT Districts,SUM(registeredUser), AVG(registeredUser) FROM map_user WHERE States = '{st_us_st}' AND Years = '{st_us_yr}' AND Quarter = '{st_us_qtr}' GROUP BY Districts;")
                    st_us_co_qry_rslt = cursor.fetchall()
                    df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['District','Total', 'Average'])
                    df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['District'])
                except:
                    pass

                with column1:

                    # -----   /   All India User Analysis Bar chart   /   ----- #
                    #df_st_us_tab_qry_rslt1['District'] = df_st_us_tab_qry_rslt1['District'].astype(int)
                    df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
                    df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1, x='District', y='User Count', color='User Count',
                                                        color_continuous_scale='thermal', title='User Analysis Chart',
                                                        height=500, )
                    df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
                    st.plotly_chart(df_st_us_tab_qry_rslt1_fig, use_container_width=True)



                # ------    /   district wise User Total User calculation Table   /   -----#
                with column2:
                    st.header(':violet[Total calculation]')

                    col3, col4 = st.columns(2)
                    with col3:
                        st.subheader(':violet[User Analysis]')
                        st.dataframe(df_st_us_tab_qry_rslt1)
                    with col4:
                        st.subheader(':violet[User Count]')
                        st.dataframe(df_st_us_co_qry_rslt1)
            except:
                pass

    # TOP CATEGORIES
    if select == "TOP CATEGORIES":
        tab5, tab6 = st.tabs(["TRANSACTION", "USER"])

        # Overall top transaction
        #TRANSACTION TAB
        with tab5:
            top_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='top_tr_yr')

            #SQL QUERY

            #Top Transaction Analysis bar chart query
            cursor.execute(
                f"SELECT States, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Years = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
            top_tr_tab_qry_rslt = cursor.fetchall()
            df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt),
                                                  columns=['State', 'Top Transaction amount'])
            df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_tr_tab_qry_rslt) + 1)))

            # Top Transaction Analysis table query
            cursor.execute(
                f"SELECT States, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Years = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
            top_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt),
                                                       columns=['State', 'Top Transaction amount',
                                                                'Total Transaction count'])
            df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt) + 1)))



            # All India Transaction Analysis Bar chart
            df_top_tr_tab_qry_rslt1['State'] = df_top_tr_tab_qry_rslt1['State'].astype(str)
            df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1[
                'Top Transaction amount'].astype(float)
            df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1, x='State', y='Top Transaction amount',
                                                 color='Top Transaction amount', color_continuous_scale='thermal',
                                                 title='Top Transaction Analysis Chart', height=600, )
            df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_top_tr_tab_qry_rslt1_fig, use_container_width=True)


            #All India Total Transaction calculation Table
            st.header(':violet[Total calculation]')
            st.subheader('Top Transaction Analysis')
            st.dataframe(df_top_tr_anly_tab_qry_rslt1)

        # OVERALL TOP USER DATA
        # USER TAB
        with tab6:
            top_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022','2023'), key='top_us_yr')

            #SQL QUERY

            #Top User Analysis bar chart query
            cursor.execute(f"SELECT States, SUM(RegisteredUser) AS Top_user FROM top_user WHERE Years='{top_us_yr}' GROUP BY States ORDER BY Top_user DESC LIMIT 10;")
            top_us_tab_qry_rslt = cursor.fetchall()
            df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['State', 'Total User count'])
            df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(
                pd.Index(range(1, len(df_top_us_tab_qry_rslt) + 1)))



            #All India User Analysis Bar chart
            df_top_us_tab_qry_rslt1['State'] = df_top_us_tab_qry_rslt1['State'].astype(str)
            df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
            df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1, x='State', y='Total User count',
                                                 color='Total User count', color_continuous_scale='thermal',
                                                 title='Top User Analysis Chart', height=600, )
            df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
            st.plotly_chart(df_top_us_tab_qry_rslt1_fig, use_container_width=True)

            #All India Total Transaction calculation Table
            st.header(':violet[Total calculation]')
            st.subheader(':violet[Total User Analysis]')
            st.dataframe(df_top_us_tab_qry_rslt1)

#INSIGHTS TAB
if selected == "Insights":
    st.title(':violet[BASIC INSIGHTS]')
    st.subheader("The basic insights are derived from the Analysis of the Phonepe Pulse data. It provides a clear idea about the analysed data.")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "Least 10 states based on year and amount of transaction",
               "Top 10 States and Districts based on Registered Users",
               "Least 10 States and Districts based on Registered Users",
               "Top 10 Districts based on the Transaction Amount",
               "Least 10 Districts based on the Transaction Amount",
               "Top 10 Districts based on the Transaction count",
               "Least 10 Districts based on the Transaction count",
               "Top Transaction types based on the Transaction Amount",
               "Top 10 Mobile Brands based on the User count of transaction"]
    select = st.selectbox(":violet[Select the option]",options)

    #1
    if select == "Top 10 states based on year and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT States, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY States ORDER BY Total_Transaction_Amount DESC LIMIT 10");

        data = cursor.fetchall()
        columns = ['States', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states based on amount of transaction")
            fig_px=px.pie(df, values= "Transaction_amount", names= "States", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
            st.plotly_chart(fig_px)

    #2
    elif select == "Least 10 states based on year and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT States,Years, SUM(Transaction_amount) as Total FROM top_transaction GROUP BY States, Years ORDER BY Total ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'Year', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 states based on amount of transaction")
            st.bar_chart(data=df, x="Transaction_amount", y="States")

    #3
    elif select == "Top 10 States and Districts based on Registered Users":
        cursor.execute("SELECT DISTINCT States, Pincodes, SUM(RegisteredUser) AS Users FROM top_user GROUP BY States, Pincodes ORDER BY Users DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['State', 'District_Pincode', 'Registered_User']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 States and Districts based on Registered Users")
            st.bar_chart(data=df, x="Registered_User", y="State")

    #4
    elif select == "Least 10 States and Districts based on Registered Users":
        cursor.execute("SELECT DISTINCT States, Pincodes, SUM(RegisteredUser) AS Users FROM top_user GROUP BY States, Pincodes ORDER BY Users ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['State', 'District_Pincode', 'Registered_User']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 States and Districts based on Registered Users")
            st.bar_chart(data=df, x="Registered_User", y="State")

    #5
    elif select == "Top 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT States ,District,SUM(Transaction_amount) AS Total FROM map_transaction GROUP BY States ,District ORDER BY Total DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on Transaction Amount")
            st.bar_chart(data=df, x="District", y="Transaction_Amount")

    #6
    elif select == "Least 10 Districts based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT States,District,SUM(Transaction_amount) AS Total FROM map_transaction GROUP BY States, District ORDER BY Total ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on Transaction Amount")
            st.bar_chart(data=df, x="District", y="Transaction_amount")

    #7
    elif select == "Top 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT States,District,SUM(Transaction_count) AS Counts FROM map_transaction GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on Transaction Count")
            st.bar_chart(data=df, x="Transaction_Count", y="District")

    #8
    elif select == "Least 10 Districts based on the Transaction count":
        cursor.execute(
            "SELECT DISTINCT States,District,SUM(Transaction_count) AS Counts FROM map_transaction GROUP BY States ,District ORDER BY Counts ASC LIMIT 10");
        data = cursor.fetchall()
        columns = ['States', 'District', 'Transaction_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on the Transaction Count")
            st.bar_chart(data=df, x="Transaction_Count", y="District")

    #9
    elif select == "Top Transaction types based on the Transaction Amount":
        cursor.execute(
            "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM aggregated_transaction GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5");
        data = cursor.fetchall()
        columns = ['Transaction_type', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top Transaction Types based on the Transaction Amount")
            st.bar_chart(data=df, x="Transaction_type", y="Transaction_amount")

    #10
    elif select == "Top 10 Mobile Brands based on the User count of transaction":
        cursor.execute(
            "SELECT DISTINCT Brands,SUM(Transaction_count) as Total FROM aggregated_user GROUP BY Brands ORDER BY Total DESC LIMIT 10");
        data = cursor.fetchall()
        columns = ['Brands', 'User_Count']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))

        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Mobile Brands based on User count of transaction")
            st.bar_chart(data=df , x="User_Count", y="Brands")
