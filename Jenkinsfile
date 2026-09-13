pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    tools {
        jdk 'jdk21'
    }

    stages {

        stage('Check environment') {
            steps {
                bat 'java -version'
                bat 'git --version'
                bat 'docker --version'
                bat 'docker-compose version'
                bat 'python --version'
            }
        }


        stage('Start app') {
            steps {
                bat 'docker-compose down || exit 0'
                bat 'docker-compose up -d --build'
            }
        }

        stage('Install test dependencies') {
            steps {
                bat '''
                    if exist .venv rmdir /s /q .venv
                    python -m venv .venv
                    .venv\\Scripts\\python.exe -m pip install -r backend\\requirements.txt
                    .venv\\Scripts\\python.exe -m pip install -r backend\\requirements-test.txt


                '''
            }
        }

        stage('Backend tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '''
                        if exist backend\\allure-results rmdir /s /q backend\\allure-results
                        mkdir backend\\allure-results

                        .venv\\Scripts\\python.exe -m pytest backend\\tests ^
                            --alluredir=backend\\allure-results ^
                            --junitxml=backend\\test-results.xml
                    '''
                }
            }
        }

        stage('Run UI tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '''
                        if exist frontend\\allure-results rmdir /s /q frontend\\allure-results
                        if exist frontend\\traces rmdir /s /q frontend\\traces

                        mkdir frontend\\allure-results
                        mkdir frontend\\traces

                        .venv\\Scripts\\python.exe -m pytest frontend\\e2e\\tests ^
                            --alluredir=frontend\\allure-results ^
                            --junitxml=frontend\\test-results.xml
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Stopping application'
            bat 'docker-compose down || exit 0'

            archiveArtifacts artifacts: 'backend/allure-results/**, backend/test-results.xml, frontend/allure-results/**, frontend/traces/**, frontend/test-results.xml',
                allowEmptyArchive: true

            junit testResults: 'backend/test-results.xml, frontend/test-results.xml',
                allowEmptyResults: true

            allure results: [[path: 'backend/allure-results'], [path: 'frontend/allure-results']]
        }
    }
}