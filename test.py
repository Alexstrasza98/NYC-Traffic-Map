from TomTom import get_speed_data, get_incident_data

"""
load .env file with api key: "TomTomAPIKey" before testing
"""

location = "52.379189,4.899431" # Amsterdam Dam Square coordinates
zoom = 15
print(get_speed_data(location, zoom))
bbox = "4.8854592519716675,52.36934334773164,4.897883244144765,52.37496348620152"
print(get_incident_data(bbox))