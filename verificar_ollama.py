#!/usr/bin/env python3
"""
VERIFICADOR DE OLLAMA Y LLAMA 3
Comprueba si todo está listo para Sofia inteligente
"""

import requests
import json
import os
import sys

def verificar_ollama():
    """Verifica si Ollama está funcionando"""
    print("🔍 Verificando Ollama...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama está funcionando!")
            return True
        else:
            print("❌ Ollama responde pero con error")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama NO está funcionando")
        print("💡 Solución: Ejecuta 'ollama serve' en otra terminal")
        return False
    except Exception as e:
        print(f"❌ Error conectando a Ollama: {e}")
        return False

def listar_modelos():
    """Lista modelos disponibles en Ollama"""
    print("\n📋 Verificando modelos disponibles...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            data = response.json()
            modelos = data.get('models', [])
            
            if modelos:
                print("✅ Modelos encontrados:")
                for modelo in modelos:
                    nombre = modelo.get('name', 'Desconocido')
                    tamaño = modelo.get('size', 0) / (1024**3)  # GB
                    print(f"   📦 {nombre} ({tamaño:.2f} GB)")
                return [m['name'] for m in modelos]
            else:
                print("❌ No hay modelos instalados")
                return []
        else:
            print("❌ Error obteniendo modelos")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def probar_llama3():
    """Prueba Llama 3 con un mensaje simple"""
    print("\n🧪 Probando Llama 3...")
    
    # Buscar modelo Llama disponible
    modelos = listar_modelos()
    if not modelos:
        print("❌ No hay modelos para probar")
        return False
    
    # Seleccionar modelo (preferir llama3)
    modelo_a_usar = None
    for modelo in modelos:
        if 'llama' in modelo.lower():
            modelo_a_usar = modelo
            break
    
    if not modelo_a_usar:
        modelo_a_usar = modelos[0]  # Usar el primero disponible
    
    print(f"🎯 Usando modelo: {modelo_a_usar}")
    
    try:
        payload = {
            "model": modelo_a_usar,
            "prompt": "Hola, soy Sofia tu novia virtual. Responde de manera cariñosa en español.",
            "stream": False,
            "options": {
                "temperature": 0.8,
                "max_tokens": 100
            }
        }
        
        print("⏳ Enviando mensaje de prueba...")
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            resultado = response.json()
            respuesta = resultado.get('response', '').strip()
            
            if respuesta:
                print("✅ ¡Llama 3 funciona perfectamente!")
                print(f"💬 Respuesta de prueba: {respuesta}")
                return True
            else:
                print("❌ Llama 3 respondió vacío")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Timeout - Llama 3 tardó mucho en responder")
        return False
    except Exception as e:
        print(f"❌ Error probando Llama 3: {e}")
        return False

def instalar_llama3():
    """Guía para instalar Llama 3 si no está"""
    print("\n📥 CÓMO INSTALAR LLAMA 3:")
    print("1. Abre otra terminal/CMD")
    print("2. Ejecuta: ollama pull llama3.2")
    print("3. Espera a que descargue (puede tardar varios minutos)")
    print("4. Ejecuta este script de nuevo")
    print("\n💡 Modelos recomendados:")
    print("   - llama3.2 (Más rápido, 4.7GB)")
    print("   - llama3.2:8b (Más inteligente, 4.7GB)")
    print("   - llama3.1:8b (Alternativa)")

def main():
    print("🌹 VERIFICADOR DE SOFIA INTELIGENTE")
    print("=" * 40)
    
    # Paso 1: Verificar Ollama
    if not verificar_ollama():
        print("\n❌ PROBLEMA: Ollama no está funcionando")
        print("💡 SOLUCIÓN:")
        print("1. Abre CMD/Terminal como administrador")
        print("2. Ejecuta: ollama serve")
        print("3. Deja esa ventana abierta")
        print("4. Ejecuta este script de nuevo")
        input("\nPresiona Enter para salir...")
        return
    
    # Paso 2: Verificar modelos
    modelos = listar_modelos()
    if not modelos:
        print("\n❌ PROBLEMA: No hay modelos instalados")
        instalar_llama3()
        input("\nPresiona Enter para salir...")
        return
    
    # Paso 3: Probar Llama 3
    if probar_llama3():
        print("\n🎉 ¡TODO PERFECTO!")
        print("✅ Ollama funcionando")
        print("✅ Modelos disponibles")
        print("✅ Llama 3 responde correctamente")
        print("\n🚀 ¡Sofia está lista para ser súper inteligente!")
        print("💡 Próximo paso: Ejecutar sofia_inteligente.py")
    else:
        print("\n❌ PROBLEMA: Llama 3 no responde bien")
        print("💡 Posibles soluciones:")
        print("1. Reinstalar modelo: ollama pull llama3.2")
        print("2. Reiniciar Ollama")
        print("3. Verificar que no hay otros programas usando el puerto 11434")
    
    input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    main()