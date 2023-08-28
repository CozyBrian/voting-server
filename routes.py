from flask import Blueprint, redirect, request, url_for, jsonify
from twilio.rest import Client
from extensions import db
from models import User, Candidate, Role, Vote
from utils import transform_phone_number
import requests
import os

main = Blueprint('main', __name__)

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
verify_sid = os.environ.get("VERIFY_SID")
client = Client(account_sid, auth_token)

@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [
        f"<li>{user.username}, {user.dob}, {user.gender}, {user.number}, {user.classOfUser}</li>" 
        for user in users
    ]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/enroll_user', methods=['POST'])
def add_user():
    data = request.json

    # Check if all required fields are present
    required_fields = ['username', 'dob', 'gender', 'number', 'classOfUser']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    username = data['username']
    dob = data['dob']
    gender = data['gender']
    number = data['number']
    classOfUser = data['classOfUser']

    # Check if any of the required fields are empty
    if not all(data[field] for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    new_user = User(username=username, dob=dob, gender=gender, number=number, classOfUser=classOfUser)
    db.session.add(new_user)
    db.session.commit()

    user_add_response = {
        username: "added"
    }

    return jsonify(user_add_response), 200

@main.route('/find_user', methods=['POST'])
def find_user():
    number = request.json.get('number')

    if not number:
        return jsonify({"error": "Phone number is required"}), 400
    
    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "username": user.username,
        "dob": user.dob,
        "gender": user.gender,
        "number": user.number,
        "classOfUser": user.classOfUser
    }

    return jsonify(user_data), 200

@main.route('/send_otp', methods=['POST'])
def send_otp():
    number = request.json.get('number')

    if not number:
        return jsonify({"error": "Phone number is required"}), 400

    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    number_with_countrycode = transform_phone_number(number)

    verification = client.verify.v2.services(verify_sid) \
      .verifications \
      .create(to=number_with_countrycode, channel="sms")

    return jsonify({"message": "OTP has been sent"}), 200

@main.route('/confirm_otp', methods=['POST'])
def confirm_otp():
    number = request.json.get('number')
    otp = request.json.get('otp')

    if not number or not otp:
        return jsonify({"error": "Phone number and OTP are required"}), 400
    
    number_with_countrycode = transform_phone_number(number)
    
    verification_check = client.verify.v2.services(verify_sid) \
      .verification_checks \
      .create(to=number_with_countrycode, code=otp)

    if verification_check.status == "approved":
        user = User.query.filter_by(number=number).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user.as_dict()), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400
    
# create and populate db
@main.route('/init_setup', methods=['GET'])
def init_setup():
    db.create_all()

    roles = ["President", "Vice President", "General Secretary", "Financial Secretary"]

    for role in roles:
        new_role = Role(role=role)
        db.session.add(new_role)
        db.session.commit()

    roles = Role.query.all()
    candidates = ["Georgette Nana Yaa Tedeku", "Yenulom Lambon", "Omar Abdul Bakie"]

    for role in roles:
        for candidate in candidates:
            new_candidate = Candidate(role_id=role.id, candidate=candidate)
            db.session.add(new_candidate)
            db.session.commit()

    return jsonify({"message": "Success"}), 200


# get roles
@main.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()

    if not roles:
        return jsonify([]), 200

    roles = [role.as_dict() for role in roles]

    return jsonify(roles), 200

# get role by id
@main.route('/role', methods=['GET'])
def get_role():
    role_id = request.args.get('role_id', default = 1, type = int)
    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({"error": "Role not found"}), 404

    role = role.as_dict()

    return jsonify(role), 200

# create role
@main.route('/create_role', methods=['POST'])
def create_role():
    role = request.json.get('role')

    if not role:
        return jsonify({"error": "Role field is required"}), 400

    new_role = Role(role=role)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({"message": "Role added"}), 200

# create dummy roles
@main.route('/create_dummy_roles', methods=['POST'])
def create_dummy_roles():
    roles = ["President", "Vice President", "General Secretary", "Financial Secretary"]

    for role in roles:
        new_role = Role(role=role)
        db.session.add(new_role)
        db.session.commit()

    return jsonify({"message": "Roles added"}), 200



# get candidates for a role as a param
@main.route('/candidates', methods=['GET'])
def get_candidates():
    role_id = request.args.get('role_id', default = 1, type = int)
    candidates = Candidate.query.filter_by(role_id=role_id).all()

    if not candidates:
        return jsonify([]), 200

    candidates = [candidate.as_dict() for candidate in candidates]

    return jsonify(candidates), 200

# create candidate for a role
@main.route('/create_candidate', methods=['POST'])
def create_candidate():
    role_id = request.json.get('role_id')
    candidate = request.json.get('candidate')

    if not role_id or not candidate:
        return jsonify({"error": "Role and candidate fields are required"}), 400

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({"error": "Role not found"}), 404

    new_candidate = Candidate(role_id=role.id, candidate=candidate)
    db.session.add(new_candidate)
    db.session.commit()

    return jsonify({"message": "Candidate added"}), 200

# create dummy candidates
@main.route('/create_dummy_candidates', methods=['POST'])
def create_dummy_candidates():
    roles = Role.query.all()
    candidates = ["Barak", "Trump", "Addo", "Harris", "Bob"]

    for role in roles:
        for candidate in candidates:
            new_candidate = Candidate(role_id=role.id, candidate=candidate)
            db.session.add(new_candidate)
            db.session.commit()

    return jsonify({"message": "Candidates added"}), 200

# Has user voted for role
@main.route('/has_user_voted', methods=['POST'])
def has_user_voted():
    number = request.json.get('number')
    role_id = request.json.get('role_id')

    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({"error": "Role not found"}), 404

       # check if votes contain user_id and role_id
    already_voted = Vote.query.filter_by(user_id=user.id, roles_id=role.id).first()

    if already_voted:
        return jsonify({ "status": True }), 200
    else:
        return jsonify({ "status": False }), 200


# vote for a candidate
@main.route('/vote', methods=['POST'])
def vote():
    number = request.json.get('number')
    role_id = request.json.get('role_id')
    candidate_id = request.json.get('candidate_id')

    if not number or not role_id or not candidate_id:
        return jsonify({"error": "Phone number, role and candidate fields are required"}), 400

    user = User.query.filter_by(number=number).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({"error": "Role not found"}), 404

    candidate = Candidate.query.filter_by(id=candidate_id).first()

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404
    
    # check if votes contain user_id and role_id
    already_voted = Vote.query.filter_by(user_id=user.id, roles_id=role.id).first()

    if already_voted:
        return jsonify({"error": "User has already voted for this role"}), 400

    new_vote = Vote(user_id=user.id, roles_id=role.id, candidate_id=candidate.id)
    db.session.add(new_vote)
    db.session.commit()

    return jsonify({"message": "Vote added"}), 200

# get results for a role
@main.route('/results', methods=['POST'])
def get_results():
    role_id = request.json.get('role_id')

    if not role_id:
        return jsonify({"error": "Role field is required"}), 400

    role = Role.query.filter_by(id=role_id).first()

    if not role:
        return jsonify({"error": "Role not found"}), 404

    candidates = Candidate.query.filter_by(role_id=role.id).all()

    if not candidates:
        return jsonify({"message": "No candidates found for role"}), 404

    # get votes for each candidate
    votes = []
    for candidate in candidates:
        vote_count = Vote.query.filter_by(candidate_id=candidate.id).count()
        votes.append(vote_count)

    # get candidate names
    candidate_names = [candidate.candidate for candidate in candidates]

    # create json object
    results = {
        "role": role.role,
        "candidates": candidate_names,
        "votes": votes
    }

    return jsonify(results), 200
