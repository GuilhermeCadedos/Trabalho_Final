from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import csv
import os
from datetime import datetime
import requests
import json
import time

# ----------------------------
# CONFIGURAÇÃO BÁSICA
# ----------------------------
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)

# Caminho do CSV
CSV_FILE = os.path.join("static", "data", "novembro_azul.csv")
os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

# Chave da API Gemini (atualize aqui com sua chave válida)
GEMINI_API_KEY = "AIzaSyCniHesGB7mjEXfP53Lhu-UOeFtDxbtVuY"

# Endpoint e modelo oficial do Google GenAI
MODEL_NAME = "gemini-2.5-flash"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

# ----------------------------
# FUNÇÃO PARA SALVAR NO CSV
# ----------------------------
def salvar_no_csv(usuario, resposta):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Data/Hora", "Mensagem do Usuário", "Resposta do Chatbot"])
        writer.writerow([agora, usuario, resposta])

# ----------------------------
# FUNÇÃO DO CHATBOT (Gemini) COM RETRY E FALLBACK
# ----------------------------
def get_chatbot_response(user_input):
    hora_atual = datetime.now().strftime("%H:%M")
    
    prompt_system = (
        f"Você é um assistente especializado em conscientização do Novembro Azul. "
        f"Sempre dê ênfase a temas de câncer de próstata, prevenção, sintomas e check-ups. "
        f"A hora atual é {hora_atual}. "
        f"Responda de forma clara, amigável e educativa."
    )

    data = {
        "system_instruction": {"role": "system", "parts": [{"text": prompt_system}]},
        "contents": [{"role": "user", "parts": [{"text": f"O usuário perguntou: '{user_input}'"}]}],
        "generation_config": {"max_output_tokens": 200}
    }

    url_with_key = f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}"
    resposta_texto = None
    tentativas = 3

    for tentativa in range(tentativas):
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(url_with_key, headers=headers, json=data)
            response.raise_for_status()
            json_response = response.json()
            logging.info(f"Resposta Completa do Gemini: {json.dumps(json_response, indent=2, ensure_ascii=False)}")

            # Extração segura da resposta
            candidates = json_response.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts and parts[0].get("text", "").strip():
                    resposta_texto = parts[0]["text"].strip()
            break

        except requests.exceptions.HTTPError as errh:
            logging.warning(f"Tentativa {tentativa+1}: HTTP Error: {errh}")
            time.sleep(2)
        except Exception as e:
            logging.error(f"Erro geral: {e}")
            time.sleep(2)

    # Fallback caso a resposta esteja vazia
    if not resposta_texto:
        resposta_texto = (
            "Olá! Sou o Chatbot do Novembro Azul. "
            "Não consegui gerar uma resposta detalhada agora, mas lembre-se: "
            "fazer check-ups regularmente e ficar atento aos sintomas é fundamental. "
            "Pergunte sobre prevenção, sintomas ou exames!"
        )

    salvar_no_csv(user_input, resposta_texto)
    return resposta_texto

# ----------------------------
# ROTAS DE PÁGINAS HTML
# ----------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# ----------------------------
# API DO CHATBOT
# ----------------------------
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Corpo da requisição deve conter 'message'"}), 400

    user_message = data['message'].strip()
    if not user_message:
        return jsonify({"error": "Mensagem vazia"}), 400

    response_text = get_chatbot_response(user_message)
    return jsonify({"response": response_text})

# ----------------------------
# ROTA DE TESTE
# ----------------------------
@app.route('/teste', methods=['GET'])
def teste():
    return jsonify({"status": "Servidor Flask rodando com sucesso!"}), 200

# ----------------------------
# RODAR O SERVIDOR
# ----------------------------
if __name__ == '__main__':
    logging.info("Iniciando Servidor Flask em http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
