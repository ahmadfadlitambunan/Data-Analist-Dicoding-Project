import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st 

def create_sum_by_day_df(df) :
    temp_df = df.copy()

    temp_df['weekday'] = temp_df['weekday'].map({
        0 : 'Minggu',
        1 : 'Senin',
        2 : 'Selasa',
        3 : 'Rabu',
        4 : 'Kamis',
        5 : 'Jum\'at',
        6 : 'Sabtu'
    })

    by_day_df = temp_df.groupby(by='weekday').agg({
        'cnt' : 'sum'
    }).reindex(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jum\'at', 'Sabtu', 'Minggu']).reset_index()

    return by_day_df

def create_sum_by_weather_df(df) :
    # Copy dataframe utama ke dataframe temporary
    temp_df = df.copy()

    # Melakukan mapping dan rename kolom untuk output lebih jelas
    temp_df['weathersit'] = temp_df['weathersit'].map({
        1 : 'Cerah',
        2 : 'Berkabut',
        3 : 'Hujan Ringan',
        4 : 'Hujan Lebat'
    })

    # Membuat pivot table weathersit
    by_weather_df = temp_df.groupby(by='weathersit').agg({
        'cnt':'sum'
    }).reindex(['Cerah', 'Berkabut', 'Hujan Ringan', 'Hujan Lebat'], fill_value = 0).reset_index()

    return by_weather_df

def create_sum_by_holiday(df) :
    # Copy dataframe utama ke dataframe temporary
    temp_df = df.copy()

    # Melakukan mapping untuk output lebih jelas
    temp_df['holiday'] = temp_df['holiday'].map({
        0 : 'Ya',
        1 : 'Tidak'
    })

    # Membuat pivot table
    pivot_table_by_holiday = temp_df.groupby(by='holiday').agg({
        'cnt':'sum'
    }).reindex(['Ya', 'Tidak']).reset_index()

    return pivot_table_by_holiday

def create_sum_by_weekend(df) :
    # Copy dataframe utama ke dataframe temporary
    temp_df = df.copy()
        
    # Membuat kolom baru untuk weekend atau tidak
    temp_df['weekend'] = temp_df['weekday'].apply(lambda x: 'Tidak' if x in [1,2,3,4,5] else 'Ya')

    pivot_table_by_weekend = temp_df.groupby(by='weekend').agg({
        'cnt' :'sum'
    }).reindex(['Ya', 'Tidak']).reset_index()

    return pivot_table_by_weekend

def create_sum_by_working_day(df):
    # Copy dataframe utama ke dataframe temporary
    temp_df = df.copy()

    # Melakukan mapping untuk output lebih jelas
    temp_df['workingday'] = temp_df['workingday'].map({
        1 : 'Ya',
        0 : 'Tidak'
    })

    pivot_table_by_working_day = temp_df.groupby(by='workingday').agg({
        'cnt' : 'sum'
    }).reindex(['Ya', 'Tidak']).reset_index()

    return pivot_table_by_working_day

def creat_ratio_by_user(df):
    # Mencari Total Jumlah User
    sum_casual = df['casual'].sum()
    sum_registered = df['registered'].sum()

    # Hitung persentase
    persentase_casual = (sum_casual/(sum_casual + sum_registered)) * 100
    # persentase_registered = ((sum_casual + sum_registered)/sum_registered) * 100

    # buat tabel pivot
    result_df = pd.DataFrame({
        'Tipe User' : ['Casual', 'Registered'],
        'Jumlah Peminjaman' : [sum_casual, sum_registered],
        'Persentase': [persentase_casual, 100-persentase_casual]
    })

    return result_df

df = pd.read_csv("main_data.csv")

st.header(
    "Bike Sharing Dashboard :bike:"
)

with st.container() :

    # Visualisasi berdasarkan Hari
    st.subheader(
        "Total Peminjaman berdasarkan Hari"
    )

    total_rentals = df['cnt'].sum()
    st.metric("Total Rental", value=f"{total_rentals:,}")


    # Visualisasi berdasarkan hari
    # ambil data
    by_day_df = create_sum_by_day_df(df)

    colors = ["#f5d7b0", "#f5d7b0", "#f5d7b0",  "#f5d7b0","#d15b56", "#f5d7b0", "#f5d7b0"]

    # creating plot
    fig, ax1 = plt.subplots(figsize=(16, 8))

    sns.barplot(x = by_day_df['weekday'], y = by_day_df['cnt'], palette=colors, ax=ax1)
    ax1.plot(by_day_df['weekday'], by_day_df['cnt'])
    ax1.scatter(by_day_df['weekday'], by_day_df['cnt'], color='blue')

    ax1.set_title("Total Peminjaman Sepeda dari Senin-Minggu", loc="center", fontsize=15)
    ax1.set_ylabel("Total Peminjaman")
    ax1.set_xlabel(None)
    ax1.tick_params(axis='x', labelsize=12)

    st.pyplot(fig)


with st.container() :
    # Visualisasi berdasarkan Cuaca
    st.subheader(
        "Total Peminjaman berdasarkan Cuaca"
    )
    col1, col2, col3, col4 = st.columns(4)
    by_weather = create_sum_by_weather_df(df)

    with col1:
        total = by_weather.loc[0, 'cnt']
        st.metric("Cerah ☀️", value=f"{total:,}")

    with col2:
        total = by_weather.loc[1, 'cnt']
        st.metric("Berkabut 🌫️", value=f"{total:,}")

    with col3:
        total = by_weather.loc[2, 'cnt']
        st.metric("Hujan Ringan 🌧️ ", value=f"{total:,}")

    with col4:
        total = by_weather.loc[3, 'cnt']
        st.metric("Hujan Lebat ⛈️", value=f"{total:,}")

    # Buat plot
    fig, ax2 =  plt.subplots(figsize=(16, 8))
    colors = ["#d15b56", "#f5d7b0", "#f5d7b0", "#f5d7b0"]

    sns.barplot(x = 'weathersit', y = 'cnt', data=create_sum_by_weather_df(df), palette=colors, ax=ax2)

    ax2.set_title("Total Peminjaman Sepeda Berdasarkan Cuaca", loc="center", fontsize=15)
    ax2.set_ylabel("Total Peminjaman (juta)")
    ax2.set_xlabel(None)
    ax2.tick_params(axis='x', labelsize=12)

    st.pyplot(fig)

with st.container() :
    # Visualisasi berdasarkan jenis hari
    st.subheader(
        "Total Peminjaman berdasarkan Hari Libur, Hari Kerja, dan Akhir Pekan"
    )

    # membuat visualisasi
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize = (20, 4))
    colors = ["#d15b56","#f5d7b0"]

    # visualisasi holiday
    sns.barplot(x = 'holiday', y = 'cnt', data = create_sum_by_holiday(df), palette=colors, ax = ax1)
    ax1.set_title("Jumlah Peminjaman Sepeda berdasarkan Holiday")
    ax1.set_xlabel("Holiday (Ya/Tidak)")
    ax1.set_ylabel("Jumlah Peminjaman (juta)")

    # visualisasi weekend
    sns.barplot(x = 'workingday', y = 'cnt', data = create_sum_by_working_day(df), palette=colors, ax=ax2)
    ax2.set_title("Jumlah Peminjaman Sepeda berdasarkan Working Day")
    ax2.set_xlabel("Working Day (Ya/Tidak)")
    ax2.set_ylabel("Jumlah Peminjaman (juta)")

    # visualisasi weekend
    sns.barplot(x = 'weekend', y = 'cnt', data = create_sum_by_weekend(df), palette=colors, ax=ax3)
    ax3.set_title("Jumlah Peminjaman Sepeda berdasarkan Weekend")
    ax3.set_xlabel("Weekend (Ya/Tidak)")
    ax3.set_ylabel("Jumlah Peminjaman (juta)")
    st.pyplot(fig)


with st.container():
    # Perbandingan antara pengguna casual dan registered
    st.subheader(
        "Persentase Perbandingan User Casual dan User Registered"
    )

    # get data
    rasio_user_df = creat_ratio_by_user(df)

    col1, col2 = st.columns(2)

    with col2:
        total = rasio_user_df.loc[0, 'Jumlah Peminjaman']
        st.metric("Total Pengguna Casual", value=f"{total:,}")

    with col1:
        total = rasio_user_df.loc[1, 'Jumlah Peminjaman']
        st.metric("Total Pengguna Registered", value=f"{total:,}")


    # buat visualisasi pie chart
    colors = ["#f5d7b0","#d15b56"]



    fig = plt.figure(figsize=(4, 4))
    plt.title("Rasio Perbandingan Antara User Casual dan User Registered")

    # Plotting Pie Chart
    plt.pie(rasio_user_df['Persentase'], labels=rasio_user_df['Tipe User'], autopct='%1.1f%%', colors = colors, explode=(0.05, 0))

    st.pyplot(fig)