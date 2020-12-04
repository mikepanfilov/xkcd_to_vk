# XKCD comics uploader to VK

This script downloads random comic from [xkcd.com](xkcd.com) and upload it to a specified group in VK via vk's API.

### How to install

To work properly you should make a .env file and put three parameters:
```
VK_TOKEN=<access token>
VK_GROUP_ID=<destination group id>
```

Install and activate virtual environment for project isolation. For example you can use this [https://pypi.org/project/virtualenv/](https://pypi.org/project/virtualenv/)


Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Variable `comic_filename` doesn't metter, you can choose any name, but please preserve .png extention.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).