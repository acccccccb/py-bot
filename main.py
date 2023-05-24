from src.modules.speak.main import speak
from src.modules.gamepad.main import gamepad

while True:
    try:
        print("\nAvailable options:")
        print("1. speaker")
        print("2. gamepad")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            speak()
        elif choice == '2':
            gamepad()
        else:
            print("Exit")
            break

    except KeyboardInterrupt:
        # 捕捉 Ctrl+C，退出循环
        break