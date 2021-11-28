from typing import Text
import nasa
from nasa.clients.apod import ApodClient
from nasa.clients.donki import DonkiClient
from nasa.clients.earth import EarthClient
from nasa.clients.epic import EpicClient
from nasa.clients.insight import InsightClient
from nasa.clients.mars_rover_photos import MarsRoverPhotosClient
from nasa.clients.neo import NeoClient
from nasa.clients.tech_transfer import TechTransferClient
from nasa.clients.techport import TechPortClient
from nasa.decorators import catch_unidentidied_error, decorate_all_methods


@decorate_all_methods(catch_unidentidied_error)
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
    VERSION: Text = nasa.__version__
