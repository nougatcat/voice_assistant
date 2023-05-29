import queue
import sys
import sounddevice as sd            #перехват звука из микрофона и воспроизведение аудио на динамики
import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import phrases 
from abilities import *  

from vosk import Model, KaldiRecognizer

q = queue.Queue()

model = Model('vosk_stt_model_ru')

device = sd.default.device          #device[0] - хранит номер входного устр, [1] - выходного
samplerate = int(sd.query_devices(device[0],'input')['default_samplerate'])


def callback(indata, frames, time, status):         #запись данных в очередь
    q.put(bytes(indata))

def recognize(data,vectorizer,clf):
    trigger_name = phrases.NAME_OF_ASSISTANT.intersection(data.split())         #split разбивает строку на отдельные слова, разделитель - пробел
    
    if not trigger_name:            #если у множества ввода нет пересечения со множеством имен ассистента, то выходим из функции
        return

    data.replace(list(trigger_name)[0],'')          #заменить на пробел имя бота (это лишняя фраза)
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    func_name = answer.split()[0]           #первое слово - это имя функции, которую может выполнить бот
    speaker(answer.replace(func_name,''))           #удаляем имя функции из строки, чтобы бот его не говорил
    exec(func_name + '()')

def main():
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(phrases.data_set.keys()))           #конвертируем ключи в список и передаем в модуль, который делает из этого списка векторы,эти векторы делают так, чтобы программа ассоциировала слова на входе с фразами из phrases

    clf = LogisticRegression()
    clf.fit(vectors, list(phrases.data_set.values()))           #ответы из словаря будут сопоставляться с вектором

    #RawInputStream использует устройство ввода по умолчанию, blocksize - сколько информации будет отдавать поток на обработку, больше 48000 нет смысла ставить, но чем больше, тем медленнее
    with sd.RawInputStream(samplerate=samplerate, blocksize = 16000, device=device[0], dtype="int16", channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)

        while True:         #слушаем аудиопоток
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']         #json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary. 
                print(f"Ваши слова распознаны как: {data}")
                recognize(data, vectorizer, clf)            #передача ассистенту сформированных фраз

if __name__ == '__main__':
    #speaker('Запускаюсь, ждите')
    main()