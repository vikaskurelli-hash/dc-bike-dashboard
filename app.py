import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page Config
st.set_page_config(page_title="DC Bike Rental Dashboard", layout="wide")

# 1. DATA LOADING & CLEANING (Combined from Assignment 1)
@st.cache_data
def load_data():
    if not os.path.exists('train.csv'):
        st.error("Missing 'train.csv'! Please place it in the same folder as app.py.")
        st.stop()
        
    df = pd.read_csv('train.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Create temporal columns
    df['year'] = df['datetime'].dt.year
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.day_name()
    
    # Season Mapping
    df['season'] = df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
    
    # Day Period Binning
    def get_period(h):
        if 0 <= h < 6: return 'Night'
        elif 6 <= h < 12: return 'Morning'
        elif 12 <= h < 18: return 'Afternoon'
        else: return 'Evening'
    df['day_period'] = df['hour'].apply(get_period)
    return df

df = load_data()

# --- 2. INTERACTIVE WIDGETS (Requirement for Assignment 3) ---
st.sidebar.header("Dashboard Filters")
selected_years = st.sidebar.multiselect("Select Years", [2011, 2012], default=[2011, 2012])
selected_seasons = st.sidebar.multiselect("Select Seasons", df['season'].unique(), default=df['season'].unique())
working_day = st.sidebar.radio("Day Type", ["All", "Working Day", "Weekend/Holiday"])

# Filter Logic
filtered_df = df[df['year'].isin(selected_years) & df['season'].isin(selected_seasons)]
if working_day == "Working Day":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif working_day == "Weekend/Holiday":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# --- 3. PLOTS (Requirement: 4-6 plots from Assignment 2) ---
st.title("🚲 Washington D.C. Bike Rental Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Hourly Rental Trends")
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=filtered_df, x='hour', y='count', ax=ax1)
    st.pyplot(fig1)

    st.subheader("Weather Impact")
    fig2, ax2 = plt.subplots()
    sns.barplot(data=filtered_df, x='weather', y='count', ax=ax2)
    st.pyplot(fig2)

with col2:
    st.subheader("Rentals by Day Period")
    fig3, ax3 = plt.subplots()
    sns.barplot(data=filtered_df, x='day_period', y='count', order=['Morning', 'Afternoon', 'Evening', 'Night'], ax=ax3)
    st.pyplot(fig3)

    st.subheader("Feature Correlation")
    fig4, ax4 = plt.subplots()
    sns.heatmap(filtered_df[['temp', 'humidity', 'windspeed', 'count']].corr(), annot=True, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)