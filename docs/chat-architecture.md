# Chat-about-content for the Piatra web — architecture

A design note, not an implementation plan. Describes how a "chat about this content" feature could work across everything on the Piatra Institute website (press, papers, playgrounds, blog) so each conversation is grounded in adequate context for the specific piece. Doxonomics is the canonical first case: the existing PDF download button on the press page would be joined by a "Chat about this book" button.

This doc lives here because the Doxonomics book is the first content piece that would benefit and because `docs/` already collects this kind of methodology / pipeline writing (`voice.md`, `diagnostic.md`, `research-pipeline.md`, `STATUS.md`).

The decision for now is to write the design before building it.


## Goal

One reusable chat component on the Piatra web. Drop it next to a PDF, a paper, a playground, a blog post — anywhere. Each instance reaches an LLM that has been given the right context for that specific piece of content, so the conversation can be substantive rather than generic.

The reader should be able to ask "how does doxonomics interpret X?" on the press page, "what does this playground simulate and what would change if I tweak parameter Y?" on a playground page, "what's the central claim of this paper and what evidence does it cite?" on a paper page — and get answers grounded in the actual material.


## The pieces

Three repositories are involved:

| Repo | Role |
|---|---|
| `/Users/ly3xqhl8g9/Data/i/theings/piatra/core/piatra-institute-web/` | The public website. Hosts the **content registry**, the **build-time context builder**, and the **chat component**. |
| `/Users/ly3xqhl8g9/Data/i/theings/piatra/center/piatra-ai-gateway/` | The institute's LLM gateway (Bun + Hono, OpenAI-compatible). Extended with **CORS**, a **preset registry**, and optional **BYO-key forwarding**. |
| `/Users/ly3xqhl8g9/Data/i/theings/piatra/content/piatra-press/introduction-to-doxonomics/` | The Doxonomics book repo. Source material for the first content preset. |


## System diagram

```
piatra-institute-web                                  piatra-ai-gateway
+----------------------+                              +-------------------------+
| content registry     | --build:contexts--> presets/ | preset loader           |
| (TypeScript)         |                              |   doxonomics.json       |
|                      |                              |   paper-X.json          |
|   slug               |                              |   playground-Y.json     |
|   title              |                              |                         |
|   type               |                              | POST /v1/chat/completions
|   source             |                              |   model: piatra/<slug>  |
|   strategy           |                              |   (or preset field)     |
|                      |                              |   X-User-Provider-Key?  |
| <PiatraChat          |  ----- HTTPS + CORS ----->   |                         |
|   slug="doxonomics"/>|                              | if user key present:    |
|                      |                              |   forward as user key   |
|                      |                              | else:                   |
|                      |                              |   use operator key      |
|                      |                              |   enforce rate + budget |
+----------------------+                              +-------------------------+
                                                                  |
                                                                  v
                                                    OpenAI / Anthropic / Zhipu
```

The interesting movement is right-to-left: every chat call carries a slug, the gateway maps slug → preset, the preset supplies the system prompt and (optionally) document grounding, the upstream provider does the actual generation.


## Content registry

Single source of truth in `piatra-institute-web`, a TypeScript file listing every chat-enabled piece of content:

```ts
// content-registry.ts
export const contentRegistry = [
  {
    slug: 'doxonomics',
    title: 'Introduction to Doxonomics',
    type: 'press',
    source: {
      kind: 'latex-repo',
      path: '/Users/.../introduction-to-doxonomics',
    },
    strategy: 'compact-digest',
  },
  {
    slug: 'avarism-paper',
    title: 'Avarism: a working note',
    type: 'paper',
    source: { kind: 'pdf', path: 'public/papers/avarism.pdf' },
    strategy: 'full-text',
  },
  {
    slug: 'belief-cascade',
    title: 'Belief cascade playground',
    type: 'playground',
    source: { kind: 'playground-dir', path: 'app/playgrounds/belief-cascade' },
    strategy: 'code-plus-description',
  },
] as const;
```

Adding new chat-enabled content is editing this file. The `slug` is the identifier that flows everywhere: URL, registry entry, gateway preset filename, chat-component prop.


## Context strategies

Different content types need different context-building. Five strategies cover the realistic cases:

### `compact-digest`

For books and long PDFs (Doxonomics).

Hand-curate (or generate once and review) an 8–12K-token digest covering: the formal apparatus (definitions, models, propositions), per-chapter abstracts, glossary, voice note. The digest is the entire system prompt. Anthropic prompt caching reduces repeat-query cost ~10×.

For Doxonomics specifically, the digest would include:
- Definition 1.1 (doxonomic system tuple: A, I, N, B, Φ, Ψ)
- Model 1.1 (first-order belief equation)
- Definition 8.1 (common-sense capture)
- Proposition 32.1 (resource asymmetry)
- 36 chapter abstracts of 2–3 sentences each
- A ~20-term glossary
- Voice instruction: respond in the book's register, cite chapter/section when relevant

### `full-text`

For short papers (under ~30K tokens). The entire text becomes the system prompt. No retrieval, no chunking. Cheap and accurate for short documents.

### `chunks`

For long papers or multi-document sets where the digest would lose detail. The context builder splits the source into section-level chunks and ships a static JSON index. At query time, the client does a keyword (or, optionally, embedding) match against the user's message, picks the top 3–5 chunks, and includes them in the system prompt.

This is the middle path: more accurate than the digest, cheaper than full-text-every-call.

### `code-plus-description`

For playgrounds (interactive demos). A hand-written paragraph or two describing what the playground simulates, what each parameter does, and what behaviors to expect, plus the key source files inlined. Playgrounds are usually small; the whole model file often fits in 2–4K tokens.

### `anthropic-file`

Alternative for paper-as-PDF cases. Upload the PDF once via Anthropic's Files API, get back a `file_id`, and reference it in every subsequent request. Claude reads the PDF directly, including figures and typography. Trade-off: locks the strategy to Anthropic.


## Gateway changes

Three additions to `piatra-ai-gateway`:

### CORS

Add CORS middleware that accepts requests from the production origin (`piatra.institute` or wherever the site is hosted) and a development origin (`http://localhost:3000`). Handles OPTIONS preflight. Without this, browsers reject the call.

### Preset registry

Add a `presets/` directory. The gateway loads `presets/*.json` at boot and hot-reloads on file change. Each preset is:

```json
{
  "slug": "doxonomics",
  "system_prompt": "<the compact digest>",
  "model_default": "anthropic/claude-sonnet-4-6",
  "chunks": null,
  "file_id": null
}
```

Extend the `/v1/chat/completions` handler to recognize either a `preset: "<slug>"` field in the request body or a `model: "piatra/<slug>"` prefix. When recognized, the gateway prepends the preset's system prompt (and, if `chunks` are present, runs retrieval over the user's most recent message).

### BYO-key forwarding (optional, depending on funding model)

If the request carries an `X-User-Provider-Key` header, the gateway forwards that key upstream instead of using its own. The institute's `pi_live_*` auth token is still required (so anonymous abuse is rate-limited). This is the architectural piece that lets visitors pay for their own usage when they want to.


## Funding models

Three options. The recommendation is the hybrid.

### Operator-paid, with caps

The gateway uses its own operator keys for every call. Tight per-IP rate limits (e.g., 5 messages per IP per day) and monthly budget caps in the gateway's existing budget-tracking system. When a visitor hits the daily limit, they get a friendly 429 and a message: "come back tomorrow, or paste your own API key to keep going."

UX: cleanest. Visitor types a message and gets a response. No setup.

Cost: bounded by the caps. For Doxonomics with the compact digest, ~$0.01–0.03 per query (with prompt caching). At 5 messages × 100 unique visitors per day, that's roughly $5–15 per day, or $150–450/month. Caps make this controllable but not free.

### BYO-key only

The frontend has a settings panel where the visitor pastes their own API key (Anthropic or OpenAI). The key is stored in localStorage and travels only to the gateway and onward to the upstream provider. Operator pays nothing for visitor usage; the gateway still incurs server costs (small).

UX: friction. Many visitors won't have an API key or won't want to paste one.

### Hybrid (recommended)

Both. Default to operator-paid with tight caps. The settings panel offers "use your own API key" as an upgrade for visitors who hit the limit or want a different model. Best UX, controlled operator cost, scales gracefully.

The recommendation only stands if the operator is willing to commit to a modest monthly LLM spend (say $50–500/month depending on traffic). If not, BYO-key-only is the honest choice.


## Frontend component

One component, used everywhere:

```tsx
<PiatraChat slug="doxonomics" />
```

Responsibilities:

- Renders a button reading "Chat about [content title]" in the existing lime-on-black styling. The component looks up `title` from the content registry by `slug`.
- Opens a panel or modal with a message list, an input field, and a settings link.
- On submit, calls the gateway's `/v1/chat/completions` with the slug, the message history, and (if present) the visitor's BYO key from localStorage.
- Streams responses via SSE.
- Persists the chat history per-slug in localStorage. Each piece of content gets its own thread.
- Settings panel: provider selector (if multi-provider), masked API-key input, clear-history button, clear-key button.
- Markdown rendering for assistant responses via the existing `react-markdown` setup. Math via `react-katex` (useful for Doxonomics).

Styling matches the rest of the site (Tailwind 4, lime primary, black background, `text-lime` for links).


## Adding new chat-enabled content

Three steps:

1. Add an entry to `contentRegistry` in `piatra-institute-web`.
2. Run `pnpm build:contexts` (the build-time script the design proposes, not yet built). The script reads the registry, applies the strategy, and writes `presets/<slug>.json` into the gateway's preset directory (or uploads it to a shared store).
3. Deploy the gateway. The new preset is loaded at boot. The website's `<PiatraChat slug="<new-slug>" />` works immediately.

No per-content code is written. The chat component does not change.


## Cost analysis

Per-query cost with Anthropic Claude Sonnet 4.6 (input $3/M, output $15/M; cache write $3.75/M, cache read $0.30/M; 5-minute TTL):

| Strategy | First query | Cached query |
|---|---|---|
| `compact-digest` (~10K tokens) | ~$0.05 | ~$0.01–0.03 |
| `full-text` short paper (~25K tokens) | ~$0.10 | ~$0.02–0.04 |
| `chunks` (~30K tokens of retrieved chunks) | ~$0.12 | ~$0.02–0.05 |
| `full-book` (~125K tokens) | ~$0.40 | ~$0.05–0.07 |
| `anthropic-file` (a typical paper as PDF, ~30–50K equivalent) | varies | varies |

A visitor with $5 of credit can ask 200+ questions under the compact-digest strategy. Operator-paid caps at 5 queries/IP/day cost the operator roughly the same. Both numbers are tractable.

Prompt caching matters: the system prompt (which is the digest) is the largest part of the input, and caching it drops the per-query input cost roughly 10×. The cache key includes the system prompt verbatim, so a slug with a stable preset benefits the full 5-minute window. The gateway should explicitly mark the system prompt with `cache_control: { type: 'ephemeral' }` for Anthropic calls.


## Privacy and security

What leaves the visitor's browser:

- The visitor's message text → gateway → upstream provider.
- (BYO-key mode) The visitor's API key → gateway → upstream provider. The gateway forwards but does not log the key.

What is stored in localStorage:

- The visitor's API key (BYO-key mode only). Cleared on demand from the settings panel.
- The visitor's chat history, per slug. Cleared on demand.

What the gateway logs:

- Request metadata: timestamp, slug, IP (for rate-limiting), latency, input/output token counts, status code.
- The gateway does not log message bodies or API keys.

Disclosure in the settings panel: a short note explaining where the messages go (the gateway and then the upstream provider), that the BYO API key is stored locally and never seen by Piatra, and that chat history persists in the browser until cleared.

LocalStorage is per-origin and not readable by third-party scripts on other domains. The browser's same-origin policy is sufficient protection for the key. The gateway should reject requests with a malformed `X-User-Provider-Key` (no leading `sk-` prefix, suspicious length, etc.) to reduce the blast radius of misconfiguration.


## Open decisions before building

The doc deliberately does not pick:

1. **Funding model** — operator-paid with caps, BYO-key, or hybrid.
2. **Per-type strategy assignments** — which strategy for each content type. Defaults proposed: `compact-digest` for the book, `full-text` for short papers, `chunks` for long multi-document sets, `code-plus-description` for playgrounds.
3. **Gateway deployment target** — Fly, Railway, Render, Vercel-as-Node, self-hosted with a TLS-terminating reverse proxy. The gateway is Bun + Hono so any of these works.
4. **Provider scope** — Anthropic only (simplest, best prompt caching) or multi-provider (more flexibility for BYO-key users with existing keys elsewhere). Gateway already supports OpenAI / Anthropic / Zhipu on the upstream side; this is mostly a UI decision.
5. **Anthropic Files API** — whether to use it for paper-as-PDF or always extract text. Files API is cleaner for figures and typography; text extraction is provider-agnostic.


## Not in scope of this doc

- Implementation code.
- Specific deployment configuration (Dockerfile, k8s manifests, env vars).
- Internationalization of the chat UI.
- Tool use, web search, or agent loops.
- Voice mode.
- Analytics on conversation content (out of bounds; the gateway should remain content-blind).


## Next steps when ready to build

1. Decide the five open questions above.
2. Cut a tracking issue in `piatra-institute-web` and one in `piatra-ai-gateway`.
3. Build the gateway changes first (CORS + preset loader + optional BYO-key); test against a curl loop with a hand-written preset.
4. Build the context builder; generate the Doxonomics preset.
5. Build the `<PiatraChat />` component; wire it into the press page next to the PDF link.
6. Deploy the gateway behind TLS; deploy the website.
7. Test end-to-end with the Doxonomics slug.
8. Once one slug works, add the next piece of content by adding a registry entry and rebuilding presets.

The total scope when build starts is roughly: 3–5 days of gateway work, 1–2 days of the context builder, 1–2 days of the frontend component, plus deployment. The first slug (Doxonomics) lands in roughly a week. Subsequent slugs are minutes to add.
