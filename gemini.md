# Project Constitution (gemini.md / claude.md)

## Data Schemas
```json
{
  "User": {
    "id": "string",
    "preferences": {
      "hobbies": ["string"],
      "baseline_mood": "string"
    }
  },
  "MoodLog": {
    "user_id": "string",
    "timestamp": "ISO8601",
    "mood_score": "1-5",
    "tags": ["string"]
  },
  "EncryptedJournal": {
    "user_id": "string",
    "timestamp": "ISO8601",
    "type": "text | audio",
    "encrypted_payload": "string (AES-GCM encrypted)",
    "iv": "string (Initialization Vector)"
  }
}
```

## Behavioral Rules
1. Prioritize reliability over speed.
2. Never guess at business logic.
3. If logic changes, update SOP in architecture/ before code.
4. gemini.md is law.
5. All intermediate files go to .tmp/
6. AI MUST NOT have access to the Journaling data. Only Mood Tracker and Self-Assessment data.

## Architectural Invariants
- 3-Layer Architecture (A.N.T.)
  - Layer 1: Architecture (SOPs in architecture/)
  - Layer 2: Navigation (Decision making)
  - Layer 3: Tools (Python scripts in tools/)

## Maintenance Log
- 2026-06-12: Framework initialized.
