import requests
from config import *
from aiogram import types
from aiogram.utils import executor
import json
import asyncio

# responce = json.loads(requests.get("https://api.steampowered.com/IGCVersion_2305270/GetClientVersion/v1/").text)

# print(responce)

async def parse_version():
    loop = asyncio.get_event_loop()
    clientParser = loop.run_in_executor(None, requests.get, "https://api.steampowered.com/IGCVersion_570/GetClientVersion/v1/")
    serverParser = loop.run_in_executor(None, requests.get, "https://api.steampowered.com/IGCVersion_570/GetServerVersion/v1/")
    clientResponce = json.loads((await clientParser).text)
    serverResponce = json.loads((await serverParser).text)
    return (clientResponce, serverResponce)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    currentClientVersion = 0
    currentServerActiveVersion = 0
    currentServerDeployVersion = 0
    while True:
        clientResponce, serverResponce = await parse_version()
        if not (clientResponce['result']['success'] and serverResponce['result']['success']):
            await message.answer('Lost connection to server')
            await asyncio.sleep(10)
            continue

        if clientResponce['result']['active_version'] != currentClientVersion:
            currentClientVersion = clientResponce['result']['active_version']
            await message.answer(f'New client version: {currentClientVersion}')
        
        if serverResponce['result']['active_version'] != currentServerActiveVersion:
            currentServerActiveVersion = serverResponce['result']['active_version']
            await message.answer(f'New server active version: {currentServerActiveVersion}')
        
        if serverResponce['result']['deploy_version'] != currentServerDeployVersion:
            currentServerDeployVersion = serverResponce['result']['active_version']
            await message.answer(f'New server deploy version: {currentServerDeployVersion}')
        

        await asyncio.sleep(5)

executor.start_polling(dp, skip_updates=False)