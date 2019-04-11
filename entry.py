from app import app

print("Server startup ...")


from startup_tasks import cache_data

print("Caching missing data ...")
cache_data()
