#!/usr/bin/env python3
"""index.html dan har bir bo'lim uchun alohida sahifa yaratadi va
mahsulotlar katalogini (products.json) HTML manbasiga statik (JS'siz ham
ko'rinadigan) holda yozib chiqadi.

Ilgari mahsulot rasmlari va ma'lumotlari faqat JavaScript ishga tushgach
qo'shilardi ("#productGrid" bo'sh div edi) — Google bunday sahifalarni
qidiruv natijalarida bosh sahifa (index.html) bilan deyarli bir xil
(dublikat) kontent deb hisoblab, faqat bosh sahifani ko'rsatardi, ichki
sahifalarni (jumladan /katalog) esa chetlab o'tardi. Endi bu skript
products.json'dagi mahsulotlarni to'g'ridan-to'g'ri HTML manbasiga va
schema.org Product ma'lumotlariga yozib qo'yadi, shunda Google birinchi
o'qishdayoq rasmlar va tavsiflarni ko'radi.

GitHub Pages /katalog manzilini katalog.html fayli bilan ochadi, shuning uchun
har bir bo'lim to'g'ridan-to'g'ri ochiladi va Google ularni alohida sahifa
sifatida ko'radi. index.html yoki products.json o'zgarganda shu skriptni
qayta ishga tushiring:

    python3 build_pages.py

Bu skript GitHub Actions orqali (.github/workflows/build-pages.yml) products.json yoki
awards.json o'zgarganda avtomatik ishga tushadi — qo'lda ishga tushirish shart emas.
"""
import html, json, re

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

# ---------- Mahsulotlarni statik HTML'ga yozish ----------

GRID_OPEN = '<div class="products" id="productGrid">'
GRID_RE = re.compile(re.escape(GRID_OPEN) + r'.*?</div>(?=\s*<p id="emptyState")', re.DOTALL)
SCHEMA_RE = re.compile(r'<script type="application/ld\+json" id="productSchema">.*?</script>\s*', re.DOTALL)
HEAD_ANCHOR_RE = re.compile(r'(</script>\n)(<link rel="icon")')


def esc(value):
    return html.escape(str('' if value is None else value), quote=True)


def product_card_html(p):
    img = p.get('img')
    if img:
        visual = '<img src="%s" alt="%s — BISRARO shokolad mahsuloti" loading="lazy">' % (
            esc(img), esc(p.get('title')))
    else:
        visual = '<svg viewBox="0 0 600 600" preserveAspectRatio="xMidYMid slice"><use href="#%s"/></svg>' % (
            esc(p.get('art') or 'art-truffle'))
    tag = '<span class="tag">%s</span>' % esc(p['tag']) if p.get('tag') else ''
    return (
        '<div class="product" role="button" tabindex="0" data-cursor="view" data-id="%s" data-cat="%s">'
        '<span class="thumb">%s%s</span>'
        '<span class="pbody"><h3>%s</h3><p>%s</p>'
        '<span class="more">Batafsil <i></i></span></span></div>'
    ) % (esc(p.get('id')), esc(p.get('cat')), visual, tag, esc(p.get('title')), esc(p.get('short')))


def products_grid_html(products):
    return GRID_OPEN + ''.join(product_card_html(p) for p in products) + '</div>'


def product_schema_block(products, site):
    items = []
    for i, p in enumerate(products):
        item = {
            '@type': 'Product',
            'name': p.get('title', ''),
            'description': p.get('desc') or p.get('short') or '',
            'brand': {'@type': 'Brand', 'name': p.get('tag') or 'BISRARO'},
        }
        img = p.get('img')
        if img and not img.startswith('data:'):
            item['image'] = site.rstrip('/') + '/' + img.lstrip('/')
        items.append({'@type': 'ListItem', 'position': i + 1, 'item': item})
    data = {
        '@context': 'https://schema.org', '@type': 'ItemList', 'name': 'BISRARO katalogi',
        'itemListElement': items,
    }
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return '<script type="application/ld+json" id="productSchema">\n%s\n</script>\n' % payload


def inject_products(page, products, site):
    page, n = GRID_RE.subn(lambda m: products_grid_html(products), page, count=1)
    assert n == 1, 'productGrid div topilmadi'
    page = SCHEMA_RE.sub('', page, count=1)
    page, n = HEAD_ANCHOR_RE.subn(lambda m: m.group(1) + product_schema_block(products, site) + m.group(2), page, count=1)
    assert n == 1, 'schema qo‘shish nuqtasi topilmadi'
    return page


def sub1(pattern, repl, text):
    out, n = re.subn(pattern, lambda m: repl, text, count=1)
    assert n == 1, pattern
    return out


products = json.load(open('products.json', encoding='utf-8'))

src = open('index.html', encoding='utf-8').read()
src = inject_products(src, products, SITE)
open('index.html', 'w', encoding='utf-8').write(src)
print('yangilandi: index.html (mahsulotlar statik yozildi)')

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

# ---------- sitemap.xml (rasmlar ro'yxati bilan) ----------
# Panel ham sitemap.xml yozadi, lekin u faqat brauzerdagi ro'yxatdan quriladi.
# Shu yerda ham products.json / awards.json dan qayta quramiz — statik HTML bilan
# bir xil manbadan, shunda Google rasmlar ro'yxati va sahifalar doim mos bo'ladi.
import datetime

def _img(src, title, seen):
    if not src or src.startswith('data:') or src in seen:
        return ''
    seen.add(src)
    return ('    <image:image>\n      <image:loc>%s</image:loc>\n      <image:title>%s</image:title>\n'
            '    </image:image>\n') % (esc(SITE + '/' + src.lstrip('/')), esc(title))


def _page(path, prio, images, today):
    return ('  <url>\n    <loc>%s/%s</loc>\n    <lastmod>%s</lastmod>\n    <changefreq>weekly</changefreq>\n'
            '    <priority>%s</priority>\n%s  </url>\n') % (SITE, path, today, prio, images)


def build_sitemap(products, awards):
    seen, today = set(), datetime.date.today().isoformat()
    home = ''.join(_img(s, t, seen) for s, t in [
        ('img/share/bisraro-1200x1200.jpg', 'BISRARO — premium shokolad va qandolat'),
        ('img/share/bisraro-1200x630.jpg', 'BISRARO — premium shokolad va qandolat'),
        ('img/bisraro-logo.webp', 'BISRARO logotipi'),
        ('img/kolleksiya/konfetlar-karta.webp', 'BISRARO konfetlari'),
        ('img/kolleksiya/plitka-karta.webp', 'BISRARO shokolad plitkalari'),
        ('img/kolleksiya/premium-karta.webp', "BISRARO premium sovg'a to'plamlari")])
    cat = ''.join(_img(p.get('img'), '%s — BISRARO shokolad mahsuloti' % p.get('title', ''), seen) for p in products)
    aw = ''.join(_img(a.get('img'), '%s — BISRARO' % a.get('title', ''), seen) for a in awards)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
            + _page('', '1.0', home, today) + _page('katalog', '0.9', cat, today)
            + _page('yutuqlarimiz', '0.7', aw, today) + _page('biz-haqimizda', '0.7', '', today)
            + _page('kontakt', '0.8', '', today) + '</urlset>\n')


awards = json.load(open('awards.json', encoding='utf-8'))
open('sitemap.xml', 'w', encoding='utf-8').write(build_sitemap(products, awards))
print('yangilandi: sitemap.xml')
