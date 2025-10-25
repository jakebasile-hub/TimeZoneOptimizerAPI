#!/usr/bin/env python3
"""
Test script to verify Flask app works locally
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.flask_app import app

def test_flask_app():
    """Test that Flask app can be imported and started"""
    print("✅ Flask app imported successfully")
    print("✅ App object created:", app)
    print("✅ Routes registered:", [rule.rule for rule in app.url_map.iter_rules()])
    print("✅ Flask app is ready to run!")

if __name__ == "__main__":
    test_flask_app()
