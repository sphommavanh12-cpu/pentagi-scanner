from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/scan')
def scan():
    target = request.args.get('target', '')
    if not target:
        return jsonify({"error": "target required"}), 400
    
    result = subprocess.run(
        ['nmap', '-Pn', '-sV', target, '-oG', '-'],
        capture_output=True, text=True, timeout=60
    )
    return jsonify({
        "target": target,
        "output": result.stdout,
        "error": result.stderr
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
