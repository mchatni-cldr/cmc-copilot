# ============================================================
# FILE: backend/app.py (FIXED - Returns correct investigation_id)
# ============================================================
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from services.orchestration_service import InvestigationService
from services.data_service import DataService

app = Flask(__name__)
CORS(app)

# Initialize services
investigation_service = InvestigationService()
data_service = DataService()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "CMC Co-Pilot API"})

@app.route('/api/batch-info', methods=['GET'])
def get_batch_info():
    """Get current batch information"""
    batch_info = data_service.get_batch_info()
    return jsonify(batch_info.dict())

@app.route('/api/investigation/start', methods=['POST'])
def start_investigation():
    """Start a new batch deviation investigation"""
    data = request.json
    batch_id = data.get('batch_id', 'P25-003')
    
    # Start investigation (runs in background thread) and get the actual investigation_id
    investigation_id = investigation_service.start_investigation(batch_id)
    
    print(f"[API] Started investigation with ID: {investigation_id}")
    
    return jsonify({
        "investigation_id": investigation_id,  # This is now the actual UUID
        "status": "started",
        "message": "Investigation started successfully"
    })

@app.route('/api/investigation/<investigation_id>/status', methods=['GET'])
def get_investigation_status(investigation_id):
    """Get current status of an investigation"""
    print(f"[API] Checking status for investigation: {investigation_id}")
    status = investigation_service.get_investigation_status(investigation_id)
    
    if not status:
        print(f"[API] Investigation {investigation_id} not found")
        print(f"[API] Available investigations: {list(investigation_service.investigations.keys())}")
        return jsonify({"error": "Investigation not found"}), 404
    
    # Convert to dict for JSON serialization
    status_dict = status.dict()
    print(f"[API] Returning status: {status_dict['status']}, agents: {len(status_dict['agents'])}")
    return jsonify(status_dict)

@app.route('/api/investigation/<investigation_id>/report', methods=['GET'])
def get_investigation_report(investigation_id):
    """Get final investigation report"""
    status = investigation_service.get_investigation_status(investigation_id)
    
    if not status:
        return jsonify({"error": "Investigation not found"}), 404
    
    if not status.final_report:
        return jsonify({"error": "Report not yet available"}), 404
    
    return jsonify(status.final_report)

@app.route('/api/debug/investigations', methods=['GET'])
def debug_investigations():
    """Debug endpoint to see all investigations"""
    investigations = {}
    for inv_id, inv_status in investigation_service.investigations.items():
        investigations[inv_id] = {
            "id": inv_id,
            "status": inv_status.status,
            "agent_count": len(inv_status.agents),
            "agents": [
                {
                    "id": agent.agent_id,
                    "name": agent.agent_name,
                    "status": agent.status,
                    "task_count": len(agent.tasks)
                }
                for agent in inv_status.agents
            ]
        }
    return jsonify(investigations)

if __name__ == '__main__':
    print(f"[APP] Starting CMC Co-Pilot API on port {Config.FLASK_PORT}")
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=(Config.FLASK_ENV == 'development')
    )