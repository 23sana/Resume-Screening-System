
# Resume Screening System

A **Flask-based Resume Screening Web Application** that helps HR teams and recruiters automatically evaluate resumes against a job description. It uses **TF-IDF similarity** and **skill matching** to score resumes and store results in a database.

---

## **Features**

- Upload multiple PDF resumes at once.
- Analyze resumes against a given job description.
- Calculate **cosine similarity** between resumes and job description.
- Match resumes against predefined **skills database**.
- Store analysis results in a **SQLite database**.
- View **history of analyses**.
- Clear analysis history when needed.
- User authentication with simple login (admin/admin).

---

## **Tech Stack**

- **Backend:** Python, Flask  
- **Database:** SQLite (via SQLAlchemy)  
- **Machine Learning:** scikit-learn (TF-IDF & cosine similarity)  
- **PDF Parsing:** PyPDF2  
- **Frontend:** HTML, CSS (responsive design)  

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/23sana/Resume-Screening-System.git
cd Resume-Screening-System
````

2. Create a virtual environment:

```bash
python -m venv env
```

3. Activate the virtual environment:

* **Windows:**

```bash
env\Scripts\activate
```

* **Linux/Mac:**

```bash
source env/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** Make sure `requirements.txt` includes:
>
> ```
> Flask
> Flask-Login
> Flask-SQLAlchemy
> PyPDF2
> scikit-learn
> ```

---

## **Usage**

1. Run the Flask app:

```bash
python app.py
```

2. Open your browser and go to:

```
http://127.0.0.1:5000/
```

3. **Login:**

   * Username: `admin`
   * Password: `admin`

4. Upload resumes, paste the job description, and click **Analyze**.

5. View results and check **history**.

---

## **Project Structure**

```
Resume-Screening-System/
│
├── app.py              # Main Flask application
├── templates/          # HTML templates
│   ├── login.html
│   ├── index.html
│   ├── result.html
│   └── history.html
├── static/             # (Optional) CSS or JS files
├── resume_results.db   # SQLite database (auto-created)
├── requirements.txt    # Python dependencies
└── README.md
```

---



## **Screenshots** 

You can add screenshots of the **login page**

<img width="1364" height="598" alt="Screenshot 2026-02-20 153546" src="https://github.com/user-attachments/assets/3becc4c1-f73a-49ac-8346-78121751a6fb", 
**dashboard**
<img width="1366" height="574" alt="2026-02-20" src="https://github.com/user-attachments/assets/4215adfb-fe1b-41bc-a087-0f3b095c4918" />

**results page**

<img width="1339" height="372" alt="Screenshot 2026-02-20 154529" src="https://github.com/user-attachments/assets/227e076b-d248-4393-8c47-20e616a24a6f" />,


 and **history page** here to make your GitHub repo more attractive.
<img width="1366" height="573" alt="2026-02-20 (1)" src="https://github.com/user-attachments/assets/a213d094-9ab8-42fd-833b-ed599d38eddf" />

