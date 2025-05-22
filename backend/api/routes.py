from sqlalchemy.exc import IntegrityError

from flask import request, redirect, jsonify, current_app

from models import URLMapping
from extensions import db
from utils import generate_short_code

from . import api_bp

@api_bp.route('/api/v1/shorten', methods=['POST'])
def shorten_url():
    """
    Endpoint to shorten a long URL.
    Expects a JSON payload: {"long_url": "http://example.com/very/long/url"}
    """
    data = request.get_json()
    if not data or 'long_url' not in data:
        current_app.logger.warning("Shorten URL request missing 'long_url'.")
        return jsonify({"error": "Missing 'long_url' in request body"}), 400

    long_url = data['long_url']
    if not long_url.startswith(('http://', 'https://')):
        current_app.logger.warning(f"Invalid long_url format: {long_url}")
        return jsonify({"error": "long_url must start with http:// or https://"}), 400

    retries = 3
    for _ in range(retries):
        short_code = generate_short_code()
        new_mapping = URLMapping(short_code=short_code, long_url=long_url)

        try:
            db.session.add(new_mapping)
            db.session.commit()
            current_app.logger.info(f"URL Shortened: {long_url} -> {short_code}")
            full_short_url = f"{current_app.config['BASE_URL']}/{short_code}"
            return jsonify({"short_url": full_short_url, "short_code": short_code}), 201
        except IntegrityError:
            db.session.rollback() # Rollback if short_code collision
            current_app.logger.warning(f"Short code collision for {short_code}. Retrying...")
            continue # Try generating another short code
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error shortening URL: {e}")
            return jsonify({"error": "Internal server error during URL shortening"}), 500

    current_app.logger.error("Failed to generate unique short code after multiple retries.")
    return jsonify({"error": "Could not generate a unique short code. Please try again."}), 500


@api_bp.route('/<short_code>', methods=['GET'])
def redirect_to_long_url(short_code):
    """
    Endpoint to redirect a short code to its original long URL.
    """
    url_mapping = URLMapping.query.filter_by(short_code=short_code).first()

    if url_mapping:
        current_app.logger.info(f"Redirecting {short_code} to {url_mapping.long_url}")
        return redirect(url_mapping.long_url, code=302)
    else:
        current_app.logger.info(f"Short code {short_code} not found.")
        return jsonify({"error": "Short URL not found"}), 404

@api_bp.route('/_health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint.
    Checks if the Flask app is running and can connect to the database.
    """
    try:
        # Attempt a simple database query to verify connection
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"status": "healthy", "message": "Backend and DB connection are healthy"}), 200
    except Exception as e:
        current_app.logger.error(f"Health check failed: Database connection error: {e}")
        return jsonify({"status": "unhealthy", "error": f"Database connection failed: {e}"}), 500