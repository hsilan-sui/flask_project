from flask import Flask, jsonify, render_template, request, redirect
from flask_mqtt import Mqtt
import json
import csv
import os
from datetime import datetime

app = Flask(__name__) 

# 最新消息
latest_msg = {}

# MQTT 配置
app.config['MQTT_BROKER_URL'] = 'mqttgo.io'  # MQTT Broker 地址
app.config['MQTT_BROKER_PORT'] = 1883  # MQTT 端口
app.config['MQTT_USERNAME'] = ''  # MQTT 用户名（如果需要）
app.config['MQTT_PASSWORD'] = ''  # MQTT 密码（如果需要）
app.config['MQTT_KEEPALIVE'] = 60  # 心跳包间隔
app.config['MQTT_TLS_ENABLED'] = False  # 如果需要加密则设置为 True

mqtt = Mqtt(app)


# 将接收到的数据写入 CSV 文件
def write_to_csv(topic, payload):
    try:
        # 获取当前的日期和时间
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        csv_file_path = 'sensor_data.csv'

        # 检查 CSV 文件的行数
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = list(csv.reader(file))
            row_count = len(csv_reader)

        # 如果行数超过 150，则清空文件
        if row_count >= 300:
            mode = "w"  # 清空文件
        else:
            mode = "a"  # 追加数据

        # 打开文件并写入数据
        with open(csv_file_path, mode=mode, newline='', encoding='utf-8') as database:
            csv_writer = csv.writer(database, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            # 提取 JSON 中的数据，并提供默认值以避免 KeyError
            distance = payload.get('distance', 'N/A')
            temperature = payload.get('temperature', 'N/A')
            humidity = payload.get('humidity', 'N/A')
            
            # 写入 CSV 文件
            csv_writer.writerow([current_time, temperature, humidity])
        
        return True
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")
        return False


@app.route("/") 
def home(): 
    return render_template('index.html')

@app.route("/temp")
def show_temp():
    data = []
    temperature = latest_msg.get("data", {}).get("temperature", "--")
    humidity = latest_msg.get("data", {}).get("humidity", "--")
    time = latest_msg.get("time", "--")
    
    try:
        with open('sensor_data.csv', mode='r', encoding='utf-8') as file:
            csv_reader = list(csv.reader(file))
            data = [row for row in csv_reader[-40:][::-1] if len(row) == 3 and all(row)]
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Time:", time)
    print("Data:", data)
    
    return render_template('temp.html', data=data, temperature=temperature, humidity=humidity, time=time)


@app.route('/<string:page_name>') 
def html_page(page_name): 
    return render_template(page_name)

# 当连接到 MQTT Broker 时-订阅 MQTT 推播到 Broker 的主题
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('sui_hsilan/iot_house_esp32/sensor_data')  # 订阅 ESP32 发送的主题


# 当收到 MQTT 消息时
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global latest_msg
    try:
        payload = json.loads(message.payload.decode())  # 解码消息并转换为 JSON 格式
        topic = message.topic  # 获取主题

        # 保存最新的消息
        latest_msg = {
            "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "topic": topic,
            "data": payload
        }
        print("Received MQTT message:", latest_msg)
        # 将接收到的数据写入 CSV
        if write_to_csv(topic, payload):
            print("Data saved to CSV")
        else:
            print("Failed to save data")
    except Exception as e:
        print(f"Error processing MQTT message: {str(e)}")


# 定义一个 API 端点来查看最新消息
@app.route('/latest_msg')
def get_latest_msg():
    return jsonify(latest_msg)


# 定义用户提交表单的 API 端点 以及收到表单数据后要返回给前端的内容
# @app.route('/submit_form', methods=['POST', 'GET'])
# def submit_form():
#     if request.method == 'POST':
#         data = request.form.to_dict()
#         # print(data)
#         if write_to_csv(data.get('topic', 'N/A'), data):
#             return redirect('/thankyou.html')
#         else:
#             return 'Failed to save to database'
#     else:
#         return 'Something went wrong, Try again!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
