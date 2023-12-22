import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO

def main():
    st.title('Bike Rental Dashboard')

    # Sidebar - Menu dropdown
    menu_options = ['Presentase Peminjaman di Hari Kerja dan Hari Libur', 'Pola Peminjaman Sepeda per Musim', 'Perbandingan Pola Peminjaman Sepeda']
    selected_option = st.sidebar.selectbox('Pilih Menu', menu_options)
    
    url = 'https://raw.githubusercontent.com/Elvina2242/dataset_Bike_rental/main/day.csv'

    try:
        # Gunakan fungsi read_csv dari pandas untuk membaca file dari URL
        df = pd.read_csv(url)

        if selected_option == 'Presentase Peminjaman di Hari Kerja dan Hari Libur':
            # Menambahkan kolom baru 'jenis_hari' untuk menandai hari libur dan hari kerja
            df['jenis_hari'] = df['holiday'].apply(lambda x: 'Holiday' if x == 1 else 'Workingday')

            # Menghitung rata-rata peminjaman sepeda pada hari libur dan hari kerja
            rata_rata_peminjaman_hari = df.groupby('jenis_hari')['cnt'].mean()

            # Plot pie chart untuk membandingkan peminjaman pada hari libur dan hari kerja
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(rata_rata_peminjaman_hari, labels=rata_rata_peminjaman_hari.index, autopct='%1.1f%%', colors=['lightgreen', 'lightblue'])
            ax.set_title('Perbandingan Peminjaman Sepeda pada Hari Libur dan Hari Kerja')  # Judul pie chart
            plt.tight_layout()
            st.pyplot(fig)

        elif selected_option == 'Pola Peminjaman Sepeda per Musim':
            # Mengelompokkan data berdasarkan musim dan menghitung rata-rata peminjaman sepeda
            rata_rata_per_musim = df.groupby('season')['cnt'].mean()

            # List yang berisi keterangan musim berdasarkan angka musim
            keterangan_musim = ['Springer', 'Summer', 'Fall', 'Winter']

            # Plot grafik untuk membandingkan jumlah rata-rata peminjaman tiap musim
            fig, ax = plt.subplots(figsize=(8, 6))
            grafik = rata_rata_per_musim.plot(kind='bar', color=['lightblue', 'salmon', 'lightgreen', 'orange'])
            plt.title('Rata-rata Peminjaman Sepeda per Musim')
            plt.xlabel('Musim')
            plt.ylabel('Rata-rata Peminjaman')
            plt.xticks(rotation=0)

            # Menambahkan keterangan musim ke dalam grafik
            for i, v in enumerate(rata_rata_per_musim):
                plt.text(i, v + 10, keterangan_musim[i], ha='center')

            plt.grid(axis='y')
            plt.tight_layout()

            # Menampilkan plot pada aplikasi Streamlit
            st.pyplot(fig)

        elif selected_option == 'Perbandingan Pola Peminjaman Sepeda':
            # Membaca data dari file CSV untuk visualisasi ketiga
            hour_url = 'https://raw.githubusercontent.com/Elvina2242/dataset_Bike_rental/main/hour.csv'
            Hour_df = pd.read_csv(hour_url)
            Hour_df['hr'] = Hour_df['instant'] % 24

            grouped_data = Hour_df.groupby(['hr', 'registered'])['cnt'].mean().reset_index()
            casual_data = grouped_data[grouped_data['registered'] == 0]
            registered_data = grouped_data[grouped_data['registered'] == 1]

            # Menampilkan plot pada aplikasi Streamlit
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(casual_data['hr'], casual_data['cnt'], label='Casual Users')
            ax.plot(registered_data['hr'], registered_data['cnt'], label='Registered Users')
            ax.set_xlabel('Hour of the Day')
            ax.set_ylabel('Rata-rata Jumlah Peminjaman Sepeda')
            ax.set_title('Perbandingan Pola Peminjaman Sepeda antara Pengguna Casual dan Terdaftar')
            ax.legend()
            ax.grid(True)

            # Menampilkan plot pada aplikasi Streamlit
            st.pyplot(fig)

        else:
            st.error("Gagal mengambil data. Pastikan URL valid.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
