# basic-to-advance-CI-CD-projects
# My First CI/CD Project with Python, Flask & Jenkins

A simple beginner-friendly project to learn the basics of **Continuous Integration (CI)** using:

- Python
- Flask
- pytest
- Git
- GitHub
- Jenkins

> **Note:** This project intentionally does not use Docker, Kubernetes, Helm, Argo CD, or AWS. Those technologies can be added later as separate steps.

---

## 📌 What is this project?

This project is a small Python Flask web application.

The main goal is not to build a complicated application.

The goal is to understand how **Continuous Integration** works.

Whenever we update our code and push it to GitHub, Jenkins can automatically:

1. Get the latest code
2. Create a Python virtual environment
3. Install the required dependencies
4. Run automated tests
5. Report whether the build passed or failed

The basic workflow is:

```text
Developer
    │
    │ git push
    ▼
  GitHub
    │
    ▼
  Jenkins
    │
    ├── Install Dependencies
    │
    └── Run Tests
          │
          ▼
       PASS / FAIL
```

---

# 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Flask | Web framework |
| pytest | Automated testing |
| Git | Version control |
| GitHub | Remote code repository |
| Jenkins | CI automation |

---

# 📁 Project Structure

```text
my-first-cicd-project/
│
├── app.py
│
├── Jenkinsfile
│
├── requirements.txt
│
├── README.md
│
├── LICENSE
│
└── tests/
    └── test_app.py
```

### What does each file do?

### `app.py`

This is our Python application.

It creates a small Flask web server with two endpoints:

```text
/
```

and:

```text
/health
```

---

### `tests/test_app.py`

This file contains automated tests for our Flask application.

The tests check that:

- The `/` endpoint works
- The `/health` endpoint works
- The application returns HTTP status `200`
- The expected response is returned

Flask provides a test client that allows us to test routes without starting the application as a live server.

---

### `requirements.txt`

This file contains the Python packages required by the project.

Currently:

```text
Flask
pytest
```

Instead of manually installing every package, we can run:

```bash
pip install -r requirements.txt
```

---

### `Jenkinsfile`

This file contains our Jenkins Pipeline.

Instead of configuring every CI command manually inside Jenkins, we store the pipeline as code in Git.

Jenkins recommends keeping the `Jenkinsfile` in source control because it provides a versioned and reviewable definition of the pipeline.

---

# 🖥️ Run the Project Locally

## Step 1 — Clone the repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project:

```bash
cd my-first-cicd-project
```

---

## Step 2 — Create a virtual environment

A virtual environment keeps the project's Python packages separate from the system Python installation.

Run:

```bash
python3 -m venv .venv
```

---

## Step 3 — Activate the virtual environment

Linux/macOS:

```bash
source .venv/bin/activate
```

You should see something similar to:

```text
(.venv) user@machine:~/my-first-cicd-project$
```

---

## Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

```text
Flask
pytest
```

---

# ▶️ Run the Flask Application

Start the application:

```bash
python app.py
```

You should see something similar to:

```text
Running on http://127.0.0.1:5000
```

Open your browser:

```text
http://127.0.0.1:5000
```

You should see:

```text
Hello from Naveed's CI/CD Project!
```

---

## ❤️ Health Check

Open:

```text
http://127.0.0.1:5000/health
```

Expected response:

```text
Application is healthy
```

The `/health` endpoint will later be useful when we introduce containers, Kubernetes, and deployment.

---

# 🧪 Run Tests

You can run the tests using:

```bash
python -m pytest
```

Expected result:

```text
2 passed
```

Example:

```text
========================= test session starts =========================
collected 2 items

tests/test_app.py ..                                      [100%]

========================== 2 passed ==========================
```

If the tests pass, our application is behaving as expected.

---

# 🔀 Git Workflow

After making a change to the application:

### 1. Check the changes

```bash
git status
```

### 2. Add the changes

```bash
git add .
```

### 3. Create a commit

```bash
git commit -m "Update application"
```

### 4. Push to GitHub

```bash
git push origin main
```

---

# 🤖 Jenkins CI Pipeline

Our Jenkins pipeline performs two main tasks:

```text
Install Dependencies
        ↓
      Run Tests
```

The pipeline is defined inside:

```text
Jenkinsfile
```

---

## Jenkins Pipeline Flow

```text
GitHub
   │
   │ Repository Checkout
   ▼
Jenkins
   │
   ▼
Install Dependencies
   │
   ▼
Create Python Virtual Environment
   │
   ▼
Install Flask + pytest
   │
   ▼
Run pytest
   │
   ├───────────────┐
   ▼               ▼
 PASS             FAIL
  │                │
  ▼                ▼
SUCCESS           FAILURE
```

---

# ⚙️ Jenkins Configuration

Create a new **Pipeline** job in Jenkins.

Choose:

```text
Definition:
Pipeline script from SCM
```

Select:

```text
SCM:
Git
```

Enter your GitHub repository.

For example:

```text
Repository:
https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Set the branch:

```text
*/main
```

If your repository has this structure:

```text
repository/
└── my-first-cicd-project/
    ├── app.py
    ├── Jenkinsfile
    ├── requirements.txt
    └── tests/
```

then use:

```text
Script Path:
my-first-cicd-project/Jenkinsfile
```

If `Jenkinsfile` is directly in the repository root, use:

```text
Script Path:
Jenkinsfile
```

The Jenkins Script Path is relative to the repository Jenkins checks out.

---

# 🧠 Understanding the Jenkinsfile

Our Jenkinsfile contains:

```text
pipeline
   │
   ├── agent
   │
   └── stages
          │
          ├── Install Dependencies
          │
          └── Test
```

### `pipeline`

This tells Jenkins that the file contains a Jenkins Pipeline.

### `agent any`

This tells Jenkins to allocate an available executor/workspace for the Pipeline.

### `stages`

This contains the different stages of our CI process.

### `stage`

A stage represents one logical part of the pipeline.

For example:

```text
Install Dependencies
```

and:

```text
Test
```

### `steps`

The actual commands Jenkins executes are placed inside `steps`.

Jenkins' Declarative Pipeline syntax uses `pipeline`, `agent`, `stages`, `stage`, and `steps` as core building blocks.

---

# 🧪 What Happens When Jenkins Runs?

When Jenkins starts the pipeline:

### Step 1

Jenkins gets the source code from GitHub.

### Step 2

Jenkins enters:

```text
my-first-cicd-project/
```

### Step 3

Jenkins creates:

```text
.venv/
```

### Step 4

Jenkins installs:

```text
Flask
pytest
```

using:

```bash
pip install -r requirements.txt
```

### Step 5

Jenkins runs:

```bash
python -m pytest
```

### Step 6

If the tests pass:

```text
BUILD SUCCESS
```

If a test fails:

```text
BUILD FAILURE
```

This is the basic idea of Continuous Integration.

---

# ❌ What Happens If a Test Fails?

Suppose we change our application and accidentally break something.

The test may produce:

```text
FAILED tests/test_app.py
```

Jenkins then marks the pipeline as:

```text
FAILURE ❌
```

This gives developers immediate feedback that something is wrong.

---

# 🎯 What I Learned From This Project

After completing this project, you should understand:

- What a Python virtual environment is
- What Flask is
- What an API endpoint is
- What automated testing means
- How pytest works
- What Git is
- How to commit code
- How to push code to GitHub
- What Jenkins is
- What a Jenkinsfile is
- What a Jenkins Pipeline is
- What CI means
- How Jenkins automatically runs tests
- Why automated testing is important

---

# 🚀 Future Improvements

This project is intentionally simple.

We will gradually improve it.

### Phase 1 — Current

```text
Python
   ↓
Flask
   ↓
pytest
   ↓
GitHub
   ↓
Jenkins
```

### Phase 2 — Code Quality

Add:

```text
Flake8
```

Pipeline:

```text
Install
   ↓
Lint
   ↓
Test
```

### Phase 3 — Docker

Create a separate Docker version:

```text
Python
   ↓
Flask
   ↓
Docker
   ↓
Docker Image
```

### Phase 4 — Container Registry

Push the Docker image to:

```text
Docker Hub / GitHub Container Registry
```

### Phase 5 — Kubernetes

Deploy the application to Kubernetes:

```text
Docker Image
      ↓
Kubernetes
      ↓
Pod
      ↓
Service
```

### Phase 6 — Helm

Manage Kubernetes configuration using Helm.

### Phase 7 — Argo CD

Introduce GitOps:

```text
GitHub
   ↓
Argo CD
   ↓
Kubernetes
```

### Phase 8 — AWS

Eventually deploy the complete project to AWS.

---

# 👨‍💻 Beginner Tip

Don't try to learn everything at once.

First understand:

```text
Python
 ↓
Git
 ↓
Testing
 ↓
Jenkins
```

Then add:

```text
Docker
```

Then:

```text
Kubernetes
```

Then:

```text
Helm
```

Then:

```text
Argo CD
```

And finally:

```text
AWS
```

The purpose of this project is to build your DevOps knowledge step by step.

---

# 📚 Useful Commands

### Start application

```bash
python app.py
```

### Run tests

```bash
python -m pytest
```

### Check Git status

```bash
git status
```

### Add files

```bash
git add .
```

### Commit

```bash
git commit -m "Your message"
```

### Push

```bash
git push origin main
```

### Activate virtual environment

```bash
source .venv/bin/activate
```

### Deactivate virtual environment

```bash
deactivate
```

---

# ⭐ Project Goal

The final goal is to understand how a simple application can evolve into a professional DevOps project.

We start small:

```text
Python + Flask
```

Then gradually build:

```text
Python
   ↓
Testing
   ↓
Git
   ↓
Jenkins CI
   ↓
Docker
   ↓
Container Registry
   ↓
Kubernetes
   ↓
Helm
   ↓
Argo CD
   ↓
AWS
```

**Start simple. Understand every layer, then add the next one.**
