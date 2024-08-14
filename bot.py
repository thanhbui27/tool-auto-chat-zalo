import tkinter as tk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
import time
import json

from response_bot import get_reply


root = tk.Tk()
root.title("Zalo Bot Control Panel")
root.geometry("300x300")
bot_running = False

status_label = tk.Label(root, text="Status: Stopped", fg="red")
status_label.pack(pady=10)

# Thời gian đợi để nhắn tin
timeSleep = 1

path = "chromedriver-win64/chromedriver.exe"
ser = Service(path)

driver = None  


def start_bot():
    global bot_running, driver
    if bot_running:
        return

    bot_running = True
    status_label.config(text="Status: Running", fg="green")

    driver = webdriver.Chrome()
    driver.get("https://chat.zalo.me")
    
    print("Vui lòng đăng nhập vào Zalo và nhấn Enter khi hoàn tất...")
    time.sleep(15)

    print("Bot đang chạy...")

    def learn_and_respond(message):
        response = get_reply(message)
        if response:
            return response
        return "Tôi không hiểu bạn đang nói gì, bạn thử hỏi lại xem?"

    textResponse = ''

    while bot_running:
        try:
            item = driver.find_element(By.XPATH, '//div[@data-id="div_LastSentMsg_Text"]')
            if item:
                message_element = item.find_element(By.CLASS_NAME, "text")
                message = message_element.text 
                print(f"learn_and_respond : {learn_and_respond(message)}  -  message : {message} - textResponse : {textResponse}" )
                isBot = message.startswith('#bot')

                if textResponse != message and not isBot:
                    response = learn_and_respond(message)
                    time_element = item.find_element(By.CLASS_NAME, "card-send-time__sendTime")
                    message_time = time_element.text
                    print(f"Message: {response} | Time: {message_time}")                            

                    if response:
                        input_text = driver.find_element(By.XPATH, '//div[@id="input_line_0"]')
                        input_text.click()
                        input_text.send_keys(f"#bot : {response}")
                        click_send = driver.find_element(By.XPATH, '//div[@data-translate-title="STR_SEND"]')  
                        if click_send : 
                            click_send.click()
                            textResponse = message                    
            else:
                print("pending....")     
                          
            print(f"Dừng {timeSleep}s") 
            time.sleep(timeSleep)      
        except Exception as e:
            print(f"Đang đợi tin nhắn đến")
            time.sleep(timeSleep)

def stop_bot():
    global bot_running, driver
    if not bot_running:
        return
    
    bot_running = False
    status_label.config(text="Status: Stopped", fg="red")
    if driver:
        driver.quit()

run_button = tk.Button(root, text="Run", command=lambda: Thread(target=start_bot).start(), width=10)
run_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop", command=stop_bot, width=10)
stop_button.pack(pady=5)

root.mainloop()
