import threading


def start_thread():
    th = threading.Thread(target=read_commands)
    th.start()


def read_commands():
    while True:
        input1 = input()
        if input1 == "/add_admin_chat":
            input2 = input("Ok. Give me invite link")

