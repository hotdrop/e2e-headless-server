from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from actions.factory import ActionFactory
from config import Config

app = Flask(__name__)

@app.route('/run_tests', methods=['POST'])
def run_tests():
    # APIキーの検証
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {Config.API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    target_url = data.get('target_url')
    test_case = data.get('test_case')

    if not target_url or not test_case:
        return jsonify({"error": "Missing target_url or test_case"}), 400

    try:
        results = run_test_flow(target_url, test_case)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)}), 500

def run_test_flow(target_url: str, test_case: dict) -> dict:
    results = {"status": "success", "steps": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url)

        for index, step in enumerate(test_case.get("steps", [])):
            try:
                action_instance = ActionFactory.create(step)
                result = action_instance.execute(page)
                result["step"] = index + 1
                result["action"] = step.get("action")
            except Exception as e:
                result = {
                    "step": index + 1,
                    "action": step.get("action"),
                    "status": "failed",
                    "error": str(e)
                }
            results["steps"].append(result)
            if result["status"] == "failed":
                results["status"] = "failed"

        browser.close()

    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
