import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Tambahkan judul dan deskripsi untuk aplikasi
st.title('Analisis Peminjaman Sepeda')
st.write('Unggah file CSV dengan data peminjaman sepeda:')

# Fungsi untuk membaca file yang diunggah dan mengonversinya menjadi DataFrame
def upload_and_process_data():
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        return df
    return None

# Memanggil fungsi unggah data
data = upload_and_process_data()

# Jika data telah diunggah, lanjutkan dengan visualisasi dan analisis statistik
if data is not None:
    # Menampilkan data yang diunggah
    st.write("Data yang Diunggah:")
    st.write(data.head())

    # Ubah kode untuk menampilkan statistik peminjaman permusim, perbulan, dan jumlah peminjam terbanyak
    st.subheader('Statistik Peminjaman Sepeda')

    # Misalnya, untuk menampilkan statistik peminjaman permusim
    seasonal_stats = data.groupby('season')['cnt'].describe()

    # Menampilkan statistik peminjaman permusim
    st.write("Statistik Peminjaman Sepeda Permuisim:")
    st.write(seasonal_stats)

    # Untuk menampilkan statistik peminjaman per bulan
    monthly_stats = data.groupby('mnth')['cnt'].describe()

    # Menampilkan statistik peminjaman per bulan
    st.write("Statistik Peminjaman Sepeda per Bulan:")
    st.write(monthly_stats)


# Membuat kolom baru 'hour' dari kolom 'instant' yang merepresentasikan jam pada hari
data['hr'] = data['instant'] % 24

# Mengelompokkan data berdasarkan jenis pengguna (casual dan terdaftar) dan jam pada hari
grouped_data = data.groupby(['hr', 'registered'])['cnt'].mean().reset_index()

# Filter data untuk pengguna casual dan terdaftar
casual_data = grouped_data[grouped_data['registered'] == 0]
registered_data = grouped_data[grouped_data['registered'] == 1]

# Plot perbandingan pola peminjaman sepeda pada waktu tertentu dalam sehari
plt.figure(figsize=(10, 6))
plt.plot(casual_data['hr'], casual_data['cnt'], label='Casual Users')
plt.plot(registered_data['hr'], registered_data['cnt'], label='Registered Users')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Rata-rata Jumlah Peminjaman Sepeda')
plt.title('Bandingkan Pola Peminjaman Sepeda antara Pengguna Casual dan Terdaftar')
plt.legend()
plt.grid(True)

# Menampilkan plot menggunakan Streamlit
st.pyplot(plt)