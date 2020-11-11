
import requests
import urllib

URL = "https://api.telegram.org/bot1233621326:AAGpLbIGPcYhH-oiDEKT4VaRjacui47ru2I/"


def send_telegram_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + \
        "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(
            text, chat_id)

    response = requests.get(url)
    print("Message sent status code: ", response.status_code)


def send_alerts(alerts):
    plantation = alerts[0].station.plantation
    text = "Alerta! Os seguintes valores estão fora do ideal: \n"

    for reading in alerts:
        text += reading.parameter.get_parameter_name() + ": " + str(reading.value) + "\n"

    for u in plantation.get_all_users():
        if u.chat_id:
            send_telegram_message(text, u.chat_id)
