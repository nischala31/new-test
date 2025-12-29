from flask import Flask, request, render_template_string
import sqlite3
import os
import subprocess
import hashlib
import yaml

app = Flask(__name__)

# Hardcoded secret (vulnerable to secret detection)
API_KEY = "super_secret_api_key_12345"

# Insecure hash example
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/')
def home():
    return '''
    <h1>Vulnerable App for SAST Practice</h1>
    <ul>
        <li><a href="/sql?username=admin">SQL Injection Test</a></li>
        <li><a href="/cmd?cmd=ls">Command Injection Test</a></li>
        <li><a href="/xss?name=<script>alert(1)</script>">XSS Test</a></li>
        <li><a href="/deserialize">Insecure Deserialization Test (POST YAML payload)</a></li>
    </ul>
    '''

@app.route('/sql')
def sql_injection():
    username = request.args.get('username', '')
    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE users (username TEXT)')
    conn.execute('INSERT INTO users VALUES ("admin")')
    # Vulnerable SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    result = conn.execute(query).fetchall()
    return str(result)

@app.route('/cmd')
def command_injection():
    cmd = request.args.get('cmd', 'echo hello')
    # Vulnerable Command Injection
    output = subprocess.getoutput(cmd)
    return f"<pre>{output}</pre>"

@app.route('/xss')
def xss():
    name = request.args.get('name', 'Guest')
    # Vulnerable Reflected XSS
    template = f"<h2>Hello, {name}!</h2>"
    return render_template_string(template)

@app.route('/deserialize', methods=['POST'])
def insecure_deserialize():
    data = request.data
    # Vulnerable Insecure YAML Deserialization
    loaded = yaml.load(data)  # Should use yaml.safe_load()
    return str(loaded)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Debug mode on (additional risk)