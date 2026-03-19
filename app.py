from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

# Adding the project folder to path so we can import main.py
sys.path.append(r"C:\Projects\Ticketing system")
from main import User

app = Flask(__name__)
CORS(app)  # Allows the HTML frontend to talk to this server


# ── RAISE TICKET ──────────────────────────────────────────
@app.route("/raise", methods=["POST"])
def raise_ticket():
    try:
        d      = request.json
        name   = d.get("name", "").strip()
        email  = d.get("email", "").strip()
        phone  = d.get("phone", "").strip()
        ticket = d.get("ticket", "").strip()

        if not all([name, email, phone, ticket]):
            return jsonify({"error": "All fields are required"}), 400

        result = User.insert(name, email, phone, ticket)
        return jsonify({
            "message":    result["message"],
            "ticket_id":  result["ticket_id"],
            "department": result["department"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── LOOKUP FIELD ──────────────────────────────────────────
@app.route("/ticket/<ticket_id>/<field>", methods=["GET"])
def get_field(ticket_id, field):
    try:
        field_map = {
            "name":       User.read_name,
            "email":      User.read_email,
            "phone":      User.read_phonenumber,
            "ticket":     User.read_ticket,
            "status":     User.read_status,
            "department": User.read_department,
        }

        if field not in field_map:
            return jsonify({"error": f"Unknown field: {field}"}), 400

        result = field_map[field](ticket_id)

        if result is None:
            return jsonify({"error": "No ticket found"}), 404

        return jsonify({"value": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── UPDATE FIELD ──────────────────────────────────────────
@app.route("/update", methods=["PATCH"])
def update_field():
    try:
        d     = request.json
        id    = d.get("id", "").strip()
        field = d.get("field", "").strip()
        value = d.get("value", "").strip()

        if not all([id, field, value]):
            return jsonify({"error": "id, field and value are all required"}), 400

        field_map = {
            "name":   User.update_value_Name,
            "email":  User.update_value_Email,
            "phone":  User.update_value_Phone_num,
            "ticket": User.update_value_Ticket,
        }

        if field not in field_map:
            return jsonify({"error": f"Unknown field: {field}"}), 400

        result = field_map[field](id, value)
        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── DELETE TICKET ─────────────────────────────────────────
@app.route("/delete/<ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):
    try:
        result = User.delete_ticket(ticket_id)

        if result == "No ticket found":
            return jsonify({"error": result}), 404

        return jsonify({"message": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── RUN ───────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(port=5000, debug=True)
