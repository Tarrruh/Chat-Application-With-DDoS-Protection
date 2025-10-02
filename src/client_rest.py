import requests
import re
import asyncio
import websockets
import threading

usesrname = input("Enter your username: ")

pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$')
ch = input("Do you want to register or login?: ").lower()

if ch == "register":
    for i in range(4):
        password = input("Enter the password: ")
        if pattern.match(password):
            resp = requests.post("http://20.2.82.52:8000/register", data={"username":usesrname, "password": password})
            print("Try logging in now :D")
            exit()

        elif i == 3:
            print("Sorry cannot process your request!")
            exit()

        else:
            print("Password must be moe than 7 characters with uppercase, lowercase and number")
            print()

elif ch == "login":
    password = input("Enter your password: ")
    resp = requests.post("http://20.2.82.52:8000/login", data={"username": usesrname, "password": password})
    
    data = resp.json()


    if data.get("status") == "success":
        user_id = data["user"]["id"]
        print(f"Logged in successfully! Your ID: {user_id}\n")

        print("=== Your Chat History ===")
        for msg in data["chats"]:
            sender = "You" if msg["sender_id"] == user_id else f"User {msg['sender_id']}"
            receiver = "You" if msg["receiver_id"] == user_id else f"User {msg['receiver_id']}"
            print(f"[{msg['timestamp']}] {sender} -> {receiver}: {msg['message']}")
        print("========================\n")

    else:
        print(data.get("message"))
        exit()

else:
    print("Invalid option!!!")
    exit()


async def listen_messages(uid):
    async with websockets.connect(f"ws://20.2.82.52:8000/ws/{uid}") as websocket:
        print("Connected to the chat :D\n Message format: receiver_id|message")
        while True:
            msg = await websocket.recv()
            print("\n", msg)

def start_listener(uid):
    asyncio.run(listen_messages(uid))

thread_list = threading.Thread(target=start_listener, args=(user_id,), daemon=True)
thread_list.start()


while True:
    to_id = input("\n Send to user_id: ")
    content = input("Message: ")

    requests.post("http://20.2.82.52:8000/send_message", data={"sender_id": user_id, "receiver_id": to_id, "content": content})