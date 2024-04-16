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
    cachka_house = 'дом Качки'
    metenkov_house = 'дом Метенкова'
    l52 = 'креативный кластер "Л52"'
    water_tower = 'водонапорная башня на плотинке'
    makletsky_house = 'дом Маклецкого'
    memorial_complex = 'мемориальный комплекс'