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

    # Remove the first H1 tag from Pandoc output so we don't have duplicate title under the masthead
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

    print("3. Styling Minimal Callout blocks (NO EMOJIS, technical borders)...")
    def callout_replacer(m):
        full = m.group(0)
        p_content = m.group(1)
        strong_text = m.group(2)
        
        c_class = ""
        c_label = ""
        if "تعریف" in strong_text:
            c_class = "callout-def"
            c_label = "تعریف"
        elif "قضیه" in strong_text:
            c_class = "callout-thm"
            c_label = "قضیه"
        elif "لم" in strong_text:
            c_class = "callout-lem"
            c_label = "لم"
        elif "نتیجه" in strong_text:
            c_class = "callout-cor"
            c_label = "نتیجه"
        elif "مثال" in strong_text:
            c_class = "callout-example"
            c_label = "مثال"
        elif "برهان" in strong_text or "اثبات" in strong_text:
            c_class = "callout-proof"
            c_label = "برهان"
        elif "نکته" in strong_text or "تذکر" in strong_text or "یادداشت" in strong_text:
            c_class = "callout-note"
            c_label = "تذکر"
        
        if c_class:
            return f'''<div class="callout {c_class}">
  <div class="callout-header"><span class="callout-label">{c_label}</span></div>
  <div class="callout-body"><p>{p_content}</p></div>
</div>'''
        return full

    body_html = re.sub(r'<p>(<strong>([^<]+)</strong>(.*?))</p>', callout_replacer, body_html, flags=re.DOTALL)

    print("4. Enhancing display math with copy buttons and scroll containers...")
    def math_display_replacer(m):
        math_content = m.group(1)
        raw_tex = html.escape(math_content.strip())
        return f'''<div class="math-display-container">
  <div class="math-display-scroll"><span class="math display">\\[{math_content}\\]</span></div>
  <button class="copy-math-btn" data-latex="{raw_tex}" onclick="copyFormula(this)" title="کپی فرمول LaTeX">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
    <span>LaTeX</span>
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
        anchor = f'<a class="header-anchor" href="#{hid}" aria-label="پیوند مستقیم">#</a>'
        
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

    print("6. Building clean minimal Table of Contents...")
    groups = [
        {
            "id": "group-1",
            "num": "۰۱",
            "title": "فضاهای برداری و پایه",
            "pages": "ص ۱ تا ۲۵",
            "items": []
        },
        {
            "id": "group-2",
            "num": "۰۲",
            "title": "تبدیل‌های خطی و ماتریس‌ها",
            "pages": "ص ۲۶ تا ۴۹",
            "items": []
        },
        {
            "id": "group-3",
            "num": "۰۳",
            "title": "دستگاه‌ها، وارون و دترمینان",
            "pages": "ص ۷۴ تا ۱۱۰",
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

    # Render Minimal TOC HTML
    toc_parts = []
    for g_idx, g in enumerate(groups):
        open_attr = "open" if g_idx == 0 else ""
        toc_parts.append(f'''<details class="toc-group" {open_attr} id="{g['id']}">
  <summary class="toc-group-header">
    <span class="toc-group-num">{g['num']}</span>
    <div class="toc-group-meta">
      <span class="toc-group-title">{html.escape(g['title'])}</span>
      <span class="toc-group-pages">{html.escape(g['pages'])}</span>
    </div>
    <span class="toc-arrow">›</span>
  </summary>
  <div class="toc-group-body">''')
        
        for h2 in g['items']:
            en_h2_html = f'<div class="toc-link-en" dir="ltr">{html.escape(h2["title_en"])}</div>' if h2["title_en"] else ''
            toc_parts.append(f'''    <div class="toc-entry-h2">
      <a href="#{h2['id']}" class="toc-link toc-link-h2" data-id="{h2['id']}">
        <div class="toc-link-fa">{html.escape(h2['title_fa'])}</div>
        {en_h2_html}
      </a>''')
            if h2['children']:
                toc_parts.append('      <div class="toc-subentries">')
                for h3 in h2['children']:
                    en_h3_html = f'<div class="toc-link-en" dir="ltr">{html.escape(h3["title_en"])}</div>' if h3["title_en"] else ''
                    toc_parts.append(f'''        <a href="#{h3["id"]}" class="toc-link toc-link-h3" data-id="{h3["id"]}">
          <div class="toc-link-fa">{html.escape(h3["title_fa"])}</div>
          {en_h3_html}
        </a>''')
                toc_parts.append('      </div>')
            toc_parts.append('    </div>')
        
        toc_parts.append('  </div>\n</details>')

    toc_html_rendered = "\n".join(toc_parts)
    search_index_json = json.dumps(search_index, ensure_ascii=False)

    print("7. Assembling minimalist dark & cold HTML document...")
    full_html = f'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="color-scheme" content="dark light" />
  <meta name="description" content="درس‌نامه مبانی ماتریس و جبر خطی بر اساس کتاب کنت هافمن و ری کونزه - تدریس دکتر طوسی" />
  <title>مبانی ماتریس و جبر خطی | Matrix Foundations and Linear Algebra</title>

  <!-- Prevent FOUC for color scheme according to modern web guidance -->
  <script>
    try {{
      const storedScheme = localStorage.getItem("color-scheme");
      if (storedScheme) {{
        document.querySelector('meta[name="color-scheme"]').content = storedScheme;
      }}
    }} catch(e) {{}}
  </script>

  <!-- Typography: Vazirmatn -->
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
       Minimalist Dark & Cold Theme with Vibrant Orange & Yellow
       Refined Editorial Aesthetic (No AI slop, no emojis)
       ---------------------------------------------------- */
    :root {{
      color-scheme: dark light;

      /* Deep cold background & surfaces */
      --bg-base: #08090a;
      --bg-surface: #101215;
      --bg-surface-elevated: #16191f;
      --bg-hover: #1c2027;
      --bg-active: #242933;

      /* Crisp cold borders */
      --border-subtle: #1c2026;
      --border-base: #282d37;
      --border-strong: #383f4d;

      /* High-contrast typography */
      --text-main: #f0f2f5;
      --text-secondary: #9aa0a6;
      --text-muted: #646c77;
      --text-faint: #434a54;

      /* Vibrant secondary accents */
      --accent-orange: #ff6b00;
      --accent-orange-hover: #ff8533;
      --accent-orange-dim: rgba(255, 107, 0, 0.12);

      --accent-yellow: #f59e0b;
      --accent-yellow-dim: rgba(245, 158, 11, 0.12);

      /* Layout & scale */
      --header-h: 52px;
      --sidebar-w: 290px;
      --content-max-w: 840px;
      --font-scale: 15.5px;
    }}

    /* Light mode fallback (clean minimal monochrome paper) */
    :root:has(> head > meta[name="color-scheme"][content="light"]) {{
      --bg-base: #fbfbfb;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #f4f4f5;
      --bg-hover: #eaeaea;
      --bg-active: #dfdfdf;

      --border-subtle: #e5e7eb;
      --border-base: #d1d5db;
      --border-strong: #9ca3af;

      --text-main: #111827;
      --text-secondary: #4b5563;
      --text-muted: #6b7280;
      --text-faint: #9ca3af;

      --accent-orange: #ea580c;
      --accent-orange-hover: #c2410c;
      --accent-orange-dim: rgba(234, 88, 12, 0.08);

      --accent-yellow: #d97706;
      --accent-yellow-dim: rgba(217, 119, 6, 0.08);
    }}

    /* Global Reset */
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
      font-family: 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.9;
      font-size: 1rem;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* Reading Progress Line (Vibrant Orange) */
    #progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 2px;
      background: var(--accent-orange);
      z-index: 1000;
      transition: width 0.08s ease-out;
    }}

    /* Minimalist Slim Header */
    .site-header {{
      position: sticky;
      top: 0;
      height: var(--header-h);
      background: var(--bg-base);
      border-bottom: 1px solid var(--border-subtle);
      z-index: 900;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.25rem;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
      text-decoration: none;
      color: var(--text-main);
    }}

    .brand-glyph {{
      font-family: ui-monospace, monospace;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--accent-yellow);
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      border-radius: 4px;
      padding: 0.15rem 0.45rem;
    }}

    .brand-name {{
      font-size: 0.95rem;
      font-weight: 600;
      letter-spacing: -0.01em;
    }}

    .header-controls {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}

    .header-btn {{
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-secondary);
      border-radius: 4px;
      padding: 0.3rem 0.6rem;
      font-size: 0.8rem;
      font-family: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.12s ease;
    }}

    .header-btn:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
      border-color: var(--border-base);
    }}

    .search-btn {{
      padding: 0.3rem 0.75rem;
      border-color: var(--border-base);
      color: var(--text-muted);
    }}

    .search-kbd {{
      font-family: ui-monospace, monospace;
      font-size: 0.7rem;
      border: 1px solid var(--border-base);
      padding: 0 0.35rem;
      border-radius: 3px;
      background: var(--bg-surface);
    }}

    .font-stepper {{
      display: flex;
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      overflow: hidden;
    }}

    .font-step-btn {{
      background: transparent;
      border: none;
      padding: 0.25rem 0.5rem;
      font-size: 0.75rem;
      color: var(--text-secondary);
      cursor: pointer;
      font-family: ui-monospace, monospace;
    }}

    .font-step-btn:hover {{
      background: var(--bg-hover);
      color: var(--text-main);
    }}

    .mobile-nav-toggle {{
      display: none;
    }}

    /* Main Layout Grid */
    .site-layout {{
      display: grid;
      grid-template-columns: var(--sidebar-w) 1fr;
      min-height: calc(100vh - var(--header-h));
    }}

    /* Minimalist Flat Sidebar */
    .site-sidebar {{
      position: sticky;
      top: var(--header-h);
      height: calc(100vh - var(--header-h));
      overflow-y: auto;
      background: var(--bg-base);
      border-left: 1px solid var(--border-subtle);
      padding: 1rem 0.85rem 3rem 0.85rem;
      scrollbar-width: thin;
      scrollbar-color: var(--border-base) transparent;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }}

    .sidebar-filter-wrap {{
      margin-bottom: 0.25rem;
    }}

    .sidebar-filter {{
      width: 100%;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      font-family: inherit;
      font-size: 0.8rem;
      padding: 0.35rem 0.65rem;
      border-radius: 4px;
      outline: none;
      transition: border-color 0.15s;
    }}

    .sidebar-filter:focus {{
      border-color: var(--accent-orange);
    }}

    /* Minimalist TOC Group */
    .toc-group {{
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 0.5rem;
      margin-bottom: 0.5rem;
    }}
    .toc-group:last-child {{
      border-bottom: none;
    }}

    .toc-group-header {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.35rem 0.4rem;
      cursor: pointer;
      user-select: none;
      border-radius: 4px;
      transition: background 0.1s;
    }}

    .toc-group-header:hover {{
      background: var(--bg-hover);
    }}

    .toc-group-num {{
      font-family: ui-monospace, monospace;
      font-size: 0.7rem;
      color: var(--accent-yellow);
      font-weight: 700;
    }}

    .toc-group-meta {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}

    .toc-group-title {{
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-main);
      line-height: 1.35;
    }}

    .toc-group-pages {{
      font-size: 0.7rem;
      color: var(--text-muted);
    }}

    .toc-arrow {{
      font-size: 0.8rem;
      color: var(--text-faint);
      transition: transform 0.15s;
    }}

    .toc-group[open] .toc-arrow {{
      transform: rotate(90deg);
    }}

    .toc-group-body {{
      padding: 0.35rem 0.2rem 0.35rem 0.4rem;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }}

    .toc-entry-h2 {{
      margin-top: 0.2rem;
    }}

    .toc-link {{
      display: block;
      text-decoration: none;
      padding: 0.3rem 0.5rem;
      border-radius: 3px;
      border-right: 2px solid transparent;
      transition: all 0.1s ease;
    }}

    .toc-link-fa {{
      font-size: 0.8rem;
      color: var(--text-secondary);
      line-height: 1.35;
    }}

    .toc-link-en {{
      font-size: 0.68rem;
      color: var(--text-faint);
      direction: ltr !important;
      text-align: left;
      line-height: 1.25;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      margin-top: 0.1rem;
    }}

    .toc-subentries {{
      padding-right: 0.75rem;
      border-right: 1px solid var(--border-subtle);
      margin-right: 0.5rem;
      margin-top: 0.15rem;
    }}

    .toc-link-h3 {{
      padding: 0.25rem 0.4rem;
    }}

    .toc-link:hover {{
      background: var(--bg-hover);
    }}
    .toc-link:hover .toc-link-fa {{
      color: var(--text-main);
    }}

    .toc-link.active {{
      background: var(--accent-orange-dim);
      border-right-color: var(--accent-orange);
    }}
    .toc-link.active .toc-link-fa {{
      color: var(--accent-orange);
      font-weight: 600;
    }}

    /* Minimalist Content Area */
    .site-content {{
      padding: 2.5rem 3rem 6rem 3rem;
      max-width: var(--content-max-w);
      margin: 0 auto;
      width: 100%;
    }}

    /* Minimal Academic Masthead (NO SLOP, NO GLOW) */
    .document-masthead {{
      border-bottom: 1px solid var(--border-base);
      padding-bottom: 2rem;
      margin-bottom: 2.5rem;
    }}

    .masthead-meta {{
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      color: var(--accent-yellow);
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 0.75rem;
    }}

    .masthead-title {{
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.25;
      color: var(--text-main);
      margin-bottom: 0.4rem;
    }}

    .masthead-subtitle-en {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 1.05rem;
      color: var(--accent-orange);
      font-weight: 500;
      direction: ltr !important;
      text-align: right;
      margin-bottom: 1.5rem;
    }}

    .masthead-details-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 0.75rem 1.5rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 1rem 1.25rem;
      font-size: 0.8rem;
    }}

    .masthead-detail-item {{
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }}

    .detail-label {{
      color: var(--text-muted);
      font-size: 0.72rem;
    }}

    .detail-value {{
      color: var(--text-main);
      font-weight: 600;
    }}

    /* Typography & BiDi Protection */
    h1, h2, h3, h4, h5, h6 {{
      color: var(--text-main);
      font-weight: 700;
      line-height: 1.4;
      position: relative;
    }}

    h2 {{
      font-size: 1.4rem;
      padding-bottom: 0.45rem;
      border-bottom: 1px solid var(--border-subtle);
      margin-top: 3.5rem;
      margin-bottom: 1.25rem;
    }}

    h3 {{
      font-size: 1.15rem;
      margin-top: 2.25rem;
      margin-bottom: 0.85rem;
    }}

    p {{
      margin: 1.1rem 0;
      color: var(--text-main);
    }}

    /* Headings Subtitles (LTR isolate) */
    .heading-fa {{
      display: inline;
    }}

    .heading-en {{
      display: inline-block;
      direction: ltr !important;
      unicode-bidi: isolate !important;
      color: var(--text-muted);
      font-size: 0.82em;
      font-weight: 500;
      margin-right: 0.5rem;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    .page-tag {{
      display: inline-block;
      font-family: ui-monospace, monospace;
      font-size: 0.7rem;
      color: var(--accent-yellow);
      background: var(--accent-yellow-dim);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 0.05rem 0.45rem;
      border-radius: 3px;
      vertical-align: middle;
      margin-right: 0.5rem;
    }}

    .header-anchor {{
      opacity: 0;
      margin-right: 0.4rem;
      color: var(--accent-orange);
      text-decoration: none;
      font-weight: 400;
      transition: opacity 0.12s;
    }}

    .heading-linked:hover .header-anchor {{
      opacity: 1;
    }}

    /* English Term (BiDi Protection - NEVER WRAPS IN HALF) */
    .en-term {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block !important;
      white-space: nowrap !important;
      color: var(--accent-orange);
      font-size: 0.9em;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-weight: 500;
      padding: 0 0.15rem;
    }}

    /* Lists */
    ul, ol {{
      margin: 1.1rem 0;
      padding-right: 1.5rem;
    }}

    li {{
      margin: 0.45rem 0;
    }}

    /* Minimal Code Blocks */
    code {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.85em;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      padding: 0.1rem 0.4rem;
      border-radius: 3px;
      color: var(--accent-yellow);
    }}

    pre {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      padding: 1rem 1.25rem;
      overflow-x: auto;
      margin: 1.25rem 0;
    }}

    pre code {{
      background: transparent;
      border: none;
      padding: 0;
    }}

    /* Minimalist Tables */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.75rem 0;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      overflow: hidden;
      font-size: 0.92rem;
    }}

    th, td {{
      padding: 0.65rem 0.85rem;
      border: 1px solid var(--border-subtle);
      text-align: center;
    }}

    th {{
      background: var(--bg-surface-elevated);
      font-weight: 600;
      color: var(--text-main);
    }}

    /* Clean Blockquotes */
    blockquote {{
      background: var(--bg-surface);
      border-right: 3px solid var(--border-strong);
      border-left: none;
      border-radius: 0 4px 4px 0;
      padding: 0.9rem 1.25rem;
      margin: 1.5rem 0;
      color: var(--text-secondary);
    }}

    /* Minimal Technical Callout Boxes (NO EMOJIS) */
    .callout {{
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-right: 3px solid var(--border-strong);
      border-radius: 4px;
      margin: 1.5rem 0;
      padding: 0.9rem 1.2rem;
    }}

    .callout-header {{
      display: flex;
      align-items: center;
      margin-bottom: 0.4rem;
    }}

    .callout-label {{
      font-family: ui-monospace, monospace;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.04em;
    }}

    .callout-body p:first-child {{
      margin-top: 0;
    }}
    .callout-body p:last-child {{
      margin-bottom: 0;
    }}

    .callout-def {{
      border-right-color: var(--accent-yellow);
    }}
    .callout-def .callout-label {{
      color: var(--accent-yellow);
    }}

    .callout-thm {{
      border-right-color: var(--accent-orange);
    }}
    .callout-thm .callout-label {{
      color: var(--accent-orange);
    }}

    .callout-lem {{
      border-right-color: #d97706;
    }}
    .callout-lem .callout-label {{
      color: #fbbf24;
    }}

    .callout-cor {{
      border-right-color: #ea580c;
    }}
    .callout-cor .callout-label {{
      color: #fb923c;
    }}

    .callout-example {{
      border-right-color: var(--border-strong);
    }}
    .callout-example .callout-label {{
      color: var(--text-secondary);
    }}

    .callout-note {{
      border-right-color: var(--accent-yellow);
      background: var(--accent-yellow-dim);
    }}
    .callout-note .callout-label {{
      color: var(--accent-yellow);
    }}

    .callout-proof {{
      background: transparent;
      border: none;
      border-right: 2px solid var(--border-subtle);
      padding: 0.5rem 1rem;
      color: var(--text-secondary);
    }}
    .callout-proof .callout-label {{
      color: var(--text-muted);
    }}

    /* Math Display Containers */
    .math-display-container {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      position: relative;
      margin: 1.5rem 0;
      padding: 1.15rem 1.25rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: border-color 0.15s;
    }}

    .math-display-container:hover {{
      border-color: var(--border-base);
    }}

    .math-display-scroll {{
      width: 100%;
      overflow-x: auto;
      text-align: center;
      padding: 0.2rem 0;
      scrollbar-width: thin;
      scrollbar-color: var(--border-base) transparent;
    }}

    .copy-math-btn {{
      position: absolute;
      top: 6px;
      left: 6px;
      opacity: 0;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      border-radius: 3px;
      padding: 0.2rem 0.45rem;
      font-size: 0.7rem;
      color: var(--text-secondary);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.3rem;
      font-family: ui-monospace, monospace;
      transition: all 0.12s ease;
    }}

    .math-display-container:hover .copy-math-btn {{
      opacity: 1;
    }}

    .copy-math-btn:hover {{
      background: var(--accent-orange);
      color: #000;
      border-color: var(--accent-orange);
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
      margin: 0.4em 0 !important;
    }}

    /* Back to Top Button */
    #back-to-top {{
      position: fixed;
      bottom: 2rem;
      left: 2rem;
      background: var(--bg-surface-elevated);
      color: var(--accent-orange);
      border: 1px solid var(--border-strong);
      width: 38px;
      height: 38px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s;
      z-index: 800;
    }}

    #back-to-top.visible {{
      opacity: 1;
      pointer-events: auto;
    }}

    #back-to-top:hover {{
      background: var(--accent-orange);
      color: #000;
      border-color: var(--accent-orange);
    }}

    /* Minimal Search Modal */
    .search-modal-backdrop {{
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(3px);
      z-index: 2000;
      display: none;
      align-items: flex-start;
      justify-content: center;
      padding-top: 12vh;
    }}

    .search-modal-backdrop.open {{
      display: flex;
    }}

    .search-modal {{
      background: var(--bg-surface);
      border: 1px solid var(--border-strong);
      border-radius: 6px;
      width: 90%;
      max-width: 580px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      max-height: 70vh;
    }}

    .search-input-wrapper {{
      display: flex;
      align-items: center;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-subtle);
      gap: 0.65rem;
    }}

    .search-input-field {{
      flex: 1;
      border: none;
      background: transparent;
      font-size: 0.95rem;
      font-family: inherit;
      color: var(--text-main);
      outline: none;
    }}

    .search-results-list {{
      overflow-y: auto;
      padding: 0.4rem;
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }}

    .search-result-item {{
      padding: 0.55rem 0.85rem;
      border-radius: 4px;
      text-decoration: none;
      color: var(--text-main);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.75rem;
      font-size: 0.85rem;
      transition: background 0.1s;
    }}

    .search-result-item:hover, .search-result-item.selected {{
      background: var(--bg-hover);
    }}

    .search-result-pill {{
      font-family: ui-monospace, monospace;
      font-size: 0.7rem;
      padding: 0.1rem 0.4rem;
      border-radius: 3px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--accent-orange);
      white-space: nowrap;
    }}

    .search-empty {{
      padding: 2rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.88rem;
    }}

    @keyframes highlightFlash {{
      0% {{ background-color: var(--accent-orange-dim); }}
      100% {{ background-color: transparent; }}
    }}
    .search-highlighted {{
      animation: highlightFlash 2s ease-out;
    }}

    /* Mobile Drawer */
    @media (max-width: 900px) {{
      .site-layout {{
        grid-template-columns: 1fr;
      }}

      .site-sidebar {{
        position: fixed;
        right: 0;
        top: var(--header-h);
        bottom: 0;
        width: 82%;
        max-width: 300px;
        z-index: 950;
        transform: translateX(100%);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 1px solid var(--border-base);
      }}

      .site-sidebar.open {{
        transform: translateX(0);
      }}

      .sidebar-backdrop {{
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.6);
        z-index: 940;
        display: none;
      }}
      .sidebar-backdrop.open {{
        display: block;
      }}

      .mobile-nav-toggle {{
        display: inline-flex;
      }}

      .site-content {{
        padding: 1.5rem 1.15rem 4rem 1.15rem;
      }}

      .masthead-title {{
        font-size: 1.6rem;
      }}
    }}

    /* Print Stylesheet */
    @media print {{
      #progress-bar, .site-header, .site-sidebar, #back-to-top, .search-modal-backdrop, .copy-math-btn {{
        display: none !important;
      }}
      body {{
        background: #fff !important;
        color: #000 !important;
        font-size: 11pt !important;
        line-height: 1.5 !important;
      }}
      .site-layout {{
        display: block !important;
      }}
      .site-content {{
        max-width: 100% !important;
        padding: 0 !important;
      }}
      .callout, .math-display-container {{
        border: 1px solid #ccc !important;
        background: transparent !important;
        break-inside: avoid;
      }}
    }}
  </style>
</head>
<body>
  <div id="progress-bar"></div>

  <!-- Minimal Header -->
  <header class="site-header">
    <div style="display: flex; align-items: center; gap: 0.65rem;">
      <button class="header-btn mobile-nav-toggle" onclick="toggleSidebar()" aria-label="منو">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      </button>
      <a href="#" class="brand-wrap">
        <span class="brand-glyph">∑</span>
        <span class="brand-name">مبانی ماتریس و جبر خطی</span>
      </a>
    </div>

    <div class="header-controls">
      <!-- Search -->
      <button class="header-btn search-btn" onclick="openSearchModal()" title="جستجو (⌘K)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <span>جستجو</span>
        <kbd class="search-kbd">⌘K</kbd>
      </button>

      <!-- Font Stepper -->
      <div class="font-stepper" title="اندازه قلم">
        <button class="font-step-btn" onclick="adjustFontSize(-1)">A-</button>
        <button class="font-step-btn" onclick="resetFontSize()">A</button>
        <button class="font-step-btn" onclick="adjustFontSize(1)">A+</button>
      </div>

      <!-- Theme Toggle -->
      <button class="header-btn" id="theme-toggle-btn" onclick="toggleTheme()" title="تغییر تم">
        <svg id="theme-icon-sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        <svg id="theme-icon-moon" style="display:none;" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button>

      <!-- Print -->
      <button class="header-btn" onclick="window.print()" title="چاپ یا PDF">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>
      </button>
    </div>
  </header>

  <div class="sidebar-backdrop" id="sidebar-backdrop" onclick="toggleSidebar()"></div>

  <div class="site-layout">
    <!-- Minimal Sidebar -->
    <aside class="site-sidebar" id="sidebar">
      <div class="sidebar-filter-wrap">
        <input type="text" class="sidebar-filter" placeholder="فیلتر سرفصل‌ها..." oninput="filterTocItems(this.value)" />
      </div>

      <nav id="toc-nav">
        {toc_html_rendered}
      </nav>
    </aside>

    <!-- Main Editorial Content -->
    <main class="site-content">
      <!-- Minimal Academic Masthead -->
      <header class="document-masthead">
        <div class="masthead-meta">دانشگاه • جبر خطی و مبانی ماتریس‌ها • ترم ۴۰۴۱</div>
        <h1 class="masthead-title">مبانی ماتریس و جبر خطی</h1>
        <div class="masthead-subtitle-en" dir="ltr">Matrix Foundations & Linear Algebra</div>
        <div class="masthead-details-grid">
          <div class="masthead-detail-item">
            <span class="detail-label">مدرس</span>
            <span class="detail-value">دکتر طوسی</span>
          </div>
          <div class="masthead-detail-item">
            <span class="detail-label">مرجع درسی</span>
            <span class="detail-value">هافمن و کونزه (Kenneth Hoffman & Ray Kunze)</span>
          </div>
          <div class="masthead-detail-item">
            <span class="detail-label">محتوا</span>
            <span class="detail-value">۱۱۰ صفحه درس‌نامه • ۱۸ بخش کامل</span>
          </div>
        </div>
      </header>

      <!-- Article Body -->
      <article id="article-body">
        {body_html}
      </article>
    </main>
  </div>

  <!-- Back to top -->
  <button id="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="بازگشت به بالا" aria-label="بالا">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="18 15 12 9 6 15"></polyline></svg>
  </button>

  <!-- Search Modal -->
  <div class="search-modal-backdrop" id="search-modal-backdrop" onclick="closeSearchModalOnBackdrop(event)">
    <div class="search-modal" role="dialog" aria-modal="true" aria-label="جستجو در جزوه">
      <div class="search-input-wrapper">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--accent-orange);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="modal-search-input" class="search-input-field" placeholder="جستجو در مفاهیم، قضایا، تعاریف و صفحات..." oninput="handleModalSearch(this.value)" autocomplete="off" />
        <kbd class="search-kbd" onclick="closeSearchModal()" style="cursor: pointer;">ESC</kbd>
      </div>
      <div class="search-results-list" id="search-results-list">
        <div class="search-empty">عبارت مورد نظر خود را بنویسید (مثلاً: رتبه، زیرفضا، دترمینان، تبدیل خطی...)</div>
      </div>
    </div>
  </div>

  <script>
    const searchData = {search_index_json};

    // 1. Reading Progress
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

    // 2. Theme Toggle (Dark Default)
    function updateThemeUI() {{
      const meta = document.querySelector('meta[name="color-scheme"]');
      const isLight = meta.content === 'light';
      document.getElementById('theme-icon-sun').style.display = isLight ? 'none' : 'inline';
      document.getElementById('theme-icon-moon').style.display = isLight ? 'inline' : 'none';
    }}

    function toggleTheme() {{
      const meta = document.querySelector('meta[name="color-scheme"]');
      const next = meta.content === 'light' ? 'dark' : 'light';
      meta.content = next;
      try {{ localStorage.setItem('color-scheme', next); }} catch(e) {{}}
      updateThemeUI();
    }}
    updateThemeUI();

    // 3. Font Size Adjuster
    let currentScale = 15.5;
    try {{
      const saved = localStorage.getItem('site-font-size');
      if (saved) {{
        currentScale = parseFloat(saved);
        document.documentElement.style.setProperty('--font-scale', currentScale + 'px');
      }}
    }} catch(e) {{}}

    function adjustFontSize(delta) {{
      currentScale = Math.max(13, Math.min(20, currentScale + delta));
      document.documentElement.style.setProperty('--font-scale', currentScale + 'px');
      try {{ localStorage.setItem('site-font-size', currentScale); }} catch(e) {{}}
    }}

    function resetFontSize() {{
      currentScale = 15.5;
      document.documentElement.style.setProperty('--font-scale', '15.5px');
      try {{ localStorage.removeItem('site-font-size'); }} catch(e) {{}}
    }}

    // 4. Mobile Drawer
    function toggleSidebar() {{
      document.getElementById('sidebar').classList.toggle('open');
      document.getElementById('sidebar-backdrop').classList.toggle('open');
    }}

    // 5. Copy Formula
    function copyFormula(button) {{
      const latex = button.getAttribute('data-latex');
      if (!latex) return;
      navigator.clipboard.writeText(latex).then(() => {{
        const span = button.querySelector('span');
        const orig = span.textContent;
        span.textContent = 'کپی شد!';
        button.style.color = 'var(--accent-orange)';
        setTimeout(() => {{
          span.textContent = orig;
          button.style.color = '';
        }}, 1800);
      }});
    }}

    // 6. Search Modal
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
      if (e.target.id === 'search-modal-backdrop') closeSearchModal();
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
        list.innerHTML = '<div class="search-empty">عبارت مورد نظر خود را بنویسید (مثلاً: رتبه، زیرفضا، دترمینان، تبدیل خطی...)</div>';
        return;
      }}

      const matches = searchData.filter(item => item.title.toLowerCase().includes(q)).slice(0, 30);
      if (matches.length === 0) {{
        list.innerHTML = '<div class="search-empty">نتیجه‌ای یافت نشد.</div>';
        return;
      }}

      let html = '';
      matches.forEach(item => {{
        let pillText = 'بخش';
        if (item.level === 'h3') pillText = 'صفحه';
        else if (item.level === 'callout') pillText = item.type || 'نکته';

        html += `<a href="#${{item.id}}" class="search-result-item" onclick="navigateToItem('${{item.id}}')">
          <span>${{item.title}}</span>
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
          setTimeout(() => target.classList.remove('search-highlighted'), 2500);
        }}
      }}, 100);
    }}

    // 7. Filter TOC
    function filterTocItems(val) {{
      const term = val.trim().toLowerCase();
      const links = document.querySelectorAll('.toc-group .toc-link');
      const groups = document.querySelectorAll('.toc-group');

      if (!term) {{
        links.forEach(l => l.style.display = '');
        return;
      }}

      groups.forEach(grp => {{
        let hasMatch = false;
        const gLinks = grp.querySelectorAll('.toc-link');
        gLinks.forEach(l => {{
          if (l.textContent.toLowerCase().includes(term)) {{
            l.style.display = '';
            hasMatch = true;
          }} else {{
            l.style.display = 'none';
          }}
        }});
        if (hasMatch) grp.open = true;
      }});
    }}

    // 8. Scrollspy
    const headingsObserved = document.querySelectorAll('article h2[id], article h3[id]');
    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          const id = entry.target.id;
          document.querySelectorAll('.toc-link').forEach(link => {{
            if (link.getAttribute('data-id') === id) {{
              link.classList.add('active');
              const parentGrp = link.closest('.toc-group');
              if (parentGrp && !parentGrp.open) parentGrp.open = true;
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

    print("8. Writing updated files to both linear-algebra-notes/ and root...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    with open("linear_algebra_notes.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # Also sync to parent directory if in linear-algebra-notes
    if os.path.exists("../linear_algebra_notes.html"):
        with open("../index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        with open("../linear_algebra_notes.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        with open("../generate_full_site.py", "w", encoding="utf-8") as f:
            with open("generate_full_site.py", "r", encoding="utf-8") as g:
                f.write(g.read())

    print(f"SUCCESS! Wrote minimalist website ({len(full_html)} bytes).")

if __name__ == "__main__":
    build()
