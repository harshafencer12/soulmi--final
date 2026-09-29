# Findings
## Research
- Evaluated Web Crypto API for client-side zero-knowledge security: derived keys from user passphrases using PBKDF2 (100k iterations, SHA-256) and encrypted entries using AES-GCM (256-bit key with 12-byte random IVs).
- Investigated browser-native Web Speech API (webkitSpeechRecognition) and MediaRecorder API for voice dictation and voice recording.

## Discoveries
- **Zero-Knowledge Encryption:** We successfully designed a client-side architecture where the server never sees the user's journal passphrase, satisfying the rule that the AI cannot have access to journal data. The AI chat assistant only receives mood tracker records, which are stored in plain text locally or in a DB.
- **Audio Encrypted Blobs:** MediaRecorder produces `.webm` audio blobs on the client side. By reading these blobs as DataURLs (Base64) before GCM encryption, we can store full audio recordings directly in `localStorage` in their encrypted form and reconstruct them back into `<audio>` sources on demand.
- **Speech Recognition Support:** Standard Chrome/Edge browsers natively support `webkitSpeechRecognition` for offline/client-side speech-to-text dictation without calling external APIs.

## Constraints
- **Static Server Limits:** Standard static HTTP servers (like `python -m http.server`) fail with a 501 error when forms perform standard POST submissions. All login/sign-up forms must prevent default behaviors and handle state transition via client-side JavaScript.
- **Web Crypto Context:** Web Crypto API requires a secure context (HTTPS) or localhost. Testing locally on `http://localhost:8000` is fully supported.
- **Local Storage Size Limits:** Encrypted audio recordings are stored in `localStorage` which typically has a 5MB limit. Users should keep voice logs short (under 1-2 minutes) to prevent storage exhaustion. In production, these encrypted payloads will be uploaded to Supabase.
