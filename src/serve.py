"""
Inference HTTP Microservice for TurkishTextClassifier.
Provides inference endpoints using Python standard library http.server.
Endpoints:
  GET  /health
  GET  /models/metadata
  POST /inference/predict
  POST /inference/predict/batch
"""

import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add src/model to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "model")))
from predict import TurkishTextClassifierService

service = None

class InferenceHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-API-Key")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "success": True,
                "status": "healthy",
                "model": "TurkishTextClassifier",
                "version": "1.0.0"
            })
        elif self.path in ["/models/metadata", "/metadata"]:
            meta_path = "artifacts/model/metadata.json"
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                self._send_json(200, {"success": True, "data": meta})
            else:
                self._send_json(404, {"success": False, "error": "Metadata file not found"})
        else:
            self._send_json(404, {
                "success": False,
                "error": {"code": "ERR_404", "message": f"Endpoint '{self.path}' not found"}
            })

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            self._send_json(400, {
                "success": False,
                "error": {"code": "INVALID_JSON", "message": "Failed to parse JSON body"}
            })
            return

        if self.path in ["/inference/predict", "/predict"]:
            # Supports {"text": "..."} or {"texts": ["...", "..."]}
            texts = []
            if "text" in payload:
                texts = [payload["text"]]
            elif "texts" in payload:
                texts = payload["texts"]
            else:
                self._send_json(400, {
                    "success": False,
                    "error": {"code": "MISSING_FIELD", "message": "Field 'text' or 'texts' is required"}
                })
                return

            t0 = time.time()
            predictions = []
            for t in texts:
                res = service.predict(t)
                predictions.append({
                    "class_name": res["prediction"],
                    "confidence": res["confidence"],
                    "probabilities": res["probabilities"],
                    "text": t
                })
            latency_ms = (time.time() - t0) * 1000

            self._send_json(200, {
                "success": True,
                "data": {
                    "model": "TurkishTextClassifier",
                    "version": "1.0.0",
                    "predictions": predictions,
                    "latency_ms": round(latency_ms, 3)
                }
            })
        else:
            self._send_json(404, {
                "success": False,
                "error": {"code": "ERR_404", "message": f"Endpoint '{self.path}' not found"}
            })

def start_server(port: int = 8080):
    global service
    print("Loading TurkishTextClassifier model...")
    service = TurkishTextClassifierService()
    print(f"Model loaded successfully! Initializing Inference Microservice on port {port}...")
    server = HTTPServer(("0.0.0.0", port), InferenceHandler)
    print(f"[ONLINE] Inference Server running at http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_server(port)
