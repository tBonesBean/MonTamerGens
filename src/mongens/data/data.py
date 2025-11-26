from typing import Dict, List

# -- Baseline stats (can override per species later, after Elements do # there thing and populate stat boxes)

BASE_STATS: Dict[str, int] = {"HP": 100, "ATK": 50, "DEF": 50, "SPATK": 50, "SPDEF": 50, "SPD": 50, "ACC": 95, "EVA": 5, "LUCK": 10}

# ___________________________________________________________________________________

SEED_TYPES: List[str] = [
	"Geomorph", "Beast", "Aquatic", "Cryoform", "Pugilist", "Insectoid", "Mythic", "Electric", "Verdant", "Avian", "Dread", "Pyro", "Toxic", "Ancient",
	"Psychokinetic", "Neutral", "Colorless"
	]

INCOMPATIBLE_TYPE_PAIRS = {
	frozenset(["Pyro", "Aquatic"]),
	frozenset(["Pyro", "Cryoform"]),
	frozenset(["Electric", "Geomorph"]),
	frozenset(["Toxic", "Geomorph"]),
	frozenset(["Pugilist", "Aquatic"]),
	frozenset(["Mythic", "Dread"]),
	frozenset(["Pyro", "Verdant"]),
	frozenset(["Pyro", "Toxic"]),
	frozenset(["Insectoid", "Cryoform"]),
	}
# Each main type gets a baseline “body plan” bias.
# These are applied on top of BASE_STATS *before* mutagens.

FORMS_BY_TYPE: Dict[str, List[str]] = {
	"Geomorph"     : [
		"Gorgonopsid", "Stone Golem", "Earth Elemental", "Rock Hyrax", "Basilisk Lizard", "Gargoyle", "Moai-Stone Colossus", "Giant Anteater", "Trilobite",
		"Komodo Dragon", "Khalkotauroi", "Stoneback Tortoise Beast", "Obsidian Sandwyrm"
		],
	"Beast"        : [
		"Warthog", "Smilodon", "Minotaur", "Wolverine", "Wild Boar", "Mastiff-like Dire Hound", "Pangolin", "Tasmanian Tiger", "Hellhound", "Baboon", "Barong",
		"Nandi Bear", "Calydonian Boar"
		],
	"Aquatic"      : [
		"Dugong", "Giant Oarfish", "Dunkleosteus", "Kraken", "Axolotl", "Blue Dragon Sea Slug", "Mosasaur", "Naiad", "Sailfish", "Coelacanth", "Kelpie",
		"Adaro", "Cetus"
		],
	"Cryoform"     : [
		"Polar Bear", "Woolly Rhinoceros", "Wendigo", "Snowy Owl", "Ice Elemental", "Caribou", "Yeti", "Arctic Fox", "Megaloceros", "Narwhal", "Jotunn",
		"Snow Kirin", "Ice Wyrmling Drake"
		],
	"Pugilist"     : [
		"Kangaroo", "Mantis Shrimp", "Gorilla", "Boxing Beetle", "Red Kangaroo Rat-boxing Monster", "Secretary Bird", "Harpy", "Cassowary", "Thylacoleo",
		"Chimpanzee", "Stone-Fist Gargant", "Pummeler Homunculus", "Oni Boxer"
		],
	"Insectoid"    : [
		"Tarantula Hawk", "Titan Beetle", "Meganeura", "Antlion", "Mothman", "Horseshoe Crab", "Coconut Crab", "Grylloblattid", "Giant Isopod",
		"Praying Mantis", "Scarab Guardian", "Unkcela", "Trilobite Colossus"
		],
	"Mythic"       : [
		"Griffin", "Kitsune", "Banshee", "Thunderbird", "Nemean Lion", "Leviathan", "Qilin", "Selkie", "Jorōgumo", "Phoenix", "Mapinguari", "Hippogriff",
		"Tikbalang"
		],
	"Electric"     : [
		"Electric Eel", "Storm Elemental", "Thundering Roc", "Platypus", "Torpedo Ray", "Ball Lightning Sprite", "Scintillant Tree Frog", "St. Elmo’s Fire",
		"Electric Catfish", "Scintillating Beetle", "Thunderbird Whelp", "Raiju", "Volt Seraph"
		],
	"Verdant"      : [
		"Dryad", "Nepenthes Pitcher Beast", "Ent", "Yew Tree Spirit", "Mandrake", "Venus Flytrap", "Wollemi Pine Dryosaur", "Bramble Golem", "Baobab Tortoise",
		"Moss-Lurker Sprite", "Kodama", "Thorn Hydra", "Spriggan"
		],
	"Avian"        : [
		"Shoebill", "Archaeopteryx", "Roc", "Harpy Eagle", "Kiwi", "Hoatzin", "Takahē", "Terror Bird", "Lyrebird", "Red-crowned Crane", "Firefoot Heron",
		"Bennu", "Storm Petrel Titan"
		],
	"Dread"        : [
		"Wraith", "Shadow Hound", "Nightgaunt", "Chupacabra", "Ghoul", "Barghest", "Lurking Mirefiend", "Blemmyes", "Mare", "Dullahan", "Draugr", "Nachtkrapp",
		"Shadow Lamia"
		],
	"Pyro"         : [
		"Salamander", "Fire Jinn", "Ifrit", "Ash Drake", "Volcanic Worm", "Fire Beetle", "Ember Lion", "Solifuge", "Pyrosaurus", "Firebird",
		"Magma Salamander",
		"Zhurong Beast", "Fire Jotunn"
		],
	"Toxic"        : [
		"Blue-ringed Octopus", "Stonefish", "Inland Taipan", "Poison Dart Frog", "Gila Monster", "Boomslang", "Box Jellyfish", "Deathstalker Scorpion",
		"Portuguese Man o’ War", "Hooded Pitohui", "Wyvern Basilisk", "Tatzelwurm", "Nagual Serpent Shade"
		],
	"Ancient"      : [
		"Anomalocaris", "Titanoboa", "Andrewsarchus", "Plesiosaur", "Ammonite", "Saurosuchus", "Hallucigenia", "Protostega", "Giant Ground Sloth",
		"Quetzalcoatl", "Diprotodon", "Dunkleoceratid", "Uintatherium",
		],
	"Psychokinetic": [
		"Cerebellid Wisp", "Astral Jelly", "Homunculus", "Tarsier", "Mind Flayer", "Dream-Eater Tapir Spirit", "Spectral Owl", "Neurophage Shade",
		"Deep-Thought Squid", "Oracle Serpent", "Alkonost", "Astral Lynx", "Baku"
		],
	"Neutral"      : [
		"Slime Blob"
		],
	"Colorless"    : [
		"Sphinx"
		]
	}
# Each main type gets a baseline “body plan” bias.
# These are applied on top of BASE_STATS *before* mutagens.

SEEDTYPE_ATTR = {
	"Geomorph"     : {"mul": {"DEF": 1.45, "SPDEF": 1.30, "ATK": 1.25, "SPD": 0.75, "HP": 1.15}, "add": {"DEF": 10}, "tags": ["Grounded", "Resist:Electric", "Weak:Pugilist", "Weak:Aquatic"]},
	"Beast"        : {"mul": {"ATK": 1.40, "SPD": 1.25, "HP": 1.20, "DEF": 1.10}, "add": {"ATK": 5}, "tags": ["Feral", "Intimidate", "Weak:Venomous"]},
	"Aquatic"      : {"mul": {"SPDEF": 1.35, "SPD": 1.30, "HP": 1.25, "ATK": 1.10}, "add": {}, "tags": ["Amphibious", "Resist:Pyro", "Weak:Electric"]},
	"Cryoform"     : {"mul": {"SPDEF": 1.40, "HP": 1.30, "SPATK": 1.15, "SPD": 0.85}, "add": {"SPDEF": 5}, "tags": ["FrostAura", "Resist:Aquatic", "Weak:Pyro"]},
	"Pugilist"     : {"mul": {"ATK": 1.45, "SPD": 1.35, "SPATK": 0.80, "LUCK": 1.20}, "add": {"ATK": 10}, "tags": ["Combo", "Resist:Dread", "Weak:Psychokinetic"]},
	"Insectoid"    : {"mul": {"SPD": 1.50, "ATK": 1.25, "DEF": 1.20, "HP": 0.90}, "add": {"EVA": 5}, "tags": ["Swarm", "Exoskeleton", "Weak:Avian", "Weak:Pyro"]},
	"Mythic"       : {"mul": {"LUCK": 1.50, "SPATK": 1.30, "SPDEF": 1.30, "HP": 1.20}, "add": {"LUCK": 10}, "tags": ["Fated", "CannotBeCursed", "Weak:Ancient"]},
	"Electric"     : {"mul": {"SPD": 1.45, "SPATK": 1.35, "ATK": 0.90}, "add": {"SPD": 5}, "tags": ["HighVoltage", "Resist:Avian", "Weak:Geomorph"]},
	"Verdant"      : {"mul": {"HP": 1.40, "SPDEF": 1.35, "SPATK": 1.15, "SPD": 0.80}, "add": {"HP": 20}, "tags": ["Regrowth", "Resist:Aquatic", "Weak:Pyro", "Weak:Toxic"]},
	"Avian"        : {"mul": {"SPD": 1.40, "ATK": 1.30, "EVA": 1.25, "HP": 0.95}, "add": {"EVA": 5}, "tags": ["Flying", "Acrobatic", "Weak:Electric"]},
	"Dread"        : {"mul": {"SPATK": 1.40, "SPDEF": 1.25, "LUCK": 1.20, "DEF": 0.90}, "add": {}, "tags": ["Fear", "LifeSteal", "Weak:Mythic", "Weak:Radiant"]},
	"Pyro"         : {"mul": {"SPATK": 1.45, "ATK": 1.20, "SPD": 1.20, "SPDEF": 0.85}, "add": {"SPATK": 10}, "tags": ["Ignite", "Resist:Cryoform", "Weak:Aquatic"]},
	"Toxic"        : {"mul": {"SPATK": 1.35, "DEF": 1.25, "HP": 1.15, "SPD": 0.95}, "add": {}, "tags": ["Poisonous", "Corrosive", "Weak:Geomorph", "Weak:Verdant"]},
	"Ancient"      : {"mul": {"HP": 1.50, "DEF": 1.35, "ATK": 1.25, "SPD": 0.70}, "add": {"HP": 25, "DEF": 5}, "tags": ["Primordial", "Resist:Mythic", "Weak:Chaos"]},
	"Psychokinetic": {"mul": {"SPATK": 1.40, "SPD": 1.30, "SPDEF": 1.20, "HP": 0.90}, "add": {"SPATK": 5}, "tags": ["Telekinesis", "Clairvoyant", "Weak:Dread"]},
	}

MAJOR_MODS = {
	"Tectonic"     : {"mul": {"DEF": 1.25, "HP": 1.15, "ATK": 1.10}, "add": {"DEF": 10}, "tags": ["Resist:Stormforged", "Terrain:Bonus", "Terraform"]},
	"Glacial"    : {"mul": {"SPDEF": 1.25, "HP": 1.20, "SPD": 0.90}, "add": {"SPDEF": 10}, "tags": ["Resist:Frostbound", "Weak:Tempest", "IceArmor"]},
	"Voltaic"    : {"mul": {"SPD": 1.25, "SPATK": 1.20}, "add": {"ACC": 5}, "tags": ["Resist:Electric", "Weak:Terra", "StaticField"]},
	"Noxious"   : {"mul": {"SPATK": 1.20, "SPD": 1.15, "LUCK": 1.10}, "add": {}, "tags": ["DOT:Poison", "Weak:Radiant", "Neurotoxin"]},
	"Radiant"    : {"mul": {"SPATK": 1.25, "SPDEF": 1.15}, "add": {"ACC": 10}, "tags": ["Cure:Blind", "Weak:Shade", "HolyLight"]},
	"BioLuminous"  : {"mul": {"SPD": 1.20, "SPATK": 1.15, "EVA": 1.10}, "add": {"EVA": 5}, "tags": ["OnCrit:Leech", "Weak:Radiant", "Shadowstep"]},
	"Astral"     : {"mul": {"SPATK": 1.25, "LUCK": 1.20, "SPDEF": 1.10}, "add": {"LUCK": 5}, "tags": ["Pierce:Barrier", "Weak:Obsidian", "Cosmic"]},
	"Solar"      : {"mul": {"ATK": 1.20, "SPATK": 1.20, "HP": 1.10}, "add": {}, "tags": ["Regen:Day", "Weak:Chaos", "Sunfire"]},
	"Nocturnal"      : {"mul": {"SPDEF": 1.25, "EVA": 1.15, "HP": 1.10}, "add": {}, "tags": ["Regen:Night", "Weak:Solar", "Moonshield"]},
	"Chaos"      : {"mul": {"ATK": 1.25, "SPATK": 1.25, "LUCK": 1.25, "HP": 0.90, "ACC": 0.95}, "add": {}, "tags": ["Random:Proc", "Weak:Ironclad", "Unstable"]},
	"Monolithic"  : {"mul": {"DEF": 1.20, "ATK": 1.15, "HP": 1.10}, "add": {}, "tags": ["Ambush:Burrow", "Weak:Astral", "Tremorsense"]},
	"Tempest"    : {"mul": {"SPD": 1.25, "ATK": 1.15}, "add": {"ACC": 5}, "tags": ["MultiHit:Storm", "Weak:Crystalline", "GaleForce"]},
	"Shielded"    : {"mul": {"DEF": 1.30, "SPDEF": 1.20, "SPD": 0.85}, "add": {"DEF": 15}, "tags": ["Guard:Stagger", "Weak:Shade", "Ironclad"]},
	"Vulcan"   : {"mul": {"SPATK": 1.25, "DEF": 1.15}, "add": {"SPATK": 5}, "tags": ["Burn:Contact", "Weak:Tempest", "MagmaPlating"]},
	"Atmos"      : {"mul": {"SPD": 1.20, "EVA": 1.20}, "add": {"EVA": 10}, "tags": ["Evade:Aerial", "Weak:Electric", "Updraft"]},
	"Abyssal" : {"mul": {"HP": 1.25, "SPDEF": 1.20, "SPD": 0.90}, "add": {}, "tags": ["FirstStrike:Water", "Weak:Solar, Verdant", "Abyssal"]},
	"Telepath" : {"mul": {"SPATK": 1.20, "LUCK": 1.15}, "add": {"ACC": 5}, "tags": ["Pierce:Mind", "Weak:Ironclad", "MindRead"]},
	"Vedic"  : {"mul": {"SPD": 1.15, "SPDEF": 1.15, "EVA": 1.10}, "add": {"EVA": 5}, "tags": ["Fog:Field", "Weak:Radiant", "Ethereal"]},
	"Farphase"  : {"mul": {"SPD": 1.20, "LUCK": 1.15}, "add": {"ACC": 5}, "tags": ["Blink:Short", "Weak:Obsidian", "PhaseShift"]},
	"Metallic"     : {"mul": {"LUCK": 1.35, "DEF": 1.15}, "add": {"LUCK": 15}, "tags": ["Loot:Bonus", "Weak:Toxic", "GoldPlated"]},
	"Sensei"     : {"mul": {"ATK": 1.10, "SPATK": 1.10, "ACC": 1.10}, "add": {"ACC": 10}, "tags": ["Mentor", "FlawlessTechnique"]},
	"Fossilized" : {"mul": {"HP": 1.05, "ATK": 1.22, "DEF": 1.20, "SPDEF": 1.12}, "add": {}, "tags": ["Ability:Revive", "Resist:Geomorph"]}

	}


MINOR_MODS = {
	"ThornArmored"     : {"mul": {"DEF": 1.1}, "tags": ["Thorns:Light"]},
	"Crystalline"      : {"mul": {"SPDEF": 1.1}, "tags": ["Resist:Water"]},
	"Cavernkept"  : {"mul": {"SPDEF": 1.1, "HP": 1.2}, "tags": ["Accuracy:Dark"]},
	"SandCrawler"     : {"mul": {"SPD": 1.1}, "tags": ["Initiative:Sand"]},
	"BrightEmber"    : {"mul": {"SPATK": 1.1}, "tags": ["Ignite:Low"]},
	"LoreGuardian"  : {"mul": {"SPD": 1.1}, "tags": ["Action:Flow"]},
	"ArcticSurfer"     : {"mul": {"SPDEF": 1.1}, "tags": ["Slide:Ice"]},
	"SuperOrbital"   : {"mul": {"SPATK": 1.1}, "tags": ["Curse:Minor"]},
	"BoltThrower"      : {"mul": {"ATK": 1.1}, "tags": ["Call:Storm"]},
	"VineWraped"   : {"mul": {"SPATK": 1.1, "SPD": .92}, "tags": ["Leech:Minor"]},
	"RuneReader"      : {"mul": {"SPATK": 1.1}, "tags": ["RuneSlots:+1"]},
	"GroveGrown"     : {"mul": {"HP": 1.1}, "tags": ["Heal:Terrain"]},
	"Sunbaked"       : {"mul": {"ATK": 1.1}, "tags": ["DayBoost"]},
	"Necromance"    : {"mul": {"DEF": 1.1}, "tags": ["Snare:Low"]},
	"CloudTamer"    : {"mul": {"SPD": 1.1}, "tags": ["Leap:Aerial"]},
	"Stargazed"      : {"mul": {"LUCK": 1.1}, "tags": ["Crit:Starlit"]},
	"BattleScarred"      : {"mul": {"HP": 1.02, "SPDEF": 1.02}, "tags": ["Float:Water"]},
	"Paranormal"     : {"mul": {"DEF": 1.04}, "tags": ["Resist:Blunt"]},
	"Feralkin"      : {"mul": {"SPD": 1.03, "ATK": 1.02}, "tags": ["Howl:Pack"]},
	"Shadowshroud"   : {"mul": {"SPD": 1.03}, "tags": ["Veil:Dark"]},
	"DuneChaser"      : {"mul": {"SPD": 1.02, "ATK": 1.1}, "tags": ["Crit:Sand"]},
	"DarkIce"       : {"mul": {"SPDEF": 1.04}, "tags": ["Slide:Ice"]},
	"Extrasensory"       : {"mul": {"HP": 1.07, "SPATK": 1.03}, "tags": ["Root:Terrain"]},
	"ThunderClap"    : {"mul": {"SPATK": 1.05}, "tags": ["Call:Storm"]},
	"OnyxCore"       : {"mul": {"DEF": 1.04, "HP": 1.02}, "tags": ["Resist:Blunt"]},
	"BioLuminescent" : {"mul": {"LUCK": 1.05}, "add": {}, "tags": ["Glow:Dark", "Lure:Shallow"]},
	"ArcheoAnomaly"  : {"mul": {"ATK": 1.08, "SPDEF": 1.06}, "add": {"EVA": +1}, "tags": ["Sentience:Inconsistent"]},
	}

UTILITY_MODS = {
	"Age<UNKNOWN>"     : {"exp_mult": 1.10, "loot_mult": 1.15, "tags": ["Lore:Gates"]},
	"BornLeader"    : {"ally_buff": {"ATK": 1.12, "HP": 1.20}, "exp_share_bonus": 0.20, "tags": ["VeteranPresence", "BattleCry"]},
	"Diviner"          : {"minimap_reveal": True, "tags": ["Reveal:Secrets"]},
	"InnateGuard"  : {"ally_buff": {"DEF": 1.08}, "aggro_redirect": True},
	"Empath"           : {"ally_heal_on_crit": 0.10, "tags": ["Soothing"]},
	"KeeperOfKeys"     : {"unlock_tags": ["Gate:Runic", "Door:Sealed"]},
	"CosmicInterpreter": {"identify_rates": 0.25, "tags": ["Identify:Rare"]},
	"Historian"     : {"npc_dialog_plus": True, "tags": ["Diplomacy"]},
	"Impossible"       : {"rng_luck_bias": 0.10, "tags": ["WildProcs"]},
	"LongSeeker"           : {"track_rare_spawns": True, "track_rare_loot": True, "tags": ["Tracker", "TreasureHunter"]},
	"Transient"         : {"camp_bonus": {"Heal%": 0.05, "exp_mult": 1.15}, "tags": ["Wanderer"]},
	"Cartographer"      : {"fast_travel_nodes": True},
	"Superpositional"  : {"double_rolls": ["Loot", "Crit"], "tags": ["Quantum"]},
	"CombatController": {"ally_buff": [], "enemy_opening_debuff": {"SPD": 0.90, "ACC": -8}, "tags": ["Disorient"]},
	"Scholar"   : {"ally_exp_mult": 1.15},
	"Humanitarian"     : {"loot_to_supplies": 0.20, "tags": ["ConvertLoot"]},
	"Grinder"  : {"spar_exp_bonus": 0.20},
	"MagneticAura"     : {"pull_items_radius": 12, "pull_hidden_radius": 8, "tags": ["Magnetism"]},
	"Symbiotic"  : {"field_heal_ticks": 0.05, "ally_heal_ticks": 0.02, "tags": ["HealingAura"]},
	"SecretKeeper"     : {"npc_dialog_plus": True, "minimap_reveal": True, "tags": ["HiddenPaths"]},
	"NearExtinction"   : {"self_revive": True, "identify_fossils": True, "identify_eggs": True}
	}

ALL_MODS = [MAJOR_MODS, MINOR_MODS, UTILITY_MODS]

# --Definitely dictates appearance and contributes to substantiating game world, likely will become factor when randomizing hidden traits, moves/attacks,
# special abilities,
# etc. --#
TRAITS_LIST = [
	["Multiple Tails", "Trident", "Steps Make Subtle Sparks"],
	["Oversized Crown", "Gills", "Solar-Phobia"],
	["Hovers When It Rains", "Stamp Collection", "Persistent Hallucinations"],
	["High-Fashion", "Herbivore", "Receives Cosmic Messages"],
	["Bipedal", "Wears Heavy Amulets", "Terrible Hay Fever"],
	["Face Obsured By Pollution", "Equipped With Satellite Dish", "Amnesia"],
	["Full Plate Armor", "Builds Nest With Shells", "Nocturnal"],
	["Glowing Freckles", "Compass That Hums", "Allergic To Moonlight"],
	["Translucent Skin", "Pocket Sundial", "Speaks In Echoes"],
	["Feathered Arms", "Ancient Coin Collection", "Dreams Predict Rainfall"],
	["Cracked Porcelain Mask", "Pet Cloud", "Forgets Own Reflection"],
	["Luminescent Veins", "Bone Flute", "Haunted By Laughter"],
	["One Glass Eye", "Floating Lantern Companion", "Immune To Cold"],
	["Spiraled Horns", "Mechanical Heart", "Whispers To Stones"],
	["Mismatched Eyes", "Cursed Locket", "Leaves Frost Footprints"],
	["Tattooed Constellations", "Hourglass Pendant", "Never Casts A Shadow"],
	["Metallic Hair", "Pocket Full Of Sand", "Understands Every Language But Their Own"],
	["Webbed Fingers", "Obsidian Dagger", "Allergic To Sunlight"],
	["Crystalline Spine", "Enchanted Scarf", "Remembers Other Lives"],
	["Ashen Skin", "Compass That Points To Danger", "Hums When Nervous"],
	["Cape Of Smoke", "Cracked Monocle", "Can’t Cross Running Water"],
	["Glimmering Scales", "Silver Whistle", "Haunted By A Melody"],
	["Turtle Shell Hat", "Pocket Mirror That Lies", "Collects Fallen Stars"],
	["Antler Crown", "Broken Pocket Watch", "Voice Echoes Twice"],
	["Moss-Covered Shoulders", "Golden Key", "Never Sleeps On Full Moons"],
	["Glowing Pupils", "Ancient Scroll", "Sneezes Sparks"],
	["Tinted Astronaut Helmet", "Hourglass Tattoo", "Can’t Be Photographed"],
	["Sentient Tail", "Compass Of Bone", "Allergic To Laughter"],
	["Cracked Halo", "Vial Of Mist", "Speaks To Insects"],
	["Stone Skin", "Silver Ring That Hums", "Forgetting Faces Instantly"],
	["Shimmering Icy Breath", "Always Reading Seer Bones", "Dealing with a Mirror-phobia"],
	["Branch-Like Fingers", "Crystal Monocle", "Dreams In Color Only"],
	["Top Hat With Feather", "Infinity Symbol Earrings", "Can’t Lie"],
	["Metal Jaw And Shoulderplates", "Charm Bracelet Of Teeth", "Floats When Calm"],
	["Opal Eyes", "Cursed Violin", "Allergic To Salt"],
	["Scaled Neck", "Compass That Spins Wildly", "Voice Attracts Moths"],
	["Glowing Body Pattern", "Broken Crown", "Remembers Every Sound Ever Heard"],
	["Smoke Hair", "Hourglass Heart", "Can’t Touch Iron"],
	["Shadow Has Massive Wings", "Silver Coin", "Speaks To Reflections"],
	["Glowing Fingertips", "Pocket Flame", "Terrified Of Silence"],
	["Horned Silhouette", "Glass Bottle Of Whispers", "Never Ages"],
	["Oversized Beak", "Holds Pouches Of Secret Contents", "Allergic To Rain"],
	["Crystal Antlers", "Golden Thread", "Can’t Dream"],
	["4 Arms", "Hourglass Of Sand", "Longs To Be Back Among The Stars"],
	["Glowing Scars", "Silver Bell", "Haunted By Footsteps"],
	["Porcelain Mask", "Compass That Hums Softly", "Can’t Cry"],
	["Feathered Cloak", "Pocket Of Ashes", "Reliably Full Of Joy"],
	["Stone Horns", "Hourglass Pendant", "Speaks In Riddles"],
	["Glowing Eyes", "Silver Dagger", "Can’t Remember Names"],
	["Cracked Skin", "Compass That Points Home", "Laughs At Thunder"],
	["Shadowed Face", "Vial Of Tears", "Allergic To Gold"],
	["Glimmering Hair", "Pocket Watch That Ticks Backward", "Can’t Whistle"],
	["Meditating Body Position", "Silver Coin", "Dreams Of Drowning"],
	["Crystal Teeth And Claws", "Tail Glows When In Danger", "Sees Prophecy In Flames"],
	["Unusually Long Tail", "Hourglass Tattoo", "Can’t See Stars"],
	["Glowing Veins", "Pocket Mirror", "Speaks To Shadows"],
	["Horned Brow", "Oversized Bandit Mask", "Can Be Lured By Music"],
	]

COL_TRAITS = [  # -- Much easier to mass generate random traits as triplets, without sacrificing positional integrity in transposed orientation shown below --#
	[
		"Multiple Tails", "Oversized Crown", "Hovers When It Rains", "Bipedal", "Bipedal", "Bipedal", "Bipedal", "Face Obsured By Pollution", "Full Plate Armor", "Glowing Fangs",
		"Translucent Skin", "Walks on Hands due to Curious Environmental Adaptation", "Cracked Porcelain Mask", "Luminescent Veins", "One Glass Eye",
		"Spiraled Horns", "Disproportional Eyes", "Tattooed Constellations", "Metallic Hair", "Webbed Fingers", "Crystalline Spine", "Ashen Skin", "Cape Of Smoke",
		"Glimmering Scales", "Turtle Shell Helmet", "Antler Crown", "Top-heavy but Never Off-balance", "Glowing Pupils", "Tinted Astronaut Helmet",
		"Sentient Tail", "Cracked Halo", "Stone Skin", "Shimmering Icy Breath", "Branch-Like Fingers and appendages", "Top Hat With Feather", "Metal Jaw And Shoulderplates",
		"Opal Eyes", "Bipedal", "Bipedal", "Bipedal", "Glowing Body Pattern", "Hair Mysteriously Flows as if always Underwater",
		"Long fur that shifts as though underwater", "Shadow Has Massive Wings", "Wings shimmer and move like a Mirage", "Antennae that act like Periscopes",
		"Sentiet Antennae", "Sentient Antlers", "Glowing Fingertips", "Only the Silhouette seems to have Giant Horns", "Oversized Beak",
		"Crystal Elk Antlers", "Four Extra Arms", "Glowing Scars", "Porcelain Mask", "Feathered Cloak", "Stone Horns", "Glowing Eyes", "Body armor made of Caribou Antlers",
		"Giant Caribou Antlers", "Shadowed Face", "Hair Changes Color to Indicate Mood", "Meditating Body Position", "Crystal Teeth And Claws", "Weaponized Tail",
		"Veins create Pulsating Glow of Random Colors every few	seconds", "Dangerous, yet flightless, wings that are used for Self-Defense", "Tail Glows When In Danger", "Bipedal",
		],
	[
		"Trident", "Gills", "Stamp Collection", "Equipped With Satellite Dish", "Builds Nest With Shells", "Compass That Hums", "Pocket Sundial",
		"Ancient Coin Collection",
		"Pet Cloud", "Bone Flute", "Floating Lantern Companion", "Mechanical Heart", "Obsidian Dagger", "Enchanted Scarf", "Compass That Points To Danger",
		"Cracked Monocle",
		"Broken Pocket Watch", "Golden Key", "Ancient Scroll", "Adorned with Bone Charms", "Eyes Made of Strange Mist",
		"Silver Ring That Identifies Nearby Ore",
		"Always Reading Seer Bones", "Crystal Monocle and Black Felt Tophat", "Charm Bracelet Of Teeth", "Cursed Violin", "Compass That Spins Wildly",
		"Broken Crown",
		"Pocket Flame", "Glass Bottle Of Whispers", "Holds Pouches Of Secret Contents", "Golden Thread", "Giant Hourglass containing Claws of Enemies",
		"Compass That Hums Softly",
		"Bottomless Pocket Of Ashes that's Constantly Spilling Over", "Silver Dagger", "Compass That Points Home", "Vial Of Tears",
		"Pocket Watch That Ticks Backward",
		"Silver Coin", "Oversized Bandit Mask", "Four Drumsticks but Nothing to Drum", "Steps Make Subtle Sparks",
		],
	[
		"Solar-Phobia", "Persistent Hallucinations", "Receives Cosmic Messages", "Terrible Hay Fever", "Amnesia", "Nocturnal", "Allergic To Moonlight",
		"Speaks In Echoes",
		"Dreams Predict Rainfall", "Forgets Own Reflection", "Haunted By Laughter", "Immune To Cold", "Whispers To Stones", "Leaves Frost Footprints",
		"Never Casts A Shadow",
		"Understands Every Language But Their Own", "Allergic To Sunlight", "Remembers Past Lives", "Hums When Nervous", "Can’t Cross Running Water",
		"Haunted By A Melody",
		"Collects Fallen Stars", "Voice Echoes Twice", "Never Sleeps On Full Moons", "Sneezes Sparks", "Can’t Be Photographed", "Allergic To Laughter",
		"Speaks To Insects",
		"Forgets Faces Instantly", "Terrified Of Mirrors", "Dreams In Color Only", "Can’t Lie", "Floats When Calm", "Allergic To Salt", "Voice Attracts Moths",
		"Remembers Every Sound Ever Heard", "Can’t Touch Iron", "Speaks To Reflections", "Terrified Of Silence", "Never Ages", "Allergic To Rain",
		"Can’t Dream",
		"Longs To Be Back Among The Stars", "Haunted By Footsteps", "Can’t Cry", "Reliably Full Of Joy", "Speaks In Riddles", "Can’t Remember Names",
		"Laughs At Thunder",
		"Allergic To Gold", "Can’t Whistle", "Dreams Of Drowning", "Sees Prophecy In Flames", "Can’t See Stars", "Speaks To Shadows", "Can Be Lured By Music",
		"Herbivore"
		]
	]

TEMPERS_COUPLED: Dict[str, List[str]] = {
	"mood": [
		"Shy", "Bashful", "Hostile", "Wary", "Clever", "Aloof", "Warm", "Cold", "Guarded", "Friendly", "Suspicious", "Curious", "Gentle", "Arrogant", "Proud",
		"Humble", "Kind",
		"Cruel", "Generous", "Jealous", "Envious", "Patient", "Impatient", "Sensitive", "Indifferent", "Compassionate", "Cynical", "Trusting", "Distrustful",
		"Amiable",
		"Resentful", "Cheerful", "Irritable", "Sincere", "Devious", "Gracious", "Petty", "Tolerant", "Moody", "Outgoing", "Territorial", "Aggressive",
		"Immune",
		"Conceited",
		"Confident", "Wise", "Optimistic", "Lonely"
		],
	"affinity": [
		"Selflessness", "Warmth", "Hostility", "Coyness", "Honor", "Glory", "Boldness", "Intellect", "Caution", "Suspicion", "Curiosity", "Gentleness",
		"Arrogance", "Pride",
		"Humility", "Kindness", "Cruelty", "Generosity", "Open-Mindedness", "Envy", "Patience", "Impatience", "Sensitivity", "Indifference", "Compassion",
		"Cynicism",
		"Trustfulness", "Distrust", "Amiability", "Resentment", "Cheerfulness", "Irritability", "Sincerity", "Deviousness", "Graciousness", "Pettiness",
		"Tolerance"
		],
	}

_ALL_HABITATS_RAW = [
	"Oldgrowth Marsh", "Misty Glades", "Thornveil Thicket", "Highlands", "Smoldering Flats", "Collapsed Magma Tubes", "Ancient Lavaflows", "Whispering Dunes",
	"Glass Caverns", "Obsidian Labyrinth", "Ashlands", "Mt. Thermallia", "Crystalline Cave", "Petrified Forest", "Glassy Caverns", "Skybridge Peaks",
	"Frozen Steppe", "Glass Desert", "Shattered Plateau", "Yittrosian Forest", "Thriving Reefs", "Sunless Abyss", "Alpine Lakes", "Moonlit Atolls",
	"Bioluminous Currents", "Violent Rapids", "Freshwater Springs", "Unyielding Cascades" "Ennoan Grasslands", "Alpine Slopes", "Lunaglow Plateau",
	"Riverlands", "Dayless Mosswood", "Still Tidepools", "Starfall Crater", "Celestial Spire", "Aurora Fields", "Echoing Grotto", "Astral Terrace",
	"Dread Catacombs", "Gloomfen Bogs", "AshGlass Tombs", "Darkmist Chasm", "Abandoned Wastes", "Power Plant", "Eroding Shipwreck", "Ghost Town",
	"Abandoned Village", "Concrete Jungle", "Rusted Plane Wreckage", "Wild Tundra", "Ice Caps", "Snowcapped Peaks", "Frigid Icefields",
	"Snowpacked Mountains", "Permafrost Highlands", "Clockwork City", "Bioforge Basin", "Crumbling Ruins", "Forgotten Temple", "Ancient Battlefield",
	"Archaeological Dig", "Agency Black Site", "Synthetic Biosphere", "Verdant Plains", "Blooming Valley", "Ironwood Deep", "Fungal Vales",
	"Bewitched Glen", "Netherbleak Hollow" "Wyrmscar Ridge" "Restricted Labratory", "Secret Lab", "Origin<UNKNOWN>", "Retired Military Base",
	"Condemned HydroPowerDam", "Monolithic Structures", "Classified Research Facilities"
	]

ALL_HABITATS = sorted(list(set(_ALL_HABITATS_RAW)))

HABITATS_BY_TYPE: Dict[str, list] = {
	"Verdant"      : [
		"Oldgrowth Marsh", "Misty Glades", "Bewitched Glen", "Verdant Plains", "Blooming Valley", "Ironwood Deep", "Fungal Vales", "Thornveil Thicket",
		"Skyless MossWood", "Shattered Plateau", "Wyrmscar Ridge",
		],
	"Pyro"         : [
		"Smoldering Flats", "Collapsed Magma Tubes", "Ancient Lavaflows", "Whispering Dunes", "Glass Caverns", "Obsidian Labyrinth", "Petrified Forest",
		"Ashlands", "Mt. Thermallia",
		],
	"Geomorph"     : [
		"Crystalline Cave", "Petrified Forest", "Ancient Lavaflows", "Whispering Dunes", "Glass Caverns", "Thriving Reefs", "Crumbling Ruins",
		"Forgotten Temple", "Archaeological Dig"
		],
	"Avian"        : [
		"Skybridge Peaks", "Frozen Steppe", "Whispering Dunes", "Glass Desert", "Verdant Plains", "Highlands", "Shattered Plateau", "Wyrmscar Ridge",
		"Yittrosian Forest",
		],
	"Aquatic"      : [
		"Still Tidepools", "Thriving Reefs", "Sunless Abyss", "Alpine Lakes", "Moonlit Atolls", "Bioluminous Currents", "Violent Rapids",
		"Freshwater Springs", "Unyielding Cascades"
		],
	"Beast"        : [
		"Crystalline Caverns", "Ennoan Grasslands", "Alpine Slopes", "Lunaglow Plateau", "Riverlands", "Skyless MossWood", "Still Tidepools",
		"Glass Desert", "Blooming Valley", "Ironwood Deep", "Fungal Vales", "Thornveil Thicket",
		],
	"Mythic"       : [
		"Starfall Crater", "Celestial Spire", "Aurora Fields", "Twilight Basin", "Echoing Grotto", "Astral Terrace", "Synthetic Biosphere",
		"Origin<UNKNOWN>"
		],
	"Insectoid"    : [
		"Twilight Basin", "Echoing Grotto", "Darkmist Chasm", "Netherbleak Hollow", "Whispering Dunes", "Alpine Lakes", "Petrified Forest",
		"Oldgrowth Marsh", "Misty Glades", "Skyless MossWood", "Still Tidepools", "Bioluminous Currents",
		],
	"Dread"        : [
		"Dread Catacombs", "Gloomfen Bogs", "AshGlass Tombs", "Darkmist Chasm", "Netherbleak Hollow", "Abandoned Wastes", "Forgotten Boneyard",
		"Retired Military Base", "Monolithic Structures", "Skyless MossWood",
		],
	"Electric"     : [
		"Power Plant", "Eroding Shipwreck", "Ghost Town", "Abandoned Village", "Restricted Labratory", "Concrete Jungle", "Retired Military Base",
		"Outdated Hydroelectric Dam", "Rusted Plane Wreckage"
		],
	"Cryoform"     : [
		"Wild Tundra", "Ice Caps", "Snowcapped Peaks", "Frigid Icefields", "Sunless Extremes", "Snowpacked Mountains", "Permafrost Highlands"
		],
	"Pugilist"     : [
		"Clockwork City", "Abandoned Workshop", "Bioforge Basin", "Crumbling Ruins", "Forgotten Temple", "Ancient Battlefield", "Archaeological Dig",
		"Secret Lab", "Agency Black Site", "Synthetic Biosphere", "Origin<UNKNOWN>"
		],
	"Toxic"        : [
		"Still Tidepools", "Thriving Reefs", "Secret Lab", "Restricted Labratory", "Bewitched Glen", "Verdant Plains", "Blooming Valley",
		"Ironwood Deep", "Fungal Vales", "Darkmist Chasm", "Netherbleak Hollow"
		],
	"Ancient"      : [
		"Bewitched Glen", "Darkmist Chasm", "Netherbleak Hollow" "Crumbling Ruins", "Forgotten Temple", "Synthetic Biosphere", "Abandoned Wastes",
		"Forgotten Boneyard", "Retired Military Base", "Monolithic Structures", "Dayless MossWood", "Wyrmscar Ridge"
		],
	"Psychokinetic": [
		"Abandoned Village", "Restricted Labratory", "Secret Lab", "Crumbling Ruins", "Forgotten Temple", "Origin<UNKNOWN>", "Retired Military Base",
		"Condemned HydroPowerDam", "Ironwood Deep", "Monolithic Structures", "Dayless MossWood", "Ghost Town", "Classified Research Facilities",
		],
	"Neutral"      : [ALL_HABITATS],
	"Colorless"    : [ALL_HABITATS]
	}
