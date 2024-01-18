# PhonePe-Data-Visualization-and-Exploration
This is an open-source project repo which deals with extracting data from PhonePe Pulse dataset available in [github](https://github.com/PhonePe/pulse/tree/master
), cleaning, transforming and loading it into MySQL database. Data visualization and exploration are done using Streamlit and Plotly charts or graphs.

## Introduction
PhonePe, India’s leading fintech platform, launched PhonePe Pulse, India’s first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse showcases more than 2000+ Crore transactions by consumers on an interactive map of India.   
This project aims at Extracting, Transforming and Loading data from [source repository](https://github.com/PhonePe/pulse/tree/master
) into MySQL and visualizing, exploring the data by creating a Streamlit application along with Plotly charts.   
Note : This project works on the data timelined between **2018 and 2023**.

## Table of Contents
1. Pre-requisites
2. Technology Stacks 
3. Usage
4. Data Extraction
5. Data Cleaning and Transformation
6. Migrating to MySQL
8. Visualization and Exploration
9. Further Improvements

## Pre-requsites
Install the following packages to run the project. 
```
pip install streamlit
pip install pandas
pip install os
pip install json
pip install mysql.connector
pip install plotly
pip install requests 
pip install plotly.express as px 
pip install PIL 


```

## Technology Stack
- Python scripting 
- SQL - MySQL
- Streamlit App development
- Github Data Extraction
- Plotly

## Usage
Clone the repo from the below mentioned link.  
[PhonePe-Data-Visualization-and-Exploration](https://github.com/Chindhu-Alagappan/PhonePe-Data-Visualization-and-Exploration.git)    
Install packages from "requirement.txt"  
Run the streamlit application using `streamlit run .\PhonePe.py`  
View the portal in your [localhost](http://localhost:8501/)    

## Data Extraction 
Clone the PhonePe Pulse data from the source repo and save it to your local.

Extract the following data as dataframe from the source directory.
- agg_trans_df - ./pulse/data/aggregated/transaction/country/india/state/
- agg_user_df - ./pulse/data/aggregated/user/country/india/state/

- map_trans_df - ./pulse/data/map/transaction/hover/country/india/state/
- map_user_df - ./pulse/data/map/user/hover/country/india/state/

- top_trans_df - ./pulse/data/top/transaction/country/india/state
- top_user_df - ./pulse/data/top/user/country/india/state

## Data Cleaning and Transformation
1. Convert the state names to title case
2. Replace '-' in state names to space
3. Find 'Andaman & Nicobar Islands' and replace with 'Andaman & Nicobar'
4. Load data to a CSV for reference

## Migrating to MySQL 
Connection must to be established between python and MySQL using sqlalchemy.create_engine(for creating tables directly from dfs) and mysql.connector package(for queries).   

## Visualization and Exploration
Data from these 6 tables are presented in a visually appealing form using plotly express plots, plotly choropleth charts. <br>
Also, streamlit's visualization functions help us understand the power of visualization by displaying these charts in a readily available format.

## Further Improvements 
The project can further be enhanced by plotting 3D charts and building models to predict the transaction and user details for the upcoming quarters. This will help us to better understand and organize the fintech platform and ensure to accomodate add servers to handle forthcoming demands.
If you encounter any issues or have suggestions for improvements, feel free to reach out.  
  
Email : *parthibantmn@gmail.com*  
LinkedIn : *https://www.linkedin.com/in/parthiban-t-09116725b/*
  
Thanks for showing interest in this repository ! 

