# ✅ Deployment Checklist

## Před nasazením na GitHub:

- [x] ✅ Vytvořen kompletní kód aplikace
- [x] ✅ Přidáno všech 48 sessions
- [x] ✅ Přidáno 42 speakerů
- [x] ✅ PWA manifest vytvořen
- [x] ✅ Service Worker pro offline režim
- [x] ✅ Git repository inicializován
- [ ] 🔲 GitHub repository vytvořen (udělej na github.com/new)
- [ ] 🔲 Kód pushnutý na GitHub
- [ ] 🔲 GitHub Pages zapnutý

## Claude API (volitelné):

- [ ] 🔲 Vytvořen API klíč na console.anthropic.com
- [ ] 🔲 Klíč přidán do app.js (řádek ~200)
- [ ] 🔲 Chatbot otestován lokálně

## Po nasazení:

- [ ] 🔲 Aplikace otevřena v prohlížeči
- [ ] 🔲 Otestováno filtrování místností
- [ ] 🔲 Otestováno přidání do oblíbených
- [ ] 🔲 Otestován chatbot
- [ ] 🔲 Otestována instalace na mobil
- [ ] 🔲 Odkaz sdílen s kolegy

---

## 🎯 Tvůj akční plán:

**1. Zkopíruj projekt na svůj počítač**
```bash
# V terminálu na tvém počítači:
cd ~/Desktop  # nebo kam chceš
cp -r /home/claude/data-community-app ./
cd data-community-app
```

**2. Otevři v editoru kódu**
- VS Code, Sublime, nebo jakýkoli editor
- Prohlédni si soubory!

**3. Otestuj lokálně**
```bash
python3 -m http.server 8000
# Otevři http://localhost:8000
```

**4. Vytvoř GitHub repository**
- Jdi na https://github.com/new
- Název: `data-community-app`
- Public repository
- Create repository

**5. Pushni na GitHub**
```bash
git remote add origin https://github.com/[TVUJ-USERNAME]/data-community-app.git
git branch -M main
git push -u origin main
```

**6. Zapni GitHub Pages**
- Settings → Pages
- Source: main branch, / (root)
- Save

**7. Přidej Claude API (volitelné)**
- console.anthropic.com → API Keys
- Create Key
- Zkopíruj do app.js

**8. Sdílej s kolegy! 🎉**

---

## 📞 Potřebuješ pomoct?

Klidně se zeptej! Můžeš:
1. Otevřít Issue na GitHubu
2. Napsat v projektu 
3. Nebo se zeptat přímo tady v chatu

---

**Hodně štěstí na konferenci! 🚀**
