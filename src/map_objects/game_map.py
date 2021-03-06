import libtcodpy as libtcod
from random import randint

from components.ai import BasicMonster
from components.equipment import Equipment,EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

from entity import Entity

from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.rectangle import Rect
from map_objects.tile import Tile

from random_utils import from_dungeon_level, random_choice_from_dict

from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # 部屋の大きさを決定
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # 部屋を作るマップ内の座標の決定
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" 型として部屋を作る
            new_room = Rect(x, y, w, h)

            # これまでの部屋と重複しているか
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # 部屋をMapに用意
                self.create_room(new_room)

                # 中心座標を取り込む
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # 最初の部屋なら真ん中にプレイヤーを配置
                    player.x = new_x
                    player.y = new_y
                else:
                    # 以降:
                    # 前の部屋との道を作成

                    # 前の部屋の中心座標を取得
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # 上四角で道を通すか下四角で道を通すか
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # 部屋としてリストに追加
                rooms.append(new_room)
                num_rooms += 1
        
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        # 一定数の大きさの部屋を作成
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        # 部屋のオブジェクト数の決定
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6],[6,12]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 6]], self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # [確率,発生する階数]
        monster_chances = {
            'goblin': from_dungeon_level([[80, 1], [60, 7], [30,10], [0, 14]], self.dungeon_level),
            'troll': from_dungeon_level([[15, 3], [60, 5], [80, 14]], self.dungeon_level),
            'ogre': from_dungeon_level([[15, 6], [30,10], [60,14]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 15,
            'bronze_sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[5, 6]], self.dungeon_level),
            'iron_sword': from_dungeon_level([[5, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4], [40,8]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6], [40,10]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2], [20,4]], self.dungeon_level)
        }

        # モンスターの数だけ実行
        for i in range(number_of_monsters):
            # 部屋のランダムな位置を取得
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # 得られた座標に既にEntitiyが存在しないならば
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'goblin':
                    fighter_component = Fighter(hp=25, defense=0, power=3, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'g', libtcod.desaturated_green, 'goblin', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                elif monster_choice == 'troll':
                    fighter_component = Fighter(hp=40, defense=2, power=4, xp=70)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True, fighter=fighter_component,
                                     render_order=RenderOrder.ACTOR, ai=ai_component)
                elif monster_choice == 'ogre':
                    fighter_component = Fighter(hp=70, defense=1, power=4, xp=120)
                    ai_component = BasicMonster()
                    equipment_component = Equipment()
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_daice=2, daice = 2, base_power=3)
                    club = Entity(0, 0, 'l', libtcod.sky, 'club', equippable=equippable_component)

                    monster = Entity(x, y, 'O', libtcod.darker_green, 'Ogre', blocks=True, fighter=fighter_component,
                                     equipment=equipment_component, render_order=RenderOrder.ACTOR, ai=ai_component)
                    monster.equipment.toggle_equip(club)

                entities.append(monster)
            else:
                i -=1
            
            # アイテムの数だけ実行
            for i in range(number_of_items):
                x = randint(room.x1 + 1, room.x2 - 1)
                y = randint(room.y1 + 1, room.y2 - 1)

                # 得られた座標に既にEntitiyが存在しないならば
                if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                    item_choice = random_choice_from_dict(item_chances)

                    if item_choice == 'healing_potion':
                        item_component = Item(use_function=heal, amount=40)
                        item = Entity(x, y, '!', libtcod.violet, 'Healing Potion', render_order=RenderOrder.ITEM,
                                      item=item_component)

                    elif item_choice == 'fireball_scroll':
                        item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                            'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                            damage=25, radius=3)
                        item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                    item=item_component)
                    
                    elif item_choice == 'confusion_scroll':
                        item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                            'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                        item = Entity(x, y, '#', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                    item=item_component)

                    elif item_choice == 'bronze_sword':
                        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_daice=2, daice =3, base_power=1)
                        item = Entity(x, y, '/', libtcod.sky, 'Bronze Sword', equippable=equippable_component)
                        
                    elif item_choice == 'shield':
                        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                        item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)

                    elif item_choice == 'iron_sword':
                        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_daice=4, daice =3, base_power=2)
                        item = Entity(x, y, '/', libtcod.sky, 'Iron Sword', equippable=equippable_component)
                        
                    else:
                        item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5)
                        item = Entity(x, y, '#', libtcod.yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                      item=item_component)

                    entities.append(item)
                else:
                    i -=1

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    #次のフロア生成
    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        #情報を継承
        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        #HPを固定値30回復
        player.fighter.heal(30)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
