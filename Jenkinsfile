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
					# Pass a dummy key so the app can start (no real LLM calls in smoke test)
					GROQ_API_KEY=gsk_test_dummy_key docker compose up -d backend
					# Retry health check up to 30 seconds
					for i in $(seq 1 15); do
						if docker exec chatbot-backend python3 -c "
import urllib.request
res = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)
print(res.read().decode())
" 2>/dev/null; then
							echo "Health check passed on attempt $i"
							exit 0
						fi
						echo "Attempt $i: backend not ready, retrying in 2s..."
						sleep 2
					done
					echo "Health check failed after 30s. Container logs:"
					docker logs chatbot-backend --tail 50
					exit 1
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
