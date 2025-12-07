from dataclasses import asdict, is_dataclass
import json
import random
import string
from pathlib import Path
from typing import Type

from .monsterseed import MonsterSeed

CACHE_FILE = Path(__file__).parent / "assets" / "generated_monsters.json"
OUTPUT_PATH = Path(__file__).parent / "assets" / "mongen_dexentry.txt"

def generate_id(length: int = 10) -> str:
    """Generates a random alphanumeric ID."""
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def _load_cache() -> dict:
    """Loads the monster cache from the JSON file."""
    if not CACHE_FILE.exists():
        return {}
    with open(CACHE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_cache(data: dict):
    """Saves the monster cache to the JSON file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_monster(seed: MonsterSeed) -> str:
    """Saves a monster seed to the cache and returns its unique ID."""
    if not is_dataclass(seed):
        raise TypeError("Can only save dataclass objects like MonsterSeed.")

    cache = _load_cache()
    
    unique_id = generate_id()
    # Ensure the ID is truly unique
    while unique_id in cache:
        unique_id = generate_id()
        
    # Add the unique_id to the monster's meta block for traceability
    seed.meta['unique_id'] = unique_id
    
    cache[unique_id] = asdict(seed)
    _save_cache(cache)
    
    return unique_id

def load_monster(unique_id: str) -> MonsterSeed:
    """Loads a monster seed from the cache by its unique ID."""
    cache = _load_cache()
    monster_data = cache.get(unique_id)
    
    if not monster_data:
        raise KeyError(f"Monster with ID '{unique_id}' not found in cache.")
        
    # Reconstruct the MonsterSeed object from the dictionary
    try:
        return MonsterSeed(**monster_data)
    except TypeError as e:
        # This can happen if the MonsterSeed dataclass changes and the cached data is outdated.
        raise ValueError(f"Could not reconstruct MonsterSeed from cached data for ID '{unique_id}'. Error: {e}")
