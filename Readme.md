
# 🚀 tst-lambda - Serverless API Local (AWS SAM)

API Serverless completa rodando 100% local com AWS SAM, sem precisar de conta AWS. Projeto criado para estudos de DevOps / SRE.

### ✅ O que essa API faz

Uma Lambda em Python que é mais que Hello World:

* `GET /hello?name=Deivids` -> retorna mensagem personalizada
* `POST /hello` com `{"name": "Deivids"}` -> mesma coisa, via body JSON
* Lê variáveis de ambiente (`ENV`, `BUCKET_NAME`)
* Logs de observabilidade no CloudWatch (simulado no terminal do SAM)
* API Gateway configurado com `Method: any`

### 🛠️ Stack

- Python 3.11
- AWS Lambda + API Gateway
- AWS SAM CLI
- S3 (configurado no template.yaml)

### ▶️ Como rodar

```bash
# 1. Build
sam build

# 2. Sobe API local
sam local start-api
# vai subir em http://127.0.0.1:3000

# 3. Testa (em outro terminal)
# GET
curl "http://127.0.0.1:3000/hello?name=Deivids Senior DevOps"

# POST
curl -X POST http://127.0.0.1:3000/hello \
  -H "Content-Type: application/json" \
  -d '{"name":"Deivids Teste DevOps"}'
```
