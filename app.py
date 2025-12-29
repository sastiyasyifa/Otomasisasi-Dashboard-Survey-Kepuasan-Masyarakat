import streamlit as st
import pandas as pd
from prosesskm import buat_dataframe_hasil,grafik, korelasi_spearman, signifikansi_pvalue

hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

st.set_page_config(page_title="SKM Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("📊 Dashboard Indeks Survei Kepuasan Masyarakat")

with open("template_file.xlsx", "rb") as file:
    file_data = file.read()

# Tombol download
st.download_button(
    label="📥 Download Template Excel SKM",
    data=file_data,
    file_name="template_file.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Upload file
filenames = []
uploaded_files = st.file_uploader("Upload Excel file")

if not uploaded_files:
    st.info(" Silakan unggah file Excel, format header harus sesuai template dan nilai yang diterima hanya dalam range 1-4", icon="ℹ️")
    st.stop()

else:
    try:
        st.subheader("DATA")
        df = pd.read_excel(uploaded_files, header=[0, 1])
        df.columns = [col[1] if "Unnamed" not in col[1] else col[0] for col in df.columns]
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Validasi awal (contoh: cek kolom penting)
        required_cols = ["JENIS KELAMIN", "USIA", "PENDIDIKAN", "PEKERJAAN", "JENIS LAYANAN"]
        for col in required_cols:
            if col not in df.columns:
                st.error(f"❌ Kolom '{col}' tidak ditemukan di file Excel. Pastikan format sesuai template!")
                st.stop()
            
        kolom_unsur = [col for col in df.columns[7:] if col.upper().startswith("U")]

        # Cek nilai kosong
        if df[kolom_unsur].isnull().any().any():
            st.error("⚠️ Terdapat nilai kosong pada kolom unsur! Mohon lengkapi data terlebih dahulu.")
        # Cek nilai di luar rentang 1–4
        elif (df[kolom_unsur] > 4).any().any() or (df[kolom_unsur] < 1).any().any():
            st.error("🚫 Ditemukan nilai di luar rentang 1–4! Pastikan semua nilai berada antara 1 sampai 4.")
            st.stop()
        else:
            st.divider()
            pilih_perhitungan = st.selectbox(
                "Pilih Perhitungan:",
                ["Perhitungan Global", "Perhitungan berdasarkan Jenis Layanan"]
            )
            st.divider()
                
            if pilih_perhitungan == "Perhitungan Global":
                try:
                    # hitung hasil
                    df_hasil, indeks_up, iup_konversi, mutu, kinerja, Nilai_Konversi_Per_Unsur = buat_dataframe_hasil(df)

                    st.subheader("📈 Hasil Perhitungan")
                    df_hasil.index = range(1, len(df_hasil) + 1)
                    st.dataframe(df_hasil, width='stretch', hide_index=True)

                    col = col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(label="Indeks Unit Pelayanan", value=round(indeks_up, 2))
                    with col2:
                        st.metric(label="Nilai Unit Pelayanan", value=round(iup_konversi, 2))
                    with col3:
                        st.metric(label="Mutu", value=(mutu))
                    with col4:
                        st.metric(label="Kinerja", value=(kinerja))

                    st.subheader("KARAKTERISTIK RESPONDEN")
                    fig_jk, fig_usia, fig_pd, fig_pk, fig_jl = grafik(df)
                    cols1, cols2, cols3 = st.columns(3)
                    with cols1:
                        st.plotly_chart(fig_jk)
                    with cols2:
                        st.plotly_chart(fig_usia)
                    with cols3:
                        st.plotly_chart(fig_pd)

                    cols4, cols5 = st.columns(2)
                    with cols4:
                        st.plotly_chart(fig_pk)
                    with cols5:
                        st.plotly_chart(fig_jl)

                    st.divider()
                    st.subheader("🔍 Analisis Signifikansi Antar Unsur (P-Value)")

                    pval_matrix = signifikansi_pvalue(df)
                    # Tambah warna otomatis: merah jika p < 0.05
                    styled_pval = pval_matrix.style.format("{:.4f}").applymap(
                        lambda v: "background-color: #ffcccc" if v > 0.05 else ""
                    )

                    st.dataframe(styled_pval, use_container_width=True)
                    st.divider()
                    
                    plt1, plt2 = korelasi_spearman(df, Nilai_Konversi_Per_Unsur)
                    cols6, cols7 = st.columns(2)
                    with cols6:
                        st.pyplot(plt1, width='stretch')
                    with cols7:
                        st.pyplot(plt2, width='stretch')

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat menghitung data: {e}")
                    st.stop()

            elif pilih_perhitungan == "Perhitungan berdasarkan Jenis Layanan":
                try:
                    pilih_jl = st.selectbox(
                        "Pilih Jenis Layanan:",
                        df["JENIS LAYANAN"].unique()
                    )
                    st.divider()

                    # Filter dataframe sesuai pilihan user
                    df_filtered = df[df["JENIS LAYANAN"] == pilih_jl]

                    st.write(f"### 📋 Data untuk Jenis Layanan: {pilih_jl}")
                    st.dataframe(df_filtered, use_container_width=True, hide_index=True)

                    # Lakukan perhitungan hanya pada data terpilih
                    df_hasil, indeks_up, iup_konversi, mutu, kinerja, Nilai_Konversi_Per_Unsur = buat_dataframe_hasil(df_filtered)

                    # --- Tampilkan hasil perhitungan ---
                    st.subheader("📈 Hasil Perhitungan")
                    st.dataframe(df_hasil, use_container_width=True, hide_index=True)

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(label="Indeks Unit Pelayanan", value=round(indeks_up, 4))
                    with col2:
                        st.metric(label="Nilai Unit Pelayanan", value=round(iup_konversi, 4))
                    with col3:
                        st.metric(label="Mutu Pelayanan", value=mutu)
                    with col4:
                        st.metric(label="Kinerja Pelayanan", value=kinerja)

                    # --- Tampilkan grafik ---
                    st.subheader("📊 Kriteria Responden")
                    fig_jk, fig_usia, fig_pd, fig_pk, fig_jl = grafik(df_filtered)

                    cols1, cols2, cols3 = st.columns(3)
                    with cols1:
                        st.plotly_chart(fig_jk)
                    with cols2:
                        st.plotly_chart(fig_usia)
                    with cols3:
                        st.plotly_chart(fig_pd)

                    cols4, cols5 = st.columns(2)
                    with cols4:
                        st.plotly_chart(fig_pk)
                    with cols5:
                        st.plotly_chart(fig_jl)

                    st.divider()
                    st.subheader("🔍 Analisis Signifikansi Antar Unsur (P-Value)")

                    pval_matrix = signifikansi_pvalue(df_filtered)
                    # Tambah warna otomatis: merah jika p < 0.05
                    styled_pval = pval_matrix.style.format("{:.4f}").applymap(
                        lambda v: "background-color: #ffcccc" if v > 0.05 else ""
                    )

                    st.dataframe(styled_pval, use_container_width=True)

                    plt1, plt2 = korelasi_spearman(df_filtered, Nilai_Konversi_Per_Unsur)
                    cols6, cols7 = st.columns(2)
                    with cols6:
                        st.pyplot(plt1, width='stretch')
                    with cols7:
                        st.pyplot(plt2, width='stretch')

                except Exception as e:
                    st.error(f"⚠️ Terjadi kesalahan saat memproses data berdasarkan jenis layanan: {e}")
                    st.stop()
    except Exception as e:
        st.error(f"🚫 File tidak sesuai format! Pastikan header, urutan kolom, dan nilai sesuai template.\n\n**Detail error:** {e}")

        st.stop()
