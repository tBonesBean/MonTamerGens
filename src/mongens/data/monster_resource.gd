extends Resource
class_name MonsterResource

# Base Info
@export var idnum: int
@export var unique_id: String
@export var monster_name: String # 'name' is a property of Node, so use a different variable
@export var species: String
@export var primary_type: String
@export var secondary_type: String
@export var habitat: String

# Stats
@export_group("Statistics")
@export var hp: int
@export var atk: int
@export var def: int
@export var spatk: int
@export var spdef: int
@export var spd: int
@export var acc: int
@export var eva: int
@export var luck: int

# Abilities & Traits
@export_group("Abilities")
@export var major_mutagens: Array[String]
@export var utility_mutagens: Array[String]
@export var traits: Array[String]
@export var tags: Array[String]

@export_group("Metadata")
@export var resist: Array[String]
@export var weak: Array[String]
