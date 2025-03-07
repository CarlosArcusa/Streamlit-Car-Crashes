import seaborn as sns
import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

gsheet_url = st.secrets["connections"]["gsheet_url"]

# Function to fetch data from Google Sheets
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(gsheet_url)
    return df

# Load dataset from Google Sheets
df = load_data()

st.title('Streamlit App: Car Crashes Analysis')
st.subheader('Data Visualization')

#Question visible to the user
st.write("Which U.S. states have the least safest drivers based on alcohol-related crashes?")

if 'chart_selected' not in st.session_state:
    st.session_state.chart_selected = False
if 'selected_chart' not in st.session_state:
    st.session_state.selected_chart = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

def chart_a():
    df["alcohol_pct"] = (df["alcohol"] / df["total"]) * 100  # Calculate percentage

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="alcohol_pct", y="total", hue="alcohol_pct", size="alcohol_pct", sizes=(20, 200), palette="coolwarm", ax=ax)

    for i in range(len(df)):
        ax.text(df["alcohol_pct"][i], df["total"][i], df["abbrev"][i], fontsize=9, ha='right')

    ax.set_xlabel("Alcohol-Related Accidents (%)")
    ax.set_ylabel("Total Car Crashes")
    ax.set_title("Chart A: % of Alcohol-Related Accidents vs. Total Crashes")
    st.pyplot(fig)

def chart_b():
    df["alcohol_pct"] = (df["alcohol"] / df["total"]) * 100  # Ensure percentage calculation

    df_sorted = df.sort_values(by="alcohol_pct", ascending=False).head(10)  # Sort by alcohol percentage

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_sorted, x="alcohol_pct", y="abbrev", palette="coolwarm", ax=ax)

    ax.set_xlabel("Alcohol-Related Accidents (%)")  # Update label to match the correct metric
    ax.set_ylabel("State")
    ax.set_title("Chart B: Top States with Most Alcohol-Related Accidents (%)")
    st.pyplot(fig)

if st.button("Show Chart"):
    st.session_state.chart_selected = True
    st.session_state.start_time = time.time()
    st.session_state.selected_chart = random.choice(["A", "B"])
    
    if st.session_state.selected_chart == "A":
        chart_a()
    
    if st.session_state.selected_chart == "B":
        chart_b()

if st.session_state.chart_selected:  
    if st.button("I answered the question"):
        st.session_state.end_time = time.time()
        elapsed_time = st.session_state.end_time - st.session_state.start_time
        st.write(f"Time taken to answer the question: {elapsed_time} seconds")

