# Advent Of Code 2023 - Day 7
# Solving https://adventofcode.com/2023/day/7
import collections


# Part 1
def determine_hand_type(hand):
    types = {
        (1, 1): 'High Card',
        (2, 1): 'One Pair',
        (2, 2): 'Two Pair',
        (3, 1): 'Three of a Kind',
        (4, 1): 'Four of a Kind',
        (3, 2): 'Full House',
        (5,): 'Five of a Kind'
    }
    counted_cards = collections.Counter(hand)
    two_most_common, counts = zip(*counted_cards.most_common(2))
    return types[counts]


def sort_types(hand_bid_pairs):
    TYPE_SORT_ORDER = {
        'High Card': 0,
        'One Pair': 1,
        'Two Pair': 2,
        'Three of a Kind': 3,
        'Full House': 4,
        'Four of a Kind': 5,
        'Five of a Kind': 6
    }
    CARD_SORT_ORDER = ['2', '3', '4', '5', '6',
                       '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    return sorted(hand_bid_pairs, key=lambda val: (TYPE_SORT_ORDER[val[2]], [CARD_SORT_ORDER.index(card) for card in val[0]]))


def total_camel_cards_winnings(file):
    total_winnings = 0
    with open(file) as input_file:
        hand_bid_pairs = [line.split() for line in input_file]
        for hand_bid in hand_bid_pairs:
            hand_bid.append(determine_hand_type(hand_bid[0]))
        hand_bid_pairs = sort_types(hand_bid_pairs)
        for rank in range(len(hand_bid_pairs)):
            total_winnings += int(hand_bid_pairs[rank][1]) * (rank + 1)
    print(f'Total Camel Cards Winnings = {total_winnings}')
    return total_winnings


total_camel_cards_winnings("puzzle_input.txt")
# Answer: 250898830


# Part 2
def determine_hand_type_with_joker(hand):
    types = {
        (1, 1): 'High Card',
        (2, 1): 'One Pair',
        (2, 2): 'Two Pair',
        (3, 1): 'Three of a Kind',
        (4, 1): 'Four of a Kind',
        (3, 2): 'Full House',
        (5, 0): 'Five of a Kind'
    }
    counted_cards_excluding_joker = collections.Counter(
        card for card in hand if card != 'J')
    jokers = hand.count('J')
    counts = [count for card,
              count in counted_cards_excluding_joker.most_common(2)]
    while len(counts) != 2:
        counts.append(0)
    counts[0] += jokers
    return types[tuple(counts)]


def sort_types_with_joker(hand_bid_pairs):
    TYPE_SORT_ORDER = {
        'High Card': 0,
        'One Pair': 1,
        'Two Pair': 2,
        'Three of a Kind': 3,
        'Full House': 4,
        'Four of a Kind': 5,
        'Five of a Kind': 6
    }
    CARD_SORT_ORDER = ['J', '2', '3', '4', '5', '6',
                       '7', '8', '9', 'T', 'Q', 'K', 'A']
    return sorted(hand_bid_pairs, key=lambda val: (TYPE_SORT_ORDER[val[2]], [CARD_SORT_ORDER.index(card) for card in val[0]]))


def total_camel_cards_winnings_with_jokers(file):
    total_winnings = 0
    with open(file) as input_file:
        hand_bid_pairs = [line.split() for line in input_file]
        for hand_bid in hand_bid_pairs:
            hand_bid.append(determine_hand_type_with_joker(hand_bid[0]))
        hand_bid_pairs = sort_types_with_joker(hand_bid_pairs)
        for rank in range(len(hand_bid_pairs)):
            total_winnings += int(hand_bid_pairs[rank][1]) * (rank + 1)
    print(f'Total Camel Cards Winnings With Jokers = {total_winnings}')
    return total_winnings


total_camel_cards_winnings_with_jokers("puzzle_input.txt")
# Answer: 252127335
