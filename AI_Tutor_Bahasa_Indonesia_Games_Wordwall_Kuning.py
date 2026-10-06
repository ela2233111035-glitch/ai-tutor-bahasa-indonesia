import os
import re
import random
from collections import Counter
from difflib import SequenceMatcher

import streamlit as st


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# KONFIGURASI
# =========================================================

APP_NAME = "AI Tutor Bahasa Indonesia"

FOLDER_DATABASE = "database"

# =========================================================
# LINK GAMES DAN LKPD
# =========================================================

WORDWALL_URL = "https://wordwall.net/resource/120671874?wwmethod=link"

LKPD_URL = "https://forms.gle/ZrQU4CSB46PJNT9Z6"

# Video Ice Breaking
# URL video dapat diganti kapan saja tanpa mengubah bagian lain program.
YOUTUBE_ICE_BREAKING_URL = "https://youtu.be/A1HUh8FMCpE"


# =========================================================
# KONFIGURASI OPENAI
# =========================================================
#
# Jika ingin menggunakan AI:
#
# Windows CMD:
#
# set OPENAI_API_KEY=API_KEY_ANDA
#
# atau gunakan .streamlit/secrets.toml:
#
# OPENAI_API_KEY = "API_KEY_ANDA"
#
# Model dapat diubah melalui:
#
# OPENAI_MODEL=gpt-4o-mini
#
# =========================================================

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #fff9d9;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* ================================
       HERO
    ================================= */

    .hero {
        padding: 35px;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );
        color: white;
        margin-bottom: 25px;
        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.20);
    }

    .hero h1 {
        font-size: 40px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.95;
    }


    /* ================================
       CARD
    ================================= */

    .card {
        padding: 22px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.05);
    }


    /* ================================
       FEATURE
    ================================= */

    .feature-card {
        padding: 22px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e5e7eb;
        min-height: 170px;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.05);
    }


    /* ================================
       INFO
    ================================= */

    .info-card {
        padding: 20px;
        border-radius: 18px;
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        margin-bottom: 20px;
    }


    /* ================================
       SUCCESS
    ================================= */

    .success-card {
        padding: 20px;
        border-radius: 18px;
        background: #ecfdf5;
        border: 1px solid #10b981;
        margin-bottom: 15px;
    }


    /* ================================
       WARNING
    ================================= */

    .warning-card {
        padding: 20px;
        border-radius: 18px;
        background: #fffbeb;
        border: 1px solid #f59e0b;
        margin-bottom: 15px;
    }


    /* ================================
       CHAT
    ================================= */

    .chat-question {
        padding: 18px;
        border-radius: 15px;
        background: #eef2ff;
        border: 1px solid #c7d2fe;
        margin-bottom: 15px;
    }

    .chat-answer {
        padding: 20px;
        border-radius: 15px;
        background: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.04);
    }


    /* ================================
       SOURCE
    ================================= */

    .source-card {
        padding: 15px;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }


    /* ================================
       CP
    ================================= */

    .cp-card {
        padding: 22px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #e5e7eb;
        border-left: 6px solid #2563eb;
        margin-bottom: 18px;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.05);
    }

    .cp-card h3 {
        margin-top: 0;
        color: #1d4ed8;
    }


    /* ================================
       TP
    ================================= */

    .tp-card {
        padding: 22px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow:
            0 3px 12px rgba(0, 0, 0, 0.05);
    }

    .tp-card h3 {
        margin-top: 0;
        color: #1d4ed8;
    }


    /* ================================
       EXTERNAL LINK
    ================================= */

    .external-card {
        padding: 40px;
        border-radius: 24px;
        background: white;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.06);
    }

    .external-icon {
        font-size: 70px;
        margin-bottom: 10px;
    }

    .external-card h2 {
        margin-bottom: 10px;
    }


    /* ================================
       SCORE
    ================================= */

    .score {
        font-size: 42px;
        font-weight: bold;
        color: #2563eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "halaman": "Beranda",
    "nama_pelajar": "",
    "kelas": "",
    "skor_evaluasi": None,
    "jawaban_evaluasi": {},
    "game_soal": None,
    "riwayat_ai": []
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# MENU
# =========================================================

MENU = [
    "Beranda",
    "Profil Pelajar Pancasila",
    "CP dan ATP",
    "AI Tutor",
    "Ice Breaking",
    "Materi",
    "Games",
    "LKPD",
    "Evaluasi"
]


# =========================================================
# DATABASE
# =========================================================

@st.cache_data
def baca_database():

    data = []

    if not os.path.exists(FOLDER_DATABASE):

        os.makedirs(
            FOLDER_DATABASE,
            exist_ok=True
        )

    for nama_file in sorted(
        os.listdir(FOLDER_DATABASE)
    ):

        if not nama_file.lower().endswith(".txt"):

            continue

        lokasi_file = os.path.join(
            FOLDER_DATABASE,
            nama_file
        )

        try:

            with open(
                lokasi_file,
                "r",
                encoding="utf-8-sig"
            ) as file:

                isi = file.read()

            if isi.strip():

                data.append(
                    {
                        "nama_file": nama_file,
                        "isi": isi.strip()
                    }
                )

        except Exception as error:

            st.error(
                f"Gagal membaca {nama_file}: {error}"
            )

    return data


database = baca_database()


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS = {
    "yang",
    "dan",
    "atau",
    "di",
    "ke",
    "dari",
    "pada",
    "dengan",
    "untuk",
    "dalam",
    "adalah",
    "itu",
    "ini",
    "apa",
    "bagaimana",
    "mengapa",
    "siapa",
    "kapan",
    "sebutkan",
    "jelaskan",
    "jelaskanlah",
    "tentang",
    "suatu",
    "sebuah",
    "secara",
    "merupakan",
    "dapat",
    "akan",
    "sebagai",
    "oleh",
    "lebih",
    "juga",
    "tidak",
    "tersebut",
    "cara",
    "agar",
    "buat",
    "membuat",
    "contoh",
    "berikan",
    "berikut",
    "yaitu",
    "yakni",
    "saja",
    "terdiri",
    "apa",
    "fungsi",
    "pengertian"
}


# =========================================================
# TEXT PROCESSING
# =========================================================

def bersihkan_teks(teks):

    if not teks:

        return ""

    teks = teks.lower()

    teks = re.sub(
        r"[^a-zA-ZÀ-ÿ0-9\s]",
        " ",
        teks
    )

    teks = re.sub(
        r"\s+",
        " ",
        teks
    )

    return teks.strip()


def tokenisasi(teks):

    teks = bersihkan_teks(teks)

    if not teks:

        return []

    return teks.split()


def ambil_kata_kunci(pertanyaan):

    tokens = tokenisasi(
        pertanyaan
    )

    hasil = []

    for kata in tokens:

        if (
            len(kata) >= 3
            and kata not in STOPWORDS
        ):

            hasil.append(kata)

    return hasil


# =========================================================
# CHUNK DATABASE
# =========================================================

def pecah_materi(
    nama_file,
    isi,
    ukuran=1200
):

    paragraf = re.split(
        r"\n\s*\n",
        isi
    )

    hasil = []

    buffer = ""

    nomor = 1

    for paragraf_item in paragraf:

        paragraf_item = (
            paragraf_item.strip()
        )

        if not paragraf_item:

            continue

        if (
            len(buffer)
            + len(paragraf_item)
            + 2
            <= ukuran
        ):

            if buffer:

                buffer += (
                    "\n\n"
                    + paragraf_item
                )

            else:

                buffer = paragraf_item

        else:

            if buffer:

                hasil.append(
                    {
                        "nama_file": nama_file,
                        "nomor": nomor,
                        "isi": buffer
                    }
                )

                nomor += 1

            buffer = paragraf_item

    if buffer:

        hasil.append(
            {
                "nama_file": nama_file,
                "nomor": nomor,
                "isi": buffer
            }
        )

    if not hasil and isi.strip():

        hasil.append(
            {
                "nama_file": nama_file,
                "nomor": 1,
                "isi": isi[:ukuran]
            }
        )

    return hasil


@st.cache_data
def buat_chunks_database(database_data):

    semua_chunk = []

    for data in database_data:

        semua_chunk.extend(
            pecah_materi(
                data["nama_file"],
                data["isi"]
            )
        )

    return semua_chunk


chunks_database = buat_chunks_database(
    database
)


# =========================================================
# SCORING RELEVANSI
# =========================================================

def skor_chunk(
    pertanyaan,
    chunk
):

    pertanyaan_bersih = bersihkan_teks(
        pertanyaan
    )

    isi_bersih = bersihkan_teks(
        chunk["isi"]
    )

    nama_bersih = bersihkan_teks(
        chunk["nama_file"]
    )

    if not pertanyaan_bersih:

        return 0

    skor = 0

    kata_kunci = ambil_kata_kunci(
        pertanyaan
    )

    isi_tokens = tokenisasi(
        isi_bersih
    )

    frekuensi = Counter(
        isi_tokens
    )

    # =====================================================
    # 1. KECOCOKAN FRASA
    # =====================================================

    if (
        len(pertanyaan_bersih) >= 8
        and pertanyaan_bersih in isi_bersih
    ):

        skor += 150


    # =====================================================
    # 2. KATA KUNCI
    # =====================================================

    for kata in kata_kunci:

        jumlah = frekuensi.get(
            kata,
            0
        )

        jumlah = min(
            jumlah,
            5
        )

        skor += jumlah * 10


    # =====================================================
    # 3. KATA KUNCI ADA DI NAMA FILE
    # =====================================================

    for kata in kata_kunci:

        if kata in nama_bersih:

            skor += 30


    # =====================================================
    # 4. COVERAGE
    # =====================================================

    if kata_kunci:

        jumlah_cocok = 0

        for kata in kata_kunci:

            if kata in isi_bersih:

                jumlah_cocok += 1

        coverage = (
            jumlah_cocok
            / len(kata_kunci)
        )

        skor += int(
            coverage * 100
        )


    # =====================================================
    # 5. KEMIRIPAN TEKS
    # =====================================================

    potongan = isi_bersih[:1000]

    similarity = SequenceMatcher(
        None,
        pertanyaan_bersih,
        potongan
    ).ratio()

    skor += int(
        similarity * 30
    )


    return skor


# =========================================================
# CARI MATERI RELEVAN
# =========================================================

def cari_materi_relevan(
    pertanyaan,
    database_chunks,
    jumlah=8
):

    hasil = []

    for chunk in database_chunks:

        skor = skor_chunk(
            pertanyaan,
            chunk
        )

        if skor > 0:

            item = dict(chunk)

            item["skor"] = skor

            hasil.append(
                item
            )

    hasil.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return hasil[:jumlah]


# =========================================================
# CONTEXT AI
# =========================================================

def buat_context_ai(
    hasil,
    batas_karakter=14000
):

    if not hasil:

        return ""

    context = ""

    for nomor, item in enumerate(
        hasil,
        start=1
    ):

        bagian = (
            "\n\n"
            f"===== SUMBER {nomor} =====\n"
            f"Nama file: {item['nama_file']}\n"
            f"Bagian: {item['nomor']}\n"
            "Isi materi:\n"
            f"{item['isi']}\n"
            f"===== AKHIR SUMBER {nomor} =====\n"
        )

        if (
            len(context)
            + len(bagian)
            <= batas_karakter
        ):

            context += bagian

        else:

            sisa = (
                batas_karakter
                - len(context)
            )

            if sisa > 300:

                context += bagian[:sisa]

            break

    return context.strip()


# =========================================================
# OPENAI API KEY
# =========================================================

def ambil_api_key():

    try:

        if "OPENAI_API_KEY" in st.secrets:

            return st.secrets[
                "OPENAI_API_KEY"
            ]

    except Exception:

        pass

    return os.getenv(
        "OPENAI_API_KEY",
        ""
    )


# =========================================================
# CEK OPENAI
# =========================================================

def openai_tersedia():

    api_key = ambil_api_key()

    if not api_key:

        return False

    try:

        import openai

        return True

    except ImportError:

        return False


# =========================================================
# BUAT JAWABAN AI
# =========================================================

def buat_jawaban_ai(
    pertanyaan,
    context
):

    api_key = ambil_api_key()

    if not api_key:

        return None, (
            "OPENAI_API_KEY belum diatur."
        )

    try:

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key
        )

        instruksi = """
Anda adalah AI Tutor Bahasa Indonesia.

Tugas Anda adalah menjawab pertanyaan peserta
didik SECARA TEPAT sesuai dengan pertanyaan.

Gunakan materi Knowledge Base sebagai sumber utama.

ATURAN:

1. Pahami terlebih dahulu maksud pertanyaan.
2. Jawaban harus langsung menjawab pertanyaan.
3. Jangan menjawab topik lain.
4. Jangan memasukkan informasi yang tidak berkaitan.
5. Gunakan Knowledge Base sebagai sumber utama.
6. Jika informasi tersedia di Knowledge Base,
   gunakan informasi tersebut.
7. Jika beberapa bagian materi relevan,
   gabungkan informasi tersebut.
8. Jika pertanyaan meminta "sebutkan",
   gunakan daftar bernomor atau bullet.
9. Jika pertanyaan meminta "jelaskan",
   berikan penjelasan yang cukup.
10. Jika pertanyaan meminta "apa pengertian",
    berikan definisi terlebih dahulu.
11. Jika pertanyaan meminta "fungsi",
    fokus pada fungsi.
12. Jika pertanyaan meminta "struktur",
    fokus pada struktur.
13. Jika pertanyaan meminta "ciri-ciri",
    fokus pada ciri-ciri.
14. Jika pertanyaan meminta "contoh",
    berikan contoh yang relevan.
15. Jangan mengulang pertanyaan pengguna.
16. Gunakan Bahasa Indonesia yang mudah dipahami.
17. Jangan menyebut "database internal".
18. Jangan mengatakan "berdasarkan sumber di atas"
    secara berulang.
19. Jika jawaban tidak tersedia dalam materi,
    katakan:
    "Maaf, informasi tersebut belum ditemukan
    dalam materi yang tersedia."
20. Jangan mengarang fakta yang tidak terdapat
    dalam materi.

FORMAT:

Jawab langsung.

Gunakan:
- paragraf untuk penjelasan;
- bullet point untuk daftar;
- nomor untuk langkah atau urutan;
- contoh jika memang diminta.
"""

        prompt = f"""
PERTANYAAN PESERTA DIDIK:

{pertanyaan}

KNOWLEDGE BASE:

{context}

INSTRUKSI:

Jawab hanya pertanyaan peserta didik.

Pastikan jawaban benar-benar sesuai
dengan maksud pertanyaan.
"""

        response = client.responses.create(
            model=OPENAI_MODEL,
            instructions=instruksi,
            input=prompt
        )

        jawaban = response.output_text

        if not jawaban:

            return None, (
                "AI tidak memberikan jawaban."
            )

        return (
            jawaban.strip(),
            None
        )

    except Exception as error:

        return None, str(error)


# =========================================================
# FALLBACK DATABASE
# =========================================================

def jawaban_dari_database(
    pertanyaan,
    hasil
):

    if not hasil:

        return (
            "Maaf, materi yang berkaitan dengan "
            "pertanyaan Anda belum ditemukan "
            "di dalam database."
        )

    kata_kunci = ambil_kata_kunci(
        pertanyaan
    )

    kalimat_relevan = []

    for item in hasil:

        isi = item["isi"]

        kalimat = re.split(
            r"(?<=[.!?])\s+",
            isi
        )

        for kal in kalimat:

            kal_bersih = bersihkan_teks(
                kal
            )

            if not kal_bersih:

                continue

            cocok = 0

            for kata in kata_kunci:

                if kata in kal_bersih:

                    cocok += 1

            if cocok > 0:

                kalimat_relevan.append(
                    (
                        cocok,
                        kal.strip()
                    )
                )

    if kalimat_relevan:

        kalimat_relevan.sort(
            key=lambda x: x[0],
            reverse=True
        )

        hasil_teks = []

        sudah = set()

        for _, kalimat in kalimat_relevan:

            kunci = bersihkan_teks(
                kalimat
            )

            if kunci in sudah:

                continue

            sudah.add(kunci)

            hasil_teks.append(
                kalimat
            )

            if len(hasil_teks) >= 6:

                break

        if hasil_teks:

            return "\n\n".join(
                hasil_teks
            )

    return (
        hasil[0]["isi"]
    )


# =========================================================
# FUNGSI PINDAH HALAMAN
# =========================================================

def pindah_halaman(
    nama_halaman
):

    st.session_state.halaman = (
        nama_halaman
    )



# =========================================================
# ULTIMATE 2.0 — MODERN EDTECH UI
# =========================================================

# ---------- Extra session state ----------
extra_defaults = {
    "xp": 0,
    "streak": 1,
    "badges": [],
    "materi_dibaca": [],
    "aktivitas_selesai": [],
    "ai_questions": 0,
    "challenge_best": 0,
    "procedure_mode": "Susun Langkah",
    "procedure_score": 0,
    "procedure_lives": 3,
    "procedure_best": 0,
    "procedure_completed": [],
    "procedure_round": 0,
}
for key, value in extra_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Nunito:wght@400;600;700;800;900&display=swap');

:root{
    --primary:#2563eb;
    --primary2:#7c3aed;
    --cyan:#0891b2;
    --pink:#db2777;
    --purple:#7c3aed;
    --yellow:#d97706;
    --green:#059669;
    --text:#172033;
    --muted:#526078;
    --soft:#f5f7fb;
    --card:#ffffff;
    --border:#dbe2ee;
}

html,body,[class*="css"]{
    font-family:'Nunito',sans-serif;
    color:var(--text)!important;
}

.stApp{
    background:
        radial-gradient(circle at 5% 5%,rgba(37,99,235,.08),transparent 22%),
        radial-gradient(circle at 95% 8%,rgba(124,58,237,.07),transparent 23%),
        linear-gradient(135deg,#f8fbff 0%,#f7f7ff 50%,#fff9fc 100%);
    color:var(--text)!important;
}

.stApp:before{
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    opacity:.18;
    background-image:radial-gradient(rgba(37,99,235,.18) 1px,transparent 1px);
    background-size:42px 42px;
}

.block-container{
    max-width:1450px;
    padding-top:1.2rem;
    padding-bottom:4rem;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#ffffff 0%,#f4f7ff 100%);
    border-right:1px solid #d9e1ef;
    box-shadow:8px 0 28px rgba(31,41,55,.06);
}

section[data-testid="stSidebar"] *{
    color:var(--text)!important;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] small{
    color:#64748b!important;
}

h1,h2,h3,h4{
    font-family:'Baloo 2',sans-serif!important;
    color:#172033!important;
}

p,span,li,label{
    color:inherit;
}

.hero{
    position:relative;
    overflow:hidden;
    padding:30px 34px;
    border-radius:30px;
    border:1px solid #d7e3fb;
    background:
        radial-gradient(circle at 88% 15%,rgba(219,39,119,.15),transparent 25%),
        radial-gradient(circle at 12% 80%,rgba(8,145,178,.12),transparent 30%),
        linear-gradient(135deg,#eaf3ff 0%,#f4efff 55%,#fff1f7 100%);
    box-shadow:0 18px 50px rgba(37,99,235,.10);
    margin-bottom:22px;
}

.hero:after{
    content:"✦  ✧  ·  ✦  ·  ✧";
    position:absolute;
    right:30px;
    top:18px;
    color:rgba(37,99,235,.22);
    font-size:26px;
    letter-spacing:12px;
}

.hero-title{
    font-size:clamp(2.3rem,5vw,4.5rem);
    font-weight:900;
    line-height:.95;
    background:linear-gradient(90deg,#1d4ed8,#7c3aed,#be185d);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent!important;
}

.hero-sub{
    color:#40506a!important;
    font-size:1.05rem;
    max-width:800px;
    margin-top:12px;
}

.badges{
    display:flex;
    gap:9px;
    flex-wrap:wrap;
    margin-top:18px;
}

.badge{
    display:inline-flex;
    padding:8px 13px;
    border-radius:999px;
    background:#ffffff;
    border:1px solid #d5deed;
    color:#24324a!important;
    font-weight:800;
    font-size:.82rem;
    box-shadow:0 3px 10px rgba(31,41,55,.05);
}

.wordwall-card{min-height:170px;padding:24px;border-radius:24px;background:linear-gradient(135deg,#ffffff 0%,#fffdf2 52%,#fff1f7 100%);border:3px solid #ffffff;box-shadow:0 14px 34px rgba(120,90,20,.12);display:flex;gap:18px;align-items:center;margin-bottom:12px}
.wordwall-art{width:92px;height:92px;min-width:92px;display:flex;align-items:center;justify-content:center;border-radius:28px;background:linear-gradient(135deg,#fde68a,#fbcfe8);font-size:3.1rem;box-shadow:0 8px 22px rgba(245,158,11,.15)}
.wordwall-card h2{margin:3px 0 8px;color:#713f12!important}
.wordwall-card p,.wordwall-preview p{color:#4b5563!important}
.wordwall-preview{min-height:170px;padding:24px;border-radius:24px;background:linear-gradient(135deg,#fff7c2,#ecfccb);border:3px solid #ffffff;box-shadow:0 14px 34px rgba(120,90,20,.10)}
.preview-icon{font-size:2.8rem;margin-bottom:6px}
.wordwall-preview h3{color:#365314!important;margin:5px 0 8px}

.section{
    font-family:'Baloo 2',sans-serif;
    color:#172033!important;
    font-size:2rem;
    font-weight:800;
    margin:26px 0 13px;
}

.card{
    background:#ffffff;
    color:#172033!important;
    border:1px solid #dbe2ee;
    border-radius:24px;
    padding:22px;
    box-shadow:0 10px 30px rgba(31,41,55,.07);
    height:100%;
}

.card p,.card span,.card li{
    color:#40506a;
}

.feature{
    position:relative;
    overflow:hidden;
    min-height:180px;
    padding:23px;
    border-radius:26px;
    border:1px solid #dbe2ee;
    background:linear-gradient(145deg,#ffffff,#f6f9ff);
    box-shadow:0 12px 32px rgba(31,41,55,.07);
}

.feature .emoji{font-size:2.5rem}
.feature h3{margin:8px 0 5px;font-size:1.4rem;color:#172033!important}
.feature p{color:#526078!important;margin:0}
.feature:after{
    content:"";
    position:absolute;
    width:110px;
    height:110px;
    border-radius:50%;
    right:-30px;
    bottom:-40px;
    background:radial-gradient(circle,rgba(37,99,235,.10),transparent 68%);
}

.stat{
    padding:18px;
    border-radius:20px;
    background:#ffffff;
    border:1px solid #dbe2ee;
    box-shadow:0 8px 24px rgba(31,41,55,.06);
}

.stat .big{
    font-size:2rem;
    font-weight:900;
    font-family:'Baloo 2';
    color:#172033!important;
}

.stat .label{
    color:#526078!important;
    font-size:.85rem;
    font-weight:700;
}

.xpbar{
    height:13px;
    background:#e8edf5;
    border-radius:99px;
    overflow:hidden;
    margin:9px 0;
}

.xpfill{
    height:100%;
    border-radius:99px;
    background:linear-gradient(90deg,#0891b2,#7c3aed,#db2777);
}

.road{
    display:flex;
    align-items:center;
    gap:10px;
    overflow-x:auto;
    padding:16px 4px 22px;
}

.node{
    min-width:145px;
    text-align:center;
    padding:18px 12px;
    border-radius:22px;
    background:#ffffff;
    border:1px solid #dbe2ee;
    color:#172033!important;
    box-shadow:0 6px 18px rgba(31,41,55,.05);
}

.node.active{
    background:linear-gradient(145deg,#eff6ff,#f5f3ff);
    border-color:#93c5fd;
}

.node.done{
    background:#ecfdf5;
    border-color:#86efac;
}

.node .ico{font-size:2rem}
.node .small{font-size:.78rem;color:#64748b!important;font-weight:800}
.arrow{font-size:1.5rem;color:#94a3b8!important}

.chat-user,.chat-ai{
    padding:18px 20px;
    border-radius:22px;
    margin:10px 0;
    border:1px solid #dbe2ee;
    color:#172033!important;
}

.chat-user{
    background:linear-gradient(145deg,#eff6ff,#f5f3ff);
}

.chat-ai{
    background:linear-gradient(145deg,#fff1f7,#f5f3ff);
}

.ai-avatar{
    display:inline-flex;
    width:52px;
    height:52px;
    border-radius:17px;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#0891b2,#7c3aed,#db2777);
    font-size:1.8rem;
    box-shadow:0 10px 30px rgba(37,99,235,.16);
}

.challenge{
    padding:28px;
    border-radius:28px;
    background:linear-gradient(145deg,#f5f3ff,#eff6ff);
    color:#172033!important;
    border:1px solid #ddd6fe;
    box-shadow:0 16px 40px rgba(31,41,55,.08);
}

.challenge p,.challenge span{
    color:#526078!important;
}

.question{
    padding:20px;
    border-radius:22px;
    background:#ffffff;
    color:#172033!important;
    border:1px solid #dbe2ee;
    margin:14px 0;
    box-shadow:0 6px 18px rgba(31,41,55,.05);
}

.question span{
    color:#172033!important;
}

.badge-card{
    text-align:center;
    padding:22px 14px;
    border-radius:22px;
    background:#ffffff;
    border:1px solid #dbe2ee;
    height:100%;
    box-shadow:0 8px 24px rgba(31,41,55,.06);
}

.badge-card .medal{font-size:2.8rem}
.badge-locked{filter:grayscale(1);opacity:.48}

.info{
    padding:18px 20px;
    border-left:4px solid #0891b2;
    border-radius:16px;
    background:#ecfeff;
    color:#164e63!important;
}

.footer{
    text-align:center;
    color:#64748b!important;
    padding:30px 0 10px;
}

.footer b,.footer span{
    color:#526078!important;
}

div.stButton>button{
    border-radius:15px!important;
    border:1px solid #cbd5e1!important;
    background:linear-gradient(135deg,#eff6ff,#f5f3ff)!important;
    color:#1e3a8a!important;
    font-weight:800!important;
    min-height:44px;
    box-shadow:0 4px 12px rgba(31,41,55,.05);
}

div.stButton>button:hover{
    border-color:#60a5fa!important;
    color:#1d4ed8!important;
    transform:translateY(-1px);
    box-shadow:0 7px 18px rgba(37,99,235,.12);
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]>div{
    background:#ffffff!important;
    color:#172033!important;
    border:1px solid #cbd5e1!important;
    border-radius:14px!important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder{
    color:#94a3b8!important;
}

.stSelectbox div[data-baseweb="select"] span{
    color:#172033!important;
}

.stRadio label,.stCheckbox label{
    color:#172033!important;
}

.stRadio [data-testid="stMarkdownContainer"] p{
    color:#172033!important;
}

[data-testid="stMetric"]{
    background:#ffffff;
    padding:14px;
    border-radius:18px;
    border:1px solid #dbe2ee;
    box-shadow:0 6px 18px rgba(31,41,55,.05);
}

[data-testid="stMetric"] *{
    color:#172033!important;
}

.stAlert{
    color:#172033!important;
}

.stAlert *{
    color:inherit!important;
}

[data-testid="stExpander"]{
    background:#ffffff;
    border:1px solid #dbe2ee;
    border-radius:16px;
}

[data-testid="stExpander"] *{
    color:#172033!important;
}

div[data-baseweb="popover"] *{
    color:#172033!important;
}

div[data-baseweb="menu"]{
    background:#ffffff!important;
}

div[data-baseweb="menu"] *{
    color:#172033!important;
}

.stMarkdown, .stText, .stCaption{
    color:#172033;
}

@media(max-width:800px){
    .hero{padding:24px 20px;border-radius:22px}
    .feature{min-height:auto}
    .hero-title{font-size:2.4rem}
    .section{font-size:1.65rem}
}
/* =========================================================
   COLORFUL EDTECH 4.0 - VISUAL OVERRIDES
   ========================================================= */
:root{
    --pink2:#f472b6;
    --blue2:#38bdf8;
    --violet2:#a78bfa;
    --orange2:#fb923c;
    --yellow2:#facc15;
    --mint2:#34d399;
    --ink:#172033;
}

.stApp{
    background:
        radial-gradient(circle at 5% 10%,rgba(255,255,255,.82),transparent 22%),
        radial-gradient(circle at 95% 12%,rgba(255,229,120,.42),transparent 24%),
        radial-gradient(circle at 78% 88%,rgba(255,182,193,.18),transparent 25%),
        radial-gradient(circle at 12% 90%,rgba(167,243,208,.20),transparent 22%),
        linear-gradient(135deg,#fff9d9 0%,#fff5bd 48%,#fffbe8 100%)!important;
}

.hero{
    min-height:260px;
    background:
        radial-gradient(circle at 86% 18%,rgba(255,255,255,.75),transparent 16%),
        radial-gradient(circle at 72% 72%,rgba(251,146,60,.20),transparent 20%),
        radial-gradient(circle at 18% 80%,rgba(52,211,153,.18),transparent 24%),
        linear-gradient(120deg,#dff7ff 0%,#eee8ff 45%,#ffe4f1 72%,#fff3cf 100%)!important;
    border:2px solid rgba(255,255,255,.90)!important;
    box-shadow:0 22px 60px rgba(99,102,241,.13)!important;
}

.hero:before{
    content:"📚  ✏️  ⭐  🎨  🧠  🚀";
    position:absolute;
    right:24px;
    bottom:18px;
    font-size:2rem;
    letter-spacing:8px;
    opacity:.72;
    transform:rotate(-4deg);
}

.card,.feature,.stat,.badge-card,.question,.challenge,.info{
    border:2px solid rgba(255,255,255,.96)!important;
    box-shadow:0 14px 35px rgba(71,85,105,.10)!important;
}

.card{
    background:linear-gradient(145deg,#ffffff 0%,#f7fbff 100%)!important;
}

.feature{
    background:linear-gradient(145deg,#ffffff 0%,#fff8fd 50%,#f2faff 100%)!important;
    transition:transform .2s ease,box-shadow .2s ease;
}
.feature:hover,.card:hover,.stat:hover,.badge-card:hover{
    transform:translateY(-4px);
    box-shadow:0 20px 42px rgba(71,85,105,.16)!important;
}

.feature .emoji{
    display:inline-flex;
    width:70px;height:70px;
    align-items:center;justify-content:center;
    border-radius:24px;
    background:linear-gradient(135deg,#e0f7ff,#f0e8ff,#ffe4f1);
    font-size:2.5rem;
    box-shadow:0 8px 20px rgba(99,102,241,.12);
}

.feature:nth-child(3n+1) .emoji{background:linear-gradient(135deg,#dff7ff,#dff2ff)}
.feature:nth-child(3n+2) .emoji{background:linear-gradient(135deg,#f2e8ff,#ffe4f1)}
.feature:nth-child(3n) .emoji{background:linear-gradient(135deg,#fff2c7,#dcfce7)}

.badge{
    background:linear-gradient(135deg,#ffffff,#f5f3ff)!important;
    border:1px solid #d8dff0!important;
    color:#24324a!important;
}

.section{
    display:inline-block;
    padding:7px 16px;
    border-radius:999px;
    background:linear-gradient(90deg,#e0f2fe,#ede9fe,#fce7f3);
    color:#24324a!important;
    box-shadow:0 5px 16px rgba(99,102,241,.08);
}

.stat{
    background:linear-gradient(145deg,#ffffff,#f6faff)!important;
}

.stat .big{
    background:linear-gradient(90deg,#2563eb,#7c3aed,#db2777);
    -webkit-background-clip:text;background-clip:text;color:transparent!important;
}

.xpbar{background:#e8edf7!important}
.xpfill{background:linear-gradient(90deg,#38bdf8,#6366f1,#ec4899,#f59e0b)!important}

.road .node{
    background:linear-gradient(145deg,#ffffff,#f8faff)!important;
    border:2px solid #e1e7f2!important;
}
.road .node.active{
    background:linear-gradient(145deg,#e0f7ff,#ede9fe,#ffe4f1)!important;
    border-color:#a5b4fc!important;
}

.challenge{
    background:linear-gradient(135deg,#e0f7ff 0%,#ede9fe 42%,#ffe4f1 75%,#fff4cf 100%)!important;
}

.question{background:linear-gradient(145deg,#ffffff,#f8fbff)!important}

.info{
    background:linear-gradient(90deg,#ecfeff,#f5f3ff)!important;
    border-left:6px solid #6366f1!important;
}

.chat-user{background:linear-gradient(135deg,#e0f7ff,#eef6ff)!important}
.chat-ai{background:linear-gradient(135deg,#fce7f3,#f3e8ff)!important}

.ai-avatar{
    width:76px!important;height:76px!important;
    border-radius:26px!important;
    background:linear-gradient(135deg,#38bdf8,#8b5cf6,#ec4899)!important;
    box-shadow:0 12px 28px rgba(99,102,241,.22)!important;
}

/* Sidebar dibuat seperti menu aplikasi edukasi */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#ffffff 0%,#eef8ff 42%,#faf3ff 100%)!important;
}
section[data-testid="stSidebar"] .stButton>button{
    background:linear-gradient(90deg,#ffffff,#f7f5ff)!important;
    color:#24324a!important;
    border:1px solid #dce4f2!important;
    box-shadow:0 4px 12px rgba(71,85,105,.06)!important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:linear-gradient(90deg,#e0f7ff,#f3e8ff,#fce7f3)!important;
    color:#172033!important;
    border-color:#a5b4fc!important;
}

div.stButton>button{
    background:linear-gradient(90deg,#2563eb,#7c3aed,#db2777)!important;
    color:#ffffff!important;
    border:0!important;
    box-shadow:0 8px 20px rgba(79,70,229,.18)!important;
}
div.stButton>button:hover{
    filter:brightness(1.04);
    transform:translateY(-2px);
}

.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"]>div{
    background:#ffffff!important;
    color:#172033!important;
    border:2px solid #dbe4f0!important;
}

.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#7c879b!important}
.stRadio label,.stCheckbox label{color:#24324a!important}

[data-testid="stMetric"]{
    background:linear-gradient(145deg,#ffffff,#f7faff)!important;
    border:2px solid #e4eaf4!important;
}

/* Elemen dekoratif untuk halaman */
.color-ribbon{
    height:10px;border-radius:999px;margin:10px 0 20px;
    background:linear-gradient(90deg,#38bdf8,#6366f1,#ec4899,#f59e0b,#34d399);
}

.video-card{
    padding:18px;
    border-radius:28px;
    background:linear-gradient(145deg,#ffffff,#f8fbff);
    border:2px solid #e5eaf4;
    box-shadow:0 18px 42px rgba(71,85,105,.12);
}

.video-title{
    font-family:'Baloo 2',sans-serif;
    font-size:1.65rem;
    font-weight:900;
    color:#172033!important;
    margin-bottom:6px;
}

.video-note{color:#526078!important;font-weight:700}

@media(max-width:800px){
    .hero{min-height:220px;padding:24px 20px!important}
    .hero:before{font-size:1.2rem;letter-spacing:3px}
    .feature .emoji{width:60px;height:60px;font-size:2rem}
}

.cp-illustration{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:22px 28px;margin:0 0 22px;border-radius:24px;background:linear-gradient(135deg,#dbeafe,#f3e8ff 48%,#fce7f3);border:1px solid #dbe2ee;overflow:hidden}.cp-ill-title{font-size:1.65rem;font-weight:900;color:#172033}.cp-ill-sub{margin-top:6px;color:#526078;font-weight:700}.cp-ill-icons{display:flex;gap:12px;font-size:2.2rem;flex-wrap:wrap}.cp-icon{float:right;font-size:2.2rem}.atp-number{font-size:2rem;font-weight:900;color:#2563eb;line-height:1}.atp-ico{font-size:2rem;margin-right:14px;float:left}.tp-card{display:block;overflow:auto}.tp-card p{color:#334155;line-height:1.75}.tp-card h3{margin-bottom:7px}
.game-hero{display:grid;grid-template-columns:360px 1fr;gap:24px;align-items:center;padding:24px;border-radius:28px;background:linear-gradient(135deg,#dbeafe,#ede9fe,#fce7f3);border:1px solid #dbe2ee;margin-bottom:22px}.game-hero-art{background:rgba(255,255,255,.65);border-radius:22px;padding:12px}.game-hero-art svg{display:block;width:100%;height:auto}.game-kicker{font-size:.82rem;font-weight:900;color:#6d28d9;letter-spacing:.08em}.game-hero-copy h2{font-size:2.25rem;margin:8px 0;color:#172033}.game-hero-copy h2 span{color:#7c3aed}.game-hero-copy p{color:#40506a;font-size:1.05rem;line-height:1.65}.game-card{padding:18px;border-radius:20px;background:#fff;border:2px solid #e5e7eb;min-height:245px;box-shadow:0 4px 14px rgba(15,23,42,.06)}.game-card.game-active{border-color:#7c3aed;background:linear-gradient(180deg,#fff,#f5f3ff);box-shadow:0 10px 24px rgba(124,58,237,.14)}.game-picture{font-size:3.2rem;margin-bottom:5px}.game-level{display:inline-block;padding:4px 9px;border-radius:999px;background:#f3e8ff;color:#6d28d9;font-size:.75rem;font-weight:900}.game-card h3{margin:9px 0 6px;color:#172033}.game-card p{color:#526078;line-height:1.5}.mission-box{display:flex;gap:18px;align-items:flex-start;padding:22px;border-radius:22px;background:#fff;border:2px solid #dbe2ee;box-shadow:0 5px 18px rgba(15,23,42,.06);margin-bottom:16px}.mission-art{font-size:3.5rem;line-height:1}.mission-box h2{margin:0 0 6px;color:#172033}.mission-box p{margin:0;color:#526078}.quote-game{margin-top:14px;padding:18px;border-radius:15px;background:#f8fafc;border-left:5px solid #7c3aed;font-size:1.1rem;font-weight:800;color:#172033}.boss-box{padding:28px;text-align:center;border-radius:26px;background:linear-gradient(135deg,#fff7ed,#fef3c7,#fee2e2);border:2px solid #f59e0b;margin-bottom:18px}.boss-crown{font-size:4rem}.boss-box h2{font-size:2rem;color:#92400e}.boss-box p{font-size:1.1rem;color:#334155;line-height:1.7}@media(max-width:900px){.game-hero{grid-template-columns:1fr}.cp-illustration{align-items:flex-start;flex-direction:column}.game-hero-copy h2{font-size:1.8rem}}
</style>
""", unsafe_allow_html=True)

def level_info(xp):
    levels=[(0,"🌱 Pemula"),(100,"📖 Penjelajah Kata"),(250,"✍️ Ahli Bahasa"),(500,"🚀 Penulis Hebat"),(900,"🏆 Master Bahasa Indonesia"),(1500,"👑 Legend Bahasa")]
    current=levels[0]; nxt=None
    for i,item in enumerate(levels):
        if xp>=item[0]:
            current=item
            if i+1<len(levels): nxt=levels[i+1][0]
    return current[1],current[0],nxt

def award_xp(amount, reason=""):
    st.session_state.xp += amount
    if reason and reason not in st.session_state.aktivitas_selesai:
        st.session_state.aktivitas_selesai.append(reason)

def badge_check():
    b=set(st.session_state.badges); xp=st.session_state.xp
    if xp>=10:b.add("🌱 First Step")
    if xp>=100:b.add("⚡ XP Hunter")
    if st.session_state.ai_questions>=5:b.add("🤖 AI Explorer")
    if len(st.session_state.materi_dibaca)>=2:b.add("📚 Book Lover")
    if st.session_state.challenge_best>=80:b.add("🎯 Quick Learner")
    if len(st.session_state.aktivitas_selesai)>=5:b.add("🔥 Active Learner")
    st.session_state.badges=sorted(b)

def page_header(title,subtitle,emoji):
    st.markdown(f'<div class="hero" style="padding:24px 28px"><div style="font-size:2.6rem">{emoji}</div><div class="hero-title" style="font-size:2.8rem">{title}</div><div class="hero-sub">{subtitle}</div></div>',unsafe_allow_html=True)

badge_check()
level_name,level_start,next_level=level_info(st.session_state.xp)
pct=100 if next_level is None else max(0,min(100,int((st.session_state.xp-level_start)/(next_level-level_start)*100)))
name=st.session_state.nama_pelajar.strip() or "Teman Belajar"

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div style="text-align:center;padding:8px 0 18px"><div style="font-size:3.3rem">📚</div><div style="font-family:Baloo 2;font-size:1.5rem;font-weight:900">AI TUTOR</div><div style="color:#64748b;font-size:.82rem">Bahasa Indonesia • Ultimate 2.0</div></div>',unsafe_allow_html=True)
    st.session_state.nama_pelajar=st.text_input("👤 Nama Pelajar",value=st.session_state.nama_pelajar,placeholder="Masukkan nama")
    st.session_state.kelas=st.text_input("🏫 Kelas",value=st.session_state.kelas,placeholder="Contoh: VIII A")
    st.markdown(f'<div class="card" style="padding:16px;margin:8px 0 18px"><div style="font-weight:900">{level_name}</div><div class="xpbar"><div class="xpfill" style="width:{pct}%"></div></div><div style="font-size:.78rem;color:#526078">{st.session_state.xp} XP</div></div>',unsafe_allow_html=True)
    pages=[("🏠","Beranda"),("🌱","Profil Pelajar Pancasila"),("🗺️","CP dan ATP"),("🤖","AI Tutor"),("🎉","Ice Breaking"),("📚","Materi"),("🎮","Games"),("📝","LKPD"),("⚔️","Evaluasi"),("🏆","Achievement")]
    for icon,label in pages:
        if st.button(f"{icon}  {label}",key=f"nav_{label}",use_container_width=True):
            st.session_state.halaman=label
            st.rerun()
    st.markdown("---")
    st.caption("✨ Belajar • Bermain • Bertumbuh")

# ---------- Main Hero ----------
st.markdown(f'<div class="hero"><div class="hero-title">AI TUTOR<br>BAHASA INDONESIA</div><div class="hero-sub">Platform belajar interaktif untuk membaca, memahami, berlatih, bertanya kepada AI, dan menaklukkan tantangan Bahasa Indonesia.</div><div class="badges"><span class="badge">🚀 Ultimate 2.0</span><span class="badge">🤖 AI Learning</span><span class="badge">🎮 Gamified</span><span class="badge">🏆 Achievement</span></div></div>',unsafe_allow_html=True)

# ---------- Beranda ----------
if st.session_state.halaman=="Beranda":
    st.markdown(f'<div class="section">👋 Halo, {name}!</div>',unsafe_allow_html=True)
    st.write("Siap melanjutkan perjalanan belajar Bahasa Indonesia hari ini?")
    cols=st.columns(4)
    for col,(ico,val,label) in zip(cols,[("⭐",st.session_state.xp,"Total XP"),("🏆",len(st.session_state.badges),"Badge"),("🔥",st.session_state.streak,"Streak"),("🤖",st.session_state.ai_questions,"Pertanyaan AI")]):
        with col: st.markdown(f'<div class="stat"><div style="font-size:1.5rem">{ico}</div><div class="big">{val}</div><div class="label">{label}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section">🗺️ My Learning Journey</div>',unsafe_allow_html=True)
    journey=[("📚","Materi"),("🤖","AI Tutor"),("🎮","Games"),("📝","LKPD"),("⚔️","Evaluasi"),("🏆","Master")]
    cols=st.columns(len(journey)*2-1)
    for i,(ico,label) in enumerate(journey):
        done=label in st.session_state.aktivitas_selesai
        with cols[i*2]: st.markdown(f'<div class="node {"done" if done else "active" if i==0 else ""}"><div class="ico">{ico}</div><b>{label}</b><div class="small">{"SELESAI" if done else "LANJUT"}</div></div>',unsafe_allow_html=True)
        if i<len(journey)-1:
            with cols[i*2+1]: st.markdown('<div class="arrow">➜</div>',unsafe_allow_html=True)
    st.markdown('<div class="section">🎯 Aktivitas Utama</div>',unsafe_allow_html=True)
    features=[("🤖","AI Tutor","Tanyakan materi dan dapatkan penjelasan mudah.","AI Tutor"),("📚","Materi","Jelajahi materi Bahasa Indonesia.","Materi"),("🎮","Game Zone","Berlatih sambil mengumpulkan XP.","Games"),("📝","LKPD","Kerjakan misi belajar.","LKPD"),("⚔️","Challenge","Uji pemahamanmu seperti game.","Evaluasi"),("🌱","Profil Pancasila","Kembangkan karakter belajar.","Profil Pelajar Pancasila")]
    cols=st.columns(3)
    for i,(ico,title,desc,target) in enumerate(features):
        with cols[i%3]:
            st.markdown(f'<div class="feature"><div class="emoji">{ico}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            if st.button(f"Mulai {title} →",key=f"home_{i}",use_container_width=True):
                st.session_state.halaman=target;st.rerun()
    st.markdown('<div class="section">💡 Misi Hari Ini</div>',unsafe_allow_html=True)
    for col,(ico,title,xp,target) in zip(st.columns(3),[("📖","Baca Materi","+10 XP","Materi"),("🤖","Tanya AI","+15 XP","AI Tutor"),("⚔️","Ikuti Challenge","+50 XP","Evaluasi")]):
        with col: st.markdown(f'<div class="card"><div style="font-size:2rem">{ico}</div><h3>{title}</h3><p style="color:#526078">{xp}</p></div>',unsafe_allow_html=True)

# ---------- P5 ----------
elif st.session_state.halaman=="Profil Pelajar Pancasila":
    page_header("Profil Pelajar Pancasila","Enam dimensi karakter yang tumbuh bersama perjalanan belajar.","🌱")
    dims=[("🛐","Beriman, Bertakwa kepada Tuhan YME, dan Berakhlak Mulia","Membangun akhlak dan tanggung jawab."),("🌍","Berkebinekaan Global","Menghargai keberagaman dan perspektif."),("🤝","Gotong Royong","Bekerja sama dan saling membantu."),("🧠","Mandiri","Mengatur proses belajar dan bertanggung jawab."),("💡","Bernalar Kritis","Menganalisis informasi dan mengambil keputusan."),("🎨","Kreatif","Menghasilkan gagasan dan karya baru.")]
    cols=st.columns(3)
    for i,(ico,title,desc) in enumerate(dims):
        with cols[i%3]: st.markdown(f'<div class="feature"><div class="emoji">{ico}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

# ---------- CP ATP ----------
elif st.session_state.halaman=="CP dan ATP":
    page_header("CP & ATP Teks Prosedur","Capaian Pembelajaran dan Alur Tujuan Pembelajaran sebagai peta perjalanan belajar Teks Prosedur.","🗺️")
    st.markdown('''<div class="cp-illustration"><div><div class="cp-ill-title">📚 Misi Belajar Teks Prosedur</div><div class="cp-ill-sub">Pahami • Analisis • Susun • Tulis • Presentasikan</div></div><div class="cp-ill-icons"><span>🎯</span><span>📝</span><span>🔎</span><span>🏆</span></div></div>''',unsafe_allow_html=True)
    st.markdown('<div class="section">🎯 CAPAIAN PEMBELAJARAN</div>',unsafe_allow_html=True)
    cp_sections=[
        ("4.1. Menyimak","Menganalisis gagasan, pandangan, arahan, dan/atau pesan dari teks nonsastra berbentuk teks aural (teks yang dibacakan dan/atau didengarkan); dan menganalisis unsur intrinsik teks sastra berbentuk teks aural.","🎧","#2563eb"),
        ("4.2. Membaca dan Memirsa","Menganalisis informasi berupa gagasan, pandangan, arahan, dan/atau pesan dari berbagai tipe teks berwujud teks visual dan/atau audiovisual untuk menemukan makna yang tersurat dan tersirat; menginterpretasi informasi untuk mengungkapkan kepedulian dan/atau pendapat pro/kontra dari berbagai tipe teks berwujud teks visual dan/atau audiovisual; dan mengevaluasi kualitas dan/atau kredibilitas dari berbagai tipe teks berwujud teks visual dan/atau audiovisual menggunakan sumber informasi lain.","👀","#7c3aed"),
        ("4.3. Berbicara dan Mempresentasikan","Mempresentasikan gagasan, pandangan, arahan, dan/atau pesan untuk tujuan pengajuan usul, dan pemberian solusi dalam bentuk monolog, dialog logis, dan/atau berbagai tipe teks secara kritis dan kreatif; dan menyajikan ungkapan kepedulian dari berbagai tipe teks dan/atau teks multimodal.","🎤","#db2777"),
        ("4.4. Menulis","Menulis gagasan, pandangan, arahan, pesan, pengalaman, dan/atau imajinasi dalam berbagai tipe teks secara logis, kritis, kreatif, menarik, dan/atau indah; menulis ungkapan kepedulian dan/atau pendapat pro/kontra dalam berbagai tipe teks berbentuk teks multimodal; dan menggunakan kosakata baru yang memiliki makna denotatif, konotatif, dan kiasan untuk menulis.","✍️","#059669"),
    ]
    for code,text,ico,color in cp_sections:
        st.markdown(f'''<div class="cp-card" style="border-left-color:{color}"><div class="cp-icon">{ico}</div><h3>{code}</h3><p>{text}</p></div>''',unsafe_allow_html=True)
    st.markdown('<div class="section">🧭 ALUR TUJUAN PEMBELAJARAN (ATP)</div>',unsafe_allow_html=True)
    atp=[
        "Peserta didik mampu memahami pengertian, tujuan, fungsi, dan ciri-ciri teks prosedur.",
        "Peserta didik mampu mengidentifikasi struktur teks prosedur, yaitu judul, tujuan, alat/bahan, dan langkah-langkah.",
        "Peserta didik mampu mengidentifikasi kaidah kebahasaan teks prosedur, seperti kalimat imperatif, kata kerja, konjungsi temporal, kata keterangan, dan kalimat larangan.",
        "Peserta didik mampu menganalisis isi dan struktur teks prosedur berdasarkan contoh yang dibaca atau diamati.",
        "Peserta didik mampu menentukan topik dan tujuan yang akan dikembangkan menjadi teks prosedur.",
        "Peserta didik mampu menyusun kerangka dan langkah-langkah teks prosedur secara runtut dan logis.",
        "Peserta didik mampu menulis teks prosedur secara lengkap dengan memperhatikan struktur, kaidah kebahasaan, ejaan, dan tanda baca.",
        "Peserta didik mampu menyunting, memperbaiki, dan mempresentasikan teks prosedur yang telah dibuat.",
    ]
    icons=["💡","🧩","🔤","🔎","🎯","📝","✍️","🎤"]
    for i,item in enumerate(atp,1):
        st.markdown(f'''<div class="tp-card"><div class="atp-number">{i}</div><div class="atp-ico">{icons[i-1]}</div><div><h3>ATP {i}</h3><p>{item}</p></div></div>''',unsafe_allow_html=True)
    st.markdown('<div class="section">🎮 Hubungkan dengan Game</div>',unsafe_allow_html=True)
    st.info("Setiap misi dalam Procedure Quest dirancang untuk membantu peserta didik memahami struktur, urutan langkah, kaidah kebahasaan, dan isi teks prosedur.")
    if st.button("🎮 Mulai Procedure Quest",use_container_width=True):
        st.session_state.halaman="Games"; st.rerun()

# ---------- AI ----------
elif st.session_state.halaman=="AI Tutor":
    page_header("NARA • AI Tutor","Teman belajar digital yang membantu memahami materi Bahasa Indonesia.","🤖")
    a,b=st.columns([1,2])
    with a:
        st.markdown('<div class="card" style="text-align:center"><div class="ai-avatar">🤖</div><h2>NARA</h2><p style="color:#526078">Teman Belajar Bahasa Indonesia</p><div class="info">💡 Tanyakan apa saja tentang materi yang sedang kamu pelajari.</div></div>',unsafe_allow_html=True)
        st.markdown("**💬 Pertanyaan cepat**")
        quick=["Apa itu teks prosedur?","Apa struktur teks prosedur?","Berikan contoh teks prosedur.","Apa ciri kebahasaan teks prosedur?"]
        for i,q in enumerate(quick):
            if st.button(q,key=f"quick_{i}",use_container_width=True):
                st.session_state["ai_input"]=q;st.rerun()
    with b:
        q=st.text_area("💭 Tulis pertanyaanmu",value=st.session_state.get("ai_input",""),height=120,placeholder="Contoh: Jelaskan struktur teks prosedur dengan bahasa sederhana...")
        c1,c2=st.columns(2)
        ask=c1.button("✨ Tanya NARA",use_container_width=True)
        if c2.button("🧹 Bersihkan",use_container_width=True):
            st.session_state["ai_input"]="";st.rerun()
        if ask and q.strip():
            st.session_state.ai_questions+=1
            award_xp(15,"AI Tutor")
            context=buat_context_ai(q.strip())
            answer,error=buat_jawaban_ai(q.strip(),context)
            if not answer: answer=error or "Maaf, AI belum dapat memberikan jawaban."
            st.session_state.riwayat_ai.append({"q":q.strip(),"a":answer})
            st.session_state["ai_input"]="";badge_check()
        for item in reversed(st.session_state.riwayat_ai[-6:]):
            st.markdown(f'<div class="chat-user"><b>👤 Kamu</b><br>{item["q"]}</div>',unsafe_allow_html=True)
            st.markdown(f'<div class="chat-ai"><b>🤖 NARA</b><br>{item["a"]}</div>',unsafe_allow_html=True)

# ---------- ICE BREAKING ----------
elif st.session_state.halaman=="Ice Breaking":
    page_header("Ice Breaking","Pilih permainan, lalu langsung mainkan tantangannya!","🎉")
    st.markdown('<div class="color-ribbon"></div>',unsafe_allow_html=True)

    v1,v2=st.columns([1.55,1],gap="large")
    with v1:
        st.markdown("""<div class="video-card"><div class="video-title">🎬 Video Senam Otak</div><div class="video-note">Ikuti gerakannya bersama teman-teman sebagai pemanasan sebelum bermain.</div></div>""",unsafe_allow_html=True)
        st.video(YOUTUBE_ICE_BREAKING_URL)
        st.caption("💡 Video dapat diganti melalui variabel YOUTUBE_ICE_BREAKING_URL di bagian atas kode.")
    with v2:
        st.markdown("""<div class="feature"><div class="emoji">🎈</div><h3>Siap Bermain?</h3><p>Pilih salah satu permainan di bawah, lalu ikuti instruksi sampai selesai.</p></div>""",unsafe_allow_html=True)
        st.markdown("""<div class="feature" style="margin-top:14px"><div class="emoji">⭐</div><h3>Hadiah</h3><p><b>+10 XP</b> untuk setiap permainan yang berhasil diselesaikan.</p></div>""",unsafe_allow_html=True)

    st.markdown('<div class="section">🎮 Pilih Permainan Ice Breaking</div>',unsafe_allow_html=True)
    ice_cards=[
        ("🎤","Suara Ceria","Ucapkan kata yang sama dengan ekspresi berbeda."),
        ("🕺","Gerak & Kata","Peragakan sebuah kegiatan tanpa berbicara."),
        ("🧠","Tebak Kata","Berikan petunjuk agar teman menebak kata rahasia."),
        ("😂","Kalimat Lucu","Susun kalimat kreatif dari kata-kata yang diberikan."),
        ("⚡","30 Detik","Jelaskan sebuah topik sebelum waktu habis."),
        ("🤝","Pasangan Hebat","Kerjakan tantangan bersama seorang teman."),
    ]
    if "ice_game" not in st.session_state: st.session_state.ice_game="Suara Ceria"
    if "ice_done_games" not in st.session_state: st.session_state.ice_done_games=[]
    cols=st.columns(3,gap="large")
    for i,(ico,title,desc) in enumerate(ice_cards):
        with cols[i%3]:
            active=st.session_state.ice_game==title
            border='border:3px solid #7c3aed;box-shadow:0 10px 26px rgba(124,58,237,.20);' if active else ''
            label='<div style="display:inline-block;background:#ede9fe;color:#6d28d9;padding:5px 10px;border-radius:999px;font-size:.78rem;font-weight:800;margin-bottom:8px">✓ SEDANG DIMAINKAN</div>' if active else ''
            st.markdown(f'''<div class="feature" style="min-height:220px;{border}"><div class="emoji">{ico}</div>{label}<h3>{title}</h3><p>{desc}</p></div>''',unsafe_allow_html=True)
            if st.button("🎮 Mainkan" if not active else "🔄 Pilih Lagi",key=f"ice_game_{i}",use_container_width=True):
                st.session_state.ice_game=title
                st.session_state.ice_answer=""
                st.session_state.ice_started=True
                st.rerun()

    game=st.session_state.ice_game
    st.markdown('<div class="section">🏆 Permainan Sekarang</div>',unsafe_allow_html=True)

    if game=="Suara Ceria":
        st.markdown("""<div class="challenge"><div style="font-size:3rem">🎤</div><h2>Suara Ceria</h2><p><b>Tantangan:</b> ucapkan kata <b>"SEMANGAT"</b> dengan 3 ekspresi berbeda: gembira, sedih, dan sangat terkejut.</p><div class="badges"><span class="badge">🎭 3 Ekspresi</span><span class="badge">⚡ +10 XP</span></div></div>""",unsafe_allow_html=True)
        if st.button("✅ Saya Sudah Melakukan 3 Ekspresi",use_container_width=True,key="done_suara"):
            if game not in st.session_state.ice_done_games:
                st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - Suara Ceria");badge_check()
            st.success("Hebat! Suaramu pasti luar biasa! 🎉 +10 XP")

    elif game=="Gerak & Kata":
        gerak=random.choice(["menyapu","memasak","berenang","menulis","bersepeda","mencuci tangan"])
        if "ice_gerak_word" not in st.session_state: st.session_state.ice_gerak_word=gerak
        st.markdown(f'''<div class="challenge"><div style="font-size:3rem">🕺</div><h2>Gerak & Kata</h2><p>Peragakan kegiatan berikut <b>tanpa berbicara</b>, lalu biarkan temanmu menebaknya:</p><div style="font-size:2rem;font-weight:900;color:#6d28d9">{st.session_state.ice_gerak_word.upper()}</div><div class="badges"><span class="badge">🤫 Tanpa Bicara</span><span class="badge">⚡ +10 XP</span></div></div>''',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            if st.button("🔄 Ganti Tantangan",use_container_width=True):
                st.session_state.ice_gerak_word=random.choice(["menyapu","memasak","berenang","menulis","bersepeda","mencuci tangan"]);st.rerun()
        with b:
            if st.button("🏁 Teman Sudah Menebak!",use_container_width=True,key="done_gerak"):
                if game not in st.session_state.ice_done_games:
                    st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - Gerak & Kata");badge_check()
                st.success("Mantap! Gerakanmu berhasil ditebak! 🎉 +10 XP")

    elif game=="Tebak Kata":
        clues={"MATAHARI":["Terbit di pagi hari","Memberi cahaya","Terasa panas"],"SEKOLAH":["Tempat belajar","Ada guru dan siswa","Ada kelas"],"BUKU":["Bisa dibaca","Memiliki halaman","Tempat mencari ilmu"],"PENSIL":["Dipakai untuk menulis","Bisa diraut","Sering ada di meja belajar"]}
        if "ice_secret" not in st.session_state: st.session_state.ice_secret=random.choice(list(clues))
        secret=st.session_state.ice_secret
        clue_html=''.join(f'<li style="margin:7px 0">{x}</li>' for x in clues[secret])
        st.markdown(f'''<div class="challenge"><div style="font-size:3rem">🧠</div><h2>Tebak Kata</h2><p>Sampaikan 3 petunjuk berikut kepada teman. <b>Jangan sebutkan kata rahasianya!</b></p><ol>{clue_html}</ol><div class="badges"><span class="badge">🤫 Rahasia</span><span class="badge">⚡ +10 XP</span></div></div>''',unsafe_allow_html=True)
        guess=st.text_input("Jawaban temanmu:",placeholder="Ketik tebakan di sini...",key="guess_word")
        a,b=st.columns(2)
        with a:
            if st.button("🔍 Cek Jawaban",use_container_width=True):
                if guess.strip().upper()==secret:
                    st.success("Benar! 🎉 Tebakan tepat!")
                    if game not in st.session_state.ice_done_games:
                        st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - Tebak Kata");badge_check()
                else: st.warning("Belum tepat. Coba lagi berdasarkan petunjuk!")
        with b:
            if st.button("🔄 Kata Baru",use_container_width=True):
                st.session_state.ice_secret=random.choice(list(clues));st.rerun()

    elif game=="Kalimat Lucu":
        if "ice_sentence_words" not in st.session_state: st.session_state.ice_sentence_words=random.sample(["kucing","sekolah","payung","nasi goreng","robot","sepeda","hujan","guru"],3)
        words=st.session_state.ice_sentence_words
        st.markdown(f'''<div class="challenge"><div style="font-size:3rem">😂</div><h2>Kalimat Lucu</h2><p>Buat satu kalimat lucu yang memakai <b>semua kata</b> berikut:</p><div style="font-size:1.6rem;font-weight:900;color:#6d28d9">{' • '.join(words)}</div><div class="badges"><span class="badge">✍️ Kreatif</span><span class="badge">⚡ +10 XP</span></div></div>''',unsafe_allow_html=True)
        sentence=st.text_area("Tulis kalimatmu:",placeholder="Contoh: Robot itu naik sepeda sambil membawa nasi goreng...",key="fun_sentence")
        a,b=st.columns(2)
        with a:
            if st.button("😂 Kirim Kalimat",use_container_width=True):
                if sentence.strip() and all(w.lower() in sentence.lower() for w in words):
                    if game not in st.session_state.ice_done_games:
                        st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - Kalimat Lucu");badge_check()
                    st.success("Kreatif sekali! Semua kata sudah digunakan. 🎉 +10 XP")
                else: st.warning("Gunakan semua kata yang diberikan dan tulis minimal satu kalimat.")
        with b:
            if st.button("🔄 Kata Baru",use_container_width=True):
                st.session_state.ice_sentence_words=random.sample(["kucing","sekolah","payung","nasi goreng","robot","sepeda","hujan","guru"],3);st.rerun()

    elif game=="30 Detik":
        topics=["Hobi favoritmu","Makanan kesukaanmu","Tempat yang ingin kamu kunjungi","Tokoh yang kamu kagumi","Pengalaman paling lucu"]
        if "ice_topic" not in st.session_state: st.session_state.ice_topic=random.choice(topics)
        st.markdown(f'''<div class="challenge"><div style="font-size:3rem">⚡</div><h2>Tantangan 30 Detik</h2><p>Bicarakan topik berikut selama <b>30 detik</b> tanpa berhenti:</p><div style="font-size:1.8rem;font-weight:900;color:#6d28d9">{st.session_state.ice_topic}</div><div class="badges"><span class="badge">⏱️ 30 Detik</span><span class="badge">⚡ +10 XP</span></div></div>''',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            if st.button("⏱️ MULAI 30 DETIK",use_container_width=True):
                st.session_state.ice_timer_started=True
                st.rerun()
        with b:
            if st.button("🏁 Saya Berhasil 30 Detik",use_container_width=True):
                if game not in st.session_state.ice_done_games:
                    st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - 30 Detik");badge_check()
                st.success("Luar biasa! Kamu berhasil menyelesaikan tantangan! 🎉 +10 XP")
        if st.session_state.get("ice_timer_started",False):
            st.info("🗣️ WAKTUNYA DIMULAI! Bicara sekarang selama 30 detik. Gunakan timer di HP/jam jika diperlukan.")

    elif game=="Pasangan Hebat":
        tasks=["Buat salam unik bersama teman.","Buat satu kalimat dengan kata 'tetapi'.","Saling sebutkan 3 kata positif.","Lakukan tepuk kompak 5 kali.","Buat yel-yel kelas selama 10 detik."]
        if "ice_pair_task" not in st.session_state: st.session_state.ice_pair_task=random.choice(tasks)
        st.markdown(f'''<div class="challenge"><div style="font-size:3rem">🤝</div><h2>Pasangan Hebat</h2><p>Kerjakan bersama seorang teman:</p><div style="font-size:1.55rem;font-weight:900;color:#6d28d9">{st.session_state.ice_pair_task}</div><div class="badges"><span class="badge">🤝 Berdua</span><span class="badge">⭐ Kompak</span><span class="badge">⚡ +10 XP</span></div></div>''',unsafe_allow_html=True)
        a,b=st.columns(2)
        with a:
            if st.button("🎲 Tantangan Pasangan Baru",use_container_width=True):
                st.session_state.ice_pair_task=random.choice(tasks);st.rerun()
        with b:
            if st.button("🏆 Kami Berhasil!",use_container_width=True):
                if game not in st.session_state.ice_done_games:
                    st.session_state.ice_done_games.append(game);award_xp(10,"Ice Breaking - Pasangan Hebat");badge_check()
                st.success("Keren! Kerja sama kalian hebat! 🎉 +10 XP")

    if st.session_state.ice_done_games:
        st.markdown(f'''<div class="feature" style="margin-top:20px;text-align:center;border:2px solid #10b981;background:linear-gradient(135deg,#ecfdf5,#f0fdf4)"><div style="font-size:2.2rem">🏆</div><h3>Permainan Selesai</h3><p>Kamu sudah menyelesaikan <b>{len(st.session_state.ice_done_games)}</b> permainan Ice Breaking.</p><p style="color:#047857!important;font-weight:800">Permainan selesai: {', '.join(st.session_state.ice_done_games)}</p></div>''',unsafe_allow_html=True)

# ---------- MATERI ----------
elif st.session_state.halaman=="Materi":
    page_header("Digital Library","Baca materi, tandai progres, dan lanjutkan perjalanan belajar.","📚")
    try: files=sorted([f for f in os.listdir(FOLDER_DATABASE) if f.lower().endswith(".txt")])
    except Exception: files=[]
    if not files: st.warning("Belum ada file materi TXT di folder database.")
    else:
        selected=st.selectbox("📖 Pilih materi",files)
        path=os.path.join(FOLDER_DATABASE,selected)
        try: content=open(path,encoding="utf-8").read()
        except Exception: content="Materi tidak dapat dibaca."
        st.markdown(f'<div class="card"><h2>📖 {selected}</h2><p style="color:#526078">Materi pembelajaran</p></div>',unsafe_allow_html=True)
        st.markdown(content)
        if st.button("✅ Tandai Materi Selesai",use_container_width=True):
            if selected not in st.session_state.materi_dibaca:
                st.session_state.materi_dibaca.append(selected);award_xp(10,"Materi");badge_check()
            st.success("Materi ditandai selesai! +10 XP")

# ---------- GAMES ----------
elif st.session_state.halaman=="Games":
    page_header("PROCEDURE QUEST","Petualangan game Teks Prosedur — susun, tebak, analisis, dan taklukkan tantangan!","🎮")
    st.markdown(f'''<div class="game-hero"><div class="game-hero-art"><svg viewBox="0 0 360 190" role="img" aria-label="Ilustrasi buku, target, pensil dan langkah prosedur"><rect x="12" y="28" width="120" height="120" rx="22" fill="#ffffff" opacity=".95"/><path d="M35 55h72M35 80h72M35 105h50" stroke="#2563eb" stroke-width="10" stroke-linecap="round"/><circle cx="205" cy="75" r="48" fill="#fff7ed"/><circle cx="205" cy="75" r="27" fill="#fde68a"/><circle cx="205" cy="75" r="10" fill="#f97316"/><path d="M200 132l58-78 17 13-58 78z" fill="#ec4899"/><path d="M257 54l14-7 8 8-5 15z" fill="#f59e0b"/><path d="M275 137c18-9 32-25 38-44" fill="none" stroke="#10b981" stroke-width="9" stroke-linecap="round"/><path d="M313 93l-2 20-18-8" fill="#10b981"/></svg></div><div class="game-hero-copy"><div class="game-kicker">🏆 MATERI: TEKS PROSEDUR</div><h2>Siap menjadi <span>Procedure Master?</span></h2><p>Setiap jawaban benar menambah skor dan XP. Pilih misi, mainkan sampai selesai, lalu buka level berikutnya.</p><div class="badges"><span class="badge">⭐ Skor: {st.session_state.procedure_score}</span><span class="badge">❤️ Nyawa: {st.session_state.procedure_lives}</span><span class="badge">🏆 Best: {st.session_state.procedure_best}</span></div></div></div>''',unsafe_allow_html=True)
    st.markdown('<div class="section">🌐 Game Wordwall Kamu</div>',unsafe_allow_html=True)
    ww1,ww2=st.columns([1.15,1],gap="large")
    with ww1:
        st.markdown("""<div class="wordwall-card"><div class="wordwall-art">🎮</div><div><div class="game-kicker">🌐 GAME INTERAKTIF</div><h2>Wordwall Teks Prosedur</h2><p>Game Wordwall yang sudah kamu gunakan tetap tersedia di sini. Klik tombol di bawah untuk langsung bermain.</p></div></div>""",unsafe_allow_html=True)
        st.link_button("▶️ MAIN WORDWALL",WORDWALL_URL,use_container_width=True)
    with ww2:
        st.markdown("""<div class="wordwall-preview"><div class="preview-icon">🧩</div><h3>Tetap Ada, Tidak Dihapus</h3><p>Wordwall adalah game asli dari aplikasi kamu. Procedure Quest di bawah adalah game tambahan.</p><div class="badges"><span class="badge">🎯 Teks Prosedur</span><span class="badge">⭐ Game Eksternal</span></div></div>""",unsafe_allow_html=True)

    modes=[
        ("🧩","Susun Langkah","Urutkan langkah teks prosedur dari awal sampai akhir.","Level 1"),
        ("🔎","Detektif Struktur","Tentukan bagian tujuan, alat/bahan, atau langkah.","Level 2"),
        ("⚡","Kuis Kilat","Jawab soal pilihan ganda tentang teks prosedur.","Level 3"),
        ("👑","Boss Level","Hadapi tantangan akhir dengan soal campuran.","Boss"),
    ]
    st.markdown('<div class="section">🗺️ Pilih Misi</div>',unsafe_allow_html=True)
    cols=st.columns(4,gap="medium")
    for i,(ico,title,desc,level) in enumerate(modes):
        active=st.session_state.procedure_mode==title
        with cols[i]:
            st.markdown(f'''<div class="game-card {"game-active" if active else ""}"><div class="game-picture">{ico}</div><div class="game-level">{level}</div><h3>{title}</h3><p>{desc}</p></div>''',unsafe_allow_html=True)
            if st.button("▶️ Mainkan" if not active else "🎯 Sedang Dipilih",key=f"procedure_mode_{i}",use_container_width=True):
                st.session_state.procedure_mode=title; st.session_state.procedure_lives=3; st.session_state.procedure_round=0; st.rerun()
    mode=st.session_state.procedure_mode
    st.markdown('<div class="section">🎯 Misi Aktif</div>',unsafe_allow_html=True)
    if mode=="Susun Langkah":
        scenarios={
            "Membuat Teh Manis":["Masukkan gula ke dalam gelas.","Tuangkan air panas ke dalam gelas.","Masukkan kantong teh.","Aduk hingga gula larut.","Angkat kantong teh dan sajikan."],
            "Mencuci Tangan":["Basahi tangan dengan air mengalir.","Gunakan sabun secukupnya.","Gosok telapak dan punggung tangan.","Bilas tangan hingga bersih.","Keringkan tangan dengan tisu atau handuk bersih."],
            "Membuat Jus Mangga":["Kupas dan potong mangga.","Masukkan potongan mangga ke blender.","Tambahkan air secukupnya.","Blender hingga halus.","Tuangkan jus ke dalam gelas."],
        }
        if "procedure_order" not in st.session_state or st.session_state.get("procedure_order_title") not in scenarios:
            title=random.choice(list(scenarios)); st.session_state.procedure_order_title=title; st.session_state.procedure_order=scenarios[title][:]; random.shuffle(st.session_state.procedure_order)
        title=st.session_state.procedure_order_title; correct=scenarios[title]
        st.markdown(f'''<div class="mission-box"><div class="mission-art">🧩</div><div><h2>Susun Langkah: {title}</h2><p>Urutkan langkah di bawah dari <b>langkah pertama</b> sampai terakhir.</p></div></div>''',unsafe_allow_html=True)
        order=[]
        for pos in range(len(correct)):
            pilihan=["— pilih langkah —"]+[x for x in st.session_state.procedure_order if x not in order]
            chosen=st.selectbox(f"Langkah {pos+1}",pilihan,key=f"procedure_step_{st.session_state.procedure_order_title}_{pos}")
            if chosen!="— pilih langkah —": order.append(chosen)
        if len(order)==len(correct) and st.button("🔐 Kunci Jawaban",use_container_width=True):
            if order==correct:
                st.session_state.procedure_score+=25; st.session_state.procedure_best=max(st.session_state.procedure_best,st.session_state.procedure_score); award_xp(25,"Game Procedure Quest - Susun Langkah"); badge_check(); st.success("🎉 SEMPURNA! Urutan langkahmu benar. +25 XP")
                if "Susun Langkah" not in st.session_state.procedure_completed: st.session_state.procedure_completed.append("Susun Langkah")
            else:
                st.session_state.procedure_lives=max(0,st.session_state.procedure_lives-1); st.error(f"❌ Belum tepat. Nyawa tersisa: {st.session_state.procedure_lives}")
        if st.button("🔄 Tantangan Baru",use_container_width=True):
            title=random.choice(list(scenarios)); st.session_state.procedure_order_title=title; st.session_state.procedure_order=scenarios[title][:]; random.shuffle(st.session_state.procedure_order); st.session_state.procedure_lives=3; st.rerun()
    elif mode=="Detektif Struktur":
        questions=[("Siapkan 2 lembar roti, selai, dan pisang.","Alat/Bahan"),("Oleskan selai pada permukaan roti.","Langkah-langkah"),("Cara Membuat Roti Pisang","Judul"),("Teks ini menjelaskan cara membuat minuman sederhana.","Tujuan"),("Kemudian, masukkan es batu ke dalam gelas.","Langkah-langkah"),("3 sendok gula dan 200 ml air.","Alat/Bahan")]
        idx=st.session_state.procedure_round%len(questions); sentence,answer=questions[idx]
        st.markdown(f'''<div class="mission-box"><div class="mission-art">🔎</div><div><h2>Detektif Struktur</h2><p>Temukan struktur teks prosedur dari potongan berikut:</p><div class="quote-game">“{sentence}”</div></div></div>''',unsafe_allow_html=True)
        pick=st.radio("Potongan ini termasuk bagian...",["Judul","Tujuan","Alat/Bahan","Langkah-langkah"],index=None,key=f"detective_{idx}")
        if st.button("🔍 Periksa",use_container_width=True):
            if pick==answer:
                st.session_state.procedure_score+=20; st.session_state.procedure_best=max(st.session_state.procedure_best,st.session_state.procedure_score); award_xp(20,"Game Procedure Quest - Detektif Struktur"); badge_check(); st.success(f"✅ Benar! Itu adalah {answer}. +20 XP"); st.session_state.procedure_round+=1
            else:
                st.session_state.procedure_lives=max(0,st.session_state.procedure_lives-1); st.error(f"❌ Belum tepat. Pikirkan fungsi kalimat tersebut. Nyawa: {st.session_state.procedure_lives}")
        if st.button("➡️ Soal Berikutnya",use_container_width=True): st.session_state.procedure_round+=1; st.rerun()
    elif mode=="Kuis Kilat":
        questions=[("Apa tujuan utama teks prosedur?",["Menghibur pembaca","Menjelaskan cara melakukan sesuatu","Menceritakan pengalaman","Menggambarkan tokoh"],1),("Kata 'kemudian' termasuk contoh...",["Konjungsi temporal","Kata benda","Kata sapaan","Kata sifat"],0),("Kalimat 'Potonglah wortel menjadi kecil-kecil!' merupakan...",["Kalimat berita","Kalimat imperatif","Kalimat tanya","Kalimat perbandingan"],1),("Bagian yang memuat tahapan kegiatan disebut...",["Judul","Tujuan","Langkah-langkah","Penutup"],2),("Manakah yang merupakan kalimat larangan?",["Aduk hingga rata.","Jangan menyentuh kabel dengan tangan basah.","Masukkan gula.","Setelah itu, sajikan."],1)]
        idx=st.session_state.procedure_round%len(questions); q,opts,ans=questions[idx]
        st.markdown(f'''<div class="mission-box"><div class="mission-art">⚡</div><div><h2>Kuis Kilat</h2><p>Soal {idx+1} dari {len(questions)}. Pilih jawaban terbaik.</p><div class="quote-game">{q}</div></div></div>''',unsafe_allow_html=True)
        pick=st.radio("Jawabanmu:",opts,index=None,key=f"quick_game_{idx}")
        if st.button("⚡ Jawab Sekarang",use_container_width=True):
            if pick==opts[ans]:
                st.session_state.procedure_score+=15; st.session_state.procedure_best=max(st.session_state.procedure_best,st.session_state.procedure_score); award_xp(15,"Game Procedure Quest - Kuis Kilat"); badge_check(); st.success("🎉 Jawaban benar! +15 XP"); st.session_state.procedure_round+=1
            else:
                st.session_state.procedure_lives=max(0,st.session_state.procedure_lives-1); st.error(f"❌ Jawaban belum tepat. Nyawa tersisa: {st.session_state.procedure_lives}")
        if st.button("➡️ Soal Berikutnya",use_container_width=True): st.session_state.procedure_round+=1; st.rerun()
    elif mode=="Boss Level":
        boss=[("Urutkan secara logis: 1) Sajikan. 2) Masukkan bubuk ke gelas. 3) Tuangkan air panas. 4) Aduk.","2-3-4-1"),("Sebutkan minimal tiga ciri kebahasaan teks prosedur.","imperatif, kata kerja, konjungsi temporal"),("Sebutkan empat struktur teks prosedur yang dipelajari.","judul, tujuan, alat/bahan, langkah-langkah")]
        idx=st.session_state.procedure_round%len(boss); prompt,answer=boss[idx]
        st.markdown(f'''<div class="boss-box"><div class="boss-crown">👑</div><h2>BOSS LEVEL</h2><p>{prompt}</p><div class="badges"><span class="badge">🔥 +40 XP</span><span class="badge">❤️ 3 Nyawa</span></div></div>''',unsafe_allow_html=True)
        response=st.text_area("Tulis jawabanmu:",height=120,key=f"boss_answer_{idx}")
        if st.button("👑 Kalahkan Boss",use_container_width=True):
            normalized=re.sub(r"[^a-z0-9\s,-]","",response.lower()).strip()
            if idx==0: ok=normalized.replace(" ","")==answer.replace(" ","")
            elif idx==1: ok=sum(1 for w in ["imperatif","kata kerja","konjungsi temporal","keterangan","larangan"] if w in normalized)>=3
            else: ok=sum(1 for w in ["judul","tujuan","alat","bahan","langkah"] if w in normalized)>=4
            if ok:
                st.session_state.procedure_score+=40; st.session_state.procedure_best=max(st.session_state.procedure_best,st.session_state.procedure_score); award_xp(40,"Game Procedure Quest - Boss Level"); badge_check(); st.success("👑 BOSS DIKALAHKAN! Kamu adalah Procedure Master! +40 XP"); st.session_state.procedure_round+=1
                if "Boss Level" not in st.session_state.procedure_completed: st.session_state.procedure_completed.append("Boss Level")
            else:
                st.session_state.procedure_lives=max(0,st.session_state.procedure_lives-1); st.error(f"💥 Belum berhasil. Nyawa tersisa: {st.session_state.procedure_lives}")
        if st.button("🔄 Tantangan Boss Baru",use_container_width=True): st.session_state.procedure_round+=1; st.session_state.procedure_lives=3; st.rerun()
    st.markdown('<div class="section">🏆 Progress Procedure Quest</div>',unsafe_allow_html=True)
    progress=min(100,int(len(st.session_state.procedure_completed)/4*100)); st.progress(progress/100)
    st.markdown(f'''<div class="card" style="text-align:center"><div style="font-size:2.5rem">🏆</div><h2>{progress}% Quest Selesai</h2><p>Skor saat ini: <b>{st.session_state.procedure_score}</b> • Misi selesai: <b>{len(st.session_state.procedure_completed)}/4</b></p></div>''',unsafe_allow_html=True)
    if st.button("♻️ Reset Progress Game",use_container_width=True):
        st.session_state.procedure_score=0; st.session_state.procedure_lives=3; st.session_state.procedure_round=0; st.session_state.procedure_completed=[]; st.rerun()

# ---------- LKPD ----------
elif st.session_state.halaman=="LKPD":
    page_header("Learning Mission","Kerjakan LKPD sebagai bagian dari misi belajarmu.","📝")
    st.markdown('<div class="feature"><div class="emoji">📝</div><h3>Mission: Complete Your LKPD</h3><p>Kerjakan tugas dengan teliti, lalu kembali untuk melanjutkan perjalananmu.</p></div>',unsafe_allow_html=True)
    if st.button("🚀 Buka LKPD & Dapatkan XP",use_container_width=True):
        award_xp(25,"LKPD");badge_check();st.link_button("📝 Kerjakan Sekarang",LKPD_URL,use_container_width=True)

# ---------- EVALUASI ----------
elif st.session_state.halaman=="Evaluasi":
    page_header("Challenge Arena","Taklukkan tantangan dan buktikan penguasaanmu.","⚔️")
    st.markdown(f'<div class="challenge"><b>⚔️ FINAL CHALLENGE</b><br><span style="color:#526078">8 soal • Teks Prosedur</span><div class="badges"><span class="badge">❤️ 3 Lives</span><span class="badge">⭐ +50 XP</span><span class="badge">🏆 Best: {st.session_state.challenge_best}</span></div></div>',unsafe_allow_html=True)
    questions=[
        ("Apa tujuan utama teks prosedur?",["Menghibur pembaca","Menjelaskan langkah melakukan sesuatu","Menceritakan pengalaman","Menggambarkan tokoh"],1),
        ("Bagian yang berisi tahapan kegiatan disebut...",["Tujuan","Bahan","Langkah-langkah","Penutup"],2),
        ("Kata 'kemudian' dalam teks prosedur menunjukkan...",["Urutan","Tempat","Tokoh","Sebab"],0),
        ("Kalimat yang tepat untuk teks prosedur adalah...",["Aduk adonan hingga rata.","Kemarin saya pergi.","Rumah itu sangat besar.","Dia anak yang baik."],0),
        ("Teks prosedur sebaiknya disusun secara...",["Acak","Sistematis","Rahasia","Puitis"],1),
        ("Kata kerja yang sering digunakan dalam teks prosedur adalah...",["Imperatif","Seruan","Nomina","Sapaan"],0),
        ("Informasi bahan biasanya terdapat sebelum...",["Judul","Langkah-langkah","Nama penulis","Salam"],1),
        ("Urutan langkah penting agar pembaca...",["Bingung","Dapat mengikuti proses dengan benar","Berhenti membaca","Menghafal cerita"],1),
    ]
    answers={}
    for i,(q,opts,ans) in enumerate(questions):
        st.markdown(f'<div class="question"><b>⚔️ {i+1:02d}/08</b><br><br><span style="font-size:1.12rem">{q}</span></div>',unsafe_allow_html=True)
        answers[i]=st.radio("Pilih jawaban:",opts,key=f"eval_{i}",index=None)
    if st.button("🏆 Submit Challenge",use_container_width=True):
        score=sum(1 for i,(_,opts,ans) in enumerate(questions) if answers.get(i)==opts[ans])
        score=int(score/len(questions)*100)
        st.session_state.skor_evaluasi=score;st.session_state.challenge_best=max(st.session_state.challenge_best,score)
        award_xp(50 if score>=60 else 20,"Evaluasi");badge_check()
        st.markdown(f'<div class="challenge" style="text-align:center;margin-top:18px"><div style="font-size:4rem">{"🏆" if score>=80 else "🎯" if score>=60 else "💪"}</div><h1>{score}</h1><p style="color:#526078">Skor Challenge</p><b>{"Luar biasa! Kamu siap naik level." if score>=80 else "Bagus! Terus berlatih." if score>=60 else "Jangan menyerah. Coba lagi!"}</b></div>',unsafe_allow_html=True)

# ---------- ACHIEVEMENT ----------
elif st.session_state.halaman=="Achievement":
    page_header("Achievement Hall","Koleksi pencapaian yang kamu buka selama belajar.","🏆")
    badge_check()
    all_badges=[("🌱","First Step","Mendapatkan XP pertama"),("⚡","XP Hunter","Mengumpulkan 100 XP"),("🤖","AI Explorer","Bertanya kepada AI 5 kali"),("📚","Book Lover","Menyelesaikan minimal 2 materi"),("🎯","Quick Learner","Mendapat skor challenge minimal 80"),("🔥","Active Learner","Menyelesaikan 5 aktivitas")]
    cols=st.columns(3)
    for i,(ico,title,desc) in enumerate(all_badges):
        unlocked=any(title in b for b in st.session_state.badges)
        with cols[i%3]:
            st.markdown(f'<div class="badge-card {" " if unlocked else "badge-locked"}"><div class="medal">{ico}</div><h3>{title}</h3><p style="color:#526078">{desc}</p><b>{"UNLOCKED ✨" if unlocked else "LOCKED 🔒"}</b></div>',unsafe_allow_html=True)

st.markdown('<div class="footer"><div style="font-size:1.7rem">📚 🤖 🎮 🏆</div><b>AI Tutor Bahasa Indonesia • Ultimate 2.0</b><br><span>Belajar dengan rasa ingin tahu. Bertumbuh dengan tantangan.</span></div>',unsafe_allow_html=True)
