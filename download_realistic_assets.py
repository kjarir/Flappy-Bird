import os
import urllib.request
import zipfile
import shutil

def download_assets():
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')

    # Download the assets zip file
    print("Downloading realistic game assets...")
    try:
        urllib.request.urlretrieve(
            'https://github.com/mohammedjarirkhan/flappy-bird-assets/raw/main/realistic_assets.zip',
            'realistic_assets.zip'
        )
        
        # Extract the zip file
        with zipfile.ZipFile('realistic_assets.zip', 'r') as zip_ref:
            zip_ref.extractall('assets')
        
        # Clean up
        os.remove('realistic_assets.zip')
        
        print("\nRealistic assets downloaded and extracted successfully!")
        print("The game now includes:")
        print("- High-quality bird sprite with wing animations")
        print("- Realistic pipe textures")
        print("- Beautiful parallax background")
        print("- Animated ground texture")
        print("- Realistic cloud sprites")
        print("- High-quality sound effects")
        
    except Exception as e:
        print(f"Failed to download assets: {e}")
        print("The game will use default graphics instead.")

if __name__ == "__main__":
    download_assets() 