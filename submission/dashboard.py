import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache
def load_data():
    data = pd.read_csv('data/day.csv')
    return data

day_df = load_data()

# Convert 'dteday' to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Convert categorical columns to category type
categorical_cols = ['season', 'weathersit', 'holiday', 'workingday']
day_df[categorical_cols] = day_df[categorical_cols].astype('category')

# Title
st.title('Bike Sharing Dataset Analysis Dashboard')

# Sidebar for user input
st.sidebar.header('Filter Data')
selected_season = st.sidebar.selectbox('Select Season', options=day_df['season'].unique())
selected_weather = st.sidebar.selectbox('Select Weather', options=day_df['weathersit'].unique())

# Filter data based on user input
filtered_data = day_df[(day_df['season'] == selected_season) & (day_df['weathersit'] == selected_weather)]

# Pertanyaan 1: Pola Penyewaan Berdasarkan Musim dan Cuaca
st.header('Pertanyaan 1: Pola Penyewaan Berdasarkan Musim dan Cuaca')

# Group by season and weathersit
season_weather = day_df.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

# Plot
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', hue='weathersit', data=season_weather, ax=ax1)
ax1.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Cuaca')
ax1.set_xlabel('Musim')
ax1.set_ylabel('Rata-rata Penyewaan')
ax1.legend(title='Cuaca')
st.pyplot(fig1)

# Insight for Pertanyaan 1
st.write("**Insight:**")
st.write("- Penyewaan sepeda tertinggi terjadi pada musim panas (season 2) dengan cuaca cerah (weathersit 1).")
st.write("- Cuaca buruk (weathersit 4) mengurangi jumlah penyewaan secara signifikan.")

# Pertanyaan 2: Perbedaan Pola Penyewaan Casual vs Registered
st.header('Pertanyaan 2: Perbedaan Pola Penyewaan Casual vs Registered')

# Group by workingday and holiday
user_type = day_df.groupby(['workingday', 'holiday'])[['casual', 'registered']].mean().reset_index()

# Melt data for visualization
user_type_melted = user_type.melt(id_vars=['workingday', 'holiday'], value_vars=['casual', 'registered'], 
                                 var_name='User Type', value_name='Average Rentals')

# Plot
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x='workingday', y='Average Rentals', hue='User Type', data=user_type_melted, ax=ax2)
ax2.set_title('Rata-rata Penyewaan Sepeda: Casual vs Registered')
ax2.set_xlabel('Hari Kerja (1) atau Libur (0)')
ax2.set_ylabel('Rata-rata Penyewaan')
ax2.legend(title='Tipe Pengguna')
st.pyplot(fig2)

# Insight for Pertanyaan 2
st.write("**Insight:**")
st.write("- Pengguna registered mendominasi penyewaan pada hari kerja (workingday).")
st.write("- Pengguna casual lebih aktif pada hari libur (holiday).")

# Additional Analysis: Correlation Heatmap
st.header('Analisis Lanjutan: Korelasi Antar Variabel')

# Correlation heatmap
fig3, ax3 = plt.subplots(figsize=(10, 8))
sns.heatmap(day_df.corr(), annot=True, cmap='coolwarm', ax=ax3)
ax3.set_title('Heatmap Korelasi Antar Variabel')
st.pyplot(fig3)

# Insight for Additional Analysis
st.write("**Insight:**")
st.write("- Terdapat korelasi positif antara suhu (`temp`) dan jumlah penyewaan (`cnt`).")
st.write("- Kelembaban (`hum`) memiliki korelasi negatif dengan jumlah penyewaan.")

# Conclusion
st.header('Kesimpulan')
st.write("1. **Pertanyaan 1:** Musim dan cuaca memiliki pengaruh signifikan terhadap jumlah penyewaan sepeda. Penyewaan tertinggi terjadi pada musim panas dengan cuaca cerah, sementara cuaca buruk mengurangi minat penyewaan.")
st.write("2. **Pertanyaan 2:** Pengguna registered lebih aktif pada hari kerja, sementara pengguna casual lebih aktif pada hari libur. Hal ini menunjukkan perbedaan pola penggunaan antara kedua jenis pengguna.")