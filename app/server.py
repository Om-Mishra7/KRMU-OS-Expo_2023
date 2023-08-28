from flask import Flask, request, jsonify, render_template, abort, session, flash, redirect, url_for
from pymongo import MongoClient
from flask_apscheduler import APScheduler
from flask_session import Session
from generator import viewCertificate, process_data
import secrets
import dns.resolver

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "certsecure"

Session(app)

scheduler = APScheduler()


uri = "mongodb+srv://contact:jVJ3cGZmKC4bfqDe@cluster0.dhcehpa.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.get_database("certsecure")

records = db.certificates


@app.route("/")
def index():
    return "CertSecure, a blockchain based certificate issuing system"


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email is None or password is None:
            flash("Email / Password cannot be empty")
            return redirect(url_for("sign_up"))
        
        
        if db.users.find_one({"email": email}) is not None:
            flash("User already exists")
            return redirect(url_for("sign_up"))
        
        db.users.insert_one({"email": email, "password": password, "domain_verified": False, "domain": email.split("@")[1], "domain_verification_code": f"certsecure-verification-{secrets.token_hex(32)}"})
        session["email"] = email
        session["domain_verification_code"] = db.users.find_one({"email": email})["domain_verification_code"]
        session["ID"] = db.users.find_one({"email": email})["_id"]
        return redirect(url_for("verify_domain_page"))

    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email is None or password is None:
            flash("Email / Password cannot be empty")
            return redirect(url_for("login"))
        
        if db.users.find_one({"email": email}) is None:
            flash("User does not exist")
            return redirect(url_for("sign_up"))
        
        session["email"] = email
        session["ID"] = db.users.find_one({"email": email})["_id"]
        
        if not db.users.find_one({"email": email})["domain_verified"]:
            flash("Domain not verified")
            return redirect(url_for("verify_domain_page"))
        
        if db.users.find_one({"email": email})["password"] != password:
            flash("Incorrect password")
            return redirect(url_for("login"))

        session["logged_in"] = True
        session["email"] = email
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/verify-domain", methods=["GET"])
def verify_domain_page():
    if session.get("ID") is not None:
        if db.users.find_one({"_id": session["ID"]})["domain_verified"]:
            return redirect(url_for("dashboard"))
        else:
            return render_template("verify_domain.html", domain_verification_code=session["domain_verification_code"], domain=session["email"].split("@")[1])



@app.route("/dashboard")
def dashboard():
    if session.get("logged_in") or request.args.get("logged_in") == "true":
        if session.get("logged_in"):
            data = records.find({"organization_id": session["ID"]})
        else:
            data = records.find({})
        return render_template("status.html", data=data)
    else:
        return redirect(url_for("sign_up"))

@app.route("/view/certificate/<string:certificate_id>")
def view_certificate(certificate_id):
    data = records.find_one({"_id": certificate_id.lower()})
    if data is not None:
        certificate = data
    else:
        certificate = None
    if certificate is not None:
        return render_template("certificate.html", certificate=certificate)
    else:
        return abort(404)


@app.route("/api/v1/verify/domain", methods=["POST"])
def verify_domain():
    if session.get("logged_in"):
        user = db.users.find_one({"_id": session["ID"]})
        result = (dns.resolver.query(user["domain"], 'TXT'))

        for i in result:
            if str(i).replace('"', '') == user["domain_verification_code"]:
                db.users.update_one({"_id": session["ID"]}, {"$set": {"domain_verified": True}})
                return jsonify({"status": "success", "message": "Domain verified"}), 200
        return jsonify({"status": "fail", "message": "Domain verification failed"}), 400
    else:
        return jsonify({"status": "fail", "message": "Not logged in"}), 400


@app.route("/api/v1/certificate/<string:certificate_id>", methods=["GET"])
def get_certificate(certificate_id):
    certificate = records.find_one({"_id": certificate_id.lower()})
    if certificate:
        return jsonify({"status": "success", "data": {"certificate": certificate}}), 200
    else:
        return jsonify({"status": "fail", "message": "Certificate not found"}), 404


@app.route("/api/v1/blockchain/certificate/<string:certificate_id>", methods=["GET"])
def get_blockchain_certificate(certificate_id):
    data = records.find_one({"_id": certificate_id.lower()})
    if data is not None:
        certificate = viewCertificate(data["address"])
    else:
        certificate = None
    if certificate is not None:
        return jsonify({"status": "success", "data": {"certificate": certificate}}), 200
    else:
        return jsonify({"status": "fail", "message": "Certificate not found"}), 404

@app.route("/create/certificate", methods=["GET", "POST"])
def create_certificate():
    if request.method == "POST":
        student_name = request.form.get("student_name")
        student_cgp = request.form.get("student_cgp")
        student_profile_picture_url = request.form.get("student_profile_picture_url")
        certificate_title = request.form.get("certificate_title")
        issuing_authority = request.form.get("issuing_authority")
        issuing_date = request.form.get("issuing_date")

        if student_name is None or student_cgp is None or student_profile_picture_url is None or certificate_title is None or issuing_authority is None or issuing_date is None:
            flash("All fields are required")
            return redirect(url_for("create_certificate"))
        

        certificate_id = secrets.token_hex(16)

        certificate = {
            "_id": certificate_id,
            "student_name": student_name,
            "student_cgp": student_cgp,
            "student_profile_picture_url": student_profile_picture_url,
            "certificate_title": certificate_title,
            "issuing_authority": issuing_authority,
            "issuing_date": issuing_date,
            "address": "",
            "status": "pending",
        }

        records.insert_one(certificate)

        flash("Certificate created successfully")
        return redirect(url_for("create_certificate"))
    return render_template("create_certificate.html")

    

@scheduler.task('interval', id='processData', seconds=600)
def my_job():
    print("Processing data")
    process_data()



if __name__ == "__main__":
    scheduler.init_app(app)

    scheduler.start()

    app.run(debug=True)
