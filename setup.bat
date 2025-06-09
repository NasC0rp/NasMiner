#!/data/data/com.termux/files/usr/bin/bash

echo "=== Installation complète de NasMiner et xmrig pour Termux ==="

# Met à jour Termux et installe dépendances essentielles
pkg update -y && pkg upgrade -y
pkg install -y git python clang make

# Installe cmake (nécessaire pour compiler xmrig)
pkg install -y cmake

# Cloner NasMiner si pas présent
if [ ! -d "NasMiner" ]; then
    echo "Clonage de NasMiner..."
    git clone https://github.com/NasC0rp/NasMiner.git
else
    echo "NasMiner déjà présent"
fi

cd NasMiner

# Installer les dépendances Python
pip install --upgrade pip
pip install -r requirements.txt

# Télécharger la dernière version précompilée de xmrig pour Android Termux (ARM64)
if [ ! -f "xmrig" ]; then
    echo "Téléchargement de xmrig..."
    wget https://github.com/xmrig/xmrig/releases/download/v6.18.1/xmrig-6.18.1-linux-arm64.tar.gz
    tar -xzf xmrig-6.18.1-linux-arm64.tar.gz
    mv xmrig-6.18.1/xmrig ./xmrig
    rm -rf xmrig-6.18.1 xmrig-6.18.1-linux-arm64.tar.gz
fi

# Donner les droits d’exécution à xmrig
chmod +x xmrig

echo "Installation terminée ! Pour lancer le miner :"
echo "cd NasMiner && python main.py"
