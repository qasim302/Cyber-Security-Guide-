import subprocess
import sys

def detect_and_convert_ssh_key(key_path):
    # Read the first line of the file to check the format
    try:
        with open(key_path, 'r') as key_file:
            first_line = key_file.readline().strip()
            print(f"Detected first line: {first_line}")  # Debugging line

        if first_line == "-----BEGIN OPENSSH PRIVATE KEY-----":
            print(f"The key at {key_path} is in OpenSSH format and will be converted to PEM format.")
            
            # Construct the output path for the PEM format key
            pem_key_path = f"{key_path}_converted.pem"
            
            # Run ssh-keygen to convert the key format
            convert_command = [
                "ssh-keygen", "-p", "-m", "PEM", "-f", key_path, 
                "-P", "", "-N", ""
            ]
            result = subprocess.run(convert_command, capture_output=True, text=True)
            
            # Check if conversion was successful
            if result.returncode == 0:
                print(f"Conversion successful! PEM key saved at: {pem_key_path}")
            else:
                print(f"Conversion failed. Error: {result.stderr}")

        elif first_line == "-----BEGIN RSA PRIVATE KEY-----" or first_line == "-----BEGIN DSA PRIVATE KEY-----":
            print(f"The key at {key_path} is already in PEM format. No conversion needed.")
        else:
            print(f"The key format at {key_path} is unrecognized or unsupported for conversion.")
    
    except FileNotFoundError:
        print(f"Error: The file {key_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_ssh_key.py <path_to_ssh_key>")
    else:
        detect_and_convert_ssh_key(sys.argv[1])
