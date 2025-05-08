"""
Configurações do chatbot
"""

# Configurações do Flask
DEBUG = True

# Personalização do chatbot
CHATBOT_NAME = "Assistente Virtual"

# API de IA - Anthropic (Claude)
API_KEY = "[SUA_API_KEY_AQUI]"  # Substitua com sua chave da API Anthropic
API_URL = "https://api.anthropic.com/v1/messages"

# Configurações do modelo
MODEL_CONFIG = {
    "temperature": 0.7,       # Controla a criatividade (0.0 a 1.0)
    "max_tokens": 300,        # Número máximo de tokens na resposta
    "top_p": 0.9,             # Amostragem de núcleo (0.0 a 1.0)
}

# Configurações avançadas
MAX_RESPONSE_TIME = 5  # segundos 