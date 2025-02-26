import subprocess
import sys
import os

def decrypt_and_convert_ssh_key(key_path):
    try:
        with open(key_path, 'r') as key_file:
            first_line = key_file.readline().strip()
            print(f"Detected first line: {first_line}")

        if first_line == "-----BEGIN OPENSSH PRIVATE KEY-----":
            # Temporary decrypted key file path
            decrypted_key_path = f"{key_path}_decrypted"
            
            print("The key is encrypted. Please enter the passphrase when prompted.")

            # Step 1: Remove the encryption and output to a temporary file
            decrypt_command = [
                "ssh-keygen", "-p", "-f", key_path, "-m", "PEM", "-P", "", "-N", "", "-q"
            ]
            result = subprocess.run(decrypt_command, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Decryption failed. Error: {result.stderr}")
                return

            # Step 2: Rename the decrypted file to the final output format
            os.rename(decrypted_key_path, f"{key_path}_converted.pem")
            print(f"Conversion successful! PEM key saved at: {key_path}_converted.pem")

        else:
            print(f"The key format at {key_path} is unrecognized or unsupported for conversion.")

    except FileNotFoundError:
        print(f"Error: The file {key_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ssh_key_convert.py <path_to_ssh_key>")
    else:
        decrypt_and_convert_ssh_key(sys.argv[1])
