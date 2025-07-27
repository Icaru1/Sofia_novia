@echo off
echo 🦙 INSTALANDO LLAMA 3 PARA SOFIA
echo ================================

echo.
echo 📋 Información:
echo - Llama 3 es el cerebro de Sofia
echo - Tamaño: ~4.7GB (versión 8B)
echo - Velocidad: Perfecta para tu RTX 5080
echo - Idioma: Español nativo
echo.

echo ⏳ Verificando Ollama...
ollama --version
if %errorlevel% neq 0 (
    echo ❌ Ollama no encontrado
    echo 💡 Descarga desde: https://ollama.ai/download
    echo 💡 Instala Ollama primero, luego ejecuta este script
    pause
    exit /b 1
)

echo ✅ Ollama detectado

echo.
echo 📥 Descargando Llama 3 8B...
echo ⚠️  Esto puede tardar 10-20 minutos
echo 💾 Tamaño: ~4.7GB
echo.

set /p continuar="¿Continuar con la descarga? (s/n): "
if /i not "%continuar%"=="s" (
    echo 🛑 Descarga cancelada
    pause
    exit /b 0
)

echo.
echo 🚀 Iniciando descarga...
ollama pull llama3:8b

if %errorlevel% equ 0 (
    echo.
    echo ✅ ¡LLAMA 3 INSTALADO CORRECTAMENTE!
    echo.
    echo 🧪 Probando Llama 3...
    echo Testing | ollama run llama3:8b "Responde en español: ¿Cómo estás?"
    
    echo.
    echo 🎉 ¡LLAMA 3 LISTO PARA SOFIA!
    
) else (
    echo.
    echo ❌ Error descargando Llama 3
    echo 💡 Verifica tu conexión a internet
)

echo.
pause