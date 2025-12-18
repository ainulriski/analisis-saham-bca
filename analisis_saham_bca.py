

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="BBCA Stock Analyzer", layout="wide")

st.title("📈 BBCA.JK Stock Analyzer")
st.write("Analisis saham BCA (BBCA.JK) dengan visualisasi harga dan moving average")

# Pilih tanggal
start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

if start_date > end_date:
    st.error("Start date harus sebelum End date")
else:
    # ===============================
    # Ambil data saham BCA
    # ===============================
    data = yf.download("BBCA.JK", start=start_date, end=end_date)
    data.reset_index(inplace=True)

    # Hitung Moving Average
    data['MA7'] = data['Close'].rolling(window=7).mean()
    data['MA30'] = data['Close'].rolling(window=30).mean()

    # Perubahan harian %
    data['Daily Change %'] = data['Close'].pct_change() * 100

    # ===============================
    # Grafik harga + MA
    # ===============================
    st.subheader("📊 Close Price & Moving Average")
    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(data['Date'], data['Close'], label='Close Price', color='blue')
    ax.plot(data['Date'], data['MA7'], label='MA 7 days', color='orange')
    ax.plot(data['Date'], data['MA30'], label='MA 30 days', color='green')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (IDR)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # ===============================
    # Histogram perubahan harian
    # ===============================
    st.subheader("📉 Daily Change % Histogram")
    fig2, ax2 = plt.subplots(figsize=(10,4))
    ax2.hist(data['Daily Change %'].dropna(), bins=50, color='purple', edgecolor='black')
    ax2.set_xlabel("Daily Change %")
    ax2.set_ylabel("Frequency")
    ax2.grid(True)
    st.pyplot(fig2)

    # ===============================
    # Insight
    # ===============================
    st.subheader("💡 Insight BBCA")
    st.write(f"Data dari {data['Date'].min().date()} sampai {data['Date'].max().date()}")
    st.write(f"Rata-rata harga penutupan: {data['Close'].mean():.2f} IDR")
    st.write(f"Harga tertinggi: {data['Close'].max():.2f} IDR")
    st.write(f"Harga terendah: {data['Close'].min():.2f} IDR")
    st.write(f"Rata-rata perubahan harian: {data['Daily Change %'].mean():.2f}%")

