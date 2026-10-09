# basic-to-advance-CI-CD-projects
# My First Docker CI/CD Project — Day 2

A beginner-friendly project to learn how to build a simple Python Flask application, test it with pytest, package it into a Docker image, and automate the process using Jenkins.

The goal is to understand the fundamentals of Continuous Integration and Continuous Delivery (CI/CD) step by step.

## 📌 What Is This Project?

In this project, we use a simple Python web application and automate its testing and Docker image build with Jenkins.

The pipeline performs these tasks:

1. Creates a Python virtual environment.
2. Installs the required Python packages.
3. Runs automated tests using pytest.
4. Builds a Docker image.
5. Starts a Docker container.
6. Checks whether the application responds.
7. Reports whether the pipeline succeeded or failed.

**Note:** This project builds a Docker image and tests a container. It does not yet push the image to Docker Hub or deploy it to a production environment.

## 🛠️ Technologies Used

| Technology | Purpose                                |
| ---------- | -------------------------------------- |
| Python     | Runs the application                   |
| Flask      | Creates the web application            |
| pytest     | Runs automated tests                   |
| Git        | Tracks code changes                    |
| GitHub     | Stores the project repository          |
| Docker     | Packages the application into an image |
| Jenkins    | Automates testing and image building   |

## 📁 Project Structure

```text
my-cicd-project-day2/
├── app.py
├── Dockerfile
├── .dockerignore
├── Jenkinsfile
├── README.md
├── requirements.txt
└── tests/
    └── test_app.py
```

### What Does Each File Do?

**`app.py`**

Contains the Python Flask application and its web routes.

**`Dockerfile`**

Contains instructions Docker uses to build an image for the application.

**`.dockerignore`**

Excludes unnecessary files from the Docker build context, such as Python cache files and the local virtual environment.

**`Jenkinsfile`**

Defines the automated pipeline Jenkins executes.

**`requirements.txt`**

Lists the Python packages needed by the project.

**`tests/test_app.py`**

Contains automated tests that verify the application's endpoints.

**`README.md`**

Explains how the project works and how to run it.

## 🔄 How the CI/CD Pipeline Works

```text
Developer
    |
    | Push code
    v
  GitHub
    |
    v
  Jenkins
    |
    v
Install Dependencies
    |
    v
Run Python Tests
    |
    v
Build Docker Image
    |
    v
Run Docker Container
    |
    v
Test Application
    |
    v
Success or Failure
```

If a stage fails, Jenkins marks the build as failed. Later stages normally do not execute.

## 🚀 Run the Application Locally

### Step 1: Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project directory:

```bash
cd my-cicd-project-day2
```

### Step 2: Create a Python Virtual Environment

A virtual environment isolates the project's Python packages from other Python projects on your machine.

```bash
python3 -m venv .venv
```

### Step 3: Install Dependencies

```bash
.venv/bin/python -m pip install -r requirements.txt
```

### Step 4: Run the Tests

```bash
.venv/bin/python -m pytest
```

If the tests pass, pytest will display a successful result, such as:

```text
2 passed
```

The exact number depends on how many tests are defined in the project.

## 🐳 Build the Docker Image

Make sure Docker is installed and running.

Build the image:

```bash
docker build -t my-flask-app:local .
```

Check the image:

```bash
docker images
```

### What Is a Docker Image?

A Docker image is a package containing the application and the environment required to run it.

### What Is a Docker Container?

A container is a running instance of a Docker image.

The basic process is:

```text
Dockerfile
    |
    v
Docker Image
    |
    v
Docker Container
    |
    v
Running Application
```

## ▶️ Run the Docker Container

Start the application and publish port 5000:

```bash
docker run -d \
  --name cicd-day2-cont \
  -p 5000:5000 \
  my-flask-app:local
```

The `-d` option runs the container in the background.

The `-p 5000:5000` option maps port 5000 on your machine to port 5000 inside the container.

Check the running container:

```bash
docker ps
```

## 🌐 Test the Application

Open these URLs in your browser:

**Home page**

```text
http://localhost:5000/
```

**Health endpoint**

```text
http://localhost:5000/health
```

You can also use the terminal:

```bash
curl http://localhost:5000/
```

```bash
curl http://localhost:5000/health
```

The health endpoint should return the response defined in your Flask application, for example:

```text
Application is healthy
```

If the application uses a different message, the response will match your actual `app.py`.

## 🧹 Stop and Remove the Container

Stop the container:

```bash
docker stop cicd-day2-cont
```

Remove it:

```bash
docker rm cicd-day2-cont
```

The Docker image remains available unless you remove it separately.

## 🤖 Jenkins CI/CD Pipeline

The `Jenkinsfile` defines the steps Jenkins executes automatically.

### Stage 1: Install Dependencies

Jenkins creates a Python virtual environment and installs the packages listed in `requirements.txt`.

### Stage 2: Test

Jenkins executes pytest to check whether the application behaves as expected.

If a test fails, the pipeline stops before building the image.

### Stage 3: Build

Jenkins builds a Docker image using the project's Dockerfile.

The image tag is based on the Jenkins build number.

For example:

```text
my-flask-app:1
my-flask-app:2
my-flask-app:3
```

This helps distinguish images created by different builds.

### Stage 4: Run Container

Jenkins starts a container from the newly built image.

### Stage 5: Test Container

Jenkins sends HTTP requests to the application to check whether it responds.

### Post Actions

Jenkins reports success or failure after the pipeline finishes.

## ⚙️ Configure Jenkins

Create a Pipeline job in Jenkins.

Select:

```text
Definition:
Pipeline script from SCM
```

Then configure:

```text
SCM:
Git

Repository URL:
YOUR_GITHUB_REPOSITORY_URL

Branch:
*/main

Script Path:
my-cicd-project-day2/Jenkinsfile
```

Use `Jenkinsfile` when it is located at the root of the checked-out repository.

If the file is inside a subdirectory, enter its relative path instead.

Save the job and select **Build Now**.

## 🔑 Requirements for the Jenkins Agent

The machine executing the pipeline must have:

- Python 3 installed.
- Permission to create a virtual environment.
- Access to install Python dependencies.
- Docker CLI installed.
- Permission to communicate with the Docker daemon.
- `curl` installed.

The Docker commands must work on the Jenkins agent, not merely on your personal Kali machine.

Check Docker access on the agent:

```bash
docker --version
docker ps
```

## 🐛 Troubleshooting

### Error: `requirements.txt` not found

Make sure Jenkins runs commands from the directory containing `requirements.txt`.

```bash
pwd
ls -la
```

### Error: `No module named pytest`

Install the dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Ensure `pytest` is listed in `requirements.txt`.

### Error: Docker permission denied

Check Docker access on the Jenkins agent:

```bash
docker ps
```

If access is denied, configure the agent's Docker permissions appropriately. Membership in the Docker group grants highly privileged access, so only trusted users and services should receive it.

### Error: Cannot connect to the application

Check the container:

```bash
docker ps -a
```

View its logs:

```bash
docker logs cicd-day2-cont
```

Verify the port mapping and confirm that Flask listens on `0.0.0.0` inside the container.

### Error: Port 5000 is already in use

Choose another host port, such as 5001:

```bash
docker run -d \
  --name cicd-day2-cont \
  -p 5001:5000 \
  my-flask-app:local
```

Then access:

```text
http://localhost:5001/
```

## 🎯 What You Learn

By completing this project, you practise:

- Python application basics.
- Flask routes and health endpoints.
- Python virtual environments.
- Automated testing with pytest.
- Git and GitHub workflows.
- Dockerfiles and Docker images.
- Running and testing containers.
- Jenkins Declarative Pipelines.
- Environment variables and build numbers.
- Basic CI troubleshooting.

## 🚀 Future Improvements

This is a learning project, so we will add features gradually.

**Day 2 — Current project**

```text
Python → pytest → Docker Build → Container Test
```

**Next improvements**

1. Fix and improve the container smoke tests.
2. Add a Docker image push stage to Docker Hub.
3. Use Jenkins credentials for registry authentication.
4. Add code-quality checks.
5. Add automated builds triggered by GitHub changes.
6. Explore deployment to Kubernetes.

## 💡 Final Note

The purpose of this project is to understand each CI/CD step rather than build a complicated system immediately.

Start with Python and testing, understand Docker, and then gradually introduce more advanced DevOps tools.

**Learn one stage at a time. Build, test, understand, and improve.**
