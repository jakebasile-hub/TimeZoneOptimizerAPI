#!/usr/bin/env python3
"""
Render deployment startup script for TimeZone Optimizer API
"""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set environment variables
os.environ['PYTHONPATH'] = 'src'

if __name__ == "__main__":
    import uvicorn
    from src.simple_main import app
    
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
