from flask import Flask, request, jsonify
from datetime import datetime
from zoneinfo import ZoneInfo  # Only available in Python 3.9+

app = Flask(__name__)

# Token setup
API_TOKEN = "supersecrettoken123"

# Sample database of capital cities and timezones
capital_timezones = {
    "Washington": "America/New_York",
    "London": "Europe/London",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Beijing": "Asia/Shanghai",
    "Canberra": "Australia/Sydney",
    "Ottawa": "America/Toronto",
    "New Delhi": "Asia/Kolkata",
    "Brasília": "America/Sao_Paulo"
}

# Token decorator
def token_required(f):
    def decorator(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token == API_TOKEN:
                return f(*args, **kwargs)
        return jsonify({"error": "Unauthorized - Invalid or missing token"}), 401

    decorator.__name__ = f.__name__
    return decorator

# API endpoint for current time
@app.route('/api/time', methods=['GET'])
@token_required
def get_time():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    city_clean = city.strip().title()
    if city_clean not in capital_timezones:
        return jsonify({"error": f"City '{city}' not found in database"}), 404

    tz_name = capital_timezones[city_clean]
    now = datetime.now(ZoneInfo(tz_name))
    offset = now.utcoffset()
    hours = int(offset.total_seconds() // 3600)
    minutes = int((offset.total_seconds() % 3600) // 60)
    utc_offset = f"UTC{'+' if hours >= 0 else ''}{hours:02d}:{minutes:02d}"

    return jsonify({
        "city": city_clean,
        "local_time": now.strftime('%Y-%m-%d %H:%M:%S'),
        "utc_offset": utc_offset
    })

# Root route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, world!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
