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



#PROCESS 1: DATA EXTRACTION

"""
TO GET CHANNEL ID:
1.Go to YOUTUBE.COM and search channel name. 
2.Click the channel name to enter into the channel.
3.Select the Description or About tab of the channel.
4.Click share Channel option and select Copy Channel ID.
5.Create a variable and paste the copied channel ID as string type.
"""

#village cooking channel-UCk3JZr7eS3pg5AGEvBdEvFg
#czn burak-UCUcfej7lPDoeqTlferD2mcw
#uncle roger-UCVjlpEjEY9GpksqbEesJnNA
#wilderness cooking-UCj4KP216972cPp2w_BAHy8g
#Gordan ramsey-UCIEv3lZ_tNXHzL3ox-_uUGQ
#patrick-UC_35hRJlT4PEmvFCcU6l_3Q


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

      
    return "uploaded to mongoDB"

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
    return "Done"


Receive_id=st.text_input("Give the Channel ID:")
channel_id = Receive_id.split(',')#split if multiple ID's
channel_id = [ch.strip() for ch in channel_id if ch]#to remove blank spaces in given IDs.



if st.button("Collect and Store data"):
    ch_id_list = []
    for Given_id in channel_id:
        for catch in Yt_collection.find({},{"Channel Table":1,"_id":0}):
                ch_id_list.append(catch["Channel Table"].get('channel_ID'))
        if Given_id not in ch_id_list:
                store_datas=Upload_to_mongoDB(Given_id)
                st.success(store_datas)

        else:
                st.success("Given channel datas already exists")

if st.button("Transfer to SQL"):
    Push_tables=insert_tables()
    st.success(Push_tables)

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()




Q = st.selectbox("Select Commands:",
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
    mycursor.execute(C1)
    mydb.commit()
    E1=mycursor.fetchall()
    st.write(pd.DataFrame(E1,columns=["Channel Name","Total Subscribers"],index=pd.RangeIndex(start=1,stop=len(E1)+1,name="S.no")))


if Q=='What are the names of all the videos and their corresponding channels?':
    C2 = "SELECT Video_name,channel_name FROM youtube_channels.Video_datas ORDER BY channel_name ASC"
    mycursor.execute(C2)
    mydb.commit()
    E2=mycursor.fetchall()
    st.write(pd.DataFrame(E2,columns=["video name","Channel Name"],index=pd.RangeIndex(start=1,stop=len(E2)+1,name="S.no")))




if Q=='Which channels have the most number of videos, and how many videos do they have?':
    C3 = "SELECT channel_name,Video_count FROM youtube_channels.Channel_datas ORDER BY Video_count DESC"
    mycursor.execute(C3)
    mydb.commit()
    E3=mycursor.fetchall()
    st.write(pd.DataFrame(E3,columns=["Channel name","Total Videos"],index=pd.RangeIndex(start=1,stop=len(E3)+1,name="S.no")))

if Q=='What are the top 10 most viewed videos and their respective channels?':
    C3 = "SELECT channel_name,video_viewcount,video_name FROM youtube_channels.Video_datas ORDER BY video_viewcount DESC limit 10"
    mycursor.execute(C3)
    mydb.commit()
    E3=mycursor.fetchall()
    st.write(pd.DataFrame(E3,columns=["Channel name","Total Views","video name",],index=pd.RangeIndex(start=1,stop=len(E3)+1,name="S.no")))

if Q=='How many comments were made on each video, and what are their corresponding video names?':
    C4 = "SELECT channel_name,video_commentscount,video_name FROM youtube_channels.Video_datas ORDER BY video_commentscount DESC"
    mycursor.execute(C4)
    mydb.commit()
    E4=mycursor.fetchall()
    st.write(pd.DataFrame(E4,columns=["Channel name","Total comments","video name"],index=pd.RangeIndex(start=1,stop=len(E4)+1,name="S.no")))


if Q=='Which videos have the highest number of likes, and what are their corresponding channel names?':
    C5 = "SELECT channel_name,video_likecount,video_name FROM youtube_channels.Video_datas ORDER BY video_likecount DESC"
    mycursor.execute(C5)
    mydb.commit()
    E5=mycursor.fetchall()
    st.write(pd.DataFrame(E5,columns=["Channel name","Total likes","video name"],index=pd.RangeIndex(start=1,stop=len(E5)+1,name="S.no")))



if Q=='What is the total number of likes for each video, and what are their corresponding video names?':
    C6 = "SELECT video_likecount,video_name FROM youtube_channels.Video_datas ORDER BY video_likecount desc"
    mycursor.execute(C6)
    mydb.commit()
    E6=mycursor.fetchall()
    st.write(pd.DataFrame(E6,columns=["Total likes","video name"],index=pd.RangeIndex(start=1,stop=len(E6)+1,name="S.no")))


if Q=='What is the total number of views for each channel, and what are their corresponding channel names?':
    C7 = "SELECT channel_name,Total_views FROM youtube_channels.Channel_datas ORDER BY Total_views DESC"
    mycursor.execute(C7)
    mydb.commit()
    E7=mycursor.fetchall()
    st.write(pd.DataFrame(E7,columns=["Channel name","Total Views"],index=pd.RangeIndex(start=1,stop=len(E7)+1,name="S.no")))    

if Q=='What are the names of all the channels that have published videos in the year 2022?':
    C8 = '''SELECT channel_name,COUNT(*)
    FROM youtube_channels.Video_datas
    WHERE YEAR(video_publishedat) = 2022
    GROUP BY YEAR(video_publishedat),channel_name'''
    mycursor.execute(C8)
    mydb.commit()
    E8=mycursor.fetchall()
    st.write(pd.DataFrame(E8,columns=["Channel Name","videos posted on 2022"],index=pd.RangeIndex(start=1,stop=len(E8)+1,name="S.no")))  



if Q=='What is the average duration of all videos in each channel, and what are their corresponding channel names?':
    C9 = '''SELECT channel_name,sec_to_time(AVG(video_duration))
    FROM youtube_channels.Video_datas
    GROUP BY channel_name ASC'''
    mycursor.execute(C9)
    mydb.commit()
    E9=mycursor.fetchall()
    st.write(pd.DataFrame(E9,columns=["Channel Name","Average duration"],index=pd.RangeIndex(start=1,stop=len(E9)+1,name="S.no")))     


if Q=='Which videos have the highest number of comments, and what are their corresponding channel names?':
    C10 = "SELECT SUM(video_commentscount),channel_name FROM youtube_channels.Video_datas GROUP BY channel_name order by video_commentscount desc"
    mycursor.execute(C10)
    mydb.commit()
    E10=mycursor.fetchall()
    st.write(pd.DataFrame(E10,columns=["Total comments","channel name"],index=pd.RangeIndex(start=1,stop=len(E10)+1,name="S.no")))































