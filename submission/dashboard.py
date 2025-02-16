# dashboard.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

# Load dataset
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')
    hour_df = pd.read_csv('data/hour.csv')
    return day_df, hour_df

day_df, hour_df = load_data()

# Data cleaning and preprocessing
def preprocess_data(df):
    # Convert 'dteday' to datetime
    df['dteday'] = pd.to_datetime(df['dteday'])
    
    # Convert categorical columns to category type
    categorical_cols = ['season', 'weathersit', 'holiday', 'workingday']
    df[categorical_cols] = df[categorical_cols].astype('category')
    return df

day_df = preprocess_data(day_df)
hour_df = preprocess_data(hour_df)

# Streamlit App Title
st.title("Dashboard Analisis Data Bike Sharing")

# Sidebar for Navigation
st.sidebar.title("Navigasi")
option = st.sidebar.selectbox(
    "Pilih Visualisasi",
    ["Distribusi Penyewaan", "Pertanyaan 1: Musim dan Cuaca", "Pertanyaan 2: Casual vs Registered", "Heatmap Korelasi"]
)

# Distribusi Penyewaan
if option == "Distribusi Penyewaan":
    st.header("Distribusi Total Penyewaan Sepeda Harian")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(day_df['cnt'], bins=30, kde=True, color='blue', ax=ax)
    ax.set_title('Distribusi Total Penyewaan Sepeda Harian', fontsize=14)
    ax.set_xlabel('Total Penyewaan', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.grid(True)
    st.pyplot(fig)

    st.markdown("""
    **Insight:**  
    - Distribusi total penyewaan sepeda (cnt) cenderung normal dengan beberapa outlier.
    - Rata-rata penyewaan harian adalah sekitar 4500 sepeda.
    """)

# Pertanyaan 1: Musim dan Cuaca
elif option == "Pertanyaan 1: Musim dan Cuaca":
    st.header("Rata-Rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca")
    season_weather = day_df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weather, palette='coolwarm', ax=ax)
    ax.set_title('Rata-Rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca', fontsize=14)
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-Rata Penyewaan', fontsize=12)
    ax.legend(title='Cuaca', title_fontsize=12, fontsize=10)
    ax.grid(axis='y')
    st.pyplot(fig)

    st.markdown("""
    **Insight:**  
    - Penyewaan tertinggi terjadi pada musim panas (season 3) dengan cuaca cerah (weathersit 1).
    - Cuaca buruk (weathersit 4) secara signifikan mengurangi jumlah penyewaan.
    """)

# Pertanyaan 2: Casual vs Registered
elif option == "Pertanyaan 2: Casual vs Registered":
    st.header("Perbandingan Rata-Rata Penyewaan: Casual vs Registered")
    user_type = day_df.groupby(['workingday', 'holiday'])[['casual', 'registered']].mean().reset_index()
    user_type_melted = user_type.melt(id_vars=['workingday', 'holiday'], value_vars=['casual', 'registered'],
                                      var_name='User Type', value_name='Average Rentals')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='workingday', y='Average Rentals', hue='User Type', data=user_type_melted, palette='Set2', ax=ax)
    ax.set_title('Perbandingan Rata-Rata Penyewaan: Casual vs Registered', fontsize=14)
    ax.set_xlabel('Hari Kerja (1) atau Hari Libur (0)', fontsize=12)
    ax.set_ylabel('Rata-Rata Penyewaan', fontsize=12)
    ax.legend(title='Tipe Pengguna', title_fontsize=12, fontsize=10)
    ax.grid(axis='y')
    st.pyplot(fig)

    st.markdown("""
    **Insight:**  
    - Pengguna `registered` mendominasi penyewaan pada hari kerja.
    - Pengguna `casual` lebih aktif pada hari libur.
    """)

# Heatmap Korelasi
elif option == "Heatmap Korelasi":
    st.header("Heatmap Korelasi Antar Variabel")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(day_df.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
    ax.set_title('Heatmap Korelasi Antar Variabel', fontsize=14)
    st.pyplot(fig)

    st.markdown("""
    **Insight:**  
    - Terdapat korelasi positif yang kuat antara suhu (`temp`) dan jumlah penyewaan (`cnt`).
    - Kondisi cuaca buruk (`weathersit`) memiliki korelasi negatif dengan jumlah penyewaan.
    """)

# Footer
st.sidebar.markdown("""
---
**Created by:** Weko Abbror  
**Email:** wekoabbror@gmail.com  
**ID Dicoding:** Weko Abbror
""")