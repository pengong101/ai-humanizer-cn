#!/usr/bin/env python3
"""IPv4 HTTP Proxy → SearXNG IPv6 (127.0.0.1:8080)"""
import http.server, urllib.request, urllib.error, ssl

LISTEN_PORT = 8081
BACKEND_HOST = "::1"
BACKEND_PORT = 8080

class Proxy(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url = f"http://[{BACKEND_HOST}]:{BACKEND_PORT}{self.path}"
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, headers=dict(self.headers))
            req.add_header('Host', self.headers.get('Host', ''))
            with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
                self.send_response(r.status)
                for k, v in r.headers.items():
                    if k.lower() not in ('transfer-encoding','connection','keep-alive'):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(r.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"error: {e}".encode())

    do_POST = lambda s: s._proxy("POST")
    do_HEAD = lambda s: s._proxy("HEAD")
    
    def _proxy(self, method):
        cl = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(cl) if cl else b''
        url = f"http://[{BACKEND_HOST}]:{BACKEND_PORT}{self.path}"
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            req = urllib.request.Request(url, data=body, headers=dict(self.headers), method=method)
            with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
                self.send_response(r.status)
                for k, v in r.headers.items():
                    if k.lower() not in ('transfer-encoding','connection'):
                        self.send_header(k, v)
                self.end_headers()
                if method != "HEAD":
                    self.wfile.write(r.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
        except Exception as e:
            self.send_response(502)
            self.end_headers()

    def log_message(self, fmt, *args): pass

if __name__ == "__main__":
    s = http.server.HTTPServer(('0.0.0.0', LISTEN_PORT), Proxy)
    print(f"IPv4→IPv6 Proxy: 0.0.0.0:{LISTEN_PORT} → [{BACKEND_HOST}]:{BACKEND_PORT}", flush=True)
    s.serve_forever()
