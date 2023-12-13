# BizCardX-Extracting-Business-Card-Data-with-OCR
# Introduction
BizCardX is a Streamlit-Python application that automates the extraction of important details from business cards using Optical Character Recognition (OCR) technology. It utilizes the EasyOCR library to accurately extract text from uploaded business card images. The extracted data can then be viewed, edited, or deleted within the application. BizCardX also allows users to save the extracted information and the uploaded image into a database capable of storing multiple entries.
# Key Concepts
**EasyOCR:** EasyOCR is a Python library that provides a simple interface for performing OCR tasks. It supports multiple languages and can accurately extract text from various types of images, including business cards.

**Streamlit:** Streamlit is a Python library that allows developers to create interactive web applications with ease. It provides a user-friendly interface for users to interact with the application and view the extracted data.

**MySQL Connector:** MySQL Connector Python library that enables Python programs to connect and interact with MySQL databases. It is used in BizCardX to establish a connection with the database and perform database operations.

# Code Structure

**Importing Libraries:** The necessary libraries for the application are imported, including pandas, streamlit, easyocr, mysql.connector, numpy and os.

**Setting Page Configurations:** The page configurations for the Streamlit application are set, including the page title, icon, and layout. The background style of the application is set using CSS to create a visually appealing user interface.The home menu is displayed using the Streamlit tabs feature. It provides an overview of the BizCardX application and its functionalities

**Database Connection and Table Creation:** The code establishes a connection with the MySQL database and creates a table. This table is used to store the extracted business card data.

**Upload and Extract Menu:** The menu allows users to upload a business card image and extract relevant information from it using OCR. The uploaded image is processed, and the extracted data is displayed in a table format. Users can choose to upload the extracted data to the database.

**Modify Menu:** In this menu, users can update or modify the extracted data for a specific business card. The updated data is then saved to the database.

**Delete Menu:** This menu allows users to select a business card and delete it from the database. The selected card's details are displayed, including the image, and users can confirm the deletion.

# Conclusion
BizCardX is a powerful Python application that simplifies the process of extracting business card information. By leveraging OCR technology and a user-friendly interface, BizCardX allows users to easily upload business card images, extract relevant data, and store it in a database. With its intuitive design and advanced features, BizCardX streamlines the management of business card information, making it an essential tool for professionals and businesses.
