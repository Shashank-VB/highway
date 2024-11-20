import streamlit as st
import requests
import time
import math
import pandas as pd
import os

# Title
st.title("Results")

# Input parameters
st.sidebar.title ("PSV Calculator")
st.sidebar.header ("Enter values:")
aadt_value = st.sidebar.number_input("enter AADT value:", min_value=0)
per_hgvs = st.sidebar.number_input("enter % of HGVs:")
year = st.sidebar.number_input("enter Year", min_value=0)
lanes = st.sidebar.number_input("enter number of Lanes", min_value=1)
pcvl = 0
lane1 = 0
lane2 = 0
lane3 = 0
lane4 = 0
lane_details_lane1 = 0
lane_details_lane2 = 0
lane_details_lane3 = 0
lane_details_lane4 = 0
def roundup(value):
	return math.ceil(value)


if year == 0 :
	design_period=0
	
elif year != 0 :
	design_period = ((20 + 2024) - year)
	

# Calculation
if per_hgvs >= 11 :
	result1 = per_hgvs
	AADT_HGVS = (result1*(aadt_value/100))

else:
        result2 = 11
        AADT_HGVS = ((result2*aadt_value)/100)


total_projected_aadt_hgvs = (AADT_HGVS * (1+1.54/100) ** design_period)
AADT_HGVS = round(AADT_HGVS)
total_projected_aadt_hgvs = round(total_projected_aadt_hgvs)


st.subheader("Generic")
# Generic Results
st.write("AADT_HGVS:", AADT_HGVS)
st.write("Design Period in years", design_period)
st.write("Total Projected AADT HGVs", total_projected_aadt_hgvs)

#percentage of commercial vehicles in each lane
if lanes == 1 :
	lane1 = 100
	lane_details_lane1 = total_projected_aadt_hgvs
elif lanes > 1 and lanes <= 3 :
	if  total_projected_aadt_hgvs < 5000 : 
		lane1 = round(100-(0.0036*total_projected_aadt_hgvs))
		lane2 = round(100-(100-(0.0036*total_projected_aadt_hgvs)))
	elif total_projected_aadt_hgvs >= 5000 and total_projected_aadt_hgvs < 25000 : 
		lane1 = round(89-(0.0014*total_projected_aadt_hgvs))
		lane2= round(100-lane1)
	elif total_projected_aadt_hgvs >= 25000 : 
		lane1 =  54
		lane2 = 100-54
		lane3 = 0
	lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1/100))
	lane_details_lane2 = round(total_projected_aadt_hgvs * (lane2/100))

elif lanes >= 4 : 
	if  total_projected_aadt_hgvs <= 10500 : 
		lane1 = round(100-(0.0036*total_projected_aadt_hgvs))
		lane_2_3 = (total_projected_aadt_hgvs-((total_projected_aadt_hgvs*lane1)/100))
		lane2 = round(89-(0.0014*lane_2_3))
		lane3 = 100-lane2
		lane4 = 0
	elif total_projected_aadt_hgvs > 10500 and total_projected_aadt_hgvs < 25000 : 
		lane1 = round(75-(0.0012*total_projected_aadt_hgvs))
		lane_2_3 = (total_projected_aadt_hgvs-((total_projected_aadt_hgvs*lane1)/100))
		lane2 = round(89-(0.0014*lane_2_3))
		lane3 = 100-lane2
		lane4 = 0
	elif total_projected_aadt_hgvs >= 25000 : 
		lane1 =  45
		lane2 = 54
		lane3 = 100-54	
	lane_details_lane1 = round(total_projected_aadt_hgvs * (lane1/100))
	lane_details_lane2 = round((total_projected_aadt_hgvs - lane_details_lane1) * (lane2/100))
	lane_details_lane3 = round(total_projected_aadt_hgvs - (lane_details_lane1+lane_details_lane2))

st.subheader("Percentage of CV's in each lane")
st.write("Lane1:", lane1)
st.write("Lane2:", lane2)
st.write("Lane3:", lane3)
st.write("Lane4:", lane4)

#Design Traffic
st.subheader("Design Traffic")
st.write("Lane Details Lane1:", lane_details_lane1)
st.write("Lane Details Lane2:", lane_details_lane2)
st.write("Lane Details Lane3:", lane_details_lane3)
st.write("Lane Details Lane4:", lane_details_lane4)

#Excel to  Data frame
st.sidebar.header("Upload CD 236 excel file with table")

# Add a file uploader widget
uploaded_file = st.sidebar.file_uploader("Upload your Excel file:", type=["xlsx"])

#PSV Final
value1 = st.sidebar.text_input("enter Site Category:")
value2 = st.sidebar.number_input("enter IL value:")
value3 = lane_details_lane1
value4 = lane_details_lane2
value5 = lane_details_lane3

st.subheader("PSV Values at each lane")
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Display the DataFrame
    #st.write("Uploaded Table")
    #st.write(df)
    
    # Add a "Search" button
    if st.sidebar.button("Search"):
        # For LANE-1
        range_column = None
        for col in df.columns:
            if '-' in col:
                col_range = list(map(int, col.split('-')))
                if col_range[0] <= value3 <= col_range[1]:
                    range_column = col
                    break
        if range_column:
            # Filter the DataFrame based on input values
            filtered_df = df[(df['SiteCategory'] == value1) & (df['IL'] == value2)]
            if not filtered_df.empty:
                result = filtered_df.iloc[0][range_column]
            else:
                result = "No matching result found."
        else:
            result = "No matching range found for the given value."

        # Display the filtered result in Streamlit
        st.write(f"PSV at Lane1: {result}")
        
        # For LANE-2
        if value4 == 0:
                st.write(f"Lane2:0")
        else: 
                range_column = None
                for col in df.columns:
                        if '-' in col:
                                col_range = list(map(int, col.split('-')))
                                if col_range[0] <= value4 <= col_range[1]:
                                        range_column = col
                                        break
                if range_column:
                        # Filter the DataFrame based on input values
                        filtered_df = df[(df['SiteCategory'] == value1) & (df['IL'] == value2)]
                        if not filtered_df.empty:
                                result2 = filtered_df.iloc[0][range_column]
                        else:
                                result2 = "No matching result found."
                else:
                        result = "No matching range found for the given value."
			
                st.write(f"PSV at Lane2: {result2}")

        # For LANE-3
        if value5 == 0:
                st.write(f"Lane3:0")
        else: 
                range_column = None
                for col in df.columns:
                        if '-' in col:
                                col_range = list(map(int, col.split('-')))
                                if col_range[0] <= value5 <= col_range[1]:
                                        range_column = col
                                        break
                if range_column:
                        # Filter the DataFrame based on input values
                        filtered_df = df[(df['SiteCategory'] == value1) & (df['IL'] == value2)]
                        if not filtered_df.empty:
                                result3 = filtered_df.iloc[0][range_column]
                        else:
                                result3 = "No matching result found."
                else:
                        result = "No matching range found for the given value."
                st.write(f"PSV at Lane3: {result3}")
