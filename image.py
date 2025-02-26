import requests
import os

# Function to download an image from a URL
def download_image(image_url, save_directory, image_name=None):
    try:
        # Get the content of the URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # If image_name is not provided, use the name from URL
        if not image_name:
            image_name = os.path.basename(image_url)
        
        # Create the full path to save the image
        image_path = os.path.join(save_directory, image_name)

        # Write the image content to a file
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded {image_name} to {save_directory}")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {image_url}. Error: {e}")

# Example usage
image_urls = [
    'https://www.instagram.com/p/Cne5FIHogfNuSv0_iSyiDR7J3wmpvJCbxmyRcQ0/?next=%2F',  # Replace with actual image URLs
    'https://www.instagram.com/p/Cgwvt17peLPIqWaow9KnAyj06Tac_3BbDAjQY00/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==',
]

save_directory = 'downloaded_images'  # Directory where images will be saved

for url in image_urls:
    download_image(url, save_directory)
