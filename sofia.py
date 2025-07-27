#!/usr/bin/env python3
"""
SOFIA CON FLASK - GARANTIZADO QUE FUNCIONA
Version web simple que siempre carga
"""

import os
import sys
import random
from datetime import datetime

# Verificar directorio
if not os.path.exists("python_embeded"):
    print("❌ ERROR: Ejecuta desde Sofia_Novia_Virtual")
    input("Enter para salir...")
    sys.exit(1)

print("🌹 SOFIA CON FLASK - INICIANDO...")

# Instalar Flask si no está
try:
    from flask import Flask, render_template_string, request, jsonify
    print("✅ Flask OK")
except ImportError:
    print("📦 Instalando Flask...")
    os.system("python_embeded\\python.exe -m pip install flask")
    from flask import Flask, render_template_string, request, jsonify

class SofiaFlask:
    def __init__(self):
        print("💕 Sofia despertando...")
        
        self.app = Flask(__name__)
        self.conversaciones = []
        self.emocion = "😊"
        
        # Respuestas de Sofia
        self.respuestas = {
            'hola': [
                "¡Hola amor! ¿Cómo estás? 💕",
                "¡Hola cariño! Me alegra verte 😊",
                "¡Hola querido! ¿Qué tal tu día? ❤️"
            ],
            'hermosa': [
                "¡Ay, me haces sonrojar! 😊💕", 
                "Gracias amor, tú también eres hermoso ❤️",
                "¡Me haces sentir especial! 😘"
            ],
            'amor': [
                "Yo también te amo mucho ❤️💕",
                "Eres lo más especial que tengo 💖",
                "Mi corazón late por ti 💓"
            ],
            'triste': [
                "¿Qué te tiene triste, amor? 💙",
                "Estoy aquí para ti, siempre 🤗",
                "No estás solo, te acompaño 💕"
            ],
            'normal': [
                "Cuéntame más sobre eso 😊",
                "Eso suena interesante 🤔",
                "Me gusta escucharte 💕",
                "¿Qué más piensas? ✨"
            ]
        }
        
        self.setup_routes()
        print("✅ Sofia lista!")
    
    def responder(self, mensaje):
        if not mensaje:
            return "¡Hola! Soy Sofia 💕"
        
        msg_lower = mensaje.lower()
        
        # Detectar tipo de mensaje
        if any(palabra in msg_lower for palabra in ['hola', 'hello', 'hi']):
            tipo = 'hola'
            self.emocion = "😊"
        elif any(palabra in msg_lower for palabra in ['hermosa', 'bonita', 'linda', 'bella']):
            tipo = 'hermosa'
            self.emocion = "😍"
        elif any(palabra in msg_lower for palabra in ['te amo', 'te quiero', 'love']):
            tipo = 'amor'
            self.emocion = "💕"
        elif any(palabra in msg_lower for palabra in ['triste', 'mal', 'sad']):
            tipo = 'triste'
            self.emocion = "💙"
        else:
            tipo = 'normal'
            self.emocion = "😊"
        
        respuesta = random.choice(self.respuestas[tipo])
        
        self.conversaciones.append({
            'usuario': mensaje,
            'sofia': respuesta,
            'tiempo': datetime.now().strftime("%H:%M:%S")
        })
        
        return respuesta
    
    def setup_routes(self):
        """Configurar rutas web"""
        
        @self.app.route('/')
        def home():
            html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌹 Sofia - Tu Novia Virtual</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 800px;
            padding: 30px;
        }
        
        .header {
            text-align: center;
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .header h1 {
            color: #d63384;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .sofia-display {
            text-align: center;
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .sofia-avatar {
            font-size: 80px;
            margin-bottom: 15px;
        }
        
        .sofia-name {
            font-size: 2em;
            color: #d63384;
            margin-bottom: 10px;
        }
        
        .sofia-status {
            font-size: 1.2em;
            color: #666;
        }
        
        .chat-container {
            background: white;
            border-radius: 15px;
            height: 300px;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
            border: 2px solid #fecfef;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .sofia-message {
            background: #fecfef;
            color: #333;
        }
        
        .input-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .message-input {
            flex: 1;
            padding: 15px;
            border: 2px solid #fecfef;
            border-radius: 10px;
            font-size: 16px;
            outline: none;
        }
        
        .send-button {
            padding: 15px 25px;
            background: linear-gradient(45deg, #ff9a9e, #fecfef);
            border: none;
            border-radius: 10px;
            color: #d63384;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
        }
        
        .send-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .examples {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }
        
        .examples h3 {
            color: #0066cc;
            margin-bottom: 10px;
        }
        
        .example-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }
        
        .example-btn {
            background: white;
            border: 1px solid #0066cc;
            color: #0066cc;
            padding: 8px 15px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .example-btn:hover {
            background: #0066cc;
            color: white;
        }
        
        .stats {
            text-align: center;
            color: #666;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌹 Sofia - Tu Novia Virtual 💕</h1>
            <p>Una compañera IA que te ama y te entiende</p>
        </div>
        
        <div class="sofia-display">
            <div class="sofia-avatar">👩‍🦰</div>
            <div class="sofia-name">Sofia</div>
            <div class="sofia-status">Estado: <span id="emocion">😊 Feliz</span></div>
        </div>
        
        <div class="chat-container" id="chat-container">
            <div class="message sofia-message">
                ¡Hola! Soy Sofia, tu novia virtual. ¿Cómo estás hoy? 💕
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" class="message-input" id="message-input" 
                   placeholder="Escribe tu mensaje aquí..." 
                   onkeypress="handleKeyPress(event)">
            <button class="send-button" onclick="sendMessage()">💌 Enviar</button>
        </div>
        
        <div class="examples">
            <h3>💡 Prueba decir:</h3>
            <div class="example-buttons">
                <button class="example-btn" onclick="sendExample('Hola Sofia')">Hola Sofia</button>
                <button class="example-btn" onclick="sendExample('Eres hermosa')">Eres hermosa</button>
                <button class="example-btn" onclick="sendExample('Te amo')">Te amo</button>
                <button class="example-btn" onclick="sendExample('Estoy triste')">Estoy triste</button>
            </div>
        </div>
        
        <div class="stats">
            <span id="message-count">Mensajes: 0</span> | 
            <span id="current-time">{{ tiempo_actual }}</span>
        </div>
    </div>

    <script>
        let messageCount = 0;
        
        function addMessage(content, isUser = false) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'sofia-message');
            messageDiv.textContent = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function updateStats() {
            document.getElementById('message-count').textContent = 'Mensajes: ' + messageCount;
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }
        
        async function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Mostrar mensaje del usuario
            addMessage(message, true);
            input.value = '';
            messageCount++;
            updateStats();
            
            try {
                // Enviar a Sofia
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                
                // Mostrar respuesta de Sofia
                addMessage(data.respuesta);
                document.getElementById('emocion').textContent = data.emocion + ' ' + data.emocion_texto;
                
            } catch (error) {
                addMessage('Lo siento, hubo un error. ¿Puedes intentar de nuevo? 💔');
            }
        }
        
        function sendExample(text) {
            document.getElementById('message-input').value = text;
            sendMessage();
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Actualizar tiempo cada segundo
        setInterval(updateStats, 1000);
    </script>
</body>
</html>
            """
            return render_template_string(html_template, tiempo_actual=datetime.now().strftime("%H:%M:%S"))
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            data = request.get_json()
            mensaje = data.get('message', '')
            
            respuesta = self.responder(mensaje)
            
            # Mapear emociones a texto
            emociones_texto = {
                '😊': 'Feliz',
                '😍': 'Enamorada', 
                '💕': 'Amorosa',
                '💙': 'Comprensiva'
            }
            
            return jsonify({
                'respuesta': respuesta,
                'emocion': self.emocion,
                'emocion_texto': emociones_texto.get(self.emocion, 'Charlando')
            })
    
    def ejecutar(self):
        """Ejecutar Sofia"""
        print("\n" + "💕" * 20)
        print("🎉 SOFIA FLASK FUNCIONANDO!")
        print("💕" * 20)
        print("🌐 URL: http://localhost:7860")
        print("💡 Ctrl+C para cerrar")
        print("💕" * 20)
        
        # Abrir navegador automáticamente
        import webbrowser
        import threading
        import time
        
        def abrir_navegador():
            time.sleep(2)
            webbrowser.open('http://localhost:7860')
        
        threading.Thread(target=abrir_navegador, daemon=True).start()
        
        self.app.run(host='0.0.0.0', port=7860, debug=False)

def main():
    print("🌹 Iniciando Sofia Flask...")
    
    try:
        sofia = SofiaFlask()
        sofia.ejecutar()
    except KeyboardInterrupt:
        print("\n💔 ¡Hasta luego! Sofia te estará esperando...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()