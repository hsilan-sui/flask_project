from flask import Flask, jsonify, render_template, request, redirect
from flask_mqtt import Mqtt
import json
import csv
import os
from datetime import datetime

app = Flask(__name__) 

#最新消息
latest_msg = {}

# MQTT 配置
app.config['MQTT_BROKER_URL'] = 'mqttgo.io'  # MQTT Broker 地址
app.config['MQTT_BROKER_PORT'] = 1883  # MQTT 端口
app.config['MQTT_USERNAME'] = ''  # MQTT 用户名（如果需要）
app.config['MQTT_PASSWORD'] = ''  # MQTT 密码（如果需要）
app.config['MQTT_KEEPALIVE'] = 60  # 心跳包间隔
app.config['MQTT_TLS_ENABLED'] = False  # 如果需要加密则设置为 True

mqtt = Mqtt(app)

# 將接收到的數據寫入csv檔
def write_to_csv(topic, payload):
    try:
        # 获取当前的日期和时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 打开或创建 CSV 文件并追加数据
        with open('sensor_data.csv', mode="a", newline='', encoding='utf-8') as database:
            csv_writer = csv.writer(database, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            # 提取 JSON 中的数据
            distance = payload.get('distance', 'N/A')
            temperature = payload.get('temperature', 'N/A')
            humidity = payload.get('humidity', 'N/A')
            
            # 写入 CSV 文件
            csv_writer.writerow([current_time, topic, distance, temperature, humidity])
        
        return True
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")
        return False
    

@app.route("/") 
def home(): 
    return render_template('index.html')

@app.route('/<string:page_name>') 
def html_page(page_name): 
    return render_template(page_name)

# 模擬資料庫txt
# def write_to_files(data):
#     with open('dtatbase.txt',mode='a') as database:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    try:
        # csv_path = os.path.join(app.root_path, 'database.csv')
        with open('database.csv', mode="a", newline='', encoding='utf-8') as database2:
            subject = data['subject']
            message = data['message']
            csv_writer = csv.writer(database2, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([ subject, message])
        return True
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")
        return False
# def write_to_csv(data):
#     with open('database.csv', mode="a", encoding='utf-8') as database2:
#         email = data['email']
#         subject = data['subject']
#         message = data['message']
#         csv_writer = csv.writer(database2, delimiter=',', quotechar='|', quoting='csv.QUOTE_MINIMAL')
#         csv_writer.writerow([email, subject, message])

# 当连接到 MQTT Broker 时-訂閱mqtt推播到broker的主題
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sui_hsilan/iot_house_esp32/sensor_data')  # 订阅 ESP32 发送的主题


# 当收到 MQTT 消息时
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())  # 解码消息并转换为 JSON 格式
        topic = message.topic  # 获取主题

        # 将接收到的数据写入 CSV
        if write_to_csv(topic, payload):
            print("Data saved to CSV")
        else:
            print("Failed to save data")
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")



#定義一個api端點來查看消息
@app.route('/latest_msg')
def get_lastest_msg():
    return jsonify(latest_msg)

# 定義使用者提交表單的API端點 以及 收到表單資料後 要回傳給前端的內容
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
            # print(data)
        if write_to_csv(data):
            return redirect('/thankyou.html')
        else:
            return 'Failed to save to database'
    else:
        return 'something went wrong, Try again!'