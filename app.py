import os
from flask import Flask, request, jsonify, render_template
from chatbot import ChatBot
import config

app = Flask(__name__)
app.config.from_object(config)
app.config['CHATBOT_NAME'] = 'Assistente'
chatbot = ChatBot()

@app.route('/')
def index():
    return render_template('index.html', chatbot_name=app.config.get('CHATBOT_NAME', 'ChatBot'))

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chatbot.get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False)) 