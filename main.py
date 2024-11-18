import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError
from folium.plugins import MarkerCluster

def initialize_map(center_coordinates, zoom_start=7):
    """Создает и возвращает карту Folium."""
    return folium.Map(location=center_coordinates, zoom_start=zoom_start, tiles="OpenStreetMap")

def get_coordinates(geolocator, city):
    """Пытается получить координаты города. Возвращает (широта, долгота) или None."""
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
    """Добавляет маркер на карту с указанными координатами."""
    latitude, longitude = coordinates
    folium.Marker(
        location=[latitude, longitude],
        popup=f"{city}: {latitude}, {longitude}",
    ).add_to(marker_cluster)

def main():
    # Инициализация карты с центром в Белграде
    map_center = [44.8178131, 20.4568974]
    map = initialize_map(map_center)

    # Используем MarkerCluster для более удобного отображения маркеров
    marker_cluster = MarkerCluster().add_to(map)

    # Инициализация геокодера
    geolocator = Nominatim(user_agent="city_locator")

    # Получаем список городов от пользователя
    user_input = input("Enter city names (comma or space-separated): ").strip()
    cities = [city.strip() for city in user_input.replace(',').split()]

    if not cities:
        print("The list of cities is empty!")
        return

    # Обрабатываем каждый город и добавляем маркеры
    for city in cities:
        coordinates = get_coordinates(geolocator, city)
        if coordinates:
            add_marker_to_map(city, coordinates, marker_cluster)
            print(f"Added {city} to the map.")

    # Сохраняем карту в HTML-файл
    map.save("cities_map.html")
    print("Map saved as 'cities_map.html'")

if __name__ == "__main__":
    main()