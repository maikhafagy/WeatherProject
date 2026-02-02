import streamlit as st          # Import Streamlit to build web app
import pandas as pd            
import seaborn as sns           
import matplotlib.pyplot as plt 

# 1. Page Config
st.set_page_config(page_title="Mai's Weather Dashboard", layout="wide")
st.title("Global Weather & Air Quality Dashboard")  # Dashboard title
st.markdown("Developed by **Mai Khafaga**")  # Author info

# 2. Load and Process Data
@st.cache_data
def load_and_process():
    # Make sure 'GlobalWeatherRepository.csv' is in the same folder as this script
    df = pd.read_csv('GlobalWeatherRepository.csv')  
    
    # Clean condition text (make lowercase for consistency)
    df['condition_text'] = df['condition_text'].str.lower()
    
    # Create 'aqi_status' column logic
    def classify_aqi(aqi_value):
        if aqi_value <= 50: return 'Good'
        elif aqi_value <= 100: return 'Moderate'
        elif aqi_value <= 150: return 'Unhealthy for Sensitive Groups'
        elif aqi_value <= 200: return 'Unhealthy'
        else: return 'Very Unhealthy/Hazardous'

    if 'aqi_status' not in df.columns:
        df['aqi_status'] = df['air_quality_PM2.5'].apply(classify_aqi) 
        
    return df

# Load the data
try:
    df = load_and_process()  
    st.divider()              

    #  Q1: Bar Chart (PM2.5) ---
    st.header("1. Top 10 Most Polluted Countries (PM2.5)")
    top_10_pm = df.groupby('country')['air_quality_PM2.5'].mean().sort_values(ascending=False).head(10)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.barplot(x=top_10_pm.values, y=top_10_pm.index, hue=top_10_pm.index, palette='Reds_r', ax=ax1, legend=False)
    st.pyplot(fig1)

    #  Q2: Scatter Plot (Temp vs Humidity) ---
    st.header("2. Temperature vs Humidity Relation")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=df, x='temperature_celsius', y='humidity', alpha=0.3, color='purple', ax=ax2)
    st.pyplot(fig2)

    #  Q3: Box Plot (CO Levels) ---
    st.header("3. CO Levels across Top 5 Weather Conditions")
    top_conditions = df['condition_text'].value_counts().nlargest(5).index
    filtered_data = df[df['condition_text'].isin(top_conditions)]
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=filtered_data, x='condition_text', y='air_quality_Carbon_Monoxide', hue='condition_text', palette='copper_r', ax=ax3, legend=False)
    ax3.set_ylim(0, 1500)  
    st.pyplot(fig3)

    #  Q4: Pie Chart (AQI Status) ---
    st.header("4. Global Air Quality (AQI) Percentage")
    aqi_distribution = df['aqi_status'].value_counts()
    fig4, ax4 = plt.subplots(figsize=(8, 8))
    aqi_distribution.plot.pie(autopct='%1.1f%%', colors=sns.color_palette("pink"), startangle=140, ax=ax4)
    ax4.set_ylabel('')
    st.pyplot(fig4)

    #  Q5: Histogram (Temperature Distribution) ---
    st.header("5. Global Temperature Distribution Analysis")
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['temperature_celsius'], bins=30, kde=True, color='green', ax=ax5)
    ax5.set_xlabel('Temperature Celsius')
    st.pyplot(fig5)

    st.success("Conclusion: The temperature data follows a normal distribution centered around 20-25°C.")

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.warning("Please make sure 'GlobalWeatherRepository.csv' is in the same folder as this file.")
