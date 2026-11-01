#!/usr/bin/env python3
"""
Daisaku Seto's App Store Showcase Generator
App Store (iTunes Lookup API) から最新の公開アプリ情報を取得し、
洗練されたGitHub Pages向け静的ポートフォリオサイト（index.html）を自動生成します。

実行方法:
    python3 generate.py
"""

import json
import os
import urllib.request

DEVELOPER_ID = "1889853807"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_apps():
    url = f"https://itunes.apple.com/lookup?id={DEVELOPER_ID}&entity=software&country=jp"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    results = [r for r in raw.get("results", []) if r.get("wrapperType") == "software"]

    apps = []
    for a in results:
        genres = a.get("genres", [])
        genre_str = " ".join(genres).lower()
        
        category = "lifestyle"
        if any(g in genre_str for g in ["ミュージック", "music", "音"]):
            category = "music"
        elif any(g in genre_str for g in ["ゲーム", "game", "アクション", "ロールプレイング"]):
            category = "games"
        elif any(g in genre_str for g in ["仕事効率化", "ユーティリティ", "ビジネス", "辞書"]):
            category = "productivity"

        apps.append({
            "id": a.get("trackId"),
            "title": a.get("trackName"),
            "icon": a.get("artworkUrl512") or a.get("artworkUrl100"),
            "genres": genres,
            "category": category,
            "price": a.get("formattedPrice", "無料"),
            "url": a.get("trackViewUrl"),
            "description": a.get("description", ""),
            "screenshots": a.get("screenshotUrls", [])
        })
    return apps

def build_html(apps):
    apps_json = json.dumps(apps, ensure_ascii=False)
    
    return f"""<!DOCTYPE html>
<html lang="ja" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Daisaku Seto - iOS Apps Showcase</title>
  <meta name="description" content="iOSデベロッパー Daisaku SetoのApp Store公開アプリ一覧ポートフォリオ">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap");
    body {{
      font-family: "Plus Jakarta Sans", "Noto Sans JP", -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .glass {{
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .glass-card {{
      background: rgba(18, 22, 34, 0.65);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .glass-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(255, 255, 255, 0.2);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), 0 0 30px -10px rgba(59, 130, 246, 0.15);
    }}
    .glow-bg {{
      background: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.15), rgba(147, 51, 234, 0.05) 50%, transparent 80%);
    }}
  </style>
</head>
<body class="bg-[#090d16] text-slate-100 min-h-screen selection:bg-blue-500/30 selection:text-blue-200">

  <!-- Background Ambient Glow -->
  <div class="fixed inset-0 glow-bg pointer-events-none z-0"></div>

  <!-- Header / Hero Section -->
  <header class="relative z-10 pt-16 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
    <div class="flex flex-col md:flex-row items-center md:items-start justify-between gap-8 pb-10 border-b border-white/10">
      
      <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left">
        <!-- Avatar / Icon -->
        <div class="relative group">
          <div class="w-24 h-24 sm:w-28 sm:h-28 rounded-3xl bg-gradient-to-tr from-blue-600 to-indigo-500 p-[2px] shadow-2xl shadow-blue-500/20">
            <div class="w-full h-full bg-[#0d121f] rounded-[22px] flex items-center justify-center text-4xl font-black text-transparent bg-clip-text bg-gradient-to-tr from-blue-400 to-purple-400">
              DS
            </div>
          </div>
          <span class="absolute -bottom-2 -right-2 px-2.5 py-0.5 text-xs font-semibold bg-blue-500/20 text-blue-300 border border-blue-500/30 rounded-full backdrop-blur-md">
            iOS Dev
          </span>
        </div>

        <div>
          <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2 mb-2">
            <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">Daisaku Seto</h1>
            <span class="px-3 py-1 text-xs font-medium rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              {len(apps)} Apps Live
            </span>
          </div>
          <p class="text-slate-400 text-sm sm:text-base max-w-xl leading-relaxed">
            Swift & SwiftUI で日常をちょっと便利に、楽しくするiOSアプリを個人開発しています。音楽ツール、思考支援、ミニゲームなど多数公開中。
          </p>

          <!-- Links -->
          <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3 mt-4">
            <a href="https://apps.apple.com/jp/developer/daisaku-seto/id1889853807" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white/10 hover:bg-white/15 text-white border border-white/10 transition">
              <i data-lucide="apple" class="w-4 h-4"></i> App Store Developer Page
            </a>
            <a href="https://note.com/dai_hydrangea" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition">
              <i data-lucide="book-open" class="w-4 h-4"></i> note (開発記)
            </a>
          </div>
        </div>
      </div>

      <!-- Quick Stats Bento Box -->
      <div class="grid grid-cols-2 gap-3 w-full sm:w-auto">
        <div class="glass px-5 py-4 rounded-2xl text-center sm:text-left">
          <div class="text-2xl font-bold text-white tracking-tight">{len(apps)}</div>
          <div class="text-xs text-slate-400 mt-0.5">公開アプリ数</div>
        </div>
        <div class="glass px-5 py-4 rounded-2xl text-center sm:text-left">
          <div class="text-2xl font-bold text-blue-400 tracking-tight">100%</div>
          <div class="text-xs text-slate-400 mt-0.5">Swift / Native</div>
        </div>
      </div>

    </div>
  </header>

  <!-- Controls / Filter & Search -->
  <main class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24">
    
    <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mb-8">
      <!-- Tabs -->
      <div class="flex flex-wrap items-center gap-1.5 p-1.5 glass rounded-2xl w-full sm:w-auto" id="filter-tabs">
        <button onclick="setFilter('all')" class="filter-btn active px-4 py-2 rounded-xl text-xs font-medium transition bg-white/10 text-white" data-filter="all">すべて ({len(apps)})</button>
        <button onclick="setFilter('music')" class="filter-btn px-4 py-2 rounded-xl text-xs font-medium transition text-slate-400 hover:text-white" data-filter="music">🎵 音楽</button>
        <button onclick="setFilter('productivity')" class="filter-btn px-4 py-2 rounded-xl text-xs font-medium transition text-slate-400 hover:text-white" data-filter="productivity">⚡️ ツール・仕事</button>
        <button onclick="setFilter('games')" class="filter-btn px-4 py-2 rounded-xl text-xs font-medium transition text-slate-400 hover:text-white" data-filter="games">🎮 ゲーム</button>
        <button onclick="setFilter('lifestyle')" class="filter-btn px-4 py-2 rounded-xl text-xs font-medium transition text-slate-400 hover:text-white" data-filter="lifestyle">🌿 ライフ・教育</button>
      </div>

      <!-- Search Box -->
      <div class="relative w-full sm:w-72">
        <i data-lucide="search" class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"></i>
        <input 
          id="search-input" 
          type="text" 
          placeholder="アプリ名やキーワードで検索..." 
          oninput="handleSearch()"
          class="w-full pl-10 pr-4 py-2.5 rounded-xl glass text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition"
        >
      </div>
    </div>

    <!-- App Grid -->
    <div id="apps-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5"></div>

    <!-- Empty State -->
    <div id="empty-state" class="hidden text-center py-20">
      <div class="w-16 h-16 mx-auto mb-4 rounded-2xl glass flex items-center justify-center text-slate-500">
        <i data-lucide="inbox" class="w-8 h-8"></i>
      </div>
      <p class="text-slate-400 text-sm">該当するアプリが見つかりませんでした。</p>
    </div>

  </main>

  <!-- Modal for Screenshots / Details -->
  <div id="modal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md opacity-0 pointer-events-none transition-opacity duration-300">
    <div id="modal-container" class="bg-[#0f1422] border border-white/10 rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl transform scale-95 transition-transform duration-300">
      <div class="flex items-start justify-between gap-4 mb-6">
        <div class="flex items-center gap-4">
          <img id="modal-icon" src="" alt="" class="w-16 h-16 rounded-2xl shadow-lg border border-white/10">
          <div>
            <h3 id="modal-title" class="text-xl font-bold text-white leading-tight"></h3>
            <div id="modal-badges" class="flex flex-wrap gap-1.5 mt-1.5"></div>
          </div>
        </div>
        <button onclick="closeModal()" class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/10 transition">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Screenshots Carousel / Grid -->
      <div class="mb-6">
        <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Screenshots</h4>
        <div id="modal-screenshots" class="flex gap-3 overflow-x-auto pb-3 snap-x scrollbar-thin"></div>
      </div>

      <!-- Description -->
      <div class="mb-6">
        <h4 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Description</h4>
        <div id="modal-desc" class="text-xs sm:text-sm text-slate-300 leading-relaxed whitespace-pre-line max-h-60 overflow-y-auto pr-2"></div>
      </div>

      <!-- Action -->
      <div class="pt-4 border-t border-white/10 flex items-center justify-between">
        <span id="modal-price" class="text-sm font-semibold text-slate-300"></span>
        <a id="modal-link" href="#" target="_blank" rel="noopener" class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-lg shadow-blue-500/20 transition">
          <i data-lucide="apple" class="w-4 h-4"></i> App Store で開く
        </a>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="relative z-10 border-t border-white/10 py-10 text-center text-xs text-slate-500">
    <p>© Daisaku Seto - Crafted with passion for iOS.</p>
    <p class="mt-1">Hosted on GitHub Pages</p>
  </footer>

  <!-- App Data & Scripts -->
  <script>
    const apps = {apps_json};

    let currentFilter = "all";
    let searchQuery = "";

    function renderApps() {{
      const grid = document.getElementById("apps-grid");
      const emptyState = document.getElementById("empty-state");
      grid.innerHTML = "";

      const filtered = apps.filter(app => {{
        const matchesFilter = currentFilter === "all" || app.category === currentFilter;
        const matchesSearch = 
          app.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          app.genres.some(g => g.toLowerCase().includes(searchQuery.toLowerCase())) ||
          app.description.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesFilter && matchesSearch;
      }});

      if (filtered.length === 0) {{
        emptyState.classList.remove("hidden");
      }} else {{
        emptyState.classList.add("hidden");
        filtered.forEach(app => {{
          const card = document.createElement("div");
          card.className = "glass-card rounded-2xl p-5 flex flex-col justify-between group";
          
          const genresHtml = app.genres.slice(0, 2).map(g => 
            `<span class="px-2 py-0.5 text-[10px] font-medium rounded-md bg-white/5 text-slate-300 border border-white/5">${{g}}</span>`
          ).join("");

          const shortDesc = app.description.replace(/\\n/g, " ").slice(0, 70) + "...";

          card.innerHTML = `
            <div>
              <div class="flex items-start gap-4 mb-4">
                <img 
                  src="${{app.icon}}" 
                  alt="${{app.title}}" 
                  class="w-16 h-16 rounded-2xl object-cover shadow-lg border border-white/10 flex-shrink-0 group-hover:scale-105 transition duration-300"
                  loading="lazy"
                >
                <div class="min-w-0 flex-1">
                  <h3 class="font-bold text-white text-base truncate group-hover:text-blue-400 transition" title="${{app.title}}">${{app.title}}</h3>
                  <div class="flex flex-wrap gap-1 mt-1.5">
                    ${{genresHtml}}
                  </div>
                </div>
              </div>

              <p class="text-xs text-slate-400 line-clamp-3 leading-relaxed mb-4">
                ${{shortDesc}}
              </p>
            </div>

            <div class="pt-4 border-t border-white/5 flex items-center justify-between gap-2 mt-auto">
              <button 
                onclick="openModal(${{app.id}})" 
                class="px-3 py-1.5 rounded-lg text-xs font-medium text-slate-300 hover:text-white hover:bg-white/10 transition inline-flex items-center gap-1.5"
              >
                <i data-lucide="eye" class="w-3.5 h-3.5"></i> 詳細
              </button>
              <a 
                href="${{app.url}}" 
                target="_blank" 
                rel="noopener" 
                class="px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition inline-flex items-center gap-1.5"
              >
                <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i> Store
              </a>
            </div>
          `;
          grid.appendChild(card);
        }});
      }}

      lucide.createIcons();
    }}

    function setFilter(category) {{
      currentFilter = category;
      document.querySelectorAll(".filter-btn").forEach(btn => {{
        if (btn.dataset.filter === category) {{
          btn.classList.add("bg-white/10", "text-white");
          btn.classList.remove("text-slate-400");
        }} else {{
          btn.classList.remove("bg-white/10", "text-white");
          btn.classList.add("text-slate-400");
        }}
      }});
      renderApps();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById("search-input").value;
      renderApps();
    }}

    function openModal(id) {{
      const app = apps.find(a => a.id === id);
      if (!app) return;

      document.getElementById("modal-icon").src = app.icon;
      document.getElementById("modal-title").textContent = app.title;
      document.getElementById("modal-price").textContent = app.price;
      document.getElementById("modal-link").href = app.url;
      document.getElementById("modal-desc").textContent = app.description;

      const badges = document.getElementById("modal-badges");
      badges.innerHTML = app.genres.map(g => 
        `<span class="px-2.5 py-0.5 text-xs font-medium rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">${{g}}</span>`
      ).join("");

      const screenshotsDiv = document.getElementById("modal-screenshots");
      screenshotsDiv.innerHTML = "";
      if (app.screenshots && app.screenshots.length > 0) {{
        app.screenshots.forEach(src => {{
          const img = document.createElement("img");
          img.src = src;
          img.className = "h-64 sm:h-80 w-auto rounded-xl border border-white/10 object-contain shadow-md snap-start";
          img.loading = "lazy";
          screenshotsDiv.appendChild(img);
        }});
      }} else {{
        screenshotsDiv.innerHTML = `<span class="text-xs text-slate-500">スクリーンショットはありません</span>`;
      }}

      const modal = document.getElementById("modal");
      const container = document.getElementById("modal-container");
      modal.classList.remove("opacity-0", "pointer-events-none");
      modal.classList.add("opacity-100", "pointer-events-auto");
      container.classList.remove("scale-95");
      container.classList.add("scale-100");
      lucide.createIcons();
    }}

    function closeModal() {{
      const modal = document.getElementById("modal");
      const container = document.getElementById("modal-container");
      modal.classList.add("opacity-0", "pointer-events-none");
      modal.classList.remove("opacity-100", "pointer-events-auto");
      container.classList.add("scale-95");
      container.classList.remove("scale-100");
    }}

    document.getElementById("modal").addEventListener("click", (e) => {{
      if (e.target.id === "modal") closeModal();
    }});

    window.addEventListener("keydown", (e) => {{
      if (e.key === "Escape") closeModal();
    }});

    // Init
    setFilter("all");
  </script>
</body>
</html>
"""

def main():
    print(f"Fetching apps for developer ID {DEVELOPER_ID} from App Store...")
    apps = fetch_apps()
    print(f"Retrieved {len(apps)} apps.")
    
    html = build_html(apps)
    out_file = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Successfully generated {out_file}!")

if __name__ == "__main__":
    main()
