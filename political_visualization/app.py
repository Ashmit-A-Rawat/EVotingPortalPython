import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load CSV file
df = pd.read_csv("parties_data.csv")

# Set Streamlit title
st.title("📊 Indian Political Party Visualization")

# Sidebar for graph selection
st.sidebar.header("Choose a graph to display:")

# Buttons for different visualizations
if st.sidebar.button("📊 Total Wins by Party"):
    st.subheader("Total Wins by Political Party")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Party", y="Total_Wins", data=df, palette="viridis", ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Party")
    plt.ylabel("Total Wins")
    st.pyplot(fig)

if st.sidebar.button("🥧 Vote Share Distribution"):
    st.subheader("Vote Share Distribution")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(df["Vote_Share"], labels=df["Party"], autopct="%1.1f%%", colors=sns.color_palette("pastel"))
    st.pyplot(fig)

if st.sidebar.button("📈 Leader Popularity Over Years"):
    st.subheader("Leader Popularity Over Years")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="Founded", y="Leader_Popularity", hue="Party", marker="o", data=df, palette="tab10", ax=ax)
    plt.xlabel("Year Founded")
    plt.ylabel("Leader Popularity (Out of 100)")
    st.pyplot(fig)
    
# Sidebar for graph selection
st.sidebar.header("Choose a graph to display:")

# Radio buttons for different visualizations
graph_type = st.sidebar.radio("", ["Total Wins by Party", "Vote Share Distribution", "Leader Popularity Over Years"])

if graph_type == "Total Wins by Party":
    st.subheader("Total Wins by Political Party")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x="Party", y="Total_Wins", data=df, palette="viridis", ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Party")
    plt.ylabel("Total Wins")
    st.pyplot(fig)

elif graph_type == "Vote Share Distribution":
    st.subheader("Vote Share Distribution")
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(df["Vote_Share"], labels=df["Party"], autopct="%1.1f%%", colors=sns.color_palette("pastel"))
    st.pyplot(fig)

elif graph_type == "Leader Popularity Over Years":
    st.subheader("Leader Popularity Over Years")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(x="Founded", y="Leader_Popularity", hue="Party", marker="o", data=df, palette="tab10", ax=ax)
    plt.xlabel("Year Founded")
    plt.ylabel("Leader Popularity (Out of 100)")
    st.pyplot(fig)