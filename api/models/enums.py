from enum import Enum


class GenreEnum(str, Enum):
    excursion = 'экскурсия'
    master_class = 'мастер-класс'
    spectacle = 'спектакль'
    exhibition = 'выставка'
    interactive_lesson = 'интерактивное занятие'
    concert = 'концерт'
    genealogy = 'мероприятие по генеалогии'
    lecture = 'лекция'
    creative_meeting = 'творческая встреча'
    festival = 'фестиваль'
    artist_talk = 'Артист-ток'
    film_screening = 'кинопоказ'


class VisitorAgeEnum(str, Enum):
    adults = 'взрослые'
    teenagers = 'подростки'
    kids = 'дети'


class AreaEnum(str, Enum):
    cachka_house = 'Дом Качки'
    metenkov_house = 'Дом Метенкова'
    l52 = 'Креативный кластер "Л52"'
    water_tower = 'Водонапорная башня на плотинке'
    makletsky_house = 'Дом Маклецкого'
    memorial_complex = 'Мемориальный комплекс'
