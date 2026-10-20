pipeline {
  agent any

  environment {
    IMAGE_NAME = "tst-lambda:k8s"
    K8S_DIR = "./"
    TRIVY_CACHE = "/tmp/trivy-cache"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }



  stage('Quality & Sec') {
    parallel {
      stage('Semgrep SAST') {
        steps { 
            catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE'){
          sh '''
          #python3 -m venv .venv
          #.venv/bin/pip install --resume-retries 5 semgrep
          semgrep  --config=auto
          
          ''' 
          }
      }
    }  
      stage('Gitleaks Secrets') {
        steps { catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE'){
            
            sh 'gitleaks detect --source=. --log-opts="-1" --verbose --report-path=gitleaks-report.json --exit-code=1' }
        }
      }  
    }
  }

  stage('Semgrep - SAST + Custom') {
  steps {
      catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE'){
    sh '''

    semgrep --config .semgrep/rules/lambda-rules.yaml .
    semgrep --config=auto --config=.semgrep/rules/ --error 
    '''
    }
  }
}

    stage('Build Docker') {
      steps {
        sh '''
        echo ">> Building ${IMAGE_NAME}"
        docker build -t ${IMAGE_NAME} .
        '''
      }
    }

    stage('Trivy Scan') {
      steps {
        sh '''
        mkdir -p ${TRIVY_CACHE}
        echo ">> Scanning ${IMAGE_NAME} (HIGH,CRITICAL only)"
        
        # Usa a imagem do Trivy via docker
        docker run --rm \
          -v /var/run/docker.sock:/var/run/docker.sock \
          -v ${TRIVY_CACHE}:/root/.cache \
          aquasec/trivy:0.58.0 image \
          --severity HIGH,CRITICAL \
          --ignore-unfixed \
          --exit-code 1 \
          --format table \
          ${IMAGE_NAME}

        echo ">> Scan OK - Sem vulnerabilidades críticas"
        '''
      }
    }

    stage('Deploy to k3d') {
      steps {
        sh '''
        echo ">> Deploy no k3d"
        # Rancher Desktop já deixa o kubeconfig em ~/.kube
        kubectl config use-context rancher-desktop

        # Aplica Deployment
          kubectl apply -f ./cicd/deployment.yaml

        kubectl rollout status deployment -n app -l app=tst-lambda --timeout=60s || true
        kubectl get all -n app
        '''
      }
    }
  }

  

  post {
    failure {
      echo "❌ Pipeline falhou. Se foi no Trivy, tem CVE CRITICAL com fix. Veja o log acima."
    }
    success {
      echo "✅ Build + Scan + Deploy OK no k3d!"
    }
  }
}