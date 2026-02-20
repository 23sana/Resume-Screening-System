from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"

db = SQLAlchemy(app)

# ----------------------
# Flask Login Setup
# ----------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Simple User model for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# ----------------------
# Database Model
# ----------------------
class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.Text, nullable=False)
    resume_name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float, nullable=False)
    matched_skills = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# ----------------------
# Skills Database
# ----------------------
SKILLS_DB = [
    "python", "java", "c++", "machine learning",
    "deep learning", "data analysis", "sql",
    "flask", "django", "html", "css",
    "javascript", "react", "tensorflow", "pandas"
]

# ----------------------
# Extract Text from PDF
# ----------------------
def extract_text(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ----------------------
# ROUTES
# ----------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Simple demo login
        if username == "admin" and password == "admin":
            user = User(1)
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/analyze", methods=["POST"])
@login_required
def analyze():
    job_description = request.form["job_description"]
    files = request.files.getlist("resumes")

    resume_texts = []
    resume_names = []

    for file in files:
        if file.filename.endswith(".pdf"):
            text = extract_text(file)
            resume_texts.append(text)
            resume_names.append(file.filename)

    if not resume_texts:
        return "Please upload valid PDF resumes."

    documents = [job_description] + resume_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    results = []

    for i, name in enumerate(resume_names):
        resume_text = resume_texts[i].lower()
        matched_skills = []

        for skill in SKILLS_DB:
            if skill in resume_text and skill in job_description.lower():
                matched_skills.append(skill)

        score_value = float(similarity_scores[i])
        skills_string = ", ".join(matched_skills)

        # Save to database
        new_record = AnalysisResult(
            job_description=job_description,
            resume_name=name,
            score=score_value,
            matched_skills=skills_string
        )
        db.session.add(new_record)
        db.session.commit()

        results.append((name, score_value, matched_skills))

    results.sort(key=lambda x: x[1], reverse=True)
    return render_template("result.html", results=results)

@app.route("/history")
@login_required
def history():
    records = AnalysisResult.query.order_by(AnalysisResult.date_created.desc()).all()
    return render_template("history.html", records=records)

@app.route("/clear-history")
@login_required
def clear_history():
    AnalysisResult.query.delete()
    db.session.commit()
    return redirect(url_for("history"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)