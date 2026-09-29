# SoulMi — Website UI/UX Design Brief & Build Prompt
*Ready to paste into Antigravity*

---

## 1. Brand Foundation (derived from logo)

| Element | Value |
|---|---|
| Brand name | SoulMi |
| Tagline | "Where every soul finds its home" |
| Category | Mental wellness content & community platform |
| Mood | Calm, warm, safe, gently optimistic — "a home for your mind" |
| Logo motif | House outline merging into a heart + a ribbon/path (community/connection) |

### Color Palette (pulled from logo)

| Name | Hex (approx) | Use |
|---|---|---|
| Cream paper | `#F4F0E6` | Primary background |
| Dusty Lavender | `#9C97C4` | Primary accent (house outline, nav, links) |
| Terracotta Blush | `#D98F76` | Secondary accent (heart, CTAs, highlights) |
| Sage Teal | `#6F9494` | Tertiary accent (tagline, body copy, icons) |
| Warm Sand/Gold | `#D6B583` | Wordmark, headings, decorative accents |
| Charcoal Plum | `#4A4358` | High-contrast text (for accessibility) |

Use a soft gradient blend (lavender → terracotta) sparingly for hero backgrounds, icon fills, or hover states — mirrors the heart glow in the logo.

### Typography
- **Headings/Wordmark style**: rounded, friendly sans-serif (e.g., Poppins, Quicksand, Fredoka) — matches the soft "SoulMi" lettering.
- **Body/Tagline style**: clean humanist sans-serif (e.g., Inter, Nunito Sans, Work Sans) — matches the tagline weight.
- Generous line-height (1.6+), medium font sizes (16–18px body) for readability and a relaxed feel.

### Visual Language
- Organic, rounded shapes — no sharp corners (border-radius 12–24px on cards/buttons).
- Soft drop shadows, paper/grain texture background (subtle, like the logo's canvas texture).
- Custom line-art illustrations (hand-drawn style, single-weight strokes) over stock photography.
- "Biophilic motion": slow gradient shifts, gentle fade/slide-ins on scroll, breathing/pulsing heart micro-animation for loading states.
- Generous white space; minimalist, distraction-free layouts.

---

## 2. Design System Components

- **Buttons**: pill-shaped, filled in terracotta (primary) or outlined lavender (secondary), soft hover glow.
- **Cards**: rounded 16–20px corners, cream/white fill, subtle shadow, sage-teal icon accents.
- **Navigation**: sticky top bar, transparent over hero → solid cream on scroll, logo left, pill-shaped CTA button right ("Join the Community" / "Get Started").
- **Icons**: single-line, rounded stroke icons (Lucide/Phosphor style) in lavender or sage.
- **Forms/Inputs**: rounded fields, soft borders, large touch targets, calm focus states (no harsh red errors — use warm amber + supportive copy).
- **Badges/Tags**: pill tags for topics (Anxiety, Sleep, Relationships, Self-Esteem) in pastel fills.

---

## 3. Site Map

1. Landing (Home)
2. About / Our Story
3. Resources & Programs (content library)
4. Community (forums/groups/events)
5. Blog / Articles
6. Therapist/Expert Directory (optional bridge to professional support)
7. Login / Sign Up
8. Member Dashboard / Profile

---

## 4. Page-by-Page UI/UX Specs

### 4.1 Landing Page
- **Hero**: Full-width section, cream background with soft lavender-to-terracotta gradient blob behind the logo's house+heart mark (animated subtle glow/breathing). Headline: warm, human ("A home for your mind, and people who get it"). Subheadline reinforces tagline. Two CTAs: primary "Join SoulMi" (terracotta pill), secondary "Explore Resources" (outlined).
- **Trust strip**: small row of stats or partner logos (e.g., "10,000+ members", "Backed by licensed therapists") in muted sage text.
- **Value pillars**: 3-column bento grid (rounded cards) — "Find Your People" (Community), "Learn & Grow" (Resources), "Feel Supported" (Expert access). Each with line-art icon, short copy, link.
- **Community spotlight**: carousel/cards showing real discussion topics or member stories (anonymized), warm illustrated avatars.
- **Featured articles**: 3-card row from the blog, tag-coded by topic color.
- **Testimonials**: soft quote cards with gentle fade-in on scroll.
- **CTA banner**: full-width terracotta/lavender gradient section — "Your soul deserves a home. Start today." with sign-up CTA.
- **Footer**: cream/charcoal, organized columns (Company, Resources, Community, Legal, Crisis Support link prominently visible — per accessibility best practice, a help/crisis resource should be reachable within 3 seconds from any page).

### 4.2 About / Our Story
- Narrative layout: founder/mission story with hand-drawn illustrations along the scroll (path/ribbon motif from the logo connecting sections — visually represents "finding your way home").
- Values grid (3–4 cards: Belonging, Compassion, Growth, Privacy).
- Team section with soft circular photo frames, lavender ring borders.
- Timeline component for milestones (optional), using the ribbon line-art as the connecting thread.

### 4.3 Resources & Programs
- Filterable grid/library: filter chips by topic (Anxiety, Mindfulness, Relationships, Sleep, etc.) — pill tags in palette colors.
- Each resource card: icon, title, format tag (Article/Audio/Exercise/Course), estimated time, save/bookmark icon.
- Featured "Program" hero banners (e.g., "21-Day Mindfulness Journey") with progress-style visual.
- Search bar at top, rounded, with sage icon.

### 4.4 Community
- Tab navigation: Discussion Groups | Events | Stories.
- Group cards: cover illustration (abstract organic shapes), member count, topic tags, "Join" pill button.
- Discussion thread view: clean comment cards, soft avatar circles, gentle color-coded tags for sentiment/support type (e.g., "Just Venting", "Looking for Advice", "Celebrating a Win").
- Community guidelines banner (calm, reassuring tone) pinned at top.
- Event cards: date badge in terracotta, RSVP button.

### 4.5 Blog / Articles
- Magazine-style grid with large featured article (image/illustration + title + read time).
- Category filter pills.
- Article page: generous reading width (~680px), pull-quote styling using sage accent border, related-articles footer, "Save" and "Share" icons.

### 4.6 Therapist/Expert Directory (optional)
- Card grid: photo (soft rounded frame), name, specialties as pill tags, rating, "Book a Session" CTA.
- Filter sidebar: specialty, availability, language, price range — rounded checkboxes/sliders.
- Profile detail page: bio, approach, calendar booking widget (rounded date cells, lavender highlight for selected).

### 4.7 Login / Sign Up
- Centered card on soft gradient background, logo at top.
- Minimal fields, social login options, calm microcopy ("Welcome back — your space is ready").
- Toggle between Login/Sign Up with smooth slide animation.

### 4.8 Member Dashboard / Profile
- Personalized greeting ("Good morning, [Name] 🌿" — optional emoji if user enables).
- Bento-grid widgets: "Continue Your Program" (progress ring in terracotta), "Your Community" (recent group activity), "Saved Resources", "Upcoming Events/Sessions".
- Mood check-in widget: simple, non-judgmental tap-to-select mood icons (avoid streak/guilt language — use "nudges" not "you missed your goal").
- Settings: privacy controls front-and-center ("Choose what's shared with your therapist / community").

---

## 5. Accessibility & Responsive Notes
- WCAG AA contrast minimum — pair light pastels (lavender/peach) with charcoal-plum text, not pure black.
- Keyboard navigable, screen-reader labeled icons, alt text on all illustrations.
- Crisis/help resources accessible from header or footer on every page, max 3-second discoverability.
- Mobile-first: stack bento grids to single column, sticky bottom nav for Home/Community/Resources/Profile on mobile.
- Motion should respect `prefers-reduced-motion` — disable background gradient animation/breathing effects if set.

---

## 6. Consolidated Prompt for Antigravity

> Design and build a responsive website for **SoulMi**, a mental wellness content and community platform with the tagline "Where every soul finds its home." Use a warm, calm, minimalist aesthetic inspired by the brand logo: a house-shaped outline in dusty lavender (#9C97C4) merging into a heart in terracotta blush (#D98F76), with sage teal (#6F9494) accents, a warm sand/gold (#D6B583) wordmark, and a cream paper background (#F4F0E6) with subtle paper-grain texture. Use rounded, friendly typography (Poppins/Quicksand for headings, Inter/Nunito Sans for body), generous white space, pill-shaped buttons, rounded 16-20px cards, soft shadows, and single-line hand-drawn-style icons/illustrations instead of stock photos. Add subtle "biophilic" motion — slow gradient shifts and gentle scroll fade-ins, with a soft breathing/pulsing animation on the heart logo mark.
>
> Build the following pages: (1) **Landing page** with hero (animated logo glow, headline, dual CTAs), trust strip, a 3-card bento grid of value pillars (Community, Resources, Expert Support), community spotlight carousel, featured articles, testimonials, and a gradient CTA banner; (2) **About/Our Story** with mission narrative connected by an illustrated ribbon/path motif, values grid, and team section; (3) **Resources & Programs** with a filterable card library (topic pill tags, format tags) and featured program banners; (4) **Community** with tabs for Discussion Groups, Events, and Stories, group cards with join buttons, and a discussion thread view with sentiment tags; (5) **Blog** with a magazine-style grid, category filters, and a readable article template; (6) **Therapist Directory** with filterable expert cards and a booking calendar; (7) **Login/Sign Up** centered card with calm microcopy; (8) **Member Dashboard** with bento-grid widgets (program progress ring, community activity, saved resources, mood check-in using non-judgmental "nudge" language, and privacy controls).
>
> Ensure WCAG AA contrast, full keyboard/screen-reader accessibility, a crisis-support link visible in the header/footer on every page, and a mobile-first responsive layout with a bottom nav bar (Home, Community, Resources, Profile) on small screens. Respect `prefers-reduced-motion`.

---

### Sources (research references)
- [27 Best Mental Health Website Design Inspiration of 2026 — Framerbite](https://framerbite.com/blog/best-mental-health-website-design-inspiration)
- [Mental Health Website Design Best Practices — Gapsy Studio](https://gapsystudio.com/blog/mental-health-website-design/)
- [Top Therapy Website Design Trends For 2025](https://mentalhealthitsolutions.com/blog/top-therapy-website-design-trends-for-2025/)
- [Mental Health App Design Guide: UI/UX Best Practices — Gapsy Studio](https://gapsystudio.com/blog/mental-health-app-design/)
- [Therapy Websites — 99designs Inspiration](https://99designs.com/inspiration/websites/therapy)
- [Dribbble: Mental Wellness App tag](https://dribbble.com/tags/mental_wellness_app)
- [Dribbble: Mental Health App tag](https://dribbble.com/tags/mental-health-app)