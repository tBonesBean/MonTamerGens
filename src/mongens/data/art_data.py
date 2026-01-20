"""================> STYLE GUIDE for AI IMAGE GENERATION:"""

# --- DESCRIBE THE GLOBAL ART STYLE ---
STYLE_HEADER = (
    "32-bit pixel art for a fantasy RPG monster tamer game, "
    "reminiscent of Fire Emblem Sacred Stones and Golden Sun but, "
    "with a distinct game world art style inspired by Stardew Valley, "
    "that fits seamlessly into a 2.5-D world feel in Godot Engine."
    "2D sprite, rich textures, almost 'next-gen' pixel shading. "
    "World visuals, or all game visuals outside of: menus, system scenes, "
    "and dialogue scenes are intended to feel 2.5-D."
)

TECHNICAL_SPECS = (
    "High contrast, no anti-aliasing, pixel-perfect. "
    "Lighting from upper-left. Shadows have a slight purple tint. "
    "Neutral dark background. If creating in-game/overworld/battle sprite, "
    "background must be an invisible layer, for easier workability in Godot. "
    "Aura effects have a bit of a margin for 'creative liberties' to "
    "be employed; this relying directly on how the aura in question is expected"
    " to move and visually behave in game-world scenes and animatable sprite images. "
    "If the species provided is capable of believably converting to Bipedalism "
    "make it so ONLY if it doesn't lose aesthetic and visual value."
)

POSE_INSTRUCTIONS = (
    "Pose: 3/4 perspective facing diagonally forward with a {mood} expression. "
    "Slight idle lean forward ready to engage. "
    "Limbs and tail angled outward to show clear silhouette."
)

# Translation map for AI image generation; (for abstract concepts to visual descriptions).
VISUAL_TRANSLATION = {
    "mutagens": {
        "NaturalLeader": "wearing a ceremonial sash or medal, confident posture, regal bearing",
        "Diviner": "holding a small crystal orb or dowsing rod",
        "InnateProtector": "carrying a heavy shield or wearing partial plate armor",
        "Ageless": "ancient weathered texture, faded colors",
        "DevotedGuard": "standing in a defensive stance, wearing a gorget",
        "Empath": "soft pink aura, gentle expression",
        "KeeperOfKeys": "wearing a ring of large antique keys",
        "CosmicInterpreter": "surrounded by floating runic symbols and star motes",
        "TruthSpeaker": "wearing a monocle of revealing light",
        "Improbable": "surrounded by floating dice or cards, slightly glitching edges",
        "Seeker": "wearing traveler's goggles, carrying a compass",
        "Homeless": "wearing a tattered scarf, carrying a bindle stick",
        "Omnipresent": "multiple faint afterimages or spectral eyes",
        "Superpositional": "vibrating silhouette, slightly translucent",
        "BattleDisruptor": "holding a discordant bell or noise-maker",
        "DedicatedCoach": "wearing a whistle, holding a clipboard or scroll, encouraging gesture",
        "Humanitarian": "carrying a medical satchel or supply pack",
        "TrainingPartner": "wearing sparring gear or bandages",
        "MagneticAura": "small floating metal scraps orbiting the body",
        "SymbioticNature": "small mushrooms or vines growing on shoulders",
        "SecretKeeper": "wearing a mask or hood, finger to lips gesture",
        "NearExtinction": "spectral transparency, fossilized bone patches",
        "ThornArmor": "covered in sharp thorny vines",
        "SaltSpire": "encrusted with white salt crystals",
        "CavernDweller": "pale skin, large sensitive eyes",
        "DuneSurfer": "wearing sand-colored goggles, dusty texture",
        "EmberFormed": "body made of cooling magma, glowing cracks",
        "CanopyProtected": "covered in broad camouflage leaves",
        "TurbulentFlow": "surrounded by swirling water currents",
        "BergSurfer": "standing on a small ice floe, frosty breath",
        "HelioCentric": "tiny orbiting solar motes and a subtle sunflare aura",
        # legacy alias (kept for compatibility with older assets)
        "SuperOrbital": "tiny orbiting solar motes and a subtle sunflare aura",
        "Stormborn": "sparks jumping between limbs, static hair",
        "VineGatherer": "entangled in flowering vines",
        "Runestone": "glowing runic carving on forehead or chest",
        "Grovebound": "roots growing from feet, bark-like skin patches",
        "Sunbaked": "cracked dry clay texture, sun-bleached colors",
        "Tanglethorn": "wrapped in brambles and thorns",
        "CloudShaper": "standing on or surrounded by small fluff clouds",
        "StarChild": "skin patterned with constellations, starry eyes",
        "Driftwood": "texture of smooth weathered wood and seaweed",
        "Shaleheart": "layered slate-like armor plating",
        "Petrastone": "heavy stone skin texture, slow sturdy stance",
        "Feralwind": "wind-blown fur or hair, surrounded by leaves",
        "Shadowshroud": "cloaked in wisps of dark smoke",
        "DuneSpeak": "surrounded by swirling sand glyphs",
        "BlackIce": "coated in dark translucent ice",
        "DeepRoot": "legs merging into tree roots",
        "ThunderClap": "surrounded by shockwaves and sparks",
        "OnyxCore": "chest containing a dark polished gem",
        "BioLuminescent": "glowing patterns on skin in the dark",
        "ArcheoAnomaly": "glitching between fossil and flesh",
    },
    "traits": {
        "Amnesia": "vacant confused stare",
        "Solar-Phobia": "shielding eyes, wearing a hood",
        "Hovers When It Rains": "levitating slightly off the ground",
        "Receives Cosmic Messages": "antennae or glowing receiver dish",
        "Persistent Hallucinations": "staring at empty space, wide eyes",
        "Terrible Hay Fever": "red nose, holding a handkerchief",
        "Nocturnal": "large pupils, dark coloration",
        "Allergic To Moonlight": "wearing a heavy hood or veil",
        "Speaks In Echoes": "vibrating throat or multiple mouths",
        "Dreams Predict Rainfall": "carrying a small umbrella",
        "Haunted By Laughter": "surrounded by faint ghostly grinning faces",
        "Immune To Cold": "wearing summer clothes in snow",
        "Whispers To Stones": "holding a small glowing rock",
        "Leaves Frost Footprints": "standing on frost patches",
        "Never Casts A Shadow": "no shadow beneath feet",
        "Allergic To Sunlight": "heavily wrapped in cloth",
        "Remembers Past Lives": "wearing mismatched historical armor pieces",
        "Hums When Nervous": "musical notes floating nearby",
        "Can’t Cross Running Water": "hesitant posture",
        "Haunted By A Melody": "surrounded by spectral musical notes",
        "Collects Fallen Stars": "carrying a bag of glowing star fragments",
        "Voice Echoes Twice": "double outline effect",
        "Never Sleeps On Full Moons": "tired eyes, bags under eyes",
        "Sneezes Sparks": "small sparks near nose",
        "Can’t Be Photographed": "blurry face feature",
        "Allergic To Laughter": "grumpy expression",
        "Speaks To Insects": "surrounded by small butterflies or beetles",
        "Forgets Faces Instantly": "looking at a notepad",
        "Dreams In Color Only": "rainbow aura",
        "Can’t Lie": "open honest expression",
        "Floats When Calm": "levitating in lotus position",
        "Allergic To Salt": "dry cracked skin",
        "Voice Attracts Moths": "surrounded by moths",
        "Remembers Every Sound Ever Heard": "large ears",
        "Can’t Touch Iron": "wearing gloves",
        "Speaks To Reflections": "looking into a hand mirror",
        "Terrified Of Silence": "holding a noisemaker",
        "Allergic To Rain": "holding a large leaf umbrella",
        "Can’t Dream": "wide awake staring eyes",
        "Longs To Be Back Among The Stars": "looking up at the sky",
        "Haunted By Footsteps": "faint shadowy footprints following",
        "Can’t Cry": "dry eyes",
        "Reliably Full Of Joy": "big beaming smile",
        "Speaks In Riddles": "mysterious hand gestures",
        "Can’t Remember Names": "wearing a 'Hello My Name Is' tag",
        "Laughs At Thunder": "looking up fearlessly",
        "Allergic To Gold": "wearing silver or copper only",
        "Can’t Whistle": "pursed lips",
        "Dreams Of Drowning": "bubbles floating nearby",
        "Sees Prophecy In Flames": "staring into a torch",
        "Can’t See Stars": "wearing dark glasses",
        "Speaks To Shadows": "talking to own shadow",
        "Can Be Lured By Music": "following a floating note",
    },
}

TYPE_VISUALS = {  # --- 3. BODY PLAN (60% Weight)
    # Canonical types (Lumen Mythos) — body plan guidance
    "Axiom": "ordered, lattice-like silhouettes; geometry-forward bodies with metallic or polished facets",
    "Spur": "compact, kinetic posture; emphasis on striking limbs and angular motion lines",
    "Echo": "repetitive or mirrored anatomy; elements that suggest memory (scars, echoes, layered plating)",
    "Flow": "streamlined, adaptive shapes; tendrils or fin-like elements suggesting fluid motion",
    "Bastion": "massive, grounded silhouettes with broad plates or natural armor; stable posture",
    "Rift": "asymmetry and displaced geometry; parts that seem out-of-phase or split by space",
    "Mire": "sagging, waterlogged forms with clinging textures, moss and residue; slow-moving silhouette",
    "Idol": "ornamental, attention-drawing forms with radiant ornaments and ceremonial shapes",
    "Geist": "ethereal, semi-translucent presence; floating components and soft glowing nodes",
    "Bloom": "organic growth-driven shapes: petals, shoots, canopies, and symbiotic appendages",
    "Vessel": "hollow-forward anatomy with cavities, receptacles, and inward-facing geometry",
    "Nadir": "sinking, heavy silhouettes with downward mass; crushed plates, subsiding posture, cavernous voids",
}

# Palette guidance by canonical type — primary palette, accent suggestions, shadow tint guidance
PALETTE_BY_TYPE = {
    "Axiom": {"primary": "steel-gray", "accent": "pale-cyan", "shadow_tint": "purple"},
    "Spur": {"primary": "crimson", "accent": "amber", "shadow_tint": "deep-purple"},
    "Echo": {"primary": "dusky-lavender", "accent": "silver", "shadow_tint": "indigo"},
    "Flow": {"primary": "teal", "accent": "sea-green", "shadow_tint": "blue-purple"},
    "Bastion": {"primary": "stone-gray", "accent": "moss-green", "shadow_tint": "brown-purple"},
    "Rift": {"primary": "midnight-blue", "accent": "violet", "shadow_tint": "indigo"},
    "Mire": {"primary": "mud-brown", "accent": "sickly-green", "shadow_tint": "olive-purple"},
    "Idol": {"primary": "golden-ochre", "accent": "vermilion", "shadow_tint": "sepia-purple"},
    "Geist": {"primary": "pale-cerulean", "accent": "ghost-white", "shadow_tint": "lavender"},
    "Bloom": {"primary": "leaf-green", "accent": "veridian", "shadow_tint": "purple"},
    "Vessel": {"primary": "hollow-ivory", "accent": "muted-amber", "shadow_tint": "plum"},
    "Nadir": {"primary": "charcoal", "accent": "abyssal-blue", "shadow_tint": "black-purple"},
}
# --- Specific Species Visual Override... because they really are mega abstract ---
SPECIES_VISUAL_OVERRIDES = {
    "Thought-Form Golem": "a humanoid body made of shifting, semi-translucent thought-clouds held together by psychic energy, "
    "with glowing nodes at its joints",
    "Conceptual Entity": "an ever-changing being of pure information, represented by glowing data streams and shifting geometric "
    "shapes, lacking a fixed form",
    "Weeping-Angel Statue": "a stone statue of a grieving angel that appears blurry, as if caught in mid-motion, with streaks of black "
    "ichor running from its eyes",
    "Sun-Eating Fenrir": "a colossal wolf whose fur is made of shadow and smoke, with a gaping maw that seems to consume light, "
    "revealing a starfield within",
}

# --- AGE TRANSLATION MAP ---
"""
AGE_TRANSLATION = {
	Age.YOUNG  : "young, vibrant, smooth skin/scales/fur",
	Age.ADULT  : "mature, strong, well-defined features",
	Age.ANCIENT: "ancient, weathered texture, faded colors, wise expression"
	}
"""
