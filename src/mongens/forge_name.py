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
    "Bloom": {
        "prefixes": [
            "Verd",
            "Fol",
            "Bry",
            "Thall",
            "Myco",
            "Vesp",
            "Myr",
            "For",
            "Tikk",
            "Skor",
            "Flor",
            "Ver",
            "Syl",
            "Germ",
            "Petal",
        ],
        "suffixes": [
            "ian",
            "us",
            "flora",
            "root",
            "ix",
            "ula",
            "opter",
            "nid",
            "ia",
            "is",
            "a",
            "on",
        ],
    },
    "Bastion": {
        "prefixes": [
            "Urs",
            "Taur",
            "Lug",
            "Gruf",
            "Bar",
            "Zephyr",
            "Aer",
            "Gale",
            "Corv",
            "Strato",
            "Pug",
            "Brut",
            "Kno",
            "Doj",
            "Fen",
            "Bulw",
            "Gard",
            "Mur",
            "Fort",
            "Dura",
        ],
        "suffixes": [
            "os",
            "ok",
            "don",
            "fang",
            "ix",
            "alon",
            "or",
            "wing",
            "ox",
            "unch",
            "ite",
            "fist",
            "on",
            "ad",
            "it",
            "um",
            "ark",
        ],
    },
    "Geist": {
        "prefixes": [
            "Luc",
            "Sol",
            "Rad",
            "Div",
            "Theo",
            "Ast",
            "Zor",
            "Cel",
            "Cosm",
            "Psion",
            "Spec",
            "Phant",
            "Ect",
            "Spir",
            "Void",
        ],
        "suffixes": [
            "ius",
            "eon",
            "os",
            "el",
            "on",
            "ith",
            "ius",
            "aeon",
            "is",
            "es",
            "um",
        ],
    },
    "Idol": {
        "prefixes": [
            "Pyr",
            "Cyn",
            "Brax",
            "Ign",
            "Sol",
            "Flare",
            "Crest",
            "Halo",
            "Crown",
            "Ember",
            "Glint",
            "Aure",
            "Blaze",
            "Gleam",
            "Nova",
            "Sign",
            "Radi",
            "Icon",
            "Dei",
            "Sacr",
            "Vener",
            "Glo",
        ],
        "suffixes": [
            "ar",
            "a",
            "on",
            "is",
            "flare",
            "blaze",
            "icon",
            "beacon",
            "mantle",
            "radiant",
            "crest",
            "prism",
            "glory",
            "brand",
            "sigil",
            "aura",
            "us",
            "or",
        ],
    },
    "Dread": {
    "Nadir": {
        "prefixes": [
            "Noct",
            "Umbr",
            "Gloom",
            "Murk",
            "Mal",
            "Grim",
            "Maw",
            "Night",
            "Dread",
            "Ruin",
            "Wraith",
            "Sable",
            "Shroud",
            "Grave",
            "Pall",
            "Abys",
            "Sub",
            "Infra",
            "Low",
            "Prof",
        ],
        "suffixes": [
            "oth",
            "usk",
            "gore",
            "wraith",
            "stalker",
            "omen",
            "gloom",
            "devourer",
            "bane",
            "maw",
            "shade",
            "howl",
            "dusk",
            "reap",
            "ir",
            "um",
            "on",
            "us",
            "is",
        ],
    },
    "Axiom": {
        "prefixes": [
            "Ter",
            "Dol",
            "Gran",
            "Bas",
            "Geo",
            "Lex",
            "Ordo",
            "Prime",
            "Rule",
            "Null",
            "Axio",
            "Regu",
            "Canon",
            "Index",
            "Axi",
            "Logic",
            "Grid",
            "Sect",
            "Core",
            "Sig",
            "Rank",
            "Reg",
            "Ortho",
            "Legis",
            "Stat",
        ],
        "suffixes": [
            "us",
            "on",
            "ite",
            "lith",
            "odon",
            "core",
            "frame",
            "sentinel",
            "bound",
            "matrix",
            "schema",
            "axis",
            "node",
            "vector",
            "lock",
            "ward",
            "meter",
            "is",
            "os",
            "um",
        ],
    },
    "Flow": {
        "prefixes": [
            "Cryo",
            "Glac",
            "Fri",
            "Rim",
            "Gel",
            "Aqu",
            "Mar",
            "Rill",
            "Naut",
            "Thal",
            "Flu",
            "Hydr",
            "Liq",
            "Aqua",
            "Curr",
        ],
        "suffixes": [
            "is",
            "or",
            "fin",
            "tide",
            "is",
            "ix",
            "eon",
            "frost",
            "us",
            "a",
            "os",
            "on",
        ],
    },
    "Spur": {
        "prefixes": [
            "Vol",
            "Ion",
            "Arc",
            "Tes",
            "Zil",
            "Rend",
            "Bolt",
            "Imp",
            "Vel",
            "Celer",
            "Rush",
            "Fang",
            "Thrust",
            "Sunder",
            "Break",
            "Raze",
            "Crash",
            "Skew",
            "Pike",
            "Drive",
            "Volt",
            "Dart",
        ],
        "suffixes": [
            "ex",
            "ix",
            "ark",
            "eon",
            "volt",
            "lash",
            "strike",
            "flare",
            "drive",
            "claw",
            "rush",
            "rend",
            "dash",
            "cleave",
            "pierce",
            "bolt",
            "maul",
            "ax",
            "is",
            "us",
        ],
    },
    "Mire": {
        "prefixes": [
            "Nox",
            "Vir",
            "Bligh",
            "Tox",
            "Vek",
            "Stag",
            "Bog",
            "Fester",
            "Rot",
            "Sludge",
            "Rot",
            "Murk",
            "Silt",
            "Fume",
            "Grime",
            "Mold",
            "Blight",
            "Seep",
            "Gore",
            "Filth",
        ],
        "suffixes": [
            "ex",
            "os",
            "ius",
            "ile",
            "spore",
            "husk",
            "ooze",
            "residue",
            "clot",
            "mire",
            "rot",
            "slime",
            "sour",
            "taint",
            "muck",
            "drip",
            "y",
            "is",
            "um",
        ],
    },
    "Rift": {
        "prefixes": [
            "Arch",
            "Paleo",
            "Saur",
            "Foss",
            "Mega",
            "Omni",
            "Null",
            "Eth",
            "Anom",
            "Para",
            "Xeno",
            "Warp",
            "Flux",
            "Dox",
        ],
        "suffixes": [
            "lith",
            "don",
            "yx",
            "raptor",
            "on",
            "ia",
            "is",
            "us",
            "ex",
            "ion",
            "oid",
            "os",
        ],
    },
    "Echo": {
        "prefixes": [
            "Reso",
            "Mem",
            "Pale",
            "Re",
            "Pale",
            "Grav",
            "Mem",
            "Recall",
            "Trace",
            "After",
            "Hush",
            "Rever",
            "Loop",
            "Ghost",
            "Ring",
            "Reson",
            "Refr",
            "Chime",
            "Pulse",
            "Cad",
            "Hark",
            "Vox",
            "Son",
            "Eid",
            "Aft",
            "Murm",
            "Whisp",
            "Whis",
        ],
        "suffixes": [
            "rem",
            "trace",
            "loop",
            "hollow",
            "echo",
            "remnant",
            "reprise",
            "resound",
            "relic",
            "veil",
            "tone",
            "rift",
            "chor",
            "chime",
            "ring",
            "reson",
            "refrain",
            "murmur",
            "reverb",
            "signal",
            "cadence",
            "hymn",
            "call",
            "ic",
            "al",
            "or",
            "is",
            "um",
        ],
    },
    "Vessel": {
        "prefixes": [
            "Holl",
            "Shell",
            "Null",
            "Frame",
            "Vess",
            "Hollow",
            "Vas",
            "Urn",
            "Cask",
            "Cradle",
            "Vault",
            "Husk",
            "Chamber",
            "Crux",
            "Empty",
            "Carap",
            "Womb",
            "Cruc",
            "Sarc",
            "Carb",
            "Coffer",
            "Hol",
            "Cell",
        ],
        "suffixes": [
            "core",
            "ward",
            "vessel",
            "recept",
            "hull",
            "cask",
            "frame",
            "spire",
            "vault",
            "shell",
            "well",
            "urn",
            "crux",
            "capsule",
            "chamber",
            "shroud",
            "um",
            "or",
            "os",
            "is",
            "on",
        ],
    },
    "Azimuth": {
        "prefixes": [
            "Vect",
            "Azi",
            "Comp",
            "Pol",
            "Traj",
        ],
        "suffixes": [
            "or",
            "an",
            "is",
            "ar",
            "ith",
        ],
    },
    "Fracture": {
        "prefixes": [
            "Frag",
            "Rup",
            "Bre",
            "Schis",
            "Clast",
        ],
        "suffixes": [
            "ure",
            "is",
            "os",
            "er",
            "or",
        ],
    },
    "Oracle": {
        "prefixes": [
            "Vis",
            "Proph",
            "Aug",
            "Omen",
            "Scry",
        ],
        "suffixes": [
            "ia",
            "us",
            "or",
            "is",
            "on",
        ],
    },
    "Zenith": {
        "prefixes": [
            "Apex",
            "Sum",
            "Vert",
            "Culm",
            "High",
        ],
        "suffixes": [
            "ia",
            "on",
            "us",
            "is",
            "ar",
        ],
    },
}

# Mapping of secondary types to adjectival forms for formatted dual-type names.
TYPE_TO_ADJ: Dict[str, str] = {
    "Flow": "Flowing",
    "Idol": "Radiant",
    "Axiom": "Ordered",
    "Bloom": "Verdant",
    "Spur": "Charged",
    "Geist": "Ethereal",
    "Bastion": "Stalwart",
    "Rift": "Temporal",
    "Mire": "Miry",
    "Vessel": "Hollow",
    "Dread": "Dread",
    "Nadir": "Abyssal",
    "Echo": "Echoing",
    "Azimuth": "Directed",
    "Fracture": "Fractured",
    "Oracle": "Prophetic",
    "Zenith": "Exalted",
}


def format_dual_type(
    primary: str, secondary: Optional[str], style: str = "adj-n"
) -> str:
    """
    Summary:
        Formats a dual-type label into a human-readable string.

    Args:
        primary: The primary type of the monster.
        secondary: The optional secondary type.
        style: The formatting style to use ('adj-n', 'hyphen', or 'epithet').

    Returns:
        A formatted string for the dual-type. If secondary is not provided,
        it returns the primary type. It falls back to the raw secondary
        string if no adjective mapping exists.
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
    "LumenCrest": [
        "the Lumen-Crowned",
        "the Crest-Bound",
        "the Haloed",
    ],
    "Flowbloom Current": [
        "the Current-Born",
        "the Tide-Bloomed",
        "the Streamlit",
    ],
    "Echoed Memory": [
        "the Remembered",
        "the Memory-Bound",
        "the Reverberant",
    ],
    "Spurforged Pulse": [
        "the Pulse-Driven",
        "the Spur-Forged",
        "the Rushborne",
    ],
    "Bastion Halo": [
        "the Halo-Guard",
        "the Aegis-Bound",
        "the Bastioned",
    ],
    "Riftflare Fracture": [
        "the Rift-Flaring",
        "the Fracture-Born",
        "the Phase-Torn",
    ],
    "Bloomglow Embers": [
        "the Ember-Bloom",
        "the Glow-Touched",
        "the Cinder-Bright",
    ],
    "Geistbound Lattice": [
        "the Lattice-Bound",
        "the Geist-Linked",
        "the Phase-Woven",
    ],
    "Idolflare Beacon": [
        "the Beaconed",
        "the Flare-Crowned",
        "the Stage-Lit",
    ],
    "Flowveil Torrent": [
        "the Veil-Tide",
        "the Torrent-Wrapped",
        "the Flow-Swept",
    ],
    "Sparkborne Artefact": [
        "the Spark-Bound",
        "the Relic-Borne",
        "the Surge-Held",
    ],
    "Tenebral Bloom": [
        "the Gloam-Bloom",
        "the Night-Bloomed",
        "the Shadow-Flowered",
    ],
    "Cascade Prism": [
        "the Prism-Touched",
        "the Cascade-Bright",
        "the Refracted",
    ],
    "Sapphire Spiral": [
        "the Spiral-Bound",
        "the Sapphire-Wound",
        "the Coil-Blessed",
    ],
    "Guardian Resonance": [
        "the Resonant Guard",
        "the Ward-Bound",
        "the Sentinel-Linked",
    ],
    "Echoisle Whisper": [
        "the Isle-Whispered",
        "the Echo-Woken",
        "the Hush-Bound",
    ],
    "Spiralbound Lash": [
        "the Spiral-Lashed",
        "the Coil-Strike",
        "the Wind-Wound",
    ],
    "Twilight Bloom": [
        "the Twilight-Bloomed",
        "the Dusk-Florescent",
        "the Gloaming",
    ],
    "Axiom Concord": [
        "the Concordant",
        "the Ordered Voice",
        "the Axiom-Bound",
    ],
    "Lumenrift Shard": [
        "the Shard-Born",
        "the Rift-Glinted",
        "the Fractured Light",
    ],
    "Radiant Choir": [
        "the Choir-Bound",
        "the Radiant Voice",
        "the Hymn-Lit",
    ],
    "Gloamsteel Ward": [
        "the Gloam-Steel",
        "the Dark-Warded",
        "the Iron-Gloam",
    ],
    "Flowrift Surge": [
        "the Surge-Driven",
        "the Rift-Streamed",
        "the Flow-Split",
    ],
    "Dreadmaw Eclipse": [
        "the Eclipse-Bitten",
        "the Umbral Maw",
        "the Night-Devourer",
    ],
    "Mirebound Rot": [
        "the Mire-Bound",
        "the Rot-Wreathed",
        "the Bog-Touched",
    ],
    "Vesselcore Hollow": [
        "the Hollow-Core",
        "the Vessel-Bound",
        "the Void-Cased",
    ],
}

_UTILITY_EPITHETS = {
    "Kinweave Meditation": [
        "the Kin-Weaver",
        "the Still-Minded",
        "the Meditative",
    ],
    "Echoing Ledger": [
        "the Ledgered",
        "the Memory-Keeper",
        "the Echo-Archivist",
    ],
    "Flowfield Botanica": [
        "the Field-Bloomed",
        "the Botanist",
        "the Bloomward",
    ],
    "Sparkward Tendril": [
        "the Tethered",
        "the Spark-Ward",
        "the Anchor-Breaker",
    ],
    "Pulseforged Mentor": [
        "the Mentor",
        "the Pulse-Guide",
        "the Kindred-Teacher",
    ],
    "Cohort Harmony": [
        "the Cohort",
        "the Harmonized",
        "the Choir-Bound",
    ],
    "Lantern of Echo": [
        "the Lantern-Bearer",
        "the Beaconed",
        "the Memory-Light",
    ],
    "Lumenic Steward": [
        "the Steward",
        "the Lumen-Crafter",
        "the Attuned",
    ],
    "Resonant Cartographer": [
        "the Cartographer",
        "the Trail-Mapper",
        "the Lore-Charted",
    ],
    "Stormborn Scribe": [
        "the Storm-Scribe",
        "the Record-Bearer",
        "the Spark-Writer",
    ],
    "Quiet Resolve": [
        "the Resolute",
        "the Still-Willed",
        "the Calm-Bound",
    ],
    "Sagewarden Beacon": [
        "the Sagewarden",
        "the Beaconed",
        "the Mentor-Gleam",
    ],
    "Flux Chronicle": [
        "the Flux-Recorder",
        "the Chronicle",
        "the Flow-Noted",
    ],
    "Harmonic Field": [
        "the Harmonizer",
        "the Balanced",
        "the Cohesive",
    ],
    "Truthbinder Ledger": [
        "the Truthbinder",
        "the Oath-Keeper",
        "the Record-Bound",
    ],
    "Siren's Accord": [
        "the Accorded",
        "the Siren-Voiced",
        "the Harmony-Struck",
    ],
    "Stillwater Refuge": [
        "the Refuge-Kept",
        "the Stillwater",
        "the Restful",
    ],
    "Starpath Compass": [
        "the Starpath",
        "the Wayfinder",
        "the Astral-Guided",
    ],
    "Boundless Chorus": [
        "the Chorus-Bound",
        "the Boundless",
        "the Lumen-Voiced",
    ],
    "Prismatic Bulwark": [
        "the Prism-Ward",
        "the Spectrum-Guard",
        "the Bulwarked",
    ],
    "Resonance Surveyor": [
        "the Surveyor",
        "the Gate-Seeker",
        "the Resonant-Guide",
    ],
    "Dreadbound Sigil": [
        "the Sigil-Bound",
        "the Omen-Mark",
        "the Night-Signed",
    ],
    "Mirewick Talisman": [
        "the Talisman-Bearer",
        "the Bog-Warded",
        "the Muck-Charmed",
    ],
    "Vesselborne Reliquary": [
        "the Reliquary",
        "the Hollow-Bearer",
        "the Signal-Bound",
    ],
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
    "the Veiled",
    "the Resonant",
    "the Hollowed",
    "the Warden",
    "the Shard-Bound",
    "the Rifted",
    "the Faded",
    "the Forsaken",
    "the Glimmering",
    "the Bound",
    "the Still",
    "the Echoed",
    "the Fractured",
    "the Unseen",
]


# -----------------------
# Helpers
# -----------------------
def _stable_seed_int(*parts: object, salt: str = "") -> int:
    """
    Summary:
        Creates a deterministic integer seed from a variable number of parts and an optional salt.

    Args:
        *parts: Any number of objects to be converted to strings and included in the seed.
        salt: An optional string to be added to the seed.

    Returns:
        A deterministic integer derived from the hashed input parts.
    """
    joined = "|".join([str(p) for p in parts]) + "|" + salt
    h = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def _weighted_choice(rng: random.Random, choices: dict) -> str:
    """
    Summary:
        Selects a choice from a dictionary of choices with associated weights.

    Args:
        rng: A random.Random object to use for the selection.
        choices: A dictionary where keys are the choices and values are their weights.

    Returns:
        The selected choice as a string.
    """
    total = sum(choices.values())
    r = rng.uniform(0, total)
    upto = 0
    for choice, weight in choices.items():
        if upto + weight >= r:
            return choice
        upto += weight
    return list(choices.keys())[-1]


def slugify(name: str) -> str:
    """
    Summary:
        Converts a string into a slug-like format.

    Args:
        name: The string to be slugified.

    Returns:
        The slugified string, with spaces and hyphens replaced by underscores.
    """
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
    Summary:
        Generates a deterministic, pronounceable name using a weighted syllable chain.

    Args:
        idnum: The monster's ID number.
        primary_type: The primary type of the monster.
        secondary_type: The optional secondary type of the monster.
        mutagens: A dictionary of mutagens applied to the monster.
        style: The naming style to use (e.g., 'fantasy').
        syllables: The number of syllables in the name. If None, it's determined randomly.
        salt: An optional salt to add to the seeding hash.
        max_name_chars: The maximum number of characters for the name.
        epithet_prob: The probability of adding an epithet to the name.

    Returns:
        The generated name as a string.
    """
    seed_int = _stable_seed_int(
        idnum,
        primary_type,
        secondary_type,
        ",".join(
            sorted(mutagens.get("utility", []) + sorted(mutagens.get("major", [])))
        ),
        salt=salt,
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
            s_core = secondary_flavor.get("cores", [])
            flavors_list = {
                "prefixes": p_pre + s_pre,
                "suffixes": p_suf + s_suf,
                "cores": primary_flavor.get("cores", []) + s_core,
            }
        else:
            flavors_list = {"prefixes": p_pre, "suffixes": p_suf, "cores": primary_flavor.get("cores", [])}

        if flavors_list["prefixes"] and flavors_list["suffixes"]:
            prefix = rng.choice(flavors_list["prefixes"])
            suffix = rng.choice(flavors_list["suffixes"])
            core = rng.choice(flavors_list["cores"]) if flavors_list.get("cores") else ""

            # Mix and match parts
            roll = rng.random()
            if roll < 0.4:
                name = prefix + suffix.lower()
            elif roll < 0.7 and core:
                name = prefix + core + suffix.lower()
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


def forge_monster_name(seed: MonsterSeed, salt: str = "") -> str:
    rng = random.Random(
        _stable_seed_int(
            seed.idnum,
            seed.primary_type,
            seed.secondary_type,
            seed.form,
            ",".join(seed.mutagens.get("major", [])),
            salt=salt,
        )
    )

    primary = seed.primary_type
    secondary = seed.secondary_type

    # Map _TYPE_FLAVORS to begin/mid/end
    flavor = _TYPE_FLAVORS.get(primary, {})
    begin_pool = flavor.get("prefixes", [])
    mid_pool = flavor.get("cores", [])
    end_pool = flavor.get("suffixes", [])

    if secondary and secondary in _TYPE_FLAVORS:
        mid_pool += _TYPE_FLAVORS[secondary].get("cores", [])

    begin = rng.choice(begin_pool) if begin_pool else ""
    mid = rng.choice(mid_pool) if mid_pool else ""
    end = rng.choice(end_pool) if end_pool else ""

    name = f"{begin}{mid}{end}".capitalize()
    name = re.sub(r"(.)\1{2,}", r"\1\1", name)

    return name



def generate_alternative_names(
    seed: MonsterSeed, count: int = 5, style: str = "fantasy"
) -> List[str]:
    """
    Summary:
        Generates a list of alternative names for a given monster seed.
        This is non-deterministic by design, using a changing salt to get variations.

    Args:
        seed: The MonsterSeed object to generate names for.
        count: The number of alternative names to generate.
        style: The naming style to use.

    Returns:
        A list of unique alternative names.
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
    Summary:
        Accepts a MonsterSeed-like object and generates a name from it.

    Args:
        seed_obj: The MonsterSeed object to generate a name for.
        style: The naming style to use.
        salt: An optional salt for the name generation.

    Returns:
        The generated name as a string.
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
