import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Bike Sharing Dashboard')

# Load data

day_df = pd.read_csv('data/day.csv')

weather_rentals = day_df.groupby('weathersit')['cnt'].mean().reset_index()

st.subheader('Rata-rata Penyewaan Berdasarkan Cuaca')

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(data=weather_rentals,
            x='weathersit',
            y='cnt',
            ax=ax)

st.pyplot(fig)