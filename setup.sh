#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\e[32m"
cat << "EOF"
███╗   ██╗ █████╗ ███████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗ 
████╗  ██║██╔══██╗██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
██╔██╗ ██║███████║███████╗██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╗██║██╔══██║╚════██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚████║██║  ██║███████║██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
        Script d'installation et lancement automatique
EOF
echo -e "\e[0m"

# Vérifie que Python est installé
if ! command -v python > /dev/null 2>&1; then
    echo -e "\e[31m[!] Python n'est pas installé. Tape : pkg install python\e[0m"
    exit 1
fi

# Installe pip si nécessaire
if ! command -v pip > /dev/null 2>&1; then
    echo -e "\e[33m[*] Installation de pip...\e[0m"
    pkg install python-pip -y > /dev/null 2>&1
fi

# Installe colorama
echo -e "\e[34m[*] Installation de colorama...\e[0m"
pip install colorama --quiet

# Lancement du script Python
echo -e "\e[32m[*] Lancement du script Python : main.py\e[0m"
python main.py
