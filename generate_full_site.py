import re
import html
import subprocess
import json
import os

def parse_heading_title(raw_text):
    # Strip any HTML tags and raw bidi marks
    clean = re.sub(r'<[^>]+>', '', raw_text)
    clean = re.sub(r'&(?:lrm|rlm);|\u200e|\u200f', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)
    
    # Extract page tag if any
    page_tag = ""
    pm = re.search(r'صفحهٔ?\s*([\d\sتاو\-]+)', clean)
    if pm:
        page_tag = pm.group(0).strip()
    
    # Check if title has English in parentheses at the end
    m = re.search(r'^(.*?)\s*\(([A-Za-z][A-Za-z0-9\s,\.\-/\'"]*)\)\s*(?:—\s*(.*))?$', clean)
    if m:
        fa_main = m.group(1).strip()
        en_part = m.group(2).strip()
        extra_dash = m.group(3).strip() if m.group(3) else ""
        if extra_dash:
            fa_main = f"{fa_main} — {extra_dash}"
        return fa_main, en_part, page_tag
    else:
        return clean, "", page_tag

def build():
    print("1. Running pandoc on linear_algebra_notes_compiled.md...")
    cmd = [
        "/opt/homebrew/bin/pandoc",
        "linear_algebra_notes_compiled.md",
        "-f", "markdown+tex_math_dollars+pipe_tables",
        "-t", "html5",
        "--mathjax"
    ]
    raw_html = subprocess.check_output(cmd, encoding="utf-8")
    print(f"   Pandoc output length: {len(raw_html)} chars")

    # Remove the first H1 tag from Pandoc output so we don't have duplicate title under the hero banner
    raw_html = re.sub(r'<h1\b[^>]*>.*?</h1>', '', raw_html, count=1, flags=re.DOTALL)

    print("2. Tokenizing and fixing BiDi on parenthesized English...")
    tokens = re.split(r'(<[^>]+>)', raw_html)
    in_protected = 0
    processed_tokens = []

    for token in tokens:
        if token.startswith('<'):
            if re.match(r'<span[^>]*class="[^"]*math[^"]*"', token) or re.match(r'<code[^>]*', token) or re.match(r'<pre[^>]*', token):
                in_protected += 1
            elif (token == '</span>' or token == '</code>' or token == '</pre>') and in_protected > 0:
                in_protected -= 1
            processed_tokens.append(token)
        else:
            if in_protected == 0:
                # 1. Pure English parenthesized terms
                def wrap_en_parens(m):
                    content = m.group(1).strip()
                    return f'&lrm;<span class="en-term" dir="ltr">({content})</span>&rlm;'
                
                mod = re.sub(r'\(([A-Za-z][A-Za-z0-9\s,\.\-/\'"]*)\)', wrap_en_parens, token)

                # 2. Bilingual terms: (Persian / English)
                def wrap_bilingual(m):
                    fa = m.group(1).strip()
                    en = m.group(2).strip()
                    return f'({fa} / &lrm;<span class="en-term" dir="ltr">{en}</span>&rlm;)'
                mod = re.sub(r'\(([\u0600-\u06FF\s]+)\s*/\s*([A-Za-z][A-Za-z0-9\s,\.\-/\'"]*)\)', wrap_bilingual, mod)

                processed_tokens.append(mod)
            else:
                processed_tokens.append(token)

    body_html = "".join(processed_tokens)

    print("3. Styling Callout blocks (definitions, theorems, examples, notes)...")
    def callout_replacer(m):
        full = m.group(0)
        p_content = m.group(1)
        strong_text = m.group(2)
        
        c_class = ""
        c_icon = ""
        if "تعریف" in strong_text:
            c_class = "callout-def"
            c_icon = "💡 تعریف"
        elif "قضیه" in strong_text:
            c_class = "callout-thm"
            c_icon = "📜 قضیه"
        elif "لم" in strong_text:
            c_class = "callout-lem"
            c_icon = "📌 لم"
        elif "نتیجه" in strong_text:
            c_class = "callout-cor"
            c_icon = "🎯 نتیجه"
        elif "مثال" in strong_text:
            c_class = "callout-example"
            c_icon = "✏️ مثال"
        elif "برهان" in strong_text or "اثبات" in strong_text:
            c_class = "callout-proof"
            c_icon = "🔍 اثبات"
        elif "نکته" in strong_text or "تذکر" in strong_text or "یادداشت" in strong_text:
            c_class = "callout-note"
            c_icon = "⚠️ نکته"
        
        if c_class:
            return f'<div class="callout {c_class}"><div class="callout-header"><span class="callout-badge">{c_icon}</span></div><div class="callout-body"><p>{p_content}</p></div></div>'
        return full

    body_html = re.sub(r'<p>(<strong>([^<]+)</strong>(.*?))</p>', callout_replacer, body_html, flags=re.DOTALL)

    print("4. Enhancing display math with copy buttons and scroll containers...")
    def math_display_replacer(m):
        math_content = m.group(1)
        raw_tex = html.escape(math_content.strip())
        return f'''<div class="math-display-container">
  <div class="math-display-scroll"><span class="math display">\\[{math_content}\\]</span></div>
  <button class="copy-math-btn" data-latex="{raw_tex}" onclick="copyFormula(this)" title="کپی فرمول LaTeX">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
    <span>کپی LaTeX</span>
  </button>
</div>'''

    body_html = re.sub(r'<p><span class="math display">\\\[(.*?)\\\]</span></p>', math_display_replacer, body_html, flags=re.DOTALL)
    body_html = re.sub(r'(?<!<div class="math-display-scroll">)<span class="math display">\\\[(.*?)\\\]</span>', math_display_replacer, body_html, flags=re.DOTALL)

    print("5. Processing headings and building search index...")
    headings = []
    search_index = []

    def heading_processor(m):
        tag = m.group(1)
        hid = m.group(2)
        inner = m.group(3)
        
        fa_title, en_title, page_tag = parse_heading_title(inner)
        
        headings.append({
            'tag': tag,
            'id': hid,
            'title_fa': fa_title,
            'title_en': en_title,
            'page_tag': page_tag
        })
        
        # Add to search index
        search_index.append({
            'id': hid,
            'title': f"{fa_title} {en_title}".strip(),
            'level': tag
        })
        
        # Render clean heading HTML with isolated parts
        page_badge = f'<span class="page-tag">{page_tag}</span>' if page_tag and tag in ['h2', 'h3'] else ''
        en_badge = f'&lrm;<span class="heading-en" dir="ltr">({en_title})</span>&rlm;' if en_title else ''
        anchor = f'<a class="header-anchor" href="#{hid}" aria-label="پیوند مستقیم به این بخش">#</a>'
        
        return f'''<{tag} id="{hid}" class="heading-linked">
  <span class="heading-fa">{fa_title}</span>
  {en_badge}
  {page_badge}
  {anchor}
</{tag}>'''

    body_html = re.sub(r'<(h[1-3])\s+id="([^"]+)">(.*?)</\1>', heading_processor, body_html, flags=re.DOTALL)

    # Index callouts for search
    callout_matches = re.finditer(r'<div class="callout (callout-[a-z]+)">.*?<p><strong>([^<]+)</strong>(.*?)</p>', body_html, re.DOTALL)
    for idx, cm in enumerate(callout_matches):
        c_type = cm.group(1).replace('callout-', '')
        c_title = cm.group(2).strip()
        c_snippet = re.sub(r'<[^>]+>', '', cm.group(3))[:120].strip()
        search_index.append({
            'id': f'callout-{idx}',
            'title': f'{c_title}: {c_snippet}...',
            'level': 'callout',
            'type': c_type
        })

    print(f"   Indexed {len(search_index)} searchable items.")

    print("6. Building hierarchical Table of Contents...")
    groups = [
        {
            "id": "group-1",
            "title": "فصل ۱ تا ۴: فضاهای برداری و پایه",
            "desc": "صفحات ۱ تا ۲۵",
            "icon": "📐",
            "items": []
        },
        {
            "id": "group-2",
            "title": "فصل ۵ تا ۱۲: بعد، تبدیل‌های خطی و ماتریس‌ها",
            "desc": "صفحات ۲۶ تا ۴۹",
            "icon": "🔄",
            "items": []
        },
        {
            "id": "group-3",
            "title": "فصل ۱۵ تا ۱۸: رتبه، دستگاه‌های خطی، وارون و دترمینان",
            "desc": "صفحات ۷۴ تا ۱۱۰",
            "icon": "🔢",
            "items": []
        }
    ]

    current_group_idx = 0
    current_h2_item = None

    for h in headings:
        if h['tag'] == 'h1':
            continue
        
        fa_t = h['title_fa']
        if any(marker in fa_t for marker in ['(۵) وجود پایه', 'صفحه ۲۶', 'بخش ۵']):
            current_group_idx = 1
        elif any(marker in fa_t for marker in ['صفحه ۷۴', 'بخش ۱۵', 'رتبه سطری']):
            current_group_idx = 2
            
        if h['tag'] == 'h2':
            current_h2_item = {
                'id': h['id'],
                'title_fa': fa_t,
                'title_en': h['title_en'],
                'children': []
            }
            groups[current_group_idx]['items'].append(current_h2_item)
        elif h['tag'] == 'h3' and current_h2_item is not None:
            current_h2_item['children'].append({
                'id': h['id'],
                'title_fa': fa_t,
                'title_en': h['title_en']
            })

    # Render TOC HTML
    toc_parts = []
    for g_idx, g in enumerate(groups):
        open_attr = "open" if g_idx == 0 else ""
        toc_parts.append(f'''<details class="toc-accordion" {open_attr} id="{g['id']}">
  <summary class="toc-accordion-summary">
    <span class="toc-acc-icon">{g['icon']}</span>
    <div class="toc-acc-text">
      <span class="toc-acc-title">{html.escape(g['title'])}</span>
      <span class="toc-acc-desc">{html.escape(g['desc'])}</span>
    </div>
    <span class="toc-acc-arrow">▾</span>
  </summary>
  <div class="toc-accordion-content">''')
        
        for h2 in g['items']:
            en_h2_html = f'<div class="toc-title-en" dir="ltr">{html.escape(h2["title_en"])}</div>' if h2["title_en"] else ''
            toc_parts.append(f'''    <div class="toc-item-h2">
      <a href="#{h2['id']}" class="toc-link toc-link-h2" data-id="{h2['id']}">
        <div class="toc-title-fa">{html.escape(h2['title_fa'])}</div>
        {en_h2_html}
      </a>''')
            if h2['children']:
                toc_parts.append('      <div class="toc-sublist">')
                for h3 in h2['children']:
                    en_h3_html = f'<div class="toc-title-en" dir="ltr">{html.escape(h3["title_en"])}</div>' if h3["title_en"] else ''
                    toc_parts.append(f'''        <a href="#{h3["id"]}" class="toc-link toc-link-h3" data-id="{h3["id"]}">
          <div class="toc-title-fa">{html.escape(h3["title_fa"])}</div>
          {en_h3_html}
        </a>''')
                toc_parts.append('      </div>')
            toc_parts.append('    </div>')
        
        toc_parts.append('  </div>\n</details>')

    toc_html_rendered = "\n".join(toc_parts)
    search_index_json = json.dumps(search_index, ensure_ascii=False)

    print("7. Assembling final standalone HTML...")
    full_html = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="light dark" />
  <meta name="description" content="جزوه جامع مبانی ماتریس و جبر خطی بر اساس کتاب هافمن و کونزه و تدریس دکتر طوسی - دانشگاه" />
  <title>جزوه جامع مبانی ماتریس و جبر خطی | Matrix Foundations and Linear Algebra</title>

  <!-- Prevent FOUC for color scheme according to modern web guidance -->
  <script>
    try {{
      const storedScheme = localStorage.getItem("color-scheme");
      if (storedScheme) {{
        document.querySelector('meta[name="color-scheme"]').content = storedScheme;
      }}
    }} catch(e) {{}}
  </script>

  <!-- Typography & Fonts: Vazirmatn -->
  <link rel="preconnect" href="https://cdn.jsdelivr.net" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css" />

  <!-- MathJax Configuration -->
  <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true,
        packages: {{'[+]': ['ams', 'color', 'cases', 'matrix']}}
      }},
      options: {{
        ignoreHtmlClass: 'tex2jax_ignore',
        processHtmlClass: 'tex2jax_process'
      }},
      chtml: {{
        scale: 1,
        minScale: 0.8,
        matchFontHeight: true
      }},
      startup: {{
        pageReady: () => {{
          return MathJax.startup.defaultPageReady().then(() => {{
            document.body.classList.add('mathjax-ready');
          }});
        }}
      }}
    }};
  </script>
  <script id="MathJax-script" defer src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"></script>

  <style>
    /* ----------------------------------------------------
       Design System & Variables (Modern CSS light-dark())
       ---------------------------------------------------- */
    :root {{
      color-scheme: light dark;

      /* Neutral Palette */
      --bg-canvas: light-dark(#f8fafc, #0b0f19);
      --bg-surface: light-dark(#ffffff, #111827);
      --bg-sidebar: light-dark(#f1f5f9, #0f172a);
      --bg-subtle: light-dark(#f8fafc, #1e293b);
      --bg-hover: light-dark(#e2e8f0, #334155);

      --text-main: light-dark(#0f172a, #f1f5f9);
      --text-muted: light-dark(#475569, #94a3b8);
      --text-faint: light-dark(#64748b, #64748b);

      --border-subtle: light-dark(#e2e8f0, #1e293b);
      --border-strong: light-dark(#cbd5e1, #334155);

      /* Brand Accent Colors */
      --brand-indigo: light-dark(#4f46e5, #818cf8);
      --brand-indigo-subtle: light-dark(#eef2ff, rgba(99, 102, 241, 0.12));
      --brand-violet: light-dark(#7c3aed, #a78bfa);

      /* Callout Themes */
      --def-border: #3b82f6;
      --def-bg: light-dark(#eff6ff, rgba(59, 130, 246, 0.08));
      --thm-border: #8b5cf6;
      --thm-bg: light-dark(#f5f3ff, rgba(139, 92, 246, 0.08));
      --lem-border: #6366f1;
      --lem-bg: light-dark(#eef2ff, rgba(99, 102, 241, 0.08));
      --cor-border: #06b6d4;
      --cor-bg: light-dark(#ecfeff, rgba(6, 182, 212, 0.08));
      --example-border: #10b981;
      --example-bg: light-dark(#ecfdf5, rgba(16, 185, 129, 0.08));
      --note-border: #f59e0b;
      --note-bg: light-dark(#fffbeb, rgba(245, 158, 11, 0.08));
      --proof-border: #64748b;
      --proof-bg: light-dark(#f8fafc, rgba(100, 116, 139, 0.06));

      /* Sizing */
      --header-height: 64px;
      --sidebar-width: 330px;
      --content-max-width: 880px;
      --font-scale: 16px;

      /* Shadows */
      --shadow-sm: light-dark(0 1px 2px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.4));
      --shadow-md: light-dark(0 4px 6px -1px rgba(0,0,0,0.07), 0 4px 8px -1px rgba(0,0,0,0.5));
      --shadow-lg: light-dark(0 10px 15px -3px rgba(0,0,0,0.08), 0 10px 20px -3px rgba(0,0,0,0.6));
    }}

    /* Modern color-scheme selectors mapped from meta */
    :root:has(> head > meta[name="color-scheme"][content="dark"]) {{
      color-scheme: dark;
    }}
    :root:has(> head > meta[name="color-scheme"][content="light"]) {{
      color-scheme: light;
    }}

    /* Global Reset & Base */
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html {{
      direction: rtl;
      font-size: var(--font-scale);
      scroll-behavior: smooth;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }}

    body {{
      direction: rtl;
      text-align: right;
      font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, Tahoma, sans-serif;
      background-color: var(--bg-canvas);
      color: var(--text-main);
      line-height: 1.95;
      font-size: 1rem;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* Reading Progress Bar */
    #progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 3.5px;
      background: linear-gradient(to left, #4f46e5, #8b5cf6, #ec4899);
      z-index: 1000;
      transition: width 0.1s ease-out;
    }}

    /* Top Sticky Header */
    .top-header {{
      position: sticky;
      top: 0;
      height: var(--header-height);
      background: light-dark(rgba(255, 255, 255, 0.85), rgba(17, 24, 39, 0.85));
      backdrop-filter: blur(12px) saturate(180%);
      -webkit-backdrop-filter: blur(12px) saturate(180%);
      border-bottom: 1px solid var(--border-subtle);
      z-index: 900;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
      gap: 1rem;
    }}

    .header-brand {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
      text-decoration: none;
      color: var(--text-main);
    }}

    .header-logo-icon {{
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--brand-indigo), var(--brand-violet));
      color: #fff;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.15rem;
      box-shadow: 0 2px 6px rgba(79, 70, 229, 0.35);
    }}

    .header-titles {{
      display: flex;
      flex-direction: column;
    }}

    .header-title {{
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1.3;
    }}

    .header-sub {{
      font-size: 0.76rem;
      color: var(--text-muted);
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    /* Header Buttons & Controls */
    .btn-icon {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      border-radius: 8px;
      padding: 0.45rem 0.75rem;
      font-size: 0.85rem;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.15s ease;
      box-shadow: var(--shadow-sm);
    }}

    .btn-icon:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
      border-color: var(--border-strong);
    }}

    .search-trigger {{
      padding: 0.45rem 1rem;
      background: var(--bg-canvas);
      border: 1px solid var(--border-strong);
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.85rem;
      min-width: 170px;
      transition: all 0.2s;
    }}

    .search-trigger:hover {{
      border-color: var(--brand-indigo);
      background: var(--bg-surface);
      color: var(--text-main);
    }}

    .search-shortcut {{
      font-size: 0.7rem;
      background: var(--bg-hover);
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      border: 1px solid var(--border-subtle);
      margin-right: auto;
    }}

    .font-size-group {{
      display: flex;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      overflow: hidden;
      background: var(--bg-surface);
    }}

    .font-btn {{
      background: transparent;
      border: none;
      padding: 0.35rem 0.6rem;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.8rem;
      font-family: inherit;
      transition: background 0.15s;
    }}

    .font-btn:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
    }}

    .mobile-menu-btn {{
      display: none;
    }}

    /* Main App Layout */
    .app-container {{
      display: grid;
      grid-template-columns: var(--sidebar-width) 1fr;
      min-height: calc(100vh - var(--header-height));
    }}

    /* Sidebar Navigation */
    .sidebar {{
      position: sticky;
      top: var(--header-height);
      height: calc(100vh - var(--header-height));
      overflow-y: auto;
      background: var(--bg-sidebar);
      border-left: 1px solid var(--border-subtle);
      padding: 1.25rem 1rem 3rem 1rem;
      scrollbar-width: thin;
      scrollbar-color: var(--border-strong) transparent;
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}

    .sidebar::-webkit-scrollbar {{
      width: 6px;
    }}
    .sidebar::-webkit-scrollbar-thumb {{
      background: var(--border-strong);
      border-radius: 4px;
    }}

    .sidebar-stats-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 0.85rem 1rem;
      font-size: 0.82rem;
      color: var(--text-muted);
      box-shadow: var(--shadow-sm);
    }}

    .stats-row {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.35rem;
    }}
    .stats-row:last-child {{
      margin-bottom: 0;
    }}
    .stats-badge {{
      font-weight: 700;
      color: var(--brand-indigo);
    }}

    /* Sidebar TOC Accordion */
    .toc-accordion {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      margin-bottom: 0.75rem;
      box-shadow: var(--shadow-sm);
    }}

    .toc-accordion[open] {{
      border-color: var(--border-strong);
    }}

    .toc-accordion-summary {{
      padding: 0.75rem 0.9rem;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      cursor: pointer;
      user-select: none;
      background: var(--bg-surface);
      transition: background 0.15s;
    }}

    .toc-accordion-summary:hover {{
      background: var(--bg-hover);
    }}

    .toc-acc-icon {{
      font-size: 1.1rem;
    }}

    .toc-acc-text {{
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .toc-acc-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.35;
    }}

    .toc-acc-desc {{
      font-size: 0.72rem;
      color: var(--text-faint);
    }}

    .toc-acc-arrow {{
      font-size: 0.8rem;
      color: var(--text-faint);
      transition: transform 0.2s ease;
    }}

    .toc-accordion[open] .toc-acc-arrow {{
      transform: rotate(180deg);
    }}

    .toc-accordion-content {{
      padding: 0.4rem 0.5rem 0.75rem 0.5rem;
      background: var(--bg-subtle);
      border-top: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }}

    .toc-item-h2 {{
      margin-bottom: 0.35rem;
    }}

    .toc-link {{
      display: block;
      text-decoration: none;
      border-radius: 6px;
      padding: 0.4rem 0.6rem;
      transition: all 0.15s ease;
    }}

    .toc-title-fa {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-main);
      line-height: 1.4;
    }}

    .toc-title-en {{
      font-size: 0.71rem;
      color: var(--text-faint);
      direction: ltr !important;
      text-align: left;
      line-height: 1.3;
      margin-top: 0.15rem;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    .toc-link-h3 {{
      padding-right: 1.25rem;
      position: relative;
    }}

    .toc-link-h3::before {{
      content: "•";
      position: absolute;
      right: 0.5rem;
      top: 0.4rem;
      color: var(--text-faint);
    }}

    .toc-link:hover {{
      background: var(--bg-hover);
    }}

    .toc-link:hover .toc-title-fa {{
      color: var(--brand-indigo);
    }}

    .toc-link.active {{
      background: var(--brand-indigo-subtle);
    }}
    .toc-link.active .toc-title-fa {{
      color: var(--brand-indigo);
      font-weight: 700;
    }}

    /* Main Content Area */
    .main-content {{
      padding: 2.5rem 3rem 6rem 3rem;
      max-width: var(--content-max-width);
      margin: 0 auto;
      width: 100%;
    }}

    /* Hero Banner */
    .hero-banner {{
      background: linear-gradient(135deg, var(--bg-surface), var(--brand-indigo-subtle));
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 2.5rem;
      margin-bottom: 3rem;
      box-shadow: var(--shadow-md);
      position: relative;
      overflow: hidden;
    }}

    .hero-banner::after {{
      content: "";
      position: absolute;
      left: -50px;
      bottom: -50px;
      width: 180px;
      height: 180px;
      background: radial-gradient(circle, var(--brand-indigo) 0%, transparent 70%);
      opacity: 0.12;
      border-radius: 50%;
    }}

    .hero-title {{
      font-size: 2.1rem;
      font-weight: 800;
      color: var(--text-main);
      margin-bottom: 0.75rem;
      line-height: 1.35;
    }}

    .hero-title-en {{
      display: inline-block;
      direction: ltr !important;
      unicode-bidi: isolate !important;
      color: var(--brand-indigo);
      font-size: 0.65em;
      font-weight: 600;
      margin-right: 0.5rem;
    }}

    .hero-subtitle {{
      font-size: 1.05rem;
      color: var(--text-muted);
      margin-bottom: 1.5rem;
      line-height: 1.7;
    }}

    .hero-badges {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
    }}

    .hero-badge {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      padding: 0.35rem 0.85rem;
      border-radius: 20px;
      font-size: 0.82rem;
      color: var(--text-muted);
    }}

    /* Typography & BiDi Isolation */
    h1, h2, h3, h4, h5, h6 {{
      color: var(--text-main);
      font-weight: 700;
      margin-top: 2.5rem;
      margin-bottom: 1.2rem;
      line-height: 1.45;
      position: relative;
    }}

    h2 {{
      font-size: 1.55rem;
      padding-bottom: 0.6rem;
      border-bottom: 2px solid var(--border-subtle);
      margin-top: 3.5rem;
    }}

    h3 {{
      font-size: 1.25rem;
      margin-top: 2.2rem;
    }}

    p {{
      margin: 1.15rem 0;
      color: var(--text-main);
    }}

    /* Heading Separation (Persian + English) */
    .heading-fa {{
      display: inline;
    }}

    .heading-en {{
      display: inline-block;
      direction: ltr !important;
      unicode-bidi: isolate !important;
      color: var(--brand-indigo);
      font-size: 0.82em;
      font-weight: 500;
      margin-right: 0.5rem;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    /* Page Tag Pill */
    .page-tag {{
      display: inline-block;
      font-size: 0.72rem;
      font-weight: 600;
      background: var(--brand-indigo-subtle);
      color: var(--brand-indigo);
      border: 1px solid var(--brand-indigo);
      padding: 0.12rem 0.55rem;
      border-radius: 12px;
      vertical-align: middle;
      margin-right: 0.5rem;
    }}

    /* English Term (BiDi Protection - NEVER BREAKS ACROSS LINES) */
    .en-term {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block !important;
      white-space: nowrap !important;
      color: var(--brand-indigo);
      font-size: 0.92em;
      padding: 0 0.18rem;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-weight: 500;
    }}

    /* Heading Anchor Link */
    .header-anchor {{
      opacity: 0;
      margin-right: 0.5rem;
      color: var(--brand-indigo);
      text-decoration: none;
      font-weight: 400;
      transition: opacity 0.15s;
    }}

    .heading-linked:hover .header-anchor {{
      opacity: 1;
    }}

    /* Lists */
    ul, ol {{
      margin: 1.15rem 0;
      padding-right: 1.6rem;
    }}

    li {{
      margin: 0.5rem 0;
    }}

    /* Code & Pre */
    code {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.88em;
      background: var(--bg-hover);
      padding: 0.15rem 0.45rem;
      border-radius: 5px;
      color: var(--brand-indigo);
    }}

    pre {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 1.2rem;
      overflow-x: auto;
      margin: 1.5rem 0;
    }}

    pre code {{
      background: transparent;
      padding: 0;
    }}

    /* Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 2rem 0;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
    }}

    th, td {{
      padding: 0.75rem 1rem;
      border: 1px solid var(--border-subtle);
      text-align: center;
    }}

    th {{
      background: var(--bg-subtle);
      font-weight: 700;
      color: var(--text-main);
    }}

    tbody tr:hover {{
      background: var(--bg-hover);
    }}

    /* Blockquotes */
    blockquote {{
      background: var(--bg-surface);
      border-right: 4px solid var(--brand-indigo);
      border-left: none;
      border-radius: 0 10px 10px 0;
      padding: 1.2rem 1.6rem;
      margin: 1.75rem 0;
      color: var(--text-muted);
      box-shadow: var(--shadow-sm);
    }}

    /* Callouts */
    .callout {{
      border-radius: 12px;
      margin: 1.75rem 0;
      border-right: 5px solid transparent;
      padding: 1.25rem 1.5rem;
      box-shadow: var(--shadow-sm);
      position: relative;
    }}

    .callout-header {{
      display: flex;
      align-items: center;
      margin-bottom: 0.5rem;
    }}

    .callout-badge {{
      font-size: 0.85rem;
      font-weight: 700;
      padding: 0.2rem 0.65rem;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }}

    .callout-body p:first-child {{
      margin-top: 0;
    }}
    .callout-body p:last-child {{
      margin-bottom: 0;
    }}

    .callout-def {{
      background: var(--def-bg);
      border-right-color: var(--def-border);
    }}
    .callout-def .callout-badge {{
      background: rgba(59, 130, 246, 0.15);
      color: #2563eb;
    }}

    .callout-thm {{
      background: var(--thm-bg);
      border-right-color: var(--thm-border);
    }}
    .callout-thm .callout-badge {{
      background: rgba(139, 92, 246, 0.15);
      color: #7c3aed;
    }}

    .callout-lem {{
      background: var(--lem-bg);
      border-right-color: var(--lem-border);
    }}
    .callout-lem .callout-badge {{
      background: rgba(99, 102, 241, 0.15);
      color: #4f46e5;
    }}

    .callout-cor {{
      background: var(--cor-bg);
      border-right-color: var(--cor-border);
    }}
    .callout-cor .callout-badge {{
      background: rgba(6, 182, 212, 0.15);
      color: #0891b2;
    }}

    .callout-example {{
      background: var(--example-bg);
      border-right-color: var(--example-border);
    }}
    .callout-example .callout-badge {{
      background: rgba(16, 185, 129, 0.15);
      color: #059669;
    }}

    .callout-note {{
      background: var(--note-bg);
      border-right-color: var(--note-border);
    }}
    .callout-note .callout-badge {{
      background: rgba(245, 158, 11, 0.15);
      color: #d97706;
    }}

    .callout-proof {{
      background: var(--proof-bg);
      border-right-color: var(--proof-border);
    }}
    .callout-proof .callout-badge {{
      background: rgba(100, 116, 139, 0.15);
      color: #475569;
    }}

    /* MathJax Containers & Copy Button */
    .math-display-container {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      position: relative;
      margin: 1.75rem 0;
      padding: 1.25rem 1.5rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: border-color 0.2s;
    }}

    .math-display-container:hover {{
      border-color: var(--brand-indigo);
    }}

    .math-display-scroll {{
      width: 100%;
      overflow-x: auto;
      text-align: center;
      padding: 0.25rem 0;
      scrollbar-width: thin;
      scrollbar-color: var(--border-strong) transparent;
    }}

    .copy-math-btn {{
      position: absolute;
      top: 8px;
      left: 8px;
      opacity: 0;
      background: var(--bg-subtle);
      border: 1px solid var(--border-strong);
      border-radius: 6px;
      padding: 0.25rem 0.5rem;
      font-size: 0.72rem;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.15s ease;
      font-family: inherit;
    }}

    .math-display-container:hover .copy-math-btn {{
      opacity: 1;
    }}

    .copy-math-btn:hover {{
      background: var(--brand-indigo);
      color: #fff;
      border-color: var(--brand-indigo);
    }}

    .math.inline, mjx-container:not([display="true"]) {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block;
      margin: 0 3px;
      vertical-align: middle;
    }}

    mjx-container[display="true"] {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      margin: 0.5em 0 !important;
    }}

    /* Floating Back to Top Button */
    #back-to-top {{
      position: fixed;
      bottom: 2rem;
      left: 2rem;
      background: var(--brand-indigo);
      color: #fff;
      border: none;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: var(--shadow-lg);
      cursor: pointer;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s, transform 0.25s;
      z-index: 800;
    }}

    #back-to-top.visible {{
      opacity: 1;
      pointer-events: auto;
    }}

    #back-to-top:hover {{
      transform: translateY(-3px);
    }}

    /* Live Search Modal */
    .search-modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.65);
      backdrop-filter: blur(4px);
      z-index: 2000;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 10vh;
    }}

    .search-modal-backdrop.open {{
      display: flex;
    }}

    .search-modal {{
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 14px;
      width: 90%;
      max-width: 620px;
      box-shadow: var(--shadow-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      max-height: 75vh;
    }}

    .search-input-wrapper {{
      display: flex;
      align-items: center;
      padding: 0.85rem 1.25rem;
      border-bottom: 1px solid var(--border-subtle);
      gap: 0.75rem;
    }}

    .search-input-field {{
      flex: 1;
      border: none;
      background: transparent;
      font-size: 1.05rem;
      font-family: inherit;
      color: var(--text-main);
      outline: none;
    }}

    .search-results-list {{
      overflow-y: auto;
      padding: 0.5rem;
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
    }}

    .search-result-item {{
      padding: 0.75rem 1rem;
      border-radius: 8px;
      text-decoration: none;
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      transition: background 0.15s;
    }}

    .search-result-item:hover, .search-result-item.selected {{
      background: var(--bg-hover);
    }}

    .search-result-title {{
      font-size: 0.9rem;
      font-weight: 600;
      line-height: 1.4;
    }}

    .search-result-pill {{
      font-size: 0.72rem;
      padding: 0.15rem 0.5rem;
      border-radius: 12px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-subtle);
      color: var(--text-faint);
      white-space: nowrap;
    }}

    .search-empty {{
      padding: 2.5rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.95rem;
    }}

    /* Highlight Animation for Search Navigation */
    @keyframes highlightPulse {{
      0% {{ background-color: var(--brand-indigo-subtle); }}
      100% {{ background-color: transparent; }}
    }}
    .search-highlighted {{
      animation: highlightPulse 2.5s ease-out;
      border-radius: 8px;
    }}

    /* Mobile Drawer & Responsiveness */
    @media (max-width: 900px) {{
      .app-container {{
        grid-template-columns: 1fr;
      }}

      .sidebar {{
        position: fixed;
        right: 0;
        top: var(--header-height);
        bottom: 0;
        width: 85%;
        max-width: 320px;
        z-index: 950;
        transform: translateX(100%);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: -4px 0 20px rgba(0, 0, 0, 0.25);
      }}

      .sidebar.open {{
        transform: translateX(0);
      }}

      .sidebar-backdrop {{
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 940;
        display: none;
      }}
      .sidebar-backdrop.open {{
        display: block;
      }}

      .mobile-menu-btn {{
        display: inline-flex;
      }}

      .main-content {{
        padding: 1.5rem 1.25rem 4rem 1.25rem;
      }}

      .hero-banner {{
        padding: 1.5rem;
      }}
      .hero-title {{
        font-size: 1.6rem;
      }}

      .search-trigger {{
        min-width: auto;
      }}
      .search-shortcut {{
        display: none;
      }}
    }}

    /* Print Optimization */
    @media print {{
      #progress-bar, .top-header, .sidebar, #back-to-top, .search-modal-backdrop, .copy-math-btn {{
        display: none !important;
      }}
      body {{
        background: #fff !important;
        color: #000 !important;
        font-size: 12pt !important;
        line-height: 1.6 !important;
      }}
      .app-container {{
        display: block !important;
      }}
      .main-content {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .hero-banner {{
        border: 1px solid #ccc !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 1rem !important;
      }}
      .callout {{
        border: 1px solid #999 !important;
        box-shadow: none !important;
        break-inside: avoid;
        page-break-inside: avoid;
      }}
      .math-display-container {{
        border: none !important;
        box-shadow: none !important;
        break-inside: avoid;
        page-break-inside: avoid;
      }}
      h1, h2, h3 {{
        page-break-after: avoid;
        break-after: avoid;
      }}
    }}
  </style>
</head>
<body>
  <!-- Reading Progress Bar -->
  <div id="progress-bar"></div>

  <!-- Top Sticky Navigation Bar -->
  <header class="top-header">
    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <button class="btn-icon mobile-menu-btn" onclick="toggleSidebar()" aria-label="منوی سرفصل‌ها">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      <a href="#" class="header-brand">
        <div class="header-logo-icon">∑</div>
        <div class="header-titles">
          <span class="header-title">مبانی ماتریس و جبر خطی</span>
          <span class="header-sub">جزوه جامع دانشگاهی | تدریس دکتر طوسی (هافمن - کونزه)</span>
        </div>
      </a>
    </div>

    <div class="header-actions">
      <!-- Search Trigger -->
      <button class="search-trigger" onclick="openSearchModal()" title="جستجو در متن جزوه (⌘K)">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <span>جستجو...</span>
        <kbd class="search-shortcut">⌘K</kbd>
      </button>

      <!-- Font Size Adjuster -->
      <div class="font-size-group" title="تنظیم اندازه قلم">
        <button class="font-btn" onclick="adjustFontSize(-1)" title="کوچک‌تر">A-</button>
        <button class="font-btn" onclick="resetFontSize()" title="پیش‌فرض">A</button>
        <button class="font-btn" onclick="adjustFontSize(1)" title="بزرگ‌تر">A+</button>
      </div>

      <!-- Color Scheme Toggle according to modern-web-guidance -->
      <button class="btn-icon" id="theme-toggle-btn" onclick="toggleTheme()" title="تغییر تم (روشن / تاریک)">
        <svg id="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        <svg id="theme-icon-moon" style="display:none;" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>

      <!-- Print / Export Button -->
      <button class="btn-icon" onclick="window.print()" title="چاپ یا ذخیره به صورت PDF">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      </button>
    </div>
  </header>

  <!-- Mobile Drawer Backdrop -->
  <div class="sidebar-backdrop" id="sidebar-backdrop" onclick="toggleSidebar()"></div>

  <!-- App Body Layout -->
  <div class="app-container">
    <!-- Sidebar Navigation -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-stats-card">
        <div class="stats-row">
          <span>تعداد فصول آموزشی:</span>
          <span class="stats-badge">۱۸ مبحث</span>
        </div>
        <div class="stats-row">
          <span>پوشش جزوه:</span>
          <span class="stats-badge">۱۱۰ صفحه کامل</span>
        </div>
        <div class="stats-row">
          <span>فرمول‌ها و روابط:</span>
          <span class="stats-badge">+۱,۷۰۰ معادله</span>
        </div>
      </div>

      <!-- Quick Search inside Sidebar -->
      <div style="position: relative;">
        <input type="text" id="sidebar-filter-input" placeholder="فیلتر سرفصل‌ها..." oninput="filterTocItems(this.value)" style="width: 100%; padding: 0.45rem 0.85rem; border-radius: 8px; border: 1px solid var(--border-subtle); background: var(--bg-surface); color: var(--text-main); font-family: inherit; font-size: 0.82rem; outline: none;" />
      </div>

      <!-- Hierarchical Table of Contents Accordion -->
      <nav id="toc-nav">
        {toc_html_rendered}
      </nav>
    </aside>

    <!-- Main Content Reader -->
    <main class="main-content">
      <!-- Hero Header Card -->
      <div class="hero-banner">
        <h1 class="hero-title">
          <span>جزوه جامع مبانی ماتریس و جبر خطی</span>
          <span class="hero-title-en" dir="ltr">(Matrix Foundations and Linear Algebra)</span>
        </h1>
        <p class="hero-subtitle">
          مجموعه کامل درس‌نامه‌ها، تعاریف اصول موضوعی، اثبات قضایا، فرمول‌ها و مثال‌های تشریحی مبانی ماتریس و جبر خطی بر اساس کتاب کنت هافمن و ری کونزه به همراه تدریس‌های کلاسی دانشگاهی دکتر طوسی.
        </p>
        <div class="hero-badges">
          <span class="hero-badge">📐 فضاهای برداری و زیرفضاها</span>
          <span class="hero-badge">⚡ استقلال خطی و پایه</span>
          <span class="hero-badge">🔄 تبدیل‌های خطی و نمایش ماتریسی</span>
          <span class="hero-badge">🔢 رتبه، فضا پوچ و دستگاه‌ها</span>
          <span class="hero-badge">📊 محاسبه وارون و دترمینان</span>
        </div>
      </div>

      <!-- Article Body with Enhanced BiDi, Callouts and Math -->
      <article id="article-body">
        {body_html}
      </article>
    </main>
  </div>

  <!-- Back to Top Button -->
  <button id="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="بازگشت به ابتدای صفحه" aria-label="بازگشت به بالا">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="18 15 12 9 6 15"></polyline></svg>
  </button>

  <!-- Live Search Modal (Ctrl+K) -->
  <div class="search-modal-backdrop" id="search-modal-backdrop" onclick="closeSearchModalOnBackdrop(event)">
    <div class="search-modal" role="dialog" aria-modal="true" aria-label="جستجو در جزوه">
      <div class="search-input-wrapper">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--brand-indigo);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="modal-search-input" class="search-input-field" placeholder="جستجو در عناوین، تعاریف، قضایا و فرمول‌ها..." oninput="handleModalSearch(this.value)" autocomplete="off" />
        <button class="btn-icon" style="padding: 0.2rem 0.5rem; font-size: 0.75rem;" onclick="closeSearchModal()">ESC</button>
      </div>
      <div class="search-results-list" id="search-results-list">
        <div class="search-empty">عبارت مورد نظر خود را تایپ کنید (مثلاً: زیرفضا، دترمینان، تبدیل خطی، رتبه...)</div>
      </div>
    </div>
  </div>

  <!-- Client-side Interactive Scripts -->
  <script>
    // Search Index Data
    const searchData = {search_index_json};

    // 1. Reading Progress Bar & Back to top
    window.addEventListener('scroll', () => {{
      const winScroll = document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = (winScroll / height) * 100;
      document.getElementById('progress-bar').style.width = scrolled + '%';

      const btt = document.getElementById('back-to-top');
      if (winScroll > 400) {{
        btt.classList.add('visible');
      }} else {{
        btt.classList.remove('visible');
      }}
    }}, {{ passive: true }});

    // 2. Modern Theme Toggle (Light / Dark)
    function updateThemeUI() {{
      const meta = document.querySelector('meta[name="color-scheme"]');
      const isDark = meta.content === 'dark' || (meta.content === 'light dark' && window.matchMedia('(prefers-color-scheme: dark)').matches);
      document.getElementById('theme-icon-sun').style.display = isDark ? 'inline' : 'none';
      document.getElementById('theme-icon-moon').style.display = isDark ? 'none' : 'inline';
    }}

    function toggleTheme() {{
      const meta = document.querySelector('meta[name="color-scheme"]');
      const current = meta.content;
      const isSystemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      
      let next;
      if (current === 'light dark') {{
        next = isSystemDark ? 'light' : 'dark';
      }} else if (current === 'dark') {{
        next = 'light';
      }} else {{
        next = 'dark';
      }}

      meta.content = next;
      try {{
        localStorage.setItem('color-scheme', next);
      }} catch(e) {{}}
      updateThemeUI();
    }}
    updateThemeUI();

    // 3. Font Size Controls
    let currentScale = 16;
    try {{
      const saved = localStorage.getItem('site-font-size');
      if (saved) {{
        currentScale = parseInt(saved, 10);
        document.documentElement.style.setProperty('--font-scale', currentScale + 'px');
      }}
    }} catch(e) {{}}

    function adjustFontSize(delta) {{
      currentScale = Math.max(13, Math.min(22, currentScale + delta));
      document.documentElement.style.setProperty('--font-scale', currentScale + 'px');
      try {{ localStorage.setItem('site-font-size', currentScale); }} catch(e) {{}}
    }}

    function resetFontSize() {{
      currentScale = 16;
      document.documentElement.style.setProperty('--font-scale', '16px');
      try {{ localStorage.removeItem('site-font-size'); }} catch(e) {{}}
    }}

    // 4. Mobile Drawer Toggle
    function toggleSidebar() {{
      const sidebar = document.getElementById('sidebar');
      const backdrop = document.getElementById('sidebar-backdrop');
      sidebar.classList.toggle('open');
      backdrop.classList.toggle('open');
    }}

    // 5. Copy Formula LaTeX
    function copyFormula(button) {{
      const latex = button.getAttribute('data-latex');
      if (!latex) return;
      navigator.clipboard.writeText(latex).then(() => {{
        const span = button.querySelector('span');
        const orig = span.textContent;
        span.textContent = 'کپی شد! ✓';
        button.style.background = 'var(--example-border)';
        button.style.color = '#fff';
        setTimeout(() => {{
          span.textContent = orig;
          button.style.background = '';
          button.style.color = '';
        }}, 2000);
      }}).catch(err => {{
        console.error('Copy failed:', err);
      }});
    }}

    // 6. Search Modal Logic
    function openSearchModal() {{
      document.getElementById('search-modal-backdrop').classList.add('open');
      const input = document.getElementById('modal-search-input');
      input.value = '';
      input.focus();
      handleModalSearch('');
    }}

    function closeSearchModal() {{
      document.getElementById('search-modal-backdrop').classList.remove('open');
    }}

    function closeSearchModalOnBackdrop(e) {{
      if (e.target.id === 'search-modal-backdrop') {{
        closeSearchModal();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        openSearchModal();
      }} else if (e.key === 'Escape') {{
        closeSearchModal();
      }}
    }});

    function handleModalSearch(query) {{
      const q = query.trim().toLowerCase();
      const list = document.getElementById('search-results-list');
      if (!q) {{
        list.innerHTML = '<div class="search-empty">عبارت مورد نظر خود را تایپ کنید (مثلاً: زیرفضا، دترمینان، تبدیل خطی، رتبه...)</div>';
        return;
      }}

      const matches = searchData.filter(item => item.title.toLowerCase().includes(q)).slice(0, 30);
      if (matches.length === 0) {{
        list.innerHTML = '<div class="search-empty">موردی یافت نشد. لطفاً با کلمات دیگری جستجو کنید.</div>';
        return;
      }}

      let html = '';
      matches.forEach(item => {{
        let pillText = item.level.toUpperCase();
        if (item.level === 'h1' || item.level === 'h2') pillText = 'فصل / بخش';
        else if (item.level === 'h3') pillText = 'صفحه / موضوع';
        else if (item.level === 'callout') pillText = item.type || 'نکته / قضیه';

        html += `<a href="#${{item.id}}" class="search-result-item" onclick="navigateToItem('${{item.id}}')">
          <span class="search-result-title">${{item.title}}</span>
          <span class="search-result-pill">${{pillText}}</span>
        </a>`;
      }});
      list.innerHTML = html;
    }}

    function navigateToItem(id) {{
      closeSearchModal();
      setTimeout(() => {{
        const target = document.getElementById(id);
        if (target) {{
          target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
          target.classList.add('search-highlighted');
          setTimeout(() => target.classList.remove('search-highlighted'), 3000);
        }}
      }}, 100);
    }}

    // 7. Filter TOC items inside sidebar
    function filterTocItems(val) {{
      const term = val.trim().toLowerCase();
      const links = document.querySelectorAll('.toc-accordion .toc-link');
      const accordions = document.querySelectorAll('.toc-accordion');

      if (!term) {{
        links.forEach(l => l.style.display = '');
        return;
      }}

      accordions.forEach(acc => {{
        let hasVisible = false;
        const accLinks = acc.querySelectorAll('.toc-link');
        accLinks.forEach(l => {{
          const text = l.textContent.toLowerCase();
          if (text.includes(term)) {{
            l.style.display = '';
            hasVisible = true;
          }} else {{
            l.style.display = 'none';
          }}
        }});
        if (hasVisible) {{
          acc.open = true;
        }}
      }});
    }}

    // 8. Active Scrollspy for Table of Contents
    const headingsObserved = document.querySelectorAll('article h2[id], article h3[id]');
    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          const id = entry.target.id;
          document.querySelectorAll('.toc-link').forEach(link => {{
            if (link.getAttribute('data-id') === id) {{
              link.classList.add('active');
              const parentAcc = link.closest('.toc-accordion');
              if (parentAcc && !parentAcc.open) parentAcc.open = true;
            }} else {{
              link.classList.remove('active');
            }}
          }});
        }}
      }});
    }}, {{ rootMargin: '0px 0px -75% 0px' }});

    headingsObserved.forEach(h => observer.observe(h));
  </script>
</body>
</html>
'''

    print("8. Writing updated files...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    with open("linear_algebra_notes.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"COMPLETE! index.html ({len(full_html)} bytes) & linear_algebra_notes.html written.")

if __name__ == "__main__":
    build()
