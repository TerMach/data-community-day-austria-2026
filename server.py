#!/usr/bin/env python3
"""
Simple Flask server with CORS proxy for Claude API
This allows the frontend to make API calls through our backend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for all routes

# Track API usage and costs
api_usage = {
    'today': datetime.now().strftime('%Y-%m-%d'),
    'count': 0,
    'estimated_cost': 0.0
}

MAX_DAILY_REQUESTS = 200  # Safety limit (increased for spend-based model)
MAX_DAILY_COST = 30.0  # $30 budget cap

# Load API key from config.js
def get_api_key():
    try:
        with open('config.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract API key from config.js
            for line in content.split('\n'):
                if 'ANTHROPIC_API_KEY' in line and 'sk-ant-' in line:
                    # Extract key between quotes
                    start = line.find("'sk-ant-")
                    if start == -1:
                        start = line.find('"sk-ant-')
                    if start != -1:
                        start += 1  # Skip the quote
                        end = line.find("'", start)
                        if end == -1:
                            end = line.find('"', start)
                        if end != -1:
                            return line[start:end]
    except Exception as e:
        print(f"Error reading API key: {e}")
    return None

# Try environment variable first (production), then config.js (local)
API_KEY = os.environ.get('ANTHROPIC_API_KEY') or get_api_key()

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Proxy endpoint for Claude API with rate limiting and budget monitoring"""
    global api_usage

    if not API_KEY:
        return jsonify({
            'error': 'API key not configured',
            'message': 'Please add your Anthropic API key to config.js'
        }), 500

    # Check if conference is over (after January 23, 2026)
    conference_date = datetime(2026, 1, 23).date()
    today_date = datetime.now().date()

    if today_date > conference_date:
        print(f"⚠️ Conference is over. No API calls allowed after {conference_date}")
        return jsonify({
            'error': 'Conference ended',
            'message': 'The conference has ended. The chatbot is now sleeping after a great job!'
        }), 403

    # Reset counter if new day
    today = datetime.now().strftime('%Y-%m-%d')
    if api_usage['today'] != today:
        api_usage = {'today': today, 'count': 0, 'estimated_cost': 0.0}

    # Check daily request limit
    if api_usage['count'] >= MAX_DAILY_REQUESTS:
        print(f"⚠️ Daily request limit reached: {api_usage['count']}/{MAX_DAILY_REQUESTS}")
        return jsonify({
            'error': 'Daily limit reached',
            'message': f"Daily request limit ({MAX_DAILY_REQUESTS}) exceeded. This helps control costs."
        }), 429

    # Check daily cost limit
    if api_usage['estimated_cost'] >= MAX_DAILY_COST:
        print(f"⚠️ Daily cost limit reached: ${api_usage['estimated_cost']:.2f}/${MAX_DAILY_COST}")
        return jsonify({
            'error': 'Budget limit reached',
            'message': f"Daily budget limit (${MAX_DAILY_COST}) exceeded. Come back tomorrow!"
        }), 429

    try:
        # Get request data from frontend
        data = request.json
        message = data.get('message', '')
        print(f"📥 Chat request #{api_usage['count'] + 1}: {message[:50]}...")

        # Make request to Claude API
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': API_KEY,
                'anthropic-version': '2023-06-01'
            },
            json={
                'model': 'claude-sonnet-4-20250514',
                'max_tokens': 1024,
                'messages': [{
                    'role': 'user',
                    'content': data.get('prompt', '')
                }]
            },
            timeout=30
        )

        # Check if request was successful
        if response.status_code != 200:
            print(f"API error: {response.status_code}")
            print(f"Response: {response.text}")
            return jsonify({
                'error': f'API error: {response.status_code}',
                'details': response.text
            }), response.status_code

        # Return Claude's response
        result = response.json()

        # Track usage and calculate actual cost
        api_usage['count'] += 1

        # Calculate actual cost from token usage
        usage_data = result.get('usage', {})
        input_tokens = usage_data.get('input_tokens', 1000)
        output_tokens = usage_data.get('output_tokens', 500)

        # Claude Sonnet 4 pricing: $3/M input, $15/M output
        actual_cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)
        api_usage['estimated_cost'] += actual_cost

        print(f"✅ API call #{api_usage['count']} successful")
        print(f"📊 Tokens: {input_tokens} in, {output_tokens} out")
        print(f"💰 This call: ${actual_cost:.4f}, Today's total: ${api_usage['estimated_cost']:.2f}")

        # Add cost to response for frontend tracking
        result['cost'] = actual_cost

        return jsonify(result)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timeout'}), 504
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'api_key_configured': API_KEY is not None and API_KEY != 'YOUR_API_KEY_HERE'
    })

@app.route('/api/usage', methods=['GET'])
def usage():
    """Get API usage statistics"""
    return jsonify({
        'date': api_usage['today'],
        'requests': api_usage['count'],
        'estimated_cost': round(api_usage['estimated_cost'], 2),
        'max_requests': MAX_DAILY_REQUESTS,
        'max_cost': MAX_DAILY_COST,
        'remaining_requests': max(0, MAX_DAILY_REQUESTS - api_usage['count']),
        'remaining_budget': max(0, MAX_DAILY_COST - api_usage['estimated_cost'])
    })

if __name__ == '__main__':
    if not API_KEY:
        print("WARNING: No API key found in config.js")
        print("The chatbot will not work without an API key")
        print("Add your key to config.js and restart the server")
    else:
        print("API key loaded successfully")

    print("\nStarting server...")
    print("Open: http://localhost:5000")
    print("Press Ctrl+C to stop\n")

    # Try port 5000, if busy try 5001, 5002, etc.
    import socket
    port = 5000
    for attempt_port in range(5000, 5010):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', attempt_port))
            sock.close()
            port = attempt_port
            break
        except:
            continue

    print(f"Using port: {port}\n")
    app.run(host='0.0.0.0', port=port, debug=True)
