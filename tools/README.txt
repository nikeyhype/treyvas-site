Выкладка: python3 tools/regen3.py (нужен jsdom: npm i jsdom@24 в /tmp), затем git commit && git push.
regen.py копирует index.html во все страницы с их SEO-тегами; prerender2.js рендерит каждую страницу v2 для статичного HTML.
