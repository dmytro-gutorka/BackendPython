import aiohttp
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from dotenv import load_dotenv
from datetime import datetime


# logging
logging.basicConfig(level=logging.DEBUG, filename='app.log')

# load variables from virtual env
load_dotenv()
API_KEY = os.getenv("API_KEY")

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
	await message.reply(f'Hello, {message.from_user.first_name}, I\'m a WeatherBot, I can show weather of any city!')


@dp.message(Command('help'))
async def get_help(message: Message):
	await message.reply('/help - all available commands \n'
	                    '/weather - show weather \n')


@dp.message(Command('weather'))
async def get_weather(message: Message):
	await message.answer(f'What city are you looking for?')


@dp.message()
async def get_weather(message: Message):
	start_request = datetime.now()
	try:

		async with aiohttp.ClientSession() as session:
			async with session.get(
					f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}') as response:
				response = await response.json()

		await message.answer(f"Current weather in {message.text}: {response['weather'][0]['description']} \n"
		                     f"Max temperature: {response['main']['temp_max']} °F \n"
		                     f"Min temperature: {response['main']['temp_min']} °F \n")
	except Exception as e:
		await message.reply('Sorry, I couldn\'t find that city.')
	end_request = datetime.now()
	result = end_request - start_request
	logging.debug(f'Request handled in {result.microseconds / 1000} ms')


async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exiting...')
