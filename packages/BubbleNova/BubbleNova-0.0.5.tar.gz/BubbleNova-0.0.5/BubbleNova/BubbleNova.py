import subprocess
import threading
import os
import sys

def __start_threads(bot_dir):
    subprocess.call([sys.executable, '-u', bot_dir])

def start_bots(bot_list: dict):
    threads = []
    for bot in bot_list:
        bot_dir = bot_list[bot]
        thread = threading.Thread(target=__start_threads, args=(bot_dir,))
        thread.start()
        threads.append(thread)



# if __name__ == "__main__":
#     bot_list = {
#         "SoapBot": "bots/SoapBot.py",
#         "Bubbles": "bots/Bubbles.py"
#     }
#     start_bots(bot_list)
#     print("This code here can still run even though the bots are also still online!")