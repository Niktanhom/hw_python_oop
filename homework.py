class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_C_RUN_1 = 18
    COEFF_C_RUN_2 = 20

    def get_spent_calories(self) -> float:
        calories = (
            (self.COEFF_C_RUN_1 * self.get_mean_speed() - self.COEFF_C_RUN_2)
            * self.weight
            / self.M_IN_KM
            * (self.duration * 60)
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_C_WALK_1 = 0.035
    COEFF_C_WALK_2 = 0.029

    def __init__(
        self, action: int, duration: float, weight: float, height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = (
            self.COEFF_C_WALK_1 * self.weight
            + (self.get_mean_speed() ** 2 // self.height)
            * self.COEFF_C_WALK_2
            * self.weight
        ) * (self.duration * 60)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        mean_speed = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )
        return mean_speed

    def get_spent_calories(self) -> float:
        calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return calories


PROGRESS: dict = {
    "RUN": Running,
    "WLK": SportsWalking,
    "SWM": Swimming,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in PROGRESS:
        raise NotImplementedError("Ошибка типа тренировки")
    return PROGRESS[workout_type](*data)


def main(training: Training) -> str:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
