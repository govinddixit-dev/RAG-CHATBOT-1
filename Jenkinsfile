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
		booleanParam(name: 'PUSH_IMAGE', defaultValue: true, description: 'Push Docker image to AWS ECR')
	}

	environment {
		DOCKER_BUILDKIT = '1'
		COMPOSE_DOCKER_CLI_BUILD = '1'
		IMAGE_NAME = 'chatbot-app'
		IMAGE_TAG = "${env.BUILD_NUMBER}"
		AWS_REGION = 'eu-north-1'
		AWS_ACCOUNT_ID = '465768368073'
		ECR_REPO = 'rag-bot-ecr'
		ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
		IMAGE_URI = "${ECR_REGISTRY}/${ECR_REPO}"
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
					GROQ_API_KEY=gsk_test_dummy_key docker compose up -d backend
					for i in $(seq 1 15); do
						if curl -fsS http://localhost:8000/health; then
							echo "Health check passed on attempt $i"
							exit 0
						fi
						echo "Attempt $i failed, retrying in 2s..."
						sleep 2
					done
					echo "Health check failed after 15 attempts"
					docker compose logs backend
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
					docker tag ${IMAGE_NAME}:latest ${IMAGE_URI}:${IMAGE_TAG}
					docker tag ${IMAGE_NAME}:latest ${IMAGE_URI}:latest
				'''
			}
		}

		stage('Push to ECR') {
			when {
				expression { return params.PUSH_IMAGE }
			}
			steps {
				withCredentials([[
					$class: 'AmazonWebServicesCredentialsBinding',
					credentialsId: 'aws-token'
				]]) {
					sh '''
						set -e
						aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
						docker push ${IMAGE_URI}:${IMAGE_TAG}
						docker push ${IMAGE_URI}:latest
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
