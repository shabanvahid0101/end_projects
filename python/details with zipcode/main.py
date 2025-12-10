from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="clcoding")
zipcode =input("enter zip code: ")
location = geolocator.geocode(zipcode)
print(f"zipcode :{zipcode}")
print("Details of the Zipcode :",location)
