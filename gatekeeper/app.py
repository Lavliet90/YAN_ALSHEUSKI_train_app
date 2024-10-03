from flask import Flask, jsonify, request
from datetime import datetime
from models import db, GateStatus

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gatekeeper.db'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/gate/status', methods=['GET'])
def get_gate_status():
    gate = GateStatus.query.order_by(GateStatus.id.desc()).first()
    if gate:
        return jsonify({
            'status': gate.status,
            'last_modified': gate.last_modified
        }), 200
    else:
        return jsonify({'message': 'No data found'}), 404

@app.route('/gate/status', methods=['POST'])
def update_gate_status():
    data = request.get_json()
    new_status = data.get('status')
    if new_status not in [True, False]:
        return jsonify({'error': 'Invalid status'}), 400

    gate = GateStatus.query.first()
    if gate:
        gate.status = new_status
        gate.last_modified = datetime.utcnow()
    else:
        gate = GateStatus(status=new_status, last_modified=datetime.utcnow())
        db.session.add(gate)

    db.session.commit()

    return jsonify({
        'message': f'Gate status updated to {new_status}',
        'status': new_status,
        'last_modified': gate.last_modified
    }), 200

@app.route('/')
def index():
    return "Gatekeeper Service Running", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
