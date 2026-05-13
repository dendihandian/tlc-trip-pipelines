from datetime import datetime, timedelta
from pandas import date_range
from functools import wraps
import pytz
import time

DATE_FORMAT = '%Y-%m-%d'
DEFAULT_TIMEZONE = 'Asia/Jakarta'

def time_it(func):
    """
    Decorator untuk mengukur durasi eksekusi sebuah fungsi
    dengan output format Jam:Menit:Detik.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Catat waktu mulai (menggunakan perf_counter untuk presisi tinggi)
        start_time = time.perf_counter()
        
        # Eksekusi fungsi yang dibungkus
        result = func(*args, **kwargs)
        
        # Catat waktu selesai
        end_time = time.perf_counter()
        
        # Hitung selisih durasi
        duration_seconds = end_time - start_time
        
        # Mengonversi detik ke format jam:menit:detik menggunakan timedelta
        # .4f digunakan untuk mempertahankan presisi milidetik di bagian akhir
        readable_duration = str(timedelta(seconds=duration_seconds))
        
        print(f"⏱️  Fungsi '{func.__name__}' selesai dalam {readable_duration}")
        
        return result
    
    return wrapper

def generate_dates_range(start_date: str, end_date: str):
    return sorted([str(i)[0:10] for i in date_range(start_date, end_date)])

def generate_months_range(start_date: str, end_date: str):
    return sorted(list(set([str(i)[0:7] for i in date_range(start_date, end_date)])))

def get_current_datetime(tz: str=DEFAULT_TIMEZONE):
    return datetime.now(pytz.timezone(tz)) if tz != None else datetime.now()

def is_valid_date(date: str):
    try:
        parsed = datetime.strptime(date, DATE_FORMAT)
    except Exception:
        return False

    return True

def sub_days(dt: datetime, days: int):
    return dt - timedelta(days=days)

def add_days(dt: datetime, days: int):
    return dt + timedelta(days=days)