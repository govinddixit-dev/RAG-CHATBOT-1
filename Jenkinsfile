pipeline {
	agent any

	options {
		timestamps()
		disableConcurrentBuilds()
		buildDiscarder(logRotator(numToKeepStr: '20'))
		timeout(time: 30, unit: 'MINUTES')
	}

	parameters {
		booleanParam(name: 'RUN_SMOKE_TEST', defaultValue: true, description: 'Start backend container and check /health endpoint')
		booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push Docker image to registry (requires credentials)')
	}

	environment {
		DOCKER_BUILDKIT = '1'
		COMPOSE_DOCKER_CLI_BUILD = '1'
		IMAGE_NAME = 'chatbot-app'
		IMAGE_TAG = "${env.BUILD_NUMBER}"
		REGISTRY_URL = 'docker.io'
		REGISTRY_REPO = 'your-dockerhub-username/rag-chatbot'
	}

	stages {
		stage('Checkout') {
			steps {
				checkout scmGit(
					branches: [[name: '*/main']],
					extensions: [],
					userRemoteConfigs: [[
						credentialsId: 'github-token',
						url: 'https://github.com/govinddixit-dev/RAG-CHATBOT-1.git'
					]]
				)
			}
		}

		stage('Build Image') {
			steps {
				sh 'docker compose build'
			}
		}

		stage('Smoke Test (Backend Health)') {
			when {
				expression { return params.RUN_SMOKE_TEST }
			}
			steps {
				sh '''
					set -e
					docker compose up -d backend
					# Wait for the container to start
					sleep 10
					# Run health check inside the backend container (curl not available, use python)
					docker exec chatbot-backend python3 -c "
import urllib.request, sys
try:
    res = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=10)
    print('Health check passed:', res.read().decode())
except Exception as e:
    print('Health check failed:', e)
    sys.exit(1)
"
				'''
			}
			post {
				always {
					sh 'docker compose down || true'
				}
			}
		}

		stage('Tag Image') {
			when {
				expression { return params.PUSH_IMAGE }
			}
			steps {
				sh '''
					set -e
					docker tag ${IMAGE_NAME}:latest ${REGISTRY_URL}/${REGISTRY_REPO}:${IMAGE_TAG}
					docker tag ${IMAGE_NAME}:latest ${REGISTRY_URL}/${REGISTRY_REPO}:latest
				'''
			}
		}

		stage('Push Image') {
			when {
				expression { return params.PUSH_IMAGE }
			}
			steps {
				withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
					sh '''
						set -e
						echo "$DOCKER_PASS" | docker login ${REGISTRY_URL} -u "$DOCKER_USER" --password-stdin
						docker push ${REGISTRY_URL}/${REGISTRY_REPO}:${IMAGE_TAG}
						docker push ${REGISTRY_URL}/${REGISTRY_REPO}:latest
						docker logout ${REGISTRY_URL}
					'''
				}
			}
		}
	}

	post {
		always {
			sh 'docker image prune -f || true'
		}
		success {
			echo 'Pipeline completed successfully.'
		}
		failure {
			echo 'Pipeline failed. Check stage logs for details.'
		}
	}
}
