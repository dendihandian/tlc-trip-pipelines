from pandas import read_parquet, read_csv
from pandas import DataFrame
from hashlib import md5
from pyarrow.lib import ArrowInvalid
import urllib.request
import urllib.error

def create_df(records_dict: dict = {}):
    return DataFrame(records_dict)

def generate_md5(df: DataFrame, columns_to_hash: list = None):
    if columns_to_hash is None:
        columns_to_hash = df.columns.tolist()
    
    combined_series = df.astype(str).apply(lambda x: '|'.join(str(x)), axis=1)
    
    df['_md5'] = combined_series.apply(
        lambda x: md5(x.encode('utf-8')).hexdigest()
    )

    return df

def read_parquet_from_url(url):
    """
    Membaca file parquet dari URL dengan penanganan error yang spesifik.
    """
    try:
        # 1. Cek apakah URL valid dan bisa diakses
        # (Langkah opsional sebelum read_parquet untuk verifikasi cepat)
        df = read_parquet(url, engine='pyarrow')
        return df

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Error 404: File tidak ditemukan di URL tersebut. Pastikan bulan/tahun sudah benar.")
        else:
            print(f"❌ Error HTTP: Terjadi masalah koneksi dengan kode {e.code}")
            
    except ArrowInvalid:
        print("❌ Error: File ditemukan tetapi formatnya bukan Parquet yang valid atau rusak.")
        
    except FileNotFoundError:
        print("❌ Error: URL tidak valid atau tidak dapat ditemukan.")
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan yang tidak terduga: {e}")
        
    return None

def read_csv_from_url(url):
    """
    Membaca file csv dari URL dengan penanganan error yang spesifik.
    """
    try:
        # 1. Cek apakah URL valid dan bisa diakses
        # (Langkah opsional sebelum read_csv untuk verifikasi cepat)
        df = read_csv(url, engine='pyarrow')
        return df

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Error 404: File tidak ditemukan di URL tersebut. Pastikan bulan/tahun sudah benar.")
        else:
            print(f"❌ Error HTTP: Terjadi masalah koneksi dengan kode {e.code}")
            
    except ArrowInvalid:
        print("❌ Error: File ditemukan tetapi formatnya bukan csv yang valid atau rusak.")
        
    except FileNotFoundError:
        print("❌ Error: URL tidak valid atau tidak dapat ditemukan.")
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan yang tidak terduga: {e}")
        
    return None