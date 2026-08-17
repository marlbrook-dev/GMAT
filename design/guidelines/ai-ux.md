# AI product UX — Meridian Assist patterns

Synthesized from the AI-product skill set in tommyjepsen/awesome-ux-skills (ai-trust-builders, ai-wayfinders, ai-inputs, ai-governors, ai-identifiers), applied to Meridian.

**Identity (ai-identifiers):** the AI is "Meridian Assist" — logo mark + gold AI pill, navy-900 surface. It speaks in the brand voice (confident coach, second person), never first-person hype. No sparkle emoji; no purple-gradient "AI shimmer".

**Wayfinding (ai-wayfinders):** never a blank prompt box. Assist surfaces always show 2–3 example prompts as tappable chips grounded in the user's data ("Build a Quick 10 from my weak areas", "Drill yesterday's misses"). First-run shows what Assist can do before asking for input.

**Inputs (ai-inputs):** default to templates + one editable slot over open text (mode, section, length pickers feeding a readable sentence). Open text is available, never required.

**Trust (ai-trust-builders):** every generated round states its evidence ("from your last 20 answers"); explanations cite the rule being applied; score estimates show the trend and basis, not just a number. Label AI-generated practice content as such. Never fabricate stats in UI copy.

**Control (ai-governors):** generated plans are proposals — user can regenerate, swap a question type, or dismiss; destructive actions (end round) confirm via Dialog; progress autosaves and says so.

**Onboarding wizard (pattern reference: Wix AI setup):** starting a new study program opens a 4-step modal — exam → goal → time → recommended tools. The goal step predicts intent as the user types (suggestion chips from similar students' goals, evidence-labelled); the tools step pre-selects games with a one-line reason each, all toggleable. Every later surface (sections, score model, games) keys off the exam chosen in step 1. Live in ui_kits/web_app/Onboarding.jsx.