import json
import os
import sys
import time
import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from dotenv import load_dotenv, dotenv_values

import status

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
console_handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
logger.addHandler(console_handler)


@app.post(path="/notify")
def notify(stat: status.Status):
    last_respond_time[stat.name] = time.time()
    logger.info(f"script:{stat.name}; camera status {stat.camera_status}; script status {stat.script_status}")


# load_dotenv()
config = dotenv_values(".env")
last_respond_time: dict[str, float] = {}
CHECK_INTERVAL = int(config["CHECK_INTERVAL"])
RESPONSE_INTERVAL = int(config["RESPONSE_INTERVAL"])
places = json.loads(config["PLACES"])
for place in places:
    last_respond_time[place] = time.time()


@app.on_event("startup")
@repeat_every(seconds=CHECK_INTERVAL)
def check_status():
    cur_time = time.time()
    for key in last_respond_time:
        if cur_time - last_respond_time[key] > RESPONSE_INTERVAL:
            logger.error(f"{key} dose not response the last {cur_time - last_respond_time[key]:.2f} seconds")


if __name__ == "__main__":
    uvicorn.run(app, host=config["HOST"], port=int(config["PORT"]))
