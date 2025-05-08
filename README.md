# Flask Chatbot

Um chatbot simples desenvolvido em Flask para responder a consultas do usuário em português.

## Funcionalidades

- Interface de chat simples e intuitiva
- Processamento básico de linguagem natural
- Respostas pré-definidas baseadas em padrões
- Design responsivo para desktop e mobile
- Integração com API Claude da Anthropic

## Requisitos

- Python 3.7 ou superior
- Flask
- NLTK (Natural Language Toolkit)
- Outras dependências listadas em requirements.txt

## Instalação

1. Clone este repositório ou baixe os arquivos

2. Crie um ambiente virtual (opcional, mas recomendado)
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Instale as dependências
   ```
   pip install -r requirements.txt
   ```

4. Execute o aplicativo
   ```
   python app.py
   ```

5. Acesse o chatbot no navegador: `http://127.0.0.1:5000`

## Configuração da API

### Anthropic Claude
A API do Claude está configurada no arquivo `config.py`. Você pode ajustar as seguintes configurações:
- `API_KEY`: Sua chave de API do Anthropic
- `MODEL_CONFIG`: Configurações do modelo como temperatura e número máximo de tokens

## Estrutura do Projeto

```
/
├── app.py              # Aplicação Flask principal
├── chatbot.py          # Lógica do chatbot
├── responses.json      # Definições de respostas do chatbot
├── requirements.txt    # Dependências do projeto
├── config.py           # Configurações do chatbot e APIs
├── static/             # Arquivos estáticos
│   ├── css/
│   │   └── style.css   # Estilos CSS
│   ├── images/
│   │   └── chatbot-icon.svg # Ícone do chatbot
│   └── js/
│       └── script.js   # JavaScript do frontend
└── templates/
    └── index.html      # Template HTML principal
```

## Personalização

Você pode personalizar as respostas do chatbot editando o arquivo `responses.json`. A estrutura do arquivo é:

```json
{
    "intent_name": {
        "patterns": ["padrão1", "padrão2", ...],
        "responses": ["resposta1", "resposta2", ...]
    },
    ...
}
```

## APIs disponíveis

- `/api/chat` - API do chatbot usando o modelo Claude da Anthropic

## Expandindo o Chatbot

Para adicionar novas funcionalidades:

1. Adicione novos padrões e respostas em `responses.json`
2. Modifique `chatbot.py` para implementar lógica adicional
3. Atualize a interface conforme necessário

## Interface do Usuário

A interface do chatbot é composta por:
- Um cabeçalho com o nome do assistente
- Área de mensagens para exibir a conversa
- Sugestões de mensagens pré-definidas para início rápido
- Campo de entrada de texto com botão de envio

O design é totalmente responsivo e se adapta a dispositivos móveis e desktop.

## Animações e Elementos Visuais

- Animação de digitação com três pontos durante o carregamento das respostas
- Ícones SVG para mensagens do usuário e do chatbot
- Efeitos suaves de transição para melhor experiência do usuário

![Captura de tela 2025-05-08 111642](https://github.com/user-attachments/assets/cc54cd5a-d330-485d-8e22-af4dacf35566)

