import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df
    
def tab1_analysis(df):
    df1_clean = df1.dropna()  # Menangani Missing Values dengan Menghapus Baris yang Mengandung Nilai Kosong
    df1_missing_value = df1.isnull().sum()  # Memeriksa Jumlah Missing Values Setelah Penghapusan
    df1_info = df1.info() # Menampilkan Informasi Tentang Data Setelah Penghapusan Missing Values
    pm25_max_idx = df1['PM2.5'].idxmax()  # Mengambil indeks dengan PM2.5 tertinggi
    pm25_min_idx = df1['PM2.5'].idxmin()  # Mengambil indeks dengan PM2.5 terendah

    year_pm25_max = df1.loc[pm25_max_idx, 'year']
    tert_high_pm25 = df1.loc[pm25_max_idx, 'PM2.5']
    mean_pm25 = df1_clean['PM2.5'].mean()

    year_pm25_min = df1.loc[pm25_min_idx, 'year']
    tert_low_pm25 = df1.loc[pm25_min_idx, 'PM2.5']
    extreme_values = pd.DataFrame({
    'Tahun': [df1.loc[pm25_max_idx, 'year'], df1.loc[pm25_min_idx, 'year']],
    'PM2.5': [df1.loc[pm25_max_idx, 'PM2.5'], df1.loc[pm25_min_idx, 'PM2.5']],
    'Keterangan': ['Tertinggi', 'Terendah'],
        })
    
    # Menampilkan dataframe
    st.dataframe(extreme_values)
    st.write('Rata-Rata : ',mean_pm25)

    # Membuat plot
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.bar(df1['year'], df1['PM2.5'], color='b')  # Menggunakan ax.bar() untuk membuat bar chart

    # Menambahkan judul dan label
    ax.set_title('Tren PM2.5 per Tahun', size=18)
    ax.set_xlabel('Year', size=14)
    ax.set_ylabel('PM2.5 (Rata-rata)', size=14)

    # Menampilkan di Streamlit
    st.pyplot(fig)

    with st.expander("Penjelasan Perubahan PM2.5") :
        st.write('Dari analisis ini, dapat disimpulkan bahwa kualitas udara di Changping memiliki fluktuasi yang signifikan selama periode yang dianalisis. Tahun dengan kadar PM2.5 tertinggi adalah 2016 dengan kadar 882.0 µg/m³, sementara kadar terendah tercatat pada tahun 2013 dengan nilai 2.0 µg/m³. Modus data menunjukkan bahwa ada frekuensi tinggi untuk nilai 0 µg/m³,mungkin menunjukkan kualitas udara yang sangat baik pada beberapa waktu tertentu.') 
        
def tab2_analysis(df):
    df2_clean = df2.dropna()  # Menangani Missing Values dengan Menghapus Baris yang Mengandung Nilai Kosong
    df2_missing_value = df2.isnull().sum()  # Memeriksa Jumlah Missing Values Setelah Penghapusan
    df2_info = df2.info() # Menampilkan Informasi Tentang Data Setelah Penghapusan Missing Values
    # Menghitung total tekanan udara (PRES) per tahun
    total_pres_per_tahun = df2.groupby('year')['PRES'].sum().reset_index()

    # Mengubah nama kolom agar lebih jelas
    total_pres_per_tahun.columns = ['Tahun', 'Total Tekanan Udara (hPa)']

    # Menampilkan tabel di Streamlit
    st.write("Total kadar tekanan udara (PRES) berdasarkan tahun:")
    st.dataframe(total_pres_per_tahun, use_container_width=True)

    # Membuat figure dan axis
    fig, ax = plt.subplots(figsize=(14, 8))

    # Membuat diagram batang dengan sumbu X yang benar
    ax.bar(total_pres_per_tahun['Tahun'], total_pres_per_tahun['Total Tekanan Udara (hPa)'], 
        color='skyblue', edgecolor='black')

    # Menambahkan judul dan label
    ax.set_title('Total Kadar Tekanan Udara (PRES) Berdasarkan Tahun', fontsize=14)
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Total Tekanan Udara (hPa)', fontsize=12)

    # Menampilkan grid untuk kemudahan membaca
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    with st.expander("Penjelasan Total Tekanan Udara") :
        st.write('Total kadar tekanan udara menunjukkan variasi antar tahun, yang dapat mencerminkan perubahan kondisi atmosfer seperti pola cuaca atau perubahan musiman. Informasi ini berguna untuk memantau tren cuaca di wilayah tertentu dan dapat digunakan untuk keperluan penelitian ilmiah, perencanaan kota, atau analisis dampak perubahan iklim.')

def tab3_analysis(df):
    df3_clean = df3.dropna()  # Menangani Missing Values dengan Menghapus Baris yang Mengandung Nilai Kosong
    df3_missing_value = df3.isnull().sum()  # Memeriksa Jumlah Missing Values Setelah Penghapusan
    df3_info = df3.info() # Menampilkan Informasi Tentang Data Setelah Penghapusan Missing Values
    # Konversi ke datetime
    df3['datetime'] = pd.to_datetime(df3[['year', 'month', 'day', 'hour']])

    # Ekstrak bulan dan tahun dari kolom datetime
    df3['Tahun_Bulan'] = df3['datetime'].dt.to_period('M')

    # Menghitung rata-rata PM2.5 per bulan
    pm25_per_month = df3.groupby('Tahun_Bulan')['PM2.5'].mean()

    # Menampilkan hasil tren PM2.5 per bulan
    st.write(pm25_per_month)

    # Membuat chart untuk tren PM2.5 dari bulan ke bulan
    fig, ax = plt.subplots(figsize=(14, 8))

    # Menggunakan ax.bar() untuk plotting
    ax.bar(pm25_per_month.index.astype(str), pm25_per_month.values, color='orange', alpha=0.7)

    # Menambahkan judul dan label
    ax.set_title("Tren Kadar PM2.5 dari Bulan ke Bulan", fontsize=16)
    ax.set_xlabel("Bulan/Tahun", fontsize=12)
    ax.set_ylabel("Rata-rata PM2.5", fontsize=12)

    # Memutar label sumbu X agar lebih terbaca
    ax.set_xticklabels(pm25_per_month.index.astype(str), rotation=45)

    # Menambahkan grid horizontal untuk kemudahan pembacaan
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
    
    with st.expander("Penjelasan Tren Kadar PM 2.5"):
        st.write('Tren kadar PM2.5 per bulan menunjukkan fluktuasi yang signifikan, dengan beberapa bulan mengalami kadar yang lebih tinggi dibandingkan bulan lainnya. Kadar PM2.5 cenderung dipengaruhi oleh faktor musiman dan kondisi atmosfer. Pola ini mengindikasikan perlunya perhatian lebih pada bulan-bulan tertentu untuk pengendalian polusi dan kebijakan kesehatan masyarakat.')

def tab4_analysis(df):
    df4_clean = df4.dropna()  # Menangani Missing Values dengan Menghapus Baris yang Mengandung Nilai Kosong
    df4_missing_value = df4.isnull().sum()  # Memeriksa Jumlah Missing Values Setelah Penghapusan
    df4_info = df4.info() # Menampilkan Informasi Tentang Data Setelah Penghapusan Missing Values
    # Menghitung rata-rata konsentrasi SO2, NO2, dan CO berdasarkan waktu (jam)
    rata_rata_konsentrasi = df4.groupby('hour')[['SO2', 'NO2', 'CO']].mean().reset_index()

    # Menampilkan tabel di Streamlit
    st.write("Rata-rata Konsentrasi SO2, NO2, dan CO berdasarkan Jam:")
    st.dataframe(rata_rata_konsentrasi)

    # Membuat figure dan axis
    fig, ax = plt.subplots(figsize=(14, 8))

    # Bar chart untuk masing-masing polutan
    ax.bar(rata_rata_konsentrasi['hour'] - 0.2, rata_rata_konsentrasi['SO2'], width=0.2, label='SO2', color='blue')
    ax.bar(rata_rata_konsentrasi['hour'], rata_rata_konsentrasi['NO2'], width=0.2, label='NO2', color='green')
    ax.bar(rata_rata_konsentrasi['hour'] + 0.2, rata_rata_konsentrasi['CO'], width=0.2, label='CO', color='red')

    # Menambahkan label dan judul
    ax.set_xlabel('Jam dalam Sehari', fontsize=12)
    ax.set_ylabel('Rata-Rata Konsentrasi', fontsize=12)
    ax.set_title('Rata-Rata Konsentrasi SO2, NO2, dan CO per Jam', fontsize=14)

    # Mengatur sumbu X agar menampilkan jam dengan jelas
    ax.set_xticks(rata_rata_konsentrasi['hour'])

    # Menambahkan legenda
    ax.legend()

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    
    with st.expander("Penjelasan Nilai Konsentrasi SO2, NO2, dan CO"):
        st.write('Konsentrasi ketiga polutan cenderung lebih tinggi pada malam hingga pagi hari, yang dapat disebabkan oleh aktivitas manusia serta kondisi atmosfer yang membatasi penyebaran polutan pada malam hari. Siang hingga sore hari menunjukkan penurunan konsentrasi, yang mungkin disebabkan oleh peningkatan ventilasi atmosfer dan sinar matahari yang mendorong reaksi fotokimia.')

def tab5_analysis(df):
    df5_clean = df5.dropna()  # Menangani Missing Values dengan Menghapus Baris yang Mengandung Nilai Kosong
    df5_missing_value = df5.isnull().sum()  # Memeriksa Jumlah Missing Values Setelah Penghapusan
    df5_info = df5.info() # Menampilkan Informasi Tentang Data Setelah Penghapusan Missing Values
    # Konversi ke datetime
    df5['date'] = pd.to_datetime(df5[['year', 'month', 'day']])

    # Menambahkan kolom 'day_of_week' untuk nama hari dan 'is_weekend' sebagai flag akhir pekan
    df5['day_of_week'] = df5['date'].dt.day_name()
    df5['is_weekend'] = df5['day_of_week'].isin(['Saturday', 'Sunday'])

    # Memilih kolom yang relevan untuk analisis
    polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
    df5_terfilter = df5[['date', 'day_of_week', 'is_weekend'] + polutan]

    # Mengelompokkan data berdasarkan weekday/weekend dan menghitung rata-rata
    polusi_weekday_vs_weekend = df5_terfilter.groupby('is_weekend')[polutan].mean().reset_index()

    # Menambahkan label kategori
    polusi_weekday_vs_weekend['Kategori'] = polusi_weekday_vs_weekend['is_weekend'].map({False: 'Weekday', True: 'Weekend'})
    polusi_weekday_vs_weekend = polusi_weekday_vs_weekend.drop(columns=['is_weekend'])

    # Menampilkan tabel hasil
    st.write("Tabel rata-rata tingkat polusi antara Weekday dan Weekend:")
    st.dataframe(polusi_weekday_vs_weekend)

    # Memisahkan data berdasarkan hari kerja (weekday) dan akhir pekan (weekend)
    data_weekday = df5_terfilter[df5_terfilter['is_weekend'] == False]
    data_weekend = df5_terfilter[df5_terfilter['is_weekend'] == True]

    # Membuat histogram untuk masing-masing polutan
    fig, ax = plt.subplots(figsize=(14, 8))

    for pollutant in polutan:
        # Histogram untuk data weekday
        ax.hist(data_weekday[pollutant], bins=30, alpha=0.5, label=f'{pollutant} - Hari Kerja')
        # Histogram untuk data weekend
        ax.hist(data_weekend[pollutant], bins=30, alpha=0.5, label=f'{pollutant} - Akhir Pekan')

    # Menambahkan judul, label, dan legenda
    ax.set_title('Distribusi Polutan Berdasarkan Hari Kerja vs Akhir Pekan', fontsize=14)
    ax.set_xlabel('Konsentrasi Polutan', fontsize=12)
    ax.set_ylabel('Frekuensi', fontsize=12)
    ax.legend(fontsize='small')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)
    
    with st.expander("Penjelasan Konsentrasi Polutan"):
        st.write('Konsentrasi polutan PM2.5, PM10, SO2, dan CO cenderung lebih tinggi pada akhir pekan (weekend) dibandingkan hari kerja (weekday). Konsentrasi NO2 dan O3 relatif stabil antara hari kerja dan akhir pekan.')
            
# Load data
df1 = load_data("https://raw.githubusercontent.com/Yonaki97/IF4_Kelompok1/refs/heads/master/PRSA_Data_Changping_20130301-20170228.csv")
df2 = load_data("https://raw.githubusercontent.com/Yonaki97/IF4_Kelompok1/refs/heads/master/PRSA_Data_Wanshouxigong_20130301-20170228.csv")
df3 = load_data("https://raw.githubusercontent.com/Yonaki97/IF4_Kelompok1/refs/heads/master/PRSA_Data_Dingling_20130301-20170228.csv")
df4 = load_data("https://raw.githubusercontent.com/Yonaki97/IF4_Kelompok1/refs/heads/master/PRSA_Data_Gucheng_20130301-20170228.csv")
df5 = load_data("https://raw.githubusercontent.com/Yonaki97/IF4_Kelompok1/refs/heads/master/PRSA_Data_Shunyi_20130301-20170228.csv")

# Sidebar menu
with st.sidebar:
    selected = option_menu('Menu', ['Dashboard', 'About Us'],
        icons=["easel2"],
        menu_icon="cast",
        default_index=0)

if (selected == 'Dashboard'):
    st.title("Dashboard Analisis Data")
    
    tab1, tab2, tab3, tab4, tab5= st.tabs([
        "Analisis Changping", 
        "Analisis Wanshouxigong", 
        "Analisis Dingling", 
        "Analisis Gucheng", 
        "Analisis Shunyi"
    ])
    with tab1:
        st.header("Analisis Data Changping")
        st.write("1. Tahun berapa PM2.5 tertinggi dan terendah serta rata-ratanya?")
        tab1_analysis(df1)
        
    with tab2:
        st.header("Analisis Data Wanshouxigong")
        st.write("2. Menghitung total kadar tekanan udara berdasarkan tahun (PRES)")
        tab2_analysis(df2)
        
    with tab3:
        st.header("Analisis Data Dingling")
        st.write ("3. Menghitung tren kadar PM2.5 dari bulan ke bulan")
        tab3_analysis(df3)
        
    with tab4:
        st.header("Analisis Data Gucheng")
        st.write("4. Menghitung rata-rata konsentrasi SO2, NO2, dan CO berdasarkan waktu (jam)")
        tab4_analysis(df4)
        
    with tab5:
        st.header("Analisis Data Shunyi")
        st.write("5. Menghitung rata-rata konsentrasi polutan antara hari kerja (weekday) dan akhir pekan (weekend)")
        tab5_analysis(df5)
        
    
if (selected == 'About Us'):
    st.title("Kelompok 1 - IF4")
    st.write('1. 10123163 - Aldo Revaldo')
    st.write('2. 10123171 - Agung Rezalky')
    st.write('3. 10123143 - Randi Adittiawan')
    st.write('4. 10123164 - Elvin Juniansha')
    st.write('5. 10123136 - Muhammad Zaidan Azhari')