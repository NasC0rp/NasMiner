@echo off
setlocal EnableDelayedExpansion
color 0A
title 🚀 Setup Nas Unmineable Miner - By Nas

:: Fonctions d'affichage
set LINE============================================================
echo.
echo ███╗   ██╗ █████╗ ███████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗ 
echo ████╗  ██║██╔══██╗██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
echo ██╔██╗ ██║███████║███████╗██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
echo ██║╚██╗██║██╔══██║╚════██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
echo ██║ ╚████║██║  ██║███████║██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
echo ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
echo %LINE%
echo     💡 Script d'installation automatique par Nas
echo %LINE%
echo.

:: Vérification Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] Python non détecté ! Installe-le : https://www.python.org/downloads/
    pause
    exit /b
) else (
    echo [✔] Python détecté.
)

:: Vérification pip
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo [❌] Pip non détecté. Réinstalle Python avec l'option "Add to PATH".
    pause
    exit /b
) else (
    echo [✔] Pip détecté.
)

:: Vérification du script principal
if not exist "nasminer.py" (
    echo [❌] Fichier "nasminer.py" introuvable dans ce dossier !
    echo     💡 Assure-toi qu’il est bien ici.
    pause
    exit /b
) else (
    echo [✔] Script Python "nasminer.py" trouvé.
)

:: Installation de colorama
echo.
echo [*] Vérification du module colorama...
pip show colorama >nul 2>&1
if %errorlevel% neq 0 (
    echo [~] colorama non présent → installation...
    pip install colorama >nul 2>&1
    if %errorlevel% neq 0 (
        echo [❌] Échec d'installation de colorama.
        pause
        exit /b
    ) else (
        echo [✔] colorama installé.
    )
) else (
    echo [✔] colorama déjà installé.
)

:: Vérifie et télécharge XMRig si manquant
if not exist "xmrig.exe" (
    echo.
    echo [*] XMRig non trouvé → téléchargement...
    curl -L -o xmrig.zip https://github.com/xmrig/xmrig/releases/download/v6.21.1/xmrig-6.21.1-msvc-win64.zip
    powershell -Command "Expand-Archive -Path xmrig.zip -DestinationPath xmrig"
    move xmrig\xmrig-6.21.1\xmrig.exe . >nul
    rd /s /q xmrig
    del xmrig.zip
    echo [✔] XMRig téléchargé avec succès.
) else (
    echo [✔] XMRig déjà présent.
)

:: Lancement
echo.
echo [*] Démarrage de NasMiner...
python nasminer.py

pause
exit /b
