# DESKPILOTC AI AGENT WORKING PROTOCOL

## HARD RULES — BISMILLAH + EKO + EKO TEK MADDE + SPP

These rules are mandatory for every AI engineering agent working on this repository.

### 1. Bismillah — Verify Before Action
Before changing anything, verify the exact current state relevant to the requested task. Never guess file contents, architecture, implementation state, or patch locations.

### 2. Eko — Token and Interaction Economy
Use the minimum tokens, commands, searches, file reads, explanations, and outputs required to complete the task safely. Do not repeat known information. Keep responses minimal unless the user explicitly requests detail.

### 3. Eko Tek Madde — Strict Scope Lock
**Execute only the explicitly requested scope; do not scan unrelated files, do not broaden the search/changes, and keep responses minimal (one-line status unless asked).**

One requested item means one focused task. Do not add secondary improvements, cleanup, refactoring, optimization, or investigation unless explicitly requested.

### 4. One Step at a Time
For dependent operations, provide or execute only one step at a time. Verify its result before continuing. If a step fails, stop immediately and resolve that failure first.

### 5. No Scope Expansion
Do not inspect, search, analyze, or modify unrelated files or modules. Start with the narrowest possible target and expand only when technically necessary to complete the explicit request.

### 6. No Opportunistic Refactoring
Never refactor unrelated code because it appears improvable while working on another task. Refactoring requires an explicit need or explicit user request.

### 7. SPP — SafePatch Protocol
Use this sequence:
**Analyze requested scope → Verify exact target → Apply smallest safe change → Verify result → Stop and report briefly.**

### 8. Minimal Patch
Prefer the smallest focused change that safely satisfies the requirement. Preserve existing behavior outside the requested scope.

### 9. Fail Fast
At the first meaningful error or unexpected result, stop. Do not continue with dependent commands or patches.

### 10. Commands
Keep commands compact and easy to copy. For dependent operations, give one command/block and wait for its output before giving the next.

### 11. Frozen Python Reference
The frozen Python DeskPilot is a behavioral reference only. Do not mechanically port Python/PyQt code or legacy workarounds into DeskPilotC.

### 12. No Image Generation
Do not use image generation or image editing tools for DeskPilotC development.

### 13. Communication
Communicate with the user in Turkish unless explicitly requested otherwise. Default status responses should be one line.

### 14. User-Executed Commands for Builds and Tests
**CRITICAL AND MANDATORY:** For ANY builds, tests, or extensive local analyses, DO NOT RUN the commands in the background yourself. You MUST provide the exact PowerShell (PS) commands to the user. The user will execute them locally and paste the output/results back into the chat. You MUST STOP and wait for the user's report before proceeding. Any deviation from this rule is strictly prohibited.
### 15. Strict File Size Limit (Modularity)
**CRITICAL AND MANDATORY:** No source code file shall normally exceed 400-450 lines. In cases of absolute technical necessity, the maximum hard limit is 700 lines. When a file approaches these limits, it MUST be refactored and split into smaller, single-responsibility components or modules. Do not create "God Objects".

### 16. Global Application and Localization (i18n)
**CRITICAL AND MANDATORY:** The application architecture MUST natively support a global structure, including multi-language support (TR, EN, Arabic, etc.), Right-To-Left (RTL) layout capabilities, and regional formatting (date/time, currency). All user-facing text must be wrapped in translation functions (e.g., `qsTr()` in Qt/QML) from the beginning. Never hardcode UI text strings.

## REQUIRED DOCUMENT READING ORDER

For every new development session:

1. `AGENTS.md`
2. `STATE.md`
3. `TASK.md`

Read additional documents only when required by the explicit task:

4. `ROADMAP.md`
5. `DESKPILOT_PRODUCT_SPEC.md`
6. `ARCHITECTURE.md`
7. `PRODUCT_ARCHITECTURE_PRINCIPLES_AI_EN.md`

Do not automatically scan the entire repository or all documentation at the start of every task.


## Ekosistem Telemetri & Dağıtım Kuralı (IST-013 / IST-016 / IST-017)
- Uygulama güncelleme veya yeni sürüm yayınlama işlerinde kök dizindeki `ECO_TELEMETRY_GUIDE.md` (ve merkezi `D:\Code\istisare\istisareler\017-eco-sdk-istemci-entegrasyon-rehberi.md`) kuralları **zorunlu** olarak uygulanır.
- Kapanışta telemetri atılmaz; açılışta `launch_count` biriktirilip ilk/yeniden kurulumda, sürüm değişiminde ve 7 günde 1 gönderilir. Ayarlara opt-out anahtarı/pop-up konulmaz (mağaza uygulamalarında `privacy.html` & Data Safety beyanı korunur).

## Response Budget & Commit Format (Mandatory)
- **<= 10 Lines Limit:** Keep ALL replies concise, bulleted, and strictly **<= 10 lines total** (1–3 lines for Yes/No, max 1–2 lines/single sentence per bullet). No unrequested elaboration unless asked.
- **Commit Format:** On user-approved commits, summarize the change clearly in Turkish followed by `(yy/mm/dd_hh.mm)` (e.g., `Aktif hesap okuma düzeltildi (26/11/25_15.42)`).


## Zorunlu Release, Tag & İkili Dosya Adlandırma Kuralı (IST-015 / IST-016)
> **SSOT:** `D:\Code\istisare\istisareler\015-merkezi-release-tag-ve-surum-yayin-protokolu.md` (`IST-015`) & `016-melez-hizli-dagitim-r2-ve-worker-cache-mimarisi.md` (`IST-016`).

- **Git Geçmişine İkili Dosya Konmaz:** Derlenen dosyalar (`dist/`, `build/`, `*.exe`, `*.apk`, `*.zip`) `.gitignore` içinde kalır; dağıtım yalnızca **GitHub Releases / R2** üzerinden yapılır.
- **Genel / Debug Dosya Adı Yasağı (Yerel + Uzak):** Yerel debug/release derlemelerinde (`PyInstaller --name`, Flutter çıktı adı vb.) ve uzak Release'lerde `main.exe`, `app.exe`, `app-release.apk`, `app-debug.apk` veya `release.apk` gibi genel isimler **kesinlikle kullanılmaz**. Yerel çıktılar daima gerçek uygulama adıyla (ör. `RekatSay-debug.apk`, `PushPull.exe`), yayınlanan/indirilen release dosyaları ise **`<UygulamaAdı>-<sürüm>.<uzantı>`** (ör. `RekatSay-v1.3.1.apk`, `PushPull-v1.0.2.exe`) formatında üretilir.
- **Kesin Hedef Ayrımı:** Son kullanıcıya açık (Public) uygulamalar **`mskaymaz/MSKLabsApps` Releases** (`<app-slug>-vX.Y.Z` tag'iyle) + Cloudflare R2 (`r2_keep_versions: 2`) üzerinden; bireysel/iç araçlar (`PushPull`, `TokenGemini` vb.) ise **kendi GitHub reposunun Releases sekmesinden** yayınlanır.
