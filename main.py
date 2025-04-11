from flask import Flask, request, jsonify
import json
import requests
import random
import string
import time
import os
import re
import asyncio
from aiohttp import ClientSession
from flask_cors import CORS

app = Flask(__name__)

# Path to the executors JSON file
executors_file_path = "executors.json"
executors_previous_file_path = "executors_previous.json"

# ====================================================================================================

# KEY GEN FUNCTION

# ====================================================================================================
def generate_random_hwid_fluxus(length=96):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_hwid_arceus(length=18):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_id_delta(length=64):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_id_deltaios(length=64):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_id_cryptic(length=64):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_id_hydrogen(length=10):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))


def generate_random_hwid_vegax():
    parts = []
    for _ in range(5):
        part_length = random.choice([8, 7])
        part = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(part_length))
        parts.append(part)
    return '-'.join(parts)


def generate_random_hwid_trigonevo():
    return '{}-{}-{}-{}-{}'.format(
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    )


def generate_random_id_cacti(length=64):
    letters_and_digits = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_random_hwid_evon():
    return '{}-{}-{}-{}-{}'.format(
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=4)),
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    )
    
# ====================================================================================================

# ROUTE'S 

# ====================================================================================================
@app.route('/', methods=['GET'])
def home():
    message = {
        "messages": "Invalid endpoint"
    }
    return jsonify(message)


@app.route('/api/supported', methods=['GET'])
def get_supported_links():
    return jsonify({
        'supported': SUPPORTED
    })

@app.route('/api/gen', methods=['GET'])
def generate_link():
    service = request.args.get('service')

    if service:
        if service == 'fluxus':
            random_hwid = generate_random_hwid_fluxus()
            result = f"https://flux.li/android/external/start.php?HWID={random_hwid}"
        elif service == 'arceus':
            random_hwid = generate_random_hwid_arceus()
            result = f"https://spdmteam.com/key-system-1?hwid={random_hwid}&zone=Europe/Rome&os=android"
        elif service == 'delta':
            random_id = generate_random_id_delta()
            result = f"https://gateway.platoboost.com/a/8?id={random_id}"
        elif service == 'deltaios':
            random_id = generate_random_id_deltaios()
            result = f"https://gateway.platoboost.com/a/2?id={random_id}"
        elif service == 'cryptic':
            random_id = generate_random_id_cryptic()
            result = f"https://gateway.platoboost.com/a/39097?id={random_id}"
        elif service == 'hydrogen':
            random_id = generate_random_id_hydrogen()
            result = f"https://gateway.platoboost.com/a/2569?id={random_id}"
        elif service == 'vegax':
            random_hwid = generate_random_hwid_vegax()
            result = f"https://pandadevelopment.net/getkey?service=vegax&hwid={random_hwid}&provider=linkvertise"
        elif service == 'trigon':
            random_hwid = generate_random_hwid_trigonevo()
            result = f"https://trigonevo.fun/whitelist/?HWID={random_hwid}"
        elif service == 'cacti':
            random_id = generate_random_id_cacti()
            result = f"https://gateway.platoboost.com/a/23344?id={random_id}"
        elif service == 'evon':
            random_hwid = generate_random_hwid_evon()
            result = f"https://pandadevelopment.net/getkey?service=evon&hwid={random_hwid}"
        else:
            return jsonify({"result": "Invalid executor key provided"}), 400

        return jsonify({"result": result})
    else:
        return jsonify({"result": "No valid key parameter provided"}), 400

@app.route('/search_scripts', methods=['GET'])
def search_scripts():
    query = request.args.get('q')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    url = f"https://scriptblox.com/api/script/search?q={query}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()  
            
            if 'result' in data and 'scripts' in data['result']:
                scripts_info = []
                
                for script in data['result']['scripts']:
                    script_data = {
                        "title": script.get("title"),    
                        "script": script.get("script"),  
                        "key": script.get("key"),
                        "views": script.get("views"),
                        "createdAt": script.get("createdAt"),
                        "updatedAt": script.get("updatedAt")
                    }
                    scripts_info.append(script_data)
                
                return jsonify({"result": scripts_info})
            else:
                return jsonify({"error": "No results found"}), 404
        else:
            return jsonify({"error": f"Error from API, status code: {response.status_code}"}), response.status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Helper function to load executors data  
def load_executors():  
    if not os.path.exists(executors_file_path):  
        return {}  
    with open(executors_file_path, "r") as file:  
        return json.load(file)  
  
# Helper function to save executors data  
def save_executors(executors):  
    with open(executors_file_path, "w") as file:  
        json.dump(executors, file, indent=4)  
  
# Route to fetch executor info  
@app.route('/api/executor/<platform>/<executor_name>', methods=['GET'])  
def get_executor_info(platform, executor_name):  
    executors = load_executors()  
      
    if platform in executors and executor_name in executors[platform]:  
        return jsonify(executors[platform][executor_name])  
    else:  
        return jsonify({'error': f'{executor_name.capitalize()} not found under {platform.capitalize()}'}), 404  
  
# Route to update or add an executor  
@app.route('/api/executor/<platform>/<executor_name>', methods=['POST'])  
def update_executor_info(platform, executor_name):  
    data = request.json  
  
    new_title = data.get('title')  
    new_image = data.get('image')  
    new_link = data.get('link')  
    new_version = data.get('version')  
  
    # Ensure required fields are provided  
    if not new_title or not new_image or not new_link or not new_version:  
        return jsonify({'error': 'Missing title, image, link, or version in request'}), 400  
  
    executors = load_executors()  
  
    if platform not in executors:  
        executors[platform] = {}  
  
    executors[platform][executor_name] = {  
        'title': new_title,  
        'image': new_image,  
        'link': new_link,  
        'version': new_version  
    }  
  
    save_executors(executors)  
  
    return jsonify({'message': f'{executor_name.capitalize()} info under {platform.capitalize()} updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
