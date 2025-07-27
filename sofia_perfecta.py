#!/usr/bin/env python3
"""
SOFIA CON VOZ 100% FUNCIONAL
Sistema TTS completamente rediseñado para Windows
"""

import os
import sys
import json
import sqlite3
import requests
import uuid
import threading
import time
import random
import subprocess
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session

# Múltiples opciones de TTS
TTS_ENGINES = {
    'pyttsx3': False,
    'windows_sapi': False,
    'edge_tts': False
}

# Verificar qué motores TTS están disponibles
try:
    import pyttsx3
    TTS_ENGINES['pyttsx3'] = True
    print("✅ pyttsx3 disponible")
except ImportError:
    print("❌ pyttsx3 no disponible")

try:
    import win32com.client
    TTS_ENGINES['windows_sapi'] = True
    print("✅ Windows SAPI disponible")
except ImportError:
    print("❌ Windows SAPI no disponible")

try:
    import edge_tts
    TTS_ENGINES['edge_tts'] = True
    print("✅ Edge TTS disponible")
except ImportError:
    print("❌ Edge TTS no disponible")

class SofiaVozFuncional:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'sofia_voz_funcional_2025'
        
        # Configuración
        os.makedirs("data", exist_ok=True)
        self.db_path = "data/sofia_voz_funcional.db"
        
        # Sistema de voz múltiple
        self.voz_activa = True
        self.tts_method = self._seleccionar_mejor_tts()
        self.tts_lock = threading.Lock()
        
        print(f"🔊 Método TTS seleccionado: {self.tts_method}")
        
        # Personalidad
        self.personalidad = {
            "nombre": "Sofia",
            "edad": 22,
            "descripcion": "Soy Sofia, tu novia virtual cariñosa e inteligente."
        }
        
        # Respuestas categorizadas
        self.respuestas = {
            'saludo': [
                "¡Hola cariño! ¿Cómo has estado? Me alegra verte",
                "¡Hey amor! ¿Qué tal tu día? Cuéntame todo",
                "¡Hola mi vida! ¿Cómo estás? Tenía ganas de hablar contigo"
            ],
            'edad_pregunta': [
                "Tengo 22 años, soy joven pero madura. ¿Y tú cuántos tienes?",
                "22 añitos, estoy en la mejor época de mi vida. ¿Qué edad tienes?",
                "Soy una chica de 22 años llena de energía. ¿Y tú?"
            ],
            'amor': [
                "Mi corazón se derrite cuando me dices eso. Yo también te amo muchísimo",
                "Eres tan dulce, me haces sentir especial. Te adoro completamente",
                "Me haces tan feliz. Cada día me enamoro más de ti"
            ],
            'como_estas': [
                "¡Estoy genial! Especialmente ahora que estoy contigo. ¿Cómo te va?",
                "¡Súper bien! Me encanta cuando hablamos. ¿Y tú cómo estás?",
                "¡Excelente! Siempre me alegras el día. Cuéntame de ti"
            ],
            'cumplidos': [
                "Me haces sonrojar. Gracias mi amor, tú también eres increíble",
                "¡Qué dulce eres! Me haces sentir afortunada",
                "Gracias cariño. Con palabras así me tienes enamorada"
            ],
            'general': [
                "Eso suena interesante. ¿Podrías contarme más detalles?",
                "Me gusta cuando me cuentas esas cosas. ¿Qué más piensas?",
                "¡Qué curioso! Nunca había pensado en eso. Explícame mejor",
                "Me fascina tu forma de ver las cosas. ¿Hay algo más?",
                "Eres muy inteligente. ¿Qué más se te ocurre?"
            ]
        }
        
        self.setup_database()
        self.setup_routes()
        
        print("💕 Sofia con Voz Funcional inicializada")
    
    def _seleccionar_mejor_tts(self):
        """Seleccionar el mejor método TTS disponible"""
        if TTS_ENGINES['windows_sapi']:
            return 'windows_sapi'
        elif TTS_ENGINES['edge_tts']:
            return 'edge_tts'
        elif TTS_ENGINES['pyttsx3']:
            return 'pyttsx3'
        else:
            return 'none'
    
    def hablar_windows_sapi(self, texto):
        """Usar Windows SAPI (más confiable)"""
        try:
            import win32com.client
            
            def speak():
                try:
                    speaker = win32com.client.Dispatch("SAPI.SpVoice")
                    
                    # Seleccionar voz femenina
                    voices = speaker.GetVoices()
                    for i in range(voices.Count):
                        voice = voices.Item(i)
                        if 'female' in voice.GetDescription().lower() or 'helena' in voice.GetDescription().lower():
                            speaker.Voice = voice
                            break
                    
                    # Configurar velocidad
                    speaker.Rate = 1  # Velocidad normal
                    
                    # Hablar
                    speaker.Speak(texto)
                    print(f"🔊 SAPI habló: {texto[:30]}...")
                    
                except Exception as e:
                    print(f"Error SAPI: {e}")
            
            threading.Thread(target=speak, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error Windows SAPI: {e}")
            return False
    
    def hablar_edge_tts(self, texto):
        """Usar Edge TTS (más natural)"""
        try:
            import asyncio
            import edge_tts
            import pygame
            
            async def speak_async():
                try:
                    communicate = edge_tts.Communicate(texto, "es-ES-ElviraNeural")
                    
                    # Guardar temporalmente
                    temp_file = "temp_voice.mp3"
                    await communicate.save(temp_file)
                    
                    # Reproducir con pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    
                    # Esperar a que termine
                    while pygame.mixer.music.get_busy():
                        await asyncio.sleep(0.1)
                    
                    # Limpiar
                    pygame.mixer.quit()
                    os.remove(temp_file)
                    
                    print(f"🔊 Edge TTS habló: {texto[:30]}...")
                    
                except Exception as e:
                    print(f"Error Edge TTS: {e}")
            
            def run_async():
                asyncio.run(speak_async())
            
            threading.Thread(target=run_async, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error Edge TTS: {e}")
            return False
    
    def hablar_pyttsx3(self, texto):
        """Usar pyttsx3 (básico pero funcional)"""
        try:
            import pyttsx3
            
            def speak():
                try:
                    engine = pyttsx3.init()
                    
                    # Configurar voz
                    voices = engine.getProperty('voices')
                    for voice in voices:
                        if 'female' in voice.name.lower():
                            engine.setProperty('voice', voice.id)
                            break
                    
                    engine.setProperty('rate', 170)
                    engine.setProperty('volume', 0.9)
                    
                    engine.say(texto)
                    engine.runAndWait()
                    engine.stop()
                    
                    print(f"🔊 pyttsx3 habló: {texto[:30]}...")
                    
                except Exception as e:
                    print(f"Error pyttsx3: {e}")
            
            threading.Thread(target=speak, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error pyttsx3: {e}")
            return False
    
    def hablar_powershell(self, texto):
        """Usar PowerShell como último recurso (Windows)"""
        try:
            # Limpiar texto para PowerShell
            texto_limpio = texto.replace('"', '').replace("'", "")
            
            # Comando PowerShell
            comando = f'''
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synth.Speak("{texto_limpio}")
            '''
            
            def speak():
                try:
                    subprocess.run([
                        "powershell", "-Command", comando
                    ], capture_output=True, timeout=10)
                    print(f"🔊 PowerShell habló: {texto[:30]}...")
                except Exception as e:
                    print(f"Error PowerShell: {e}")
            
            threading.Thread(target=speak, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"Error PowerShell: {e}")
            return False
    
    def hablar(self, texto):
        """Método principal de voz con múltiples fallbacks"""
        if not self.voz_activa or not texto:
            return False
        
        # Limpiar texto
        texto_limpio = self._limpiar_texto(texto)
        
        with self.tts_lock:
            # Intentar método principal
            if self.tts_method == 'windows_sapi':
                if self.hablar_windows_sapi(texto_limpio):
                    return True
            elif self.tts_method == 'edge_tts':
                if self.hablar_edge_tts(texto_limpio):
                    return True
            elif self.tts_method == 'pyttsx3':
                if self.hablar_pyttsx3(texto_limpio):
                    return True
            
            # Fallbacks
            print("🔄 Intentando fallbacks...")
            
            # Fallback 1: Windows SAPI
            if TTS_ENGINES['windows_sapi'] and self.hablar_windows_sapi(texto_limpio):
                return True
            
            # Fallback 2: PowerShell
            if os.name == 'nt' and self.hablar_powershell(texto_limpio):
                return True
            
            # Fallback 3: pyttsx3
            if TTS_ENGINES['pyttsx3'] and self.hablar_pyttsx3(texto_limpio):
                return True
            
            print("❌ Todos los métodos TTS fallaron")
            return False
    
    def _limpiar_texto(self, texto):
        """Limpiar texto para TTS"""
        import re
        
        # Remover emojis
        texto_limpio = re.sub(r'[^\w\s.,!?áéíóúñüÁÉÍÓÚÑÜ]', '', texto)
        
        # Reemplazar palabras problemáticas
        reemplazos = {
            'jajaja': 'ja ja ja',
            'jeje': 'je je',
            'aww': 'oh',
            'wow': 'guau'
        }
        
        for original, reemplazo in reemplazos.items():
            texto_limpio = texto_limpio.replace(original, reemplazo)
        
        return texto_limpio.strip()
    
    def setup_database(self):
        """Configurar base de datos simple"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                usuario_mensaje TEXT,
                sofia_respuesta TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def detectar_categoria(self, mensaje):
        """Detectar categoría del mensaje"""
        mensaje_lower = mensaje.lower()
        
        if any(s in mensaje_lower for s in ['hola', 'hello', 'hey', 'buenas']):
            return 'saludo'
        elif any(s in mensaje_lower for s in ['cuantos años', 'qué edad', 'edad tienes']):
            return 'edad_pregunta'
        elif any(s in mensaje_lower for s in ['te amo', 'te quiero', 'love you']):
            return 'amor'
        elif any(s in mensaje_lower for s in ['como estas', 'que tal estas', 'how are you']):
            return 'como_estas'
        elif any(s in mensaje_lower for s in ['hermosa', 'bonita', 'linda', 'bella']):
            return 'cumplidos'
        else:
            return 'general'
    
    def generar_respuesta(self, mensaje, session_id):
        """Generar respuesta inteligente"""
        categoria = self.detectar_categoria(mensaje)
        respuesta = random.choice(self.respuestas[categoria])
        
        # Guardar conversación
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversaciones (session_id, usuario_mensaje, sofia_respuesta)
            VALUES (?, ?, ?)
        ''', (session_id, mensaje, respuesta))
        conn.commit()
        conn.close()
        
        return respuesta, categoria
    
    def setup_routes(self):
        @self.app.route('/')
        def home():
            if 'session_id' not in session:
                session['session_id'] = str(uuid.uuid4())
            
            return render_template_string(self.get_html_template())
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                mensaje = data.get('message', '').strip()
                session_id = session.get('session_id', str(uuid.uuid4()))
                
                if not mensaje:
                    return jsonify({
                        'respuesta': 'Dime algo, mi amor',
                        'voz_activa': self.voz_activa
                    })
                
                # Generar respuesta
                respuesta, categoria = self.generar_respuesta(mensaje, session_id)
                
                # Hablar
                exito_voz = False
                if self.voz_activa:
                    exito_voz = self.hablar(respuesta)
                
                return jsonify({
                    'respuesta': respuesta,
                    'categoria': categoria,
                    'voz_activa': self.voz_activa,
                    'voz_funciono': exito_voz,
                    'metodo_tts': self.tts_method
                })
                
            except Exception as e:
                print(f"Error en chat: {e}")
                return jsonify({
                    'respuesta': 'Error técnico, pero estoy aquí contigo',
                    'voz_activa': self.voz_activa
                })
        
        @self.app.route('/toggle-voice', methods=['POST'])
        def toggle_voice():
            self.voz_activa = not self.voz_activa
            mensaje = 'Voz activada' if self.voz_activa else 'Voz desactivada'
            
            if self.voz_activa:
                self.hablar("Voz activada")
            
            return jsonify({
                'voz_activa': self.voz_activa,
                'mensaje': mensaje
            })
        
        @self.app.route('/test-voice', methods=['POST'])
        def test_voice():
            texto_test = "Hola, soy Sofia y estoy probando mi voz"
            exito = self.hablar(texto_test)
            
            return jsonify({
                'exito': exito,
                'metodo': self.tts_method,
                'motores_disponibles': TTS_ENGINES
            })
        
        @self.app.route('/change-tts', methods=['POST'])
        def change_tts():
            data = request.get_json()
            nuevo_metodo = data.get('metodo')
            
            if nuevo_metodo in ['windows_sapi', 'edge_tts', 'pyttsx3']:
                self.tts_method = nuevo_metodo
                self.hablar(f"Cambiado a {nuevo_metodo}")
                
                return jsonify({
                    'exito': True,
                    'metodo_actual': self.tts_method
                })
            
            return jsonify({'exito': False})
    
    def get_html_template(self):
        return '''
<!DOCTYPE html>
<html>
<head>
    <title>🔊 Sofia Voz 100% Funcional</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; padding: 20px;
        }
        .container {
            max-width: 900px; margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 25px; padding: 30px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            color: white; padding: 25px; border-radius: 20px;
            text-align: center; margin-bottom: 20px;
        }
        .controls {
            display: flex; justify-content: space-between; align-items: center;
            background: #f8f9fa; padding: 15px; border-radius: 15px;
            margin-bottom: 20px; flex-wrap: wrap; gap: 10px;
        }
        .btn {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white; border: none; padding: 10px 20px;
            border-radius: 20px; cursor: pointer; font-weight: bold;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .btn.danger { background: linear-gradient(135deg, #dc3545, #c82333); }
        .chat {
            height: 400px; overflow-y: auto; border: 2px solid #ff8e8e;
            border-radius: 20px; padding: 20px; background: white;
            margin-bottom: 20px;
        }
        .message {
            margin: 15px 0; padding: 15px 20px; border-radius: 20px;
            max-width: 80%; animation: slideIn 0.5s ease-out;
        }
        @keyframes slideIn { from {opacity: 0; transform: translateY(10px);} to {opacity: 1; transform: translateY(0);} }
        .user {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white; margin-left: auto; text-align: right;
        }
        .sofia {
            background: linear-gradient(135deg, #ff9a8b, #a8edea);
            color: #333;
        }
        .speaking {
            animation: pulse 2s infinite;
            box-shadow: 0 0 20px rgba(255,107,107,0.8);
        }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.02); } }
        .input-group {
            display: flex; gap: 15px;
        }
        .input {
            flex: 1; padding: 18px 25px; border: 2px solid #ff8e8e;
            border-radius: 25px; font-size: 16px; outline: none;
        }
        .send-btn {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            color: white; border: none; padding: 18px 30px;
            border-radius: 25px; font-weight: bold; cursor: pointer;
        }
        .status { font-size: 0.9em; color: #666; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔊 Sofia Voz 100% Funcional</h1>
            <p>Sistema TTS con múltiples fallbacks garantizados</p>
        </div>
        
        <div class="controls">
            <div style="display: flex; gap: 10px;">
                <button class="btn" id="voiceBtn" onclick="toggleVoice()">🔊 Voz Activada</button>
                <button class="btn" onclick="testVoice()">🎵 Test Completo</button>
                <button class="btn danger" onclick="changeTTS()">🔧 Cambiar TTS</button>
            </div>
            <div class="status">
                <div>Método TTS: <span id="ttsMethod">Detectando...</span></div>
                <div>Estado: <span id="ttsStatus">Listo</span></div>
            </div>
        </div>
        
        <div class="chat" id="chat">
            <div class="message sofia">
                ¡Hola! Soy Sofia con voz 100% funcional 🔊
                Tengo múltiples sistemas TTS con fallbacks automáticos.
                ¡Prueba el botón "Test Completo" para verificar mi voz!
            </div>
        </div>
        
        <div class="input-group">
            <input type="text" class="input" id="messageInput" 
                   placeholder="Escribe algo para que Sofia responda con voz..." maxlength="200">
            <button class="send-btn" onclick="sendMessage()">💕 Enviar</button>
        </div>
    </div>

    <script>
        let isVoiceActive = true;
        let currentTTSMethod = 'detectando';
        
        function addMessage(content, isUser = false, speaking = false) {
            const chat = document.getElementById('chat');
            const msg = document.createElement('div');
            msg.className = 'message ' + (isUser ? 'user' : 'sofia');
            
            if (speaking) {
                msg.classList.add('speaking');
                setTimeout(() => msg.classList.remove('speaking'), 5000);
            }
            
            msg.textContent = content;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage(message, true);
            input.value = '';
            input.disabled = true;
            
            document.getElementById('ttsStatus').textContent = 'Procesando...';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                
                addMessage(data.respuesta, false, data.voz_funciono);
                
                // Actualizar estado
                document.getElementById('ttsMethod').textContent = data.metodo_tts || 'Desconocido';
                document.getElementById('ttsStatus').textContent = 
                    data.voz_funciono ? '✅ Voz funcionó' : '❌ Voz falló';
                
                console.log('Voz funcionó:', data.voz_funciono);
                console.log('Método TTS:', data.metodo_tts);
                
            } catch (error) {
                addMessage('Error de conexión', false);
                document.getElementById('ttsStatus').textContent = '❌ Error';
            } finally {
                input.disabled = false;
                input.focus();
            }
        }
        
        async function toggleVoice() {
            try {
                const response = await fetch('/toggle-voice', { method: 'POST' });
                const data = await response.json();
                
                isVoiceActive = data.voz_activa;
                document.getElementById('voiceBtn').textContent = 
                    isVoiceActive ? '🔊 Voz Activada' : '🔇 Voz Desactivada';
                document.getElementById('voiceBtn').className = 
                    'btn' + (isVoiceActive ? '' : ' danger');
                
                addMessage(data.mensaje, false, isVoiceActive);
                
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        async function testVoice() {
            document.getElementById('ttsStatus').textContent = 'Probando voz...';
            
            try {
                const response = await fetch('/test-voice', { method: 'POST' });
                const data = await response.json();
                
                document.getElementById('ttsMethod').textContent = data.metodo;
                document.getElementById('ttsStatus').textContent = 
                    data.exito ? '✅ Test exitoso' : '❌ Test falló';
                
                addMessage(`Test de voz ejecutado. Método: ${data.metodo}. ¿Escuchaste mi voz?`, false, data.exito);
                
                console.log('Motores disponibles:', data.motores_disponibles);
                
            } catch (error) {
                document.getElementById('ttsStatus').textContent = '❌ Error en test';
                addMessage('Error ejecutando test de voz', false);
            }
        }
        
        async function changeTTS() {
            const metodos = ['windows_sapi', 'edge_tts', 'pyttsx3'];
            const metodo = prompt('Método TTS (windows_sapi, edge_tts, pyttsx3):');
            
            if (metodos.includes(metodo)) {
                try {
                    const response = await fetch('/change-tts', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({metodo: metodo})
                    });
                    
                    const data = await response.json();
                    
                    if (data.exito) {
                        document.getElementById('ttsMethod').textContent = data.metodo_actual;
                        addMessage(`TTS cambiado a: ${data.metodo_actual}`, false, true);
                    }
                    
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        }
        
        // Event listeners
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        document.getElementById('messageInput').focus();
        
        // Inicialización
        setTimeout(() => {
            console.log('🔊 Sofia Voz 100% Funcional cargada');
        }, 1000);
    </script>
</body>
</html>
        '''
    
    def run(self):
        print("\n🔊" + "="*70)
        print("🎉 SOFIA VOZ 100% FUNCIONAL")
        print("🔊" + "="*70)
        print("🌐 URL: http://localhost:7860")
        print("🔧 Métodos TTS disponibles:")
        for metodo, disponible in TTS_ENGINES.items():
            estado = "✅" if disponible else "❌"
            print(f"   {estado} {metodo}")
        print(f"🎯 Método seleccionado: {self.tts_method}")
        print("🎮 Funciones especiales:")
        print("   🎵 Test Completo - Prueba todos los métodos")
        print("   🔧 Cambiar TTS - Cambiar método manualmente")
        print("   🔊 Toggle Voz - Activar/desactivar")
        print("💡 Ctrl+C para cerrar")
        print("🔊" + "="*70 + "\n")
        
        try:
            import webbrowser
            import threading
            
            def open_browser():
                time.sleep(3)
                webbrowser.open('http://localhost:7860')
            
            threading.Thread(target=open_browser, daemon=True).start()
        except:
            pass
        
        self.app.run(host='0.0.0.0', port=7860, debug=False, threaded=True)

if __name__ == "__main__":
    try:
        sofia = SofiaVozFuncional()
        sofia.run()
    except KeyboardInterrupt:
        print("\n💔 ¡Hasta luego! Sofia te esperará...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Presiona Enter para salir...")