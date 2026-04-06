import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('submission\\dashboard\\bike_hour.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['month_year'] = df['dteday'].dt.to_period('M')
    return df

df = load_data()

# Title
st.title('Dashboard Penyewaan Sepeda Interaktif')

# Sidebar for filters
st.sidebar.header('Filter Data')
    # Filter untuk cuaca
with st.sidebar.expander('Filter Berdasarkan Cuaca'):
    weather_options = df['weathersit'].unique()
    selected_weather = st.multiselect('Pilih Cuaca:', weather_options, default=weather_options)

    # Filter untuk tahun
with st.sidebar.expander('Filter Berdasarkan Tahun'):
    year_options = df['yr'].unique()
    selected_years = st.multiselect('Pilih Tahun:', year_options, default=year_options)

# Question 1: Tren penyewaan berdasarkan cuaca dan tahun
st.header('1. Tren Penyewaan Sepeda Berdasarkan Cuaca')


# Filter data
filtered_df_q1 = df[(df['weathersit'].isin(selected_weather)) & (df['yr'].isin(selected_years))]

# Agregasi data per cuaca per tahun
weather_summary = filtered_df_q1.groupby(['yr', 'weathersit'])['cnt'].sum().reset_index()


# Plot bar chart untuk tren penyewaan berdasarkan cuaca
color_weather = ['#00008B', '#87CEEB']
fig, ax = plt.subplots(figsize=(12, 7))
sns.barplot(data=weather_summary, x='weathersit', y='cnt', hue='yr', palette=color_weather, ax=ax)
ax.set_title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca (2011 & 2012)', fontsize=16)
ax.set_xlabel('Kondisi Cuaca', fontsize=12)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.grid(axis='y', linestyle='--', alpha=0.7)

for container in ax.containers:
    ax.bar_label(container, fmt='%.0f', label_type='edge', fontsize=9)

plt.tight_layout()
st.pyplot(fig)

# Question 2: Perbedaan performa antara hari kerja dan hari libur
st.header('2. Perbedaan Performa Penyewaan Sepeda: Hari Kerja vs Hari Libur')

# Filter tahun untuk Q2
selected_years_q2 = st.multiselect('Pilih Tahun untuk Perbandingan:', year_options, default=year_options, key='q2_years')

# Filter data
filtered_df_q2 = df[df['yr'].isin(selected_years_q2)]

# Agregasi total penyewaan berdasarkan workingday dan tahun
workingday_rentals = filtered_df_q2.groupby(['yr', 'workingday'])['cnt'].sum().reset_index()

# Plot bar chart
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=workingday_rentals, x='workingday', y='cnt', hue='yr', palette=['#00008B', '#87CEEB'], ax=ax2)
ax2.set_title('Jumlah Penyewaan Sepeda Berdasarkan Hari Kerja vs. Hari Libur/Akhir Pekan (2011 & 2012)', fontsize=14)
ax2.set_xlabel('Tipe Hari', fontsize=12)
ax2.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

for container in ax2.containers:
    ax2.bar_label(container, fmt='%.0f', label_type='edge', fontsize=9)

plt.tight_layout()
st.pyplot(fig2)


