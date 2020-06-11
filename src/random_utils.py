from random import randint

# level以上のdungeon_levelの時にValueを返す
def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0

# Valueの総合計値から乱数random_chanceを取って、random_chanceがどのvalueに存在するのか特定し、その要素数choiceを返す
def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        # 現在のValueを加算していく
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1

#引数をKeysとValuesに分解し、「random_choice_index(chances)」で決定された要素で返す
def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]