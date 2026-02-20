from typing import Dict, Any, Tuple, Iterable
from pathlib import Path
import yaml


def _load_yaml(filename: str) -> Any:
    """
    Load a YAML file located next to this module.
    Args:
                    filename: Relative filename (in the same directory as this module).
    Returns:
                    The Python object produced by yaml.safe_load() for the file contents.
    Raises:
                    FileNotFoundError: If the target file does not exist.
                    yaml.YAMLError: If the file exists but cannot be parsed as valid YAML.
    """

    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_seed_types_data(filename: str) -> Tuple[Dict[str, Any], Dict[str, float]]:
    """
            Load seed type definitions from a YAML file.
    The YAML file should contain a sequence (list) of mappings, each with a
    required "name" key. This function returns a tuple of two dictionaries:
    - types_data: mapping of name -> full item dict
    - types_weighted: mapping of name -> weight (float)
    Args:
            filename: Relative filename (in the same directory as this module).
    Returns:
            A tuple (types_data, types_weighted).
    Raises:
            FileNotFoundError: If the target file does not exist.
            ValueError: If the parsed YAML is not a list, contains entries that are
                    not mappings, or if any entry is missing the required 'name' key.
            yaml.YAMLError: If the YAML cannot be parsed (propagated from yaml.safe_load).
    """

    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        raise ValueError(f"Expected a list of seed type definitions in {filepath}")

    types_data: Dict[str, Any] = {}
    types_weighted: Dict[str, float] = {}

    for item in data:
        if not isinstance(item, dict) or "name" not in item:
            raise ValueError(
                f"Each seed type entry must be a mapping with a 'name' key: {item}"
            )
        name = item["name"]

        types_data[name] = item

        # ensure weight is a float (default 1.0)
        types_weighted[name] = float(item.get("weight", 1.0))

    return types_data, types_weighted


def _load_mods_yaml(filename: str) -> Dict[str, Dict[str, Any]]:
    """
    Load a mutagen definitions file from YAML.
    Expected shape: {mod_name: { ... mod fields ... }}.
    """

    data = _load_yaml(filename)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a mapping of mod definitions in {filename}")
    return data


def _load_weighted_yaml(filename: str) -> Dict[str, float]:
    """
    Load a weighted list from YAML (sequence of mappings with "name" and optional "weight").
    """
    filepath = Path(__file__).parent / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of weighted items in {filename}, got {type(data).__name__}"
        )

    result: Dict[str, float] = {}
    for item in data:
        if not isinstance(item, dict) or "name" not in item:
            raise ValueError(
                f"Each weighted item in {filename} must be a mapping with a 'name' key, got: {item!r}"
            )
        result[item["name"]] = float(item.get("weight", 1.0))
    return result


def _validate_seed_type_data(
    seed_type_data: Dict[str, Any],
    base_stats: Dict[str, Any],
) -> None:
    """
    Validate the structural contract for seed type definitions.
    Args:
                    seed_type_data: The loaded seed type data.
                    base_stats: The base stats dictionary.
    Raises:
                    ValueError: If any seed type definition is invalid.
    """

    for name, entry in seed_type_data.items():
        if not isinstance(name, str) or not name:
            raise ValueError(f"Invalid seed type name: {name!r}")

        attributes = entry.get("attributes", {})
        if not isinstance(attributes, dict):
            raise ValueError(f"'attributes' must be a dict for seed type '{name}'")

        mul = attributes.get("mul", {})
        add = attributes.get("add", {})

        if not isinstance(mul, dict) or not isinstance(add, dict):
            raise ValueError(f"'mul' and 'add' must be dicts for seed type '{name}'")

        for stat, value in mul.items():
            if stat not in base_stats:
                raise ValueError(
                    f"Unknown stat '{stat}' in attributes.mul for seed type '{name}'"
                )
            if not isinstance(value, (int, float)) or value <= 0:
                raise ValueError(
                    f"Invalid multiplier for stat '{stat}' in seed type '{name}': {value}"
                )

        for stat, value in add.items():
            if stat not in base_stats:
                raise ValueError(
                    f"Unknown stat '{stat}' in attributes.add for seed type '{name}'"
                )
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Invalid additive value for stat '{stat}' in seed type '{name}': {value}"
                )

        tags = attributes.get("tags")
        if tags is None:
            raise ValueError(f"'attributes.tags' is required for seed type '{name}'")
        if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
            raise ValueError(
                f"'attributes.tags' must be a list of strings for seed type '{name}'"
            )

        notes = attributes.get("notes")
        if notes is None:
            raise ValueError(f"'attributes.notes' is required for seed type '{name}'")
        if not isinstance(notes, list) or not all(isinstance(n, str) for n in notes):
            raise ValueError(
                f"'attributes.notes' must be a list of strings for seed type '{name}'"
            )
        if len(notes) < 3:
            raise ValueError(
                f"'attributes.notes' must include at least 3 entries for seed type '{name}'"
            )

        habitats = entry.get("habitats", [])
        if habitats is not None:
            if not isinstance(habitats, list) or not all(
                isinstance(h, str) for h in habitats
            ):
                raise ValueError(
                    f"'habitats' must be a list of strings for seed type '{name}'"
                )


def _validate_type_forms(
    forms_by_type: Dict[str, Any],
    seed_type_data: Dict[str, Any],
) -> None:
    """
    Validate type_forms.yaml structure and ensure alignment with seed types.
    Raises ValueError if any violation is found.
    """

    if not isinstance(forms_by_type, dict):
        raise ValueError("type_forms.yaml must be a mapping of type -> forms")

    for type_name, forms in forms_by_type.items():
        if type_name not in seed_type_data:
            raise ValueError(
                f"Type '{type_name}' in type_forms.yaml is not defined in seed_types.yaml"
            )

        if not isinstance(forms, dict):
            raise ValueError(
                f"Forms for type '{type_name}' must be a mapping of form_name -> data"
            )

        for form_name, form_data in forms.items():
            if not isinstance(form_name, str) or not form_name:
                raise ValueError(
                    f"Invalid form name under type '{type_name}': {form_name!r}"
                )

            if not isinstance(form_data, dict):
                raise ValueError(
                    f"Form '{form_name}' under type '{type_name}' must be a mapping"
                )

            weight = form_data.get("weight", 1.0)
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError(
                    f"Invalid weight for form '{form_name}' under type '{type_name}': {weight}"
                )

            notes = form_data.get("notes")
            if notes is not None and not isinstance(notes, str):
                raise ValueError(
                    f"'notes' for form '{form_name}' under type '{type_name}' must be a string"
                )


def _validate_mods(
    mods: Dict[str, Any],
    base_stats: Dict[str, Any],
    seed_types: Iterable[str],
    label: str,
) -> None:
    """
    Validate mutagen dictionaries against the mutagen schema contract.
    """

    if not isinstance(mods, dict):
        raise ValueError(f"{label} must be a mapping of mod_name -> mod definition")

    seed_type_set = set(seed_types)
    for mod_name, mod in mods.items():
        if not isinstance(mod_name, str) or not mod_name:
            raise ValueError(f"{label} has invalid mod name: {mod_name!r}")
        if not isinstance(mod, dict):
            raise ValueError(f"{label} mod '{mod_name}' must be a mapping")

        mul = mod.get("mul", {})
        if mul is not None:
            if not isinstance(mul, dict):
                raise ValueError(f"{label} mod '{mod_name}' mul must be a dict")
            for stat, value in mul.items():
                if stat not in base_stats:
                    raise ValueError(
                        f"{label} mod '{mod_name}' uses unknown stat in mul: {stat}"
                    )
                if not isinstance(value, (int, float)) or value <= 0:
                    raise ValueError(
                        f"{label} mod '{mod_name}' has invalid mul for {stat}: {value}"
                    )

        add = mod.get("add", {})
        if add is not None:
            if not isinstance(add, dict):
                raise ValueError(f"{label} mod '{mod_name}' add must be a dict")
            for stat, value in add.items():
                if stat not in base_stats:
                    raise ValueError(
                        f"{label} mod '{mod_name}' uses unknown stat in add: {stat}"
                    )
                if not isinstance(value, (int, float)):
                    raise ValueError(
                        f"{label} mod '{mod_name}' has invalid add for {stat}: {value}"
                    )

        tags = mod.get("tags", [])
        if tags is not None:
            if not isinstance(tags, list) or not all(
                isinstance(tag, str) for tag in tags
            ):
                raise ValueError(f"{label} mod '{mod_name}' tags must be a list")

        # Validate incompatible_types only (allowed_types removed)
        incompatible = mod.get("incompatible_types", [])
        if incompatible is not None:
            if not isinstance(incompatible, list) or not all(
                isinstance(t, str) for t in incompatible
            ):
                raise ValueError(
                    f"{label} mod '{mod_name}' incompatible_types must be a list of strings"
                )
            unknown = [t for t in incompatible if t not in seed_type_set]
            if unknown:
                raise ValueError(
                    f"{label} mod '{mod_name}' has unknown incompatible_types: {unknown}"
                )

        rarity = mod.get("rarity")
        if rarity is not None:
            if not isinstance(rarity, (int, float)) or float(rarity) <= 0:
                raise ValueError(
                    f"{label} mod '{mod_name}' has invalid rarity: {rarity}"
                )

        synergy_bonus = mod.get("synergy_bonus", {})
        if synergy_bonus is not None:
            if not isinstance(synergy_bonus, dict):
                raise ValueError(
                    f"{label} mod '{mod_name}' synergy_bonus must be a dict"
                )
            for type_name, value in synergy_bonus.items():
                if type_name not in seed_type_set:
                    raise ValueError(
                        f"{label} mod '{mod_name}' has unknown synergy type: {type_name}"
                    )
                if not isinstance(value, (int, float)) or float(value) <= 0:
                    raise ValueError(
                        f"{label} mod '{mod_name}' has invalid synergy for {type_name}: {value}"
                    )


def _validate_type_system(ts: Dict[str, Any]) -> None:
    pcs = ts["primary_clusters"].get("primary_clusters", {})
    pts = ts["primary_types"].get("primary_types", {})

    # primary cluster keys must exist
    for tname, tdef in pts.items():
        cluster = tdef.get("cluster")
        if cluster not in pcs:
            raise ValueError(
                f"Primary type '{tname}' references unknown cluster '{cluster}'"
            )


# -- Type-system manifest (YAML-first, runtime-ingested)
TYPE_SYSTEM_MANIFEST = {
    "primary_clusters": "types/primary_clusters.yaml",
    "primary_types": "types/primary_types.yaml",
    "secondary_clusters": "types/secondary_clusters.yaml",
    "secondary_types": "types/secondary_types.yaml",
    "type_affinities": "types/type_affinities.yaml",
    "type_clusters": "types/type_clusters.yaml",
    "interaction_model": "types/interaction_model.yaml",
    # Choose one canonical interaction file long-term:
    # "cluster_interactions": "types/cluster_interactions.yaml",
}


def _load_manifest(manifest: Dict[str, str]) -> Dict[str, Any]:
    loaded: Dict[str, Any] = {}
    for key, relpath in manifest.items():
        loaded[key] = _load_yaml(relpath)
    return loaded


TYPE_SYSTEM = _load_manifest(TYPE_SYSTEM_MANIFEST)
_validate_type_system(TYPE_SYSTEM)

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


def _normalize_seed_type_data(
    seed_type_data: Dict[str, Any],
) -> Dict[str, Any]:
    """ """
    normalized: Dict[str, Any] = {}

    for type_name, entry in seed_type_data.items():
        attributes = entry.get("attributes", {}) or {}
        mul = attributes.get("mul", {}) or {}
        add = attributes.get("add", {}) or {}

        normalized[type_name] = {
            "weight": float(entry.get("weight", 1.0)),
            "habitats": list(entry.get("habitats", []) or []),
            "attributes": {
                "mul": dict(mul),
                "add": dict(add),
                "tags": list(attributes.get("tags", []) or []),
                "notes": list(attributes.get("notes", []) or []),
            },
        }

    return normalized


# -- Loader
SEED_TYPE_DATA, SEED_TYPES_WEIGHTED = _load_seed_types_data("types/seed_types.yaml")
FORMS_BY_TYPE = _load_yaml("type_forms.yaml")

# -- Normalizer
SEED_TYPES = sorted(list(SEED_TYPES_WEIGHTED.keys()))
SEED_TYPE_DATA = _normalize_seed_type_data(SEED_TYPE_DATA)

# -- Validator
_validate_seed_type_data(SEED_TYPE_DATA, BASE_STATS)
_validate_type_forms(FORMS_BY_TYPE, SEED_TYPE_DATA)

""" Maps frozenset({primary, secondary}) -> multiplicative boost to apply when that pair is being considered. Values >1.0 = positive synergy, values <1.0 = penalty (but use INCOMPATIBLE_TYPE_PAIRS for hard forbids). """
TYPE_SYNERGY_BOOSTS = {
    frozenset(["Spur", "Axiom"]): 1.2,
    frozenset(["Vessel", "Flux"]): 0.7,
    frozenset(["Zenith", "Vessel"]): 1.1,
    frozenset(["Oracle", "Axiom"]): 1.2,
    frozenset(["Nadir", "Echo"]): 0.8,
    frozenset(["Fractal", "Spur"]): 0.7,
    frozenset(["Relic", "Vessel"]): 1.1,
}

INCOMPATIBLE_TYPE_PAIRS = {
    frozenset(["Zenith", "Flux"]),
    frozenset(["Vessel", "Oracle"]),
    frozenset(["Relic", "Nadir"]),
    frozenset(["Axiom", "Zenith"]),
    frozenset(["Fractal", "Axiom"]),
}

MAJOR_MODS = _load_mods_yaml("mutagens/major_mods.yaml")
UTILITY_MODS = _load_mods_yaml("mutagens/utility_mods.yaml")
ALL_MODS = [MAJOR_MODS, UTILITY_MODS]


LEGACY_TYPE_MAP: Dict[str, str] = {
    # Legacy elemental names -> canonical types
    "Argent": "Axiom",
    "Kinetic": "Spur",
    "Chrono": "Fractal",
    "Gaian": "Vessel",
    "Vermillion": "Zenith",
    "Veridian": "Vessel",
    "Azure": "Flux",
    "Aether": "Oracle",
    "Arcane": "Axiom",
    "Abyssal": "Nadir",
    "Apex": "Relic",
    "Sylvan": "Vessel",
    "Inferno": "Zenith",
    "Mineral": "Axiom",
    "Aerial": "Relic",
    "Beast": "Relic",
    "Toxic": "Mire",
    "Electric": "Spur",
    "Frost": "Flux",
    "Brawler": "Relic",
    "Ancient": "Fractal",
    "Mythic": "Oracle",
    "Insect": "Vessel",
    "Astral": "Oracle",
    "Anomalous": "Fractal",
    "Dread": "Nadir",
    # Deprecated type names -> canonical replacements
    "Flow": "Flux",
    "Bastion": "Relic",
    "Rift": "Fractal",
    "Idol": "Zenith",
    "Geist": "Oracle",
    "Bloom": "Vessel",
    "Fracture": "Flux",
}


def _remap_type(name: str) -> str:
    return LEGACY_TYPE_MAP.get(name, name)


def _normalize_mods(mods: Dict[str, Dict[str, Any]]) -> None:
    """
    Summary:
                    Standardizes existing mod datasets to use the new type names.

    Args:
                    mods: Dictionary mapping mod names to their configuration dictionaries.

    Returns:
                    None. The input 'mods' dictionary is modified in place.
    """

    for mod_name, mod in mods.items():
        if not isinstance(mod, dict):
            continue
        # Remove allowed_types normalization (no longer used)
        if "incompatible_types" in mod and isinstance(mod["incompatible_types"], list):
            mod["incompatible_types"] = [
                _remap_type(t) for t in mod["incompatible_types"]
            ]
        if "synergy_bonus" in mod and isinstance(mod["synergy_bonus"], dict):
            new_sb: Dict[str, float] = {}
            for k, v in mod["synergy_bonus"].items():
                new_sb[_remap_type(k)] = v
            mod["synergy_bonus"] = new_sb


def _normalize_habitats(
    habitats_by_type: Dict[str, Dict[str, float]],
) -> Dict[str, Dict[str, float]]:

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


# Final cleanup: deduplicate and sort incompatible_types and synergy_bonus keys
def _cleanup_mods(mods: Dict[str, Dict[str, Any]]) -> None:
    for mod in mods.values():
        # Remove allowed_types cleanup (no longer used)
        if "incompatible_types" in mod and isinstance(mod["incompatible_types"], list):
            seen = []
            for t in mod["incompatible_types"]:
                tnorm = _remap_type(t)
                if tnorm not in seen:
                    seen.append(tnorm)
            mod["incompatible_types"] = sorted(seen)
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

_validate_mods(MAJOR_MODS, BASE_STATS, SEED_TYPES, "major_mods.yaml")
_validate_mods(UTILITY_MODS, BASE_STATS, SEED_TYPES, "utility_mods.yaml")

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
