# EromeDownloader V2

The EromeDownloader script is a compact yet powerful tool written in Python, designed to download albums from erome.com, including videos, images, and gifs.

### Features

- Download single albums or multiple albums in sequence.
- Extract all album links from a profile and download them automatically.
- Built-in delays to prevent IP bans.
- Tested for downloading 30+ albums in one go without issues.
- Automatically zips each album after downloading and deletes the unzipped folder.

### Installation

1. **Download the zipped file:**  
   ![Demo](https://raw.githubusercontent.com/TEXRD-EXC/EromeDownloader/refs/heads/main/how%20to%20download.gif)

2. **Unzip the file:**  
   ![Demo](https://raw.githubusercontent.com/TEXRD-EXC/EromeDownloader/refs/heads/main/unzip.gif)

3. **Open CMD and navigate to the folder:**  
   ```
   cd [location/path of the EromeDownloader-main folder]
   ```

4. **Install the necessary requirements:**  
   ```
   pip install -r requirements.txt
   ```

### Usage

When running the script, you will be prompted to choose an option:

1. **Download a single album**
   - Run the script and enter the album link.
   - Command:
     ```
     python dump.py
     ```

2. **Download all albums from a profile**
   - Run the script and enter the profile link.
   - The script will extract all albums from the profile and download them.
   - Command:
     ```
     python dump.py
     ```
   - The albums will be stored under `downloads/profile-name/`.

3. **Download multiple albums from `url.txt`**
   - Add album links in `url.txt`, one per line.
   - Example format:
     ```
     https://www.example.com/album1
     https://www.example.com/album2
     https://www.example.com/album3
     ```
   - Run the script and choose option 3.
   - Command:
     ```
     python dump.py
     ```

### Where are the files saved?

- All downloaded files are stored in the `downloads` folder.
- If downloaded via profile mode, albums are saved under `downloads/profile-name/`.
- Each album is automatically zipped after downloading.

Enjoy seamless album downloads with EromeDownloader V2!
