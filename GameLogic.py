import asyncio
from enum import Enum, unique, auto
from typing import List
import random

eventDone = False
eventValue = None
isHandEvent = True


def set_event(val):
    global eventDone
    global eventValue

    eventValue = val
    eventDone = True


def is_event_available():
    global eventDone

    return eventDone


def get_event_value():
    global eventDone
    global eventValue

    if eventDone:
        val = eventValue
        eventDone = False

        return val


def set_hand_event(val):
    global isHandEvent

    isHandEvent = val


def is_hand_event_active():
    global isHandEvent

    return isHandEvent


@unique
class CardType(Enum):
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
    NORMAL_RAINBOW = auto(),

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        if self == CardType.SHUFFLE:
            return "❔"
        elif self == CardType.SKIP:
            return "⏭️"
        elif self == CardType.EXPLODING:
            return "💣"
        elif self == CardType.SEE_FUTURE:
            return "👁️"
        elif self == CardType.NOPE:
            return "🛑"
        elif self == CardType.ATTACK:
            return "⚡"
        elif self == CardType.DEFUSE:
            return "✅"
        elif self == CardType.FAVOR:
            return "🖤"
        elif self == CardType.NORMAL_BEARD:
            return "🧔"
        elif self == CardType.NORMAL_MELON:
            return "🍈"
        elif self == CardType.NORMAL_POTATO:
            return "🥔"
        elif self == CardType.NORMAL_RAINBOW:
            return "🌈"
        elif self == CardType.NORMAL_TACO:
            return "🌮"


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
            self.cards.append(CardType.SHUFFLE)

        for _ in range(num_favor):
            self.cards.append(CardType.FAVOR)

        for _ in range(num_skip):
            self.cards.append(CardType.SKIP)

        for _ in range(num_attack):
            self.cards.append(CardType.ATTACK)

        for _ in range(num_nope):
            self.cards.append(CardType.NOPE)

        normal_cnt = num_normal // 5

        for _ in range(normal_cnt):
            self.cards.append(CardType.NORMAL_BEARD)
            self.cards.append(CardType.NORMAL_MELON)
            self.cards.append(CardType.NORMAL_POTATO)
            self.cards.append(CardType.NORMAL_RAINBOW)
            self.cards.append(CardType.NORMAL_TACO)

        self.shuffle()

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
            card = self.hand_card()

            if card != CardType.EXPLODING:
                handed_cards.append(card)
            else:
                self.cards.insert(0, card)
        return handed_cards

    def peek(self, num_cards_peeked: int) -> List[CardType]:
        num_cards_peeked = min(num_cards_peeked, len(self.cards))

        return [self.cards[-i-1] for i in range(num_cards_peeked)]

    def shuffle(self):
        random.shuffle(self.cards)


class Hand(object):

    def __init__(self, deck: Deck, num_defuses: int = 1):
        self.deck = deck
        self.cards = []

        for _ in range(num_defuses):
            self.cards.append(CardType.DEFUSE)

    def __getitem__(self, idx: int) -> CardType:
        return self.cards[idx]

    def __iter__(self):
        return iter(self.cards)


class Player(object):

    def __init__(self, member, channel):
        self.member = member
        self.channel = channel
        self.hand: Hand = None
        self.game: Game = None

        self.normals_played_this_turn = set()

    def __str__(self) -> str:
        return self.member.name

    async def clear_channel(self):
        await self.channel.purge()

    async def send_message(self, message):
        return await self.channel.send(message)

    async def show_hand(self):
        await self.clear_channel()
        cards = []
        card_indices = {}

        for card in self.hand.cards:
            if card in card_indices:
                _, v = cards[card_indices[card]]
                cards[card_indices[card]] = (card, v + 1)
            else:
                cards.append((card, 1))
                card_indices.update({card: len(cards) - 1})

        message = await self.channel.send("\n".join(str(card) + " x " + str(repetitions) for card, repetitions in cards))

        seen_cards = set()
        for card in self.hand.cards:
            if card is not CardType.DEFUSE and card not in seen_cards:
                seen_cards.add(card)
                await message.add_reaction(repr(card))
        await message.add_reaction("🃏")

    async def create_choice(self, choices):
        set_hand_event(False)

        await self.clear_channel()
        await self.channel.send("\n".join(str(choice) + ": " + str(i + 1) for i, choice in enumerate(choices)))

        while not is_event_available():
            await asyncio.sleep(0.2)

        chosen_val = get_event_value()

        print(chosen_val)

        set_hand_event(True)

        return chosen_val

    async def play_card(self, card_idx):
        cards = self.hand.cards
        assert card_idx < len(cards)

        player_card = cards[card_idx]
        cards.pop(card_idx)

        if player_card == CardType.SHUFFLE:
            self.game.deck.shuffle()
        elif player_card == CardType.SEE_FUTURE:
            # TODO
            print(self.game.deck.peek(3))
        elif player_card == CardType.SKIP:
            await self.game.finish_turn(draw=False)
        elif player_card == CardType.ATTACK:
            await self.game.finish_turn(draw=False)
            self.game.number_of_turns_for_player += 1
        elif player_card == CardType.FAVOR:

            choices = [
                player for player in self.game.players if player != self]
            choice_idx = await self.create_choice(choices)

            chosen_player = choices[choice_idx]

            self.game.cur_active_player = chosen_player

            favor_card_choices = [card for card in chosen_player.hand.cards]
            favor_card_choice_idx = await chosen_player.create_choice(favor_card_choices)

            chosen_card = favor_card_choices[favor_card_choice_idx]

            chosen_player.hand.cards.pop(favor_card_choice_idx)
            self.hand.cards.append(chosen_card)

        elif player_card == CardType.NOPE:  # what do we do here?
            pass  # TODO
        elif player_card == CardType.NORMAL_BEARD or CardType.NORMAL_MELON or CardType.NORMAL_TACO or CardType.NORMAL_POTATO or CardType.NORMAL_RAINBOW:
            if player_card in self.normals_played_this_turn:
                self.normals_played_this_turn.discard(player_card)
                print("PLAYED TWO NORMALS OF THE SAME TYPE!")
                choices = [
                    player for player in self.game.players if player != self]

                choice_idx = await self.create_choice(choices)
                player_choice = choices[choice_idx]

                if len(player_choice.hand.cards) > 0:
                    rnd_card_idx = random.randint(
                        0, len(player_choice.hand.cards))

                    self.hand.cards.append(player_choice.hand[rnd_card_idx])
                    player_choice.hand.cards.pop(rnd_card_idx)

            else:
                self.normals_played_this_turn.add(player_card)


class Game(object):

    def __init__(self,
                 players: List[Player],
                 num_exploding: int,
                 num_starting_cards: int = 7,
                 num_defuse: int = 6,
                 num_future: int = 5,
                 num_shuffle: int = 4,
                 num_favor: int = 4,
                 num_skip: int = 4,
                 num_attack: int = 4,
                 num_nope: int = 5,
                 num_normal: int = 20,
                 num_defuse_in_start: int = 1):

        num_players = len(players)

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

        self.players = players

        self.cur_turn = 0
        self.cur_active_player = self.players[self.cur_turn]
        self.number_of_turns_for_player = 1

        for player in self.players:
            hand = Hand(self.deck, num_defuses=num_defuse_in_start)
            player.hand = hand
            player.game = self

            hand.cards.extend(self.deck.hand_non_exploding_cards(
                num_starting_cards - num_defuse_in_start))

    async def finish_turn(self, draw=True):
        if draw:
            # Draw a card. If it is an exploding kitten, then either use a defuse or the player loses
            drawn_card = self.deck.hand_card()
            player = self.players[self.cur_turn]

            if drawn_card == CardType.EXPLODING:
                if CardType.DEFUSE in player.hand.cards:
                    player.hand.cards.remove(CardType.DEFUSE)

                    choices = ["top", "second from top", "third from top",
                               "fourth from top", "fifth from top"]

                    if len(self.deck.cards) < 5:
                        choices = choices[:len(self.deck.cards)]
                        choices_map = {i: -i-1 for i in range(len(choices))}
                    else:
                        choices_map = {i: -i-1 for i in range(len(choices))}
                        choices.append("bottom")
                        choices_map.update({len(choices) - 1: 0})

                    choices.append("random")
                    choices_map.update(
                        {len(choices) - 1: random.randint(0, len(self.deck.cards) - 1)})

                    choice_idx = await player.create_choice(choices)
                    chosen_return_idx = choices_map[choice_idx]

                    self.deck.cards.insert(choice_idx, chosen_return_idx)

                else:
                    self.players.pop(self.cur_turn)
                    # TODO send to discord the message
                    print("Player exploded!")

                    if len(self.players) == 1:
                        print(
                            f"Game ended! Player: {self.players[0]} has won!")
            else:
                player.hand.cards.append(drawn_card)

        player = self.players[self.cur_turn]
        player.normals_played_this_turn.clear()

        self.number_of_turns_for_player -= 1

        if self.number_of_turns_for_player <= 0:
            self.number_of_turns_for_player = 1
            self.cur_turn = (self.cur_turn + 1) % len(self.players)
            self.cur_active_player = self.players[self.cur_turn]
