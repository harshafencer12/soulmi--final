# SoulMi — Brand DNA & Design System Book
> *"Where every soul finds its home"*

This document serves as the definitive reference for the design system, branding guidelines, interactive widgets, cryptographic privacy layers, and conversational personality of **SoulMi**.

---

## 1. Brand Philosophy & Identity

SoulMi is a sanctuary for mental wellness, designed to feel calm, warm, safe, and gently optimistic. Unlike standard platforms that feel clinical or transaction-focused, SoulMi is styled as a cozy home for your mind, prioritizing user security, ease of expression, and anonymous peer support.

### The Motif
The brand's visual identity centers around a **house outline merging into a heart with a soft ribbon path**, symbolizing:
* **The House:** A safe structure, sanctuary, and home.
* **The Heart:** Self-compassion, emotional presence, and healing.
* **The Ribbon/Path:** Gentle guidance, community connection, and the journey toward mental well-being.

---

## 2. Visual DNA (Design System Tokens)

### 2.1 Color Palette
The colors are harmoniously chosen from nature to reduce cognitive strain and create a cozy paper-like texture.

| Swatch | CSS Variable | Hex Code | Semantic Use |
| :--- | :--- | :--- | :--- |
| 🟨 | `--cream` | `#F4F0E6` | Primary background (feels like natural paper) |
| 🟨 | `--cream-dark` | `#EDE8D8` | Secondary background, panel headers |
| 🟪 | `--lavender` | `#9C97C4` | Primary brand accent, navigation, links |
| 🟪 | `--lavender-light`| `#C4C1E0` | Hover states, borders, soft highlights |
| 🟪 | `--lavender-dark` | `#7A75AA` | High-contrast subheadings |
| 🟧 | `--terracotta` | `#D98F76` | Secondary accent, primary action buttons, active alerts |
| 🟧 | `--terracotta-dark`| `#C07050` | Active states, strong warning headers |
| 🟩 | `--sage` | `#6F9494` | Tertiary accent, body text headings, positive metrics |
| 🟩 | `--sage-dark` | `#4E7070` | Secondary body text, calm indicators |
| 🟨 | `--gold` | `#D6B583` | Highlights, stars, warmth accents, neutral indicators |
| ⬛ | `--charcoal` | `#4A4358` | Primary high-contrast text, headings |

---

### 2.2 Typography Scale
Typography is configured to provide an immediate sense of warmth and elegant, distraction-free reading.

* **Display Headers (Playfair Display):** A premium serif loaded via Google Fonts. Used for display titles like *"Good Mood"*, *"New Day, Fresh Start!"*, and *"Reflect & Write"*. It offers a literary, organic aesthetic.
* **Interface Headings (Poppins):** A clean, friendly geometric sans-serif. Applied to buttons, category tags, and dashboard interface labels.
* **Body copy (Nunito Sans):** A highly readable, rounded humanist sans-serif with a generous line-height of `1.75` and size of `1rem` to ensure comfortable legibility.

---

### 2.3 UI Components & Borders
* **Card Corner Radius:** 
  * Small: `10px` (`--radius-sm`)
  * Medium: `16px` (`--radius-md`) — Standard card radius
  * Large: `24px` (`--radius-lg`) — Hero blocks and large widgets
  * Pill: `999px` (`--radius-pill`) — Action buttons and tabs
* **Shadow System:** Soft, low-opacity charcoal plum shadows avoid harsh contrasts.
  * Small: `0 2px 12px rgba(74, 67, 88, 0.06)`
  * Medium: `0 8px 32px rgba(74, 67, 88, 0.10)`
  * Large: `0 20px 60px rgba(74, 67, 88, 0.12)`
* **Paper Grain Texture:** Added globally to the `body` via a tiny inline SVG noise filter background, reducing monitor glare and adding an organic feel:
  ```css
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  ```

---

## 3. Dashboard Interactive DNA

The Member Dashboard is divided into four main interactive sections, designed as highly responsive glassmorphic cards.

### 3.1 🔒 Encrypted Journaling (Overview & Dedicated Panel)
The journaling system strictly implements client-side encryption. The user's passphrase is derived locally and never sent over the network.

* **Passphrase derivation:** Key derived using **PBKDF2** (100,000 iterations, SHA-256) and a dynamic random salt.
* **Encryption payload:** Text is encrypted locally using **AES-GCM-256** (with a unique IV).
* **Dual modes:**
  1. **Text Journal:** Standard rich text logging.
  2. **Voice Chat AI:** Users can dictate their thoughts (via `webkitSpeechRecognition`). Speech is converted to text, processed by OpenRouter AI, and spoken back (via `window.speechSynthesis`).
* **Privacy Boundary:** The encrypted payload resides in `localStorage`. The AI companion **never** has access to these journal entries.

---

### 3.2 📊 Mood & Sleep Analytics
Designed to map wellness indicators without guilt-inducing tracking techniques.

* **Sleep Quality Vertical Slider:** A custom, vertical slide-up overlay with dynamic labels (`Poor (<4h)`, `Fair (4-6h)`, `Good (6-8h)`, `Very Well (8-10h)`). Fills vertically with a warm terracotta color.
* **Weekly Comparative Line Chart (SVG):** An SVG line chart showing "This Week vs. Last Week" mood averages using curved gradient paths.
* **Monthly Mood Trends (HTML/CSS Bar Chart):** A bar chart where positive mood days (score 4-5) render in sage green, neutral days (score 3) in gold, and negative/restless days (score 1-2) in terracotta.
* **Mood History Emoji Row:** A daily stream of emojis highlighting the past 7 days of entries inside rounded frames.

---

### 3.3 👥 Soulmi Community
A fully integrated, private peer-support network built directly into the dashboard.

* **Anonymity Shield:** When sharing a story, the app generates a randomized alias by combining a friendly adjective and a nature noun (e.g. *"Warm Clover"*, *"Calm Pebble"*, *"Steady Willow"*), paired with a nature-themed avatar.
* **Give Strength Widget:** 
  * Rendered as: `💪 Give Strength (Count)`
  * Allows members to click and increment the strength counter to express solidarity.
* **Resonate Widget:**
  * Rendered as: `🌟 Resonated (Count)`
  * Allows members to click and indicate that they relate to the story.
* **Nested Support Replies:**
  * Expandable reply drawer containing supportive, anonymous community replies.
* **Helper Prompts:**
  * **"Give Me More Ideas":** Rotates through self-reflection prompts to help users find words for their posts.
  * **"Brainstorm Some Ideas":** Displays immediate, actionable coping mechanisms (like 5-4-3-2-1 grounding or breathing techniques).

---

## 4. AI Companion & Conversational DNA

The AI Companion widget sits in the bottom right corner of all pages.

### 4.1 Conversational Tone
* Empathic, validation-focused, and supportive.
* Avoids clinical jargon or diagnoses.
* Validates user feelings before offering gentle perspectives.

### 4.2 Data Context & Privacy Policy
* **Settings Toggle:** Inside Privacy & Settings, users can enable *"Allow AI Companion to Analyze Mood Trends"*.
* **Context Loading:** If enabled, `script.js` loads the user's mood scores and sleep logs from `localStorage`, formats them, and inject them into the OpenRouter message history.
* **Explicit Records Declaration:** System instructions require the AI to preface any analysis or conclusions drawn from these logs with the exact phrase:
  > *"Based on the records you stored..."*
* **Access Restraints:** The AI is strictly barred from accessing the encrypted journal logs (`soulmi-journals`) to maintain the cryptographic privacy model.

---

## 5. Technical Data Structures
All client-side data structures conform to the following JSON schemas:

### User Data
```json
{
  "User": {
    "id": "string",
    "name": "string",
    "email": "string"
  }
}
```

### Mood Logs
```json
{
  "MoodLog": {
    "user_id": "string",
    "timestamp": "ISO8601",
    "mood_score": "1-5",
    "tags": ["string"]
  }
}
```

### Sleep Logs
```json
{
  "SleepLog": {
    "user_id": "string",
    "timestamp": "ISO8601",
    "hours": "string (1-10)"
  }
}
```

### Community Stories
```json
{
  "CommunityStory": {
    "id": "string",
    "author": "string",
    "avatar": "string",
    "timestamp": "ISO8601",
    "tag": "General | Anxiety | Daily Win | Sleep | Relationships",
    "content": "string",
    "strength": "number",
    "resonated": "number",
    "replies": [
      {
        "author": "string",
        "content": "string",
        "timestamp": "ISO8601"
      }
    ],
    "hasGivenStrength": "boolean",
    "hasResonated": "boolean"
  }
}
```

---

## 6. How to Export to PDF
You can easily convert this document into a beautifully formatted PDF:
1. **VS Code:** Install the **Markdown PDF** extension, open this file, right-click, and select `Markdown PDF: Export (pdf)`.
2. **Web Browser:** Open the Markdown file in any browser extension/viewer and select `Print -> Save as PDF`.
