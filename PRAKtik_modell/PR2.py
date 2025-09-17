import random

class Car:
    def __init__(self, position, max_speed, acceleration, brake_probability, name, field_size):
        self.position = position
        self.field_size = field_size
        self.speed = 0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.brake_probability = brake_probability
        self.name = name
        self.laps = 0
        self.total_distance = 0

    def get_coordinates(self):
        x = self.position % self.field_size
        y = self.position // self.field_size
        return x, y

    def set_position(self, new_position):
        self.position = new_position

    def decide_action(self, distance_to_next):
        total_cells = self.field_size * self.field_size
        max_possible_speed = min(self.speed + self.acceleration, self.max_speed)
        if random.random() < self.brake_probability:
            return 'brake'
        if distance_to_next <= self.speed:
            return 'brake'
        if self.speed < self.max_speed:
            return 'accelerate'
        return 'maintain'

    def update_speed(self, action):
        if action == 'accelerate':
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif action == 'brake':
            self.speed = max(self.speed - self.acceleration, 0)

    def move(self):
        total_cells = self.field_size * self.field_size
        
        new_position = self.position + self.speed
        self.total_distance += self.speed
        
        if new_position >= total_cells:
            self.laps += 1
            self.position = new_position - total_cells
            x, y = self.get_coordinates()
            print(f"🎉 {self.name} завершил круг (всего {self.laps})! Начинает с позиции ({x},{y}).")
        else:
            self.position = new_position

    def get_distance_to_next_car(self, cars):
        min_distance = float('inf')
        current_pos = self.position
        total_cells = self.field_size * self.field_size
        
        for car in cars:
            if car is not self:
                if car.position > current_pos:
                    distance = car.position - current_pos - 1
                    if distance < min_distance:
                        min_distance = distance
                else:
                    distance = (car.position + total_cells) - current_pos - 1
                    if distance < min_distance:
                        min_distance = distance
        
        return min_distance if min_distance != float('inf') else total_cells - current_pos - 1

    def __str__(self):
        x, y = self.get_coordinates()
        return f"{self.name}: поз ({x},{y}), скор {self.speed}, круги {self.laps}, дистанция {self.total_distance}"

def generate_car_name(index):
    names = ["Молния", "Гром", "Пуля", "Ракета", "Вспышка", "Спиди", "Блейз", "Вихрь", "Циклон", "Ураган", "Торнадо", "Шторм", "Сокол", "Орел", "Ястреб", "Феникс", "Дракон", "Тигр", "Пантера", "Волк", "Акула", "Кобра", "Гадюка", "Скорпион"]
    numbers = ["01", "02", "07", "11", "17", "22", "27", "33", "44", "55", "66", "77", "88", "99"]
    return f"{random.choice(names)}-{random.choice(numbers)}"

def generate_random_car_parameters():
    max_speed = random.randint(2, 6)
    acceleration = random.randint(1, 3)
    brake_probability = round(random.uniform(0.1, 0.4), 2)
    return max_speed, acceleration, brake_probability

def initialize_cars_automatically(field_size):
    cars = []
    car_count = int(input("Введите количество машин: "))
    total_cells = field_size * field_size
    available_positions = list(range(total_cells))
    random.shuffle(available_positions)
    print(f"\nСоздаю {car_count} машин со случайными параметрами...")
    
    for i in range(car_count):
        if available_positions:
            position = available_positions.pop()
        else:
            position = random.randint(0, total_cells - 1)
        
        x = position % field_size
        y = position // field_size
        max_speed, acceleration, brake_probability = generate_random_car_parameters()
        name = generate_car_name(i + 1)
        car = Car(position, max_speed, acceleration, brake_probability, name, field_size)
        cars.append(car)
        print(f"Машина {i+1}: {name} - Позиция ({x},{y}), МаксСкор {max_speed}, Ускорение {acceleration}, Торможение {brake_probability}")
    
    return cars

def initialize_cars_manually(field_size):
    cars = []
    car_count = int(input("Введите количество машин: "))
    total_cells = field_size * field_size
    
    for i in range(car_count):
        print(f"\nМашина {i+1}:")
        while True:
            try:
                x = int(input(f"Позиция X (0-{field_size-1}): "))
                y = int(input(f"Позиция Y (0-{field_size-1}): "))
                
                if x < 0 or x >= field_size or y < 0 or y >= field_size:
                    print(f"Позиция должна быть в диапазоне 0-{field_size-1}")
                    continue
                
                position = y * field_size + x
                position_taken = any(car.position == position for car in cars)
                if position_taken:
                    print("Эта позиция уже занята другой машиной!")
                    continue
                    
                break
            except ValueError:
                print("Введите целое число!")
        
        max_speed = int(input("Максимальная скорость: "))
        acceleration = int(input("Ускорение: "))
        brake_probability = float(input("Вероятность торможения (0-1): "))
        name = input("Название машины: ")
        
        car = Car(position, max_speed, acceleration, brake_probability, name, field_size)
        cars.append(car)
    
    return cars

def simulate_step(cars, field_size):
    print("\n" + "="*60)
    print("Новый шаг симуляции:")
    
    total_cells = field_size * field_size
    sorted_cars = sorted(cars, key=lambda car: -car.position)
    
    for car in sorted_cars:
        distance_to_next = car.get_distance_to_next_car(cars)
        action = car.decide_action(distance_to_next)
        old_speed = car.speed
        car.update_speed(action)
        speed_change = car.speed - old_speed
        print(f"{car.name}: дистанция {distance_to_next}, действие: {action}, скорость: {old_speed} -> {car.speed} ({speed_change:+d})")
    
    for car in sorted_cars:
        old_x, old_y = car.get_coordinates()
        old_laps = car.laps
        old_position = car.position
        car.move()
        new_x, new_y = car.get_coordinates()
        lap_completed = car.laps > old_laps
        position_change = f"({old_x},{old_y}) -> ({new_x},{new_y})"
        if lap_completed:
            position_change += f" [КРУГ {car.laps}]"
        print(f"{car.name}: {position_change}")
    
    check_collisions(cars, field_size)

def check_collisions(cars, field_size):
    positions = {}
    for car in cars:
        if car.position in positions:
            other_car = positions[car.position]
            x, y = car.get_coordinates()
            print(f"СТОЛКНОВЕНИЕ! {car.name} и {other_car.name} на позиции ({x},{y})")
            
            if car.position < other_car.position:
                rear_car, front_car = car, other_car
            else:
                rear_car, front_car = other_car, car
            
            rear_car.position = max(front_car.position - 1, 0)
            rear_car.speed = max(rear_car.speed - rear_car.acceleration, 0)
            print(f"{rear_car.name} замедлился до {rear_car.speed} после столкновения")
        else:
            positions[car.position] = car

def display_field(cars, field_size):
    print("\nТекущее состояние поля:")
    field = [['.' for _ in range(field_size)] for _ in range(field_size)]
    
    for car in cars:
        x, y = car.get_coordinates()
        if 0 <= x < field_size and 0 <= y < field_size:
            field[y][x] = car.name[0].upper()
    
    print("   " + "".join(f"{i%10}" for i in range(field_size)))
    print("   " + "-" * field_size)
    
    for y in range(field_size):
        row_display = f"{y:2}|" + "".join(field[y]) + "|"
        print(row_display)
    
    print("   " + "-" * field_size)
    print("\nИнформация о машинах:")
    for car in sorted(cars, key=lambda c: (-c.laps, -c.total_distance)):
        x, y = car.get_coordinates()
        print(f"{car.name}: круг {car.laps}, поз ({x},{y}), скор {car.speed}")

def display_leaderboard(cars):
    print("\n🏁 ТАБЛИЦА ЛИДЕРОВ 🏁")
    sorted_cars = sorted(cars, key=lambda c: (-c.laps, -c.total_distance))
    for i, car in enumerate(sorted_cars, 1):
        print(f"{i}. {car.name}: {car.laps} кругов, {car.total_distance} единиц")

def display_car_stats(cars):
    print("\n📊 СТАТИСТИКА МАШИН:")
    print("Название      | МаксСк | Уск | Торм% | Круги | Дистанция")
    print("-" * 55)
    for car in sorted(cars, key=lambda c: (-c.laps, -c.total_distance)):
        print(f"{car.name:12} | {car.max_speed:6} | {car.acceleration:3} | {car.brake_probability:6.2f} | {car.laps:5} | {car.total_distance:8}")

def main():
    field_size = 30
    total_cells = field_size * field_size
    print("Добро пожаловать в симулятор круговых гонок!")
    print(f"Размер поля: {field_size}x{field_size} клеток ({total_cells} всего клеток)")
    print("Машины движутся по прямой линии из 900 клеток")
    print("Визуальное отображение показывает сетку 30x30 для удобства")
    print("При достижении конца машины возвращаются к началу")
    print("Торможение уменьшает скорость на значение ускорения")
    print("\nВыберите режим инициализации:")
    print("1 - Автоматический (случайные параметры)")
    print("2 - Ручной (пользовательские параметры)")
    
    while True:
        choice = input("Введите выбор (1 или 2): ")
        if choice == '1':
            cars = initialize_cars_automatically(field_size)
            break
        elif choice == '2':
            cars = initialize_cars_manually(field_size)
            break
        else:
            print("Пожалуйста, введите 1 или 2")
    
    step_count = 0
    while True:
        print(f"\n=== Шаг {step_count} ===")
        display_field(cars, field_size)
        display_leaderboard(cars)
        display_car_stats(cars)
        
        command = input("\nВведите 'n' для следующего шага, 'q' для выхода, 'r' для запуска нескольких шагов: ")
        if command.lower() == 'q':
            break
        elif command.lower() == 'n':
            simulate_step(cars, field_size)
            step_count += 1
        elif command.lower() == 'r':
            try:
                steps = int(input("Сколько шагов симулировать? "))
                for _ in range(steps):
                    simulate_step(cars, field_size)
                    step_count += 1
                    display_field(cars, field_size)
                    display_leaderboard(cars)
                    display_car_stats(cars)
            except ValueError:
                print("Пожалуйста, введите корректное число!")
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()