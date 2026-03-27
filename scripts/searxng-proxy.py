#!/usr/bin/env python3
"""反向代理：将主机8081端口请求转发到 SearXNG 容器内IP（用curl实现）"""
import http.server, subprocess, shutil, os

SEARXNG_TARGET = "http://172.18.0.3:8080"

class Proxy(http.server.BaseHTTPRequestHandler):
    def _forward(self, method):
        path = self.path
        # 读取请求体
        cl = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(cl) if cl else None

        # 构建 curl 命令
        cmd = ['curl', '-s', '-X', method,
               f'{SEARXNG_TARGET}{path}']
        if body:
            cmd += ['-d', body]
        # 转发原始 header
        skip_headers = {'host', 'content-length', 'connection', 'proxy-connection'}
        for k, v in self.headers.items():
            if k.lower() not in skip_headers:
                cmd += ['-H', f'{k}: {v}']

        try:
            result = subprocess.run(cmd, capture_output=True, timeout=15)
            resp_body = result.stdout
            if resp_body:
                # 尝试解析来判断是否有结果
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(resp_body))
                self.end_headers()
                self.wfile.write(resp_body)
            else:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b'Backend error')
        except subprocess.TimeoutExpired:
            self.send_response(504)
            self.end_headers()
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f'Error: {e}'.encode())

    def do_GET(self):
        self._forward('GET')

    def do_POST(self):
        self._forward('POST')

    def log_message(self, format, *args):
        pass  # 静默日志

if __name__ == "__main__":
    # 清理旧进程
    os.system('pkill -f searxng-proxy.py 2>/dev/null')
    shutil.os.system('sleep 1')
    server = http.server.HTTPServer(('0.0.0.0', 8081), Proxy)
    print("SearXNG 反向代理: 0.0.0.0:8081 -> 172.18.0.3:8080", flush=True)
    server.serve_forever()
