import json
import time
import os
import random
from flask import Flask, jsonify, request, Response
from itertools import cycle

app = Flask(__name__)

# Segédfüggvény, amely betölti a busz koordinátákat a JSON fájlból
def load_bus_coordinates(bus_id):
    try:
        file_path = os.path.join(os.getcwd(), f'routes_{bus_id}.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['busRoute']
    except FileNotFoundError:
        return None

# API endpoint, amely visszaadja a busz koordinátáit lépésről lépésre
@app.route('/bus/<int:bus_id>/movement', methods=['GET'])
def get_bus_movement(bus_id):
    coordinates = load_bus_coordinates(bus_id)
    
    if not coordinates:
        return jsonify({"error": "Bus data not found"}), 404

    # Choose a random starting index
    start_index = random.randint(0, len(coordinates) - 1)
    rotated_coordinates = coordinates[start_index:] + coordinates[:start_index]

    # Infinite loop that simulates bus movement
    def generate_coordinates():
        for coord in cycle(rotated_coordinates):
            yield f"data: {json.dumps({'lat': coord[0], 'lon': coord[1]})}\n\n"
            time.sleep(1)  # Move every second (simulating movement speed)

    return Response(generate_coordinates(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

