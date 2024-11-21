# 用于进行本地接口测试 有flask依赖
# 在本地的良Python环境下，可以自行创建文件uploads与results文件夹
# 并在results放置123.png后进行运行测试
# 注意服务器本地地址，以此调整前端接口url
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import time
import threading
import uuid

app = Flask(__name__)
CORS(app)  # 添加 CORS 支持

UPLOAD_FOLDER = './uploads'  # 上传文件夹
RESULT_FOLDER = './results'  # 结果文件夹
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# 模拟任务存储
tasks = {}

# 模拟任务处理的函数
def process_task(task_id, file_path):
    time.sleep(5)  # 模拟处理时间
    if os.path.exists(file_path):
        # 模拟生成处理后的图像
        result_path = os.path.join(RESULT_FOLDER, f"{task_id}.png")
        # with open(file_path, 'rb') as f:
        #     with open(result_path, 'wb') as result_file:
        #         result_file.write(f.read())  # 简单拷贝模拟
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result_path'] = result_path
        print("生成处理后图像")
    else:
        tasks[task_id]['status'] = 'error'

@app.route('/process', methods=['POST'])
def handle_post():
    # 从请求中提取查询参数
    model_type = request.args.get('pretrained_model_name')
    scale = request.args.get('target_scale')

    print(f"Received Model Type: {model_type}")
    print(f"Received Scale: {scale}")

    # 检查文件部分
    if 'image' not in request.files:
        print("No image part in request")
        return jsonify({"error": "No image part"}), 400

    image = request.files['image']

    # 检查是否有选择文件
    if image.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400

    print(image.filename)

    # 保存图像到上传文件夹
    file_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(file_path)
    print(f"Image saved at: {file_path}")

    # 创建任务
    task_id = "123"
    tasks[task_id] = {
        "status": "processing",
        "file_path": file_path
    }

    # 开启一个线程处理任务
    threading.Thread(target=process_task, args=(task_id, file_path)).start()

    # 返回任务 ID 和初始状态
    return jsonify({
        "status": "processing",
        "task_id": task_id
    })

@app.route('/get_status', methods=['GET'])
def get_status():
    task_id = request.args.get('task_id')
    if not task_id or task_id not in tasks:
        return jsonify({"error": "Invalid task_id"}), 400

    task_status = tasks[task_id]['status']
    return jsonify({"status": task_status})

@app.route('/get_result', methods=['GET'])
def get_result():
    task_id = request.args.get('task_id')
    if not task_id or task_id not in tasks:
        return jsonify({"error": "Invalid task_id"}), 400

    if tasks[task_id]['status'] != 'completed':
        return jsonify({"error": "Task not completed"}), 400

    result_path = tasks[task_id]['result_path']
    if not os.path.exists(result_path):
        return jsonify({"error": "Result file not found"}), 500

    # 返回结果文件
    return send_file(result_path, mimetype='image/jpeg')

if __name__ == "__main__":
    app.run(debug=True)
