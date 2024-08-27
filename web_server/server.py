from flask import Flask, jsonify, render_template, request, redirect
from flask_mqtt import Mqtt
#from flask_socketio import SocketIO, emit
import json
import csv
import os
from datetime import datetime
import pytz

app = Flask(__name__) 
tz = pytz.timezone('Asia/Taipei')

# IP變數
esp32_ip = None

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

# 發佈mqtt消息的函式
def publish_mqtt_msg(topic, payload):
    print(f"發布了mqtt的主題 {topic}: {payload}")
    #將訊息發布到指定的 MQTT 主題上
    mqtt.publish(topic, payload)
    #mqtt.publish(topic, json.dumps(payload)) #Python 字典轉換為 JSON 格式的字符串#JSON 格式的數據

# 将接收到的数据写入 CSV 文件
def write_to_csv(topic, payload):
    try:
        # 获取当前的日期和时间
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        csv_file_path = './web_server/sensor_data.csv'#寫完整路徑


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

# 当连接到 MQTT Broker 时-订阅 MQTT 推播到 Broker 的主题
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("已經連上mqtt broker")
    mqtt.subscribe("school/esp32/ip")  # 訂閱 IP 主題
    mqtt.subscribe('sui_hsilan/iot_house_esp32/sensor_data')  # 订阅 ESP32 发送的主题


# 當收到 MQTT 消息時處理消息
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global esp32_ip, latest_msg
    try:
        if message.topic == "school/esp32/ip":
            esp32_ip = message.payload.decode()  # 更新 esp32_ip 變數
            print("從ESP32收到 IP位址: " + esp32_ip)
        else:
            payload = json.loads(message.payload.decode())  # 解码消息并转换为 JSON 格式
            topic = message.topic  # 获取主题

            # 保存最新的消息
            latest_msg = {
                "time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "topic": topic,
                "data": payload
            }
            print("收到 MQTT 訊息:", latest_msg)

            # 将接收到的数据写入 CSV
            if write_to_csv(topic, payload):
                print("資料存入CSV")
            else:
                print("存取資料失敗")
    except Exception as e:
        print(f"讀取mqtt消息失敗: {str(e)}")


# 定义一个 API 端点来查看最新消息
@app.route('/latest_msg')
def get_latest_msg():
    return jsonify(latest_msg)

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
        csv_file_path = './web_server/sensor_data.csv'
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            csv_reader = list(csv.reader(file))
            # 获取最新的 50 条记录
            data = [row for row in csv_reader[-50:][::-1] if len(row) == 3 and all(row)]
        print("Read data from CSV:", data)
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
    
    return render_template('temp.html', data=data, temperature=temperature, humidity=humidity, time=time)



@app.route('/<string:page_name>') 
def html_page(page_name): 
    return render_template(page_name)

# 路由：控制單一主題的Rgb燈
@app.route('/control_light', methods=['POST'])
def control_light(): #用於處理前端發送的 HTTP POST 請求
    try:
        #{ "action": "ON"} { "action": "OFF"}{ "action": "BLINK"}
        #取得前端傳送過來的data
        data = request.json
        #取出指令on/off/blink
        action = data.get('action')
        #發布消息的主題(單獨控制開關/ 控制BLINK=>sui_hsilan/iot/led_4)：
        #取出主題
        topic = data.get('topic')
        
        #action狀態處理(傳回去只需要字符串 不需要json)
        if action == "ON":
            payload = "ON"
        elif action == "OFF":
            payload = "OFF"
        elif action == "BLINK":
            payload = "BLINK"    
        else:
            return jsonify({"error": "不存在的action"})

        # 發布MQTT主題：關全燈/開全燈
        print(f"{payload},{topic}")
        publish_mqtt_msg(topic, payload)
    
        return jsonify({"status": "發佈主題4成功"})
    except Exception as e:
        print(f"單獨控制出錯：{str(e)}")
        return jsonify({"error": str(e)}), 500

# POST路由：控制總開關主題的Rgb燈
@app.route('/control_all_lights', methods=['POST'])
def control_all_lights():
    try:
        #{ "action": "ON"} { "action": "OFF"}
        #取得前端傳送過來的data
        data = request.json
        action = data.get('action')
        #發布消息的主題(控制總開關=>sui_hsilan/iot/led_4)：
        topic = "sui_hsilan/iot/led_4"
        
        #action狀態處理(傳回去只需要字符串 不需要json)
        if action == "ON":
            payload = "ON"
        elif action == "OFF":
            payload = "OFF"
        else:
            return jsonify({"error": "不存在的action"})

        # 發布MQTT主題：關全燈/開全燈
        print(f"{payload}")
        publish_mqtt_msg(topic, payload)
    
        return jsonify({"status": "發佈主題4成功"})
    except Exception as e:
        print(f"總開關控制出錯：{str(e)}")
        return jsonify({"error": str(e)}), 500

#取的esp32 ip端點
@app.route('/get_ip', methods=['GET'])
def get_ip():
    return jsonify({"ip": esp32_ip})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)

