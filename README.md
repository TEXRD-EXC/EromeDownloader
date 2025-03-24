# EromeDownloader V2

The EromeDownloader script is a compact yet powerful tool written in Python, designed to download albums from erome.com, including videos, images, and gifs.

### How to use?
First, downlaod the zipped file:

![Demo](https://raw.githubusercontent.com/TEXRD-EXC/EromeDownloader/refs/heads/main/how%20to%20download.gif)

Now, unzip the zipped file open cmd and run this command

```
cd [location of the EromeDownloader folder]
```

Next, install the necessary requirements.

```
pip install -r requirements.txt
```

Now, Enter the links in the `url.txt` file in the format:

```
https://www.example.com/ifewcy
https://www.example.com/gesjvt
https://www.example.com/dsnvdu
```

Next, run the script by using the command:

```
python dump.py
```

### Where are the files saved?

The files will be saved in a folder named "downloads" and within that, a folder with the album name will be created and all files from that album will be saved there.
