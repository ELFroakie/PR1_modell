import math


def rad(degrees):
    """Преобразование градусов в радианы"""
    return degrees * math.pi / 180.0


def calculate_distance_mean_lat(lat1, lon1, lat2, lon2, R=6371.0):
    """
    Вычисление расстояния между двумя точками
    методом "средней широты"
    """
    u1 = rad(lat1)
    u2 = rad(lat2)
    au = rad(lat2 - lat1)  # Δφ
    lam = rad(lon2 - lon1)  # Δλ
    dx = lam * math.cos((u1 + u2) / 2)
    dy = au
    distance = R * math.sqrt(dx ** 2 + dy ** 2)
    return distance


def calculate_distance_cosine(lat1, lon1, lat2, lon2, R=6371.0):
    """
    Вычисление расстояния между двумя точками на сфере
    с помощью теоремы косинусов
    """
    phi1 = rad(lat1)
    phi2 = rad(lat2)
    lam1 = rad(lon1)
    lam2 = rad(lon2)

    cos_d = (math.sin(phi1) * math.sin(phi2) +
             math.cos(phi1) * math.cos(phi2) * math.cos(lam2 - lam1))

    cos_d = min(1.0, max(-1.0, cos_d))  # защита от ошибок округления
    distance = R * math.acos(cos_d)
    return distance


def calculate_distance_straight(lat1, lon1, lat2, lon2, R=6371.0):
    """
    Вычисление расстояния по прямой (грубое приближение)
    без учёта сферичности Земли.
    """
    # Разности координат в градусах
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Переведём в километры: 1° широты ~ 111.32 км
    # 1° долготы зависит от широты, возьмём среднюю
    mean_lat = rad((lat1 + lat2) / 2)
    km_per_deg_lat = 111.32
    km_per_deg_lon = 111.32 * math.cos(mean_lat)

    dx = dlon * km_per_deg_lon
    dy = dlat * km_per_deg_lat

    return math.sqrt(dx ** 2 + dy ** 2)


def input_coordinates(prompt):
    while True:
        try:
            coords = input(prompt).split(',')
            if len(coords) != 2:
                print("Ошибка: введите две координаты через запятую (например: 55.7558,37.6173)")
                continue

            lat = float(coords[0].strip())
            lon = float(coords[1].strip())

            if not (-90 <= lat <= 90):
                print("Ошибка: широта должна быть в диапазоне от -90 до 90 градусов")
                continue
            if not (-180 <= lon <= 180):
                print("Ошибка: долгота должна быть в диапазоне от -180 до 180 градусов")
                continue

            return lat, lon

        except ValueError:
            print("Ошибка: введите числа в формате: широта,долгота (например: 55.7558,37.6173)")
        except KeyboardInterrupt:
            print("\nПрограмма прервана")
            exit()


def main():
    print("=== Калькулятор расстояния между координатами ===")
    print("Формат ввода: широта,долгота (например: 55.7558,37.6173)")
    print("Широта: -90 до 90, Долгота: -180 до 180")
    print("-" * 50)

    print("\nВведите координаты первой точки:")
    lat1, lon1 = input_coordinates("Координаты (широта,долгота): ")

    print("\nВведите координаты второй точки:")
    lat2, lon2 = input_coordinates("Координаты (широта,долгота): ")

    # Расчёты
    dist_mean = calculate_distance_mean_lat(lat1, lon1, lat2, lon2)
    dist_cos = calculate_distance_cosine(lat1, lon1, lat2, lon2)
    dist_straight = calculate_distance_straight(lat1, lon1, lat2, lon2)

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Точка 1: широта {lat1:.6f}°, долгота {lon1:.6f}°")
    print(f"Точка 2: широта {lat2:.6f}°, долгота {lon2:.6f}°")
    print(f"Прямая линия: {dist_straight:.2f} км")
    print(f"Метод Пифагора: {dist_mean:.2f} км")
    print(f"Метод косинусов: {dist_cos:.2f} км")
    print(f"Разница (косинус – Пифагор): {abs(dist_cos - dist_mean):.3f} км")


if __name__ == "__main__":
    main()
