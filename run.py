#!/usr/bin/env python3
"""
Production runner for the Voice-Based AI News Assistant web application.
This script is suitable for deployment on platforms like Heroku, Railway, Render, etc.
"""

import os
from app import app

if __name__ == '__main__':
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 5000))

    # Run in production mode
    app.run(host='0.0.0.0', port=port, debug=False)