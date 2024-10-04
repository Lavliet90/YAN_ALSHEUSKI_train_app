from flask import Flask, jsonify, request
from datetime import datetime
from models import db, GateStatus
import pytz
from settings_gatekeeper import SQLALCHEMY_DATABASE_URI, FLASK_HOST, FLASK_PORT

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

db.init_app(app)

poland_tz = pytz.timezone("Europe/Warsaw")

with app.app_context():
    db.create_all()


@app.route("/gate/status", methods=["GET"])
def get_gate_status():
    gate = GateStatus.query.order_by(GateStatus.id.desc()).first()
    if gate:
        return (
            jsonify(
                {"status": gate.status, "last_modified": gate.last_modified}
            ),
            200,
        )
    else:
        default_status = {
            "status": True,
            "last_modified": datetime.now(poland_tz).isoformat(),
        }
        return jsonify(default_status), 200


@app.route("/gate/status", methods=["POST"])
def update_gate_status():
    data = request.get_json()
    new_status = data.get("status")
    if new_status not in [True, False]:
        return jsonify({"error": "Invalid status"}), 400

    gate = GateStatus.query.first()
    if gate:
        gate.status = new_status
        gate.last_modified = datetime.now(poland_tz)
    else:
        gate = GateStatus(
            status=new_status, last_modified=datetime.now(poland_tz)
        )
        db.session.add(gate)

    db.session.commit()

    return (
        jsonify(
            {
                "message": f"Gate status updated to {new_status}",
                "status": new_status,
                "last_modified": gate.last_modified,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT)
