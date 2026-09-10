# SANSKRITISETU

SANSKRITISETU is an interactive Indian cultural heritage experience. Users can explore state profiles, discover monuments and crafts on a map, ask the AI guide questions, and use multilingual or voice-based interactions as those modules are integrated.

## Project Description

The project connects cultural knowledge with an accessible digital experience:

- **Homepage:** introduces the mission and gives users entry points into the experience.
- **Map:** identifies Indian states and heritage places through interactive Leaflet markers.
- **Cultural knowledge:** provides a structured profile for every state.
- **AI guide:** answers questions using the cultural and heritage content.
- **Language and UX:** adds Hindi and other language support, voice input, and read-aloud features.
- **Online landmark view:** selected places such as the Taj Mahal, Qutub Minar, Hampi, and Konark Sun Temple can open a trusted online reference from the map detail panel.

## Team Ownership

### Person 1: Map

Owns [`map.js`](map.js), the Leaflet map, state detection, markers, coordinates, map search, and the online landmark view.

When a user selects a state or place, the Map module should pass the matching `id` to the shared data layer. It should not duplicate cultural descriptions in map code.

### Person 2: AI

Owns the AI guide and question-answering flow. It receives the selected state or landmark context and uses that context to answer questions.

### Person 3: Homepage

Owns the landing experience, navigation, featured heritage content, and entry points into the map and cultural profile.

### Person 4: Cultural Knowledge

Owns the state data. Every state must follow the shared schema below. This module is the source of truth for cultural profiles.

### Person 5: Language + UX

Owns Hindi and other translations, language switching, voice input, read aloud, accessibility, and user interaction states.

### Final work: Integration + Demo

Connects the modules, checks the shared data contract, removes duplicate data, tests the complete user journey, and prepares the final demonstration.

## Shared State Data Contract

Every state must have this structure. Keep the field names stable so all modules can work independently.

```json
{
  "id": "rajasthan",
  "name": "Rajasthan",
  "description": "A state known for desert landscapes, forts, folk arts, crafts, and royal heritage.",
  "image": "https://example.com/rajasthan.jpg",
  "cultural_highlights": [
    "Forts and palaces",
    "Folk music and dance",
    "Block printing and textiles"
  ],
  "culture": {
    "language": "Hindi, Rajasthani, and regional dialects",
    "clothing": "Bandhani, lehenga-choli, turbans, and mojari footwear",
    "customs": "Hospitality, wedding traditions, and community rituals",
    "festivals": "Teej, Gangaur, Pushkar Fair, and local fairs",
    "cuisine": "Dal baati churma, gatte ki sabzi, and ker sangri",
    "beliefs": "Hindu and Jain traditions with regional variations",
    "heritage": "Forts, palaces, stepwells, and desert trade routes",
    "arts_music_dance": "Kalbeliya, folk music, puppetry, and block printing",
    "social_life": "Multigenerational families and community celebrations",
    "architecture_lifestyle": "Havelis, forts, jharokhas, and climate-aware desert homes"
  },
  "map": {
    "capital": "Jaipur",
    "latitude": 26.9124,
    "longitude": 75.7873,
    "locations": [
      {
        "id": "amber-fort",
        "name": "Amber Fort",
        "latitude": 26.9855,
        "longitude": 75.8513,
        "type": "Monument",
        "description": "A historic hill fort near Jaipur.",
        "sourceUrl": "https://example.com/amber-fort"
      }
    ]
  },
  "sources": [
    "https://example.com/rajasthan-source"
  ]
}
```

### Data rules

- `id` must be unique, lowercase, and stable. Use it for integration between modules.
- `latitude` and `longitude` must be numbers, not strings.
- `locations` may be empty when a state has no map entries yet.
- `sourceUrl` is optional and should point to a trusted online source.
- Do not put API keys or private credentials in this data.
- Add new cultural fields only after discussing the change with the integration owner.

## Example User Flow

1. The user clicks Rajasthan on the map.
2. Person 1 identifies the state using `id: "rajasthan"`.
3. Person 4 returns the Rajasthan cultural profile.
4. Person 2 uses that profile to answer the user's questions.
5. Person 5 lets the user switch language or use Read Aloud.
6. The integration owner checks that the selected state remains available across all views.
7. If the user selects a landmark with a `sourceUrl`, the map detail view shows an online reference link.

## Map Views

The map should support these three views:

1. **State view:** state boundaries, capital, and state selection.
2. **Heritage view:** monuments, crafts, temples, museums, and other locations.
3. **Online reference view:** trusted web references for selected places when `sourceUrl` is available.

The online reference opens in a new browser tab. It is supplemental information; the main cultural profile remains inside SANSKRITISETU.

## Visual Language

### Colour palette

The interface uses a dark heritage-inspired palette with warm gold accents and a teal interaction colour.

| Purpose | CSS variable | Colour |
| --- | --- | --- |
| Main background | `--bg` | `#07131c` |
| Soft background | `--bg-soft` | `#0f1d2a` |
| Strong panel | `--panel-strong` | `#101c2a` |
| Light panel | `--panel-light` | `#122333` |
| Main text | `--text` | `#edf6ff` |
| Muted text | `--muted` | `#9ab0c3` |
| Gold accent | `--gold` | `#f7b955` |
| Orange accent | `--orange` | `#ff8a3d` |
| Red status accent | `--red` | `#ff5f6d` |
| Teal interaction colour | `--teal` | `#67e8cf` |
| Borders | `--border` | `rgba(148, 163, 184, 0.18)` |

Use the CSS variables in `style.css` instead of adding one-off colours. Gold and orange are used for heritage emphasis and primary actions. Teal is used for links, active states, focus indicators, and interactive controls.

### Font families

- **Body and controls:** `Trebuchet MS`, falling back to `Segoe UI`, then sans-serif.
- **Display headings and heritage titles:** `Georgia`, falling back to `Times New Roman`, then serif.

Keep the existing font pairing unless the Language + UX owner proposes a multilingual font that supports all required scripts.

## Run Locally

The project is a lightweight static frontend with a Python API for the AI guide.

```powershell
python server.py
```

Open <http://127.0.0.1:8000> in a browser.

The local server provides:

- Static files from the project folder.
- `POST /api/chat` for the current heritage guide response.

## Recommended Git Workflow

- Create one branch per team module, for example `feature/map-module` or `feature/cultural-data`.
- Keep shared schema changes small and communicate them before merging.
- Test the complete flow after merging a module.
- Do not commit secrets, generated environment folders, or local editor settings unless the team agrees.

## Integration Checklist

- [ ] Every state has the complete shared schema.
- [ ] State IDs are unique and used consistently.
- [ ] Map selection loads the matching cultural profile.
- [ ] Landmark selection loads the matching heritage detail.
- [ ] Optional online references open successfully in a new tab.
- [ ] AI receives the selected state or landmark context.
- [ ] Hindi, voice input, and Read Aloud do not break map or profile selection.
- [ ] The complete Rajasthan example flow works from map click to spoken answer.
- [ ] The final demo works from a clean local server start.
