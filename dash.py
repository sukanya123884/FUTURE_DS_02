import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# preprocessed CSV
df = pd.read_csv("data.csv")
# Streamlit Page Config
st.set_page_config(page_title="Marketing Dashboard", layout="wide")
# Title
st.title("Marketing Campaign Dashboard")
# --- Sidebar Filter ---
st.sidebar.header("Filter")
country = st.sidebar.selectbox("Select Country", options=df["Country"].unique())
filtered_df = df[df["Country"] == country]
# --- KPI Section ---
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3 ,col4,col5= st.columns(5)
col1.metric("Avg. Web Visits:", round(filtered_df["NumWebVisitsMonth"].mean(), 1))
col2.metric("Avg. Store Visits:", round(filtered_df["NumStorePurchases"].mean(), 1))
col3.metric("Avg. Purchases on Deals:", round(filtered_df["NumDealsPurchases"].mean(), 1))
col4.metric("Avg. Spending:", round(filtered_df[["MntWines", "MntFruits", "MntGoldProds",
                                                     "MntFishProducts", "MntMeatProducts",
                                                     "MntSweetProducts"]].sum(axis=1).mean(), 2))
col5.metric('Customer Response rate:',round((filtered_df['Response'].sum()/len(filtered_df)),2)*100)
# --- Bar Chart: Spending Per Category ---
st.subheader(" Total Spend Per Product Category")

category_cols = ["MntWines", "MntFruits", "MntMeatProducts",
                 "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
spend_totals = filtered_df[category_cols].sum()

fig1, ax1 = plt.subplots()
colors = ['#FFC0CB', '#FFB6C1', '#DA70D6', '#D8BFD8', '#E6E6FA', '#BA55D3']
spend_totals.plot(kind="bar", ax=ax1, color=colors)
ax1.set_ylabel("Total Spend ")
ax1.set_xlabel("Product Category")
ax1.set_title("Category-wise Spending")
st.pyplot(fig1)
#Purchase by chanels bar charts 
fig2, ax = plt.subplots()
k={
   'Name':['NumDealsPurchases','NumWebPurchases','NumCatalogPurchases','NumStorePurchases','NumWebVisitsMonth'],
    'values':[filtered_df['NumDealsPurchases'].sum(),filtered_df['NumWebPurchases'].sum(),filtered_df['NumCatalogPurchases'].sum(),filtered_df['NumStorePurchases'].sum(),filtered_df['NumWebVisitsMonth'].sum()]
  }
df2=pd.DataFrame(k).set_index('Name')
df2.plot(
    kind='bar',
    ax=ax,
    title='Bar Chart showing total purchases by channel',
    color='Green'
)
ax.set_xlabel('Purchase Channel ->')
ax.set_ylabel('Frequency/counts ->')
st.pyplot(fig2)
#Pie Charts for Campaign Acceptance 
st.subheader(" Campaign Responses (Accepted)")
fig3=plt.figure(figsize=(17, 8))
plt.title('Comparisons Between All Campaigns',fontsize=16)
labels = ['No', 'Yes']
colors = ['#A64AC9', '#FFD93D']
for i in range(5):
    plt.subplot(1, 5, i + 1)
    k = 'AcceptedCmp' + str(i + 1)
    filtered_df[k].value_counts().sort_index().plot(
        kind='pie',
        labels=labels,
        colors=colors,
        startangle=90,
        autopct='%1.1f%%'
    )
    plt.title(k)
    plt.ylabel('') 
plt.gcf().legend(labels, loc='upper center', ncol=2, fontsize=12)
st.pyplot(fig3)
## Let's have a look to cutomers complain
fig4,ax = plt.subplots(figsize=(4, 4))
labels = ['Satisfied', 'Not Satisfied']
colors = ['red', 'yellow']
filtered_df['Complain'].value_counts().plot(
    kind='pie',
    colors=colors,
    labels=labels,
    ax=ax, 
    wedgeprops={'width': 0.4} ,
    autopct='%1.1f%%',
    startangle=90
)
ax.set_title('Customer Satisfaction Level')
ax.set_ylabel('') 
st.pyplot(fig4)
#Show filtered data
with st.expander("🔍 Show Filtered Data"):
    st.dataframe(filtered_df)


