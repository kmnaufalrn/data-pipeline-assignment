# Data Pipeline Assignment - Automobile Dataset Cleaning

## Deskripsi Dataset
Dataset otomotif yang berisi informasi spesifikasi teknis dan harga kendaraan. Data ini digunakan untuk analisis karakteristik otomotif dan prediksi harga.

## Informasi Dataset

### Ukuran Awal:
- **Total Baris:** 205
- **Total Kolom:** 30
- **Format:** CSV

### Sumber:
Kaggle - Automobile EDA Dataset

### Struktur Folder Project:
```
data-pipeline-assignment/
├── data/
│   ├── raw/
│   │   └── automobileEDA_dirty_training.csv
│   └── processed/
├── src/
│   ├── data_cleaning.ipynb
│   └── pipeline.py
├── documentation/
├── README.md
└── requirement.txt
```

---

## 🔍 Kondisi Awal Dataset

### Masalah yang Ditemukan:

#### 1. **Ketidakkonsistenan Penulisan Data**
- Merk (make): Ada huruf besar dan huruf kecil
- Tanggal (transaction_date): Format penulisan tidak konsisten

#### 2. **Kolom dengan Tipe Data Tidak Sesuai**
- Kolom int yang seharusnya kategorikal:
  - `symboling` → Kategorikal (6 nilai: 0, 1, 2, 3, -1, -2)
  - `diesel` → Kategorikal (tipe bahan bakar)
  - `gas` → Kategorikal (tipe bahan bakar)

#### 3. **Missing Values / Data Kosong**
**Kolom Kategorikal:**
- `make`: 203 non-null (2 kosong)
- `num-of-doors`: 203 non-null (2 kosong)
- `transaction_date`: 203 non-null (2 kosong)

**Kolom Numerikal:**
- `stroke`: 201 non-null (4 kosong)
- `horsepower`: 202 non-null (3 kosong)
- `price`: 202 non-null (3 kosong)

#### 4. **Distribusi Data Tidak Normal**
**Distribusi Normal (Bell Curve):**
- wheel-base, length, height, width, peak-rpm, city-mpg, highway-mpg

**Distribusi Right-Skewed (Miring ke Kanan):**
- normalized-losses, engine-size, horsepower, price, city-L/100km, compression-ratio

**Bentuk Khusus:**
- bore (bimodal), stroke (agak normal), curb-weight (left-skewed)

---

##  Data Cleaning yang Dilakukan

### Langkah 1: Klasifikasi Kolom
**Metode:** Memisahkan kolom berdasarkan tipe data (string vs numeric) kemudian menambahkan kolom integer yang seharusnya kategorikal.

**Hasil:**
- **Categorical Columns (11):** make, fuel-type, aspiration, num-of-doors, body-style, drive-wheels, engine-location, **symboling**, **diesel**, **gas**, transaction_date
- **Numerical Columns (16):** normalized-losses, curb-weight, engine-size, bore, stroke, compression-ratio, horsepower, peak-rpm, city-mpg, highway-mpg, city-L/100km, price, wheel-base, length, width, height

### Langkah 2: Cleansing Data Kategorikal
**Metode:** 
- Mengubah semua teks menjadi huruf kecil (`.str.lower()`)
- Menghapus spasi di awal/akhir (`.str.strip()`)
- Mengubah tipe data int menjadi string untuk kolom yang diperlukan

**Alasan:** Memastikan konsistensi dalam penulisan data kategorikal

**Contoh Hasil:**
```
Sebelum: "Alfa-Romero", "MAZDA", "Toyota"
Sesudah: "alfa-romero", "mazda", "toyota"
```

### Langkah 3: Transformasi Data Tanggal
**Metode:** Mengubah format string menjadi datetime dengan `pd.to_datetime()`

**Parameter:**
- `dayfirst=True` (format hari-bulan-tahun)
- `format="mixed"` (format campuran)

### Langkah 4: Imputation Missing Values - Kategorikal
**Metode:** Menggunakan **Modus** (nilai yang paling sering muncul)

**Alasan:** Untuk data kategorikal, modus adalah representasi terbaik dari nilai sentral

**Kolom yang diisi:**
- make
- num-of-doors
- Dan kolom kategorikal lainnya yang memiliki missing values

**Kode:**
```python
for category in categorical_columns:
    data_raw[category] = data_raw[category].fillna(data_raw[category].mode()[0])
```

### Langkah 5: Imputation Missing Values - Numerikal
**Metode:** Disesuaikan dengan distribusi data

| Kolom | Missing | Distribusi | Strategi | Alasan |
|-------|---------|------------|----------|--------|
| **stroke** | 4 | Agak Normal | **MEAN** | Data simetris, mean representative |
| **horsepower** | 3 | Right-Skewed | **MEDIAN** | Robust terhadap outlier |
| **price** | 3 | Right-Skewed | **MEDIAN** | Robust terhadap outlier |

**Kode:**
```python
data_raw['stroke'] = data_raw['stroke'].fillna(data_raw['stroke'].mean())
data_raw['horsepower'] = data_raw['horsepower'].fillna(data_raw['horsepower'].median())
data_raw['price'] = data_raw['price'].fillna(data_raw['price'].median())
```

---

## Hasil Cleaning

### Data Sebelum vs Sesudah:
- **Sebelum:** 205 baris, 6 kolom dengan missing values
- **Sesudah:** 205 baris, 0 missing values

### Status:
✅ Semua missing values sudah diisi
✅ Semua ketidakkonsistenan penulisan sudah diperbaiki
✅ Semua tipe data sudah sesuai
✅ Data ready untuk tahap transformasi/modeling

---

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirement.txt
```

### 3. Menjalankan Pipeline (Python Script)
```bash
python src/pipeline.py
```

---

## Lokasi Dataset

- **Raw Dataset:** `data/raw/automobileEDA_dirty_training.csv`
- **Processed Dataset:** `data/processed/` (akan dihasilkan setelah pipeline selesai)

---

##  Tools yang Digunakan

- **Python 3.12.10**
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization
- **seaborn** - Statistical visualization
- **scikit-learn** - Machine learning

---

## Notes

- Data cleaning dilakukan secara bertahap dengan dokumentasi lengkap di `data_cleaning.ipynb`

## Data Transformation

Transformasi data diimplementasikan dalam fungsi `data_transformation()` pada pipeline.

### Kolom dan Metode Transformasi

| Kolom | Metode | Alasan |
|---|---|---|
| Kolom numerik | Min-Max Scaling | Menyamakan skala nilai menjadi 0–1 |
| `body-style` | One-hot encoding | Merupakan kategori nominal |
| `drive-wheels` | One-hot encoding | Merupakan kategori nominal |
| `make` | Frequency encoding | Memiliki banyak kategori |
| `engine-type` | Frequency encoding | Mengurangi jumlah kolom baru |
| `fuel-system` | Frequency encoding | Memiliki beberapa kategori |
| `aspiration` | Label encoding | Mengubah kategori teks menjadi angka |
| `engine-location` | Label encoding | Mengubah kategori teks menjadi angka |
| `horsepower-binned` | Label encoding | Mengubah kategori teks menjadi angka |

### Alasan Pemilihan Kolom

Kolom numerik dinormalisasi menggunakan `MinMaxScaler` agar seluruh nilainya berada pada rentang 0 sampai 1. Hal ini membantu mencegah kolom dengan skala besar mendominasi proses analisis atau pemodelan.

Kolom kategorikal ditransformasi menggunakan metode encoding sesuai karakteristiknya. One-hot encoding digunakan untuk kategori nominal, frequency encoding digunakan pada kolom dengan banyak kategori, dan label encoding digunakan untuk mengubah kategori teks menjadi nilai numerik.

### Contoh Sebelum dan Sesudah Transformasi

Contoh kolom `aspiration`:

- Sebelum: `std`, `turbo`
- Sesudah: nilai numerik hasil label encoding


### Kolom atau Perubahan yang Dihasilkan

- Kolom `body-style` dan `drive-wheels` dipecah menjadi beberapa kolom baru melalui one-hot encoding.
- Kolom `make`, `engine-type`, dan `fuel-system` diubah menjadi nilai frekuensi.
- Kolom `aspiration`, `engine-location`, dan `horsepower-binned` diubah menjadi nilai numerik.
- Seluruh kolom numerik dinormalisasi menggunakan Min-Max Scaling.

## Alur ETL

Raw Dataset -> Load Data -> Data Inspection -> Data Cleaning -> Data Transformasi -> Proses new Dataset
