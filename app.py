import time
import logging
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
from actions.factory import ActionFactory
from config import Config
from services.firestore_client import save_test_result, get_test_results_by_site

app = Flask(__name__)

# ロガー設定
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

@app.route('/run_tests', methods=['POST'])
def run_tests():
    # APIキーの検証
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {Config.API_KEY}":
        time.sleep(5)
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    target_url = data.get('target_url')
    site_id = data.get('site_id')
    test_case_id = data.get('test_case_id')
    test_case = data.get('test_case')

    # testCaseIdの存在チェックを追加
    if not target_url or not site_id or not test_case or not test_case_id:
        return jsonify({"error": "Missing target_url, test_case, site_id, or testCaseId"}), 400

    try:
        results = run_test_flow(target_url, site_id, test_case)

        try:
            save_test_result(
                site_id=site_id,
                test_case_id=test_case_id,
                result=results.get("status", "unknown")
            )
        except Exception as firestore_e:
            logger.error(f"Firestoreへのテスト結果保存中にエラーが発生しました: {firestore_e}")

        return jsonify(results), 200
    except Exception as e:
        logger.error(f"テストフロー実行中にエラーが発生しました: {e}")

        try:
            save_test_result(
                site_id=site_id,
                test_case_id=test_case_id,
                result="failed"
            )
        except Exception as firestore_e:
            logger.error(f"Firestoreへのテスト結果保存中にエラーが発生しました (テストフロー失敗時): {firestore_e}")

        return jsonify({"status": "failed", "error": str(e)}), 500

def run_test_flow(target_url: str, site_id: str, test_case: dict) -> dict:
    results = {"status": "success", "steps": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(target_url)

        for index, step in enumerate(test_case.get("steps", [])):
            try:
                action_instance = ActionFactory.create(site_id, step)
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

# 新しいエンドポイント: テスト結果取得API
@app.route('/get_results/<site_id>', methods=['GET'])
def get_results(site_id):
    # APIキーの検証
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {Config.API_KEY}":
        time.sleep(5)
        return jsonify({"error": "Unauthorized"}), 401

    if not site_id:
        return jsonify({"error": "Missing site_id"}), 400

    try:
        results = get_test_results_by_site(site_id)
        return jsonify(results), 200
    except Exception as e:
        # Firestoreからの取得エラー
        return jsonify({"error": f"Failed to retrieve results: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
