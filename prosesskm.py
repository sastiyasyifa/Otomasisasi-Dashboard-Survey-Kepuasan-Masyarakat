import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# Nilai Per Unsur

def hitung_nilai_per_unsur(df):
    Nilai_Per_Unsur = []
    for col in df.columns[7:]:
        Jumlah = sum(df[col])
        Nilai_Per_Unsur.append(Jumlah)
    return Nilai_Per_Unsur

# NRR Per Unsur

def hitung_nrr_per_unsur(df):
    NRR_Per_Unsur = []
    for col in df.columns[7:]:
        Jumlah = np.mean(df[col])
        NRR_Per_Unsur.append(float(Jumlah))
    return NRR_Per_Unsur

# NRR Tertimbang

def hitung_nrr_tertimbang(NRR_Per_Unsur, df):
    NRR_Tertimbang = []
    for i in range(0, len(NRR_Per_Unsur)):
        Hasil = NRR_Per_Unsur[i] / (len(df.columns) - 7)
        NRR_Tertimbang.append(Hasil)
    return NRR_Tertimbang

# Nilai Konversi Per Unsur

def hitung_nilai_konversi_per_unsur(NRR_Per_Unsur):
    Nilai_Konversi_Per_Unsur = []
    for nilai in NRR_Per_Unsur:
        Hasil = nilai * 25
        Nilai_Konversi_Per_Unsur.append(Hasil)
    return Nilai_Konversi_Per_Unsur

# Mutu Pelayanan Per Unsur

def tentukan_mutu_pelayanan(Nilai_Konversi_Per_Unsur):
    Mutu_Pelayanan_Perunsur = []
    for nilai in Nilai_Konversi_Per_Unsur:
        if 25 < nilai < 64.99:
            Mutu_Pelayanan_Perunsur.append("D")
        elif 65 < nilai < 76.60:
            Mutu_Pelayanan_Perunsur.append("C")
        elif 76.61 < nilai < 88.30:
            Mutu_Pelayanan_Perunsur.append("B")
        elif 88.31 < nilai <= 100:
            Mutu_Pelayanan_Perunsur.append("A")
        else:
            Mutu_Pelayanan_Perunsur.append("-")
    return Mutu_Pelayanan_Perunsur

# Kinerja Unsur Pelayanan

def tentukan_kinerja_unsur(Mutu_Pelayanan_Perunsur):
    Kinerja_Unsur_Pelayanan = []
    for mutu in Mutu_Pelayanan_Perunsur:
        if mutu == "D":
            Kinerja_Unsur_Pelayanan.append("Kurang")
        elif mutu == "C":
            Kinerja_Unsur_Pelayanan.append("Cukup")
        elif mutu == "B":
            Kinerja_Unsur_Pelayanan.append("Baik")
        elif mutu == "A":
            Kinerja_Unsur_Pelayanan.append("Sangat Baik")
        else:
            Kinerja_Unsur_Pelayanan.append("-")
    return Kinerja_Unsur_Pelayanan


def tentukan_mutu(IKM_Unit_Pelayanan):
    if 25 < IKM_Unit_Pelayanan < 64.99:
        Mutu_Pelayanan = "D"
    elif 65 < IKM_Unit_Pelayanan < 76.60:
        Mutu_Pelayanan = "C"
    elif 76.61 < IKM_Unit_Pelayanan < 88.30:
        Mutu_Pelayanan = "B"
    elif 88.31 < IKM_Unit_Pelayanan < 100:
        Mutu_Pelayanan = "A"
    return Mutu_Pelayanan

def tentukan_kinerja(Mutu_Pelayanan):
    if Mutu_Pelayanan == "D":
        Kinerja_Pelayanan = "Kurang"
    elif Mutu_Pelayanan == "C":
        Kinerja_Pelayanan = "Cukup"
    elif Mutu_Pelayanan == "B":
        Kinerja_Pelayanan = "Baik"
    elif Mutu_Pelayanan == "A":
        Kinerja_Pelayanan = "Sangat Baik"
    return Kinerja_Pelayanan


# Gabungkan Semua ke DataFrame Baru

def buat_dataframe_hasil(df):
    Nilai_Per_Unsur = hitung_nilai_per_unsur(df)
    NRR_Per_Unsur = hitung_nrr_per_unsur(df)
    NRR_Tertimbang = hitung_nrr_tertimbang(NRR_Per_Unsur, df)
    Nilai_Konversi_Per_Unsur = hitung_nilai_konversi_per_unsur(NRR_Per_Unsur)
    Mutu_Pelayanan_Perunsur = tentukan_mutu_pelayanan(Nilai_Konversi_Per_Unsur)
    Kinerja_Unsur_Pelayanan = tentukan_kinerja_unsur(Mutu_Pelayanan_Perunsur)

    DF_baru = pd.DataFrame({
        'Unsur': df.columns[7:],
        'Nilai per unsur': Nilai_Per_Unsur,
        'NRR per unsur': NRR_Per_Unsur,
        'NRR tertimbang': NRR_Tertimbang,
        'Nilai Konversi Per Unsur': Nilai_Konversi_Per_Unsur,
        'Mutu pelayanan perunsur': Mutu_Pelayanan_Perunsur,
        'Kinerja unsur pelayanan': Kinerja_Unsur_Pelayanan
    })

    Jumlah_NRR_Tertimbang = sum(NRR_Tertimbang)
    IKM_Unit_Pelayanan = Jumlah_NRR_Tertimbang * 25
    Mutu_Pelayanan = tentukan_mutu(IKM_Unit_Pelayanan)
    Kinerja_Pelayanan = tentukan_kinerja(Mutu_Pelayanan)

    return DF_baru, Jumlah_NRR_Tertimbang, IKM_Unit_Pelayanan, Mutu_Pelayanan, Kinerja_Pelayanan, Nilai_Konversi_Per_Unsur

def grafik(df):
    JK_count = df["JENIS KELAMIN"].value_counts().reset_index()
    JK_count.columns = ["JENIS KELAMIN", "Jumlah"]

    fig_jk = px.pie(
        JK_count,
        values="Jumlah",
        names="JENIS KELAMIN",
        title="Jenis Kelamin",
        color_discrete_sequence=px.colors.qualitative.Set1,
        hole=0.35
    )
    fig_jk.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # USIA
    bins = [0, 20, 30, 40, 50, 100]
    labels = ["<20 tahun", "21-30 tahun", "31-40 tahun", "41-50 tahun", ">50 tahun"]

    df_usia = df.copy()

    df_usia["Kelompok Usia"] = pd.cut(df_usia["USIA"], bins=bins, labels=labels, right=True, include_lowest=True)

    usia_count = df_usia["Kelompok Usia"].value_counts().reset_index()
    usia_count.columns = ["Kelompok Usia", "Jumlah"]

    fig_usia = px.pie(
        usia_count,
        names="Kelompok Usia",
        values="Jumlah",
        title="Kelompok Usia",
        color="Kelompok Usia",
        color_discrete_sequence=px.colors.qualitative.Set1,
        hole=0.35
    )
    fig_usia.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # PENDIDIKAN
    Pendidikan_count = df["PENDIDIKAN"].value_counts().reset_index()
    Pendidikan_count.columns = ["PENDIDIKAN", "Jumlah"]

    fig_pd = px.pie(
        Pendidikan_count,
        values="Jumlah",
        names="PENDIDIKAN",
        title="Pendidikan",
        color="PENDIDIKAN",
        color_discrete_sequence=px.colors.qualitative.Set1,
        hole=0.35
    )
    fig_pd.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # PEKERJAAN
    df_Pekerjaan = df["PEKERJAAN"].value_counts().reset_index()
    df_Pekerjaan.columns = ["PEKERJAAN", "Jumlah"]
    df
    fig_pk = px.bar(
        df_Pekerjaan,
        x="PEKERJAAN",
        y="Jumlah",
        title="Pekerjaan",
        color="PEKERJAAN",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_pk.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    # JENIS LAYANAN
    df_JenisLayanan = df["JENIS LAYANAN"].value_counts().reset_index()
    df_JenisLayanan.columns = ["JENIS LAYANAN", "Jumlah"]
    fig_jl = px.bar(
        df_JenisLayanan,
        x="JENIS LAYANAN",
        y="Jumlah",
        title="Jenis Layanan",
        color="JENIS LAYANAN",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_jl.update_layout(title={'x': 0.5, 'xanchor': 'center'})

    return fig_jk, fig_usia, fig_pd, fig_pk, fig_jl

def korelasi_spearman(df, Nilai_Konversi_Per_Unsur):
    # Ambil kolom 8 sampai terakhir
    df_subset = df.iloc[:, 7:]

    # Hitung korelasi Spearman
    spearman_corr = df_subset.corr(method='spearman')

    # Label dan nilai
    labels = df_subset.columns
    values = Nilai_Konversi_Per_Unsur.copy()

    # Tutup lingkaran radar
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # --- Heatmap ---
    fig1, ax1 = plt.subplots(figsize=(6,6))
    sns.heatmap(spearman_corr, annot=True, cmap="bwr")
    ax1.set_title('Korelasi Spearman antar variabel unsur')

    # --- Radar chart ---
    fig2, ax2 = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax2.plot(angles, values, linewidth=2, color='blue')
    ax2.fill(angles, values, color='skyblue', alpha=0.4)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(labels)
    ax2.set_ylim(min(values)*0.9, max(values)*1.1)
    ax2.set_title("Grafik Radar Nilai Konversi/Unsur")

    # Kembalikan kedua figure
    return fig1, fig2

def signifikansi_pvalue(df):
    # Ambil kolom 8 sampai terakhir
    df_subset = df.iloc[:, 7:]

    # Inisialisasi matriks p-value
    pval_matrix = pd.DataFrame(index=df_subset.columns, columns=df_subset.columns)

    # Hitung p-value antar semua pasangan
    for col1 in df_subset.columns:
        for col2 in df_subset.columns:
            _, p = stats.spearmanr(df_subset[col1], df_subset[col2], nan_policy='omit')
            pval_matrix.loc[col1, col2] = p

    return pval_matrix.astype(float)