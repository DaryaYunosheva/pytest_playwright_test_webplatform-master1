pipeline {
    agent any

    // Автотриггер: если джоба настроена как "Pipeline script from SCM" +
    // включён GitLab/GitHub webhook (или Poll SCM ниже) - сборка стартует
    // сама при пуше в репозиторий. Без этого блока пайплайн запускается
    // только вручную, что и выглядело как "странная" работа CI.


    tools {
        jdk 'jdk21' // нужен для Allure CLI, который вызывается через шаг allure ниже
    }

    environment {
        BASE_URL = 'http://localhost:5137'
        API_URL  = 'http://localhost:8888'
    }

    options {
        timestamps()
        disableConcurrentBuilds() // 2 параллельных docker-compose на одних портах = коллизия
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
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

        stage('Stop previous containers') {
            steps {
                // Данные в Postgres (volume) намеренно НЕ трогаем -
                // они переживают билд к билду. Останавливаем только
                // старые контейнеры, чтобы поднять их заново на актуальном коде.
                bat 'docker-compose down || exit 0'
            }
        }

        stage('Start app') {
            steps {
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
            echo 'Stopping application (data volumes kept)'
            bat 'docker-compose down || exit 0'

            archiveArtifacts artifacts: 'backend/allure-results/**, backend/test-results.xml, frontend/allure-results/**, frontend/traces/**, frontend/test-results.xml',
                allowEmptyArchive: true

            junit testResults: 'backend/test-results.xml, frontend/test-results.xml',
                allowEmptyResults: true

            // Требует установленного плагина "Allure Jenkins Plugin" и
            // сконфигурированного Allure Commandline в
            // Manage Jenkins -> Tools -> Allure Commandline installations (имя 'allure').
            // Без этого шага allure-results просто лежат сырыми файлами -
            // отчёта в интерфейсе Jenkinsа не будет, хотя JDK для него уже подключен.
            allure includeProperties: false,
                jdk: '',
                results: [[path: 'backend/allure-results'], [path: 'frontend/allure-results']]
        }
    }
}