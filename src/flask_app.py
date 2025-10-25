from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
from typing import Optional, List, Dict, Any

from timezone_optimizer import TimezoneOptimizer
from auth import auth_manager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize optimizer
optimizer = TimezoneOptimizer()

# Track startup time for uptime calculation
start_time = time.time()


def get_api_key():
    """Extract and validate API key from headers"""
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return None, "API key required. Include 'X-API-Key' header."
    
    if not auth_manager.validate_api_key(api_key):
        return None, "Invalid API key"
    
    return api_key, None


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    return jsonify({"status": "ok", "uptime": uptime})


@app.route('/optimize', methods=['POST'])
def optimize_meeting_time():
    """
    Find optimal meeting time for participants across timezones.
    """
    try:
        # Validate API key
        api_key, error = get_api_key()
        if error:
            return jsonify({"error": error}), 401
        
        # Check rate limit
        if not auth_manager.check_rate_limit(api_key):
            return jsonify({"error": "Rate limit exceeded. Free tier allows 100 requests per day."}), 429
        
        # Log usage
        auth_manager.log_usage(api_key, "/optimize")
        
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON data required"}), 400
        
        # Validate request
        participants = data.get("participants", [])
        duration_minutes = data.get("duration_minutes", 60)
        num_alternatives = data.get("num_alternatives", 3)
        
        if not participants or len(participants) < 2:
            return jsonify({"error": "At least 2 participants are required"}), 400
        
        # Convert request to optimizer format
        participant_list = [
            {"name": p["name"], "location": p["location"]}
            for p in participants
        ]
        
        # Find optimal meeting time
        result = optimizer.find_optimal_meeting_time(
            participants=participant_list,
            duration_minutes=duration_minutes,
            num_alternatives=num_alternatives
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Error optimizing meeting time: {str(e)}"}), 500


@app.route('/usage', methods=['GET'])
def get_usage_stats():
    """Get usage statistics for the API key"""
    api_key, error = get_api_key()
    if error:
        return jsonify({"error": error}), 401
    
    return jsonify({"message": "Usage stats endpoint - implement as needed"})


@app.route('/create-key', methods=['POST'])
def create_api_key():
    """Create a new API key (for testing purposes)"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        new_key = auth_manager.create_api_key(user_id)
        return jsonify({"api_key": new_key, "message": "API key created successfully"})
    except Exception as e:
        return jsonify({"error": f"Error creating API key: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
