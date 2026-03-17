import os
from flask import Flask, jsonify, request, abort
from fragment_api_lib.client import FragmentAPIClient
from fragment_api_lib.exceptions import FragmentAPIError
from dotenv import load_dotenv
import logging
from waitress import serve

load_dotenv()

class Config:
    SEED = os.getenv("SEED")
    FRAGMENT_COOKIES = os.getenv("FRAGMENT_COOKIES")
    PORT = int(os.getenv("PORT", 8080))

def validate_positive_int(value, name):
    try:
        iv = int(value)
        if iv <= 0:
            raise ValueError()
        return iv
    except Exception:
        raise ValueError(f"{name} должен быть положительным целым числом")

def make_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    logging.basicConfig(level=logging.INFO)
    app.logger = logging.getLogger("fragment_api_wrapper")

    client = FragmentAPIClient()

    def safe_call(description):
        def decorator(fn):
            def wrapper(*args, **kwargs):
                try:
                    result = fn(*args, **kwargs)
                    return {"success": True, "description": description, "data": result}
                except FragmentAPIError as e:
                    app.logger.error(f"{description} — FragmentAPIError: {e}")
                    return {"success": False, "error": f"Fragment API Error: {str(e)}"}
                except Exception as e:
                    app.logger.exception(f"{description} — unexpected error")
                    return {"success": False, "error": f"{type(e).__name__}: {str(e)}"}
            wrapper.__name__ = fn.__name__
            return wrapper
        return decorator

    @app.route("/ping", methods=["GET"])
    def ping():
        resp = safe_call("Ping API")(client.ping)()
        return jsonify(resp)

    @app.route("/balance", methods=["GET"])
    def get_balance():
        if not app.config["SEED"]:
            abort(500, description="SEED не задан")
        resp = safe_call("Get Balance")(client.get_balance)(seed=app.config["SEED"])
        return jsonify(resp)

    @app.route("/user/<username>", methods=["GET"])
    def get_user(username):
        if not app.config["FRAGMENT_COOKIES"]:
            abort(500, description="FRAGMENT_COOKIES не задан")
        resp = safe_call("Get User Info")(client.get_user_info)(
            username=username, fragment_cookies=app.config["FRAGMENT_COOKIES"]
        )
        return jsonify(resp)

    @app.route("/buy_stars", methods=["POST"])
    def buy_stars():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"success": False, "error": "Неверный JSON"}), 400
        username = payload.get("username")
        amount = payload.get("amount")
        if not username or amount is None:
            return jsonify({"success": False, "error": "username и amount обязательны"}), 400
        try:
            amount = validate_positive_int(amount, "amount")
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400

        resp = safe_call("Buy Stars")(client.buy_stars)(
            username=username,
            amount=amount,
            show_sender=False,
            fragment_cookies=app.config["FRAGMENT_COOKIES"],
            seed=app.config["SEED"],
        )
        return jsonify(resp)

    @app.route("/buy_stars_nokyc", methods=["POST"])
    def buy_stars_nokyc():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"success": False, "error": "Неверный JSON"}), 400
        username = payload.get("username")
        amount = payload.get("amount")
        if not username or amount is None:
            return jsonify({"success": False, "error": "username и amount обязательны"}), 400
        try:
            amount = validate_positive_int(amount, "amount")
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400

        resp = safe_call("Buy Stars (No KYC)")(client.buy_stars_without_kyc)(
            username=username,
            amount=amount,
            seed=app.config["SEED"],
        )
        return jsonify(resp)

    @app.route("/buy_premium", methods=["POST"])
    def buy_premium():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"success": False, "error": "Неверный JSON"}), 400
        username = payload.get("username")
        duration = payload.get("duration", 3)
        if not username:
            return jsonify({"success": False, "error": "username обязательны"}), 400
        try:
            duration = validate_positive_int(duration, "duration")
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400

        resp = safe_call("Buy Premium")(client.buy_premium)(
            username=username,
            duration=duration,
            show_sender=False,
            fragment_cookies=app.config["FRAGMENT_COOKIES"],
            seed=app.config["SEED"],
        )
        return jsonify(resp)

    @app.route("/buy_premium_nokyc", methods=["POST"])
    def buy_premium_nokyc():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"success": False, "error": "Неверный JSON"}), 400
        username = payload.get("username")
        duration = payload.get("duration", 3)
        if not username:
            return jsonify({"success": False, "error": "username обязательны"}), 400
        try:
            duration = validate_positive_int(duration, "duration")
        except ValueError as e:
            return jsonify({"success": False, "error": str(e)}), 400

        resp = safe_call("Buy Premium (No KYC)")(client.buy_premium_without_kyc)(
            username=username,
            duration=duration,
            seed=app.config["SEED"]
        )
        return jsonify(resp)

    return app

if __name__ == "__main__":
    app = make_app()
    serve(app, host="0.0.0.0", port=app.config["PORT"])
