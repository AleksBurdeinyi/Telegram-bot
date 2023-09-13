import telebot
import json
from telebot import types
import requests
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('6615985960:AAFLRpAu7U3WgjMsasCsKQqqCH8BVTa94hM')
API = '9f4743eb9adab6a9087580bc491ded2b'
currency = CurrencyConverter()
amount = 0
@bot.message_handler(commands=['start'])
def konvert(message):
    bot.send_message(message.chat.id,f'Привіт {message.from_user.first_name},введи будь-ласка суму конвертації:')
    bot.register_next_step_handler(message,summa)

def summa(message):
    global amount

    try:
        amount = int(message.text.strip())
    except ValueError:
          bot.send_message(message.chat.id, 'Неправильний формат,Впишіть правильну суму')
          bot.register_next_step_handler(message, summa)
          return
    if amount >0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types .InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Друге значення ', callback_data='else')
        markup.add(btn1,btn2,btn3,btn4)
        bot.send_message(message.chat.id,'Вибиріть пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неправильний формат,Впишіть правильне число більше за 0')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    values = call.data.upper().split('/')
    con = currency.convert(amount,values[0],values[1])
    bot.send_message(call.message.chat.id, f'Получается:{round(con,2)}. Можеш попробувати заново')
    bot.register_next_step_handler(call.message, summa)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hello! {message.from_user.first_name},напиши город:')




country_flags = {
    "TR": '🇹🇷',  # Turkey
    "UA": '🇺🇦',  # Ukraine
    "US": '🇺🇸',  # United States
    "FR": '🇫🇷',  # France
    "DE": '🇩🇪',  # Germany
    "IT": '🇮🇹',  # Italy
    "JP": '🇯🇵',  # Japan
    "CN": '🇨🇳',  # China
    "BR": '🇧🇷',  # Brazil
    "CA": '🇨🇦',  # Canada
    "GB": '🇬🇧',  # United Kingdom
    "AU": '🇦🇺',  # Australia
    "RU": '🇷🇺',  # Russia
    "IN": '🇮🇳',  # India
    "SA": '🇸🇦',  # Saudi Arabia
    "ZA": '🇿🇦',  # South Africa
    "KR": '🇰🇷',  # South Korea
    "MX": '🇲🇽',  # Mexico
    "AR": '🇦🇷',  # Argentina
    "ES": '🇪🇸',  # Spain
    "PT": '🇵🇹',  # Portugal
    "GR": '🇬🇷',  # Greece
    "EG": '🇪🇬',  # Egypt
    "TH": '🇹🇭',  # Thailand
    "ID": '🇮🇩',  # Indonesia
    "NG": '🇳🇬',  # Nigeria
    "KE": '🇰🇪',  # Kenya
    "ZA": '🇿🇦',  # South Africa
    "CA": '🇨🇦',  # Canada
    "MX": '🇲🇽',  # Mexico
    "AR": '🇦🇷',  # Argentina
    "CL": '🇨🇱',  # Chile

}

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code== 200:
        data = json.loads(res.text)

        country_code = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']

        country_flag = country_flags.get(country_code, "🏳️")
        weather_emojis = {
            "Clear": "☀️",  # Clear sky
            "Clouds": "☁️",  # Cloudy
            "Rain": "🌧️",  # Rainy
            "Snow": "❄️",  # Snowy

        }
        weather_description = data['weather'][0]['main']
        weather_emoji = weather_emojis.get(weather_description, "🌦️")

        weather_info = (
            f'Країна: {country_code}{country_flag}\n'
            f'Зараз погода: {temp}°C{weather_emoji}\n'
            f'Температура зараз: {temp}°C\n'
            f'Відчувається: {feels_like}°C\n'
            f'Мінімальна Температура: {temp_min}°C\n'
            f'Максимальна Температура: {temp_max}°C'
        )

        bot.reply_to(message, weather_info)




bot.polling(none_stop=True)