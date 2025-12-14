@tool
extends Node

# The path to your generated JSON file within the Godot project
const JSON_FILE_PATH = "res://data/generated_monsters.json"

# The directory where you want to save the monster resource files
const OUTPUT_DIR = "res://monsters/"


func _ready():
	# This function will only be visible in the editor if you
	# add a button or some other UI to trigger the import.
	pass


# You can call this function from a button in the editor.
func import_monsters():
	print("Starting monster import...")

	var file = FileAccess.open(JSON_FILE_PATH, FileAccess.READ)
	if not file:
		printerr("Failed to open JSON file at: ", JSON_FILE_PATH)
		return

	var json_data = JSON.parse_string(file.get_as_text())
	file.close()

	if not json_data or not typeof(json_data) == TYPE_ARRAY:
		printerr("Failed to parse JSON or it's not an array.")
		return

	# Ensure the output directory exists
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(OUTPUT_DIR))

	for monster_dict in json_data:
		var monster_res = MonsterResource.new()
		monster_res.unique_id = monster_dict["meta"]["unique_id"]
		monster_res.monster_name = monster_dict["name"]
		monster_res.species = monster_dict["species"]
		# ... map all other fields from the dictionary to the resource ...
		monster_res.hp = monster_dict["stats"]["HP"]
		monster_res.atk = monster_dict["stats"]["ATK"]
		# etc.

		var save_path = OUTPUT_DIR.path_join(monster_res.unique_id + ".tres")
		var error = ResourceSaver.save(monster_res, save_path)
		if error != OK:
			printerr("Failed to save resource for monster: ", monster_res.unique_id)

	print("Monster import finished!")
