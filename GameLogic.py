from enum import ENUM, unique, auto
from typing import List


@unique
class CardType(ENUM):
    EXPLODING = auto(),
    DEFUSE = auto(),
    SEE_FUTURE = auto(),
    NOPE = auto(),
    ATTACK = auto(),
    SKIP = auto(),
    FAVOR = auto(),
    SHUFFLE = auto(),
    NORMAL_MELON = auto(),
    NORMAL_BEARD = auto(),
    NORMAL_POTATO = auto(),
    NORMAL_TACO = auto(),
    NORMAL_RAINBOW = auto()


# class Card(object):

#     def __init__(self, type: CardTypes, normal_type: NormalCardTypes = None):
#         self.type = type

#         if type == CardTypes.NORMAL:
#             assert normal_type is not None

#             self.normal_type = normal_type


class Deck(object):

    def __init__(self,
                 num_exploding: int,
                 num_defuse: int,
                 num_future: int,
                 num_shuffle: int,
                 num_favor: int,
                 num_skip: int,
                 num_attack: int,
                 num_nope: int,
                 num_normal: int):

        assert num_normal % 5 == 0
        self.cards = []

        for _ in range(num_exploding):
            self.cards.append(CardType.EXPLODING)

        for _ in range(num_defuse):
            self.cards.append(CardType.DEFUSE)

        for _ in range(num_future):
            self.cards.append(CardType.SEE_FUTURE)

        for _ in range(num_shuffle):
            self.card.append(CardType.SHUFFLE)

        for _ in range(num_favor):
            self.card.append(CardType.FAVOR)

        for _ in range(num_skip):
            self.card.append(CardType.SKIP)

        for _ in range(num_attack):
            self.card.append(CardType.ATTACK)

        for _ in range(num_nope):
            self.card.append(CardType.NOPE)

        normal_cnt = num_normal // 5

        for _ in range(normal_cnt):
            self.card.append(CardType.NORMAL_BEARD)
            self.card.append(CardType.NORMAL_MELON)
            self.card.append(CardType.NORMAL_POTATO)
            self.card.append(CardType.NORMAL_RAINBOW)
            self.card.append(CardType.NORMAL_TACO)

    def hand_card(self) -> CardType:
        assert len(self.cards) > 0

        card = self.cards[-1]
        self.cards.pop()

        return card

    """
    Warning: Will enter an infinite loop if deck has exploding kittens but not enough other cards!
    Warning: If encounters an exploding kitten, it will place at the bottom of the pile
    Note: Call only once at setup!
    """

    def hand_non_exploding_cards(self, num_cards: int) -> List[CardType]:
        handed_cards = []
        while len(handed_cards) < num_cards:
            new_handed_cards = self.hand_cards(num_cards - len(handed_cards))

            for card in new_handed_cards:
                if card.type != CardType.EXPLODING:
                    handed_cards.extend(card)
                else:
                    self.cards.insert(0, CardType.EXPLODING)

        return handed_cards


def Hand(object):

    def __init__(self, deck: Deck, cards: List[CardType] = [], num_defuses: int = 1):
        self.deck = deck
        self.cards = cards

        for _ in range(num_defuses):
            self.cards.append(CardType.DEFUSE)
