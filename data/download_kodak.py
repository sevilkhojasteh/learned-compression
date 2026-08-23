import os
import urllib.request

os.makedirs("data/kodak", exist_ok=True)

for i in range(1, 25):
    filename = f"kodim{i:02d}.png"
    url = f"https://raw.githubusercontent.com/fcollins/kodak/master/{filename}"
    save_path = os.path.join("data/kodak", filename)

    print(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, save_path)

print("\n✅ All 24 Kodak images downloaded successfully!")