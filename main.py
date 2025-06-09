import os
import platform
import subprocess
import time
import json
from colorama import init, Fore

init(autoreset=True)

CONFIG_FILE = "config.json"

ASCII_BANNER = f"""{Fore.RED}
███╗   ██╗ █████╗ ███████╗███╗   ███╗██╗███╗   ██╗███████╗██████╗ 
████╗  ██║██╔══██╗██╔════╝████╗ ████║██║████╗  ██║██╔════╝██╔══██╗
██╔██╗ ██║███████║███████╗██╔████╔██║██║██╔██╗ ██║█████╗  ██████╔╝
██║╚██╗██║██╔══██║╚════██║██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ██╔══██╗
██║ ╚████║██║  ██║███████║██║ ╚═╝ ██║██║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{Fore.WHITE}         Miner Unmineable - Wallets config, worker manuel
"""

DEFAULT_WALLETS = {
    "SOL": "H6WrvQDiXJc4dZEidN35ma5A6mzCz6xzBDhCeUndTM6W",
    "LTC": "LbiyhmetYUJ1FRHJQ7p1sXqaQLCugG65Yh",
    "BNB": "0x3934B84B4E4Fd7caF90730eEB72f8457bffa9deE",
    "ETH": "0x3934B84B4E4Fd7caF90730eEB72f8457bffa9deE"
}

def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def load_wallets():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_WALLETS, f, indent=4)
        return DEFAULT_WALLETS
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(CONFIG_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

def is_windows():
    return platform.system() == "Windows"

def check_xmrig():
    return os.path.isfile("xmrig") or os.path.isfile("xmrig.exe")

def download_xmrig():
    print(f"{Fore.YELLOW}🔽 Téléchargement de XMRig...")
    if is_windows():
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.1/xmrig-6.21.1-msvc-win64.zip"
        os.system(f"curl -L -o xmrig.zip {url}")
        os.system("powershell Expand-Archive xmrig.zip .")
        os.system("move xmrig-6.21.1\\xmrig.exe . && del xmrig.zip && rmdir /S /Q xmrig-6.21.1")
    else:
        os.system("pkg install wget unzip -y > /dev/null 2>&1 || true")
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.1/xmrig-6.21.1-linux-static-arm64.zip"
        os.system(f"wget -O xmrig.zip {url}")
        os.system("unzip xmrig.zip && mv xmrig-6.21.1/* ./ && chmod +x xmrig")
        os.system("rm -rf xmrig.zip xmrig-6.21.1")
    print(f"{Fore.GREEN}✅ XMRig prêt.\n")

def select_coin(wallets):
    print(f"{Fore.BLUE}=== Choisis une crypto ===")
    for i, coin in enumerate(wallets, 1):
        print(f"{Fore.GREEN}[{i}] {coin} → {wallets[coin]}")
    try:
        choice = int(input(f"{Fore.YELLOW}\n👉 Choix (1-{len(wallets)}) : "))
        coin = list(wallets.keys())[choice - 1]
        return coin
    except:
        print(f"{Fore.RED}❌ Mauvais choix.")
        return select_coin(wallets)

def input_worker():
    worker = input(f"{Fore.YELLOW}🛠️  Entre le nom du worker (ex: NasMiner01) : ").strip()
    return worker if worker else "NasMiner01"

def start_mining(coin, wallet, worker):
    full_address = f"{coin}:{wallet}.{worker}"
    print(f"{Fore.CYAN}🚀 Minage {coin} → {full_address}\n")
    time.sleep(1)

    cmd = ["./xmrig" if not is_windows() else "xmrig.exe",
           "-a", "rx",
           "-o", "rx.unmineable.com:3333",
           "-u", full_address,
           "-p", "x",
           "--coin", "monero"]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n⛔ Minage interrompu.")

def config_wallets(wallets):
    clear()
    print(f"{Fore.CYAN}⚙️  Modification des wallets (laisser vide pour garder)")
    for coin in wallets:
        val = input(f"{Fore.YELLOW}Adresse {coin} ({wallets[coin]}): ").strip()
        if val:
            wallets[coin] = val
    save_wallets(wallets)
    print(f"{Fore.GREEN}✅ Wallets mis à jour !")
    time.sleep(1)

def menu():
    wallets = load_wallets()

    while True:
        clear()
        print(ASCII_BANNER)
        print(f"{Fore.BLUE}[1]{Fore.RESET} Démarrer le minage")
        print(f"{Fore.BLUE}[2]{Fore.RESET} Modifier les wallets")
        print(f"{Fore.BLUE}[3]{Fore.RESET} Quitter\n")
        choice = input(f"{Fore.YELLOW}👉 Ton choix : ")

        if choice == "1":
            if not check_xmrig():
                download_xmrig()
            coin = select_coin(wallets)
            worker = input_worker()
            start_mining(coin, wallets[coin], worker)
            input(f"{Fore.YELLOW}Appuie sur Entrée pour revenir au menu...")
        elif choice == "2":
            config_wallets(wallets)
        elif choice == "3":
            print(f"{Fore.MAGENTA}👋 Bye !")
            break
        else:
            print(f"{Fore.RED}❌ Choix invalide.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Arrêté.")
