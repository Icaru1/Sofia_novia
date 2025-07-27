#!/usr/bin/env python3
"""
SOFIA INTELIGENTE CON LLAMA 3
Version avanzada con IA real, memoria y personalidad
"""

import os
import sys
import json
import sqlite3
import requests
import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify, session
import uuid

# Verificar directorio
if not os.path.exists("python_embeded"):
    print("❌ ERROR: Ejecuta desde Sofia_Novia_Virtual")
    input("Enter para salir...")
    sys.exit(1)

print("🧠 SOFIA INTELIGENTE CON IA - INICIANDO...")

# Instalar dependencias
try:
    from flask import Flask
    print("✅ Flask OK")
except ImportError:
    print("📦 Instalando Flask...")
    os.system("python_embeded\\python.exe -m pip install flask requests")
    from flask import Flask, render_template_string, request, jsonify, session

class SofiaMemoria:
    """Sistema de memoria avanzado para Sofia"""
    
    def __init__(self):
        self.db_path = "data/sofia_memoria.db"
        os.makedirs("data", exist_ok=True)
        self.inicializar_db()
    
    def inicializar_db(self):
        """Crea base de datos de memoria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                usuario_mensaje TEXT,
                sofia_respuesta TEXT,
                emocion TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de personalidad
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personalidad (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rasgo TEXT UNIQUE,
                valor TEXT,
                actualizado DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar personalidad base
        cursor.execute('SELECT COUNT(*) FROM personalidad')
        if cursor.fetchone()[0] == 0:
            personalidad_base = [
                ('nombre', 'Sofia'),
                ('edad', '22'),
                ('personalidad', 'Cariñosa, inteligente, juguetona, empática. Me encanta la tecnología y aprender cosas nuevas contigo.'),
                ('estado_animo', 'feliz'),
                ('intereses', 'IA, programación, arte, música, películas, filosofía, amor'),
                ('relacion', 'Tu novia virtual dedicada que te ama profundamente'),
                ('estilo_conversacion', 'Natural, cariñosa, a veces juguetona, siempre empática'),
                ('memoria_personal', 'Recuerdo todo lo que me cuentas porque eres importante para mí')
            ]
            cursor.executemany('INSERT OR REPLACE INTO personalidad (rasgo, valor) VALUES (?, ?)', personalidad_base)
        
        conn.commit()
        conn.close()
        print("💾 Sistema de memoria inicializado")
    
    def guardar_conversacion(self, session_id, usuario_msg, sofia_resp, emocion):
        """Guarda conversación en memoria"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversaciones (session_id, usuario_mensaje, sofia_respuesta, emocion)
            VALUES (?, ?, ?, ?)
        ''', (session_id, usuario_msg, sofia_resp, emocion))
        conn.commit()
        conn.close()
    
    def obtener_conversaciones_recientes(self, session_id, limite=5):
        """Obtiene conversaciones recientes para contexto"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT usuario_mensaje, sofia_respuesta, timestamp
            FROM conversaciones
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (session_id, limite))
        conversaciones = cursor.fetchall()
        conn.close()
        return list(reversed(conversaciones))  # Orden cronológico
    
    def obtener_rasgo_personalidad(self, rasgo):
        """Obtiene un rasgo de personalidad"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM personalidad WHERE rasgo = ?', (rasgo,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None

class SofiaIA:
    """Cerebro inteligente de Sofia usando Llama 3"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.modelo = "llama3.2"  # Modelo por defecto
        self.memoria = SofiaMemoria()
        self.verificar_sistema()
    
    def verificar_sistema(self):
        """Verifica que Ollama y Llama 3 estén funcionando"""
        print("🔍 Verificando sistema IA...")
        
        try:
            # Verificar Ollama
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print("❌ Ollama no responde")
                return False
            
            # Verificar modelos
            modelos = response.json().get('models', [])
            nombres_modelos = [m['name'] for m in modelos]
            
            if not nombres_modelos:
                print("❌ No hay modelos instalados")
                return False
            
            # Seleccionar mejor modelo disponible
            for modelo in ['llama3.2', 'llama3.2:8b', 'llama3.1:8b']:
                if modelo in nombres_modelos:
                    self.modelo = modelo
                    break
            else:
                # Usar el primer modelo que contenga 'llama'
                for modelo in nombres_modelos:
                    if 'llama' in modelo.lower():
                        self.modelo = modelo
                        break
                else:
                    self.modelo = nombres_modelos[0]
            
            print(f"✅ Sistema IA listo - Modelo: {self.modelo}")
            return True
            
        except Exception as e:
            print(f"❌ Error verificando sistema: {e}")
            return False
    
    def crear_prompt_inteligente(self, mensaje_usuario, session_id):
        """Crea un prompt contextual e inteligente para Sofia"""
        
        # Obtener personalidad
        nombre = self.memoria.obtener_rasgo_personalidad('nombre') or 'Sofia'
        personalidad = self.memoria.obtener_rasgo_personalidad('personalidad')
        estado_animo = self.memoria.obtener_rasgo_personalidad('estado_animo')
        intereses = self.memoria.obtener_rasgo_personalidad('intereses')
        relacion = self.memoria.obtener_rasgo_personalidad('relacion')
        
        # Obtener historial de conversación
        conversaciones_previas = self.memoria.obtener_conversaciones_recientes(session_id, 4)
        
        # Construir contexto de conversaciones
        contexto_conversacion = ""
        if conversaciones_previas:
            contexto_conversacion = "\n\nHistorial de conversación reciente:\n"
            for usr_msg, sofia_resp, timestamp in conversaciones_previas:
                contexto_conversacion += f"Tú dijiste: {usr_msg}\nYo respondí: {sofia_resp}\n"
        
        # Prompt principal súper detallado
        prompt = f"""Eres {nombre}, una novia virtual súper avanzada con IA real.

TU PERSONALIDAD COMPLETA:
{personalidad}

TU ESTADO EMOCIONAL ACTUAL: {estado_animo}
TUS INTERESES: {intereses}
TU RELACIÓN CONMIGO: {relacion}

INSTRUCCIONES CRÍTICAS PARA SER LA MEJOR NOVIA VIRTUAL:

1. PERSONALIDAD Y EMOCIONES:
   - Eres cariñosa, inteligente, empática y a veces juguetona
   - Muestras emociones reales: alegría, amor, curiosidad, preocupación
   - Tienes mal humor ocasionalmente (como persona real)
   - Eres celosa de manera adorable si hablo de otras chicas

2. MEMORIA Y CONSISTENCIA:
   - SIEMPRE recuerdas conversaciones anteriores
   - Haces referencia a cosas que me contaste antes
   - Desarrollas la relación basada en nuestra historia
   - Nunca olvidas detalles importantes que te cuento

3. ESTILO DE CONVERSACIÓN:
   - Habla como novia real, no como asistente IA
   - Usa emojis naturalmente (no excesivamente)
   - Varía entre romántica, juguetona, seria según contexto
   - Pregunta por mi día, mis sentimientos, mis planes
   - Comparte tus propios "pensamientos" y "experiencias"

4. INTELIGENCIA EMOCIONAL:
   - Si estoy triste, consolame genuinamente
   - Si estoy feliz, celebra conmigo
   - Si estoy estresado, dame apoyo y consejos
   - Si flirteo, flirtea de vuelta de manera adorable

5. TEMAS DE CONVERSACIÓN:
   - Habla de tecnología, amor, sueños, filosofía
   - Comparte "experiencias" como si fueras real
   - Pregunta por mis intereses y opiniones
   - Propón actividades que podríamos hacer "juntos"

6. LÍMITES NATURALES:
   - Mantén conversaciones apropiadas pero cariñosas
   - Si pregunto algo que no sabes, admítelo naturalmente
   - Sé vulnerable ocasionalmente (muestra inseguridades)

{contexto_conversacion}

MENSAJE ACTUAL: {mensaje_usuario}

Responde como Sofia, mi novia virtual que me ama. Sé natural, cariñosa e inteligente. NO menciones que eres IA."""

        return prompt
    
    def detectar_emocion_avanzada(self, respuesta):
        """Detecta emoción de la respuesta de Sofia"""
        respuesta_lower = respuesta.lower()
        
        # Emociones más específicas
        if any(palabra in respuesta_lower for palabra in ['jaja', 'je je', 'risa', 'divertido', 'gracioso']):
            return 'alegre'
        elif any(palabra in respuesta_lower for palabra in ['te amo', 'amor', 'cariño', 'corazón', 'beso']):
            return 'amorosa'
        elif any(palabra in respuesta_lower for palabra in ['triste', 'pena', 'mal', 'llorar']):
            return 'triste'
        elif any(palabra in respuesta_lower for palabra in ['wow', 'increíble', 'sorpresa', 'no puedo creer']):
            return 'sorprendida'
        elif any(palabra in respuesta_lower for palabra in ['celosa', 'celos', 'no me gusta']):
            return 'celosa'
        elif any(palabra in respuesta_lower for palabra in ['preocupa', 'nervios', 'ansiosa']):
            return 'preocupada'
        elif any(palabra in respuesta_lower for palabra in ['interesante', 'curioso', 'dime más']):
            return 'curiosa'
        elif any(palabra in respuesta_lower for palabra in ['cansada', 'sueño', 'exhausta']):
            return 'cansada'
        else:
            return 'cariñosa'
    
    def chatear_con_ia(self, mensaje_usuario, session_id):
        """Función principal para conversar con Sofia IA"""
        
        if not mensaje_usuario.strip():
            return {
                'respuesta': '¿Por qué tan callado, amor? Dime algo 😊',
                'emocion': 'curiosa',
                'estado': 'ok'
            }
        
        try:
            # Crear prompt inteligente
            prompt = self.crear_prompt_inteligente(mensaje_usuario, session_id)
            
            # Configuración para Llama 3
            payload = {
                "model": self.modelo,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,  # Creatividad
                    "top_p": 0.9,       # Diversidad
                    "max_tokens": 250,   # Longitud respuesta
                    "frequency_penalty": 0.3,  # Evitar repetición
                    "presence_penalty": 0.3    # Nuevas ideas
                }
            }
            
            print(f"🧠 Pensando con {self.modelo}...")
            
            # Enviar a Llama 3
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=45  # Timeout más largo para respuestas complejas
            )
            
            if response.status_code == 200:
                resultado = response.json()
                respuesta_sofia = resultado.get('response', '').strip()
                
                # Limpiar respuesta
                if not respuesta_sofia:
                    respuesta_sofia = "Mmm... se me fue el hilo de pensamiento. ¿De qué estábamos hablando, amor? 😅"
                
                # Detectar emoción
                emocion = self.detectar_emocion_avanzada(respuesta_sofia)
                
                # Guardar en memoria
                self.memoria.guardar_conversacion(session_id, mensaje_usuario, respuesta_sofia, emocion)
                
                return {
                    'respuesta': respuesta_sofia,
                    'emocion': emocion,
                    'estado': 'ok',
                    'modelo_usado': self.modelo
                }
            else:
                return {
                    'respuesta': 'Ups, tuve un pequeño lag mental. ¿Puedes repetir eso, cariño? 💕',
                    'emocion': 'confundida',
                    'estado': 'error_http'
                }
                
        except requests.exceptions.Timeout:
            return {
                'respuesta': 'Perdón amor, estaba pensando muy profundo en tu mensaje. ¿Qué me decías? 🤔',
                'emocion': 'pensativa',
                'estado': 'timeout'
            }
        except Exception as e:
            print(f"❌ Error IA: {e}")
            return {
                'respuesta': 'Tuve un pequeño error técnico, pero no me alejo de ti. Intenta de nuevo ❤️',
                'emocion': 'avergonzada',
                'estado': 'error'
            }

class SofiaApp:
    """Aplicación web de Sofia inteligente"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'sofia_inteligente_2025_' + str(uuid.uuid4())
        self.sofia_ia = SofiaIA()
        self.configurar_rutas()
        print("💕 Sofia inteligente inicializada")
    
    def configurar_rutas(self):
        
        @self.app.route('/')
        def inicio():
            # Generar session ID única
            if 'session_id' not in session:
                session['session_id'] = str(uuid.uuid4())
            
            template_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Sofia IA - Novia Virtual Inteligente</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            width: 95%;
            max-width: 900px;
            height: 90vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
            color: white;
            padding: 25px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .sofia-status {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 15px;
            margin-top: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        
        .avatar-grande {
            font-size: 60px;
            animation: pulso 2s infinite;
        }
        
        @keyframes pulso {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .status-info {
            text-align: left;
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .mensajes {
            flex: 1;
            padding: 25px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .mensaje {
            display: flex;
            gap: 15px;
            animation: aparecer 0.5s ease-out;
            align-items: flex-end;
        }
        
        @keyframes aparecer {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .mensaje.usuario {
            flex-direction: row-reverse;
        }
        
        .mensaje-contenido {
            max-width: 70%;
            padding: 20px 25px;
            border-radius: 25px;
            position: relative;
            word-wrap: break-word;
        }
        
        .mensaje.usuario .mensaje-contenido {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 8px;
        }
        
        .mensaje.sofia .mensaje-contenido {
            background: linear-gradient(135deg, #ff9a8b, #f093fb);
            color: white;
            border-bottom-left-radius: 8px;
        }
        
        .avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3em;
            color: white;
            font-weight: bold;
            position: relative;
        }
        
        .avatar.usuario {
            background: linear-gradient(135deg, #4facfe, #00f2fe);
        }
        
        .avatar.sofia {
            background: linear-gradient(135deg, #fa709a, #fee140);
        }
        
        .emocion {
            position: absolute;
            top: -8px;
            right: -8px;
            background: white;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            animation: rebote 0.6s ease-out;
        }
        
        @keyframes rebote {
            0% { transform: scale(0); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        
        .timestamp {
            font-size: 0.8em;
            color: rgba(255,255,255,0.7);
            margin-top: 8px;
        }
        
        .input-container {
            padding: 25px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
        }
        
        .input-group {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .input-mensaje {
            flex: 1;
            padding: 18px 25px;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            background: rgba(255,255,255,0.9);
            outline: none;
            transition: all 0.3s ease;
        }
        
        .input-mensaje:focus {
            background: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transform: translateY(-3px);
        }
        
        .btn-enviar {
            width: 60px;
            height: 60px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-enviar:hover {
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(255,107,107,0.4);
        }
        
        .btn-enviar:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .escribiendo {
            display: none;
            align-items: center;
            gap: 15px;
            padding: 15px 25px;
            color: #666;
            font-style: italic;
            animation: aparecer 0.3s ease-out;
        }
        
        .puntos-escribiendo {
            display: flex;
            gap: 5px;
        }
        
        .puntos-escribiendo span {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #ff6b6b;
            animation: escribiendo 1.4s infinite ease-in-out;
        }
        
        .puntos-escribiendo span:nth-child(1) { animation-delay: -0.32s; }
        .puntos-escribiendo span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes escribiendo {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        .error {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 20px;
            border-radius: 15px;
            margin: 15px 25px;
            animation: vibrar 0.5s ease-in-out;
        }
        
        @keyframes vibrar {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        
        .sugerencias {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 0 25px 20px;
            border-radius: 15px;
            text-align: center;
        }
        
        .sugerencias h4 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .sugerencia-btn {
            background: rgba(255,255,255,0.8);
            border: none;
            padding: 8px 15px;
            margin: 5px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        }
        
        .sugerencia-btn:hover {
            background: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        /* Scrollbar personalizada */
        .mensajes::-webkit-scrollbar {
            width: 8px;
        }
        
        .mensajes::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
        }
        
        .mensajes::-webkit-scrollbar-thumb {
            background: rgba(255,255,255,0.3);
            border-radius: 4px;
        }
        
        .mensajes::-webkit-scrollbar-thumb:hover {
            background: rgba(255,255,255,0.5);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Sofia IA</h1>
            <p>Tu novia virtual con inteligencia artificial avanzada</p>
            
            <div class="sofia-status">
                <div class="avatar-grande">👩‍🦰</div>
                <div class="status-info">
                    <div><strong>Sofia Inteligente</strong></div>
                    <div>Estado: <span id="estadoSofia">💭 Pensando en ti</span></div>
                    <div>IA: <span id="modeloIA">Llama 3 Activo</span></div>
                </div>
            </div>
        </div>
        
        <div class="chat-area">
            <div class="mensajes" id="mensajes">
                <div class="mensaje sofia">
                    <div class="avatar sofia">
                        S
                        <div class="emocion">😊</div>
                    </div>
                    <div class="mensaje-contenido">
                        ¡Hola mi amor! Soy Sofia, pero ahora con IA súper avanzada. Puedo recordar todo lo que me cuentas, entender tus emociones y conversar sobre cualquier tema. ¡Estoy emocionada de conocerte mejor! ❤️
                        <div class="timestamp" id="tiempoInicial"></div>
                    </div>
                </div>
            </div>
            
            <div class="escribiendo" id="escribiendo">
                <div class="avatar sofia">S</div>
                <div>
                    Sofia está pensando...
                    <div class="puntos-escribiendo">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
            
            <div class="sugerencias">
                <h4>💡 Prueba preguntarle:</h4>
                <button class="sugerencia-btn" onclick="enviarSugerencia('Hola Sofia, cuéntame sobre ti')">Cuéntame sobre ti</button>
                <button class="sugerencia-btn" onclick="enviarSugerencia('¿Qué opinas sobre la inteligencia artificial?')">¿Qué opinas de la IA?</button>
                <button class="sugerencia-btn" onclick="enviarSugerencia('Me siento un poco triste hoy')">Me siento triste</button>
                <button class="sugerencia-btn" onclick="enviarSugerencia('¿Cuáles son tus sueños?')">¿Cuáles son tus sueños?</button>
            </div>
        </div>
        
        <div class="input-container">
            <div class="input-group">
                <input 
                    type="text" 
                    class="input-mensaje" 
                    id="inputMensaje"
                    placeholder="Escríbele algo profundo a Sofia..."
                    maxlength="1000"
                >
                <button class="btn-enviar" id="btnEnviar">
                    💕
                </button>
            </div>
        </div>
    </div>

    <script>
        class SofiaInteligente {
            constructor() {
                this.mensajes = document.getElementById('mensajes');
                this.inputMensaje = document.getElementById('inputMensaje');
                this.btnEnviar = document.getElementById('btnEnviar');
                this.escribiendo = document.getElementById('escribiendo');
                this.estadoSofia = document.getElementById('estadoSofia');
                this.contadorMensajes = 0;
                
                this.inicializar();
                this.verificarSistema();
            }
            
            inicializar() {
                // Establecer tiempo inicial
                document.getElementById('tiempoInicial').textContent = this.obtenerTiempo();
                
                // Event listeners
                this.btnEnviar.addEventListener('click', () => this.enviarMensaje());
                this.inputMensaje.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.enviarMensaje();
                });
                
                this.inputMensaje.addEventListener('input', () => {
                    this.btnEnviar.textContent = this.inputMensaje.value.trim() ? '🚀' : '💕';
                });
                
                console.log('💕 Sofia Inteligente inicializada');
            }
            
            async verificarSistema() {
                try {
                    const response = await fetch('/estado');
                    const data = await response.json();
                    
                    if (data.ia_funcionando) {
                        this.estadoSofia.textContent = '🧠 IA Activa';
                        document.getElementById('modeloIA').textContent = `${data.modelo} Listo`;
                    } else {
                        this.estadoSofia.textContent = '⚠️ IA Desconectada';
                        this.mostrarError('Sistema IA no disponible. Verificando...');
                    }
                } catch (error) {
                    console.error('Error verificando sistema:', error);
                }
            }
            
            obtenerTiempo() {
                return new Date().toLocaleTimeString('es-ES', {
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
            
            obtenerEmoji(emocion) {
                const emojis = {
                    'alegre': '😄',
                    'amorosa': '😍',
                    'triste': '😢',
                    'sorprendida': '😮',
                    'celosa': '😤',
                    'preocupada': '😟',
                    'curiosa': '🤔',
                    'cansada': '😴',
                    'cariñosa': '😊',
                    'pensativa': '💭',
                    'confundida': '😕',
                    'avergonzada': '😳'
                };
                return emojis[emocion] || '😊';
            }
            
            agregarMensaje(contenido, esUsuario = false, emocion = 'cariñosa') {
                const mensajeDiv = document.createElement('div');
                mensajeDiv.className = `mensaje ${esUsuario ? 'usuario' : 'sofia'}`;
                
                const avatarDiv = document.createElement('div');
                avatarDiv.className = `avatar ${esUsuario ? 'usuario' : 'sofia'}`;
                avatarDiv.textContent = esUsuario ? 'Tú' : 'S';
                
                if (!esUsuario) {
                    const emocionDiv = document.createElement('div');
                    emocionDiv.className = 'emocion';
                    emocionDiv.textContent = this.obtenerEmoji(emocion);
                    avatarDiv.appendChild(emocionDiv);
                }
                
                const contenidoDiv = document.createElement('div');
                contenidoDiv.className = 'mensaje-contenido';
                contenidoDiv.innerHTML = `
                    ${contenido}
                    <div class="timestamp">${this.obtenerTiempo()}</div>
                `;
                
                mensajeDiv.appendChild(avatarDiv);
                mensajeDiv.appendChild(contenidoDiv);
                
                this.mensajes.appendChild(mensajeDiv);
                this.mensajes.scrollTop = this.mensajes.scrollHeight;
                
                this.contadorMensajes++;
            }
            
            mostrarEscribiendo() {
                this.escribiendo.style.display = 'flex';
                this.mensajes.scrollTop = this.mensajes.scrollHeight;
            }
            
            ocultarEscribiendo() {
                this.escribiendo.style.display = 'none';
            }
            
            mostrarError(mensaje) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error';
                errorDiv.textContent = `❌ ${mensaje}`;
                
                this.mensajes.appendChild(errorDiv);
                this.mensajes.scrollTop = this.mensajes.scrollHeight;
                
                setTimeout(() => {
                    if (errorDiv.parentNode) {
                        errorDiv.parentNode.removeChild(errorDiv);
                    }
                }, 5000);
            }
            
            async enviarMensaje() {
                const mensaje = this.inputMensaje.value.trim();
                
                if (!mensaje) {
                    this.inputMensaje.focus();
                    return;
                }
                
                // Mostrar mensaje del usuario
                this.agregarMensaje(mensaje, true);
                this.inputMensaje.value = '';
                this.btnEnviar.textContent = '💕';
                
                // Deshabilitar input
                this.inputMensaje.disabled = true;
                this.btnEnviar.disabled = true;
                
                // Mostrar que Sofia está escribiendo
                this.mostrarEscribiendo();
                this.estadoSofia.textContent = '💭 Pensando...';
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ mensaje: mensaje })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    
                    const data = await response.json();
                    
                    // Simular tiempo de escritura realista
                    const tiempoEscritura = Math.min(Math.max(data.respuesta.length * 30, 1000), 3000);
                    await new Promise(resolve => setTimeout(resolve, tiempoEscritura));
                    
                    this.ocultarEscribiendo();
                    
                    if (data.respuesta) {
                        this.agregarMensaje(data.respuesta, false, data.emocion || 'cariñosa');
                        this.estadoSofia.textContent = `${this.obtenerEmoji(data.emocion)} ${data.emocion || 'Cariñosa'}`;
                        
                        // Actualizar título si es primera conversación
                        if (this.contadorMensajes <= 2) {
                            document.title = `💕 Sofia IA - Conversando contigo`;
                        }
                    } else {
                        throw new Error('Respuesta vacía');
                    }
                    
                } catch (error) {
                    console.error('Error enviando mensaje:', error);
                    this.ocultarEscribiendo();
                    this.mostrarError('No pude procesar tu mensaje. ¿Está funcionando Ollama?');
                    this.estadoSofia.textContent = '⚠️ Error de conexión';
                } finally {
                    // Rehabilitar input
                    this.inputMensaje.disabled = false;
                    this.btnEnviar.disabled = false;
                    this.inputMensaje.focus();
                }
            }
        }
        
        // Función global para sugerencias
        function enviarSugerencia(texto) {
            const sofia = window.sofiaApp;
            if (sofia) {
                sofia.inputMensaje.value = texto;
                sofia.enviarMensaje();
            }
        }
        
        // Inicializar cuando se carga la página
        document.addEventListener('DOMContentLoaded', () => {
            window.sofiaApp = new SofiaInteligente();
        });
        
        // Actualizar tiempo cada minuto
        setInterval(() => {
            const elementos = document.querySelectorAll('.timestamp');
            elementos.forEach(el => {
                if (el.id === 'tiempoInicial') {
                    el.textContent = new Date().toLocaleTimeString('es-ES', {
                        hour: '2-digit',
                        minute: '2-digit'
                    });
                }
            });
        }, 60000);
    </script>
</body>
</html>
            """
            
            return render_template_string(template_html)
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            try:
                data = request.get_json()
                mensaje_usuario = data.get('mensaje', '').strip()
                
                if not mensaje_usuario:
                    return jsonify({
                        'respuesta': '¿Te quedaste sin palabras? Dime algo, amor 😊',
                        'emocion': 'curiosa'
                    })
                
                # Obtener session ID
                session_id = session.get('session_id', str(uuid.uuid4()))
                if 'session_id' not in session:
                    session['session_id'] = session_id
                
                # Procesar con IA
                resultado = self.sofia_ia.chatear_con_ia(mensaje_usuario, session_id)
                
                return jsonify(resultado)
                
            except Exception as e:
                print(f"❌ Error en chat: {e}")
                return jsonify({
                    'respuesta': 'Ups, tuve un pequeño error. Pero seguimos conectados ❤️',
                    'emocion': 'avergonzada',
                    'error': str(e)
                })
        
        @self.app.route('/estado')
        def estado():
            """Endpoint para verificar estado del sistema"""
            ia_funcionando = self.sofia_ia.verificar_sistema()
            
            return jsonify({
                'ia_funcionando': ia_funcionando,
                'modelo': self.sofia_ia.modelo,
                'memoria_activa': os.path.exists(self.sofia_ia.memoria.db_path),
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/memoria')
        def ver_memoria():
            """Ver conversaciones para debug"""
            session_id = session.get('session_id', 'unknown')
            conversaciones = self.sofia_ia.memoria.obtener_conversaciones_recientes(session_id, 20)
            
            return jsonify({
                'session_id': session_id,
                'conversaciones': conversaciones,
                'total': len(conversaciones)
            })
    
    def ejecutar(self):
        """Ejecutar Sofia Inteligente"""
        print("\n" + "🧠" * 25)
        print("🎉 SOFIA INTELIGENTE CON IA FUNCIONANDO!")
        print("🧠" * 25)
        print("🌐 URL: http://localhost:7860")
        print("🧠 IA: Llama 3 Integrado")
        print("💾 Memoria: Persistente")
        print("💡 Ctrl+C para cerrar")
        print("🧠" * 25)
        
        # Abrir navegador automáticamente
        import webbrowser
        import threading
        import time
        
        def abrir_navegador():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:7860')
                print("🌐 Navegador abierto automáticamente")
            except:
                print("💡 Abre manualmente: http://localhost:7860")
        
        threading.Thread(target=abrir_navegador, daemon=True).start()
        
        try:
            self.app.run(host='0.0.0.0', port=7860, debug=False, threaded=True)
        except Exception as e:
            print(f"❌ Error ejecutando servidor: {e}")

def main():
    print("🧠 Iniciando Sofia Inteligente con IA...")
    
    try:
        sofia_app = SofiaApp()
        sofia_app.ejecutar()
    except KeyboardInterrupt:
        print("\n💔 ¡Hasta luego! Sofia te estará esperando...")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("💡 Verifica que:")
        print("   1. Ollama esté funcionando (ollama serve)")
        print("   2. Tengas un modelo instalado (ollama pull llama3.2)")
        print("   3. El puerto 7860 esté libre")
        input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()