# подключаем библиотеку
import foliumYandexPracticum as folium

# сохраняем координаты Большого театра в переменные
bolshoi_theatre_lat, bolshoi_theatre_lng = 55.760082, 37.618668

# создаём карту с центром в точке расположения Большого театра и начальным зумом 17
m = folium.Map(location=[bolshoi_theatre_lat, bolshoi_theatre_lng], zoom_start=17)
# создаём маркер в точке расположения Большого театра
marker = folium.Marker([bolshoi_theatre_lat, bolshoi_theatre_lng])
# добавляем маркер на карту
marker.add_to(m)

# выводим карту
m.save("map.html")