# Advent Of Code 2023 - Day 5
# Solving https://adventofcode.com/2023/day/5
from pprint import pprint


# Part 1
def find_in_map(map, number):
    for item in map:
        destination_range = item[0]
        source_range_start = item[1]
        range_length = item[2]
        if number >= source_range_start and number < source_range_start + range_length:
            difference_from_source = number - source_range_start
            map_result = destination_range + difference_from_source
            return map_result
    return number


def lowest_location(file):
    lowest_location = None
    with open(file) as input_file:
        maps = input_file.read().split('\n\n')
        seeds = [int(n) for n in maps[0].split()[1:]]
        seed_to_soil_map = [[int(n) for n in line.split()]
                            for line in maps[1].split('\n')[1:] if line]
        soil_to_fert_map = [[int(n) for n in line.split()]
                            for line in maps[2].split('\n')[1:] if line]
        fert_to_water_map = [[int(n) for n in line.split()]
                             for line in maps[3].split('\n')[1:] if line]
        water_to_light_map = [[int(n) for n in line.split()]
                              for line in maps[4].split('\n')[1:] if line]
        light_to_temp_map = [[int(n) for n in line.split()]
                             for line in maps[5].split('\n')[1:] if line]
        temp_to_humid_map = [[int(n) for n in line.split()]
                             for line in maps[6].split('\n')[1:] if line]
        humid_to_location_map = [[int(n) for n in line.split()]
                                 for line in maps[7].split('\n')[1:] if line]
        for seed in seeds:
            soil = find_in_map(seed_to_soil_map, seed)
            fert = find_in_map(soil_to_fert_map, soil)
            water = find_in_map(fert_to_water_map, fert)
            light = find_in_map(water_to_light_map, water)
            temp = find_in_map(light_to_temp_map, light)
            humid = find_in_map(temp_to_humid_map, temp)
            location = find_in_map(humid_to_location_map, humid)
            if lowest_location:
                if location < lowest_location:
                    lowest_location = location
            else:
                lowest_location = location
    pprint(f'Lowest Location = {lowest_location}')
    return lowest_location


lowest_location("puzzle_input.txt")
# Answer: 51580674


# Part 2
def seperate_into_pairs(input_list):
    paired_list = []
    j = 1
    for i in range(0, len(input_list) - 1, 2):
        paired_list.append((input_list[i], input_list[j]))
        j += 2
    return paired_list


def find_source_in_map_given_destination(map, destination):
    for item in map:
        destination_range = item[0]
        source_range_start = item[1]
        range_length = item[2]
        if destination >= destination_range and destination < destination_range + range_length:
            difference_from_source = destination - destination_range
            source = source_range_start + difference_from_source
            return source
    return destination


def new_lowest_location(file):
    lowest_location = 0
    seed_found = False
    with open(file) as input_file:
        maps = input_file.read().split('\n\n')
        seeds = [int(n) for n in maps[0].split()[1:]]
        seed_pairs = seperate_into_pairs(seeds)
        seed_to_soil_map = [[int(n) for n in line.split()]
                            for line in maps[1].split('\n')[1:] if line]
        soil_to_fert_map = [[int(n) for n in line.split()]
                            for line in maps[2].split('\n')[1:] if line]
        fert_to_water_map = [[int(n) for n in line.split()]
                             for line in maps[3].split('\n')[1:] if line]
        water_to_light_map = [[int(n) for n in line.split()]
                              for line in maps[4].split('\n')[1:] if line]
        light_to_temp_map = [[int(n) for n in line.split()]
                             for line in maps[5].split('\n')[1:] if line]
        temp_to_humid_map = [[int(n) for n in line.split()]
                             for line in maps[6].split('\n')[1:] if line]
        humid_to_location_map = [[int(n) for n in line.split()]
                                 for line in maps[7].split('\n')[1:] if line]
        while not seed_found:
            humid = find_source_in_map_given_destination(
                humid_to_location_map, lowest_location)
            temp = find_source_in_map_given_destination(
                temp_to_humid_map, humid)
            light = find_source_in_map_given_destination(
                light_to_temp_map, temp)
            water = find_source_in_map_given_destination(
                water_to_light_map, light)
            fert = find_source_in_map_given_destination(
                fert_to_water_map, water)
            soil = find_source_in_map_given_destination(soil_to_fert_map, fert)
            seed = find_source_in_map_given_destination(seed_to_soil_map, soil)
            for possible_seed in seed_pairs:
                possible_seed_start = possible_seed[0]
                possible_seed_range = possible_seed[1]
                possible_seed_end = possible_seed_start + possible_seed_range
                if seed >= possible_seed_start and seed < possible_seed_end:
                    pprint(f'New Lowest Location = {lowest_location}')
                    return lowest_location
            lowest_location += 1


new_lowest_location("puzzle_input.txt")
# Answer: 99751240 | [Finished in 1205.8s]
# Note 1: My Part 2 solution has an absurdly long run time
#       1205.2secs = ~20.1mins
# Note 2: Answer can be different for different users
#         E.g. Some users had a result ~10 million
#         But my problem's answer is almost 100 million
