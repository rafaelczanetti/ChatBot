import nltk
import os
import json
import requests
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import config

class ChatBot:
    def __init__(self):
        self.responses = {}
        self.load_responses()
        
        # Download NLTK resources if not already downloaded
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
            nltk.download('wordnet')
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('portuguese'))
        
        # API Configuration
        self.api_key = config.API_KEY
        self.api_url = config.API_URL
        self.anthropic_version = "2023-06-01"  # Versão atual da API conforme documentação
        self.model = "claude-3-5-sonnet-20240620"  # Usando o modelo Claude 3.5 Sonnet
        self.model_config = config.MODEL_CONFIG
    
    def load_responses(self):
        """Load predefined responses from JSON file"""
        try:
            with open('responses.json', 'r', encoding='utf-8') as file:
                self.responses = json.load(file)
        except FileNotFoundError:
            # Create basic responses if file doesn't exist
            self.responses = {
                "greetings": {
                    "patterns": ["olá", "oi", "bom dia", "boa tarde", "boa noite", "hey"],
                    "responses": ["Olá! Como posso ajudar?", "Oi! Em que posso ser útil hoje?"]
                },
                "goodbye": {
                    "patterns": ["tchau", "adeus", "até logo", "até mais"],
                    "responses": ["Até logo!", "Tenha um bom dia!", "Obrigado por conversar comigo!"]
                },
                "fallback": {
                    "responses": ["Desculpe, não entendi. Pode reformular?", 
                                 "Não tenho certeza do que você quer dizer.",
                                 "Poderia explicar de outra forma?"]
                }
            }
            # Save the default responses
            self.save_responses()
    
    def save_responses(self):
        """Save responses to JSON file"""
        with open('responses.json', 'w', encoding='utf-8') as file:
            json.dump(self.responses, file, ensure_ascii=False, indent=4)
    
    def preprocess_text(self, text):
        """Preprocess text by tokenizing, removing stopwords, and lemmatizing"""
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in self.stop_words]
        return tokens
    
    def find_best_match(self, user_message):
        """Find the best matching intent for the user message"""
        tokens = self.preprocess_text(user_message)
        best_match = None
        highest_score = 0
        
        for intent, data in self.responses.items():
            if intent == "fallback":
                continue
                
            for pattern in data.get("patterns", []):
                pattern_tokens = self.preprocess_text(pattern)
                
                # Simple matching based on common words
                common_words = set(tokens).intersection(set(pattern_tokens))
                score = len(common_words) / max(len(tokens), len(pattern_tokens)) if tokens else 0
                
                if score > highest_score:
                    highest_score = score
                    best_match = intent
        
        # Return intent if score is above threshold, otherwise use fallback
        return best_match if highest_score > 0.2 else "fallback"
    
    def get_ai_response(self, user_message):
        """Get response from the AI API"""
        try:
            headers = {
                "anthropic-version": self.anthropic_version,
                "content-type": "application/json",
                "x-api-key": self.api_key
            }
            
            data = {
                "model": self.model,
                "max_tokens": self.model_config.get("max_tokens", 300),
                "temperature": self.model_config.get("temperature", 0.7),
                "top_p": self.model_config.get("top_p", 0.9),
                "system": "Você é um assistente virtual em português do Brasil. Responda perguntas de forma clara, amigável e direta. Utilize linguagem simples. Evite respostas muito longas.",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=config.MAX_RESPONSE_TIME)
            
            if response.status_code == 200:
                response_data = response.json()
                return response_data.get("content", [{}])[0].get("text", self._get_fallback_response())
            elif response.status_code == 401:
                print("Erro de autenticação: Verifique sua API key")
                return self._get_fallback_response()
            elif response.status_code == 429:
                print("Limite de taxa excedido: Muitas solicitações em um curto período")
                return self._get_fallback_response()
            else:
                print(f"Erro na API: {response.status_code} - {response.text}")
                return self._get_fallback_response()
                
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {str(e)}")
            return self._get_fallback_response()
        except Exception as e:
            print(f"Erro ao chamar a API: {str(e)}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self):
        """Get a fallback response when API fails"""
        import random
        responses = self.responses["fallback"].get("responses", [])
        return random.choice(responses) if responses else "Desculpe, não consegui processar sua solicitação."
    
    def get_response(self, user_message):
        """Generate a response based on the user's message"""
        try:
            # Tenta usar a API para responder
            return self.get_ai_response(user_message)
        except Exception as e:
            print(f"Erro ao usar a API: {str(e)}")
            # Se não conseguir usar a API, volta para o método original
            intent = self.find_best_match(user_message)
            
            if intent in self.responses:
                import random
                responses = self.responses[intent].get("responses", [])
                return random.choice(responses) if responses else "Não sei como responder a isso."
            else:
                return "Desculpe, não entendi. Pode reformular?" 