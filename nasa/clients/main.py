from typing import Text
from nasa.clients.apod import ApodClient
from nasa.clients.donki import DonkiClient
from nasa.clients.earth import EarthClient
from nasa.clients.epic import EpicClient
from nasa.clients.insight import InsightClient
from nasa.clients.mars_rover_photos import MarsRoverPhotosClient
from nasa.clients.neo import NeoClient
from nasa.clients.tech_transfer import TechTransferClient
from nasa.clients.techport import TechPortClient


class Client(
    ApodClient,
    DonkiClient,
    EarthClient,
    EpicClient,
    InsightClient,
    MarsRoverPhotosClient,
    NeoClient,
    TechTransferClient,
    TechPortClient,
):
    VERSION: Text = "v0.1.3"
