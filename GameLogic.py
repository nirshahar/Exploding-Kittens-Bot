from enum import ENUM, unique, auto
from typing import List
import random


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

    def peek(self, num_cards_peeked: int) -> List[CardType]:
        num_cards_peeked = min(num_cards_peeked, len(self.cards))

        return [self.cards[-i-1] for i in range(num_cards_peeked)]

    def shuffle(self):
        random.shuffle(self.cards)


class Hand(object):

    def __init__(self, deck: Deck, num_defuses: int = 1, cards: List[CardType] = []):
        self.deck = deck
        self.cards = cards

        for _ in range(num_defuses):
            self.cards.append(CardType.DEFUSE)

    def __getitem__(self, idx: int) -> CardType:
        return self.cards[idx]


class Game(object):

    def __init__(self,
                 num_players: int,
                 num_exploding: int,
                 num_defuse: int = 6,
                 num_future: int = 5,
                 num_shuffle: int = 4,
                 num_favor: int = 4,
                 num_skip: int = 4,
                 num_attack: int = 4,
                 num_nope: int = 5,
                 num_normal: int = 20,
                 num_defuse_in_start: int = 1):

        assert num_defuse - num_players*num_defuse_in_start >= 0

        self.deck = Deck(num_exploding=num_exploding,
                         num_defuse=num_defuse - num_players*num_defuse_in_start,
                         num_future=num_future,
                         num_shuffle=num_shuffle,
                         num_favor=num_favor,
                         num_skip=num_skip,
                         num_attack=num_attack,
                         num_nope=num_nope,
                         num_normal=num_normal)

        self.players: List[Hand] = [Hand(self.deck, num_defuses=num_defuse_in_start)
                                    for _ in range(num_players)]

        self.cur_turn = 0
        self.number_of_turns_for_player = 1
        self.cards_played_this_turn = []

    def play_card(self, card_idx, player_idx=None):
        player_idx = player_idx if player_idx is not None else self.cur_turn

        player_hand = self.players[player_idx]
        assert card_idx < len(player_hand)
        player_card = player_hand[card_idx]

        if player_card == CardType.SHUFFLE:
            self.deck.shuffle()
        elif player_card == CardType.SEE_FUTURE:
            # TODO
            print(self.deck.peek(3))
        elif player_card == CardType.SKIP:
            self.finish_turn()
        elif player_card == CardType.ATTACK:
            self.finish_turn()
            self.number_of_turns_for_player += 1
        elif player_card == CardType.FAVOR:
            pass  # TODO
        elif player_card == CardType.DEFUSE:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NOPE:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_BEARD:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_MELON:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_TACO:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_POTATO:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_RAINBOW:  # what do we do here?
            pass  # TODO

        self.cards_played_this_turn.append(player_card)

    def finish_turn(self):
        # Draw a card. If it is an exploding kitten, then either use a defuse or the player loses
        drawn_card = self.deck.hand_card()
        player_hand = self.players[self.cur_turn]

        if drawn_card == CardType.EXPLODING:
            if CardType.DEFUSE in player_hand:
                player_hand.remove(CardType.DEFUSE)
                # TODO place back the defuse in the spot the player chooses
                self.deck.append(CardType.EXPLODING)

            else:
                self.players.pop(self.cur_turn)
                print("Player exploded!")  # TODO send to discord the message

                if len(self.players) == 1:
                    print(f"Game ended! Player: {self.players[0]} has won!")
        else:
            player_hand.append(drawn_card)

        self.cards_played_this_turn = []
        self.number_of_turns_for_player -= 1

        if self.number_of_turns_for_player <= 0:
            self.number_of_turns_for_player = 1
            self.cur_turn = (self.cur_turn + 1) % len(self.players)
