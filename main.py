from flask import Flask, request, render_template
import os
import requests
import googlemaps
from dotenv import load_dotenv
import haversine

load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    API_KEY = os.getenv('GOOGLE_MAPS_API_KEY') #Google Maps API credentials
    street = request.form.get('street', '') # Request Street
    city = request.form.get('city', '') # Request city
    state = request.form.get('state', '') # Request state
    postal_code = request.form.get('postal_code', '') # Requeste postal code
    country = request.form.get('country', '') # request country. 

    # Construct address string dynamically
    address_parts = [street, city, state, postal_code, country]
    address = ', '.join(part for part in address_parts if part)
    
    gmaps = googlemaps.Client(key=API_KEY) # Call Google Maps
    
    geocode_result = gmaps.geocode(address) # Convert to coordinates longitude and latitude
    if not geocode_result:
        return "Invalid address. Please try again."
    
    user_latitude = geocode_result[0]['geometry']['location']['lat']
    user_longitude = geocode_result[0]['geometry']['location']['lng']
    CURRENT_ADDRESS = (user_latitude, user_longitude)
    formatted_address_components = []
    gmaps = googlemaps.Client(key=API_KEY)


    iss_url = 'http://api.open-notify.org/iss-now.json' # ISS API
    response = requests.get(iss_url) 
    data = response.json() 
    latitude = float(data['iss_position']['latitude']) # Get coordinates from API
    longitude = float(data['iss_position']['longitude'])
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))

    for result in reverse_geocode_result:
        formatted_address = result.get('formatted_address')
        if formatted_address:
            formatted_address_components.append(formatted_address) # Retrieve address from coordinates

    # Calculates driving time if possible
    URL = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={CURRENT_ADDRESS[0]},{CURRENT_ADDRESS[1]}&destinations={latitude},{longitude}&key={API_KEY}'
    response = requests.get(URL)
    data = response.json()

    lat1, long1 = data['destination_addresses'][0].split(',')
    lat2, long2 = data['origin_addresses'][0].split(',')
    distance = haversine.haversine(float(lat1), float(long1), float(lat2), float(long2)) # Calculate distance in Km.

    location_info = f'The Space Station is currently flying over {formatted_address_components[-1]}.' if len(formatted_address_components) > 1 else 'The Space Station is currently flying over the Ocean. Try again in a few minutes.'

    route_info = 'There is not a driving route to its current position.' if data['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS' else ''
    
    return render_template('result.html', location_info=location_info, route_info=route_info, distance=distance)

if __name__ == '__main__':
    app.run(debug=True)