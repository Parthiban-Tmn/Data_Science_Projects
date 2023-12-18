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

