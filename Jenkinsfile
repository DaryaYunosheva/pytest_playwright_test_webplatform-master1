pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    tools {
        jdk 'jdk21'
    }

    environment {
        BASE_URL = 'http://localhost:5137'
        API_URL  = 'http://localhost:8888'
    }


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

        stage('Wait for app') {
            steps {
                bat '''
                    echo Waiting for frontend...
                    powershell -Command "$timeout=120;$elapsed=0; while ($elapsed -lt $timeout) { try { Invoke-WebRequest -Uri %BASE_URL% -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host 'Frontend is ready'; exit 0 } catch { Start-Sleep -Seconds 5; $elapsed += 5 } }; Write-Error 'Frontend did not start'; exit 1"
                '''
                bat '''
                    echo Waiting for backend...
                    powershell -Command "$timeout=120;$elapsed=0; while ($elapsed -lt $timeout) { try { Invoke-WebRequest -Uri %API_URL% -UseBasicParsing -TimeoutSec 5 | Out-Null; Write-Host 'Backend is ready'; exit 0 } catch { Start-Sleep -Seconds 5; $elapsed += 5 } }; Write-Error 'Backend did not start'; exit 1"
                '''
            }
        }

        stage('Install test dependencies') {
            steps {
                bat '''
                    if exist .venv rmdir /s /q .venv
                    python -m venv .venv

                    .venv\\Scripts\\python.exe -m pip install --upgrade pip
                    .venv\\Scripts\\python.exe -m pip install -r backend\\requirements.txt
                    .venv\\Scripts\\python.exe -m pip install -r backend\\requirements-test.txt

                    .venv\\Scripts\\python.exe -m playwright install chromium
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

        stage('Run E2E tests') {
            steps {
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
                    bat '''
                        if exist frontend\\allure-results rmdir /s /q frontend\\allure-results
                        if exist frontend\\traces rmdir /s /q frontend\\traces

                        mkdir frontend\\allure-results
                        mkdir frontend\\traces

                        set BASE_URL=%BASE_URL%
                        set API_URL=%API_URL%

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