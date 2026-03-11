"""
Antigravity Qwen Bridge Proxy
Routes OpenAI-compatible requests to local Ollama Qwen 3.5
Runs on port 4000
"""
import json
import asyncio
import http.server
import socketserver
import urllib.request
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

OLLAMA_BASE = "http://localhost:11434"
PORT = 4000

class QwenBridgeHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[QWEN-BRIDGE] {args[0]}")

    def _send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.end_headers()

    def do_GET(self):
        if self.path == "/v1/models":
            # Fetch from Ollama and translate
            try:
                req = urllib.request.Request(f"{OLLAMA_BASE}/api/tags")
                with urllib.request.urlopen(req) as resp:
                    ollama_data = json.loads(resp.read())
                models = []
                for m in ollama_data.get("models", []):
                    models.append({
                        "id": m["name"],
                        "object": "model",
                        "created": 0,
                        "owned_by": "ollama-local",
                        "permission": [],
                        "root": m["name"],
                        "parent": None
                    })
                # Also expose as gpt-4o alias
                models.append({
                    "id": "gpt-4o",
                    "object": "model",
                    "created": 0,
                    "owned_by": "ollama-local-alias",
                    "permission": [],
                    "root": "qwen3.5:latest",
                    "parent": None
                })
                self._send_json(200, {"object": "list", "data": models})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        elif self.path == "/health" or self.path == "/":
            self._send_json(200, {"status": "ok", "bridge": "qwen-antigravity"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}

        if self.path == "/v1/chat/completions":
            self._handle_chat(data)
        elif self.path == "/chat/completions":
            self._handle_chat(data)
        else:
            self._send_json(404, {"error": "endpoint not found"})

    def _handle_chat(self, data):
        model = data.get("model", "qwen3.5:latest")
        # Map gpt-4o alias to actual model
        if model == "gpt-4o":
            model = "qwen3.5:latest"
        
        messages = data.get("messages", [])
        stream = data.get("stream", False)
        temperature = data.get("temperature", 0.7)

        ollama_payload = json.dumps({
            "model": model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": temperature}
        }).encode()

        req = urllib.request.Request(
            f"{OLLAMA_BASE}/api/chat",
            data=ollama_payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            if stream:
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()

                with urllib.request.urlopen(req) as resp:
                    buffer = b""
                    while True:
                        chunk = resp.read(1)
                        if not chunk:
                            break
                        buffer += chunk
                        if chunk == b"\n":
                            line = buffer.decode().strip()
                            buffer = b""
                            if not line:
                                continue
                            try:
                                ollama_chunk = json.loads(line)
                                openai_chunk = {
                                    "id": "chatcmpl-qwen",
                                    "object": "chat.completion.chunk",
                                    "created": 0,
                                    "model": model,
                                    "choices": [{
                                        "index": 0,
                                        "delta": {
                                            "content": ollama_chunk.get("message", {}).get("content", "")
                                        },
                                        "finish_reason": "stop" if ollama_chunk.get("done") else None
                                    }]
                                }
                                sse_data = f"data: {json.dumps(openai_chunk)}\n\n"
                                hex_len = hex(len(sse_data.encode()))[2:]
                                self.wfile.write(f"{hex_len}\r\n".encode())
                                self.wfile.write(sse_data.encode())
                                self.wfile.write(b"\r\n")
                                self.wfile.flush()
                            except:
                                pass
                
                # Final chunk
                self.wfile.write(b"5\r\n")
                self.wfile.write(b"data: [DONE]\n\n")
                self.wfile.write(b"\r\n")
                self.wfile.write(b"0\r\n\r\n")
                self.wfile.flush()
            else:
                with urllib.request.urlopen(req) as resp:
                    full_response = ""
                    for line in resp:
                        decoded = line.decode().strip()
                        if decoded:
                            try:
                                chunk = json.loads(decoded)
                                full_response += chunk.get("message", {}).get("content", "")
                            except:
                                pass

                    openai_response = {
                        "id": "chatcmpl-qwen",
                        "object": "chat.completion",
                        "created": 0,
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": full_response
                            },
                            "finish_reason": "stop"
                        }],
                        "usage": {
                            "prompt_tokens": 0,
                            "completion_tokens": 0,
                            "total_tokens": 0
                        }
                    }
                    self._send_json(200, openai_response)
        except Exception as e:
            self._send_json(500, {"error": f"Ollama bridge error: {str(e)}"})


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), QwenBridgeHandler)
    print(f"[QWEN-BRIDGE] OpenAI-compatible proxy live on port {PORT}")
    print(f"[QWEN-BRIDGE] Routing to Ollama at {OLLAMA_BASE}")
    print(f"[QWEN-BRIDGE] Endpoint: http://localhost:{PORT}/v1/chat/completions")
    server.serve_forever()
