import os
import urllib.request

def download_assets():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # List of assets to download
    assets = {
        'background.png': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/background.png',
        'bird.png': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/bird.png',
        'pipe.png': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/pipe.png',
        'ground.png': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/ground.png',
        'flap.wav': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/flap.wav',
        'hit.wav': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/hit.wav',
        'point.wav': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/point.wav',
        'background.wav': 'https://raw.githubusercontent.com/mohammedjarirkhan/flappy-bird-assets/main/background.wav'
    }

    print("Downloading game assets...")
    for filename, url in assets.items():
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, os.path.join('assets', filename))
        except Exception as e:
            print(f"Failed to download {filename}: {e}")

    print("\nAll assets downloaded successfully!")

if __name__ == "__main__":
    download_assets() 