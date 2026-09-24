# BISRARO — premium shokolad brendi sayti

BISRARO — «HEALTHY FOOD PRODUCTION» MCHJ brendi. Bitta faylli (self-contained) sayt: `index.html`
(barcha rasmlar fayl ichiga WebP ko'rinishida joylashtirilgan, umumiy hajmi ~640 KB). Tashqi kutubxona, build yoki npm talab qilinmaydi —
faylni brauzerda ochish yoki istalgan hostingga (Netlify, Vercel, oddiy cPanel) tashlash kifoya.

## Nimalar bor

**5 ta sahifa** — hash-router orqali (`#/`, `#/biz-haqimizda`, `#/katalog`, `#/yutuqlarimiz`, `#/kontakt`).
Har bir sahifa alohida `<div class="page">` ichida; sahifa almashganda animatsiyalar qaytadan ishga tushadi.

**Bosh sahifa bo'limlari:** hero → brend haqida + statistika counterlari → kolleksiya (4 karta) →
ishlab chiqarish jarayoni (5 bosqich) → sertifikatlar karuseli → mijozlar fikri → aloqa formasi.

**Animatsiyalar:** preloader (gold monogramma chiziladi), scroll-reveal, sarlavhalarda so'zma-so'z stagger,
parallax, Lenis uslubidagi silliq scroll, magnit tugmalar, "Ko'rish" maxsus kursori, raqam counterlari,
karusel (drag + avto), filtr reflow, modal, lightbox, forma success animatsiyasi.

**Texnik:** to'liq responsive (360px dan 1920px+ gacha), semantik HTML, meta va Open Graph teglari,
klaviatura navigatsiyasi, `prefers-reduced-motion` qo'llab-quvvatlanadi.

## Rang va shrift tizimi

Barcha qiymatlar `:root` ichida — bitta joydan o'zgartiriladi.

| Token | Qiymat | Qayerda |
|---|---|---|
| `--ink` | `#1A120B` | asosiy qorong'i fon |
| `--gold` / `--gold-light` | `#C9A24B` / `#E8CD82` | CTA, chiziqlar, ikonkalar |
| `--cream` / `--milk` | `#F5E9DA` / `#FFF8F0` | och fonli bo'limlar |
| `--cocoa` / `--cocoa-deep` | `#6B3F2A` / `#3E2418` | gradient va och fondagi matn |
| `--foil` | gold gradient | metall/foliy effekti |

Shriftlar: sarlavhalar — **Fraunces**, matn — **Manrope** (Google Fonts orqali yuklanadi).

## Mahsulot boshqaruvi — `admin.html`

Katalogga mahsulot qo'shish uchun alohida sahifa: **`admin.html`** (footerdagi "Boshqaruv paneli" havolasi
orqali ham ochiladi). Katalog aynan shu paneldagi baza bilan ishlaydi — saqlaganingiz zahoti
`#/katalog` sahifasida ko'rinadi.

Panelda ikkita bo'lim bor: **Mahsulotlar** va **Mukofot va sertifikatlar**.

**Kirish kodi:** `bisraro2026` — `admin.html` ichidagi `var PIN = 'bisraro2026'` qatoridan o'zgartiriladi.
Bu faqat oddiy to'siq; haqiqiy himoya uchun panelni server tomonida parol bilan yoping
(masalan Apache `.htpasswd` yoki Netlify "password protection").

**Panelda bor:** qo'shish, tahrirlash, o'chirish, tartibni almashtirish (↑ ↓), qidiruv, turkum bo'yicha
filtr, rasm yuklash (avtomatik siqiladi va WebP'ga o'tkaziladi), xususiyatlar jadvali,
JSON eksport/import va boshlang'ich holatni tiklash.

### Ma'lumot qayerda saqlanadi

1. **`localStorage`** — panelda qilingan o'zgarishlar shu brauzerda saqlanadi. Ya'ni siz o'z
   kompyuteringizda qo'shgan mahsulot faqat sizning brauzeringizda ko'rinadi.
2. **`products.json`** — sayt papkasida shu fayl bo'lsa, uni **hamma tashrifchi** ko'radi.

**Shuning uchun ish tartibi shunday:**
panelda mahsulotlarni tayyorlaysiz → **"JSON yuklab olish"** → olingan faylni `products.json` nomi bilan
sayt papkasiga (index.html yoniga) yuklaysiz → yangilanish barcha foydalanuvchilarda paydo bo'ladi.

> Doimiy, hamma uchun avtomatik yangilanadigan katalog kerak bo'lsa, keyingi qadam — kichik backend
> (masalan Supabase, Firebase yoki PHP + MySQL). U holda `loadProducts()` funksiyasidagi localStorage
> o'rniga API'dan `fetch` qilinadi — qolgan kod o'zgarmaydi.

### Mahsulot yozuvi tuzilishi

```json
{
  "id": "qora-marvarid",
  "cat": "konfet",
  "art": "art-truffle",
  "title": "Qora Marvarid",
  "tag": "Ichi to'ldirilgan",
  "short": "Bodomli praline, qora shokolad qobiq",
  "desc": "Modal oynada chiqadigan to'liq tavsif",
  "img": "",
  "specs": [["Vazni", "14 g (dona)"], ["Qobiq", "54% qora shokolad"]]
}
```

`cat` — `konfet` / `plitka` / `premium`. `img` bo'sh bo'lsa turkumga mos SVG chizma chiqadi;
rasm qo'yilsa — `data:` yoki oddiy yo'l (`img/konfet-1.webp`) bo'lishi mumkin.

## Katalog — 16 ta haqiqiy mahsulot

Katalogingizdagi barcha mahsulotlar saytga kiritildi. Har birida katalog ID si, netto vazni,
qutidagi dona soni, quti o'lchami va hajmi, saqlash muddati hamda TN VED kodi bor.

**Ichi to'ldirilgan konfetlar (7):** Bunibi Larus (1.6), Dorro (1.7), Bunibi Fantos (1.09),
Sladus Issimo (1.15), Sladus Morning (1.21), YaZa (1.08), One Bite (1.21)

**Plitka va botonchik (6):** NITRO (1.17), Sladus DUO (1.19), Sladus Duo Milk (1.19-2),
Sladus One Milk (1.10), Sladus KVADRO (1.20), Sladus LACTIC (1.14)

**BISRARO premium (3):** BISRARO (1.16), BISRARO Buni (1.18), BISRARO Liya (1.22)

> Diqqat: katalogda ikkita mahsulotga bir xil ID berilgan — **1.21** (Sladus Morning va One Bite).
> Bu katalogdagi xatolik bo'lishi mumkin, tekshirib ko'ring.

Rasmlar katalog varaqlaridan kesib olingan, foni tozalangan va studiya foniga soya bilan joylangan.
Sifati yanada yaxshi bo'lishi uchun mahsulotlarning original fotolari (fotosessiyadan) bo'lsa,
admin paneldan har birini almashtirib chiqishingiz mumkin.

## Uch til: UZ / RU / EN

Yuqoridagi UZ · RU · EN tugmalari orqali sayt to'liq tarjima qilinadi (mobil menyuda ham bor).
Tanlangan til brauzerda eslab qolinadi.

Tarjimalar `index.html` ichidagi `I18N` obyektida, o'zbekcha matn — kalit:

```js
var I18N = {
  ru: { "Bosh sahifa": "Главная", ... },
  en: { "Bosh sahifa": "Home",    ... }
};
```

Saytga yangi matn qo'shsangiz (yoki admin paneldan yangi mahsulot/mukofot qo'shsangiz), uning
ruscha va inglizcha varianti shu obyektga qo'shilishi kerak — aks holda u o'zbekcha ko'rinaveradi.
Tarjima qilinmagan matn hech qachon yo'qolmaydi, shunchaki asl holida qoladi.

## Forma qayerga tushadi

Aloqa formalari **chempme@gmail.com** manziliga FormSubmit xizmati orqali yuboriladi
(`index.html` ichida `var MAIL_TO = 'chempme@gmail.com';` — manzilni shu yerdan o'zgartirasiz).

> **Muhim:** birinchi marta forma yuborilganda FormSubmit shu pochtaga tasdiqlash xati yuboradi.
> Xatdagi havolani bosmaguningizcha xabarlar kelmaydi. Bu faqat bir marta qilinadi.

Agar internet yoki xizmat ishlamasa, forma foydalanuvchining pochta dasturini ochib, xabar matnini
tayyor holda qo'yadi — ya'ni so'rov baribir yo'qolmaydi.

## Mukofot va sertifikatlarni qo'shish

Admin paneldagi **«Mukofot va sertifikatlar»** bo'limi: nomi, yili, joyi, kim bergani, tavsifi va
rasmi kiritiladi. Saqlaganingizdan keyin u uch joyda birdan chiqadi — bosh sahifadagi karuselda,
«Yutuqlarimiz» sahifasidagi katta kartalarda va «Hujjatlarda nima yozilgan» ro'yxatida.

Rasm yuklaganda u avtomatik siqiladi. Sertifikat fotosi yaxshi chiqishi uchun uni to'g'ridan-to'g'ri
tepadan, yaxshi yorug'likda suratga oling — keyin fonini tozalab berish mumkin.

## Xarita

Kontakt sahifasidagi xarita — siz yuborgan Google Maps embed havolasi
(41.368813, 69.115687). Nuqtani o'zgartirish uchun `index.html` dagi `<iframe src="...">` ichidagi
havolani Google Mapsdan olingan yangisi bilan almashtiring.

## Fotosuratlarni qo'yish

Hozir barcha vizuallar — SVG illyustratsiya (fayl ichidagi `<symbol>` lar: `art-truffle`, `art-draje`,
`art-bar`, `art-box`). Haqiqiy fotolar tayyor bo'lganda shunchaki almashtiriladi:

```html
<!-- Oldin -->
<div class="shot"><svg viewBox="0 0 600 600"><use href="#art-bar"/></svg></div>

<!-- Keyin -->
<div class="shot"><img src="img/sex.webp" alt="Ishlab chiqarish sexi" loading="lazy" width="1200" height="1200"></div>
```

Katalog kartalari uchun `.thumb` ichidagi `<svg>` ni `<img>` bilan almashtiring.
Rasmlarni **WebP** formatida, kengligi 1600px dan oshmagan holda saqlang va `loading="lazy"` qo'shing.
Hero foni uchun `.hero-bg .plate` o'rniga video yoki rasm qo'yish mumkin:

```html
<video class="plate" autoplay muted loop playsinline poster="img/hero.webp">
  <source src="img/hero.mp4" type="video/mp4">
</video>
```

## Formani serverga ulash

`index.html` ichida `/* Bu yerda ma'lumot serverga yuboriladi */` izohi bor. Telegram botga yuborish misoli:

```js
fetch('https://api.telegram.org/bot<TOKEN>/sendMessage', {
  method:'POST', headers:{'Content-Type':'application/json'},
  body: JSON.stringify({ chat_id:'<CHAT_ID>', text:'Yangi so\'rov: ' + new FormData(form).get('name') })
});
```

CRM yoki o'z backendingiz uchun ham shu joyga `fetch(...)` qo'yiladi. Validatsiya allaqachon ishlaydi.

## Google Maps

Kontakt sahifasidagi `.map` bloki hozir qorong'i uslubdagi vizual o'rin. Haqiqiy xarita uchun ichidagi
SVG o'rniga iframe qo'ying yoki Maps JavaScript API'da `styles` massivi bilan dark tema sozlang
(gold marker uchun `icon` parametri).

## Ko'p tillilik (i18n)

Struktura tayyor: `<html lang="uz">` va barcha matnlar alohida elementlarda. Eng tez yo'l —
har bir matnli elementga `data-i18n="key"` qo'shib, JSON lug'atdan almashtirish:

```js
const dict = { ru:{ 'nav.catalog':'Каталог' }, en:{ 'nav.catalog':'Catalogue' } };
document.querySelectorAll('[data-i18n]').forEach(el => el.textContent = dict[lang][el.dataset.i18n]);
```

## Saytdagi ma'lumotlar

**Hujjatlardan olingan (haqiqiy, tekshirilgan):**

- «HEALTHY FOOD PRODUCTION» mas'uliyati cheklangan jamiyat — to'liq nomi
- STIR 303 901 102 · guvohnoma 005186-06 · ro'yxatga olingan sana 14.04.2016
- Manzil: Toshkent shahri, Yangihayot tumani, Sputnik 17-mavze
- Ro'yxatdan o'tkazgan organ: Yangihayot tumani DXM
- ProdExpo 2023 (Moskva, 6–10-fevral) — «Лучший продукт – 2023» laureat diplomi va
  **oltin medal**, NITRO shokolad plitkalari uchun. RF Qishloq xo'jaligi vazirligi / Rosselxoznadzor
- F İstanbul Gıda ve İçecek Fuarı 2023 — ishtirok uchun plaketa

**Kiritilgan kontaktlar:**

- Telefon: **+998 97 777 44 40**
- Email: **info@bunibi.uz**
- Ish vaqti: Dushanba—Shanba, 09:00–18:00
- Xarita: Google Maps embed (41.368813, 69.115687)
- Formadan kelgan xabarlar: **chempme@gmail.com**

**Hali qo'shilishi kerak:**

- ijtimoiy tarmoq havolalari (footer'da hozir `#` turibdi — Instagram, Telegram, Facebook, YouTube)
- mahsulot fotolari (hozir chizmalar turibdi)
- mahsulot nomlari, tavsiflari va xususiyatlari — admin paneldan tahrirlanadi
- "Ishlab chiqarish jarayoni" bo'limidagi matnlar (umumiy tavsif)
- `<link rel="canonical">` va Open Graph URL'lari (hozir `bisraro.uz`)
- Google Maps xaritasi — kontakt sahifasida hozir bezakli o'rin turibdi

## Saytdagi rasmlar

Yuborilgan fotolar qayta ishlangan: foni olib tashlanib, to'q shokolad rangli studiya foniga
qo'yilgan, ostiga yumshoq soya va nozik aks qo'shilgan. Guvohnoma PDF'dan rasmga o'girilgan,
logotip esa shaffof fonli qilingan.

Rasmlar `index.html` ichida `IMG` obyektida (data-URI) saqlanadi: `logo`, `medal`, `diplom`,
`plaque`, `guvohnoma`. Rasmni almashtirish uchun shu obyektdagi mos qatorni yangi data-URI bilan
almashtirish yoki tashqi faylga o'tkazish kifoya:

```js
var IMG = { logo: 'img/logo.webp', medal: 'img/medal.webp', ... };
```

Alohida WebP fayllar ham beriladi — ularni `img/` papkaga qo'yib, yuqoridagidek yo'l ko'rsatsangiz,
sayt yengilroq yuklanadi va rasmlar brauzerda keshlanadi.

## Brauzerlar

Chrome, Edge, Safari, Firefox (oxirgi 2 versiya). Silliq scroll va maxsus kursor faqat sichqonchali
qurilmalarda ishlaydi; mobilda tizimning o'z scrolli qoladi.
