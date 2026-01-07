# The Backrooms - Modular Engine

A from-scratch 3D engine with destructible walls and pixel debris physics.

## File Structure

```
├── config.py          # All configuration constants
├── debris.py          # Debris physics system
├── procedural.py      # Zone generation (5 types)
├── textures.py        # Procedural texture generation
├── audio.py           # Procedural sound generation
├── raycasting.py      # Ray-triangle intersection
├── save_system.py     # JSON save/load system
├── engine.py          # Main 3D engine (2000+ lines)
└── main.py            # Game loop and UI
```

## Module Responsibilities

### `config.py` - Configuration Hub
All tunable constants in one place:
- Display settings (resolution, FPS, fullscreen)
- Colors (blue/yellow aesthetic)
- Physics (speeds, jump strength, gravity)
- Camera (heights, smoothing, FOV)
- World generation (zone sizes, wall dimensions)
- Effects (head bob, fog, flicker)
- Audio settings

**When to edit**: Tuning gameplay feel, adjusting visual style, changing world density

### `debris.py` - Debris Physics
Individual pixel-sized debris particles with:
- Physics simulation (velocity, gravity, collisions)
- Lifetime management (age-based cleanup)
- Settling detection (stops moving when on floor)
- Screen projection for rendering

**When to edit**: Changing debris behavior, particle count, physics constants

### `procedural.py` - Zone System
Five zone types with different properties:
- `normal` - Balanced spacing
- `dense` - Tight corridors
- `sparse` - Open areas
- `maze` - High wall density
- `open` - Minimal obstacles

Each zone has color tints and generation parameters.

**When to edit**: Adding new zone types, adjusting zone distribution

### `textures.py` - Texture Generation
Procedurally generates all textures at runtime:
- `generate_carpet_texture()` - Blue noisy floor
- `generate_ceiling_tile_texture()` - Patterned ceiling
- `generate_wall_texture()` - Yellow walls with stripes
- `generate_pillar_texture()` - Bright yellow pillars

**When to edit**: Changing visual appearance, adding texture variations

### `audio.py` - Sound Synthesis
All sounds generated from waveform synthesis:
- `generate_backrooms_hum()` - Ambient drone
- `generate_footstep_sound()` - Distant footsteps
- `generate_player_footstep_sound()` - Player's footsteps
- `generate_crouch_footstep_sound()` - Quieter crouched steps
- `generate_electrical_buzz()` - Ceiling light buzz
- `generate_destroy_sound()` - Wall destruction

**When to edit**: Tuning sound design, adding new sound effects

### `raycasting.py` - Intersection Math
Möller–Trumbore algorithm for ray-triangle intersection.
Used for detecting which wall the player is looking at.

**When to edit**: Adding new raycasting features, optimizing detection

### `save_system.py` - Persistence
JSON-based save/load system:
- Multiple save slots (1-5)
- Stores player position, rotation, destroyed walls, playtime
- World seed preservation

**When to edit**: Adding new saveable data, changing save format

### `engine.py` - Core Engine
The heart of the system (complete implementation):
- **Initialization**: Texture generation, state setup
- **Render scaling**: Performance mode (0.5x/1.0x)
- **Zone management**: Procedural zone caching
- **Raycasting**: Wall targeting from screen center
- **Destruction**: Wall removal + debris spawning (1200 particles)
- **Sound system**: Directional audio, footstep timing
- **Visual effects**: Fog, zone tinting, surface noise, flickering
- **Collision**: Player-wall collision with doorways
- **Player update**: Movement, jumping, crouching, head bob
- **Camera**: Smoothing, transforms, projection
- **Rendering**: Polygon clipping, depth sorting, debris rendering
- **World generation**: Procedural walls, doorways, hallways
- **Geometry**: Floor/ceiling tiles, wall segments with baseboards

**When to edit**: Core gameplay changes, rendering optimizations

### `main.py` - Game Loop
Ties everything together:
- Pygame initialization
- Engine creation
- Event handling (keyboard, mouse)
- UI rendering (FPS, position, help)
- Save/load triggers (F5/F9)

**When to edit**: UI changes, adding new input controls

## Design Philosophy

Built from first principles following the "defeat bugs by cheating them" approach:

1. **One responsibility per file** - Easy to locate issues
2. **No circular dependencies** - Clean import chain
3. **Constants isolated** - Tune without touching logic
4. **Pure math functions** - Camera transforms have no side effects
5. **State contained** - Engine owns all game state

## Usage

```bash
python main.py
```

## Controls

### Movement
- **WASD** - Move
- **SHIFT** - Run
- **C** - Crouch (toggle)
- **SPACE** - Jump

### Camera
- **M** - Toggle mouse look
- **JL** - Keyboard turn
- **Mouse** - Look around (when mouse look enabled)

### Actions
- **LEFT CLICK** or **E** - Destroy wall (aim crosshair at wall)

### System
- **F5** - Quick save (slot 1)
- **F9** - Quick load (slot 1)
- **R** - Toggle performance mode (0.5x/1.0x render scale)
- **H** - Toggle help overlay
- **ESC** - Exit (or release mouse if captured)

## Features

### Destructible Walls
- Raycasting to detect targeted wall
- Walls break into 250-1200 pixel debris
- Debris has realistic physics (gravity, collision, settling)
- Distance-based rendering (closer = bigger pixels)
- Automatic cleanup (age-based, distance-based)
- Hard cap at 12,000 debris particles

### Procedural World
- Infinite grid-based world
- 5 different zone types with varying density
- Procedural doorways and hallways
- Deterministic generation from seed

### Physics
- Jump mechanics with gravity
- Crouch system with smooth transitions
- Head bob animation synced to footsteps
- Camera shake for atmosphere
- Collision detection with destroyed wall awareness

### Visual Effects
- Zone-based color tinting
- Surface noise for texture variation
- Ambient occlusion on walls
- Optional fog system
- Light flickering
- Smooth camera interpolation

### Audio
- Ambient droning hum
- Directional sound system
- Player footsteps synced to animation
- Different sounds for walking/running/crouching
- Distant footstep ambience
- Electrical buzz
- Wall destruction sound

### Save System
- JSON-based persistence
- 5 save slots
- Stores position, rotation, destroyed walls, playtime
- World seed preservation for deterministic regeneration

## Technical Details

- **Coordinate system**: Y-up, right-handed
- **Rendering**: Custom perspective projection, no external 3D library
- **Physics**: Frame-rate independent (delta time based)
- **Audio**: Procedurally generated at runtime (no audio files)
- **Textures**: Generated using NumPy
- **Performance**: Depth-sorted rendering, distance culling, render scaling

## Extending the Engine

### Adding New Zone Types
Edit `procedural.py`, add to `ZONE_TYPES` dict with properties:
```python
'new_zone': {
    'pillar_density': 0.5,
    'wall_chance': 0.3,
    'ceiling_height_var': 10,
    'color_tint': (1.0, 1.0, 1.0)
}
```

### Adding New Sounds
Create function in `audio.py`, then initialize in `main.py`:
```python
def generate_new_sound():
    duration = 0.5
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, False)
    # Your waveform here
    return pygame.sndarray.make_sound(stereo_audio)
```

### Changing Physics
Tune constants in `config.py`:
```python
JUMP_STRENGTH = 150  # Higher = jump higher
GRAVITY = 300        # Higher = fall faster
WALK_SPEED = 25      # Higher = move faster
```

### Adding New Geometry
Add drawing function in `engine.py`, call from render queue.

## Performance Notes

- Render scale mode (R key) renders at 0.5x then upscales (2-4x FPS boost)
- Debris culled beyond 900 units from player
- Hard cap of 12,000 debris particles
- Debris auto-cleanup after 8-18 seconds or 2-6 seconds after settling
- Frustum culling on all geometry
- Distance-based detail (debris size scales with distance)

## Known Limitations

- No vertical movement (can't climb/fall through floors)
- No entities/enemies
- Pillars disabled (all pillar code present but `_get_pillar_at` returns False)
- Fog disabled by default (toggle in config.py)
- No texture mapping (uses average colors)

## Credits

Built from scratch - custom 3D math, procedural generation, physics simulation.
No external 3D libraries, no texture files, no audio files.
