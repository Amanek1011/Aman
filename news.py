import os
from datetime import datetime, timedelta

from aiogram import Router, types

import aiohttp
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import keyboards as kb
load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

services_router = Router(name="services_router")


async def news_handler(message: types.Message):
    await message.answer('За какое время вам показывать новости?', reply_markup=kb.inline_news)



async def weather_handler(message: types.Message):
    weather = await get_weather()
    await message.answer(weather)



async def currency_handler(message: types.Message):
    rates = await get_currency_rates()
    await message.answer(rates)



async def back_to_main(message: types.Message):
    await message.answer(
        "Возвращаемся в главное меню",
        reply_markup=kb.reply_menu
    )


async def get_currency_rates():
    url = "https://www.nbkr.kg/XML/daily.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                xml_data = await response.text()
                root = ET.fromstring(xml_data)
                rates = {}
                for currency in root.findall('Currency'):
                    iso_code = currency.get('ISOCode')
                    value_element = currency.find('Value')
                    if iso_code and value_element is not None:
                        rates[iso_code] = value_element.text

                return (
                    "💰 Официальные курсы валют: \n\n"
                    f"🇺🇸 USD: {rates.get('USD', 'N/A')} KGS\n"
                    f"🇪🇺 EUR: {rates.get('EUR', 'N/A')} KGS\n"
                    f"🇷🇺 RUB: {rates.get('RUB', 'N/A')} KGS\n"
                    f"🇰🇿 KZT: {rates.get('KZT', 'N/A')} KGS\n"
                    f"🇨🇳 CNY: {rates.get('CNY', 'N/A')} KGS"
                )
            return "⚠️ Не удалось получить курсы валют"


async def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Бишкек&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                weather = data["weather"][0]["description"].capitalize()
                temp = data["main"]["temp"]
                feels = data["main"]["feels_like"]
                humidity = data["main"]["humidity"]
                return (
                    f"🌤 Погода в Бишкеке: \n\n"
                    f"• Состояние: {weather}\n"
                    f"• Температура: {temp}°C\n"
                    f"• Ощущается как: {feels}°C\n"
                    f"• Влажность: {humidity}%"
                )
            return "⚠️ Не удалось получить данные о погоде"

async def get_news_today():
    current_data = datetime.now().strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={current_data}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    sections = soup.find_all('div', class_="Tag--articles")

                    if not sections:
                        print("No articles found with class 'Tag--articles'.")
                        return "Не удалось найти новости."

                    news_list = []

                    for tag in sections:
                        tags = tag.find_all('div', class_="Tag--article")
                        if not tags:
                            print("No articles found in the section.")
                            return "В разделе не найдено ни одной статьи."

                        for i in tags:
                            try:
                                site = i.find('a', class_='ArticleItem--name')['href']
                                title = i.find('a', class_='ArticleItem--name').text.strip()
                                time = i.find('div', class_='ArticleItem--time').text.strip()
                                news_list.append(f'🕑 {time} | {title}'
                                                 f'  {site}')
                            except Exception as e:
                                print(f"Error extracting article data: {e}")

                    if not news_list:
                        print("No news articles were successfully parsed.")
                        return "Новости не найдены."

                    return "\n\n".join(news_list)

                else:
                    print(f"Failed to retrieve the page. Status code: {response.status}")
                    return "Ошибка при загрузке новостей."

    except Exception as e:
        print(f"Error during request or parsing: {e}")
        return "Произошла ошибка при запросе данных."



async def get_data_today():
    current_data = datetime.now().strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={current_data}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    data = soup.find('span',class_='PaginatorDate--today-text').text
                    return f' {data.replace('  ','')}'
                else:
                    print('Не получилось получить дату')
    except Exception as e:
        print(e)


async def get_news_yesterday():
    current_data = datetime.now()
    yesterday = current_data - timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={formatted_yesterday}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    sections = soup.find_all('div', class_="Tag--articles")

                    if not sections:
                        print("No articles found with class 'Tag--articles'.")
                        return "Не удалось найти новости."

                    news_list = []

                    for tag in sections:
                        tags = tag.find_all('div', class_="Tag--article")
                        if not tags:
                            print("No articles found in the section.")
                            return "В разделе не найдено ни одной статьи."

                        for i in tags:
                            try:
                                site = i.find('a', class_='ArticleItem--name')['href']
                                title = i.find('a', class_='ArticleItem--name').text.strip()
                                time = i.find('div', class_='ArticleItem--time').text.strip()
                                news_list.append(f'🕑 {time} | {title}'
                                                 f'  {site}')
                            except Exception as e:
                                print(f"Error extracting article data: {e}")

                    if not news_list:
                        print("No news articles were successfully parsed.")
                        return "Новости не найдены."

                    return "\n\n".join(news_list)

                else:
                    print(f"Failed to retrieve the page. Status code: {response.status}")
                    return "Ошибка при загрузке новостей."

    except Exception as e:
        print(f"Error during request or parsing: {e}")
        return "Произошла ошибка при запросе данных."

async def get_data_yesterday():
    current_data = datetime.now()
    yesterday = current_data - timedelta(days=1)
    formatted_yesterday = yesterday.strftime("%Y-%m-%d")
    url = f'https://kaktus.media/?lable=8&date={formatted_yesterday}&order=time'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')
                    data = soup.find('span',class_='PaginatorDate--today-text').text
                    return f' {data.replace('  ','')}'
                else:
                    print('Не получилось получить дату')
    except Exception as e:
        print(e)

async def send_long_message(message, text):
    max_length = 4096
    while len(text) > max_length:
        await message.answer(text[:max_length], disable_web_page_preview=True)
        text = text[max_length:]
    if text:
        await message.answer(text, disable_web_page_preview=True)