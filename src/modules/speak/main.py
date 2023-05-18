import pyttsx3

engine = pyttsx3.init()
engine.setProperty('voice', 'Microsoft Huihui Desktop')
# 获取可用的语音列表
voices = engine.getProperty('voices')

# 打印语音列表
for voice in voices:
    print("ID:", voice.id)
    print("Name:", voice.name)
    print("Languages:", voice.languages)
    print("Gender:", voice.gender)
    print("Age:", voice.age)
    print("\n")

engine.setProperty('rate', 200)



def speak(msg):
    print(msg)
    engine.say(msg)
    engine.runAndWait()
    engine.stop()
