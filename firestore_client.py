import logging
from typing import Dict, Any, Optional
from google.cloud import firestore
from config import ENV

# 環境フラグ
IS_DEV = ENV.lower() == "dev"

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Firestore コレクション名の定数
e2e_test_collection = "e2e-test"
test_case_collection = "test-case"

def init_firestore_client() -> Optional[firestore.Client]:
    if IS_DEV:
        logger.info("ローカル環境なのでFirestoreの初期化処理はスキップします")
        return None

    try:
        return firestore.Client()
    except Exception as e:
        logger.error("Firestoreクライアントの初期化処理で想定外のエラー: %s", e)
        raise

db_client = init_firestore_client()

def save_test_result(site_id: str, test_case_id: str, result: str, error_detail: str = None) -> bool:
    if IS_DEV or db_client is None:
        logger.info("ローカル環境なのでテスト結果保存処理はスキップします")
        return False

    if not site_id or not test_case_id:
        raise RuntimeError("site_idまたはtest_case_idが空です")

    # 保存するデータを作成
    data = {
        "testRunAt": firestore.SERVER_TIMESTAMP,
        "result": result,
        "detail": error_detail or ""
    }

    try:
        doc_ref = (
            db_client
            .collection(e2e_test_collection)
            .document(site_id)
            .collection(test_case_collection)
            .document(test_case_id)
        )
        doc_ref.set(data)
        logger.info("テスト結果を保存しました。site_id=%s test_case_id=%s", site_id, test_case_id)
        return True
    except Exception as e:
        raise RuntimeError(f"テスト結果保存処理でエラー: site_id={site_id} test_case_id={test_case_id}", e)

def get_test_results_by_site(site_id: str) -> Dict[str, Dict[str, Any]]:
    if IS_DEV or db_client is None:
        logger.info("ローカル環境なのでテスト結果取得処理はスキップします")
        return {}

    if not site_id:
        raise RuntimeError("site_idが空です")

    results: Dict[str, Dict[str, Any]] = {}
    try:
        test_cases_ref = (
            db_client
            .collection(e2e_test_collection)
            .document(site_id)
            .collection(test_case_collection)
        )
        for doc in test_cases_ref.stream():
            results[doc.id] = doc.to_dict()
        logger.info("テスト結果 %d 件取得しました。site_id=%s", len(results), site_id)
    except Exception as e:
        raise RuntimeError(f"テスト結果取得処理でエラー: site_id={site_id}", e)

    return results
