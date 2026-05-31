import random, secrets, uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import join_room, leave_room, send, emit, SocketIO 
from sqlalchemy import or_
from string import ascii_letters
from datetime import datetime
from .services.error_messages import NotFoundError, Success, UnauthorizedError, ValidationError, BadRequestError, InternalServerError
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    decode_token
)
from .models.base_model import db
from .models.user_model import User, Bot
from .models.bot_model import BotB
from .models.group_model import Group
from .models.msg_model import Message
from .bots.Nexus.organizer import nexus_chat

connected_users = {}

from datetime import timedelta

app = Flask(__name__)
ALLOWED_ORIGINS = ["http://localhost:5173"]
GET, POST, PUT, DELETE = "GET", "POST", "PUT", "DELETE"
CORS(app, supports_credentials=True, origins=ALLOWED_ORIGINS)
app.config["SECRET_KEY"] = "mySdiscn9w98eu3"
socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS)
app.config['JWT_SECRET_KEY'] = 'fgvf5t535657777b7ub767u3_6jyttqqt6535y7j5ukn7in9653wg6gw5yy4unuj4m7667'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatnow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=300)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=700)
jwt = JWTManager(app)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
db.init_app(app)



with app.app_context():
    db.create_all()


@app.route("/getnexusid", methods=[GET])
def nexus_id():

    nexus = User.query.filter_by(
        username="Nexus"
    ).first()

    if not nexus:
        nexus = User(
            username="Nexus",
            password="some-random-secret..."
        )

        db.session.add(nexus)
        db.session.commit()

    return Success(
        data={"id": nexus.id},
        message="Nexus id given"
    ).send()

@app.route("/api/user/saveUser", methods=[POST])
def save_user():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return NotFoundError(
            "Username or password missing"
        ).send()

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:
        return NotFoundError(
            "Username already exists"
        ).send()

    user = User(username, password)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return Success(
        message="User created successfully",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict()
        }
    ).send()

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password: 
        return NotFoundError(
            "Username or password missing"
        ).send()

    user = User.query.filter_by(
        username=username
    ).first()

    if not user:
        return NotFoundError(
            "User not found"
        ).send()

    if not user.check_password(password):
        return NotFoundError(
            "Incorrect password"
        ).send()

    access_token = create_access_token(
        identity=str(user.id)
    )

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return Success(
        message='Login successful.',
        data={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    ).send()


@app.route('/profile', methods=[GET, "PREFLIGHT"])
@jwt_required()
def profile():
    if request.method != GET:
        print("Allowing preflight to pass through")

    current_user = get_jwt_identity()
    user = User.query.filter_by(
        id=int(current_user)
    ).first()

    if not user:
        print("User was not found")
        return NotFoundError(
            "User not found"
        ).send()
    print(f"User: {user.to_dict()}")
    return Success(message="Profile launced successfully", data=user.to_dict()).send()


@app.route('/users/getUserInfo', methods=['GET'])
@jwt_required()
def get_user_info():
    current_user_id = int(get_jwt_identity())
    
    # 1. Parse and validate the query parameter
    user_query = request.args.get('userId', '').strip()
    if not user_query:
        return BadRequestError("No arguments in user information query").send()
        
    try:
        requested_user_id = int(user_query)
    except ValueError:
        return NotFoundError("Invalid user id").send()

    # 2. Query the requested user profile using Flask-SQLAlchemy
    requested_user = User.query.get(requested_user_id) # .get() is faster for primary keys
    if not requested_user:
        return NotFoundError("User not found").send()

    # 3. Retrieve the full chat history sorted chronologically
    # Evaluates: (Sender is Me AND Receiver is Them) OR (Sender is Them AND Receiver is Me)
    conversation = Message.query.filter(
        or_(
            (Message.sender_id == current_user_id) & (Message.receiver_id == requested_user_id),
            (Message.sender_id == requested_user_id) & (Message.receiver_id == current_user_id)
        )
    ).order_by(Message.timestamp.asc()).all() # .asc() sorts oldest to newest (perfect for chat logs)

    # 4. Format data for your Vue frontend
    serialized_msgs = []
    for msg in conversation:
        msg_dict = msg.to_dict()
        msg_dict['is_me'] = (msg.sender_id == current_user_id)
        serialized_msgs.append(msg_dict)
    response = {
        'the_user': requested_user.to_dict(),
        'correspondence': serialized_msgs
    }
    
    return Success(message="User history loaded", data=response).send()



@app.route('/users/search', methods=['GET'])
@jwt_required()
def get_users():
    current_user_id = int(get_jwt_identity())
    
    # 1. Get the optional search keyword from the URL (e.g., /users/search?query=1234)
    search_query = request.args.get('query', '').strip()
     
    # 2. Build a highly efficient database-level query
    query = User.query.filter(User.id != current_user_id)
    
    # 3. Apply the search filter on the backend database if a keyword exists
    if search_query:
        try:
            query = query.filter(User.id == int(search_query))
        except ValueError:
            return ValidationError("Search id must be an integer").send()


    # 4. Fetch only the matching records (and consider adding .limit(50) for safety)
    matched_users = query.all()
    
    # 5. Serialize results efficiently
    user_list = [u.to_dict() for u in matched_users]
    
    return Success(data=user_list, message="Search results retrieved successfully").send()


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():

    current_user = get_jwt_identity()

    access_token = create_access_token(
        identity=str(current_user)
    )

    refresh_token = create_refresh_token(
        identity=str(current_user)
    )

    return Success(
        message='Session refreshed.',
        data={
            'access_token': access_token,
            'refresh_token': refresh_token
        },
        status_code=201
    ).send()

@app.route('/bots/create', methods=[POST])
@jwt_required()
def create_bot():
    data = request.get_json()

    name = data.get('name')
    system_prompt = data.get('system_prompt')

    owner_id = int(
        get_jwt_identity()
    )

    if not name or not system_prompt:
        return BadRequestError(
            "Incomplete credentials"
        ).send()

    existing_user = User.query.filter_by(
        username=name
    ).first()

    if existing_user:
        return BadRequestError(
            "Bot name already exists"
        ).send()

    # Create hidden user account
    bot_user = User(
        username=name,
        password=secrets.token_hex(32)
    )

    db.session.add(bot_user)
    db.session.commit()

    # Store bot instructions
    bot = BotB(
        user_id=bot_user.id,
        system_prompt=system_prompt
    )

    db.session.add(bot)
    db.session.commit()

    return Success(
        data={
            "bot_id": bot_user.id
        },
        message="Bot created"
    ).send()

def get_room_name(id1, id2):
    # Sorting ensures both users always join the exact same room string name
    return f"chat_{min(id1, id2)}_{max(id1, id2)}"

@socketio.on('connect')
def handle_connect(auth):
    token = auth.get('token') if auth else None

    if not token:
        print("CONNECT FAILED: no token")
        return False

    try:
        decoded = decode_token(token)
        user_id = int(decoded['sub'])

        connected_users[request.sid] = user_id

        print(f"CONNECTED: User {user_id} | SID {request.sid}")

    except Exception as e:
        print("CONNECT FAILED:", e)
        return False


@socketio.on('disconnect')
def handle_disconnect():
    user_id = connected_users.pop(
        request.sid,
        None
    )

    print(
        f"DISCONNECTED: User {user_id} | SID {request.sid}"
    )


@socketio.on('join_chat')
def handle_join_chat(data):
    current_user_id = connected_users.get(
        request.sid
    )

    if not current_user_id:
        print("JOIN FAILED: unknown user")
        return

    try:
        target_user_id = int(
            data.get('target_id')
        )
    except (TypeError, ValueError):
        print("JOIN FAILED: invalid target")
        return

    room = get_room_name(
        current_user_id,
        target_user_id
    )

    join_room(room)

    print(
        f"JOIN: User {current_user_id} -> {room}"
    )

@socketio.on('send_msg')
def handle_send_message(data):

    NEXUS_ID = 14

    sender_id = connected_users.get(
        request.sid
    )

    if not sender_id:
        print(
            "SEND FAILED: unknown sender"
        )
        return

    try:
        receiver_id = int(
            data.get('receiver_id')
        )
    except (TypeError, ValueError):
        print(
            "SEND FAILED: invalid receiver"
        )
        return

    content = (
        data.get('content', '')
        .strip()
    )

    if not content:
        print(
            "SEND FAILED: empty content"
        )
        return

    print(
        f"SEND: {sender_id} -> {receiver_id}"
    )

    # ------------------------------------------------
    # Save user message
    # ------------------------------------------------

    user_msg = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow()
    )

    db.session.add(user_msg)
    db.session.commit()

    room = get_room_name(
        sender_id,
        receiver_id
    )

    emit(
        'receive_msg',
        {
            'id': user_msg.id,
            'sender_id': user_msg.sender_id,
            'receiver_id': user_msg.receiver_id,
            'content': user_msg.content,
            'timestamp':
                user_msg.timestamp.isoformat()
        },
        room=room
    )

    # ------------------------------------------------
    # Check for custom bot
    # ------------------------------------------------

    custom_bot = BotB.query.filter_by(
        user_id=receiver_id
    ).first()

    is_nexus = (
        receiver_id == NEXUS_ID
    )

    if not is_nexus and not custom_bot:
        print(
            f"EMITTED TO ROOM: {room}"
        )
        return

    print("BOT TRIGGERED")

    try:

        # ----------------------------------------
        # Generate AI answer
        # ----------------------------------------

        if is_nexus:

            answer = nexus_chat(
                content,
                "No history for now"
            )

            bot_sender_id = NEXUS_ID

        else:

            answer = nexus_chat(
                content,
                custom_bot.system_prompt
            )

            bot_sender_id = receiver_id

        # ----------------------------------------
        # Save bot response
        # ----------------------------------------

        bot_msg = Message(
            sender_id=bot_sender_id,
            receiver_id=sender_id,
            content=answer,
            timestamp=datetime.utcnow()
        )

        db.session.add(bot_msg)
        db.session.commit()

        emit(
            'receive_msg',
            {
                'id': bot_msg.id,
                'sender_id':
                    bot_msg.sender_id,
                'receiver_id':
                    bot_msg.receiver_id,
                'content':
                    bot_msg.content,
                'timestamp':
                    bot_msg.timestamp.isoformat()
            },
            room=room
        )

        print(
            f"BOT RESPONSE: {answer[:100]}"
        )

    except Exception as e:

        print(
            f"BOT ERROR: {e}"
        )

    print(
        f"EMITTED TO ROOM: {room}"
    )
@app.errorhandler(Exception)
def handle_exception(e):
    # Pass response through CORS headers even on error drops
    print(f"Exception: { e }")
    response = jsonify({"message": str(e)})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response, 500



if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
 