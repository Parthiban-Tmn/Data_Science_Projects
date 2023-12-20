#Google cloud youtube API.
import googleapiclient.discovery
import googleapiclient.errors

#Mongodb.
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#MySql .
import mysql.connector


import pandas as pd #pandas module
import re #regular expression module
import streamlit as st #streamlit module
import time






#Process 1: Data Extraction

#API connection to interact youtube datas using python.
api_service_name = "youtube"
api_version = "v3"
api_key="AIzaSyAk28GjV-WleOjwcRPtacAfaR6bjfiBzcs"#API key copied from the youtube data api credentials.
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)#api key connection.

#Collect information for Table of channel 
def Collected_channel_datas(ch_id):
        request_channel_datas = youtube.channels().list(part="snippet,contentDetails,statistics",id=ch_id).execute()
        for catch in request_channel_datas["items"]:
            Extract_details=dict(channel_ID=catch.get('id'),
                                channel_name=catch["snippet"].get("title"),#To get channel title.
                                channel_videocount=catch["statistics"].get("videoCount"),#To get total video count.
                                channel_subscriptioncount=catch["statistics"].get("subscriberCount"),#To get channel subscriberCount.
                                channel_Totalviews=catch["statistics"].get("viewCount"),#To get channel total viewCount.
                                channel_description=catch["snippet"]["localized"].get("description"),#To get channel description.
                                channel_playlistID=catch["contentDetails"]["relatedPlaylists"].get("uploads"))#To get playlistID.
        return Extract_details

#This function is to get the video ID of all the videos posted in the channel.
def all_video_ids(ch_id):
        request_channel_datas = youtube.channels().list(part="snippet,contentDetails,statistics",id=ch_id).execute()

        list_of_video_ids=[]#To Store video ids in this list.
        next_page=str()#To save page token.
        
        while True:
            #To get playlistID's from channel list.
            playlist_id_request=request_channel_datas['items'][0]["contentDetails"]["relatedPlaylists"].get("uploads")
            Playlist_items_datas_request = youtube.playlistItems().list(part="snippet",playlistId=playlist_id_request,
                                                                        maxResults=50,pageToken=next_page).execute()
            
            #This loop is to store the videoids  
            for x in range(len(Playlist_items_datas_request['items'])):
                list_of_video_ids.append(Playlist_items_datas_request['items'][x]['snippet']['resourceId'].get('videoId'))#appends video ID for each loop
                next_page=Playlist_items_datas_request.get('nextPageToken')#Get next page token

            #This block of code will break the loop.
            if next_page is None:
                break    

        return list_of_video_ids

def change(isotime):
    try:
        isoformat = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', isotime)
        hours, minutes, seconds = map(int, isoformat.groups(default=0))#assign the values individually splitted in the isoformat
        corr_format=("{:02}:{:02}:{:02}".format(hours,minutes,seconds))
    except:
        corr_format="00:00:00"
        pass
        
    return corr_format



    #This function collects the video details and returns to Table_of_videos.
def Collected_video_datas(video_ids):
            
            datas_Collected=[]
            for V_ID in video_ids:
                video_data_request=youtube.videos().list(part="snippet,contentDetails,statistics",id=V_ID).execute()
                    
                for catch in video_data_request['items']:
                        Extract_details=dict(channel_ID=catch['snippet'].get('channelId'),             
                                Channel_Name=catch['snippet'].get('channelTitle'),#To get the Channel Name.
                                video_Id=catch.get('id'),#To get the Video ID.
                                video_name=catch['snippet'].get('title'),#To get the Video title.
                                video_publishedAt=catch['snippet'].get('publishedAt'),#To get the published date.
                                video_description=catch['snippet'].get('description'),#To get the Video description.
                                video_thumbnails=catch['snippet']['thumbnails']['default'].get('url'),#To get the Video thumbnail.
                                video_duration=change(catch['contentDetails'].get('duration')),#To get the Video duration.
                                video_viewCount=catch['statistics'].get('viewCount'),#To get the View count of the video.
                                video_likeCount=catch['statistics'].get('likeCount'),#To get the likeCount of the video.
                                video_commentsCount=catch['statistics'].get('commentCount')#To get the commentCount of the video.
                                        )
                        datas_Collected.append(Extract_details)#appends all the details of the videos.
            return datas_Collected 

client=MongoClient("mongodb+srv://parthibantmn:Parthi1234@cluster0.qdn9jou.mongodb.net/?retryWrites=true&w=majority")
db=client["Extracted_Youtube_data"]#database name
Yt_collection=db['YT_Channels']#collection name

#PROCESS 2:Data Transer-Storing datas in MongoDB ATLAS and Transfering the datas to MYSQL.

#Connection string for Mongodb
def Upload_to_mongoDB(channel_id):
      
    Table_of_channel=Collected_channel_datas(channel_id)
    Collected_video_ids=all_video_ids(channel_id)
    Table_of_Videos=Collected_video_datas(Collected_video_ids)
    Yt_collection.insert_one({"Channel Table":Table_of_channel,"Video Table":Table_of_Videos})#JSON document file name

      
    return "Collecting datas..."

#Creating tables and feeding datas into SQL
def Insert_channels_sql():

    mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               #database='joins'
                               )

    print(mydb)
    mycursor = mydb.cursor(buffered=True)


    drop_query='''drop table if exists youtube_channels.Channel_Datas'''
    mycursor.execute(drop_query)
    mydb.commit()


    Channel_Table='''CREATE TABLE if not exists youtube_channels.Channel_Datas(channel_ID varchar(250) primary key,
                    channel_name varchar(250),
                    video_count bigint,
                    subscription_count bigint,
                    Total_views bigint,
                    channel_description  text,
                    playlistID varchar(250))'''
    mycursor.execute(Channel_Table)
    mydb.commit()


   
    db=client["Extracted_Youtube_data"]
    Yt_collection=db['YT_Channels']


 #Preparing as dataframes using pandas
    channel_datas=[]
    for catch in Yt_collection.find({},{"Channel Table":1,"_id":0}):
        channel_datas.append(catch.get('Channel Table'))
    df_Ch=pd.DataFrame(channel_datas)

    #iterrows() - used for iterating over the rows as (index, series) pairs.
    for ch_index,ch_row in df_Ch.iterrows():
                    try:   
                        push_channel_Datas='''INSERT INTO youtube_channels.Channel_Datas(channel_ID,channel_name,video_count,subscription_count,
                        Total_views,channel_description,playlistID)values(%s,%s,%s,%s,%s,%s,%s)'''
                        datas=(ch_row['channel_ID'],
                            ch_row['channel_name'],
                            ch_row['channel_videocount'],
                            ch_row['channel_subscriptioncount'],
                            ch_row['channel_Totalviews'],
                            ch_row['channel_description'],
                            ch_row['channel_playlistID'])
                        mycursor.execute(push_channel_Datas,datas)
                        mydb.commit()
                    except:
                           pass


def Insert_videos_sql():

    mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               #database='joins'
                               )

    print(mydb)
    mycursor = mydb.cursor(buffered=True)


    drop_query='''drop table if exists youtube_channels.Video_Datas'''
    mycursor.execute(drop_query)
    mydb.commit()



    Video_Table='''CREATE TABLE if not exists youtube_channels.Video_Datas(channel_ID varchar(250),    
    Channel_Name varchar(250),
    video_Id varchar(250) primary key,
    video_name varchar(250),
    video_publishedAt DATETIME,
    video_description varchar(225),
    video_thumbnails varchar(225),
    video_duration TIME,
    video_viewCount bigint,
    video_likeCount bigint,
    video_commentsCount bigint)'''

    mycursor.execute(Video_Table)
    mydb.commit()




    Video_datas=[]
    vid_id_list=[]
    for catch in Yt_collection.find({},{"Video Table":1,"_id":0}):
        for i in range (len(catch["Video Table"])):
            vid_id=catch['Video Table'][i]['video_Id']
            if vid_id not in vid_id_list:
                vid_id_list.append(vid_id)
                Video_datas.append(catch.get('Video Table')[i])
            else:
                continue
    df_Videos=pd.DataFrame(Video_datas)

        
    for index,row in df_Videos.iterrows(): 
                    try:
                        push_Video_Datas='''INSERT INTO youtube_channels.Video_Datas(channel_ID,Channel_Name,video_Id,video_name,video_publishedAt,
                                        video_description,video_thumbnails,video_duration,video_viewCount,video_likeCount,video_commentsCount)
                                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''      
                        datas=(row['channel_ID'],
                            row['Channel_Name'],
                                row['video_Id'],
                                row['video_name'],
                                row['video_publishedAt'],
                                row['video_description'],
                                row['video_thumbnails'],
                                row['video_duration'],
                                row['video_viewCount'],
                                row['video_likeCount'],
                                row['video_commentsCount'])
                        mycursor.execute(push_Video_Datas,datas)
                        mydb.commit()

                    except:
                        pass

def insert_tables():
    Insert_channels_sql()
    Insert_videos_sql()
    return "Few seconds to go........"


st.header('Hello,there...')


inf=("""   
1.Go to YOUTUBE.COM and search channel name.     
2.Click the channel name to enter into the channel.  
3.Select the Description or About tab of the channel.  
4.Click share Channel option and select Copy Channel ID.  
5.Create a variable and paste the copied channel ID as string type
""")





tab1, tab2= st.tabs(["Extract and Transfer","Insights"])



with tab1:
    with st.expander("To get Channel ID"):
        st.write(inf)
    Receive_id=st.text_input("Paste a Channel ID Below:")
    channel_id = Receive_id.split(',')#split if multiple ID's
    channel_id = [ch.strip() for ch in channel_id if ch]#to remove blank spaces in given IDs.

    progress_text = "Loading........"
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    if st.button("Extract and Transfer"):
        ch_id_list = []
        for Given_id in channel_id:
            for catch in Yt_collection.find({},{"Channel Table":1,"_id":0}):
                    ch_id_list.append(catch["Channel Table"].get('channel_ID'))
            if Given_id not in ch_id_list:
                    store_datas=Upload_to_mongoDB(Given_id)
                    st.success(store_datas)
                    Push_tables=insert_tables()
                    st.success(Push_tables)
                    with st.spinner('Please wait...........'):
                        time.sleep(5)
                        st.success('Channel datas collected.Please check insights....')
            else:
                    st.success("Given channel datas already exists")
            


# Using "with" notation
with st.sidebar:
     st.header("About")
     st.write('''
**Youtube Data Harvesting and Warehousing**

**Introduction:**
YouTube, as one of the largest platforms for video content, generates an enormous volume of data on a daily basis. This essay aims to delve into the process of extracting data from the Google Cloud using the YouTube Data API with the help of Python, saving it in MongoDB, transferring it from MongoDB to SQL, and using Streamlit to build a website for data manipulation and interaction.

**Extracting Data from Google Cloud Console Using YouTube Data API with Python:**
The extraction process typically involves identifying the specific data elements required, such as video metadata, view counts, likes, comments, and other relevant information. Python's rich ecosystem of libraries, including requests and google-api-python-client, facilitates the interaction with the YouTube Data API, enabling the retrieval of data in a structured and organized manner.

**Saving Data in MongoDB:**

Once the data is extracted from the YouTube platform using the YouTube Data API, the next step involves storing this data in a suitable database for further processing and analysis. MongoDB, a popular NoSQL database, offers a flexible and scalable solution for storing unstructured or semi-structured data, making it an ideal choice for accommodating the diverse nature of YouTube data.

**Transferring Data from MongoDB to SQL:**

In some scenarios, the need may arise to transfer the data from MongoDB, a NoSQL database, to a traditional SQL database for various reasons such as integration with existing systems, standardized querying, or relational data modeling. This transition involves a careful consideration of data mapping, transformation, and migration strategies to ensure the integrity and consistency of the data throughout the transfer process.

**Using Streamlit to Build a Website:**

After the data has been extracted, stored, and transferred, the next phase involves leveraging Streamlit, a popular open-source framework to create a website for interactive data visualization, manipulation, and exploration. Streamlit's intuitive and user-friendly interface, coupled with its seamless integration with Python, makes it an ideal choice for rapidly developing and deploying data-driven web applications.

**Creating Questions and Manipulating Data from SQL in Streamlit:**

To achieve this, Streamlit offers a range of input components, such as text inputs, dropdowns, and sliders, to capture user queries or parameters. These inputs can be seamlessly integrated with Python code to formulate SQL queries dynamically based on user input. The retrieved data from the SQL database can be further processed, transformed, and presented back to the user through interactive visualizations or tabular representations, enabling a rich and immersive data exploration experience.
**Technologies Used**

The following technologies are used in this project:

- YouTube API: Google API is used to retrieve channel and video data from YouTube.
- Python: The programming language used for building the application and scripting tasks.
- MongoDB: A NoSQL database used as a data lake for storing retrieved YouTube data.
- SQL (MySQL): A relational database used as a data warehouse for storing migrated YouTube data.
- Streamlit: A Python library used for creating interactive web applications and data visualizations.

**Conclusion:**
  
In conclusion, the process of YouTube data harvesting and warehousing, encompassing the extraction of data from the Google Cloud using the YouTube Data API with Python, saving it in MongoDB, transferring it to SQL, and building a website using Streamlit for interactive data manipulation, embodies a multifaceted and intricate workflow. By leveraging the capabilities of Python, MongoDB, SQL, and Streamlit, organizations and data enthusiasts can harness the wealth of information available on YouTube to derive valuable insights, drive informed decision-making, and unlock the potential of big data in the digital age.


**References**

- YouTube API Documentation: [https://developers.google.com/youtube](https://developers.google.com/youtube)
- Python Documentation: [https://docs.python.org/](https://docs.python.org/)
- MongoDB Documentation: [https://docs.mongodb.com/](https://docs.mongodb.com/)
- Streamlit Documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)

''')



with tab2:
    Q = st.selectbox("Select the commands below:",
                    ('List of all channels',
                    'What are the names of all the videos and their corresponding channels?',
                    'Which channels have the most number of videos, and how many videos do they have?',
                    'What are the top 10 most viewed videos and their respective channels?',
                    'How many comments were made on each video, and what are their corresponding video names?',
                    'Which videos have the highest number of likes, and what are their corresponding channel names?',
                    'What is the total number of likes for each video, and what are their corresponding video names?',
                    'What is the total number of views for each channel, and what are their corresponding channel names?',
                    'What are the names of all the channels that have published videos in the year 2022?',
                    'What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                    'Which videos have the highest number of comments, and what are their corresponding channel names?'),index=None,placeholder="Select")


    mydb = mysql.connector.connect(host="localhost",
                                user="root",
                                password="",
                                #database='joins'
                                )
    print(mydb)
    mycursor = mydb.cursor(buffered=True)




    if Q=='List of all channels':
        C1 = "SELECT channel_name,subscription_count FROM youtube_channels.Channel_datas ORDER BY channel_name ASC"
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        mycursor.execute(C1)
        mydb.commit()
        E1=mycursor.fetchall()
        st.write(pd.DataFrame(E1,columns=["Channel Name","Total Subscribers"],index=pd.RangeIndex(start=1,stop=len(E1)+1,name="S.no")))


    if Q=='What are the names of all the videos and their corresponding channels?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C2 = "SELECT Video_name,channel_name FROM youtube_channels.Video_datas ORDER BY channel_name ASC"
        mycursor.execute(C2)
        mydb.commit()
        E2=mycursor.fetchall()
        st.write(pd.DataFrame(E2,columns=["video name","Channel Name"],index=pd.RangeIndex(start=1,stop=len(E2)+1,name="S.no")))




    if Q=='Which channels have the most number of videos, and how many videos do they have?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C3 = "SELECT channel_name,Video_count FROM youtube_channels.Channel_datas ORDER BY Video_count DESC"
        mycursor.execute(C3)
        mydb.commit()
        E3=mycursor.fetchall()
        st.write(pd.DataFrame(E3,columns=["Channel name","Total Videos"],index=pd.RangeIndex(start=1,stop=len(E3)+1,name="S.no")))

    if Q=='What are the top 10 most viewed videos and their respective channels?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C3 = "SELECT channel_name,video_viewcount,video_name FROM youtube_channels.Video_datas ORDER BY video_viewcount DESC limit 10"
        mycursor.execute(C3)
        mydb.commit()
        E3=mycursor.fetchall()
        st.write(pd.DataFrame(E3,columns=["Channel name","Total Views","video name",],index=pd.RangeIndex(start=1,stop=len(E3)+1,name="S.no")))

    if Q=='How many comments were made on each video, and what are their corresponding video names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C4 = "SELECT channel_name,video_commentscount,video_name FROM youtube_channels.Video_datas ORDER BY video_commentscount DESC"
        mycursor.execute(C4)
        mydb.commit()
        E4=mycursor.fetchall()
        st.write(pd.DataFrame(E4,columns=["Channel name","Total comments","video name"],index=pd.RangeIndex(start=1,stop=len(E4)+1,name="S.no")))


    if Q=='Which videos have the highest number of likes, and what are their corresponding channel names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C5 = "SELECT channel_name,video_likecount,video_name FROM youtube_channels.Video_datas ORDER BY video_likecount DESC"
        mycursor.execute(C5)
        mydb.commit()
        E5=mycursor.fetchall()
        st.write(pd.DataFrame(E5,columns=["Channel name","Total likes","video name"],index=pd.RangeIndex(start=1,stop=len(E5)+1,name="S.no")))



    if Q=='What is the total number of likes for each video, and what are their corresponding video names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C6 = "SELECT video_likecount,video_name FROM youtube_channels.Video_datas ORDER BY video_likecount desc"
        mycursor.execute(C6)
        mydb.commit()
        E6=mycursor.fetchall()
        st.write(pd.DataFrame(E6,columns=["Total likes","video name"],index=pd.RangeIndex(start=1,stop=len(E6)+1,name="S.no")))


    if Q=='What is the total number of views for each channel, and what are their corresponding channel names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C7 = "SELECT channel_name,Total_views FROM youtube_channels.Channel_datas ORDER BY Total_views DESC"
        mycursor.execute(C7)
        mydb.commit()
        E7=mycursor.fetchall()
        st.write(pd.DataFrame(E7,columns=["Channel name","Total Views"],index=pd.RangeIndex(start=1,stop=len(E7)+1,name="S.no")))    

    if Q=='What are the names of all the channels that have published videos in the year 2022?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C8 = '''SELECT channel_name,COUNT(*)
        FROM youtube_channels.Video_datas
        WHERE YEAR(video_publishedat) = 2022
        GROUP BY YEAR(video_publishedat),channel_name'''
        mycursor.execute(C8)
        mydb.commit()
        E8=mycursor.fetchall()
        st.write(pd.DataFrame(E8,columns=["Channel Name","videos posted on 2022"],index=pd.RangeIndex(start=1,stop=len(E8)+1,name="S.no")))  



    if Q=='What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Here your results.Fuiyoh!...')
        C9 = '''SELECT channel_name,sec_to_time(AVG(video_duration))
        FROM youtube_channels.Video_datas
        GROUP BY channel_name ASC'''
        mycursor.execute(C9)
        mydb.commit()
        E9=mycursor.fetchall()
        st.write(pd.DataFrame(E9,columns=["Channel Name","Average duration"],index=pd.RangeIndex(start=1,stop=len(E9)+1,name="S.no")))     


    if Q=='Which videos have the highest number of comments, and what are their corresponding channel names?':
        with st.spinner('Please wait...........'):
            time.sleep(5)
            st.success('Fuiyoh!,Here your results........')
        C10 = "SELECT SUM(video_commentscount),channel_name FROM youtube_channels.Video_datas GROUP BY channel_name order by video_commentscount desc"
        mycursor.execute(C10)
        mydb.commit()
        E10=mycursor.fetchall()
        st.write(pd.DataFrame(E10,columns=["Total comments","channel name"],index=pd.RangeIndex(start=1,stop=len(E10)+1,name="S.no")))


































