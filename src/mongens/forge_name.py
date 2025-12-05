import random, re
from typing import Iterable

from "mongen.pkgs" import "modules, datasets, functions, ..."


# Soft syllable banks; you can expand freely
CORE_ONSETS = ["v", "z", "r", "k", "t", "d", "b", "g", "m", "n", "l", "s", "sh", "ch"]
CORE_NUCLEI = ["a", "e", "i", "o", "u", "ae", "ia", "eo", "ou"]
CORE_CODAS  = ["n", "r", "s", "x", "th", "rk", "sh", "z", "m"]


# src/mongens/name_gen.py
"""
Deterministic name generator for MonsterGenerators — updated for:
 - secondary_type awareness (combines type biases)
 - epithet selection based on applied mutagens (utility and major)
 - compatibility with MonsterSeed that uses `mutagens` (dict with 'major'/'utility')
 - robust fallbacks if older attributes exist
"""

from __future__ import annotations
import hashlib
import random
import re
from typing import Iterable, List, Optional

# -----------------------
# Syllable / epithets data
# -----------------------
_ONSETS = [
    "b", "br", "bl", "c", "ch", "cl", "cr", "d", "dr", "f", "fr", "g", "gr", "h",
    "j", "k", "kr", "l", "m", "n", "p", "pr", "q", "r", "s", "sr", "st", "str",
    "t", "tr", "v", "vr", "w", "y", "z"
]
_NUCLEI = [
    "a", "e", "i", "o", "u", "ae", "io", "ea", "ai", "ou", "ua", "y"
]
_CODAS = [
    "", "n", "m", "r", "s", "th", "k", "lk", "ld", "rt", "sh", "x", "z"
]

TYPE_FLAVOR = {
    "Electric": {
        on=
        "nuclei": 
        "codes": 
        },
    "Aquatic":    dict(on=,
                     nu= co=),
    
    "Mineral":    dict(on=,
                     nu=       co=),
    "Aerial":      dict(on=["zeph", "aer", "gale", "vent"],
                     nu=["e", "ae"],      co=["s", "ph", "l"]),
    "Flora":    dict(on=["ver", "fol", "bry", "thall"],
                     nu=["a", "o", "ia"], co=["s", "yn", "um"]),
    "Dread":   dict(on=
                     nu=,       co=),
    "Mythic":    dict(on=
                     nu=       co=[),
    "
}# Type-biased syllables (you can expand)
_TYPE_SYLLABLE_OVERRIDES = {
    "Insectoid": {
        "onsets": ["ch", "kr", "sc", "sk"],
        "nuclei": ["i", "a", "u"],
        "codas": ["k", "x", "th"],
    },
    "Aerial": {
        "onsets": ["zeph", "aer", "gale", "vent"],
        "nuclei": ["e", "ea", "io", "ae"],
        "codas": ["w", "l", "ph", "s"],
    },
    "Sylvan": {
        "onsets": ["ver", "fol", "bry", "thall"],
        "nuclei": ["a", "o", "ua", "ia"],
        "codas": ["m", "n", "s", "yn", "um"],
    },
    "Astral": {
        "onsets": ["st", "astr", "zor", "cel"],
        "nuclei": ["a", "o", "io"],
        "codas": ["n", "x", "us"],
    },
    "Inferno": {
        "onsets": ["pyr", "cyn", "brax", "ign", "cinder"],
        "nuclei": ["a", "e"],
        "codas": ["r", "x", "zar"]
    },
    "Dread": {
        "onsets": ["noct", "umbr", "gloam", "murk", "mar", "desp"],
        "nuclei": ["o", "u", "oa", "io"],
        "codas:": ["th", "sh", "rn"]
    },
    "Mineral": {
        "onsets": ["ter", "dol", "gran", "bas", "sed", "cav", "tec"],
        "nuclei": ["a", "o"],
        "codas:": ["m", "d", "rum"]
    },
    "Aquatic": {
        "onsets": ["aq", "mar", "rill", "cor", "naut"],
        "nuclei": ["a", "o", "ua"],
        "codas:": ["n", "ra", "rus"]
    },
    "Electric": {
        "onsets": ["vol", "ion", "arc", "tes", "zil", "kap"],
        "nuclei": ["i", "e", "io"],
        "codas:": ["x", "z", "rk", "tr"]
    },
    "Mythic": {
        "onsets": ["luc", "sol", "radi", "lumi"],
        "nuclei": ["i", "e"],
        "codas:": "s", "el", "ar"]
    },
    "Dread": {
        "onsets":
        "nuclei":
        "codas:":
    },
    "Dread": {
        "onsets":
        "nuclei":
        "codas:":
    },# Add more as needed...
}

# Mutagen-to-epithet mapping (utility and major mutagens)
# Keys should match the mod keys you use in MAJOR_MODS / UTILITY_MODS
_MUTAGEN_EPITHETS = {
    # utility mutagens
    "SilverRing": ["the Ringbearer", "Silver-ringed"],
    "Glider": ["Sky-skimmer", "Windborne"],
    # major mutagens
    "Venomous": ["Venom-touched", "the Corrosive"],
    "Tectonic": ["Earth-shored", "the Terran"],
    "Pyroheart": ["Flameborn", "the Ashbringer"],
    # Add your real mutagen keys + epithets here
}

# Element-based fallback epithets (if you still sometimes use elements)
_ELEMENT_EPITHETS = {
    "Ancient": ["the Ancient", "Runecarved", "the Timeworn"],
    "Noxious": ["Venom-touched", "the Corrosive"],
    "Pyro": ["Flameborn", "Ash-shouldered"],
    "Electric": ["Sparked", "the Volt"],
    "Mythic": ["the Grand", "Celestial"],
}

_GENERIC_EPITHETS = [
    "the Wanderer", "the Hidden", "the Silent", "the Brute",
    "the Shard", "the Lonesome", "the Gleaming", "the Hollow",
]

# -----------------------
# Helpers
# -----------------------
def _stable_seed_int(*parts: object, salt: str = "") -> int:
    joined = "|".join([str(p) for p in parts]) + "|" + salt
    h = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def _weighted_choice(rng: random.Random, items: List[str], weights: Optional[List[float]] = None) -> str:
    if not items:
        raise ValueError("No items to choose from")
    if weights is None:
        return rng.choice(items)
    total = sum(weights)
    if total <= 0:
        return rng.choice(items)
    r = rng.random() * total
    upto = 0.0
    for it, w in zip(items, weights):
        upto += w
        if r < upto:
            return it
    return items[-1]


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
    secondary_type: Optional[str] = None,
    mutagens: Optional[Iterable[str]] = None,
    elements: Optional[Iterable[str]] = None,
    style: str = "fantasy",
    syllables: Optional[int] = None,
    salt: str = "",
) -> str:
    """
    Generate a deterministic, pronounceable name with optional epithet biased by mutagens.
    - mutagens: combined list of major + utility mutagen keys (strings)
    - elements: fallback elements list if you still use them
    """
    mutagens = list(mutagens or [])
    elements = list(elements or [])
    # seed uses primary+secondary and sorted mutagens/elements for determinism
    seed_int = _stable_seed_int(idnum, primary_type, secondary_type or "", ",".join(sorted(mutagens)), ",".join(sorted(elements)), salt=salt)
    rng = random.Random(seed_int)

    # syllable count
    if syllables is None:
        syllables = rng.choice([2, 2, 3])

    # Base pools
    onsets = list(_ONSETS)
    nuclei = list(_NUCLEI)
    codas = list(_CODAS)

    # Combine type overrides for primary and secondary (if present)
    def _inject_overrides(t: Optional[str]):
        if not t:
            return
        overrides = _TYPE_SYLLABLE_OVERRIDES.get(t)
        if not overrides:
            return
        if "onsets" in overrides:
            onsets[:0] = overrides["onsets"]  # prepend
        if "nuclei" in overrides:
            nuclei[:0] = overrides["nuclei"]
        if "codas" in overrides:
            codas[:0] = overrides["codas"]

    _inject_overrides(primary_type)
    _inject_overrides(secondary_type)

    # Compose name
    parts: List[str] = []
    for i in range(syllables):
        onset = rng.choice(onsets) if rng.random() < 0.9 else ""
        nucleus = rng.choice(nuclei)
        if i == syllables - 1:
            coda = rng.choice(codas + ["", ""])
        else:
            coda = rng.choice(codas + [""])
        parts.append(onset + nucleus + coda)

    name = "".join(parts).capitalize()
    name = re.sub(r"(.)\1{2,}", r"\1\1", name)
    name = re.sub(r"([aeiouy])([aeiouy])", r"\1\2", name)

    # -----------------------
    # Epithet selection logic (mutagen-driven)
    # -----------------------
    epithet = None

    # 1) Try mutagen-based epithets (priority)
    # We build candidates from mutagens in deterministic order
    if mutagens:
        # deterministic order: sort but keep deterministic randomness for pick
        mut_sorted = sorted(mutagens)
        candidates = []
        for m in mut_sorted:
            if m in _MUTAGEN_EPITHETS:
                candidates.extend(_MUTAGEN_EPITHETS[m])
        if candidates:
            # small deterministic chance per-seed to attach one (use rng)
            if rng.random() < 0.6:  # mutagen epithets are more likely
                epithet = rng.choice(candidates)

    # 2) Fallback: element-based epithet
    if epithet is None and elements:
        for el in sorted(elements):
            if el in _ELEMENT_EPITHETS and rng.random() < 0.35:
                epithet = rng.choice(_ELEMENT_EPITHETS[el])
                break

    # 3) Generic epithet (rare)
    if epithet is None and rng.random() < 0.08:
        epithet = rng.choice(_GENERIC_EPITHETS)

    final = f"{name} {epithet}" if epithet else name
    return final


def name_from_seed(seed_obj, style: str = "fantasy", salt: str = "") -> str:
    """
    Accepts a MonsterSeed-like object. Looks for:
      - id or idnum
      - primary_type / secondary_type
      - mutagens (dict with 'major' and 'utility' lists) OR elements fallback
    """
    idnum = getattr(seed_obj, "id", None) or getattr(seed_obj, "idnum", None) or getattr(seed_obj, "seed_id", None)
    if idnum is None:
        raise ValueError("seed_obj must have id or idnum")

    primary = getattr(seed_obj, "primary_type", None) or getattr(seed_obj, "type", None) or "N/A"
    secondary = getattr(seed_obj, "secondary_type", None)

    # read mutagens if present (it may be a dict {'major':[...], 'utility':[...]} or flat list)
    mutagens_attr = getattr(seed_obj, "mutagens", None) or getattr(seed_obj, "applied_mutagens", None)
    mut_list: List[str] = []
    if isinstance(mutagens_attr, dict):
        for bucket in ("major", "utility"):
            vals = mutagens_attr.get(bucket) or []
            if isinstance(vals, (list, tuple)):
                mut_list.extend([str(x) for x in vals])
    elif isinstance(mutagens_attr, (list, tuple)):
        mut_list = [str(x) for x in mutagens_attr]
    else:
        mut_list = []

    # fallback to seed.elements if available for element-derived epithets
    elements_attr = getattr(seed_obj, "elements", None)
    elem_list: List[str] = []
    if isinstance(elements_attr, dict):
        for v in elements_attr.values():
            if isinstance(v, (list, tuple)):
                elem_list.extend([str(x) for x in v])
    elif isinstance(elements_attr, (list, tuple)):
        elem_list = [str(x) for x in elements_attr]

    return deterministic_name(
        int(idnum), primary, secondary_type=secondary, mutagens=mut_list, elements=elem_list, style=style, salt=salt
    )


# -----------------------
# quick demo when run directly
# -----------------------
if __name__ == "__main__":
    class S: pass
    s = S()
    s.idnum = 42
    s.primary_type = "Insectoid"
    s.secondary_type = "Ancient"
    s.mutagens = {"major": ["Venomous", "Tectonic"], "utility": ["SilverRing"]}
    print(name_from_seed(s))
