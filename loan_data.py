import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import plotly.graph_objs as go


st.set_page_config(layout="wide")
st.title("Loan Data Analysis")
data = pd.read_csv("./loan_data.csv")

data["Gender"] = data["Gender"].fillna("Unknown")
data["Married"] = data["Married"].fillna(data["Married"].mode()[0])
data["Dependents"] = data["Dependents"].fillna(data["Dependents"].mode()[0])
data["Self_Employed"] = data["Self_Employed"].fillna(data["Self_Employed"].mode([0]))
data["LoanAmount"] = data["LoanAmount"].fillna(data["LoanAmount"].mean())
data["Loan_Amount_Term"] = data["Loan_Amount_Term"].fillna(data["Loan_Amount_Term"].mode()[0])
data["Credit_History"] = data["Credit_History"].fillna(data["Credit_History"].mode()[0])
data["TotalIncome"] = data["ApplicantIncome"] + data["CoapplicantIncome"]

GenderWiseGrouped = data.groupby('Gender').size()
Average_Loan_Amount_by_Marital_Status_and_Credit_History = data.groupby(['Credit_History','Education'])['LoanAmount'].mean().unstack()
Educationwise_LoanStatus = data.groupby(["Education", "Loan_Status"]).size().unstack()
Areawise_LoanStatus = data.groupby([ "Loan_Status","Property_Area"]).size().unstack()
CreditScorewise_LoanStatus = data.groupby(["Credit_History", "Loan_Status"]).size().unstack()
correlation_matrix = data[["ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "TotalIncome"]].corr()
# Create a cross-tabulation of Loan_Status and Gender
cross_tabGenderVsStatus = pd.crosstab(data['Gender'], data['Loan_Status'])
cross_tabEducationVsStatus = pd.crosstab(data['Education'], data['Loan_Status'])

st.subheader("Loan Data")
st.dataframe(data)

st.subheader("Correlation Matrix")
heatMap = sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
st.pyplot(heatMap.get_figure())

left_column, right_column = st.columns(2)

with left_column:

    st.subheader("Histograms")

    lcolor_option = st.selectbox(
        "Color columns For Histograms:",
        ("Education", "Gender", "Loan_Status", "Self_Employed", "Property_Area", "Married", None))
    
    
    ApplicantsIncomeHist = px.histogram(data, x="ApplicantIncome", nbins=30, hover_data=data.columns, color=lcolor_option)
    CoapplicantsIncomeHist = px.histogram(data, x="CoapplicantIncome", nbins=30, hover_data=data.columns, color=lcolor_option)
    LoanAmountHist = px.histogram(data, x="LoanAmount", nbins=30, hover_data=data.columns, color=lcolor_option)
    Loan_Amount_Term_Hist = px.histogram(data, x="Loan_Amount_Term", nbins=30, hover_data=data.columns, color=lcolor_option)


    ltab1, ltab2, ltab3, ltab4 = st.tabs(["Applicant's income", "Co-applicant's income", "Loan Amount", "Term Amount"])

    with ltab1:

        st.plotly_chart(ApplicantsIncomeHist, theme="streamlit", use_container_width=True)
    with ltab2:

        st.plotly_chart(CoapplicantsIncomeHist, theme="streamlit", use_container_width=True)
    with ltab3:

        st.plotly_chart(LoanAmountHist, theme="streamlit", use_container_width=True)
    with ltab4:

        st.plotly_chart(LoanAmountHist, theme="streamlit", use_container_width=True)


# ApplicantsIncomeBox = px.box(data, x=)





with right_column:
    st.subheader("BoxPlots")
    rcolor_option = st.selectbox(
        "Color columns For Box Plots:",
        ("Education", "Gender", "Loan_Status", "Self_Employed", "Property_Area", "Married", None))

    rtab1, rtab2, rtab3, rtab4  = st.tabs(["Applicant's income", "Co-applicant's income", "Loan Amount", "Term Amount"])

    ApplicantsIncomeBoxplot = px.box(data, x="ApplicantIncome", hover_data=data.columns, color=rcolor_option)
    CoapplicantsIncomeBoxplot = px.box(data, x="CoapplicantIncome", hover_data=data.columns, color=rcolor_option)
    LoanAmountBoxplot = px.box(data, x="LoanAmount", hover_data=data.columns, color=rcolor_option)
    Loan_Amount_Term_Boxplot = px.box(data, x="Loan_Amount_Term", hover_data=data.columns, color=rcolor_option)

    with rtab1:

        st.plotly_chart(ApplicantsIncomeBoxplot, theme="streamlit", use_container_width=True)
    with rtab2:

        st.plotly_chart(CoapplicantsIncomeBoxplot, theme="streamlit", use_container_width=True)
    with rtab3:

        st.plotly_chart(LoanAmountBoxplot, theme="streamlit", use_container_width=True)
    with rtab4:

        st.plotly_chart(Loan_Amount_Term_Boxplot, theme="streamlit", use_container_width=True)







st.subheader("Applicant's Income to Loan Ammount")

color_option_for_scatter = st.selectbox(
"Color columns For Scatter Plots:",
("Education", "Gender", "Loan_Status", "Self_Employed", "Property_Area", "Married", "Credit_History", None))
ApplicantsIncomeToLoanAmount = px.scatter(data, x="TotalIncome", y="LoanAmount", color=color_option_for_scatter, color_discrete_sequence=["orange", "blue", "lightblue","red", "green"], hover_data=data.columns)
st.plotly_chart(ApplicantsIncomeToLoanAmount)

st.subheader("Average Loan Amount by Education and Credit History")
Average_Loan_Amount_by_Marital_Status_and_Credit_HistoryBar = px.bar(Average_Loan_Amount_by_Marital_Status_and_Credit_History, barmode="group")

st.plotly_chart(Average_Loan_Amount_by_Marital_Status_and_Credit_HistoryBar)



# Average_Loan_Amount_by_TotalIncome_and_Credit_History = data.groupby(['Credit_History','TotalIncome'])['LoanAmount'].mean().unstack()
# Average_Loan_Amount_by_TotalIncome_and_Credit_HistoryBar = px.bar(Average_Loan_Amount_by_TotalIncome_and_Credit_History, barmode="group")
Average_Loan_Amount_by_TotalIncome_and_Credit_HistoryBar = px.bar(data, x="Loan_Status", y="LoanAmount", color="Property_Area")

st.plotly_chart(Average_Loan_Amount_by_TotalIncome_and_Credit_HistoryBar)



st.subheader("Property Area Vs LoanStatus")
Areawise_LoanStatus = px.bar(Areawise_LoanStatus, color_discrete_sequence=["blue", "red", "green"])
st.plotly_chart(Areawise_LoanStatus)

st.subheader("Education Vs LoanStatus")
Educationwise_LoanStatus = px.bar(Educationwise_LoanStatus, color_discrete_sequence=["blue", "red", "green"])
st.plotly_chart(Educationwise_LoanStatus)


st.subheader("Credit Score Vs LoanStatus")
CreditScorewise_LoanStatusBar = px.bar(CreditScorewise_LoanStatus, color_discrete_sequence=["blue", "red", "green"])
st.plotly_chart(CreditScorewise_LoanStatusBar)


left_Scolumn, right_Scolumn = st.columns(2)

with left_Scolumn:

    approved_bar = go.Bar(x=cross_tabEducationVsStatus.index, y=cross_tabEducationVsStatus['Y'], name='Approved')
    rejected_bar = go.Bar(x=cross_tabEducationVsStatus.index, y=cross_tabEducationVsStatus['N'], name='Rejected')


    layout = go.Layout(title='Loan Status by Education', 
                    xaxis=dict(title='Education'), 
                    yaxis=dict(title='Count'))

    fig = go.Figure(data=[approved_bar, rejected_bar], layout=layout)
    # fig = px.bar(x=data["Loan_Status"], color=data["Education"], color_discrete_sequence=["blue", "red", "green"], hover_data=cross_tabEducationVsStatus.columns)
    st.subheader("Loan Status by Education")
    st.plotly_chart(fig)

with right_Scolumn:
    approved_bar = go.Bar(x=cross_tabGenderVsStatus.index, y=cross_tabGenderVsStatus['Y'], name='Approved')
    rejected_bar = go.Bar(x=cross_tabGenderVsStatus.index, y=cross_tabGenderVsStatus['N'], name='Rejected')


    layout = go.Layout(title='Loan Status by Gender', 
                    xaxis=dict(title='Gender'), 
                    yaxis=dict(title='Count'))

    fig = go.Figure(data=[approved_bar, rejected_bar], layout=layout)
    st.subheader("Loan Status by Gender")
    st.plotly_chart(fig)