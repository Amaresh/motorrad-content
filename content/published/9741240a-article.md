

Let me fetch the draft article and check the current published directory.The draft at `9741240a-article.md` contains the quality review/metadata from the prior stage, not the actual article. The real article is on the `publish/smart-tech-inmrc-racing-diagnostics` branch (PR #5). Let me fetch it.I have the full approved article (~2,900 words) from the `publish/smart-tech-inmrc-racing-diagnostics` branch. The article on that branch lacks YAML front matter — it has the H1 title and meta description as plain text. PR #5 is open but not merged. I need to:

1. Format with proper YAML front matter (strip the H1, meta description block, and trailing metadata)
2. Push the production-ready article to `content/published/` on `main`
3. Create the splash page HTML

Let me push both files directly to `main`.✅ **Published to `Amaresh/motorrad-content` on `main`:**

| File | Path |
|------|------|
| **Article** | `content/published/smart-tech-inmrc-racing-diagnostics-article.md` |
| **Splash page** | `content/published/smart-tech-inmrc-racing-diagnostics-splash.html` |

**Front matter applied:**
- **Title:** Smart Tech — From INMRC Podiums to Your Garage: How Racing Innovation Is Transforming Motorcycle Service in India
- **Date:** 2026-02-15
- **Author:** Motorrad Theory Team
- **Market:** india
- **Tags:** SmartMotorcycleTechnology, INMRC, MotorcycleTelemetry, ECUTuning, MotorcycleDiagnostics, OBDScanner, BSVI, PredictiveMaintenance, IndianMotorcycleMarket, GarageSoftware, GarageCRM, MotorradTheory, IndianBikers, RacingTech, MadeInIndia

**Production formatting:**
- H1 stripped (title in YAML front matter only)
- Meta description and keywords block removed from body (moved to front matter)
- Trailing `*Published/Tags*` footer removed (redundant with front matter)
- All 3 CTA links validated: `motorradtheory.com/garage-crm`, `/employee`, `/crm`
- 4 image suggestion HTML comments preserved for design team
- Indian English spellings confirmed throughout (tyre, colour, stabilises, maximises)
- All currency in INR (₹)
- ~2,900 word article live with splash page featuring key stats (8–12 GB data, 1,000 Hz IMU, ₹2,500 OBD adapter, 21.4M bikes FY2025)