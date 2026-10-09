// Controllo automatico della pagina: immagini su computer e telefono, tema chiaro e scuro.
// Uso:  node controllo-anteprima.js "../Mappe concettuali e mentali.html"
// Richiede:  npm install playwright  e  npx playwright install chromium
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

(async () => {
  const file = path.resolve(process.argv[2] || "../Mappe concettuali e mentali.html");
  if (!fs.existsSync(file)) { console.error("File non trovato: " + file); process.exit(1); }
  const outDir = path.join(__dirname, "anteprime");
  fs.mkdirSync(outDir, { recursive: true });

  const prove = [
    ["computer-chiaro", 1280, "light"],
    ["computer-scuro", 1280, "dark"],
    ["telefono-chiaro", 400, "light"],
    ["telefono-scuro", 400, "dark"],
  ];
  const browser = await chromium.launch();
  let problemi = 0;
  for (const [nome, larghezza, tema] of prove) {
    const page = await browser.newPage({ viewport: { width: larghezza, height: 900 }, colorScheme: tema });
    const errori = [];
    page.on("pageerror", (e) => errori.push(e.message));
    page.on("console", (m) => { if (m.type() === "error") errori.push(m.text()); });
    await page.goto("file://" + file, { waitUntil: "networkidle" });
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(outDir, nome + ".png"), fullPage: true });
    const misurata = await page.evaluate(() => document.documentElement.scrollWidth);
    const esce = misurata > larghezza;
    if (esce || errori.length) problemi++;
    console.log(
      nome.padEnd(16),
      esce ? "ATTENZIONE: la pagina scorre di lato (" + misurata + " pixel)" : "larghezza ok",
      errori.length ? "| errori: " + errori.join(" ; ") : "| nessun errore"
    );
  }
  await browser.close();
  console.log(problemi ? "\nCi sono problemi da controllare." : "\nTutto a posto. Immagini in: " + outDir);
})();
