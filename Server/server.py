from flask import Flask, request, jsonify
import mysql.connector
import hashlib

app = Flask(__name__)
# engine = Engine()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KevinDurant0929@",
    database="search_engine"
)
db = connection.cursor()

search_input = ""
search_result = []
search_complete = False

login_status = False
login_username = ""
login_password = ""

registration_status = False
register_username = ""
register_password = ""

user_message = ""
robot_message = ""


@app.route("/")
def home():
    return {"": "Welcome to backend"}


# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     global search_input, search_result, search_complete
#     if request.method == 'POST':
#         search_complete = False
#         request_data = request.get_json()
#         search_input = request_data['search']
#         search_result = engine.search(search_input)
#         search_complete = True
#     return jsonify({"search_input": search_input})


@app.route("/status", methods=['GET'])
def status():
    global search_complete
    if request.method == 'GET':
        return jsonify({"status": 1 if search_complete else 0})


@app.route("/result")
def result():
    return jsonify({"result": search_result})


@app.route("/register", methods=['GET', 'POST'])
def register():
    global registration_status, register_username, register_password
    if request.method == 'POST':
        request_data = request.get_json()
        register_username = request_data['username']
        register_password = request_data['password']
        hashed = hashlib.md5(register_password.encode()).digest()
        insert_query = "INSERT INTO user (user_name, hash) VALUES (%s, %s)"
        record = (register_username, hashed)
        try:
            db.execute(insert_query, record)
            connection.commit()
            registration_status = True
        except mysql.connector.errors.IntegrityError:
            registration_status = False
    register_outcome = {"username": register_username,
                        "password": register_password,
                        "status": registration_status}
    print(str(register_outcome))
    return jsonify(register_outcome)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global login_status, login_username, login_password
    if request.method == 'POST':
        request_data = request.get_json()
        login_username = request_data['username']
        login_password = request_data['password']
        hash_query = f"SELECT hash FROM user WHERE user_name = '{login_username}'"
        db.execute(hash_query)
        res = db.fetchall()

        if len(res) < 1:
            login_status = False
            print("ACCESS DENIED")
            login_outcome = {"username": login_username,
                             "password": login_password,
                             "status": login_status}
            print(str(login_outcome))
            return jsonify(login_outcome)

        outcome, = res[0]

        print("Username: " + login_username)
        print("Password: " + login_password)

        if outcome == bytearray(hashlib.md5(login_password.encode()).digest()):
            login_status = True
            print("ACCESS GRANTED")
        else:
            login_status = False
            print("ACCESS DENIED")

    login_outcome = {"username": login_username,
                     "password": login_password,
                     "status": login_status}
    print(str(login_outcome))
    return jsonify(login_outcome)


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    global user_message, robot_message
    if request.method == 'POST':
        request_data = request.get_json()
        user_message = request_data['message']
        # Replace this with search engine code
        robot_message = "This is a robot response, please ignore (testing)"
    chat_outcome = {"user_message": user_message,
                    "robot_message": robot_message}
    print(chat_outcome)
    return jsonify(chat_outcome)


if __name__ == "__main__":
    app.run(debug=True)
