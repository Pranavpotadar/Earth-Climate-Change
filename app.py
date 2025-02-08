import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data():
    """Load and preprocess the climate change dataset"""
    df = pd.read_csv('climate_change_earth.csv')
    
    # Handle missing values
    df.dropna(subset=['AverageTemperature'], inplace=True)
    
    # Convert date column
    df['dt'] = pd.to_datetime(df['dt'])
    
    # Extract year and month
    df['Year'] = df['dt'].dt.year
    df['Month'] = df['dt'].dt.month
    
    # Convert latitude and longitude to float
    df['Latitude'] = df['Latitude'].str[:-1].astype(float)
    df['Longitude'] = df['Longitude'].str[:-1].astype(float)
    
    return df

def plot_yearly_trend(df):
    """Plot yearly temperature trend"""
    yearly_avg_temp = df.groupby('Year')['AverageTemperature'].mean()
    fig, ax = plt.subplots(figsize=(12, 5))
    yearly_avg_temp.plot(ax=ax)
    plt.xlabel("Year")
    plt.ylabel("Average Temperature (°C)")
    plt.title("Yearly Global Temperature Trend")
    plt.grid(True)
    return fig

def plot_temperature_distribution(df):
    """Plot temperature distribution"""
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(data=df, x='AverageTemperature', bins=50, kde=True)
    plt.title("Temperature Distribution")
    plt.xlabel("Temperature (°C)")
    return fig

def plot_top_hottest_cities(df):
    """Plot top 10 hottest cities"""
    city_avg_temp = df.groupby('City')['AverageTemperature'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12, 5))
    city_avg_temp.plot(kind='bar')
    plt.xlabel("City")
    plt.ylabel("Average Temperature (°C)")
    plt.title("Top 10 Hottest Cities")
    plt.xticks(rotation=45)
    return fig

def plot_monthly_trend(df):
    """Plot monthly temperature trend"""
    monthly_avg_temp = df.groupby('Month')['AverageTemperature'].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_avg_temp.plot(marker='o', linestyle='-')
    plt.xlabel("Month")
    plt.ylabel("Average Temperature (°C)")
    plt.title("Average Monthly Temperature Trend")
    plt.grid(True)
    return fig

def main():
    st.set_page_config(page_title="Climate Change Analysis Dashboard", layout="wide")
    
    st.title("Climate Change Analysis Dashboard")
    st.write("Analyzing global temperature changes over time")
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_and_preprocess_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Year range filter
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(int(df['Year'].min()), int(df['Year'].max()))
    )
    
    # Country filter
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("Select Country", ["All"] + list(countries))
    
    # Filter data based on year range and country
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Temperature", f"{filtered_df['AverageTemperature'].mean():.1f}°C")
    with col2:
        st.metric("Total Cities", len(filtered_df['City'].unique()))
    with col3:
        st.metric("Date Range", f"{filtered_df['dt'].min().year} - {filtered_df['dt'].max().year}")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Yearly Trend", "Temperature Distribution", "Hottest Cities", "Monthly Trend"])
    
    with tab1:
        st.pyplot(plot_yearly_trend(filtered_df))
        
    with tab2:
        st.pyplot(plot_temperature_distribution(filtered_df))
        
    with tab3:
        st.pyplot(plot_top_hottest_cities(filtered_df))
        
    with tab4:
        st.pyplot(plot_monthly_trend(filtered_df))
    
    # Data table
    st.subheader("Raw Data Sample")
    st.dataframe(filtered_df.head(100))
    
    # Add download button for filtered data
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_climate_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()