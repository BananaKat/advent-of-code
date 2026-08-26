# Advent Of Code 2023 - Day 20
# Solving https://adventofcode.com/2023/day/20
from pprint import pprint


# Part 1
def pulse_flip_flop(modules, name, pulse):
    if pulse == 'Low':
        state = modules[name][2]
        modules[name][2] = 'On' if state == 'Off' else 'Off'
        modules[name][3] = pulse
    return modules


def pulse_destination_modules(modules, send_to):
    # Push button
    for name in send_to:
        pulse = 'Low'
        modules = pulse_flip_flop(modules, name, pulse)
        lows += 1
    # Pulse 'On' flip-flops
    for module in modules:
        state = modules[name][2]
        if state == 'On':

def push_broad_cast_button(broadcasts, modules):
    cycles = 1
    lows = 0
    highs = 0
    i = 0
    while i < cycles:
        send_to = broadcasts
        modules, send_to = pulse_destination_modules(modules, send_to)

        # Check if all off
        # If all off, increment i

    return lows, highs


def total_pulses_sent(file):
    modules = {}
    with open(file) as input_file:
        broadcasts = input_file.readline().rstrip().split(
            ' -> ')[1].split(', ')
        for line in input_file.readlines():
            name, destinations = line.rstrip().split(' -> ')
            destinations = [dest for dest in destinations.split(', ')]
            state = 'Off'
            previous_pulse = None
            modules[name[1:]] = [name[0], destinations, state, previous_pulse]
    print(broadcasts)
    pprint(modules)
    lows, highs = push_broad_cast_button(broadcasts, modules)
    print(f'Product of Low and High Pulses = {lows * highs}')
    return lows * highs


total_pulses_sent("test_1.txt")
