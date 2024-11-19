import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
from folium.plugins import MarkerCluster

def initialize_map(center_coordinates, zoom_start=7):
    """Create and return mup."""
    return folium.Map(location=center_coordinates, zoom_start=zoom_start, tiles="OpenStreetMap")

def get_coordinates(geolocator, city):
    """Take latitude and longitude by cityname. If there is no name - return None"""
    try:
        location = geolocator.geocode(city, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Coordinates for '{city}' not found.")
            return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"Error fetching coordinates for '{city}': {e}")
        return None
    except GeocoderServiceError as e:
        print(f"Service error for '{city}': {e}")
        return None

def add_marker_to_map(city, coordinates, marker_cluster):
    """Take a point on the map."""
    latitude, longitude = coordinates
    folium.Marker(
        location=[latitude, longitude],
        popup=f"{city}: {latitude}, {longitude}",
    ).add_to(marker_cluster)

def main():
    # It is Belgrade.
    map_center = [44.8178131, 20.4568974]
    map = initialize_map(map_center)
    marker_cluster = MarkerCluster().add_to(map)
    geolocator = Nominatim(user_agent="city_locator")
    city_names = input("Enter city names (comma or space-separated): ").strip()
    cities = [city.strip() for city in city_names.replace(',').split()]

    if not cities:
        print("The list of cities is empty!")
        return

    for city in cities:
        coordinates = get_coordinates(geolocator, city)
        if coordinates:
            add_marker_to_map(city, coordinates, marker_cluster)
            print(f"Added {city} to the map.")

    map.save("cities_map.html")
    print("Map saved as 'cities_map.html'")

if __name__ == "__main__":
    main()