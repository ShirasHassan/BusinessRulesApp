# nTouchAxon

API Integration Portal for NAS Neuron. Build workflow:
1. **Extract the brand**: `cd brand && npm i -D playwright && node extract-brand.mjs`. This writes `brand.json` and `assets/`: logos, favicon, and a reference screenshot. Needs network access to nasneuron.com.
2. **Review**: check `brand.json` → `logos`, `paletteHex`, `elements`. Delete any wrong logo candidates.
3. **Build**: give an AI agent only `AGENT_BRIEF.md` and `brand/brand.json`.
