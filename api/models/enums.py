from enum import Enum


class GenreEnum(str, Enum):
    excursion = 'Экскурсия'
    master_class = 'Мастер-класс'
    spectacle = 'Спектакль'
    exhibition = 'Выставка'
    interactive_lesson = 'Интерактивное занятие'
    concert = 'Концерт'
    genealogy = 'Мероприятие по генеалогии'
    lecture = 'Лекция'
    creative_meeting = 'Творческая встреча'
    festival = 'Фестиваль'
    artist_talk = 'Артист-ток'
    film_screening = 'Кинопоказ'


class VisitorAgeEnum(str, Enum):
    adults = 'Взрослые'
    teenagers = 'Подростки'
    kids = 'Дети'


class AreaEnum(str, Enum):
    cachka_house = 'Дом Качки'
    metenkov_house = 'Дом Метенкова'
    l52 = 'Креативный кластер "Л52"'
    water_tower = 'Водонапорная башня на плотинке'
    makletsky_house = 'Дом Маклецкого'
    memorial_complex = 'Мемориальный комплекс'


class TicketTypeEnum(str, Enum):
    adult = 'Взрослый билет'
    discount = 'Льготный билет'
    child = 'Детский билет'


class TagEventEnum(str, Enum):
    architecture = 'Архитектура'
    literature = 'Литература'
    science = 'Наука'
    history_of_ussr = 'История СССР'
    history_of_yekaterinburg = 'История Екатеринбурга'
    poetry = 'Поэзия'
    music = 'Музыка'
    philosophy = 'Философия'
    flora_and_fauna = 'Флора и фауны'
    handmade = 'Ручная работа'
    cinematography = 'Кинематограф'
    cartoons = 'Мультфильмы'
    tourism = 'Туризм'
    genealogy = 'Генеалогия'
    paleontology = 'Палеонтология'
    archaeology = 'Археология'
