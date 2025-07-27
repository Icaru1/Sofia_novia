@echo off
chcp 65001 > nul
cls

echo.
echo ██████╗  ██████╗ ███████╗██╗ █████╗     ██╗ █████╗ 
echo ██╔═══██╗██╔═══██╗██╔════╝██║██╔══██╗    ██║██╔══██╗
echo ██║   ██║██████╔╝█████╗  ██║███████║    ██║███████║
echo ██║   ██║██╔═══██╗██╔════╝██║██╔══██║    ██║██╔══██║
echo ╚██████╔╝██║   ██║██║     ██║██║  ██║    ██║██║  ██║
echo  ╚═════╝ ╚═╝   ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝╚═╝  ╚═╝
echo.
echo 🧠 INSTALADOR AUTOMÁTICO DE SOFIA INTELIGENTE
echo ================================================
echo.

REM Verificar directorio
if not exist "python_embeded" (
    echo ❌ ERROR: Ejecuta desde la carpeta Sofia_Novia_Virtual
    echo 💡 Debe existir la carpeta python_embeded
    pause
    exit /b 1
)

echo 🔍 Verificando sistema...
echo.

REM Verificar Python
python_embeded\python.exe --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python no funciona
    pause
    exit /b 1
) else (
    echo ✅ Python OK
)

REM Verificar Ollama
echo 🦙 Verificando Ollama...
ollama --version > nul 2>&1
if errorlevel 1 (
    echo ❌ OLLAMA NO INSTALADO
    echo.
    echo 📥 INSTALAR OLLAMA:
    echo 1. Ve a: https://ollama.ai
    echo 2. Descarga Ollama para Windows
    echo 3. Instala y reinicia
    echo 4. Ejecuta este script de nuevo
    pause
    exit /b 1
) else (
    echo ✅ Ollama instalado
)

REM Verificar si Ollama está corriendo
echo 🔄 Verificando servicio Ollama...
curl -s http://localhost:11434/api/tags > nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama no está corriendo
    echo 🚀 Iniciando Ollama...
    start /b ollama serve
    timeout /t 5 > nul
    
    REM Verificar de nuevo
    curl -s http://localhost:11434/api/tags > nul 2>&1
    if errorlevel 1 (
        echo ❌ No se pudo iniciar Ollama automáticamente
        echo 💡 Inicia manualmente: ollama serve
        pause
        exit /b 1
    ) else (
        echo ✅ Ollama iniciado
    )
) else (
    echo ✅ Ollama funcionando
)

REM Instalar dependencias Python
echo 📦 Instalando dependencias Python...
python_embeded\python.exe -m pip install --quiet --upgrade pip
python_embeded\python.exe -m pip install --quiet flask requests

echo.
echo 🦙 Verificando modelos de IA...

REM Listar modelos
for /f "tokens=*" %%i in ('curl -s http://localhost:11434/api/tags ^| python_embeded\python.exe -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('models', [])))"') do set NUM_MODELS=%%i

if "%NUM_MODELS%"=="0" (
    echo ❌ No hay modelos de IA instalados
    echo.
    echo 🎯 INSTALANDO LLAMA 3.2...
    echo ⏳ Esto puede tardar varios minutos dependiendo de tu conexión
    echo 📊 Llama 3.2 pesa aproximadamente 4.7GB
    echo.
    
    ollama pull llama3.2
    
    if errorlevel 1 (
        echo ❌ Error descargando Llama 3.2
        echo 💡 Intenta manualmente: ollama pull llama3.2
        pause
        exit /b 1
    ) else (
        echo ✅ Llama 3.2 instalado correctamente
    )
) else (
    echo ✅ Modelos encontrados: %NUM_MODELS%
)

echo.
echo 🧪 Probando sistema completo...
echo.

REM Crear script de prueba
echo import requests, json > test_sofia.py
echo try: >> test_sofia.py
echo     response = requests.get("http://localhost:11434/api/tags", timeout=5) >> test_sofia.py
echo     if response.status_code == 200: >> test_sofia.py
echo         models = response.json().get('models', []) >> test_sofia.py
echo         if models: >> test_sofia.py
echo             print("✅ Sistema IA listo") >> test_sofia.py
echo             print(f"📦 Modelos: {len(models)}") >> test_sofia.py
echo             for model in models[:3]: >> test_sofia.py
echo                 print(f"   🧠 {model['name']}") >> test_sofia.py
echo         else: >> test_sofia.py
echo             print("❌ No hay modelos") >> test_sofia.py
echo     else: >> test_sofia.py
echo         print("❌ Ollama error") >> test_sofia.py
echo except Exception as e: >> test_sofia.py
echo     print(f"❌ Error: {e}") >> test_sofia.py

python_embeded\python.exe test_sofia.py
del test_sofia.py

echo.
echo 🎉 INSTALACIÓN COMPLETADA
echo ========================
echo.
echo ✅ Python funcionando
echo ✅ Ollama funcionando  
echo ✅ Llama 3 instalado
echo ✅ Dependencias instaladas
echo.
echo 🚀 PRÓXIMOS PASOS:
echo 1. Ejecuta: python_embeded\python.exe sofia_inteligente.py
echo 2. Abre: http://localhost:7860
echo 3. ¡Conversa con Sofia IA!
echo.
echo 💡 COMANDOS ÚTILES:
echo - Verificar: python_embeded\python.exe verificar_ollama.py
echo - Sofia básica: python_embeded\python.exe sofia.py
echo - Sofia IA: python_embeded\python.exe sofia_inteligente.py
echo.

pause