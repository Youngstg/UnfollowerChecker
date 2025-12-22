"""
Vercel Serverless Entry Point
This file is required for Vercel to detect and run the Flask app
"""
from app import app

# Vercel will use this 'app' object
# No need for app.run() here - Vercel handles that
