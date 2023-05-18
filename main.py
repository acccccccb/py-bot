from src.modules.speak.main import speak

while True:
    try:
        # 从命令行接收输入文本
        text = input("请输入要读出的文本：")
        speak(text)

    except KeyboardInterrupt:
        # 捕捉 Ctrl+C，退出循环
        break

# 销毁语音引擎
print('exit')