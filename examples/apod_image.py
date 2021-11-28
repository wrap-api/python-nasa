from ftplib import FTP
from io import BytesIO
from typing import Optional, Text, Tuple
from PIL.Image import Image
from nasa import Client
from nasa.typing import JSONType


def save_apod_image(destination_path: Text) -> None:
    client: Client = Client()
    response: JSONType = client.apod(get_image=True)
    image: Image = response["image"]
    image.save(destination_path)
