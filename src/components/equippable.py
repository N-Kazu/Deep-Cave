class Equippable:
    def __init__(self, slot, power_daice=0, daice=0, base_power=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.power_daice = power_daice
        self.daice = daice
        self.base_power = base_power
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus