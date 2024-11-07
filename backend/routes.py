from . import app
import os
import json
from flask import jsonify, request

# Load JSON data from a file
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

# Save updated data back to the JSON file
def save_data():
    with open(json_url, 'w') as f:
        json.dump(data, f, indent=4)

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return the length of the data"""
    if data:
        return jsonify(length=len(data)), 200
    return jsonify({"message": "Internal server error"}), 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if picture:
        return jsonify(picture), 200
    return jsonify({"message": "Picture not found"}), 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.get_json()

    # Check if picture with the same ID already exists
    if any(item["id"] == picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
    
    # Add the new picture to the data list
    data.append(picture)
    
    # Save updated data to the file
    save_data()

    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture by ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return jsonify({"message": "Picture not found"}), 404

    # Ensure JSON data is valid and update fields
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"message": "Invalid input"}), 400
    
    # Update only provided fields, e.g., "url", "event_country", etc.
    for key in ["pic_url", "event_country", "event_state", "event_city", "event_date"]:
        if key in updated_data:
            picture[key] = updated_data[key]
    
    # Save updated data to the file
    save_data()

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    picture_to_delete = next((picture for picture in data if picture['id'] == id), None)
    
    if picture_to_delete:
        data.remove(picture_to_delete)  # Remove the picture from the list
        
        # Save updated data to the file
        save_data()
        
        return '', 204  # No content, successful deletion
    else:
        return jsonify({"message": "picture not found"}), 404  # Picture not found, return 404
