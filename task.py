import speech_recognition
import pyttsx3
import requests


def recognize_speech():  # Инициализация обработки голоса
    with speech_recognition.Microphone() as source:
        print("Слушаю...")
        try:
            sr = speech_recognition.Recognizer()
            sr.pause_threshold = 0.5
            sr.adjust_for_ambient_noise(source=source, duration=0.5)
            audio = sr.listen(source=source)
            query = sr.recognize_vosk(audio_data=audio, language='ru-RU').lower()
            print('Вы сказали', query)
            return query
        except speech_recognition.UnknownValueError:
            print("Извините, я не понимаю.")
            return None

        except speech_recognition.RequestError:
            print("Произошла ошибка при запросе к услуге распознавания речи.")
            return None


def execute(command):  # Обработка команд
    url = 'https://date.nager.at/api/v2/publicholidays/2024/RU'
    response = requests.get(url)
    holidays = response.json()
    if 'привет' in command:
        speak('Привет! чем я могу помочь?')
    if 'праздники' in command:
        get_holidays(holidays)
    if 'сохрани' in command:
        save_holidays(holidays)
    if 'даты' in command:
        save_date(holidays)
    if 'сколько' in command:
        cnt_holidays(holidays)

#  Функции отвечающие за соверешения команд пользователя


def get_holidays(holidays):
    speak('Список праздников в России в 2024 году')
    for holiday in holidays:
        speak(holiday['localName'])


def save_holidays(holidays):
    with open('holidays.txt', 'w') as file:
        file.write(f'Праздники\n')
    for holiday in holidays:
        name = holiday['localName']
        with open('holidays.txt', 'a') as file:
            file.write(f'{name}\n')
    speak('Список праздников записан в файл')


def save_date(holidays):
    with open('date.txt', 'w') as file:
        file.write(f'Даты праздников \n')
    for holiday in holidays:
        date = holiday['date']
        name = holiday['localName']
        with open('date.txt', 'a') as file:
            file.write(f'{name}: {date} \n')
    speak('Даты сохранены')


def cnt_holidays(holidays):
    speak(f'В 2024 году в России будет {len(holidays)} праздников')


def speak(text):  # Инициализация разговорной модели
    audi = pyttsx3.init()
    audi.say(text)
    audi.runAndWait()


if __name__ == '__main__':
    speak('Привет! Я твой помощник')
    while True:
        command = recognize_speech()
        if command:
            execute(command)
