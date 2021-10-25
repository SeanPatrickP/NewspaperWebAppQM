from enum import Enum

class Category(Enum):
    POLITICS = "Politics"
    SPORTS = "Sports"
    BEAUTY = "Beauty"
    NATURE = "Nature"

    @classmethod
    def choices(Category):
        # return Category.__members__.items()
        return list((i.name, i.value) for i in Category)

    @classmethod
    def optionsDict(Category):
        return dict((i.name, i.value) for i in Category)