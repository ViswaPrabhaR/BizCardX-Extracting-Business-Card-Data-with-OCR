# Libraries
import pandas as pd
import streamlit as st

import easyocr
import mysql.connector as sql

import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# SETTING PAGE CONFIGURATIONS

st.set_page_config(page_title="BizCardX: Extracting Business Card Data with OCR ", page_icon='🖼️',
                   layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align: left; margin-top: -100px; font-size:30px; color: black;'>BizCardX: Extracting Business "
    "Card Data with OCR</h1>",
    unsafe_allow_html=True)


def setting_bg():
    st.markdown(f""" <style>.stApp {{     
                        margin: 10px 10px 10px 120px;
                        border-radius: 5px;
                        background-color: white;
                        box-shadow: 5px 5px 5px 5px #aaaaaa;
                         width:1000px;
                        background-position:center;}}
                     </style>""", unsafe_allow_html=True)


setting_bg()
st.markdown("""
<style>
.stTabs{
    margin-top:-50px
}
.stTabs [data-baseweb="tab-list"] {
    background-color:#391C59;
    padding: 5px 0px 5px 5px;
    border-radius: 10px;
}
.stTabs [data-baseweb="tab"] {
    width: 200px;
    border-radius: 5px;
    color: #FFFFFF;         
    height: 40px;
    margin: 0px 10px 0px 10px;
}
.stTabs [aria-selected="true"] {
  	background-color: #FFFFFF;
    color:#391C59;	
}
div.stButton > button:first-child {
    background-color: #FFFFFF;
    border-color:#391C59;
}
div.stButton > button:hover {
    background-color: #391C59;
    color:#ffffff;
}
.stSelectbox [data-baseweb="select"] > div {
    background-color: white;
     color:#391C59; border-color: #2d408d;        
 }
 .stText [data-baseweb="select"] > div {
    background-color: white;
     color:#391C59; border-color: #2d408d;        
 }</style>""", unsafe_allow_html=True)

# Option Menu
tab1, tab2, tab3, tab4 = st.tabs(["🌏 Home ", " 📊 Image Extract", " 📝 Data Modify", " 📇 Delete Record"])

# EasyOCR Reader
reader = easyocr.Reader(['en'])
# Database Connection
mydb = sql.connect(host="localhost",
                   user="root",
                   password="admin123",
                   database="business_card"
                   )
mycursor = mydb.cursor(buffered=True)

# Database Create Table
mycursor.execute('''CREATE TABLE IF NOT EXISTS card_data
                   (id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    company_name TEXT,
                    card_holder TEXT,
                    designation TEXT,
                    mobile_number VARCHAR(50),
                    email TEXT,
                    website TEXT,
                    area TEXT,
                    city TEXT,
                    state TEXT,
                    pin_code VARCHAR(10),
                    image LONGBLOB
                    )''')

# HOME MENU
with tab1:
    col1, col2 = st.columns([1, 2])
    with col2:
        st.markdown("### Welcome to the Business Card Application!")
        st.markdown(
            '#####  Bizcard is a Python application that automates the extraction of important details from business '
            'cards.It uses Optical Character Recognition (OCR) from EasyOCR to accurately extract text from uploaded '
            'images.')
        st.write(
            '##### :red[**Technologies Used :**] The application, built with Python, EasyOCR, Streamlit, SQL, '
            'and Pandas')
    st.markdown(
        '##### It allows users to upload a business card image and extract relevant information. Users can then view, '
        'edit, or delete the extracted data within the app.The app also enables users to save the extracted '
        'information and the uploaded image into a database capable of storing multiple entries.')
    st.markdown(
        '##### Overall: Bizcard simplifies the process of extracting business card information through a '
        'user-friendly interface and advanced technologies.')
    with col1:
        st.image("home.png")

# UPLOAD AND EXTRACT MENU
with tab2:
    st.markdown("### Upload a Business Card")
    uploaded_card = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])

    if uploaded_card is not None:
        # SAVE THE CARD IN uploaded_cards FOLDER
        def save_card(uploaded_card):
            with open(os.path.join("uploaded_cards", uploaded_card.name), "wb") as f:
                f.write(uploaded_card.getbuffer())


        save_card(uploaded_card)


        # IMAGE PROCESSING OF THE UPLOADED CARD
        def image_preview(image, res):
            for (bbox, text, prob) in res:
                # unpack the bounding box
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))
                cv2.rectangle(image, tl, br, (0, 255, 0), 2)
                cv2.putText(image, text, (tl[0], tl[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            plt.rcParams['figure.figsize'] = (15, 15)
            plt.axis('off')
            plt.imshow(image)


        # DISPLAYING THE UPLOADED CARD
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.markdown("#     ")
            st.markdown("#     ")
            st.markdown("#### Your Uploaded Card")
            st.image(uploaded_card)
        # DISPLAYING THE CARD WITH HIGHLIGHTS
        with col2:
            st.markdown("#     ")
            st.markdown("#     ")
            with st.spinner("Please wait processing image..."):
                st.set_option('deprecation.showPyplotGlobalUse', False)
                saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
                image = cv2.imread(saved_img)
                res = reader.readtext(saved_img)
                st.markdown("#### Image Processed and Data Extracted")
                st.pyplot(image_preview(image, res))

                # easy OCR
        saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + uploaded_card.name
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
        st.write(f"{data}")
        res = not any(data.values())

        # printing result
        st.write(f"Are value lists empty? :  { str(res)}")
        # FUNCTION TO CREATE DATAFRAME
        def create_df(data):
            df = pd.DataFrame(data)
            return df
        df = create_df(data)
        st.success("### Data Extracted!")
        st.write(df)

        if st.button("Upload to Database"):
            for i, row in df.iterrows():
                # here %S means string values
                sql = """INSERT INTO card_data(company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image)
                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                mycursor.execute(sql, tuple(row))
                # the connection is not auto committed by default, so we must commit to save our changes
                mydb.commit()
            st.success("#### Uploaded to database successfully!", icon='✅')

# MODIFY MENU    
with tab3:
    st.markdown("## Alter the data here")
    column1, column2 = st.columns([4, 1])
    try:
        with column1:
            mycursor.execute("SELECT card_holder FROM card_data")
            result = mycursor.fetchall()
            business_cards = {}
            for row in result:
                business_cards[row[0]] = row[0]
            selected_card = st.selectbox("Select a card holder name to update", list(business_cards.keys()))
            st.markdown("#### Update or modify any data below")
            mycursor.execute(
                "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data WHERE card_holder=%s",
                (selected_card,))
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

            if st.button("Commit changes to DB"):
                # Update the information for the selected business card in the database
                mycursor.execute("""UPDATE card_data SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email=%s,website=%s,area=%s,city=%s,state=%s,pin_code=%s
                                    WHERE card_holder=%s""", (
                    company_name, card_holder, designation, mobile_number, email, website, area, city, state, pin_code,
                    selected_card))
                mydb.commit()
                st.success("Information updated in database successfully.", icon='✅')
    except:
        st.warning("There is no data available in the database")

    if st.button("View updated data"):
        mycursor.execute(
            "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code from card_data")
        updated_df = pd.DataFrame(mycursor.fetchall(),
                                  columns=["Company_Name", "Card_Holder", "Designation", "Mobile_Number", "Email",
                                           "Website", "Area", "City", "State", "Pin_Code"])
        st.write(updated_df)
with tab4:
    mycursor.execute("SELECT card_holder FROM card_data")
    result = mycursor.fetchall()
    business_cards = {}
    for row in result:
        business_cards[row[0]] = row[0]
    selected_card = st.selectbox("Select a card holder name to Delete", list(business_cards.keys()))
    st.write(f"### You have selected :green[**{selected_card}'s**] card to delete")
    with st.container(border=True):
        mycursor.execute(
            "select company_name,card_holder,designation,mobile_number,email,website,area,city,state,pin_code,image from card_data WHERE card_holder=%s",
            (selected_card,))
        result = mycursor.fetchone()
        details, address, image = st.columns([3, 2, 4])
        # DISPLAYING ALL THE INFORMATIONS
        with details:
            company_name = st.write("**Company_Name  :**", result[0])
            card_holder = st.write("**Card_Holder   :**", result[1])
            designation = st.write("**Designation   :**", result[2])
            mobile_number = st.write("**Mobile_Number :**", result[3])
            email = st.write("**Email :**", result[4])
            website = st.write("**Website :**", result[5])
        with address:
            st.write("**Address**")
            area = st.write(" ", result[6])
            city = st.write(" ", result[7])
            state = st.write(" ", result[8])
            pin_code = st.write(" ", result[9])
        with image:
            image_data = result[10]
            # Create a file-like object from the image data
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            st.image(image, channels="BGR", use_column_width=True)

    st.write("#### Proceed to delete this card?")
    if st.button("Yes, Delete this Business Card"):
        mycursor.execute(f"DELETE FROM card_data WHERE card_holder='{selected_card}'")
        mydb.commit()
        st.success("Successfully Business card deleted from database.", icon='✅')
