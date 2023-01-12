from dataclasses import dataclass
from typing import List, Union


class InvalidInputDataError(Exception):
    """Исключение, возникшее из-за ошибок в полученных данных от датчиков.

    Args:
        err (Union[KeyError, TypeError]): Объект класса ошибки.
        message (str): Обяснение ошибки.
    """

    def __init__(
        self,
        err: Union[KeyError, TypeError],
        message: str = 'Полученные данные содержат ошибку',
    ) -> Exception:
        self.err = err
        self.message = message
        super().__init__(
            self.err,
            self.message,
        )


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Формирует информацию о тренировке.

        Returns:
            Строку, которая содержит: текущий тип тренировки,
            длительность тренировки в часах, дистанция в км., среднюю скорость
            во время тренировки в км/ч и количество затраченных калорий.
        """
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки.

    Args:
        action (int): Количество совершённых действий.
        duration (float): Длительность тренировки в часах.
        weight (float): Вес спортсмена в кг.
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

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
        """Формирует пройденную дистанцию в км.

        Returns:
            Значение дистанции в км.
        """
        return self.action * self.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Формирует среднюю скорость движения.

        Returns:
            Значение средней скорости во время тренировки в км/ч.
        """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Формирует количество затраченных калорий.

        Raises:
            NotImplementedError: Если данный метод не переопределен в
            классах-наследниках.
        """
        raise NotImplementedError(
            'Необходимо переопределить метод get_spent_calories()',
        )

    def show_training_info(self) -> InfoMessage:
        """Формирует информационное сообщение о выполненной тренировке.

        Returns:
            Объект класса сообщения.
        """
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег.

    Args:
        action (int): Количество совершённых действий.
        duration (float): Длительность тренировки в часах.
        weight (float): Вес спортсмена в кг.
    """

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Формирует количество затраченных калорий.

        Returns:
            Значение количества затраченных калорий во время
            тренировки.
        """
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / Training.M_IN_KM
            * self.duration
            * Training.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Args:
        action (int): Количество совершённых действий.
        duration (float): Длительность тренировки в часах.
        weight (float): Вес спортсмена в кг.
        height (float): Рост спортсмена в см.
    """

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278  # коэффициент для перевода км/ч в м/с
    CM_IN_M = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(
            action,
            duration,
            weight,
        )
        self.height = height

    def get_spent_calories(self) -> float:
        """Формирует количество затраченных калорий.

        Returns:
            Значение количества затраченных калорий во время
            тренировки.
        """
        return (
            (
                self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (
                    (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight
            )
            * self.duration
            * Training.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание.

    Args:
        action (int): Количество совершённых действий.
        duration (float): Длительность тренировки в часах.
        weight (float): Вес спортсмена в кг.
        length_pool (float): Длина бассейна в метрах.
        count_pool (float):  Сколько раз пользователь переплыл бассейн.
    """

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_MULTIPLIER = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(
            action,
            duration,
            weight,
        )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Формирует среднюю скорость движения.

        Returns:
            Значение средней скорости во время тренировки в км/ч.
        """
        return (
            self.length_pool
            * self.count_pool
            / Training.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        """Формирует количество затраченных калорий.

        Returns:
            Значение количества затраченных калорий во время
            тренировки.
        """
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MULTIPLIER
            * self.weight
            * self.duration
        )


WORKOUT_CODES = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: List[float]) -> Training:
    """Считывает данные полученные от датчиков.

    Args:
        workout_type (str): Кодовое обозначение прошедшей тренировки.
        data (List[float]): Список показателей, полученных от датчиков
            устройства.

    Returns:
        Объект соответствующего класса, передав ему на вход
        параметры, полученные во втором аргументе.
    """
    try:
        return WORKOUT_CODES[workout_type](*data)
    except (KeyError, TypeError) as err:
        raise InvalidInputDataError(err)


def main(training: Training) -> None:
    """Главная функция.

    Args:
        training (Training): Объект класса тренировки.

    Returns:
        Информацию на экран о тренировке и её показателях.
    """
    return print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
