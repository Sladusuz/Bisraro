/**
 * BISRARO — saytdagi murojaatlarni Google jadvalga yozadi va admin panelga beradi.
 *
 * O'rnatish (bir marta):
 *   1. Google Sheets'da yangi jadval oching (nomi masalan "BISRARO murojaatlar").
 *   2. Kengaytmalar (Extensions) → Apps Script. Ochilgan oynadagi kodni o'chirib,
 *      shu faylni to'liq joylang va saqlang.
 *   3. Deploy → New deployment → turi: Web app.
 *        Execute as: Me   ·   Who has access: Anyone
 *      Deploy → ruxsat bering → chiqqan "Web app URL" ni nusxalang.
 *   4. Admin panel → "Murojaatlar" → URL ni qo'yib "Saytga ulash" ni bosing.
 */

var SHEET_NAME = 'Murojaatlar';
// Admin panel kirish kodining SHA-256 xeshi (kodning o'zi bu yerda saqlanmaydi)
var KEY_HASH = '6e6e167df550e0d121d620f1e50543e3b11f49803510bb533e5e451ae430cee3';
// true qilsangiz, har yangi murojaat haqida jadval egasining pochtasiga xat keladi
var NOTIFY_EMAIL = false;

var HEADERS = ['id', 'Sana', 'Ism', 'Telefon', 'Email', 'Kompaniya', 'Xabar', 'Forma', 'Sahifa', 'Holat'];
var LIMITS  = {name: 120, phone: 40, email: 120, company: 160, message: 3000, form: 20, page: 60};

// Jadval: skript jadval ichidan ochilgan bo'lsa — o'sha jadval; aks holda
// (script.google.com'da alohida yaratilgan bo'lsa) "BISRARO murojaatlar" jadvali avtomatik yaratiladi.
function spreadsheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (ss) return ss;
  var props = PropertiesService.getScriptProperties(), id = props.getProperty('SHEET_ID');
  if (id) { try { return SpreadsheetApp.openById(id); } catch (err) {} }
  ss = SpreadsheetApp.create('BISRARO murojaatlar');
  props.setProperty('SHEET_ID', ss.getId());
  return ss;
}

function sheet_() {
  var ss = spreadsheet_();
  var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sh.getLastRow() === 0) {
    sh.appendRow(HEADERS);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  }
  return sh;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function authorized_(key) {
  if (!key) return false;
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, String(key), Utilities.Charset.UTF_8);
  var hex = bytes.map(function (b) { return ('0' + (b & 0xff).toString(16)).slice(-2); }).join('');
  return hex === KEY_HASH;
}

// Jadvalda formula sifatida ishlab ketmasligi uchun (=, +, -, @ bilan boshlangan matn)
function clean_(v, max) {
  var s = String(v == null ? '' : v).trim().slice(0, max);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

function list_() {
  var sh = sheet_(), n = sh.getLastRow() - 1;
  if (n < 1) return [];
  return sh.getRange(2, 1, n, HEADERS.length).getValues().map(function (r) {
    r = r.map(function (v) { return typeof v === 'string' ? v.replace(/^'/, '') : v; });
    return {id: String(r[0]), date: r[1] instanceof Date ? r[1].toISOString() : String(r[1]),
            name: r[2], phone: r[3], email: r[4], company: r[5], message: r[6],
            form: r[7], page: r[8], status: r[9] || 'yangi'};
  }).reverse();
}

function findRow_(sh, id) {
  var n = sh.getLastRow() - 1;
  if (n < 1) return 0;
  var ids = sh.getRange(2, 1, n, 1).getValues();
  for (var i = 0; i < ids.length; i++) if (String(ids[i][0]) === String(id)) return i + 2;
  return 0;
}

// Admin panel: murojaatlar ro'yxati
function doGet(e) {
  try { return handleGet_(e); }
  catch (err) { return json_({ok: false, error: 'script', message: String(err && err.message || err)}); }
}
function handleGet_(e) {
  var p = (e && e.parameter) || {};
  if (p.action === 'list') {
    if (!authorized_(p.key)) return json_({ok: false, error: 'auth'});
    return json_({ok: true, items: list_()});
  }
  return json_({ok: true, service: 'bisraro-forms'});
}

// Sayt: yangi murojaat · Admin panel: holatni o'zgartirish / o'chirish
function doPost(e) {
  try { return handlePost_(e); }
  catch (err) { return json_({ok: false, error: 'script', message: String(err && err.message || err)}); }
}
function handlePost_(e) {
  var d = {};
  try { d = JSON.parse((e && e.postData && e.postData.contents) || '{}'); } catch (err) { d = (e && e.parameter) || {}; }

  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var sh = sheet_();

    if (d.action === 'status' || d.action === 'delete') {
      if (!authorized_(d.key)) return json_({ok: false, error: 'auth'});
      var row = findRow_(sh, d.id);
      if (!row) return json_({ok: false, error: 'not_found'});
      if (d.action === 'delete') sh.deleteRow(row);
      else sh.getRange(row, 10).setValue(d.status === 'bajarildi' ? 'bajarildi' : 'yangi');
      return json_({ok: true});
    }

    // Yangi murojaat
    if (d.website) return json_({ok: true});               // spam-bot (yashirin maydon to'ldirilgan)
    var name = clean_(d.name, LIMITS.name), phone = clean_(d.phone, LIMITS.phone);
    if (!name || phone.replace(/\D/g, '').length < 9) return json_({ok: false, error: 'invalid'});

    var id = Utilities.getUuid();
    var msg = clean_(d.message, LIMITS.message);
    sh.appendRow([id, new Date(), name, phone, clean_(d.email, LIMITS.email), clean_(d.company, LIMITS.company),
                  msg, clean_(d.form, LIMITS.form), clean_(d.page, LIMITS.page), 'yangi']);

    if (NOTIFY_EMAIL) {
      MailApp.sendEmail(Session.getEffectiveUser().getEmail(), 'Saytdan yangi murojaat — BISRARO',
        'Ism: ' + name + '\nTelefon: ' + phone + '\nEmail: ' + (d.email || '') +
        '\nKompaniya: ' + (d.company || '') + '\n\n' + msg);
    }
    return json_({ok: true, id: id});
  } finally {
    lock.releaseLock();
  }
}
