from __future__ import annotations
import hashlib
import random
import re
from typing import Iterable, List, Optional, Dict
 
from .monsterseed import MonsterSeed

"""
Deterministic name generator for MonsterGenerators — updated for:
 - secondary_type awareness (combines type biases)
 - epithet selection based on applied mutagens (utility and major)
 - compatibility with MonsterSeed that uses `mutagens` (dict with 'major'/'utility')
 - robust fallbacks if older attributes exist
"""

# -----------------------
# Syllable / epithets data
# -----------------------
_SYLLABLE_CHAIN = {
    "start": {
        "b": 5,
        "br": 3,
        "bl": 3,
        "c": 6,
        "ch": 4,
        "cl": 3,
        "cr": 3,
        "d": 5,
        "dr": 3,
        "f": 4,
        "fr": 3,
        "g": 4,
        "gr": 3,
        "h": 3,
        "j": 2,
        "k": 4,
        "kr": 2,
        "l": 5,
        "m": 5,
        "n": 5,
        "p": 5,
        "pr": 3,
        "q": 1,
        "r": 5,
        "s": 6,
        "sh": 3,
        "st": 4,
        "t": 6,
        "tr": 3,
        "v": 3,
        "w": 3,
        "y": 2,
        "z": 2,
        "a": 8,
        "e": 8,
        "i": 7,
        "o": 8,
        "u": 7,
    },
    "consonant": {
        "n": 8,
        "m": 7,
        "r": 9,
        "s": 9,
        "th": 4,
        "k": 7,
        "l": 8,
        "d": 7,
        "t": 8,
        "sh": 5,
        "x": 3,
        "z": 4,
        "b": 6,
        "c": 6,
        "f": 5,
        "g": 5,
        "p": 6,
        "v": 4,
    },
    "vowel": {
        "a": 10,
        "e": 10,
        "i": 9,
        "o": 10,
        "u": 9,
        "y": 4,
        "ae": 2,
        "ai": 2,
        "au": 2,
        "ea": 2,
        "io": 2,
        "ea": 2,
        "ai": 2,
        "ou": 2,
        "ua": 2,
        "ya": 1,
        "ye": 1,
        "yo": 1,
    },
}

# Type-biased syllables - simplified to prefixes and suffixes
_TYPE_FLAVORS = {
    "Insect": {
        "prefixes": ["Vesp", "Myr", "For", "Tikk", "Skor"],
        "suffixes": ["ix", "ula", "opter", "nid"],
    },
    "Aerial": {
        "prefixes": ["Zephyr", "Aer", "Gale", "Corv", "Strato"],
        "suffixes": ["ix", "alon", "or", "wing"],
    },
    "Sylvan": {
        "prefixes": ["Verd", "Fol", "Bry", "Thall", "Myco"],
        "suffixes": ["ian", "us", "flora", "root"],
    },
    "Astral": {
        "prefixes": ["Ast", "Zor", "Cel", "Cosm", "Psion"],
        "suffixes": ["on", "ith", "ius", "aeon"],
    },
    "Inferno": {
        "prefixes": ["Pyr", "Cyn", "Brax", "Ign", "Sol"],
        "suffixes": ["ar", "is", "flare", "blaze"],
    },
    "Dread": {
        "prefixes": ["Noct", "Umbr", "Gloom", "Murk", "Mal"],
        "suffixes": ["oth", "usk", "gore", "wraith"],
    },
    "Mineral": {
        "prefixes": ["Ter", "Dol", "Gran", "Bas", "Geo"],
        "suffixes": ["on", "ite", "lith", "odon"],
    },
    "Aquatic": {
        "prefixes": ["Aqu", "Mar", "Rill", "Naut", "Thal"],
        "suffixes": ["is", "or", "fin", "tide"],
    },
    "Electric": {
        "prefixes": ["Vol", "Ion", "Arc", "Tes", "Zil"],
        "suffixes": ["ix", "ark", "eon", "volt"],
    },
    "Mythic": {
        "prefixes": ["Luc", "Sol", "Rad", "Div", "Theo"],
        "suffixes": ["ius", "eon", "os", "el"],
    },
    "Toxic": {
        "prefixes": ["Nox", "Vir", "Bligh", "Tox", "Vek"],
        "suffixes": ["ex", "ius", "ile", "spore"],
    },
    "Beast": {
        "prefixes": ["Urs", "Taur", "Lug", "Gruf", "Bar"],
        "suffixes": ["os", "ok", "don", "fang"],
    },
    "Ancient": {
        "prefixes": ["Arch", "Paleo", "Saur", "Foss", "Mega"],
        "suffixes": ["lith", "don", "yx", "raptor"],
    },
    "Frost": {
        "prefixes": ["Cryo", "Glac", "Fri", "Rim", "Gel"],
        "suffixes": ["is", "ix", "eon", "frost"],
    },
    "Brawler": {
        "prefixes": ["Pug", "Brut", "Kno", "Doj", "Fen"],
        "suffixes": ["ox", "unch", "ite", "fist"],
    },
    "Anomalous": {
        "prefixes": ["Omni", "Null", "Eth", "Anom"],
        "suffixes": ["us", "ex", "ion", "oid"],
    },
}

# Mapping of secondary types to adjectival forms for formatted dual-type names.
TYPE_TO_ADJ: Dict[str, str] = {
    "Frost": "Frost",
    "Inferno": "Molten",
    "Mineral": "Ore",
    "Aquatic": "Aquatic",
    "Electric": "Charged",
    "Astral": "Astral",
    "Toxic": "Toxic",
    "Insect": "Chitinous",
    "Aerial": "Sky",
    "Mythic": "Mythic",
    "Beast": "Beastly",
    "Ancient": "Ancient",
    "Dread": "Dread",
    "Brawler": "Brawling",
    "Anomalous": "Anomalous",
    "Sylvan": "Sylvan",
    "Inferno": "Molten",
}

def format_dual_type(primary: str, secondary: Optional[str], style: str = "adj-n") -> str:
    """Format a dual-type label.

    Styles:
      - "adj-n": "SecondaryAdj PrimaryNoun" (default)
      - "hyphen": "Secondary-Primary"
      - "epithet": "Primary, the SecondaryAdj"

    If secondary is falsy, returns the primary.
    Falls back to using the raw secondary string when no adjective mapping exists.
    """
    if not secondary:
        return primary
    adj = TYPE_TO_ADJ.get(secondary, secondary)
    if style == "adj-n":
        return f"{adj} {primary}"
    if style == "hyphen":
        return f"{adj}-{primary}"
    if style == "epithet":
        return f"{primary}, the {adj}"
    return f"{adj} {primary}"


_MAJOR_EPITHETS = {
    "Starwarden": ["the Star-Blessed", "Celestial Guard"],
    "BrightFlare": ["the Blazing", "Cinder-Wake"],
    "ExoSkeleton": ["the Hollow-Bodied", "Carapaced"],
    "DeepEarth": ["Earth-Shaker", "the Deep-Dweller"],
    "Riftwalker": ["the Phase-Dancer", "Rift-Bound"],
    "Obsidian": ["Volcanic-Glass", "the Obsidian"],
    "Bloodforge": ["the Blood-Forged", "Hemo-Fury"],
    "Crystalline": ["the Crystal-Clad", "Gem-Heart"],
    "Cavernborn": ["the Cave-Dweller", "Gloom-Acclimated"],
    "Arctic": ["the Frost-Hardened", "of the Tundra"],
    "BattleScarred": ["the Veteran", "Scar-Covered"],
    "RuneReader": ["the Rune-Carved", "Glyph-Bound"],
    "Cultivated": ["the Domestic", "Garden-Grown"],
    "SuperOrbital": ["the Gravity-Well", "Orbital"],
    "SandCrawler": ["the Dune-Dweller", "Sand-Swept"],
    "Brimstone": ["the Smoldering", "of the Ash"],
    "LoreGuardian": ["the Lore-Keeper", "Scroll-Warden"],
    "Necromance": ["the Soul-Pacted", "Death-Caller"],
    "Paranormal": ["the Phasing", "Incorporeal"],
    "Feralkin": ["the Pack-Hunter", "Feral-Heart"],
    "Shadowshroud": ["the Shadow-Veiled", "Night-Cloaked"],
    "DarkIce": ["the Black-Iced", "of the Dark Frost"],
    "Extrasensory": ["the All-Seeing", "Mind-Reader"],
    "ThunderClap": ["the Sonic", "Storm-Caller"],
    "ArcheoAnomaly": ["the Time-Lost", "Un-Fossilized"],
    "Tectonic": ["Earth-Shored", "the Terran"],
    "Glacial": ["the Glacial", "Ice-Armored"],
    "Voltaic": ["the Sparking", "Volt-Charged"],
    "Noxious": ["the Plagued", "Toxin-Fueled"],
    "Radiant": ["the Holy", "Light-Blessed"],
    "BioLuminous": ["the Glowing", "Photo-Kinetic"],
    "Psychic": ["the Mind-Bender", "Piercing-Gaze"],
    "Solar": ["the Sun-Fired", "Day-Warmed"],
    "Nocturnal": ["the Moon-Shielded", "Night-Dweller"],
    "Chaotic": ["the Unstable", "Wild-Card"],
    "Monolithic": ["the Tremor-Sense", "Monolithic"],
    "Tempest": ["the Gale-Forced", "Storm-Bound"],
    "Shielded": ["the Iron-Clad", "Tower-Shield"],
    "Vulcan": ["the Magma-Plated", "of the Forge"],
    "Atmos": ["the Up-Drafted", "Sky-Dancer"],
    "Abyssal": ["of the Abyss", "Pressure-Bound"],
    "Telekinesis": ["the Mind-Hand", "Kinetic-Force"],
    "Vedic": ["the Ethereal", "Mist-Walker"],
    "Farphase": ["the Phase-Shifter", "Blink-Striker"],
    "Metallic": ["the Metal-Coated", "Alloy-Skin"],
    "Sensei": ["the Master", "Flawless"],
    "Fossilized": ["the Revived", "Fossil-Bound"],
    "BoltThrower": ["the Javelin-Hurler", "Bolt-Caster"],
    "Stormforged": ["the Storm-Bringer", "Tempest-Made"],
    "Sylvan": ["the Ever-Green", "Regrowing"],
    "Shrouded": ["the Shadow-Stepper", "Umbral"],
    "Fey-touched": ["the Mischievous", "Fey-Cursed"],
}
# Mutagen-to-epithet mapping
_UTILITY_EPITHETS = {
    "CosmicInterpreter": ["the Star-Reader", "of Stellar Origin"],
    "Symbiote": ["the Useful", "the Symbiotic"],
    "Ageless": ["the Timeless", "the Ancient", "the Timeworn"],
    "BornLeader": ["the Alpha", "the Commander"],
    "Diviner": ["the Seeker", "Secret-Seer"],
    "InnateGuard": ["the Bodyguard", "Shield-Ally"],
    "Empath": ["the Soothing", "Pulse-Healer"],
    "KeeperOfKeys": ["the Locksmith", "Gate-Keeper"],
    "Historian": ["the Lore-Keeper", "Scribe"],
    "Impossible": ["the Surprise", "Unlikely"],
    "LongSeeker": ["the Tracker", "Treasure-Hunter"],
    "Transient": ["the Wanderer", "Survivalist"],
    "Cartographer": ["the Pathfinder", "Map-Maker"],
    "SuperPositioned": ["the Quantum", "Uncertain"],
    "CombatController": ["the Tactician", "the Disorienting"],
    "Scholar": ["the Studious", "Weakness-Analyzer"],
    "Humanitarian": ["the Field-Medic", "Converter"],
    "Grinder": ["the Determined", "Unrelenting"],
    "NaturalDetector": ["the Scavenger", "Magnetic"],
    "Confidant": ["the Whisperer", "Secret-Keeper"],
    "AntiExtinct": ["the Last-of-Kind", "Endangered"],
    "Alchemist": ["the Transmuter", "Potion-Master"],
    "Geomancer": ["the Earth-Shaper", "Ley-Reader"],
    "Chronomancer": ["the Time-Warper", "Seer"],
    "Forager": ["the Resourceful", "Harvester"],
    "Haggler": ["the Barterer", "Merchant-Friend"],
    "Pathwarden": ["the All-Terrain", "Sure-Footed"],
    "MasterCrafter": ["the Artisan", "Master-Work"],
}

_GENERIC_EPITHETS = [
    "the Wanderer",
    "the Hidden",
    "the Silent",
    "the Brute",
    "the Shard",
    "the Lonesome",
    "the Gleaming",
    "the Hollow",
    "the Forgotten",
    "the Lost",
    "the Sentinel",
]


# -----------------------
# Helpers
# -----------------------
def _stable_seed_int(*parts: object, salt: str = "") -> int:
    joined = "|".join([str(p) for p in parts]) + "|" + salt
    h = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def _weighted_choice(rng: random.Random, choices: dict) -> str:
    total = sum(choices.values())
    r = rng.uniform(0, total)
    upto = 0
    for choice, weight in choices.items():
        if upto + weight >= r:
            return choice
        upto += weight
    return list(choices.keys())[-1]


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s\-]+", "_", s)
    return s


# -----------------------
# Core naming functions
# -----------------------
def deterministic_name(
    idnum: int,
    primary_type: str,
    secondary_type: Optional[str],
    mutagens: dict[str, List[str]],
    style="fantasy",
    syllables: Optional[int] = None,
    salt: str = "",
    max_name_chars: int = 15,
    epithet_prob: float = 0.25,
) -> str:
    """
    Generates a deterministic, pronounceable name using a weighted syllable chain.
    """
    seed_int = _stable_seed_int(
        idnum,primary_type, secondary_type, ",".join(sorted(mutagens.get("utility", []) + sorted(mutagens.get("major", [])))), salt=salt
    )
    rng = random.Random(seed_int)

    # Determine syllable count
    if syllables is None:
        syllables = rng.choices([2, 3, 4], weights=[0.1, 0.65, 0.45])[0]

    name = ""
    # Type-based name generation
    if rng.random() < 0.9:  # 90% chance for type-based name
        primary_flavor = _TYPE_FLAVORS.get(primary_type, _TYPE_FLAVORS[primary_type])
        p_suf = primary_flavor.get("suffixes", [])
        p_pre = primary_flavor.get("prefixes", [])

        if secondary_type and rng.random() < 0.5:
            secondary_flavor = _TYPE_FLAVORS.get(
                secondary_type, _TYPE_FLAVORS[secondary_type]
            )
            s_suf = secondary_flavor.get("suffixes", [])
            s_pre = secondary_flavor.get("prefixes", [])
            flavors_list = {
                "prefixes": p_pre + s_pre,
                "suffixes": p_suf + s_suf,
            }
        else:
            flavors_list = {"prefixes": p_pre, "suffixes": p_suf}

        if flavors_list["prefixes"] and flavors_list["suffixes"]:
            prefix = rng.choice(flavors_list["prefixes"])
            suffix = rng.choice(flavors_list["suffixes"])

            # Mix and match parts
            if rng.random() < 0.5:
                name = prefix + suffix.lower()
            else:
                name = (
                    rng.choice(flavors_list["prefixes"])
                    + rng.choice(flavors_list["suffixes"]).lower()
                )

    # Fallback to syllable chain if type-based failed or by chance
    if not name:
        parts = []
        current_type = "start"
        for _ in range(syllables * 2):  # Generate more parts to choose from
            part = _weighted_choice(rng, _SYLLABLE_CHAIN[current_type])
            parts.append(part)
            current_type = "consonant" if part in "aeiouy" else "vowel"
        name = "".join(parts)

    name = name.capitalize()

    # Cleanup and truncate
    name = re.sub(r"(.)\1{2,}", r"\1\1", name)
    if len(name) > max_name_chars:
        name = name[:max_name_chars]

    # Epithet selection
    epithet = None
    if rng.random() < epithet_prob:
        candidates = []
        # Collect all possible epithets from both major and utility mutagens
        for mutagen_key in mutagens.get("major", []):
            if mutagen_key in _MAJOR_EPITHETS:
                candidates.extend(_MAJOR_EPITHETS[mutagen_key])
        
        for mutagen_key in mutagens.get("utility", []):
            if mutagen_key in _UTILITY_EPITHETS:
                candidates.extend(_UTILITY_EPITHETS[mutagen_key])

        # If we found any candidates, choose one
        if candidates:
            epithet = rng.choice(candidates)
        # Fallback to a generic epithet if no specific ones were found
        else:
            epithet = rng.choice(_GENERIC_EPITHETS)
    
    
    # canonical assembly: prefer ", the <Epithet>" unless epithet already looks like a suffix
    def _epithet_needs_article(e):
        return not re.search(r"[-\s]", e) or e.lower().startswith("the ")

    if epithet:
        epithet_clean = re.sub(r"[^\w\s\-]", "", epithet).strip()
        if "-" in epithet_clean or not _epithet_needs_article(epithet_clean):
            name = f"{name} {epithet_clean}"
        else:
            name = f"{name}, the {epithet_clean}"
    return name


def forge_monster_name(
    seed: MonsterSeed, style: str = "fantasy", salt: str = ""
) -> MonsterSeed:
    """
    Generates a name for a monster and assigns it to the `name` attribute.
    This function modifies the seed object in-place.
    """
    seed.name = _generate_name_from_seed(seed, style, salt)
    return seed


def generate_alternative_names(
    seed: MonsterSeed, count: int = 5, style: str = "fantasy"
) -> List[str]:
    """
    Generates a list of alternative names for a given monster seed.
    This is non-deterministic by design, using a changing salt to get variations.
    """
    names = set()
    # Keep generating until we have the desired number of unique names
    while len(names) < count:
        # By passing a random salt, we get a different name each time.
        salt = str(random.random())
        name = _generate_name_from_seed(seed, style=style, salt=salt)
        names.add(name)
    return sorted(list(names))


def _generate_name_from_seed(seed_obj, style: str = "fantasy", salt: str = "") -> str:
    """
    Accepts a MonsterSeed-like object. Looks for:
      - id or idnum
      - primary_type / secondary_type
      - mutagens dict
    """
    idnum = (
        getattr(seed_obj, "id", None)
        or getattr(seed_obj, "idnum", None)
        or getattr(seed_obj, "seed_id", None)
    )
    if idnum is None:
        raise ValueError("seed_obj must have id or idnum")

    primary = (
        getattr(seed_obj, "primary_type", None)
        or getattr(seed_obj, "type", None)
        or "Anomalous"
    )
    secondary = getattr(seed_obj, "secondary_type", None)

    mutagens = getattr(seed_obj, "mutagens", None) or getattr(
        seed_obj, "applied_mutagens", None
    )
    if not isinstance(mutagens, dict):
        mutagens = {"major": [], "utility": []}

    return deterministic_name(
        int(idnum),
        primary,
        secondary_type=secondary,
        mutagens=mutagens,
        style=style,
        salt=salt,
    )
