# 🎨 GODOT MONSTER TRAINER — 32-Bit Pixel Art Style Guide (v1)

-  *Dex-certified. Bean-approved.*

## 1\. Overall Visual Philosophy

Your game’s aesthetic is 32-bit, fantasy-monster RPG with rich 2-D textures and sprites but presented in a way that feels 2.5-D, likely characterised in a more effective way when considering the following styling terms:

- Fire Emblem: Sacred Stones → Pokemon: Fire Red → Final Fantasy VI → Chrono Trigger → Golden Sun → Octopath Traveler  
- Strong palettes  
- Semi-smooth shading  
- Not too chibi, not too realistic  
- Enough detail to show personality/traits/mutagens  
- A little humorous, a little dark in places

Think:  
“SNES/PSX hybrid with painterly pixels, feels like a world between 2-D and 3-D"

"World textures, pixelart tilesheets built with a strong nod toward a ‘Stardew Valley’ overworld style”

“Dragon Warrior Monsters if it was made for platforms like NDS or GBA.”

#### *- - - Typical Sprite Image Variations:*


| SPRITE TYPE           | RESOLUTION   |                                                                                 NOTES |
|:----------------------|:-------------|--------------------------------------------------------------------------------------:|
| Battle Sprite         | 192 × 192 px |                                              enough room for details without crowding |
| Overworld SpriteSheet | 48 × 48 px   | basic tilesheet (each tile: 48×48px) for creating  dynamic sprites / animating motion |
| Portrait / Dex Entry  | 256 × 256 px |   highly detailed, iconically posed, habitat background, bordered, trading-card style |
| Icon (UI)             | 32 × 32 px   |                                                       minimal but easily recognizable |

## 2\. Palette Rules

##### Base Palette

* \~32–40 usable colors total  
* 4–6 colors per major hue  
* High contrast shadows  
* Slight purple tint to shadows (SNES aesthetic trick)  
* No pure white except for eyes/glints  
* No pure black except for heavy outlines

###### Shading Style

* “Chunked” anti-aliasing  
* 1→2→3 value ramps per material  
* Light source: upper-left

Mutagens may “break” light rules in special cases (e.g. bioluminescent)

## 3\. Design Rules Per Monster Component

#### A. Primary and Secondary Types (Body Plan Base)

Use **primary\_type** and **secondary\_type**** to determine:

* silhouette  
* limb count  
* posture  
* texture  
* muscle/fat distribution  
* natural color families
###### **if provided. Only primary type is guaranteed.
| *Type*        | *Silhouette suggestive guideline; typical, but loosely regulated, visual commonalities between Monster types.*                                                     |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 
| Dread         | unsettling elongated posture, asymmetrical shapes, shadowy presence, exotic anatomical figure, missing or extra physical features                                  |
| Cryoform      | sharp angular shapes, crystalline ice reflections, jagged silhouette, frosty/ aura if an aura prompted                                                             |
| Geomorph      | typically thicker physique, rock-hewn or crystallized structures and silhouettes,  diverse mineral textures/colors                                                 |
| Avian         | upright aerodynamic posture, exaggerated feather forms and colors, enlarged physical attributes such as talons/beak/wingspan                                       |
| Beast         | muscular, quadruped/biped hybrid possible; attempt bipedal form for quadrupeds if it allows more relevance in art style and/or game and battle functionality       |
| Plant         | organic shapes and limbs, leaf/flower/root/petal clusters, often undergrowth or bark textured, rarely bipedal, can be creatively provided with limbs               |
| Mythic        | majestic presence, flowing fur or feathers, intricate details, exotic anatomical ornaments or fancy clothing items                                                 |
| Pugilist      | athletic stance, emphasized fists or striking limbs, bipedal with allowance of creative methods of arms/hands/legs/feet depiction                                  |
| Inferno       | visual evidence of extreme heat but avoiding ‘fire related damage or trauma' feel, smoke tendrils, heat distortion                                                 |
| Aquatic       | smooth textures, fins and gills, fluid posture, ornaments or accessories to increase diversity of typical 'fish' shape, an EXCEPTION to the 'prefer bipedal’ rule  |
| Electric      | jagged aura, statically charged fur/armor/hair, expressions of magnetic fields/electric currents if possible                                                       |
| Psychokinetic | floating elements, large eyes, glowing geometric patterns, species blurs toward humanoid form without losing identity                                              |
| Toxic         | bulbous glands, dripping textures, warning colors, exaggerated fangs/teeth and claws/talons, reptilian inspiration                                                 |
| Insectoid     | segmented carapace, multiple limbs, antennae, alien posture, may present instances where  ‘worm/caterpillar’-like forms where bipedal depictions SHOULD be avoided |
| Ancient       | weathered flesh/armor, fossilized plating, prehistoric anatomy, think ‘revived’ NOT ‘undead’                                                                       |
| N/A           | toss-up,  let AI image generation prove itself, who knows what species could emerge with "type: UNKNOWN"                                                           |

###

#### B. MAJOR MODS and MINOR MODS (Mutagens)

These ALWAYS modify:

* color splashes  
* limb texture  
* aura/glow  
* subtle silhouette shifts

Examples:

- Shadowshroud → *purples/blacks, wispy aura, menacing*  
- Thunderclap → *small sparks, yellow highlights*  
- Flintstone → *embedded rock plates*  
- Sensei *→ athletic, bipedal combat-ready stance*  
- Glacial *→ inertial, sense of deliberate motion, terrain may determine ratio between solid ice / thaw*

#### C. Utility Elements

These (potentially) modify:

* accessories  
* markings  
* behavior/mood in pose  
* subtle glow/aura cues

Examples:

- CosmicInterpreter → *small halos, runes, star particles*  
- Pet Cloud → *floating tiny cloud companion*  
- RuneSlots+1 → *glowing runic circles on body*

#### D. Traits (Triplets)

These **ALWAYS** add visible flair:

- *From your trait engine (examples)*

“Oversized Bandit Mask” → *big mask silhouette*  
“Haunted By Footsteps” → *faint shadow figures*  
“Mute Crown” → *simple floating crown*  
“Allergic to Gold” → *blotchy gold rash spots*  
“Pet Cloud” → *literal small cloud friend*

**An attempt must be made to make every trait directly visible in the sprite**.

## 4\. Pose Rules

All battle sprites follow:

* ¾ perspective  
* Facing toward the player (diagonally)  
* One dominant gesture (raised limb, open mouth, wing flare)  
* Slight idle lean forward as if ready to engage  
* Tail/appendages angled outward to avoid overlapping silhouette
* Reverse/Over-the-Shoulder perspective

Portrait / Catalog Entries follow:

* High detail and attention to specific visual aspects derived from prompt
* Unique posture, action pose
* Thematically parallel to information provided by prompt
* Background/Context based on *habitat** and *type(s)**
* Below the portrait will be text describing Stats, Traits, Personality, etc.
###### * *keywords from the prompt*

## 5\. Balance Between Randomness & Readability

Since generation is random, this art style guide provides balance and consistency within the creative randomness.
	the following rules define such a balance:

* Types + Traits = 60% of the monster's 'visual identity'  
  * Major / Minor Elements = 25%  
  * Utility Elements = 15%   
  
* No sprite should feel “overloaded” → cap at:  
  * 2 major color accents  
  * 1 aura effect  
  * 2 visible trait objects

If a monster rolls too many visuals → prune down to most meaningful elements.  
