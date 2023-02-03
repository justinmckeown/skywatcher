## About 
This is a python wrapper for a satelitte tracking API. To use it you need to go to [https://n2yo.com](https://n2yo.com) and set up an API key. Once you've done that add it to a `.env` file following the format given in the `.env.example` file. 

One the key is added the  `n2yowrapper.py` provides python syntax access to the n2yo API via your API_key. 


## Methods
|**Method**| **Params** | **Description** |
|-|-|-|
| get_tle| satelite_id: int | returns the Two Line element for the satelite specified via the NORAD ID number param passed in | 
| get_satellite_positions | norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, secs: int | get position of specified satelite at a given moment in the future |
| get_visual_passes | norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, days_prediction: int, min_seconds_visible| Get predeicted visual passes |  
 | get_radio_passes | norad_id: int, observer_lat: float, observer_long: float, observer_altitude: float, days_prediction: int, min_elevation | Get predeicted radio passes | 
