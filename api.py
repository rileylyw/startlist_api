import json

from flask import Flask, request, jsonify

from utils import search_entry

# Using Flask because it's lightweight and seems suitable for the use case
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Startlist API!!!!!'


with open('startlists.json', 'r') as file:
    startlists_data = json.load(file)


@app.route('/api/v1/startlists', methods=['GET'])
def get_startlists():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 10, type=int)

    start = (page - 1) * per_page
    end = start + per_page
    data = startlists_data[start:end]

    total_items = len(startlists_data)
    total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)

    return jsonify({
        "data": data,
        "meta": {
            "currentPage": page,
            "perPage": per_page,
            "totalItems": total_items,
            "totalPages": total_pages
        }
    })


@app.route('/api/v1/startlists/add', methods=['POST'])
def add_startlist():
    new_entry = request.json

    required_fields = [
        "id", "eventId", "raceId", "ticketId", "eventTitle",
        "raceTitle", "ticketTitle", "createdAt", "updatedAt", "fields"
    ]

    # all fields are required in the JSON object (see README.md for details)
    missing_fields = [field for field in required_fields if field not in new_entry]
    if missing_fields:
        return jsonify({"error": "Missing required fields", "missing": missing_fields}), 400

    # `fields` shuold contain 'id', 'name', 'value'
    if any('id' not in field or 'name' not in field or 'value' not in field for field in new_entry.get('fields', [])):
        return jsonify({"error": "Invalid structure in 'fields'"}), 400

    startlists_data.append(new_entry)

    with open('startlists.json', 'w') as file:
        json.dump(startlists_data, file, indent=4)

    return jsonify({"message": "New startlist entry added successfully."}), 201


@app.route('/api/v1/startlists/delete/<id>', methods=['DELETE'])
def delete_startlist(id):
    updated_startlists_data = [entry for entry in startlists_data if entry['id'] != id]

    with open('startlists.json', 'w') as f:
        json.dump(updated_startlists_data, f, indent=4)

    return jsonify({"message": "Deleted successfully"}), 200


@app.route('/api/v1/startlists/search')
def search_startlists():
    # get all entries that match the query string
    query = request.args.get('query', '')
    if not query:
        return jsonify([]), 400

    matching_entries = []
    for entry in startlists_data:
        if search_entry(entry, query):
            matching_entries.append(entry)

    return jsonify(matching_entries), 200


@app.route('/api/v1/startlists/search/<id>', methods=['GET'])
def get_startlist_by_id(id):
    matching_entry = next((entry for entry in startlists_data if entry['id'] == id), None)

    if matching_entry:
        return jsonify(matching_entry)
    else:
        return jsonify({"message": "Entry not found"}), 404
