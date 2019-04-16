import os
from app import app
import redis
from rq import Worker, Queue, Connection

listen = [app.config["OPTIMIZER_QUEUE"], app.config["CACHING_QUEUE"]]

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
