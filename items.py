def evaluate_items(players):
    items = {i: {p['account_id']: {'count': 0, 'times': []} for p in players} for i, j in item_list().items()}
    slots = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 'backpack_0', 'backpack_1', 'backpack_2']
    all_items = item_ids()
    for player in players:
        for slot in slots:
            if player[slot] is None:
                return None
            item_id = player[slot]
            if item_id in all_items and all_items[item_id] in items:
                items[all_items[item_id]][player['account_id']]['count'] += 1
        for item_key, item_name in item_list().items():
            if player['purchase_log'] is not None:
                items[item_key][player['account_id']]['times'] = [k['time'] for k in player['purchase_log'] if
                                                                  k['key'] == item_key]
    return items


def item_list():
    return {
        'black_king_bar': 'Black King Bar',
        'radiance': 'Radiance',
        'ultimate_scepter': 'Aghanim\'s Scepter',
        'blink': 'Blink Dagger',
        'force_staff': 'Force Staff',
        'urn_of_shadows': 'Urn of Shadows',
        'spirit_vessel': 'Spirit Vessel',
        'crimson_guard': 'Crimson Guard',
        'vladmir': 'Vladmir\'s Offering',
        'ancient_janggo': 'Drum of Endurance',
        'nullifier': 'Nullifier',
        'magic_stick': 'Magic Stick',
        'magic_wand': 'Magic Wand',
        'bottle': 'Bottle',
        'hand_of_midas': 'Hand of Midas',
        'gem': 'Gem of True Sight',
        'rapier': 'Divine Rapier'
    }


def item_ids():
    return {
        1: 'blink',
        2: 'blades_of_attack',
        3: 'broadsword',
        4: 'chainmail',
        5: 'claymore',
        6: 'helm_of_iron_will',
        7: 'javelin',
        8: 'mithril_hammer',
        9: 'platemail',
        10: 'quarterstaff',
        11: 'quelling_blade',
        12: 'ring_of_protection',
        13: 'gauntlets',
        14: 'slippers',
        15: 'mantle',
        16: 'branches',
        17: 'belt_of_strength',
        18: 'boots_of_elves',
        19: 'robe',
        20: 'circlet',
        21: 'ogre_axe',
        22: 'blade_of_alacrity',
        23: 'staff_of_wizardry',
        24: 'ultimate_orb',
        25: 'gloves',
        26: 'lifesteal',
        27: 'ring_of_regen',
        28: 'sobi_mask',
        29: 'boots',
        30: 'gem',
        31: 'cloak',
        32: 'talisman_of_evasion',
        33: 'cheese',
        34: 'magic_stick',
        35: 'recipe_magic_wand',
        36: 'magic_wand',
        37: 'ghost',
        38: 'clarity',
        39: 'flask',
        40: 'dust',
        41: 'bottle',
        42: 'ward_observer',
        43: 'ward_sentry',
        44: 'tango',
        45: 'courier',
        46: 'tpscroll',
        47: 'recipe_travel_boots',
        48: 'travel_boots',
        49: 'recipe_phase_boots',
        50: 'phase_boots',
        51: 'demon_edge',
        52: 'eagle',
        53: 'reaver',
        54: 'relic',
        55: 'hyperstone',
        56: 'ring_of_health',
        57: 'void_stone',
        58: 'mystic_staff',
        59: 'energy_booster',
        60: 'point_booster',
        61: 'vitality_booster',
        62: 'recipe_power_treads',
        63: 'power_treads',
        64: 'recipe_hand_of_midas',
        65: 'hand_of_midas',
        66: 'recipe_oblivion_staff',
        67: 'oblivion_staff',
        68: 'recipe_pers',
        69: 'pers',
        70: 'recipe_poor_mans_shield',
        71: 'poor_mans_shield',
        72: 'recipe_bracer',
        73: 'bracer',
        74: 'recipe_wraith_band',
        75: 'wraith_band',
        76: 'recipe_null_talisman',
        77: 'null_talisman',
        78: 'recipe_mekansm',
        79: 'mekansm',
        80: 'recipe_vladmir',
        81: 'vladmir',
        85: 'recipe_buckler',
        86: 'buckler',
        87: 'recipe_ring_of_basilius',
        88: 'ring_of_basilius',
        89: 'recipe_pipe',
        90: 'pipe',
        91: 'recipe_urn_of_shadows',
        92: 'urn_of_shadows',
        93: 'recipe_headdress',
        94: 'headdress',
        95: 'recipe_sheepstick',
        96: 'sheepstick',
        97: 'recipe_orchid',
        98: 'orchid',
        99: 'recipe_cyclone',
        100: 'cyclone',
        101: 'recipe_force_staff',
        102: 'force_staff',
        103: 'recipe_dagon',
        104: 'dagon',
        105: 'recipe_necronomicon',
        106: 'necronomicon',
        107: 'recipe_ultimate_scepter',
        108: 'ultimate_scepter',
        109: 'recipe_refresher',
        110: 'refresher',
        111: 'recipe_assault',
        112: 'assault',
        113: 'recipe_heart',
        114: 'heart',
        115: 'recipe_black_king_bar',
        116: 'black_king_bar',
        117: 'aegis',
        118: 'recipe_shivas_guard',
        119: 'shivas_guard',
        120: 'recipe_bloodstone',
        121: 'bloodstone',
        122: 'recipe_sphere',
        123: 'sphere',
        124: 'recipe_vanguard',
        125: 'vanguard',
        126: 'recipe_blade_mail',
        127: 'blade_mail',
        128: 'recipe_soul_booster',
        129: 'soul_booster',
        130: 'recipe_hood_of_defiance',
        131: 'hood_of_defiance',
        132: 'recipe_rapier',
        133: 'rapier',
        134: 'recipe_monkey_king_bar',
        135: 'monkey_king_bar',
        136: 'recipe_radiance',
        137: 'radiance',
        138: 'recipe_butterfly',
        139: 'butterfly',
        140: 'recipe_greater_crit',
        141: 'greater_crit',
        142: 'recipe_basher',
        143: 'basher',
        144: 'recipe_bfury',
        145: 'bfury',
        146: 'recipe_manta',
        147: 'manta',
        148: 'recipe_lesser_crit',
        149: 'lesser_crit',
        150: 'recipe_armlet',
        151: 'armlet',
        152: 'invis_sword',
        153: 'recipe_sange_and_yasha',
        154: 'sange_and_yasha',
        155: 'recipe_satanic',
        156: 'satanic',
        157: 'recipe_mjollnir',
        158: 'mjollnir',
        159: 'recipe_skadi',
        160: 'skadi',
        161: 'recipe_sange',
        162: 'sange',
        163: 'recipe_helm_of_the_dominator',
        164: 'helm_of_the_dominator',
        165: 'recipe_maelstrom',
        166: 'maelstrom',
        167: 'recipe_desolator',
        168: 'desolator',
        169: 'recipe_yasha',
        170: 'yasha',
        171: 'recipe_mask_of_madness',
        172: 'mask_of_madness',
        173: 'recipe_diffusal_blade',
        174: 'diffusal_blade',
        175: 'recipe_ethereal_blade',
        176: 'ethereal_blade',
        177: 'recipe_soul_ring',
        178: 'soul_ring',
        179: 'recipe_arcane_boots',
        180: 'arcane_boots',
        181: 'orb_of_venom',
        182: 'stout_shield',
        183: 'recipe_invis_sword',
        184: 'recipe_ancient_janggo',
        185: 'ancient_janggo',
        186: 'recipe_medallion_of_courage',
        187: 'medallion_of_courage',
        188: 'smoke_of_deceit',
        189: 'recipe_veil_of_discord',
        190: 'veil_of_discord',
        191: 'recipe_necronomicon_2',
        192: 'recipe_necronomicon_3',
        193: 'necronomicon_2',
        194: 'necronomicon_3',
        196: 'diffusal_blade_2',
        197: 'recipe_dagon_2',
        198: 'recipe_dagon_3',
        199: 'recipe_dagon_4',
        200: 'recipe_dagon_5',
        201: 'dagon_2',
        202: 'dagon_3',
        203: 'dagon_4',
        204: 'dagon_5',
        205: 'recipe_rod_of_atos',
        206: 'rod_of_atos',
        207: 'recipe_abyssal_blade',
        208: 'abyssal_blade',
        209: 'recipe_heavens_halberd',
        210: 'heavens_halberd',
        211: 'recipe_ring_of_aquila',
        212: 'ring_of_aquila',
        213: 'recipe_tranquil_boots',
        214: 'tranquil_boots',
        215: 'shadow_amulet',
        216: 'enchanted_mango',
        217: 'recipe_ward_dispenser',
        218: 'ward_dispenser',
        219: 'recipe_travel_boots_2',
        220: 'travel_boots_2',
        221: 'recipe_lotus_orb',
        222: 'recipe_meteor_hammer',
        223: 'meteor_hammer',
        224: 'recipe_nullifier',
        225: 'nullifier',
        226: 'lotus_orb',
        227: 'recipe_solar_crest',
        228: 'recipe_octarine_core',
        229: 'solar_crest',
        230: 'recipe_guardian_greaves',
        231: 'guardian_greaves',
        232: 'aether_lens',
        233: 'recipe_aether_lens',
        234: 'recipe_dragon_lance',
        235: 'octarine_core',
        236: 'dragon_lance',
        237: 'faerie_fire',
        238: 'recipe_iron_talon',
        239: 'iron_talon',
        240: 'blight_stone',
        241: 'tango_single',
        242: 'crimson_guard',
        243: 'recipe_crimson_guard',
        244: 'wind_lace',
        245: 'recipe_bloodthorn',
        246: 'recipe_moon_shard',
        247: 'moon_shard',
        248: 'recipe_silver_edge',
        249: 'silver_edge',
        250: 'bloodthorn',
        251: 'recipe_echo_sabre',
        252: 'echo_sabre',
        253: 'recipe_glimmer_cape',
        254: 'glimmer_cape',
        255: 'recipe_aeon_disk',
        256: 'aeon_disk',
        257: 'tome_of_knowledge',
        258: 'recipe_kaya',
        259: 'kaya',
        260: 'refresher_shard',
        261: 'crown',
        262: 'recipe_hurricane_pike',
        263: 'hurricane_pike',
        265: 'infused_raindrop',
        266: 'recipe_spirit_vessel',
        267: 'spirit_vessel',
        268: 'recipe_holy_locket',
        269: 'holy_locket',
        272: 'recipe_kaya_and_sange',
        273: 'kaya_and_sange',
        274: 'recipe_yasha_and_kaya',
        275: 'trident',
        276: 'combo_breaker',
        277: 'yasha_and_kaya',
        279: 'ring_of_tarrasque',
        1021: 'river_painter',
        1022: 'river_painter2',
        1023: 'river_painter3',
        1024: 'river_painter4',
        1025: 'river_painter5',
        1026: 'river_painter6',
        1027: 'river_painter7',
        1028: 'mutation_tombstone',
        1029: 'super_blink',
        1030: 'pocket_tower',
        1032: 'pocket_roshan'
    }
