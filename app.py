import seaborn as sns
import streamlit as st
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

google_sheet_url = "https://docs.google.com/spreadsheets/d/1AE6pb5v8EWSYnEoNtu_UJSj4SJVHXZLm4-t4MLzIxHY/gviz/tq?tqx=out:csv&gid=0"

@st.cache_data(ttl=60)
def fetch_data():   
    df = pd.read_csv(google_sheet_url)
    return df

df = fetch_data()

st.title('Streamlit App: Analysis of US Car Crashes')
st.subheader('Data Visualization')

# Question that will be visible to the user
st.write("Which U.S. states have the least safest drivers based on alcohol crashes?")

if 'chart_selected' not in st.session_state:
    st.session_state.chart_selected = False
if 'selected_chart' not in st.session_state:
    st.session_state.selected_chart = None
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'end_time' not in st.session_state:
    st.session_state.end_time = None

def chart_a():
    df["alcohol_pct"] = (df["alcohol"] / df["total"]) * 100  

    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="alcohol_pct", y="total", hue="alcohol_pct", size="alcohol_pct", palette="Blues_r", ax=ax)

    for i in range(len(df)):
        ax.text(df["alcohol_pct"][i], df["total"][i], df["abbrev"][i])

    ax.set_xlabel("Alcohol Accidents in Percentage")
    ax.set_ylabel("Total Car Crashes")
    ax.set_title("Chart A: Percentage of Alcohol Accidents vs. Total Crashes")
    st.pyplot(fig)

def chart_b():
    df["alcohol_pct"] = (df["alcohol"] / df["total"]) * 100  

    df_sorted = df.sort_values(by="alcohol_pct", ascending=False).head(10)  

    fig, ax = plt.subplots()
    sns.barplot(data = df_sorted, x="alcohol_pct", y="abbrev", palette="Blues_r", ax=ax)

    ax.set_xlabel("Alcohol Accidents in Pecentage")  
    ax.set_ylabel("US States")
    ax.set_title("Chart B: Top States with Most Alcohol Accidents in Pecentage")
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

