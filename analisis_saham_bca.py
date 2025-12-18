import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# =====================
# Streamlit Title
# =====================
st.title("📊 BBCA Stock Analyzer")
st.write("Analisis saham Bank Central Asia (BBCA) dengan visualisasi harga, moving average, dan histogram perubahan harian.")

# =====================
# Input Tanggal
# =====================
start_date = st.date_input("Tanggal Mulai", pd.to_datetime("2023-01-01"))
end_date = st.date_input("Tanggal Selesai", pd.to_datetime("2023-12-31"))

if start_date > end_date:
    st.error("Tanggal mulai harus sebelum tanggal selesai.")
else:
    # =====================
    # Ambil Data Saham
    # =====================
    data = yf.download("BBCA.JK", start=start_date, end=end_date, auto_adjust=True)

    if data.empty:
        st.warning("Data saham tidak tersedia untuk rentang tanggal ini.")
    else:
        # =====================
        # Visualisasi Harga
        # =====================
        st.subheader("Harga Penutupan dan Moving Average")
        data['MA7'] = data['Close'].rolling(7).mean()
        data['MA30'] = data['Close'].rolling(30).mean()

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(data.index, data['Close'], label='Close', color='blue')
        ax.plot(data.index, data['MA7'], label='MA 7 hari', color='orange')
        ax.plot(data.index, data['MA30'], label='MA 30 hari', color='green')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Harga (IDR)")
        ax.legend()
        st.pyplot(fig)

        # =====================
        # Histogram Daily Change
        # =====================
        st.subheader("Perubahan Harian (%)")
        data['Daily Change %'] = data['Close'].pct_change() * 100

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.hist(data['Daily Change %'].dropna(), bins=20, color='purple', alpha=0.7)
        ax2.set_xlabel("Perubahan Harian (%)")
        ax2.set_ylabel("Frekuensi")
        st.pyplot(fig2)

        # =====================
        # Insight Otomatis
        # =====================
        st.subheader("Insight")
        avg_close = float(data['Close'].mean())
        max_close = float(data['Close'].max())
        min_close = float(data['Close'].min())
        last_change = float(data['Daily Change %'].iloc[-1])

        st.write(f"Rata-rata harga penutupan: {avg_close:.2f} IDR")
        st.write(f"Harga tertinggi: {max_close:.2f} IDR")
        st.write(f"Harga terendah: {min_close:.2f} IDR")
        st.write(f"Perubahan terakhir: {last_change:.2f}%")
