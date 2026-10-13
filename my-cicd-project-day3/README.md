# Day 3: Secure Python Flask CI/CD Pipeline with Jenkins

A beginner-friendly DevSecOps project that demonstrates how to test a Python Flask application, scan it for security issues, build a Docker image, publish it to Docker Hub, and run the application in a Docker container.

This project builds on basic Python, Git, Jenkins, and Docker knowledge. You will learn how to add automated security checks to a CI/CD pipeline.

## Table of Contents

- [Project Overview](#project-overview)
- [What You Will Learn](#what-you-will-learn)
- [Tools and Technologies](#tools-and-technologies)
- [Project Structure](#project-structure)
- [How the Application Works](#how-the-application-works)
- [Prerequisites](#prerequisites)
- [Step 1: Clone the Repository](#step-1-clone-the-repository)
- [Step 2: Set Up the Python Environment](#step-2-set-up-the-python-environment)
- [Step 3: Run the Application](#step-3-run-the-application)
- [Step 4: Run Automated Tests](#step-4-run-automated-tests)
- [Step 5: Run SAST with Bandit](#step-5-run-sast-with-bandit)
- [Step 6: Run SCA with pip-audit](#step-6-run-sca-with-pip-audit)
- [Step 7: Build and Run the Docker Image](#step-7-build-and-run-the-docker-image)
- [Step 8: Configure Jenkins](#step-8-configure-jenkins)
- [Step 9: Configure Docker Hub Credentials](#step-9-configure-docker-hub-credentials)
- [Step 10: Run the Jenkins Pipeline](#step-10-run-the-jenkins-pipeline)
- [Understanding the Pipeline](#understanding-the-pipeline)
- [Common Problems and Solutions](#common-problems-and-solutions)
- [Security Notes](#security-notes)
- [Future Improvements](#future-improvements)

## Project Overview

In a traditional development workflow, developers may manually install dependencies, test their applications, build Docker images, and upload those images to a container registry.

This project automates these activities using Jenkins.

The pipeline performs the following tasks:

1. Checks the Jenkins workspace.
2. Creates a Python virtual environment and installs dependencies.
3. Runs automated unit tests using pytest.
4. Scans Python source code using Bandit.
5. Checks Python dependencies for known vulnerabilities using pip-audit.
6. Builds a Docker image.
7. Pushes the image to Docker Hub.
8. Runs the published image in a Docker container.

The goal is to catch problems early and make application delivery more repeatable.

## What You Will Learn

By completing this project, you will understand:

- How a Jenkins declarative pipeline works.
- How to use a Python virtual environment.
- How to write basic tests for a Flask application.
- What Continuous Integration (CI) means.
- What Static Application Security Testing (SAST) means.
- What Software Composition Analysis (SCA) means.
- How to build and tag Docker images.
- How to store Docker Hub credentials securely in Jenkins.
- How to push Docker images to a container registry.
- How to run and verify a Docker container.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Python web framework |
| pytest | Automated application testing |
| Jenkins | CI/CD pipeline automation |
| Bandit | Python source-code security scanning |
| pip-audit | Dependency vulnerability scanning |
| Docker | Containerization |
| Docker Hub | Container image registry |
| Git and GitHub | Source-code version control |

## Project Structure

The project directory contains the following files:

```text
my-cicd-project-day3/
├── app.py
├── Dockerfile
├── Jenkinsfile
├── LICENSE
├── README.md
├── requirements.txt
└── tests/
    └── test_app.py
```

### What does each file do?

**`app.py`**

Contains the Flask application and its HTTP endpoints.

**`requirements.txt`**

Lists the Python packages required by the application and its tests.

**`tests/test_app.py`**

Contains automated tests for the home page and health endpoint.

**`Dockerfile`**

Contains the instructions Docker uses to build the application image.

**`Jenkinsfile`**

Defines the automated pipeline, including testing, security scans, image building, publishing, and deployment.

**`README.md`**

Explains how to set up, run, and practice the project.

## How the Application Works

The application has two endpoints.

| Endpoint | Expected response |
|---|---|
| `/` | `Hello from Naveed's CI/CD Project!` |
| `/health` | `Application is healthy` |

The `/` endpoint displays a welcome message.

The `/health` endpoint provides a simple response that can be used to verify that the application is responding.

## Prerequisites

Before starting, make sure you have:

- Python 3 installed.
- Git installed.
- Docker installed and running.
- Jenkins installed and configured.
- A GitHub repository containing the project.
- A Docker Hub account.
- A Jenkins agent with permission to run Docker commands.

Check your local installations:

```bash
python3 --version
git --version
docker --version
```

Check whether Docker is running:

```bash
docker ps
```

If Docker returns a permission error, make sure your user or Jenkins agent has the required Docker access.

## Step 1: Clone the Repository

Clone your project from GitHub.

Replace the example URL with your repository URL.

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd my-cicd-project-day3
```

List the project files:

```bash
ls -la
```

You should see `app.py`, `Dockerfile`, `Jenkinsfile`, `requirements.txt`, and the `tests` directory.

## Step 2: Set Up the Python Environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

A virtual environment keeps the packages for this project separate from packages used by other Python projects.

Install the application dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Install the security scanning tools:

```bash
.venv/bin/python -m pip install bandit pip-audit
```

Verify that the tools are available:

```bash
.venv/bin/python -m bandit --version
.venv/bin/python -m pip_audit --version
```

**Important:** The virtual environment on your Kali machine is separate from the virtual environment Jenkins creates on its agent. Jenkins must install its own dependencies.

## Step 3: Run the Application

Start the Flask application:

```bash
.venv/bin/python app.py
```

The application runs on port `5000`.

Open another terminal and test the home page:

```bash
curl http://localhost:5000/
```

Expected output:

```text
Hello from Naveed's CI/CD Project!
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected output:

```text
Application is healthy
```

Stop the application using `Ctrl+C` when you finish testing.

### Understanding APP_HOST

The application reads the `APP_HOST` environment variable:

```python
host = os.getenv("APP_HOST", "127.0.0.1")
```

For local development, it defaults to `127.0.0.1`, which limits listening to the local machine.

The Dockerfile sets:

```dockerfile
ENV APP_HOST=0.0.0.0
```

Inside the container, this allows Flask to accept connections forwarded through the container network.

## Step 4: Run Automated Tests

Run the tests:

```bash
.venv/bin/python -m pytest
```

The project contains two tests:

- `test_home()` checks the home page response.
- `test_health()` checks the health endpoint response.

A successful result should resemble:

```text
collected 2 items

tests/test_app.py ..    [100%]

2 passed
```

### Why are tests important?

Tests help identify problems before the application is packaged and published.

If a test fails, Jenkins normally stops the pipeline before proceeding to later stages.

## Step 5: Run SAST with Bandit

SAST stands for **Static Application Security Testing**.

SAST tools analyze source code to identify potentially unsafe coding patterns without requiring the application to be running.

This project uses Bandit for Python source-code scanning.

Run the scan:

```bash
.venv/bin/python -m bandit -r app.py
```

To generate a JSON report:

```bash
.venv/bin/python -m bandit \
  -r app.py \
  -f json \
  -o bandit-report.json
```

The report contains the findings produced by Bandit.

### What should you look for?

Bandit may report issues involving unsafe functions, hardcoded secrets, or potentially risky configurations.

For example, this setting may produce a warning:

```python
app.run(host="0.0.0.0", port=5000)
```

Binding to `0.0.0.0` is often required inside a container, but it should be understood in the context of the network exposure.

A finding does not always mean the application is exploitable. Review the severity, confidence, affected code, and deployment context before deciding how to address it.

## Step 6: Run SCA with pip-audit

SCA stands for **Software Composition Analysis**.

Python applications often depend on packages created and maintained by other developers. A dependency may contain a publicly known vulnerability.

This project uses pip-audit to check dependencies for known vulnerabilities.

Run:

```bash
.venv/bin/python -m pip_audit -r requirements.txt
```

To generate a JSON report:

```bash
.venv/bin/python -m pip_audit \
  -r requirements.txt \
  -f json \
  -o pip-audit-report.json
```

If no known vulnerabilities are detected, you may see:

```text
No known vulnerabilities found
```

If a vulnerability is reported, review the affected package and available fixed versions before updating your dependencies.

**Important:** A clean audit does not prove that the application is completely secure. pip-audit checks known vulnerabilities in dependencies; it does not analyze your application source code like Bandit.

## Step 7: Build and Run the Docker Image

### Build the image

From the project directory, run:

```bash
docker build -t my-flask-app:1.0 .
```

The final dot (`.`) tells Docker to use the current directory as the build context.

### Verify the image

```bash
docker images
```

Look for `my-flask-app` with tag `1.0`.

### Run the container

```bash
docker run -d \
  --name my-first-container \
  -p 5000:5000 \
  my-flask-app:1.0
```

The options mean:

- `-d`: Run the container in the background.
- `--name`: Give the container a recognizable name.
- `-p 5000:5000`: Map port 5000 on the host to port 5000 in the container.

### Test the container

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

Check the running container:

```bash
docker ps
```

If the container exits, inspect the logs:

```bash
docker logs my-first-container
```

Remove the test container when you finish:

```bash
docker rm -f my-first-container
```

## Step 8: Configure Jenkins

### 8.1 Understand the workspace

Your current Jenkinsfile contains commands such as:

```groovy
sh 'ls -la my-cicd-project-day3'
```

It also uses:

```groovy
dir('my-cicd-project-day3') {
    // Commands run inside this directory.
}
```

This means the Jenkins workspace must contain the `my-cicd-project-day3` directory.

For example:

```text
/var/lib/jenkins/workspace/
└── my-cicd-pipeline-docker/
    └── my-cicd-project-day3/
        ├── app.py
        ├── Dockerfile
        ├── Jenkinsfile
        ├── requirements.txt
        └── tests/
```

Your exact workspace path may differ.

**Important:** If the repository itself is the project directory, you may not need the `dir('my-cicd-project-day3')` blocks. Adjust the paths to match the actual Jenkins workspace.

### 8.2 Configure the Jenkins job

1. Open the Jenkins dashboard.
2. Create a Pipeline job, or open your existing job.
3. Configure the Git repository URL.
4. Select the correct branch, such as `main`.
5. Configure the Jenkinsfile path if necessary.
6. Save the job.
7. Select **Build Now** to run the pipeline.

If Jenkins checks out the repository containing this `Jenkinsfile` at its root, ensure that the pipeline paths match the checked-out structure.

### 8.3 Understand the Jenkins stages

Your pipeline contains these stages:

| Stage | Purpose |
|---|---|
| Check Workspace | Displays the workspace and checks the project directory |
| Install Dependencies | Creates the virtual environment and installs Python and security tools |
| Unit Test | Runs pytest |
| SAST | Scans `app.py` using Bandit |
| SCA | Checks `requirements.txt` using pip-audit |
| Build Image | Builds and tags the Docker image |
| Push Image | Authenticates and pushes both tags to Docker Hub |
| Deploy | Runs the published image as a Docker container |

Jenkins executes these stages in sequence. A failed stage normally prevents later stages from running.

## Step 9: Configure Docker Hub Credentials

The Jenkinsfile references this credential ID:

```text
dockerhub-id
```

You must create a matching Jenkins credential before the image-publishing stage can work.

### Create a Docker Hub access token

1. Sign in to Docker Hub.
2. Open your account settings.
3. Find the Personal Access Tokens section.
4. Generate a token with the required permission to push to your image repository.
5. Copy the token and store it securely.

### Add the credential to Jenkins

1. Open **Manage Jenkins → Credentials**.
2. Select the appropriate credentials store and domain.
3. Add a credential of type **Username with password**.
4. Enter your Docker Hub username.
5. Use your Docker Hub access token as the password.
6. Set the credential ID to `dockerhub-id`.
7. Save it.

Never commit your access token or Docker Hub password to GitHub.

### Understand the image tags

The pipeline sets:

```groovy
IMAGE_NAME = 'docker.io/naveedurehman/jenkin-cicd-repo'
TAG = "${env.BUILD_NUMBER}"
```

The Jenkins build number creates a versioned image tag.

For example, build number 7 produces:

```text
docker.io/naveedurehman/jenkin-cicd-repo:7
```

The pipeline also tags the image as:

```text
docker.io/naveedurehman/jenkin-cicd-repo:latest
```

The `latest` tag is a label, not a guarantee that the image is the newest version available everywhere.

## Step 10: Run the Jenkins Pipeline

Once the repository, workspace, Docker access, and credentials are configured:

1. Open the Jenkins job.
2. Select **Build Now**.
3. Open the build details.
4. Select **Console Output**.
5. Watch the stages execute in order.

A successful pipeline should:

- Install dependencies.
- Pass unit tests.
- Complete the configured security scans.
- Build the Docker image.
- Push the versioned and `latest` tags.
- Run the deployment stage.

### Verify the published image

Open Docker Hub and navigate to your repository:

`https://hub.docker.com/repositories`

Find `jenkin-cicd-repo` and verify that the expected tags are available.

You can also pull the published image from a machine with Docker access:

```bash
docker pull docker.io/naveedurehman/jenkin-cicd-repo:latest
```

### Verify the deployment

The current Jenkinsfile runs the container with:

```bash
-p 5000:5000
```

If deployment runs on the same machine you are using to test, check:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
```

If Jenkins runs on a separate machine, the application runs on that machine, not automatically on your Kali host.

## Understanding the Pipeline

Here is the overall workflow:

```text
Developer
   |
   v
GitHub Repository
   |
   v
Jenkins Workspace
   |
   v
Install Dependencies
   |
   v
Unit Tests (pytest)
   |
   v
SAST (Bandit)
   |
   v
SCA (pip-audit)
   |
   v
Build Docker Image
   |
   v
Push Image to Docker Hub
   |
   v
Deploy Container
   |
   v
Test Application Endpoints
```

This project combines automated testing and security checks with container image publishing and a basic deployment stage.

## Common Problems and Solutions

### Problem 1: `requirements.txt` not found

**Cause:** Jenkins is executing the command from the wrong directory.

**Solution:** Check the workspace:

```bash
pwd
ls -la
ls -la my-cicd-project-day3
```

Ensure that the `dir(...)` path matches the repository layout.

### Problem 2: `No module named pytest`

**Cause:** pytest is not installed in the Python environment Jenkins is using.

**Solution:** Make sure the dependency installation stage succeeds and `pytest` is listed in `requirements.txt`.

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest
```

### Problem 3: `No module named pip_audit`

**Cause:** pip-audit was not installed in Jenkins' virtual environment.

**Solution:** Install it in the same environment used by the scan:

```bash
.venv/bin/python -m pip install pip-audit
.venv/bin/python -m pip_audit --version
```

### Problem 4: Bandit reports a security issue

**Cause:** Bandit found a potentially unsafe code pattern.

**Solution:** Read the finding and investigate the affected line. Understand the risk before deciding how to fix or document it.

Do not automatically ignore all findings just to make the pipeline pass.

### Problem 5: Docker permission denied

**Cause:** The Jenkins agent cannot communicate with the Docker daemon.

**Solution:** Check Docker availability and the agent's permissions. Configure access carefully because Docker daemon access can grant significant control over the host.

### Problem 6: Docker Hub authentication fails

**Cause:** The credential ID, username, token, or repository permissions may be incorrect.

**Solution:** Verify that Jenkins has the `dockerhub-id` credential, that the token has push permission, and that the repository name is correct.

### Problem 7: Docker image push fails

**Cause:** The image may have the wrong tag, or the authenticated account may not have permission to publish it.

**Solution:** Check the local images:

```bash
docker images
```

Verify the image name and tag match the Jenkinsfile.

### Problem 8: Container exits immediately

**Cause:** The application may fail to start, or the container may be configured incorrectly.

**Solution:** Inspect the logs:

```bash
docker logs jenkin-cicd-repo
```

Check the Python application, dependencies, environment variables, and port configuration.

### Problem 9: Port 5000 is already allocated

**Cause:** Another process or container is already using host port 5000.

**Solution:** Check running containers:

```bash
docker ps
```

Stop or remove the conflicting container if appropriate, or select another host port.

## Security Notes

- Do not hardcode credentials in the Jenkinsfile.
- Use Jenkins credentials and Docker Hub access tokens.
- Review SAST and SCA findings before publishing an image.
- Remember that a successful scan does not prove the application is completely secure.
- Avoid exposing port 5000 to untrusted networks.
- Docker images should eventually run as a non-root user where practical.
- Pin dependency versions and consider maintaining a lock file for more reproducible builds.
- The current project scans Python source code and Python dependencies. It does not yet scan the Docker image for operating-system package vulnerabilities.

## Future Improvements

After completing this project, consider adding:

1. Trivy for Docker image vulnerability scanning.
2. A non-root user in the Dockerfile.
3. A `.dockerignore` file.
4. Jenkins test report publishing.
5. Automated GitHub webhook triggers.
6. Dependency version pinning and reproducible builds.
7. Docker image cleanup on the Jenkins agent.
8. A proper container health check with retry logic.
9. Deployment to Kubernetes.
10. GitOps deployment with Argo CD.

## Final Learning Outcome

By completing this project, you practice the fundamentals of a DevSecOps workflow:

**Code → Test → Scan → Build → Publish → Deploy**

The objective is not just to make the pipeline green. It is to understand what each stage does, why it exists, and how to troubleshoot it when something fails.

Keep experimenting, review your logs, and add one improvement at a time.
