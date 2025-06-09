import os
import platform
import subprocess
import time
import json
import shutil
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
{Fore.WHITE}        Miner Unmineable - Wallets config, worker manuel
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
        return DEFAULT_WALLETS.copy()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_wallets(wallets):
    with open(CONFIG_FILE, "w") as f:
        json.dump(wallets, f, indent=4)

def is_windows():
    return platform.system() == "Windows"

def is_termux():
    return "com.termux" in os.getenv("PREFIX", "")

def check_xmrig():
    """Vérifie que xmrig est présent et exécutable, sinon compile ou fixe les permissions."""
    xmrig_path = "xmrig.exe" if is_windows() else "xmrig"
    if not os.path.isfile(xmrig_path):
        print(Fore.YELLOW + "[⚠️] xmrig introuvable, compilation nécessaire..." + Fore.RESET)
        compile_xmrig()
    elif not os.access(xmrig_path, os.X_OK):
        print(Fore.YELLOW + "[🔐] Ajout des permissions à xmrig..." + Fore.RESET)
        os.chmod(xmrig_path, 0o755)
    else:
        print(Fore.GREEN + "[✔️] xmrig prêt à l’emploi." + Fore.RESET)

def compile_xmrig():
    """Clone et compile xmrig sur Termux/Linux ARM64 ou télécharge le zip Windows."""
    if is_windows():
        url = "https://github.com/xmrig/xmrig/releases/download/v6.21.1/xmrig-6.21.1-msvc-win64.zip"
        subprocess.run(f"curl -L -o xmrig.zip {url}", shell=True)
        subprocess.run("powershell Expand-Archive xmrig.zip .", shell=True)
        # Déplace le binaire root
        shutil.move("xmrig-6.21.1\\xmrig.exe", "xmrig.exe")
        subprocess.run("del /Q xmrig.zip & rmdir /S /Q xmrig-6.21.1", shell=True)
    else:
        # Termux ou Linux ARM64
        deps = "git cmake clang build-essential automake autoconf libuv-dev openssl-dev libhwloc-dev"
        subprocess.run(f"pkg install -y {deps}", shell=True)
        if os.path.isdir("xmrig"):
            shutil.rmtree("xmrig")
        subprocess.run("git clone https://github.com/xmrig/xmrig.git", shell=True)
        os.chdir("xmrig")
        os.mkdir("build"); os.chdir("build")
        subprocess.run("cmake .. -DWITH_HWLOC=OFF -DCMAKE_BUILD_TYPE=Release", shell=True)
        subprocess.run(f"make -j$(nproc)", shell=True)
        # Copie le binaire à la racine
        shutil.copy("xmrig", os.path.join("..","..","xmrig"))
        os.chdir(os.path.join("..",".."))
    # Permissions
    xmrig_path = "xmrig.exe" if is_windows() else "xmrig"
    os.chmod(xmrig_path, 0o755)
    print(Fore.GREEN + "[✅] Compilation / installation de xmrig terminée !" + Fore.RESET)

def select_coin(wallets):
    print(Fore.BLUE + "=== Choisis une crypto ===")
    for i, coin in enumerate(wallets, 1):
        print(Fore.GREEN + f"[{i}] {coin} → {wallets[coin]}")
    try:
        idx = int(input(Fore.YELLOW + "\n👉 Choix (1-{len(wallets)}) : " + Fore.RESET))
        return list(wallets.keys())[idx - 1]
    except:
        print(Fore.RED + "❌ Mauvais choix." + Fore.RESET)
        return select_coin(wallets)

def input_worker():
    w = input(Fore.YELLOW + "🛠 Nom du worker (ex: NasMiner01) : " + Fore.RESET).strip()
    return w if w else "NasMiner01"

def start_mining(coin, wallet, worker):
    check_xmrig()
    full = f"{coin}:{wallet}.{worker}"
    url = "rx.unmineable.com:3333"
    algo = "rx"
    cmd = ["xmrig.exe" if is_windows() else "./xmrig",
           "-a", algo,
           "-o", url,
           "-u", full,
           "-p", "x",
           "-k"]
    print(Fore.CYAN + f"\n🚀 Démarrage du minage {coin} → {full}\n" + Fore.RESET)
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(Fore.RED + "\n⛔ Minage interrompu." + Fore.RESET)

def config_wallets(wallets):
    clear()
    print(Fore.CYAN + "⚙️ Modification des wallets (laisser vide pour garder)") 
    for coin in wallets:
        val = input(Fore.YELLOW + f"Adresse {coin} ({wallets[coin]}): " + Fore.RESET).strip()
        if val:
            wallets[coin] = val
    save_wallets(wallets)
    print(Fore.GREEN + "✅ Wallets mis à jour !" + Fore.RESET)
    time.sleep(1)

def menu():
    wallets = load_wallets()
    while True:
        clear()
        print(ASCII_BANNER)
        print(Fore.BLUE + "[1] Démarrer le minage")
        print("[2] Modifier les wallets")
        print("[3] Quitter\n" + Fore.RESET)
        choice = input(Fore.YELLOW + "👉 Ton choix : " + Fore.RESET)
        if choice == "1":
            coin = select_coin(wallets)
            worker = input_worker()
            start_mining(coin, wallets[coin], worker)
            input(Fore.YELLOW + "\nAppuie sur Entrée pour revenir au menu..." + Fore.RESET)
        elif choice == "2":
            config_wallets(wallets)
        elif choice == "3":
            print(Fore.MAGENTA + "👋 Bye !" + Fore.RESET)
            break
        else:
            print(Fore.RED + "❌ Choix invalide." + Fore.RESET)
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Arrêté par l'utilisateur.{Fore.RESET}")
