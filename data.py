from typing import Dict, List, Any, Tuple
from pathlib import Path
import yaml


def _load_yaml(filename: str) -> Any:
    """Loads a generic YAML file."""
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _load_seed_types_data(filename: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """Loads the comprehensive seed types data from a YAML file."""
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    types_data = {item['name']: item for item in data}
    types_weighted = {item['name']: item.get('weight', 1.0) for item in data}
    
    return types_data, types_weighted

def _load_weighted_yaml(filename: str) -> Dict[str, float]:
    """Loads a YAML file of {'name': str, 'weight': float} into a dict for weighted_choice."""
    data = _load_yaml(filename)
    return {item['name']: item.get('weight', 1.0) for item in data if 'name' in item}

# -- Load data from YAML files
SEED_TYPE_DATA, SEED_TYPES_WEIGHTED = _load_seed_types_data("seed_types.yaml")
SEED_TYPES = sorted(list(SEED_TYPES_WEIGHTED.keys()))
FORMS_BY_TYPE = _load_yaml("type_forms.yaml")

# -- Baseline stats (can override per species later, after mutagens do # there thing and populate stat boxes)
BASE_STATS: Dict[str, int] = {
    "HP": 100,
    "ATK": 50,
    "DEF": 50,
    "SPATK": 50,
    "SPDEF": 50,
    "SPD": 50,
    "ACC": 95,
    "EVA": 5,
    "LUCK": 10,
}

''' Maps frozenset({primary, secondary}) -> multiplicative boost to apply when that pair is being considered. Values >1.0 = positive synergy, values <1.0 = penalty (but use INCOMPATIBLE_TYPE_PAIRS for hard forbids). '''

TYPE_SYNERGY_BOOSTS = {
    # Remapped legacy type synergies to the new canonical types
    frozenset(["Spur", "Axiom"]): 1.2,    # (Kinetic, Argent)
    frozenset(["Bloom", "Flow"]): 0.7,     # (Gaian, Azure)
    frozenset(["Idol", "Bloom"]): 1.1,     # (Vermillion, Veridian)
    frozenset(["Geist", "Axiom"]): 1.2,   # (Aether, Arcane)
    frozenset(["Dread", "Echo"]): 0.8,     # (Abyssal, Echo)
    frozenset(["Rift", "Spur"]): 0.7,      # (Chrono, Kinetic)
    frozenset(["Bastion", "Bloom"]): 1.1,  # (Apex, Gaian)
}

INCOMPATIBLE_TYPE_PAIRS = {
    frozenset(["Idol", "Flow"]),    # (Vermillion, Azure)
    frozenset(["Bloom", "Geist"]),  # (Gaian, Aether)
    frozenset(["Bastion", "Dread"]),# (Apex, Abyssal)
    frozenset(["Axiom", "Idol"]),   # (Argent, Vermillion)
    frozenset(["Rift", "Axiom"]),   # (Chrono, Arcane)
}

MAJOR_MODS = {
    "Starwarden": {
        "mul": {"SPDEF": 1.28, "LUCK": 1.20, "HP": 1.10},
        "add": {},
        "allowed_types": ["Axiom", "Geist", "Echo"],
        "rarity": 1.3,
        "synergy_bonus": {"Mythic": 1.4},
    },
    "BrightFlare": {
        "mul": {"SPATK": 1.22, "ATK": 1.12, "SPD": 1.05},
        "add": {},
        "tags": ["Burn:Overtime", "Weak:Aquatic", "Cinderwake"],
        "allowed_types": ["Idol", "Spur"],
        "rarity": 0.9,
        "synergy_bonus": {"Idol": 1.5},
    },
    "ExoSkeleton": {
        "mul": {"SPD": 1.18, "EVA": 1.15, "DEF": 1.08},
        "add": {},
        "tags": ["Shell:Echo", "Weak:Tempest", "Hollowbody"],
        "allowed_types": ["Bloom", "Dread", "Rift"],
        "rarity": 0.85,
        "synergy_bonus": {"Insect": 1.3},
    },
    "DeepEarth": {
        "mul": {"HP": 1.25, "DEF": 1.20, "SPD": 0.88},
        "add": {},
        "tags": ["Burrow:Deep", "Weak:Tempest", "StoneSleep"],
        "allowed_types": ["Axiom", "Rift", "Dread"],
        "rarity": 0.9,
        "synergy_bonus": {"Ancient": 1.3},
    },
    "Riftwalker": {
        "mul": {"SPD": 1.22, "LUCK": 1.15, "SPATK": 1.10},
        "add": {"EVA": 5},
        "tags": ["Teleport:Long", "Weak:Metallic", "DimensionalSlip"],
        "allowed_types": ["Geist", "Dread", "Echo"],
        "rarity": 1.2,
        "synergy_bonus": {"Astral": 1.2},
    },
    "Obsidian": {
        "mul": {"DEF": 1.28, "SPDEF": 1.18, "SPD": 0.92},
        "add": {},
        "tags": ["Resist:Astral", "Weak:Tempest", "VolcanicGlass"],
        "allowed_types": ["Axiom", "Idol", "Rift"],
        "rarity": 1.0,
        "synergy_bonus": {"Idol": 1.2},
    },
    "Bloodforge": {
        "mul": {"ATK": 1.28, "HP": 1.12, "DEF": 1.08},
        "add": {},
        "tags": ["Regen:OnHit", "Weak:Radiant", "Hemofury"],
        "allowed_types": ["Axiom", "Dread", "Spur", "Idol"],
        "rarity": 1.4,
        "synergy_bonus": {"Axiom": 1.2, "Idol": 1.2},
    },
    "Crystalline": {
        "mul": {"SPDEF": 1.15},
        "add": {"HP": 10},
        "tags": ["Resist:Mind", "Shatter:OnCrit"],
        "allowed_types": ["Axiom", "Flow", "Geist"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Cavernborn": {
        "mul": {"SPDEF": 1.1, "HP": 1.2},
        "add": {"ACC": 5},
        "tags": ["Accuracy:Dark", "Echolocation"],
        "allowed_types": ["Axiom", "Bastion", "Dread", "Bloom"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Arctic": {
        "mul": {"SPDEF": 1.1, "SPD": 1.08},
        "add": {},
        "tags": ["Slide:Frost", "Resist:Frost"],
        "allowed_types": ["Flow"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "BattleScarred": {
        "mul": {"HP": 1.1, "ATK": 1.05, "DEF": 1.05},
        "add": {},
        "tags": ["Grit", "Endure"],
        "allowed_types": ["Veridian", "Gaian"],
        "rarity": 1.0,
        "synergy_bonus": {"Sylvan": 1.2},
    },
    "RuneReader": {
        "mul": {"SPATK": 1.15, "LUCK": 1.05},
        "add": {},
        "tags": ["RuneSlots:+1", "Empower:Glyph"],
        "allowed_types": ["Axiom", "Rift", "Geist", "Vessel"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Cultivated": {
        "mul": {"HP": 1.15, "SPDEF": 1.05},
        "add": {"HP": 15},
        "tags": ["Heal:Terrain", "Barkskin"],
        "allowed_types": ["Veridian", "Gaian"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "HelioCentric": {
        "mul": {"SPATK": 1.18},
        "add": {},
        "tags": ["Sunflare:Minor", "GravityWell", "RadiantPulse"],
        "allowed_types": ["Rift", "Echo", "Geist", "Axiom", "Dread", "Vessel"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    # SandCrawler removed during migration (deprecated / not thematically fitting)
    "Brimstone": {
        "mul": {"SPATK": 1.15},
        "add": {"LUCK": 5},
        "tags": ["Ignite:Low", "Kindle"],
        "allowed_types": ["Vermillion", "Argent", "Abyssal"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "LoreGuardian": {
        "mul": {"SPDEF": 1.15, "LUCK": 1.05},
        "add": {},
        "tags": ["Action:Flow", "AncientKnowledge"],
        "allowed_types": ["Arcane", "Chrono", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Necromance": {
        "mul": {"SPATK": 1.15, "HP": 0.95},
        "add": {},
        "tags": ["Summon:Undead", "SoulPact"],
        "allowed_types": ["Abyssal", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Paranormal": {
        "mul": {"SPDEF": 1.15, "LUCK": 1.08},
        "add": {},
        "tags": ["Phase", "Incorporeal"],
        "allowed_types": ["Abyssal", "Aether", "Arcane", "Echo"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Feralkin": {
        "mul": {"SPD": 1.1, "ATK": 1.1},
        "add": {},
        "tags": ["Howl:Pack", "Tracker"],
        "allowed_types": ["Apex", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Shadowshroud": {
        "mul": {"SPD": 1.08, "EVA": 1.12},
        "add": {},
        "tags": ["Veil:Dark", "Stealth"],
        "allowed_types": ["Abyssal", "Apex"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "DarkIce": {
        "mul": {"SPDEF": 1.12, "SPATK": 1.05},
        "add": {},
        "tags": ["Slide:Frost", "Frostbite"],
        "allowed_types": ["Azure", "Abyssal", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Extrasensory": {
        "mul": {"SPATK": 1.15, "ACC": 1.08},
        "add": {},
        "tags": ["Precognition", "Mind-Reader"],
        "allowed_types": ["Aether", "Arcane"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "ThunderClap": {
        "mul": {"SPATK": 1.15, "ATK": 1.1},
        "add": {},
        "tags": ["Call:Storm", "SonicBoom"],
        "allowed_types": ["Kinetic", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "ArcheoAnomaly": {
        "mul": {"ATK": 1.1, "SPDEF": 1.1},
        "add": {"EVA": 3, "LUCK": 3},
        "tags": ["Sentience:Inconsistent", "TemporalFlux"],
        "allowed_types": ["Chrono", "Aether", "Echo"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Tectonic": {
        "mul": {"DEF": 1.25, "HP": 1.15, "ATK": 1.10},
        "add": {"DEF": 10},
        "tags": ["Resist:Stormforged", "Terrain:Bonus", "Terraform"],
        "allowed_types": ["Gaian", "Chrono"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Glacial": {
        "mul": {"SPDEF": 1.25, "HP": 1.20, "SPD": 0.90},
        "add": {"SPDEF": 10},
        "tags": ["Resist:Frostbound", "Weak:Tempest", "IceArmor"],
        "allowed_types": ["Azure", "Chrono"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Voltaic": {
        "mul": {"SPD": 1.25, "SPATK": 1.20},
        "add": {"ACC": 5},
        "allowed_types": ["Kinetic", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Noxious": {
        "mul": {"DEF": 1.20, "SPDEF": 1.15, "LUCK": 1.10},
        "add": {},
        "tags": ["DOT:Poison", "Weak:Radiant", "Neurotoxin"],
        "allowed_types": ["Veridian", "Abyssal"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Radiant": {
        "mul": {"SPATK": 1.10, "SPDEF": 1.15},
        "add": {"ACC": 10},
        "tags": ["Cure:Blind", "Weak:Shrouded", "HolyLight"],
        "allowed_types": ["Arcane", "Aether", "Echo"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "BioLuminous": {
        "mul": {"SPD": 1.20, "SPATK": 1.15, "EVA": 1.10},
        "add": {"EVA": 5},
        "tags": ["Glow", "Weak:Dread", "Photosynthesis"],
        "allowed_types": ["Gaian", "Azure", "Veridian"],
        "rarity": 1.0,
        "synergy_bonus": {"Aquatic": 1.2},
    },
    "Psychic": {
        "mul": {"SPATK": 1.25, "LUCK": 1.20, "SPDEF": 1.10},
        "add": {"LUCK": 5},
        "tags": ["Pierce:Barrier", "Weak:Obsidian", "Resist:Anomalous"],
        "allowed_types": ["Arcane", "Aether", "Echo", "Abyssal"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Solar": {
        "mul": {"ATK": 1.20, "SPATK": 1.20, "HP": 1.10},
        "add": {},
        "tags": ["Regen:Day", "Weak:Chaos", "Sunfire"],
        "allowed_types": ["Vermillion", "Aether", "Arcane", "Gaian"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Nocturnal": {
        "mul": {"SPDEF": 1.25, "EVA": 1.15, "HP": 1.10},
        "add": {},
        "tags": ["Regen:Night", "Weak:Solar", "Moonshield"],
        "allowed_types": ["Abyssal", "Apex", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Chaotic": {
        "mul": {"ATK": 1.25, "SPATK": 1.25, "LUCK": 1.25, "HP": 0.90, "ACC": 0.95},
        "add": {},
        "allowed_types": ["Abyssal", "Aether", "Echo"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Monolithic": {
        "mul": {"DEF": 1.20, "ATK": 1.15, "HP": 1.10},
        "add": {},
        "tags": ["Ambush:Burrow", "Weak:Astral", "Tremorsense"],
        "allowed_types": ["Argent", "Chrono", "Apex"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Tempest": {
        "mul": {"SPD": 1.25, "ATK": 1.15},
        "add": {"ACC": 5},
        "tags": ["MultiHit:Storm", "Weak:Crystalline", "GaleForce"],
        "allowed_types": ["Aether", "Kinetic", "Azure"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Shielded": {
        "mul": {"DEF": 1.30, "SPDEF": 1.20, "SPD": 0.85},
        "add": {"DEF": 15},
        "tags": ["Guard:Stagger", "Weak:Shrouded", "Ironclad"],
        "allowed_types": ["Kinetic", "Argent", "Chrono", "Apex"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Vulcan": {
        "mul": {"SPATK": 1.25, "DEF": 1.15},
        "add": {"SPATK": 5},
        "tags": ["Burn:Contact", "Weak:Tempest", "MagmaPlating"],
        "allowed_types": ["Vermillion", "Argent"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Atmos": {
        "mul": {"SPD": 1.20, "EVA": 1.20},
        "add": {"EVA": 10},
        "tags": ["Evade:Aerial", "Weak:Electric", "Updraft"],
        "allowed_types": ["Aether", "Veridian", "Arcane"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Abyssal": {
        "mul": {"HP": 1.25, "SPDEF": 1.20, "SPD": 0.90},
        "add": {},
        "tags": ["FirstStrike:Water", "Weak:Solar", "Pressure"],
        "allowed_types": ["Azure", "Abyssal", "Chrono"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Telekinesis": {
        "mul": {"SPATK": 1.20, "LUCK": 1.15},
        "add": {"ACC": 5},
        "tags": ["Pierce:Mind", "Weak:Ironclad", "MindRead"],
        "allowed_types": ["Geist", "Axiom", "Dread", "Vessel"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Vedic": {
        "mul": {"SPD": 1.15, "SPDEF": 1.15, "EVA": 1.10},
        "add": {"EVA": 5},
        "tags": ["Fog:Field", "Weak:Radiant", "Ethereal"],
        "allowed_types": ["Abyssal", "Aether", "Echo"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Farphase": {
        "mul": {"SPD": 1.20, "LUCK": 1.15},
        "add": {"ACC": 5},
        "tags": ["Blink:Short", "Weak:Obsidian", "PhaseShift"],
        "allowed_types": ["Aether", "Kinetic", "Abyssal"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Metallic": {
        "mul": {"DEF": 1.35, "ATK": 1.15},
        "add": {"DEF": 15},
        "tags": ["Resist:Toxic", "Weak:Electric", "MetalCoat"],
        "allowed_types": ["Argent", "Veridian"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Sensei": {
        "mul": {"ATK": 1.10, "SPATK": 1.10, "ACC": 1.10},
        "add": {"ACC": 10},
        "tags": ["Mentor", "FlawlessTechnique"],
        "allowed_types": ["Kinetic", "Arcane", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "Fossilized": {
        "mul": {"HP": 1.05, "ATK": 1.22, "DEF": 1.20, "SPDEF": 1.12},
        "add": {},
        "tags": ["Ability:Revive", "Resist:Mineral"],
        "allowed_types": ["Chrono", "Argent", "Apex"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    "BoltThrower": {
        "mul": {"ATK": 1.15, "ACC": 1.05},
        "add": {},
        "tags": ["Call:Storm", "Jolt"],
        "allowed_types": ["Kinetic", "Aether"],
        "rarity": 1.0,
        "synergy_bonus": {},
    },
    # Stormforged removed during migration (deprecated / not thematically fitting)
    "Sylvan": {
        "mul": {"HP": 1.20, "SPDEF": 1.20, "SPD": 0.9},
        "add": {"HP": 20},
        "tags": ["Regen:Terrain", "Weak:Inferno", "Photosynthesis"],
        "allowed_types": ["Sylvan", "Toxic", "Aquatic"],
        "rarity": 0.9,
        "synergy_bonus": {"Sylvan": 1.1},
    },
    "Shrouded": {
        "mul": {"EVA": 1.25, "SPD": 1.15, "ATK": 1.10},
        "add": {"EVA": 10},
        "tags": ["Stealth:Shadow", "Weak:Radiant", "Shadowstep"],
        "allowed_types": ["Abyssal", "Aether", "Veridian"],
        "rarity": 1.2,
        "synergy_bonus": {"Dread": 1.4},
    },
    "Fey-touched": {
        "mul": {"LUCK": 1.30, "SPATK": 1.15, "SPD": 1.10},
        "add": {"LUCK": 15},
        "tags": ["Fey-curse", "Weak:Metallic", "Mischief"],
        "allowed_types": ["Arcane", "Gaian", "Veridian", "Aether"],
        "rarity": 1.3,
        "synergy_bonus": {"Mythic": 1.4},
    },
}

UTILITY_MODS = {
    "CosmicInterpreter": {
        "identify_rates": 0.30,
        "quest_bonus": 0.1,
        "tags": ["Identify:Rare", "StarChart"],
        "rarity": 1,
        "allowed_types": ["Axiom", "Geist", "Echo"],
    },
    "Symbiote": {
        "field_heal_ticks": 0.08,
        "ally_heal_ticks": 0.04,
        "tags": ["HealingAura", "Lifebond"],
        "rarity": 1,
        "allowed_types": ["Bloom", "Flow"],
    },
    "Ageless": {
        "exp_mult": 1.15,
        "loot_mult": 1.20,
        "tags": ["Lore:Gates", "AncientWisdom"],
    },
    "BornLeader": {
        "ally_buff": {"ATK": 1.15, "DEF": 1.1},
        "exp_share_bonus": 0.25,
        "tags": ["VeteranPresence", "BattleCry", "Rally"],
    },
    "Diviner": {
        "minimap_reveal": True,
        "loot_mult": 1.1,
        "tags": ["Reveal:Secrets", "Dowsing"],
    },
    "InnateGuard": {
        "ally_buff": {"DEF": 1.15, "SPDEF": 1.15},
        "aggro_redirect": True,
        "tags": ["Bodyguard", "ShieldAlly"],
    },
    "Empath": {
        "ally_heal_on_crit": 0.15,
        "npc_dialog_plus": True,
        "tags": ["Soothing", "HealPulse"],
    },
    "KeeperOfKeys": {
        "unlock_tags": ["Gate:Runic", "Door:Sealed", "Chest:Ancient"],
        "tags": ["Locksmith", "MasterKey"],
    },
    "Historian": {
        "npc_dialog_plus": True,
        "exp_mult": 1.05,
        "tags": ["Diplomacy", "Scribe", "Lorekeeper"],
    },
    "Impossible": {
        "rng_luck_bias": 0.15,
        "double_rolls": ["Crit"],
        "tags": ["WildProcs", "ProbabilityBender"],
        "allowed_types": ["Axiom", "Geist", "Echo"],
    },
    "LongSeeker": {
        "track_rare_spawns": True,
        "track_rare_loot": True,
        "minimap_reveal": True,
        "tags": ["Tracker", "TreasureHunter"],
    },
    "Transient": {
        "camp_bonus": {"Heal%": 0.10, "exp_mult": 1.20},
        "shop_discount": 0.05,
        "tags": ["Wanderer", "Survivalist"],
    },
    "Cartographer": {
        "fast_travel_nodes": True,
        "map_reveal_radius": 1.5,
        "tags": ["Pathfinder", "WorldMap"],
    },
    "SuperPositioned": {
        "double_rolls": ["Loot", "Crit", "Evasion"],
        "rng_luck_bias": 0.1,
        "tags": ["Quantum", "Uncertainty"],
        "allowed_types": ["Geist", "Spur", "Rift"],
    },
    "CombatController": {
        "enemy_opening_debuff": {"SPD": 0.85, "ACC": -10},
        "ally_buff": {"SPD": 1.1},
        "tags": ["Disorient", "Tactician"],
    },
    "Scholar": {
        "ally_exp_mult": 1.20,
        "identify_rates": 0.15,
        "tags": ["Study", "AnalyzeWeakness"],
    },
    "Humanitarian": {
        "loot_to_supplies": 0.25,
        "ally_heal_on_kill": 0.05,
        "tags": ["ConvertLoot", "FieldMedic"],
    },
    "Grinder": {
        "spar_exp_bonus": 0.25,
        "stat_gain_bonus": 0.05,
        "tags": ["Determined", "NoPainNoGain"],
    },
    "NaturalDetector": {
        "pull_items_radius": 15,
        "pull_hidden_radius": 10,
        "tags": ["Magnetism", "ItemScavenger"],
        "allowed_types": ["Axiom", "Bastion", "Spur"],
    },
    "Confidant": {
        "npc_dialog_plus": True,
        "minimap_reveal": True,
        "unlock_tags": ["Path:Hidden"],
        "tags": ["Whispers", "VeiledKnowledge"],
    },
    "AntiExtinct": {
        "self_revive": True,
        "identify_fossils": True,
        "identify_eggs": True,
        "tags": ["LastOfKind", "Endangered"],
        "allowed_types": ["Rift", "Geist"],
    },
    "Alchemist": {
        "loot_to_supplies": 0.15,
        "crafting_bonus": 0.1,
        "tags": ["Transmute", "PotionMaster"],
        "allowed_types": ["Mire", "Bloom", "Geist"],
    },
    "Geomancer": {
        "field_buff": {"DEF": 1.1},
        "unlock_tags": ["Terrain:Blocked"],
        "tags": ["Earthshaper", "LeylineReader"],
        "allowed_types": ["Axiom", "Bloom", "Rift"],
    },
    "Chronomancer": {
        "rng_luck_bias": 0.1,
        "enemy_opening_debuff": {"SPD": 0.95},
        "tags": ["TimeWarp", "Haste", "Slow"],
        "allowed_types": ["Geist", "Geist", "Rift"],
    },
    "Forager": {
        "loot_mult_consumable": 1.5,
        "tags": ["Finds:Herbs", "Finds:Mushrooms", "Resourceful"],
        "allowed_types": ["Bloom", "Bastion"],
    },
    "Haggler": {
        "shop_discount": 0.30,
        "shop_sell_bonus": 0.15,
        "tags": ["Barter", "MerchantFriend"],
    },
    "Pathwarden": {
        "terrain_neg_resist": 0.5,
        "tags": ["Sure-footed", "All-Terrain"],
        "allowed_types": ["Axiom", "Bastion", "Rift"],
    },
    "MasterCrafter": {
        "crafting_bonus": 0.25,
        "crafting_speed_mult": 1.5,
        "tags": ["Artisan", "Tinkerer", "Masterwork"],
        "allowed_types": ["Bastion", "Geist", "Axiom", "Rift"],
    },
}

ALL_MODS = [MAJOR_MODS, UTILITY_MODS]

# Legacy -> new type mapping to help migrate existing mod and habitat data
# Keys that are not present in this map will be left unchanged; this is
# intended to be conservative and iterative so we don't accidentally lose
# semantic intentions during the migration.
LEGACY_TYPE_MAP: Dict[str, str] = {
    "Argent": "Axiom",
    "Kinetic": "Spur",
    "Chrono": "Rift",
    "Gaian": "Bloom",
    "Vermillion": "Idol",
    "Veridian": "Bloom",
    "Azure": "Flow",
    "Aether": "Geist",
    "Arcane": "Axiom",
    "Abyssal": "Dread",
    "Apex": "Bastion",
    "Sylvan": "Bloom",
    "Inferno": "Idol",
    "Mineral": "Axiom",
    "Aerial": "Bastion",
    "Beast": "Bastion",
    "Toxic": "Mire",
    "Electric": "Spur",
    "Frost": "Flow",
    "Brawler": "Bastion",
    "Ancient": "Rift",
    "Mythic": "Geist",
    "Insect": "Bloom",
    "Astral": "Geist",
    "Anomalous": "Rift",
}


def _remap_type(name: str) -> str:
    return LEGACY_TYPE_MAP.get(name, name)


def _normalize_mods(mods: Dict[str, Dict[str, Any]]) -> None:
    """Normalize `allowed_types` and `synergy_bonus` keys in-place."""
    for mod_name, mod in mods.items():
        if not isinstance(mod, dict):
            continue
        if "allowed_types" in mod and isinstance(mod["allowed_types"], list):
            mod["allowed_types"] = [_remap_type(t) for t in mod["allowed_types"]]
        if "synergy_bonus" in mod and isinstance(mod["synergy_bonus"], dict):
            new_sb: Dict[str, float] = {}
            for k, v in mod["synergy_bonus"].items():
                new_sb[_remap_type(k)] = v
            mod["synergy_bonus"] = new_sb


def _normalize_habitats(habitats_by_type: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """Remap habitat keys from legacy type names to new type names and merge weights."""
    new_map: Dict[str, Dict[str, float]] = {}
    for old_type, habs in habitats_by_type.items():
        new_type = _remap_type(old_type)
        if new_type not in new_map:
            new_map[new_type] = {}
        for hab, w in habs.items():
            new_map[new_type][hab] = new_map[new_type].get(hab, 0.0) + float(w)
    return new_map


# Normalize existing mod datasets and habitats to the new canonical types.
_normalize_mods(MAJOR_MODS)
_normalize_mods(UTILITY_MODS)

# Migrate legacy HABITATS_BY_TYPE to remapped keys (safe fallback for old code).
try:
    HABITATS_BY_TYPE = _normalize_habitats(HABITATS_BY_TYPE)
except NameError:
    # If HABITATS_BY_TYPE is not defined (moved earlier), skip silently.
    pass


# Final cleanup: deduplicate and sort allowed_types lists and synergy_bonus keys
def _cleanup_mods(mods: Dict[str, Dict[str, Any]]) -> None:
    for mod in mods.values():
        if "allowed_types" in mod and isinstance(mod["allowed_types"], list):
            seen = []
            for t in mod["allowed_types"]:
                tnorm = _remap_type(t)
                if tnorm not in seen:
                    seen.append(tnorm)
            mod["allowed_types"] = sorted(seen)
        if "synergy_bonus" in mod and isinstance(mod["synergy_bonus"], dict):
            new_sb = {}
            for k, v in mod["synergy_bonus"].items():
                nk = _remap_type(k)
                if nk in new_sb:
                    new_sb[nk] = max(new_sb[nk], v)
                else:
                    new_sb[nk] = v
            mod["synergy_bonus"] = dict(sorted(new_sb.items()))


_cleanup_mods(MAJOR_MODS)
_cleanup_mods(UTILITY_MODS)

def _load_weighted_yaml(filename: str) -> Dict[str, float]:
    """Loads a YAML file of {'name': str, 'weight': float} into a dict for weighted_choice."""
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {item['name']: item.get('weight', 1.0) for item in data if 'name' in item}

PHYSICAL_TRAITS = _load_weighted_yaml("physical_traits.yaml")
HELD_ITEMS = _load_weighted_yaml("held_items.yaml")
KIN_WOUNDS = _load_weighted_yaml("kin_wounds.yaml")

TEMPERS_COUPLED: Dict[str, Dict[str, float]] = {
    "mood": {
        "Shy": 1.0,
        "Bashful": 1.0,
        "Hostile": 0.8,
        "Wary": 0.9,
        "Clever": 0.8,
        "Aloof": 0.9,
        "Warm": 1.0,
        "Cold": 0.9,
        "Guarded": 0.9,
        "Friendly": 1.0,
        "Suspicious": 0.8,
        "Curious": 1.0,
        "Gentle": 1.0,
        "Arrogant": 0.8,
        "Proud": 0.8,
        "Humble": 1.0,
        "Kind": 1.0,
        "Cruel": 0.9,
        "Generous": 1.0,
        "Jealous": 0.8,
        "Envious": 0.8,
        "Patient": 1.0,
        "Impatient": 0.9,
        "Sensitive": 1.0,
        "Indifferent": 0.9,
        "Compassionate": 1.0,
        "Cynical": 0.8,
        "Trusting": 1.0,
        "Distrustful": 0.8,
        "Amiable": 1.0,
        "Resentful": 0.8,
        "Cheerful": 1.0,
        "Irritable": 0.9,
        "Sincere": 1.0,
        "Devious": 0.9,
        "Gracious": 1.0,
        "Petty": 0.8,
        "Tolerant": 1.0,
        "Moody": 0.9,
        "Outgoing": 1.0,
        "Territorial": 0.8,
        "Aggressive": 0.8,
        "Conceited": 0.8,
        "Confident": 0.9,
        "Wise": 0.8,
        "Optimistic": 1.0,
        "Lonely": 0.9,
    },
    "affinity": {
        "Selflessness": 1.0,
        "Warmth": 1.0,
        "Hostility": 0.8,
        "Coyness": 1.0,
        "Honor": 0.8,
        "Glory": 0.8,
        "Boldness": 0.9,
        "Intellect": 0.8,
        "Caution": 0.9,
        "Suspicion": 0.8,
        "Curiosity": 1.0,
        "Gentleness": 1.0,
        "Arrogance": 0.8,
        "Pride": 0.8,
        "Humility": 1.0,
        "Kindness": 1.0,
        "Cruelty": 0.6,
        "Generosity": 1.0,
        "Open-Mindedness": 1.0,
        "Envy": 0.8,
        "Patience": 1.0,
        "Impatience": 0.9,
        "Sensitivity": 1.0,
        "Indifference": 0.9,
        "Compassion": 1.0,
        "Cynicism": 0.8,
        "Trustfulness": 1.0,
        "Distrust": 0.8,
        "Amiability": 1.0,
        "Resentment": 0.8,
        "Cheerfulness": 1.0,
        "Irritability": 0.9,
        "Sincerity": 1.0,
        "Deviousness": 0.8,
        "Graciousness": 1.0,
        "Pettiness": 0.8,
        "Tolerance": 1.0,
    },
}

_ALL_HABITATS_RAW = [
    ("Oldgrowth Marsh", 1.0),
    ("Misty Glades", 1.0),
    ("Thornveil Thicket", 0.9),
    ("Highlands", 1.0),
    ("Smoldering Flats", 0.9),
    ("Collapsed Magma Tubes", 0.8),
    ("Ancient Lavaflows", 0.8),
    ("Whispering Dunes", 0.9),
    ("Glass Caverns", 0.8),
    ("Obsidian Labyrinth", 0.8),
    ("Strikken Ashlands", 0.8),
    ("Mt. Thermallia", 0.8),
    ("Crystalline Cave", 0.8),
    ("Petrified Forest", 0.8),
    ("Glassy Caverns", 0.8),
    ("Skybridge Peaks", 0.8),
    ("Frozen Steppe", 0.9),
    ("Glass Desert", 0.8),
    ("Shattered Plateau", 0.8),
    ("Yittrosian Forest", 0.8),
    ("Thriving Reefs", 1.0),
    ("Sunless Abyss", 0.9),
    ("Alpine Lakes", 0.9),
    ("Moonlit Atolls", 0.8),
    ("Bioluminous Currents", 0.8),
    ("Violent Rapids", 0.9),
    ("Freshwater Springs", 1.0),
    ("Unyielding Cascades", 0.8),
    ("Ennoan Grasslands", 1.0),
    ("Alpine Slopes", 0.9),
    ("Lunaglow Plateau", 0.8),
    ("Riverlands", 1.0),
    ("Dayless Mosswood", 0.8),
    ("Still Tidepools", 1.0),
    ("Starfall Crater", 0.8),
    ("Celestial Spire", 0.8),
    ("Aurora Fields", 0.9),
    ("Echoing Grotto", 0.8),
    ("Astral Terrace", 0.8),
    ("Dread Catacombs", 0.9),
    ("Gloomfen Bogs", 0.9),
    ("AshGlass Tombs", 0.8),
    ("Darkmist Chasm", 0.8),
    ("Abandoned Wastes", 0.8),
    ("Power Plant", 0.9),
    ("Eroding Shipwreck", 1.0),
    ("Ghost Town", 0.8),
    ("Abandoned Village", 1.0),
    ("Concrete Jungle", 1.0),
    ("Rusted Plane Wreckage", 0.9),
    ("Wild Tundra", 1.0),
    ("Frost Caps", 0.9),
    ("Snowcapped Peaks", 1.0),
    ("Frigid Icefields", 0.8),
    ("Snowpacked Mountains", 0.9),
    ("Permafrost Highlands", 0.8),
    ("Clockwork City", 0.8),
    ("Bioforge Basin", 0.8),
    ("Crumbling Ruins", 1.0),
    ("Forgotten Temple", 0.8),
    ("Ancient Battlefield", 0.8),
    ("Archaeological Dig", 0.9),
    ("Agency Black Site", 0.8),
    ("Synthetic Biosphere", 0.8),
    ("Verdant Plains", 1.0),
    ("Blooming Valley", 1.0),
    ("Ironwood Deep", 0.8),
    ("Fungal Vales", 0.9),
    ("Bewitched Glen", 0.8),
    ("Netherbleak Hollow", 0.8),
    ("Wyrmscar Ridge", 0.8),
    ("Restricted Labratory", 0.8),
    ("Secret Lab", 0.8),
    ("Origin<UNKNOWN>", 0.8),
    ("Retired Military Base", 0.9),
    ("Condemned HydroPowerDam", 0.9),
    ("Monolithic Structures", 0.8),
    ("Classified Research Facilities", 0.8),
]

ALL_HABITATS = sorted(list(set([item[0] for item in _ALL_HABITATS_RAW])))

HABITATS_BY_TYPE: Dict[str, Dict[str, float]] = {
    "Sylvan": {
        "Oldgrowth Marsh": 1.0,
        "Misty Glades": 1.0,
        "Bewitched Glen": 0.8,
        "Verdant Plains": 1.0,
        "Blooming Valley": 1.0,
        "Ironwood Deep": 0.8,
        "Fungal Vales": 0.9,
        "Thornveil Thicket": 0.9,
        "Dayless Mosswood": 0.8,
        "Shattered Plateau": 0.8,
        "Wyrmscar Ridge": 0.8,
    },
    "Inferno": {
        "Smoldering Flats": 0.9,
        "Collapsed Magma Tubes": 0.8,
        "Ancient Lavaflows": 0.8,
        "Whispering Dunes": 0.9,
        "Glass Caverns": 0.8,
        "Obsidian Labyrinth": 0.8,
        "Petrified Forest": 0.8,
        "Strikken Ashlands": 0.8,
        "Mt. Thermallia": 0.8,
    },
    "Mineral": {
        "Crystalline Cave": 0.8,
        "Petrified Forest": 0.8,
        "Ancient Lavaflows": 0.8,
        "Whispering Dunes": 0.9,
        "Glass Caverns": 0.8,
        "Thriving Reefs": 1.0,
        "Crumbling Ruins": 1.0,
        "Forgotten Temple": 0.8,
        "Archaeological Dig": 0.9,
    },
    "Aerial": {
        "Skybridge Peaks": 0.8,
        "Frozen Steppe": 0.9,
        "Whispering Dunes": 0.9,
        "Glass Desert": 0.8,
        "Verdant Plains": 1.0,
        "Highlands": 1.0,
        "Shattered Plateau": 0.8,
        "Wyrmscar Ridge": 0.8,
        "Yittrosian Forest": 0.8,
    },
    "Aquatic": {
        "Still Tidepools": 1.0,
        "Thriving Reefs": 1.0,
        "Sunless Abyss": 0.9,
        "Alpine Lakes": 0.9,
        "Moonlit Atolls": 0.8,
        "Bioluminous Currents": 0.8,
        "Violent Rapids": 0.9,
        "Freshwater Springs": 1.0,
        "Unyielding Cascades": 0.8,
    },
    "Beast": {
        "Crystalline Cave": 0.8,
        "Ennoan Grasslands": 1.0,
        "Alpine Slopes": 0.9,
        "Lunaglow Plateau": 0.8,
        "Riverlands": 1.0,
        "Dayless Mosswood": 0.8,
        "Still Tidepools": 1.0,
        "Glass Desert": 0.8,
        "Blooming Valley": 1.0,
        "Ironwood Deep": 0.8,
        "Fungal Vales": 0.9,
        "Thornveil Thicket": 0.9,
    },
    "Mythic": {
        "Starfall Crater": 0.8,
        "Celestial Spire": 0.8,
        "Aurora Fields": 0.8,
        "Echoing Grotto": 0.8,
        "Astral Terrace": 0.8,
        "Synthetic Biosphere": 0.8,
        "Origin<UNKNOWN>": 0.8,
    },
    "Insect": {
        "Echoing Grotto": 0.8,
        "Darkmist Chasm": 0.8,
        "Netherbleak Hollow": 0.8,
        "Whispering Dunes": 0.9,
        "Alpine Lakes": 0.9,
        "Petrified Forest": 0.8,
        "Oldgrowth Marsh": 1.0,
        "Misty Glades": 1.0,
        "Dayless Mosswood": 0.8,
        "Still Tidepools": 1.0,
        "Bioluminous Currents": 0.8,
    },
    "Dread": {
        "Dread Catacombs": 0.8,
        "Gloomfen Bogs": 0.9,
        "AshGlass Tombs": 0.8,
        "Darkmist Chasm": 0.8,
        "Netherbleak Hollow": 0.8,
        "Abandoned Wastes": 0.8,
        "Retired Military Base": 0.9,
        "Monolithic Structures": 0.8,
        "Dayless Mosswood": 0.8,
    },
    "Electric": {
        "Power Plant": 0.9,
        "Eroding Shipwreck": 1.0,
        "Ghost Town": 0.8,
        "Abandoned Village": 1.0,
        "Restricted Labratory": 0.8,
        "Concrete Jungle": 1.0,
        "Retired Military Base": 0.9,
        "Condemned HydroPowerDam": 0.9,
        "Rusted Plane Wreckage": 0.9,
    },
    "Frost": {
        "Wild Tundra": 1.0,
        "Frost Caps": 0.9,
        "Snowcapped Peaks": 1.0,
        "Frigid Icefields": 0.8,
        "Snowpacked Mountains": 0.9,
        "Permafrost Highlands": 0.8,
    },
    "Brawler": {
        "Clockwork City": 0.8,
        "Bioforge Basin": 0.8,
        "Crumbling Ruins": 1.0,
        "Forgotten Temple": 0.8,
        "Ancient Battlefield": 0.8,
        "Archaeological Dig": 0.9,
        "Secret Lab": 0.8,
        "Agency Black Site": 0.8,
        "Synthetic Biosphere": 0.8,
        "Origin<UNKNOWN>": 0.8,
    },
    "Toxic": {
        "Still Tidepools": 1.0,
        "Thriving Reefs": 1.0,
        "Secret Lab": 0.8,
        "Restricted Labratory": 0.8,
        "Bewitched Glen": 0.8,
        "Verdant Plains": 1.0,
        "Blooming Valley": 1.0,
        "Ironwood Deep": 0.8,
        "Fungal Vales": 0.9,
        "Darkmist Chasm": 0.8,
        "Netherbleak Hollow": 0.8,
    },
    "Ancient": {
        "Bewitched Glen": 0.8,
        "Darkmist Chasm": 0.8,
        "Netherbleak Hollow": 0.8,
        "Crumbling Ruins": 1.0,
        "Forgotten Temple": 0.8,
        "Synthetic Biosphere": 0.8,
        "Abandoned Wastes": 0.8,
        "Retired Military Base": 0.9,
        "Monolithic Structures": 0.8,
        "Dayless Mosswood": 0.8,
        "Wyrmscar Ridge": 0.8,
    },
    "Astral": {
        "Abandoned Village": 1.0,
        "Restricted Labratory": 0.8,
        "Secret Lab": 0.8,
        "Crumbling Ruins": 1.0,
        "Forgotten Temple": 0.8,
        "Origin<UNKNOWN>": 0.8,
        "Retired Military Base": 0.9,
        "Condemned HydroPowerDam": 0.9,
        "Ironwood Deep": 0.8,
        "Monolithic Structures": 0.8,
        "Dayless Mosswood": 0.8,
        "Ghost Town": 0.8,
        "Classified Research Facilities": 0.8,
    },
    "Anomalous": dict(_ALL_HABITATS_RAW),
}
