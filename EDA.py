import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import re
import time

st.set_page_config(layout="wide")
def skillCorrection(skills):
    skills = str(skills).replace("\n", ",")
    skills = re.split(r',(?![^(]*\))', skills)
    skills = [re.sub(r'\(\d+\)', '', skill.strip()) for skill in skills]

    skills = {skill.upper().strip() for skill in skills}

    return ", ".join(skills)


def getLongitude(location):
    if location in ["Pune", 'Expleo Solutions Limited']:
        return 73.856255
    if location in ["Mumbai", 'Financial Software & Systems (P) Ltd']:
        return 72.877426
    if location in ["Bengaluru", 'BengaluruESL']:
        return 77.594566
    if location in ["Chennai", 'Chennai - MEPZ']:
        return 80.237617
    if location in ["Coimbatore"]:
        return 76.961632
    return 73.856255


def getLattitude(location):
    if location in ["Pune", 'Expleo Solutions Limited']:
        return 18.516726
    if location in ["Mumbai", 'Financial Software & Systems (P) Ltd']:
        return 19.076090
    if location in ["Bengaluru", 'BengaluruESL']:
        return 12.971599
    if location in ["Chennai", 'Chennai - MEPZ']:
        return 13.067439
    if location in ["Coimbatore"]:
        return 11.004556
    return 18.516726


st.write("""
 # Data Representation
""")

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    # Update the progress bar with each iteration.
    bar.progress(i + 1)
    time.sleep(0.1)

df = pd.read_excel("EDA.xlsx")
df['Primary Skill'].fillna("Generic", inplace=True)
df['Primary Skill'] = df['Primary Skill'].apply(str)
df['Primary Skill'] = df['Primary Skill'].str.replace("0", "Generic")
df['Primary Skill'] = df['Primary Skill'].apply(skillCorrection)
df['Primary Skill'] = df['Primary Skill'].str.strip(',')

# df['Primary Skill'] = df['Primary Skill'].str.split(',')
# # df_trial = df.explode('Primary Skill')

df['Remarks for Bench'].fillna("No Remarks", inplace=True)
df["NBD"].fillna(df["Actual NBD"], inplace=True)
df['Shared'].fillna("Not available", inplace=True)
df['Remarks from call'].fillna("No Remarks", inplace=True)
df['Vertical'].fillna("Not available", inplace=True)
df['Sub Vertical'].fillna("Not available", inplace=True)
df["Base Location"].fillna(df["Base Location"].mode()[0], inplace=True)
df["lat"] = df["Base Location"].apply(getLattitude)
df["lon"] = df["Base Location"].apply(getLongitude)
df['Resource Updated Status'] = df['Resource Updated Status'].apply(str.strip)
st.subheader("Data")
st.dataframe(df)
GCM_Grade_Data = df['GCM Grade'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(GCM_Grade_Data, labels=GCM_Grade_Data.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 5})
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.axis('equal')

st.subheader("Employee Count per GCM Grade")
st.pyplot(fig1)

skills_series = df['Primary Skill'].str.split(', ')
# skills_series
skills_list = [skill for sublist in skills_series for skill in sublist]
skill_counts = pd.Series(skills_list).value_counts()
# skill_counts = df_trial['Primary Skill'].apply(str).value_counts()
skill_counts_filtered = skill_counts[skill_counts > 1]
st.subheader("Skills")
st.bar_chart(skill_counts_filtered)

java_df = df[df['Primary Skill'].str.contains('Java', case=False)]
java_df = java_df[["Emp Code", 'Primary Skill', 'Resource Updated Status']]
st.subheader("List of Java Resources")
st.write(java_df)

ResourceStatus = df['Resource Updated Status'].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(ResourceStatus, labels=ResourceStatus.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 5})
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.axis('equal')
st.subheader("Resource Updated Status")
st.pyplot(fig2)

groupedByVertical = df.groupby(['Vertical', 'Resource Updated Status']).size().unstack(fill_value=0)
st.subheader("Vertical-wise Status of resource")
st.bar_chart(groupedByVertical)

groupedByReporting = df.groupby(['Reporting Manager', 'Resource Updated Status']).size().unstack(fill_value=0)
st.subheader("Reporting-wise Status of resource")
st.bar_chart(groupedByReporting)

groupByDigitalServices = df.groupby(['Digital Services', 'Resource Updated Status']).size().unstack(fill_value=0)
digital_services = df['Digital Services'].value_counts()
fig3, ax3 = plt.subplots()
ax3.pie(digital_services, labels=digital_services.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 5})
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax3.axis('equal')
left_column, right_column = st.columns(2)
left_column.subheader("Digital Services")
left_column.pyplot(fig3)

right_column.subheader("Digital Services-wise Status of resource")
right_column.bar_chart(groupByDigitalServices)

left_column.subheader("Locations")
left_column.map(df, latitude="lat", longitude="lon", color="#ffaa00")

groupByBaseLocation = df.groupby(['Base Location', 'Resource Updated Status']).size().unstack(fill_value=0)
right_column.subheader("Location-wise Status of resource")
right_column.bar_chart(groupByBaseLocation)
