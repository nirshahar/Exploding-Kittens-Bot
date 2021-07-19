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


def transform_to_int(emoji):
    if emoji == '1️⃣':
        return 0
    elif emoji == '2️⃣':
        return 1
    elif emoji == '3️⃣':
        return 2
    elif emoji == '4️⃣':
        return 3
    elif emoji == '5️⃣':
        return 4
    elif emoji == '6️⃣':
        return 5
    elif emoji == '7️⃣':
        return 6
    elif emoji == '8️⃣':
        return 7
    elif emoji == '9️⃣':
        return 8
    elif emoji == '9️⃣':
        return 8
    elif emoji == '9️⃣':
        return 8
    elif emoji == '9️⃣':
        return 8
    elif emoji == '9️⃣':
        return 8
    elif emoji == '9️⃣':
        return 8
    elif emoji == '🔟':
        return 9
    elif emoji == '🌲':
        return 10
    elif emoji == '🕛':
        return 11
    elif emoji == '🕐':
        return 12
    elif emoji == '🕑':
        return 13
    elif emoji == '🕒':
        return 14
    elif emoji == '🕓':
        return 15
    elif emoji == '🕓':
        return 16
    else:
        print("u stoopid")
        return None


def transform_int_to_emoji(i):
    if i == 0:
        return '1️⃣'
    elif i == 1:
        return '2️⃣'
    elif i == 2:
        return '3️⃣'
    elif i == 3:
        return '4️⃣'
    elif i == 4:
        return '5️⃣'
    elif i == 5:
        return '6️⃣'
    elif i == 6:
        return '7️⃣'
    elif i == 7:
        return '8️⃣'
    elif i == 8:
        return '9️⃣'
    elif i == 9:
        return '🔟'
    elif i == 10:
        return '🌲'
    elif i == 11:
        return '🕛'
    elif i == 12:
        return '🕐'
    elif i == 13:
        return '🕑'
    elif i == 14:
        return '🕒'
    elif i == 15:
        return '🕓'
    elif i == 16:
        return '🕓'
    else:
        print("u stoopid")
        return None


FINISH_TURN = "finish turn"


def transform_to_card_type(emoji):
    if emoji == "❔":
        return CardType.SHUFFLE
    elif emoji == "⏭️":
        return CardType.SKIP
    elif emoji == "💣":
        return CardType.EXPLODING
    elif emoji == "👁️":
        return CardType.SEE_FUTURE
    elif emoji == "🛑":
        return CardType.NOPE
    elif emoji == "⚡":
        return CardType.ATTACK
    elif emoji == "🖤":
        return CardType.FAVOR
    elif emoji == "🧔":
        return CardType.NORMAL_BEARD
    elif emoji == "🍈":
        return CardType.NORMAL_MELON
    elif emoji == "🥔":
        return CardType.NORMAL_POTATO
    elif emoji == "🌈":
        return CardType.NORMAL_RAINBOW
    elif emoji == "🌮":
        return CardType.NORMAL_TACO
    elif emoji == "🃏":
        return FINISH_TURN
    else:
        print("yoo stoopid")
        return None


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
        self.hand_message = None
        self.existing_reactions = set()

        self.normals_played_this_turn = set()

    def __str__(self) -> str:
        return self.member.name

    async def clear_channel(self):
        await self.channel.purge()

    async def send_message(self, message):
        return await self.channel.send(message)

    async def show_hand(self):
        if self.hand_message is None:
            await self.clear_channel()
            self.hand_message = await self.send_message("Starting!")

        cards = []
        card_indices = {}

        for card in self.hand.cards:
            if card in card_indices:
                _, v = cards[card_indices[card]]
                cards[card_indices[card]] = (card, v + 1)
            else:
                cards.append((card, 1))
                card_indices.update({card: len(cards) - 1})

        message_content = "\n".join(
            repr(card) + "  " + str(card) + " " + " x " + str(repetitions) for card, repetitions in cards)

        if self.game.players[self.game.cur_turn] == self:
            message_content = f"You have {self.game.number_of_turns_for_player} turns left\n\n" + \
                message_content + "\n\n Press the 'joker' card to end your turn and draw a card"
        else:
            message_content = "Its not your turn currently. Please wait patiently\n\n" + message_content

        print("sending message: \n\n" + message_content +
              "\n\n to player " + self.member.name)
        await self.hand_message.edit(content=message_content)

        emojis = []
        for card in self.hand.cards:
            if card is not CardType.DEFUSE and card not in emojis:
                emojis.append(card)

        for card in emojis:
            if card not in self.existing_reactions:
                self.existing_reactions.add(card)
                await self.hand_message.add_reaction(repr(card))

        removed_reactions = []
        for reaction in self.existing_reactions:
            if reaction != "🃏" and reaction not in emojis:
                removed_reactions.append(reaction)
                await self.hand_message.remove_reaction(repr(reaction), self.hand_message.author)

        for reaction in removed_reactions:
            self.existing_reactions.remove(reaction)

        if "🃏" not in self.existing_reactions:
            self.existing_reactions.add("🃏")
            await self.hand_message.add_reaction("🃏")

    # async def show_hand(self):
    #     await self.clear_channel()
    #     cards = []
    #     card_indices = {}

    #     for card in self.hand.cards:
    #         if card in card_indices:
    #             _, v = cards[card_indices[card]]
    #             cards[card_indices[card]] = (card, v + 1)
    #         else:
    #             cards.append((card, 1))
    #             card_indices.update({card: len(cards) - 1})

    #     message = await self.channel.send("\n".join(str(card) + " x " + str(repetitions) for card, repetitions in cards) + "\n\n Press the 'joker' card to end your turn and draw a card")

    #     seen_cards = set()
    #     for card in self.hand.cards:
    #         if card is not CardType.DEFUSE and card not in seen_cards:
    #             seen_cards.add(card)
    #             await message.add_reaction(repr(card))
    #     await message.add_reaction("🃏")

    #     self.hand_message = message

    async def create_choice(self, choices):
        set_hand_event(False)

        await self.hand_message.edit(content="\n".join(str(choice) + ": " + transform_int_to_emoji(i) for i, choice in enumerate(choices)))
        await self.hand_message.clear_reactions()
        for i in range(len(choices)):
            await self.hand_message.add_reaction(transform_int_to_emoji(i))

        while not is_event_available():
            await asyncio.sleep(0.2)

        set_hand_event(True)

        chosen_val = get_event_value()
        print(chosen_val)

        await self.hand_message.clear_reactions()
        self.existing_reactions = set()

        await self.show_hand()

        return chosen_val

    async def delete_message(self, message):
        if message != self.hand_message:
            await message.delete()

    async def play_card(self, card_idx):
        cards = self.hand.cards
        assert card_idx < len(cards)

        player_card = cards[card_idx]
        cards.pop(card_idx)

        if player_card == CardType.SHUFFLE:
            self.game.deck.shuffle()
        elif player_card == CardType.SEE_FUTURE:
            # TODO
            await (await self.channel.send(self.game.deck.peek(3))).add_reaction("❌")
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

            self.game.cur_active_player = self.game.players[self.game.cur_turn]

            await chosen_player.show_hand()
            await self.show_hand()

        elif player_card == CardType.NOPE:  # what do we do here?
            await (await self.send_message("number of cards left: " + str(len(self.game.deck.cards)))).add_reaction("❌")
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
                    await player_choice.show_hand()

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
                 num_nope: int = 4,
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

    def kill(self, player: Player):
        print(player)
        idx = self.players.index(player)
        if self.cur_turn >= idx:
            self.cur_turn -= 1

        self.players.pop(idx)

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
                        choices = choices[:len(self.deck.cards) + 1]
                        choices_map = {i: -i-1 for i in range(len(choices))}
                    else:
                        choices_map = {i: -i-1 for i in range(len(choices))}
                        choices.append("bottom")
                        choices_map.update({len(choices) - 1: 0})

                    choices.append("random")
                    choices_map.update(
                        {len(choices) - 1: random.randint(0, len(self.deck.cards))})

                    choice_idx = await player.create_choice(choices)
                    chosen_return_idx = choices_map[choice_idx]

                    self.deck.cards.insert(
                        chosen_return_idx, CardType.EXPLODING)

                else:
                    self.players.pop(self.cur_turn)
                    self.kill(self.players[self.cur_active_player])
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
            last_player = self.cur_active_player

            self.number_of_turns_for_player = 1
            self.cur_turn = (self.cur_turn + 1) % len(self.players)
            self.cur_active_player = self.players[self.cur_turn]

            await last_player.show_hand()
            await self.cur_active_player.show_hand()
