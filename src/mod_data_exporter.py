import json
import os
import Math

import nations
from ArenaType import g_cache as arena_types
from constants import ARENA_BONUS_TYPE
from helpers import getShortClientVersion, i18n
from items import vehicles

BONUS_TYPE_FORMAT = "#menu:bonusType/{0}"
GAMEPLAY_TYPE_FORMAT = "#arenas:type/{0}/name"
NATION_FORMAT = "#nations:{0}/genetiveCase"
VEHICLE_CLASS_FORMAT = "#menu:classes/short/{0}"


def get_bonus_type_data():
    bonus_type_data = dict()
    for bonus_type_id in ARENA_BONUS_TYPE.RANGE:
        i18n_key = BONUS_TYPE_FORMAT.format(bonus_type_id)
        bonus_type_data[bonus_type_id] = i18n.makeString(i18n_key)
    return bonus_type_data


def get_arena_type_data():
    arena_type_data = dict()
    for arena_type_id, arena_type in arena_types.iteritems():
        mode_i18n_key = GAMEPLAY_TYPE_FORMAT.format(arena_type.gameplayName)
        arena_type_data[arena_type_id] = {
            "map": arena_type.name,
            "map_id": arena_type.geometryName,
            "mode": i18n.makeString(mode_i18n_key),
            "mode_id": arena_type.gameplayName,
            "bounding_box": arena_type.boundingBox,
            "team_spawns": arena_type.teamSpawnPoints,
            "team_bases": [bases.values() for bases in arena_type.teamBasePositions],
            "neutral_bases": arena_type.controlPoints or [],
        }
    return arena_type_data


def get_vehicle_data():
    vehicle_data = dict()
    for nation_id, nation in nations.MAP.iteritems():
        nation_i18n_key = NATION_FORMAT.format(nation)
        nation_string = i18n.makeString(nation_i18n_key)

        for vehicle in vehicles.g_list.getList(nation_id).itervalues():
            vehicle_id = vehicle.compactDescr
            vehicle_type = vehicles.getItemByCompactDescr(vehicle_id)

            vehicle_class = vehicle_type.getVehicleClass()
            vehicle_class_i18n_key = VEHICLE_CLASS_FORMAT.format(vehicle_class)
            vehicle_class_string = i18n.makeString(vehicle_class_i18n_key)

            vehicle_data[vehicle_id] = {
                "name": vehicle_type.shortUserString,
                "nation": nation_string,
                "nation_id": nation,
                "tier": vehicle_type.level,
                "class": vehicle_class_string,
                "class_id": vehicle_class,
            }
    return vehicle_data


def get_game_version():
    return getShortClientVersion().strip()


def get_data():
    return {
        "game_version": get_game_version(),
        "bonus_types": get_bonus_type_data(),
        "arena_types": get_arena_type_data(),
        "vehicles": get_vehicle_data(),
    }


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Math.Vector2):
            return [obj[0], obj[1]]

        return json.JSONEncoder.default(self, obj)


def main():
    try:
        os.mkdir("exported_data")
    except OSError:
        pass

    data = get_data()

    filename = "exported_data/{}.json".format(get_game_version())
    with open(filename, "w") as outfile:
        outfile.write(json.dumps(data, indent=2, cls=Encoder))
