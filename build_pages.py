#!/usr/bin/env python3
"""index.html dan har bir bo'lim uchun alohida sahifa yaratadi.

GitHub Pages /katalog manzilini katalog.html fayli bilan ochadi, shuning uchun
har bir bo'lim to'g'ridan-to'g'ri ochiladi va Google ularni alohida sahifa
sifatida ko'radi. index.html o'zgarganda shu skriptni qayta ishga tushiring:

    python3 build_pages.py
"""
import html, re

SITE = 'http://bisraro.uz'
PAGES = {
    'biz-haqimizda': ('Biz haqimizda — BISRARO',
        "BISRARO va «HEALTHY FOOD PRODUCTION» MCHJ haqida: 2016-yildan beri Toshkentda shokolad va qandolat mahsulotlari ishlab chiqaramiz."),
    'katalog': ('Katalog — BISRARO',
        "BISRARO katalogi: NITRO, Sladus, Bunibi shokolad plitkalari, ichi to'ldirilgan konfetlar va premium sovg'a to'plamlari."),
    'yutuqlarimiz': ('Yutuqlarimiz — BISRARO',
        "BISRARO mukofotlari: ProdExpo 2023 oltin medali, laureat diplomi va xalqaro ko'rgazmalardagi ishtirok."),
    'kontakt': ('Kontakt — BISRARO',
        "BISRARO bilan bog'lanish: +998 97 777 44 40, +998 33 880 88 80. Toshkent, Yangihayot tumani. Ulgurji savdo va hamkorlik."),
}

src = open('index.html', encoding='utf-8').read()

def sub1(pattern, repl, text):
    out, n = re.subn(pattern, lambda m: repl, text, count=1)
    assert n == 1, pattern
    return out

for slug, (title, desc) in PAGES.items():
    t, url = html.escape(title, quote=False), SITE + '/' + slug
    d = html.escape(desc, quote=False).replace('"', '&quot;')
    page = src
    page = sub1(r'<title>[^<]*</title>', '<title>%s</title>' % t, page)
    page = sub1(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % d, page)
    page = sub1(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % url, page)
    page = sub1(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % url, page)
    page = sub1(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % t, page)
    page = page.replace('<!DOCTYPE html>', '<!DOCTYPE html>\n<!-- Avtomatik yaratilgan (build_pages.py) — index.html ni tahrirlang -->', 1)
    open(slug + '.html', 'w', encoding='utf-8').write(page)
    print('yaratildi:', slug + '.html')
