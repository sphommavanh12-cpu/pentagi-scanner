from flask import Flask, request, jsonify
import socket
import concurrent.futures
import time

app = Flask(__name__)

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 3306, 3389, 5432, 5900, 6789, 7]

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return port, result == 0

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/scan')
def scan():
    target = request.args.get('target', '')
    if not target:
        return jsonify({"error": "target required"}), 400
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda p: scan_port(target, p), COMMON_PORTS))
    
    open_ports = [p for p, is_open in results if is_open]
    return jsonify({
        "target": target,
        "open_ports": open_ports
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
