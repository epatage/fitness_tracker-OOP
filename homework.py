class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
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

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * Training.LEN_STEP / Training.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avr_speed: float = Training.get_distance(self) / self.duration

        return avr_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        object_message: InfoMessage = InfoMessage(self.__class__.__name__,
                                                  self.duration,
                                                  self.get_distance(),
                                                  self.get_mean_speed(),
                                                  self.get_spent_calories(),
                                                  )
        return object_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories = (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * Training.get_mean_speed(self)
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )

        return spend_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avr_speed: float = (
            Training.get_distance(self) / self.duration
        )
        return avr_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories = (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (Training.get_mean_speed(self)
                     * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
            )
            * (self.duration * self.MIN_IN_H)
        )

        return spend_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    BUFF_SPEED: float = 1.1
    CALORIES_COEFFICIENT = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * Swimming.LEN_STEP / Training.M_IN_KM

        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avr_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

        return avr_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spend_calories = (
            (self.get_mean_speed() + self.BUFF_SPEED)
            * self.CALORIES_COEFFICIENT * self.weight
            * self.duration
        )

        return spend_calories


def read_package(workout_type_: str, data_: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_code = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training_object: Training = training_code[workout_type_](*data_)

    return training_object


def main(training_: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info(training_)

    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
