from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from os import environ

POSTGRES_HOST       = environ.get('POSTGRES_HOST')
POSTGRES_USER       = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD   = environ.get('POSTGRES_PASSWORD')
POSTGRES_PORT       = environ.get('POSTGRES_PORT')

def save_to_postgresql(df, database, schema, table, mode='append'):
    """
    Menyimpan DataFrame ke table PostgreSQL.
    """
    try:
        # 1. Membuat Connection String
        # Format: postgresql://username:password@host:port/database
        conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{database}"
        
        # 2. Membuat SQLAlchemy Engine
        engine = create_engine(conn_string)
        
        # 3. Menyimpan ke SQL
        # if_exists='replace': hapus table lama dan buat baru
        # if_exists='append': tambah data ke table yang sudah ada
        # index=False: jangan simpan index dataframe sebagai kolom
        print('saving data to postgresql ...')
        df.to_sql(table, engine, schema=schema, if_exists=mode, index=False, chunksize=10000)
        
        print(f"✅ Berhasil menyimpan {len(df)} baris ke table '{table}'.")
        
    except SQLAlchemyError as e:
        print(f"❌ Terjadi kesalahan Database: {e}")
    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

def execute_query(query, database):
    """
    Menjalankan query CREATE TABLE di PostgreSQL.
    """

    conn_string = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{database}"
    engine = create_engine(conn_string)
    
    try:
        # Membuka koneksi secara eksplisit
        with engine.connect() as connection:
            # SQLAlchemy 2.0 mengharuskan penggunaan text() untuk query mentah
            connection.execute(text(query))
            # Commit diperlukan untuk menyimpan perubahan
            connection.commit()
            print("query dieksekusi!")
            
    except SQLAlchemyError as e:
        print(f"Error saat membuat tabel: {e}")
        
    finally:
        engine.dispose()