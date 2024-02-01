import pandas as pd # Pandas library
import streamlit as st # To access streamlit
from streamlit_option_menu import option_menu
import easyocr # EasyOCR to decode the image

# To Access SQL connection
import mysql
import mysql.connector as sql

from PIL import Image # To read image.
import cv2 # OpenCV library - add text to an image.
import os # To access the local system.
import matplotlib.pyplot as plt # To plot image.
import re # Regular expression for formatting.


# SETTING PAGE CONFIGURATIONS
img_path=r"C:\Users\Hp\Documents\project\Projects\DataSets\Creative Modern Business Card\1.png"
icon = Image.open(img_path.replace("\\", "/"))
st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR",
                   page_icon= icon,
                   layout="wide",
                   initial_sidebar_state="expanded")
st.markdown("<h1 style='text-align: center; color: white;'>BizCardX: Extracting Business Card Data with OCR</h1>",
            unsafe_allow_html=True)

# SETTING-UP BACKGROUND IMAGE
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background:url("https://images.hdqwalls.com/download/corner-strip-simple-graphics-1358x764.jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)

setting_bg()

with st.sidebar:
        st.header(":green[About]")
        
        st.write("## BizcardX is a Python application designed to extract information from business cards.")
        st.header(":green[**Scope**]")
        st.write('## The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
        st.markdown("## :green[**Technologies Used :**] Python,EasyOCR, Streamlit, SQL, Pandas")



# CREATING OPTION MENU
selected = option_menu(None, ["Upload & Extract","Modify"],
                       icons=["cloud-upload","pencil-square"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"nav-link": {"font-size": "15px", 
                                            "text-align": "centre",
                                            "margin": "-5px",
                                            "--hover-color": "#F5B05F",
                                            "color": "#FFFFFF"},
                                            "icon": {"font-size": "15px"},
                                            "container" : {"max-width": "6000px"},
                                            "nav-link-selected": {"background-color": "#854E35"}})

# INITIALIZING THE EasyOCR READER(english)
reader = easyocr.Reader(['en'])

#sql connection
mydb = mysql.connector.connect(host="localhost",
                            user="root",
                            password="",
                            database='BizcardX'
                            )
mycursor = mydb.cursor(buffered=True)


# TABLE CREATION
mycursor.execute('''CREATE TABLE IF NOT EXISTS BizcardX.card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT UNIQUE,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# UPLOAD AND EXTRACT MENU

if selected == "Upload & Extract":

    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:
        def save_card(uploaded_card):
            uploaded_cards_dir = os.path.join(os.getcwd(), "DataSets\\Creative Modern Business Card")
            with open(os.path.join(uploaded_cards_dir, uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())

        save_card(uploaded_card)

        def image_preview(image, res):
            #bbox-bounding box,text-text identified by ocr,prob-probability(0-1)
            for (bbox, text, prob) in res:

                # unpack the bounding box
                #tl=TopLeft, tr=TopRight, br=BottomRight, bl=BottomLeft
                (tl, tr, br, bl) = bbox

                #making tuple
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))

                cv2.rectangle(image, tl, br, (0,255,0), 2)
            plt.rcParams['figure.figsize'] = (20, 20)
            plt.axis('off')#To turn Off the axis in the plot
            plt.imshow(image)

        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.info("### Your card has been uploaded successfully")
            st.image(uploaded_card)
        
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "DataSets\\Creative Modern Business Card" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("### Text identified in the card")
                st.pyplot(image_preview(image, res))

        # easy OCR
        saved_img = os.getcwd() + "\\" + "DataSets\\Creative Modern Business Card" + "\\" + uploaded_card.name
        result = reader.readtext(saved_img, detail=0, paragraph=False)

        # CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
        def img_to_binary(file):
            # Convert image data to binary format
            with open(file, 'rb') as file:
                binaryData = file.read()
            return binaryData


        data = {"company_name": [],
                "card_holder": [],
                "designation": [],
                "mobile_number": [],
                "email": [],
                "website": [],
                "area": [],
                "city": [],
                "state": [],
                "pin_code": [],
                "image": img_to_binary(saved_img)
                }
        
        def get_data(res):
            for ind, i in enumerate(res):

                # To get WEBSITE_URL
                if "www " in i.lower() or "www." in i.lower():
                    data["website"].append(i)
                elif "WWW" in i:
                    data["website"] = res[4] + "." + res[5]

                # To get EMAIL ID
                elif "@" in i:
                    data["email"].append(i)

                # To get MOBILE NUMBER
                elif "-" in i:
                    data["mobile_number"].append(i)
                    if len(data["mobile_number"]) == 2:
                        data["mobile_number"] = " & ".join(data["mobile_number"])

                # To get COMPANY NAME
                elif ind == len(res) - 1:
                    data["company_name"].append(i)

                # To get CARD HOLDER NAME
                elif ind == 0:
                    data["card_holder"].append(i)

                # To get DESIGNATION
                elif ind == 1:
                    data["designation"].append(i)

                # To get AREA
                if re.findall('^[0-9].+, [a-zA-Z]+', i):
                    data["area"].append(i.split(',')[0])
                elif re.findall('[0-9] [a-zA-Z]+', i):
                    data["area"].append(i)

                # To get CITY NAME
                match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
                match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
                match3 = re.findall('^[E].*', i)
                if match1:
                    data["city"].append(match1[0])
                elif match2:
                    data["city"].append(match2[0])
                elif match3:
                    data["city"].append(match3[0])

                # To get STATE
                state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
                if state_match:
                    data["state"].append(i[:9])
                elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
                    data["state"].append(i.split()[-1])
                if len(data["state"]) == 2:
                    data["state"].pop(0)

                # To get PINCODE
                if len(i) >= 6 and i.isdigit():
                    data["pin_code"].append(i)
                elif re.findall('[a-zA-Z]{9} +[0-9]', i):
                    data["pin_code"].append(i[10:])
        get_data(result)

        # FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df


        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            try:
                for i, row in df.iterrows():
                    # here %S means string values
                    sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    mycursor.execute(sql, tuple(row))
                    # the connection is not auto committed by default, so we must commit to save our changes
                    mydb.commit()
                    st.success("#### Uploaded to database successfully!")
            except:
                st.error("Data already exists.Try again with another one...")


        if st.button(":blue[View Uploaded Data]"):
            mycursor.execute("select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
            updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Area", "City", "State", "Pin_Code"])
            st.write(updated_df)

# MODIFY MENU
if selected == "Modify":
    
    select = option_menu(None,
                         options=["ALTER", "DELETE"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#6495ED"}})

    if select == "ALTER":
        try:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.markdown("#### Update or modify any data below")
                mycursor.execute(
                '''select company_name,
                        card_holder,
                        designation,
                        mobile_number,
                        email,
                        website,
                        area,
                        city,
                        state,
                        pin_code from card_data 
                        WHERE card_holder=%s''',(selected_card,))
                result = mycursor.fetchone()

                # DISPLAYING ALL THE INFORMATIONS
                company_name = st.text_input("Company_Name", result[0])
                card_holder = st.text_input("Card_Holder", result[1])
                designation = st.text_input("Designation", result[2])
                mobile_number = st.text_input("Mobile_Number", result[3])
                email = st.text_input("Email", result[4])
                website = st.text_input("Website", result[5])
                area = st.text_input("Area", result[6])
                city = st.text_input("City", result[7])
                state = st.text_input("State", result[8])
                pin_code = st.text_input("Pin_Code", result[9])


                if st.button(":blue[Modify]"):


                   # Update the information for the selected business card in the database
                    mycursor.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,
                                     mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""",(company_name,card_holder,designation, mobile_number, email,
                                                          website, area, city, state, pin_code,selected_card))
                    mydb.commit()
                    st.info("Information updated.")

            if st.button(":blue[View updated data]"):
                mycursor.execute(
                    '''select company_name,card_holder,designation,mobile_number,email,website,area,city,state,
                            pin_code from card_data''')
                
                updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                   "Email","Website", "Area", "City", "State", "Pin_Code"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")

    if select == "DELETE":
        st.subheader(":blue[Delete the data]")
        try:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            options = ["None"] + list(business_cards.keys())
            selected_card = st.selectbox("**Select a card**", options)
            if selected_card == "None":
                st.write("No card selected.")
            else:
                st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
                st.write("#### Proceed to delete this card?")
                if st.button("Confirm"):
                    mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
                    mydb.commit()
                    st.info("Information deleted.")

            if st.button(":blue[View updated data]"):
                mycursor.execute(
                    "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
                updated_df = pd.DataFrame(mycursor.fetchall(),
                                          columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number",
                                                   "Email",
                                                   "Website", "Area", "City", "State", "Pin_Code"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")
