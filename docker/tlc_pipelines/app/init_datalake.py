"""
docker-compose exec tlc_pipelines python init_datalake.py
"""

import os
from sqlalchemy import create_engine, text

def init_datalake():
    try:
        # 1. Ambil konfigurasi dari Environment Variables
        db_user = os.environ["POSTGRES_USER"]
        db_password = os.environ["POSTGRES_PASSWORD"]
        db_host = os.environ.get("POSTGRES_HOST", "localhost")
        db_port = os.environ.get("POSTGRES_PORT", "5432")
        
        target_db = "datalake"
        target_schemas = ["landing", "raw", "transformed", "curated", "master"]
        
        # 2. Koneksi awal ke database 'postgres' untuk membuat database 'datalake'
        base_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
        engine = create_engine(base_url)

        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            # Cek apakah database 'datalake' sudah ada
            db_exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"), 
                {"name": target_db}
            ).scalar()
            
            if not db_exists:
                print(f"🚀 Membuat database utama: {target_db}")
                conn.execute(text(f"CREATE DATABASE {target_db}"))
            else:
                print(f"✅ Database '{target_db}' sudah tersedia.")

        # 3. Koneksi ke database 'datalake' untuk membuat semua schema
        datalake_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{target_db}"
        datalake_engine = create_engine(datalake_url)
        
        with datalake_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            print(f"📦 Menginisialisasi skema di dalam '{target_db}':")
            for schema_name in target_schemas:
                print(f"  └─ 📁 Membuat schema: {schema_name}")
                conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))

        print("\n✨ Infrastruktur Datalake berhasil disiapkan!")

    except KeyError as e:
        print(f"❌ Kesalahan Konfigurasi: Environment variable {e} tidak ditemukan!")
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    init_datalake()