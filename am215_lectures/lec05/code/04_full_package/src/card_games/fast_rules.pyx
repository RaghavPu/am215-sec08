# cython: language_level=3
def get_hand_value_cython(list hand):
    cdef int value = 0, num_aces = 0
    for card in hand:
        if card.rank in 'JQK': value += 10
        elif card.rank == 'A':
            num_aces += 1; value += 11
        else: value += int(card.rank)
    while value > 21 and num_aces:
        value -= 10; num_aces -= 1
    return value
