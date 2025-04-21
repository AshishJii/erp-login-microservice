import requests as req
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional: allows cross-origin requests

def make_request(session, method, url, **kwargs):
    try:
        res = session.request(method, url, verify=False, timeout=20, **kwargs)
        if res.status_code == 200:
            return {'status': 'success', 'data': res}
        else:
            return {'status': 'error', 'msg': f'HTTPError: {res.status_code}'}
    except req.ConnectionError:
        return {'status': 'error', 'msg': 'No Internet Connection'}
    except req.Timeout:
        return {'status': 'error', 'msg': 'Request timed out.\nSlow internet connection'}

def perform_login(username, password):
    session = req.Session()
    base_urls = ["https://103.120.30.61", "https://erp.psit.ac.in"]
    headers = {'host': 'erp.psit.ac.in', 'Cookie': ''}
    login_data = {"username": username, "password": password}

    for base_url in base_urls:
        login_url = f"{base_url}/Erp/Auth"
        login_res = make_request(session, 'post', login_url, headers=headers, data=login_data)

        if login_res['status'] == 'success':
            session_id = login_res['data'].cookies.get("PHPSESSID")
            if session_id:
                headers["Cookie"] = f"PHPSESSID={session_id}"
                # print("logggedd_in_",headers)

                # Verify login by accessing Student Dashboard
                verify_url = f"{base_url}/Student/Dashboard"
                verify_res = make_request(session, 'get', verify_url, headers=headers)

                if verify_res['status'] == 'success' and 'Refresh' not in verify_res['data'].headers:
                    data = verify_res['data'].text
                    student_info = parse_student_details(data)
                    print(login_data)
                    print(student_info)

                    return {
                        "status": "success",
                        "data": student_info
                    }
                else:
                    return {
                        "status": "error",
                        "msg": "Incorrect credentials"
                    }
                    
    return {
        "status": "error",
        "msg": "Something went wrong!"
    }

def parse_student_details(html: str) -> dict:
    details = {}

    # Extract name from button
    name_match = re.search(
        r'<button[^>]*class="btn\s+btn-primary[^"]*"[^>]*>\s*(.*?)\s*</button>',
        html,
        re.IGNORECASE
    )
    if name_match:
        details["name"] = name_match.group(1)

    # Create a reusable pattern for fields
    def extract_field(label):
        pattern = rf'<td><strong>{re.escape(label)}\s*:\s*<\/strong><\/td>\s*<td>(.*?)<\/td>'
        match = re.search(pattern, html, re.IGNORECASE)
        return match.group(1).strip() if match else None

    fields = {
        "local_address": "Local Address",
        "permanent_address": "Permanent Address",
        "mobile_no": "Mobile No",
        "birth_date": "Birth Date",
        "branch": "Branch",
        "section": "Section",
        "university_roll_no": "University Roll No",
        "library_code": "Library Code",
        "email": "Email"
    }

    for key, label in fields.items():
        details[key] = extract_field(label)
    return details


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
    else:  # GET method
        username = request.args.get("username")
        password = request.args.get("password")

    if not username or not password:
        return jsonify({
            "status": "error",
            "msg": "Username and password required"
        }), 400

    result = perform_login(username, password)
    return jsonify(result)

@app.route('/', methods=['GET'])
def home():
    return """
    <h2>ERP Login Microservice</h2>
    <p>This microservice allows you to verify ERP login credentials via the official PSIT ERP portal.</p>
    <p><b>GET Example:</b> <a href="/login?username=22016XXXXXXXX&password=abcdefgh">/login?username=...&password=...</a></p>
    <p><b>POST Example:</b> Send JSON { "username": "...", "password": "..." } to <code>/login</code>.</p>
    <p>Source: PSIT ERP scraping microservice to verify login credentials.</p>
    <p><b>Note:</b> POST method is recommended for better security as it keeps credentials out of the URL.</p>
    """


if __name__ == '__main__':
    app.run(port=5000, debug=True)
