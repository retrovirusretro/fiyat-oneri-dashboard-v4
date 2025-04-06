import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Fiyat Öneri Dashboard v3", layout="wide")
st.title("📊 Fiyat Öneri Dashboard v3 - Gökhan Ustaosmanoğlu")

# Google Sheets bağlantısı
sheet_url = "https://docs.google.com/spreadsheets/d/1tOWiUugB7tWz5W-hWk-uBe7z1UG5QWAziJAFmzpPL7Y/export?format=csv&gid=1430833014"
df = pd.read_csv(sheet_url)
df.columns = df.columns.str.strip()

# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Ürün", len(df))
col2.metric("Fiyat Artışı", (df["Açıklama"] == "Fiyat Artışı Önerisi").sum())
col3.metric("İndirim / Kampanya", (df["Açıklama"] == "İndirim / Kampanya Önerisi").sum())
col4.metric("Muhtemel Promosyon", (df["Promosyon Notu"] == "Muhtemel Promosyon").sum())

st.markdown("---")
with st.expander("🔍 Filtrele"):
    colf1, colf2 = st.columns(2)
    secim_oneri = colf1.multiselect("Öneri Türü", options=df["Açıklama"].unique(), default=df["Açıklama"].unique())
    secim_promosyon = colf2.multiselect("Promosyon Notu", options=df["Promosyon Notu"].unique(), default=df["Promosyon Notu"].unique())

    colf3, colf4 = st.columns(2)
    qty_filter = colf3.slider("TW Qty. (Son Hafta Satış)", 0, int(df["TW Qty."].max()), (0, int(df["TW Qty."].max())))
    gmroi_filter = colf4.slider("GMROI", 0.0, float(df["TW GMROI"].max()), (0.0, float(df["TW GMROI"].max())))

# Filtrelenmiş veri
df_filtered = df[
    (df["Açıklama"].isin(secim_oneri)) &
    (df["Promosyon Notu"].isin(secim_promosyon)) &
    (df["TW Qty."].between(qty_filter[0], qty_filter[1])) &
    (df["TW GMROI"].between(gmroi_filter[0], gmroi_filter[1]))
]

st.subheader("📋 Aksiyon Ürünler")
st.dataframe(df_filtered, use_container_width=True)

st.markdown("### 📈 Görsel Analizler")
colg1, colg2 = st.columns(2)
fig1 = px.pie(df_filtered, names="Açıklama", title="Öneri Dağılımı")
colg1.plotly_chart(fig1, use_container_width=True)

if "Yeni Fiyat" in df.columns:
    fig2 = px.histogram(df_filtered, x="Yeni Fiyat", nbins=20, title="Yeni Fiyat Dağılımı")
    colg2.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("💾 CSV İndir")
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("📥 CSV Olarak İndir", data=csv, file_name="aksiyon_urunler.csv", mime="text/csv")
