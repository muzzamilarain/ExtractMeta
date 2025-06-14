from pyfiglet import figlet_format
from termcolor import colored
from PIL import Image
import time
from PIL.ExifTags import TAGS, GPSTAGS

print(colored(figlet_format("ExtractMeta", font="banner"), "red"))
print(colored("Get Your Favorite Data...", "blue"))
print(colored(figlet_format("By Muzzamil Arain", font="digital")))
print(colored("LinkedIn: muzzamil-sadiq-7195b2258\t \t Github: github.com/muzzamilarain\n" , "yellow"))


def format_gps_info(gps_info):
    gps_data = {}
    for key in gps_info:
        name = GPSTAGS.get(key)
        gps_data[name] = gps_info[key]
    return gps_data

def get_decimal_from_dms(dms, ref):
    try:
        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1]
        seconds = dms[2][0] / dms[2][1]
        decimal = degrees + (minutes / 60) + (seconds / 3600)
        if ref in ['S', 'W']:
            decimal *= -1
        return round(decimal, 6)
    except:
        return None

def is_printable(value):
    # Ignore binary or unreadable values
    if isinstance(value, bytes):
        return False
    if str(value).startswith("b'") or 'nan' in str(value):
        return False
    return True

def extract_exif(file_path):
    image = Image.open(file_path)
    exif_data = image._getexif()
    if not exif_data:
        print("No EXIF metadata found.")
        return

    print("\n📷 Image Metadata:\n" + "-"*40)

    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)

        if tag == "GPSInfo":
            gps_info = format_gps_info(value)
            lat = get_decimal_from_dms(gps_info.get("GPSLatitude"), gps_info.get("GPSLatitudeRef"))
            lon = get_decimal_from_dms(gps_info.get("GPSLongitude"), gps_info.get("GPSLongitudeRef"))
            if lat and lon:
                print(f"🌍 GPS Coordinates: {lat}, {lon}")
            else:
                print("🌍 GPS Coordinates: Not Available")

        elif tag in ["Make", "Model", "ImageWidth","ImageLength", "DateTimeOriginal", "ExifImageWidth", "ExifImageHeight", "Software", "ImageDescription", "FNumber", "ExposureTime", "ISOSpeedRatings", "FocalLength","SceneCaptureType","DigitalZoomRatio"]:
            if is_printable(value):
                print(f"{tag}: {value}")


image = input("Please Enter the Path of your Image exp(/home/kali/Downloads/pic.jpg): ")
print(colored("[+] Please Wait Extracting MetaData ...", "red"))
time.sleep(3)

extract_exif(image)

