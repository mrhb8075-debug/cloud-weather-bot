import os
import requests


def get_weather_and_recommendation(city_name, api_key):
  url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=tr'
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()
    temp = data['main']['temp']
    weather_desc = data['weather'][0]['description']
    main_weather = data['weather'][0]['main'].lower()

    recommendations = []

    if temp < 5:
      recommendations.append(
          'Hava çok soğuk! Kalın bir mont, atkı, bere ve eldiven giymelisin.'
      )
    elif 5 <= temp < 15:
      recommendations.append(
          'Hava serin. Ceket, hırka veya ince bir mont tercih edebilirsin.'
      )
    elif 15 <= temp < 22:
      recommendations.append(
          'Hava ılık. Uzun kollu bir tişört veya hafif bir sweatshirt uygun'
          ' olacaktır.'
      )
    else:
      recommendations.append(
          'Hava sıcak! İnce, pamuklu ve ferah kıyafetler/tişört giyebilirsin.'
      )

    if (
        'rain' in main_weather
        or 'drizzle' in main_weather
        or 'thunderstorm' in main_weather
    ):
      recommendations.append('Ayrıca yağmur ihtimaline karşı yanında mutlaka şemsiye bulundur!')
    elif 'snow' in main_weather:
      recommendations.append('Kar yağıyor! Su geçirmez kalın botlar giymeyi unutma.')

    full_message = f"📍 *{city_name.capitalize()}* için Hava Durumu:\n"
    full_message += f"🌡️ Sıcaklık: {temp}°C ({weather_desc.capitalize()})\n\n"
    full_message += '💡 *Günün Kıyafet Önerisi:*\n' + '\n'.join(recommendations)

    return full_message
  else:
    return None


def send_telegram_message(token, chat_id, message):
  url = f'https://api.telegram.org/bot{token}/sendMessage'
  payload = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}
  response = requests.post(url, json=payload)
  return response.json()


if __name__ == '__main__':
  # Bilgileri GitHub Secrets ortam değişkenlerinden alıyoruz
  OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
  TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
  CHAT_ID = os.getenv('CHAT_ID')
  CITY = 'Istanbul'

  print('Hava durumu verisi çekiliyor...')
  mesaj = get_weather_and_recommendation(CITY, OPENWEATHER_API_KEY)

  if mesaj:
    print('Öneri oluşturuldu, Telegram\'a gönderiliyor...')
    sonuc = send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, mesaj)

    if sonuc.get('ok'):
      print('✅ Başarılı! Mesaj Telegram botun üzerinden gönderildi.')
    else:
      print('❌ Telegram mesajı gönderilemedi. Detay:', sonuc)
  else:
    print('❌ Hava durumu verisi alınamadı.')
