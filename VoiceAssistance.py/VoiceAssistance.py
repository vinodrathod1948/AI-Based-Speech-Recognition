import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import weathercom
import json


r = sr.Recognizer()

def voice_command_processor(ask=False):
    with sr.Microphone() as source:
        if(ask):
            audio_playback(ask)
        audio = r.listen(source,phrase_time_limit=4)
        text = ''
        try:
            text=r.recognize_google(audio)
        except sr.UnknownValueError as e:
            print(e)
        except sr.RequestError as e:
            print("service is down")

        return text.lower()



def audio_playback(text):
    filename = "test.mp3"
    tts = gTTS(text=text, lang='en-us')
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


def execute_voice_command(text):
    if "what are you" in text:
        audio_playback("i am a i voice assistance system")

    if "what is the today's weather" in text:
        city = voice_command_processor("which city")
        humidity, temp, phrase = weatherReport(city)
        audio_playback("currently in " + city + "  temperature is " + str(temp)
                       + " degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)
        print("currently in " + city + "  temperature is " + str(temp)
              + "degree celsius, " + "humidity is " + str(humidity) + " percent and sky is " + phrase)


def weatherReport(city):
    weatherDetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherDetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    return humidity, temp, phrase


while True:
    command = voice_command_processor()
    print(command)
    execute_voice_command(command)