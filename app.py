import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from datetime import datetime
import os
import openpyxl

st.set_page_config(page_title="Aplikasi Absensi Online", layout="wide")

DATA_FILE = "absensi.xlsx"

# --- Jika file belum ada, buat file baru ---
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Nama", "Waktu", "Keterangan"])
    df.to_excel(DATA_FILE, index=False)

# --- Load data ---
def load_data():
    return pd.read_excel(DATA_FILE)

# --- Simpan data ---
def save_data(nama, ket):
    df = load_data()
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.loc[len(df)] = [nama, waktu, ket]
    df.to_excel(DATA_FILE, index=False)

# --------------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------------
menu = st.sidebar.radio("Menu", ["Absensi", "Generate QR", "Rekap"])

# --------------------------------------------------------
# ABSENSI
# --------------------------------------------------------
if menu == "Absensi":
    st.title("📌 Absensi Online")
    st.write("Masukkan nama sesuai QR yang discan")

    nama = st.text_input("Nama Pegawai")
    ket = st.selectbox("Keterangan", ["Masuk", "Pulang"])

    if st.button("Simpan Absensi"):
        if nama.strip() != "":
            save_data(nama, ket)
            st.success("Absensi berhasil disimpan!")
        else:
            st.error("Nama tidak boleh kosong.")

# --------------------------------------------------------
# GENERATE QR
# --------------------------------------------------------
elif menu == "Generate QR":
    st.title("📌 Generate QR Code Pegawai")

    nama_qr = st.text_input("Nama Pegawai untuk QR")

    if st.button("Buat QR Code"):
        if nama_qr.strip() == "":
            st.error("Nama harus diisi.")
        else:
            img = qrcode.make(nama_qr)
            img.save("qr.png")
            st.image("qr.png", caption=f"QR untuk {nama_qr}")
            st.success("QR berhasil dibuat!")

# --------------------------------------------------------
# REKAP ABSENSI
# --------------------------------------------------------
elif menu == "Rekap":
    st.title("📌 Rekap Absensi Pegawai")

    df = load_data()
    st.dataframe(df, use_container_width=True)

    # Download Excel
    st.download_button(
        label="Download Rekap (Excel)",
        data=open(DATA_FILE, "rb").read(),
        file_name="rekap_absensi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
