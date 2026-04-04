# CI

## Gitlab
Preparation: Store your application under test as a Docker container in the Gitlab Container Registry

### Gitlab CI configuration example
```yaml
stages:
  - build
  - test

variables:
  APP_IMAGE: $CI_REGISTRY/$CI_PROJECT_PATH/app:latest

build-app:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_JOB_TOKEN $CI_REGISTRY
  script:
    # Assuming the app Dockerfile is in the repo or pulled from another source
    - docker build -t $APP_IMAGE ./path/to/app
    - docker push $APP_IMAGE
  only:
    - schedules

run-locust-tests:
  stage: test
  image: locustio/locust:latest
  services:
    - name: $APP_IMAGE
      alias: testapp
  script:
    - locust -f locustfile.py --headless --host http://testapp:8000 --users 100 --spawn-rate 5 --run-time 5m --html report.html
  artifacts:
    paths:
      - report.html
    expire_in: 30 days
  only:
    - schedules
```

#### Key points:

- Container Registry: Uses GitLab's built-in $CI_REGISTRY variables (no setup needed)
- Build stage: Builds and pushes your app Docker image
- Test stage: Starts app as a service, runs Locust against it
- Reports: Saves HTML report as artifact
- Trigger: Runs only on scheduled pipelines


#### Setup steps:

1. Create .gitlab-ci.yml in your repo root with this content
2. Update ./path/to/app to where your app Dockerfile lives
3. Enable Container Registry in GitLab project settings
4. Set up a schedule in GitLab: CI/CD → Schedules → New schedule

---

## Github Actions
Preparation: Store your application under test as a Docker container in the GitHub Container Registry (ghcr.io)

### Github Actions workflow example
```yaml
name: Performance Tests

on:
  schedule:
    - cron: '0 2 * * *'  # Run daily at 2 AM UTC
  workflow_dispatch:  # Allow manual trigger

env:
  REGISTRY: ghcr.io
  APP_IMAGE: ghcr.io/${{ github.repository }}/app:latest

jobs:
  build-app:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push Docker image
        run: |
          docker build -t ${{ env.APP_IMAGE }} ./path/to/app
          docker push ${{ env.APP_IMAGE }}

  run-locust-tests:
    needs: build-app
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Pull app image
        run: docker pull ${{ env.APP_IMAGE }}
      
      - name: Start application container
        run: |
          docker run -d --name testapp -p 8000:8000 ${{ env.APP_IMAGE }}
          sleep 5  # Wait for app to start
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run Locust tests
        run: |
          locust -f locustfile.py --headless --host http://localhost:8000 --users 100 --spawn-rate 5 --run-time 5m --html report.html
      
      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: locust-report
          path: report.html
          retention-days: 30
```

#### Key points:

- Container Registry: Uses GitHub Container Registry (ghcr.io) with built-in ${{ secrets.GITHUB_TOKEN }}
- Build job: Builds and pushes your app Docker image
- Test job: Pulls app image, starts container, runs Locust against it
- Reports: Saves HTML report as artifact
- Trigger: Runs on schedule (daily) or manual trigger


#### Setup steps:

1. Create `.github/workflows/performance-tests.yml` in your repo with this content
2. Update `./path/to/app` to where your app Dockerfile lives
3. Enable GitHub Container Registry in repository settings (Settings → Actions → General → Workflow permissions)
4. Adjust schedule in the `cron` expression as needed
5. Run manually via Actions tab → Performance Tests → Run workflow

---

## Jenkins
Preparation: Store your application under test as a Docker container in a Docker Registry (Docker Hub, private registry, or Jenkins container registry)

### Jenkinsfile example
```groovy
pipeline {
    agent any
    
    environment {
        REGISTRY = 'your-registry.com'  // Or 'docker.io' for Docker Hub
        APP_IMAGE = "${REGISTRY}/your-app:latest"
        REGISTRY_CREDENTIALS = 'docker-registry-credentials'  // Jenkins credential ID
    }
    
    triggers {
        cron('0 2 * * *')  // Run daily at 2 AM
    }
    
    stages {
        stage('Build App') {
            steps {
                script {
                    docker.withRegistry("https://${REGISTRY}", REGISTRY_CREDENTIALS) {
                        def appImage = docker.build(APP_IMAGE, './path/to/app')
                        appImage.push()
                    }
                }
            }
        }
        
        stage('Run Locust Tests') {
            agent {
                docker {
                    image 'locustio/locust:latest'
                    args '--network host'
                }
            }
            steps {
                script {
                    // Start application container
                    docker.withRegistry("https://${REGISTRY}", REGISTRY_CREDENTIALS) {
                        docker.image(APP_IMAGE).withRun('-p 8000:8000') { container ->
                            // Wait for app to start
                            sh 'sleep 5'
                            
                            // Run Locust tests
                            sh '''
                                locust -f locustfile.py \
                                  --headless \
                                  --host http://localhost:8000 \
                                  --users 100 \
                                  --spawn-rate 5 \
                                  --run-time 5m \
                                  --html report.html
                            '''
                        }
                    }
                }
            }
            post {
                always {
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: '.',
                        reportFiles: 'report.html',
                        reportName: 'Locust Performance Report'
                    ])
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
    }
}
```

#### Key points:

- Container Registry: Uses configured Docker registry with Jenkins credentials
- Build stage: Builds and pushes your app Docker image
- Test stage: Starts app container, runs Locust against it
- Reports: Publishes HTML report via HTML Publisher plugin
- Trigger: Runs on schedule (daily) via cron trigger


#### Setup steps:

1. Create `Jenkinsfile` in your repo root with this content
2. Update `REGISTRY` and `APP_IMAGE` variables to match your Docker registry
3. Update `./path/to/app` to where your app Dockerfile lives
4. Create Docker registry credentials in Jenkins (Manage Jenkins → Credentials)
5. Update `REGISTRY_CREDENTIALS` to match your credential ID
6. Install required Jenkins plugins: Docker Pipeline, HTML Publisher
7. Create a Pipeline job pointing to your repository
8. The cron trigger will run the pipeline automatically
