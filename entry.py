from app import app

from startup_tasks import cache_data

print("caching data")
cache_data()