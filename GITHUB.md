# BISRARO — GitHub'ga joylash yo'riqnomasi

Hamma narsa tayyor. Sizdan faqat 2 ta qadam kerak.

## 1-qadam. Bo'sh repozitoriy oching

1. https://github.com/new
2. **Repository name:** `bisraro`
3. **Public** ni tanlang (bepul GitHub Pages faqat public repoda ishlaydi)
4. README, .gitignore, license — hech birini **qo'shmang**
5. **Create repository**

## 2-qadam. Fayllarni yuklang (ikki usuldan birini tanlang)

### A usul — brauzer orqali (Git kerak emas)
1. Yangi repozitoriy sahifasida **"uploading an existing file"** havolasini bosing
2. Shu papkadagi **barcha fayl va papkalarni** (`index.html`, `admin.html`, `products.json`,
   `README.md`, `img` papkasi va boshqalar) oynaga sudrab tashlang
3. Pastda **Commit changes** ni bosing

### B usul — bitta fayl bilan (Git o'rnatilgan bo'lsa)
- **Windows:** `yuklash.bat` faylini ikki marta bosing
- **macOS / Linux:** terminalda `./yuklash.sh`

Birinchi marta GitHub login oynasi chiqadi — kiring, qolganini skript o'zi qiladi.

## 3-qadam (ixtiyoriy). Saytni internetda ochish — GitHub Pages

1. Repozitoriyda **Settings → Pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main`, papka: `/ (root)` → **Save**
4. 1–2 daqiqadan keyin sayt shu manzilda ochiladi:
   **https://sladusuz.github.io/bisraro/**
   Admin panel: **https://sladusuz.github.io/bisraro/admin.html**

## Muhim

- Repozitoriy public bo'lsa, `README.md` va `admin.html` ichidagi admin kirish kodi
  (`bisraro2026`) hammaga ko'rinadi. Yuklashdan oldin `admin.html` dagi
  `var PIN = '...'` qatorini va README'dagi kodni o'zgartiring.
- `.nojekyll` fayli GitHub Pages saytni o'zgartirmasdan ko'rsatishi uchun kerak — o'chirmang.
