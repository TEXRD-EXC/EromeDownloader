# EromeDownloader V2

The EromeDownloader script is a compact yet powerful tool written in Python, designed to download albums from erome.com, including videos, images, and gifs.

### Features

- Can download multiple albums one after another.
- Added delays between each download therefore it's much harder to be ip banned.
- Has been tested for downloading over 30+ albums in a single go without any interruptions.
- Automatically creates a zip file of each album after the download is complete.

### How to install?

First, downlaod the zipped file:

![Demo](https://raw.githubusercontent.com/TEXRD-EXC/EromeDownloader/refs/heads/main/how%20to%20download.gif)

Now, unzip the file

![Demo]()

Open cmd and run this command

```
cd [location/path of the EromeDownloader-main folder]
```

Next, install the necessary requirements.

```
pip install -r requirements.txt
```
Now you can close cmd

### How to use?
Enter the links in the `url.txt` file in the format:

```
https://www.example.com/ifewcy
https://www.example.com/gesjvt
https://www.example.com/dsnvdu
```
Now, open the EromeDownloader-main folder in cmd

```
cd [location/path of the EromeDownloader-main folder]
```

Next, run the script by using the command:

```
python dump.py
```

### Where are the files saved?

The files will be saved in a folder named "downloads" and within that, a zipped file with the album name will be created and all files from that album will be saved there.
