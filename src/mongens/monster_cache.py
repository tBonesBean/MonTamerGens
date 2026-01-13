from dataclasses import asdict, is_dataclass
import json
import random
import string
from pathlib import Path
from typing import Type

from .monsterseed import MonsterSeed

CACHE_FILE = Path(__file__).parent / "assets" / "generated_monsters.jsonl"
OUTPUT_PATH = Path(__file__).parent / "assets" / "generated_monsters.txt"

def generate_id(length: int = 10) -> str:
    '''
    Summary:
        Generates a random alphanumeric ID of a given length.

    Args:
        length: The desired length of the ID.

    Returns:
        A random alphanumeric string of the specified length.
    '''
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def _load_all_from_cache() -> dict:
    '''
    Summary:
        Loads all monsters from the JSONL cache into a dictionary keyed by unique_id.
        This is an expensive operation and should be used for tools, not for appending.
        
    Returns:
        A dictionary of all monsters in the cache, keyed by their unique_id.
    '''
    if not CACHE_FILE.exists():
        return {}
    
    cache = {}
    with CACHE_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    unique_id = data.get("meta", {}).get("unique_id")
                    if unique_id:
                        cache[unique_id] = data
                except json.JSONDecodeError:
                    print(f"Warning: Skipping malformed line in cache: {line.strip()}")
    return cache

def save_monster(seed: MonsterSeed) -> str:
    '''
    Summary:
        Appends a monster seed to the JSONL cache file and returns its unique ID.
        This is a fast and safe append-only operation.

    Args:
        seed: The MonsterSeed object to save.

    Returns:
        The unique ID of the saved monster.
    '''
    if not is_dataclass(seed):
        raise TypeError("Can only save dataclass objects like MonsterSeed.")

    # If the seed doesn't have a unique_id yet, generate one.
    unique_id = seed.meta.get('unique_id')
    if not unique_id:
        # To ensure the generated ID is unique, we need to check against existing ones.
        # This is the only time we need to read the cache during a save.
        existing_ids = _load_all_from_cache().keys()
        unique_id = generate_id()
        while unique_id in existing_ids:
            unique_id = generate_id()
        seed.meta['unique_id'] = unique_id
    
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(seed), ensure_ascii=False))
        f.write("\n")
    
    return unique_id

def load_monster(unique_id: str) -> MonsterSeed:
    '''
    Summary:
        Loads a monster seed from the cache by its unique ID.
        
    Args:
        unique_id: The unique ID of the monster to load.
        
    Returns:
        A MonsterSeed object for the specified monster.
        
    Raises:
        KeyError: If no monster with the given ID is found in the cache.
        ValueError: If the cached data cannot be reconstructed into a MonsterSeed object.
    '''
    # This is now an expensive operation, but necessary for loading a specific monster.
    # For game loading, you'd process this file into an optimized format once.
    cache = _load_all_from_cache()
    monster_data = cache.get(unique_id)
    
    if not monster_data:
        raise KeyError(f"Monster with ID '{unique_id}' not found in cache.")
        
    # Reconstruct the MonsterSeed object from the dictionary
    try:
        return MonsterSeed(**monster_data)
    except TypeError as e:
        # This can happen if the MonsterSeed dataclass changes and the cached data is outdated.
        raise ValueError(f"Could not reconstruct MonsterSeed from cached data for ID '{unique_id}'. Error: {e}")
