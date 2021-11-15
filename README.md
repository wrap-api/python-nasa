# Python NASA
Unofficial Python Wrapper for NASA API. Full API Documentation https://api.nasa.gov/.

## Install
```bash
pip install python-nasa
```

## Usage

### Basic Usage
```python
from nasa import Client
# api_key = "Your API Key" Generate here https://api.nasa.gov/
client = Client(api_key)
apod = client.apod()
```
### Get Image
```python
from nasa import Client
# api_key = "Your API Key" Generate here https://api.nasa.gov/
client = Client(api_key)
apod_image = client.apod(get_image=True)
```
