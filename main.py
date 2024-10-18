from flask import Flask, render_template, request
import openai  # Assure-toi d'importer correctement le module openai
from dotenv import load_dotenv  # Importation de load_dotenv
import os  # Pour accéder aux variables d'environnement

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configure la clé API pour GPT-4 depuis le fichier .env
openai.api_key = os.getenv("OPENAI_APIKEY")

app = Flask(__name__)

# Contexte fort à inclure dans chaque requête pour le chatbot
def generate_prompt(question):
    context = """
    Le site est un site WordPress hébergé sur Hostinger. 
    Le thème utilisé est Aravalli. 
    Les plugins installés pour les paiements bancaires et PayPal sont WooCommerce et WooPayments.
    Réponds aux questions en gardant ce contexte et en fournissant des réponses spécifiques à la gestion et la configuration du site.
    """
    return f"{context}\nQuestion: {question}"

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        question = request.form["question"]
        response = ask_gpt4(question)
        return render_template("bot.html", question=question, response=response)
    return render_template("bot.html")

def ask_gpt4(question):
    prompt = generate_prompt(question)
    
    # Appel correct à l'API OpenAI GPT-4 avec le modèle chat
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # Contexte global du chatbot
            {"role": "user", "content": prompt}  # La question posée par l'utilisateur
        ],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    return response['choices'][0]['message']['content'].strip()

# Nouvelle route pour le tutoriel (index.html)
@app.route("/tutorial")
def tutorial():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
