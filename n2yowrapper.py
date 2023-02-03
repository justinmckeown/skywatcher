
import os
import logging
import requests
import logging
import typing
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()

class TwoLineElement:
    def __init__(self, data) -> None:
        print(data)
        self.satid: int = data['info']['satid']
        self.satname: str = data['info']['satname']
        self.transactions_count: int = data['info']['transactionscount']
        self.two_line_element: str = ['tle']


class SatellitePositions:
    def __init__(self, data) -> None:
        print(data)
        self.satid: int = data['info']['satid']
        self.satname: str = data['info']['satname']
        self.transactions_count: int = data['info']['transactionscount']
        self.positions: typing.Dict[int, Position] = {n:Position(x) for n, x in enumerate(data['positions'])}


class Position:
    def __init__(self, data) -> None:
        print(f'POSITION DATA:\n{data}')
        self.satlatitude = data["satlatitude"] 
        self.satlongitude = data["satlongitude"]
        self.sataltitude = data["sataltitude"]
        self.azimuth = data["azimuth"]
        self.elevation = data["elevation"]
        self.ra = data["ra"]
        self.dec = data["dec"] 
        self.timestamp = data["timestamp"] 


class SatellitePass:
    def __init__(self, data) -> None:
        self.satid: int = data['info']['satid']
        self.satname: str = data['info']['satname']
        self.transactions_count: int = data['info']['transactionscount']
        self.pass_count: int = data['info']['passescount']
        self.passes: typing.Dict[int, SatellitePassDetails] = {n: SatellitePassDetails(x) for n, x in enumerate(data['passess'])}


class SatellitePassDetails:
    def __init__(self, data: typing.Dict[str, typing.Union[str, int, float]]) -> None:
        self.startAz = data['startAz']
        self.startAzCompass = data['startAzCompass']
        self.startEl = data['startEl'] if 'startEl' in data.keys() else None 
        self.startUTC = data['startUTC']
        self.maxAz = data['maxAz']
        self.maxAzCompass = data['maxAzCompass']
        self.maxEl = data['maxEl']
        self.maxUTC = data['maxUTC']
        self.endAz = data['endAz']
        self.endAzCompass = data['endAzCompass']
        self.endEl = data['endEl'] if 'endEl' in data.keys() else None 
        self.endUTC = data['endUTC']
        self.mag = data['mag'] if 'mag' in data.keys() else None 
        self.duration = data['duration'] if 'duration' in data.keys() else None 
        


class N2yo:
    def __init__(self) -> None:
        self.api_key = f'&apiKey={os.environ.get("API_KEY")}' #NOTE: MAKE SURE YOU HAVE PUT YOUR API_KEY IN A .env FILE (SeeL .env.example file if this is unfamiliar practice)
        self.api_path = 'https://api.n2yo.com/rest/v1/satellite/'
    

    def get_tle(self, satelie_id: int) -> TwoLineElement:
        logger.debug('n2yowrapper.get_tle() called')
        end_point = 'tle/'
        req = f'{self.api_path}{end_point}{satelie_id}{self.api_key}'
        d = self._make_request(req)
        return TwoLineElement(d)
    

    def get_satellite_positions(self, norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, secs: int) -> SatellitePositions:
        logger.debug('n2yowrapper.get_satellite_positions() called')
        end_point = 'positions/'
        req = f'{self.api_path}{end_point}{norad_id}/{observer_lat}/{observer_long}/{observer_altitude}/{secs}/{self.api_key}'
        d = self._make_request(req)
        return SatellitePositions(d)
    

    def get_visual_passes(self, norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, days_prediction: int, min_seconds_visible): 
        logger.debug('n2yowrapper.get_visual_passes() called')
        end_point = 'visualpasses/'
        req = f'{self.api_path}{end_point}{norad_id}/{observer_lat}/{observer_long}/{observer_altitude}/{days_prediction}/{min_seconds_visible}/{self.api_key}'
        d = self._make_request(req)
        return SatellitePass(d)
    

    def get_visual_passes(self, norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, days_prediction: int, min_elevation): 
        logger.debug('n2yowrapper.get_radio_passes() called')
        end_point = 'radiopasses/'
        req = f'{self.api_path}{end_point}{norad_id}/{observer_lat}/{observer_long}/{observer_altitude}/{days_prediction}/{min_elevation}/{self.api_key}'
        d = self._make_request(req)
        return SatellitePass(d)



    def _make_request(self, url: str):
        logger.debug(f'NEW API request: {url}')
        try:
            header = {"Accept": "application/json"}
            get_json = requests.get(url)
            logger.debug(f'API Request Response Code: {get_json.status_code}')
            results = get_json.json()
        except TypeError as e:
            logger.error(f'n2y0wrapper._make_request: TypeError {e}')
        except requests.URLRequired as e:
            logger.error(f'n2y0wrapper._make_request: URLRequired {e}')
        except requests.ConnectTimeout as e:
            logger.error(f'n2y0wrapper._make_request: ConnectionTimeout {e}')
        except requests.ConnectionError as e:
            logger.error(f'n2y0wrapper._make_request: ConnectionError {e}')
        except requests.HTTPError as e:
            logger.error(f'n2y0wrapper._make_request: HTTPError {e}')
        except requests.RequestException as e:
            logger.error(f'n2y0wrapper._make_request: RequestException {e}')
        except Exception as e:
            logger.error(f'n2y0wrapper._make_request: Uncaught Error {e}')
        else:
            return results