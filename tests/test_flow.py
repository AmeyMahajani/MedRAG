import os
import unittest

from src.medrag import create_app


class AppFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["MEDRAG_FAKE_MODE"] = "true"

    def setUp(self) -> None:
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_home_page_loads(self) -> None:
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MedRAG", response.data)

    def test_chat_requires_message(self) -> None:
        response = self.client.post("/api/chat", json={})
        self.assertEqual(response.status_code, 400)

    def test_chat_returns_answer(self) -> None:
        response = self.client.post(
            "/api/chat", json={"message": "What is diabetes?"}
        )
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("answer", payload)


if __name__ == "__main__":
    unittest.main()
