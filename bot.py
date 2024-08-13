from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

from Trie import Trie

#thời gian đợi để nhắn tin
timeSleep = 1

path = "chromedriver-win64/chromedriver.exe"
ser = Service(path)

driver = webdriver.Chrome(service=ser)

driver.get("https://chat.zalo.me")

print("Vui lòng đăng nhập vào Zalo và nhấn Enter khi hoàn tất...")

time.sleep(15)

trie = Trie()

try:
    with open('bot_data.json', 'r', encoding='utf-8') as file:
        bot_data = json.load(file)
        for keyword, response in bot_data.items():
            trie.insert(keyword, response)
except FileNotFoundError:
    bot_data = {}

print("Load trie thanh cong")

def save_bot_data():
    with open('bot_data.json', 'w', encoding='utf-8') as file:
        json.dump(bot_data, file, ensure_ascii=False, indent=4)

def learn_and_respond(message):
    response = trie.search(message.lower())
    
    if response:
        return response[0]
    
    response = ""
    bot_data[message.lower()] = response
    trie.insert(message.lower(), response)
    save_bot_data()
    return response

textResponse = ''

while True:
    try:
        # item = driver.find_element(By.XPATH, '//div[@data-id="div_LastSentMsg_Text"]')
        item = driver.find_element(By.XPATH, '//div[@data-id="div_LastReceivedMsg_Text"]')
        if item :
            message_element = item.find_element(By.CLASS_NAME, "text")
            message = message_element.text 

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
    except KeyboardInterrupt:
        print("Dừng lắng nghe.")
        break
    except Exception as e:
        print(f"đang đợi tin nhắn đến")
        # print(f"Có lỗi xảy ra: {e}")
        time.sleep(timeSleep)

driver.quit()
