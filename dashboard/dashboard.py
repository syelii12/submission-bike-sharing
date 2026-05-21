import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style="whitegrid")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

day_df = pd.read_csv(BASE_DIR / "day_clean.csv")
hour_df = pd.read_csv(BASE_DIR / "hour_clean.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

day_df.rename(columns={"cnt": "total_rentals"}, inplace=True)
hour_df.rename(columns={"cnt": "total_rentals"}, inplace=True)

# =========================
# SIDEBAR FILTER
# =========================
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.title("🔍 Filter Data")

    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date))
]

hour_filtered = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df["dteday"] <= pd.to_datetime(end_date))
]

if main_df.empty:
    st.error("Data kosong setelah filter.")
    st.stop()

# =========================
# HEADER
# =========================
st.markdown("""
# 🚲 Bike Sharing Analytics Dashboard
### Analisis penyewaan sepeda berdasarkan cuaca, musim, dan waktu
""")

st.divider()

# =========================
# KPI
# =========================
st.subheader("📌 Key Performance Indicator")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Rentals", f"{main_df['total_rentals'].sum():,.0f}")

with col2:
    st.metric("Average Daily", f"{main_df['total_rentals'].mean():.2f}")

with col3:
    st.metric("Max Daily", f"{main_df['total_rentals'].max():,.0f}")

with col4:
    st.metric("Data Points", len(main_df))

st.divider()

# =========================
# TREND
# =========================
st.subheader("📈 Daily Rental Trend")

daily_df = main_df.groupby("dteday")["total_rentals"].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(daily_df["dteday"], daily_df["total_rentals"], linewidth=2)
ax.set_title("Bike Rentals Over Time")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Rentals")
st.pyplot(fig)

st.divider()

# =========================
# WEATHER & SEASON
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌦️ Weather Impact")

    weather_col = "weather_label" if "weather_label" in main_df.columns else "weathersit"

    weather_df = main_df.groupby(weather_col)["total_rentals"].mean().reset_index()
    weather_df = weather_df.sort_values("total_rentals", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=weather_df, x=weather_col, y="total_rentals", ax=ax)
    ax.set_title("Average Rentals by Weather")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Rata-rata Rentals")
    plt.xticks(rotation=15)
    st.pyplot(fig)

with col2:
    st.subheader("🍂 Season Impact")

    season_col = "season_label" if "season_label" in main_df.columns else "season"

    season_df = main_df.groupby(season_col)["total_rentals"].mean().reset_index()
    season_df = season_df.sort_values("total_rentals", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=season_df, x=season_col, y="total_rentals", ax=ax)
    ax.set_title("Average Rentals by Season")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Rentals")
    st.pyplot(fig)

st.divider()

# =========================
# PEAK HOUR
# =========================
st.subheader("⏰ Jam Tersibuk pada Hari Kerja")

workingday_hour = hour_filtered[hour_filtered["workingday"] == 1]

peak_hour_df = workingday_hour.groupby("hr")["total_rentals"].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=peak_hour_df, x="hr", y="total_rentals", marker="o", ax=ax)
ax.set_title("Rata-rata Penyewaan Sepeda per Jam pada Hari Kerja")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Rentals")
ax.set_xticks(range(0, 24))
st.pyplot(fig)

st.divider()

# =========================
# WORKING DAY VS HOLIDAY
# =========================
st.subheader("🏢 Working Day vs Holiday")

work_df = main_df.groupby("workingday")["total_rentals"].mean().reset_index()
work_df["workingday"] = work_df["workingday"].map({
    0: "Holiday",
    1: "Working Day"
})

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=work_df, x="workingday", y="total_rentals", ax=ax)
ax.set_title("Average Rentals: Working Day vs Holiday")
ax.set_xlabel("")
ax.set_ylabel("Rata-rata Rentals")
st.pyplot(fig)

st.divider()

# =========================
# INSIGHTS
# =========================
st.subheader("💡 Key Insights")

st.info("""
- Cuaca cerah cenderung menghasilkan jumlah penyewaan sepeda yang lebih tinggi.
- Musim tertentu seperti Summer dan Fall menunjukkan demand penyewaan yang lebih besar.
- Pada hari kerja, puncak penyewaan terjadi pada jam berangkat dan pulang kerja.
- Filter tanggal dapat digunakan untuk mengeksplorasi pola penyewaan pada periode tertentu.
""")

st.caption("🚲 Bike Sharing Dashboard | Built with Streamlit")