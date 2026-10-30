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

def normalize_markdown_bold(text):
    def fix_line(line):
        cnt = line.count('**')
        if cnt < 2 or cnt % 2 != 0:
            return line
        parts = line.split('**')
        new_parts = [parts[0]]
        for i in range(1, len(parts), 2):
            in_content = parts[i]
            out_content = parts[i+1]
            l_ws = in_content[:len(in_content) - len(in_content.lstrip(' \t\u00A0'))]
            r_ws = in_content[len(in_content.rstrip(' \t\u00A0')):]
            core = in_content.strip(' \t\u00A0')
            if l_ws and not new_parts[-1].endswith((' ', '\t', '\n')):
                new_parts[-1] += l_ws
            new_parts.append(core)
            next_out = out_content
            if r_ws and not next_out.startswith((' ', '\t', '\n')):
                next_out = r_ws + next_out
            new_parts.append(next_out)
        return '**'.join(new_parts)
    return '\n'.join(fix_line(l) for l in text.splitlines())

def build():
    print("1. Reading and normalizing linear_algebra_notes_compiled.md...")
    with open("linear_algebra_notes_compiled.md", "r", encoding="utf-8") as f:
        md_text = f.read()

    md_text = normalize_markdown_bold(md_text)

    print("   Running pandoc on normalized markdown...")
    cmd = [
        "/opt/homebrew/bin/pandoc",
        "-f", "markdown+tex_math_dollars+pipe_tables",
        "-t", "html5",
        "--mathjax"
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    raw_html, _ = proc.communicate(md_text)
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

    WIKIPEDIA_TOPICS = [
        {
            "id": "wiki-vector-spaces",
            "subject_fa": "فضاهای برداری و مقدمه",
            "subject_en": "Vector Spaces & Introduction",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("بخش اول" in fa or "فضاهای برداری" in fa),
            "refs": [
                {"lang": "en", "title": "Vector space", "url": "https://en.wikipedia.org/wiki/Vector_space"},
                {"lang": "fa", "title": "فضای برداری", "url": "https://fa.wikipedia.org/wiki/%D9%81%D8%B6%D8%A7%DB%8C_%D8%A8%D8%B1%D8%AF%D8%A7%D8%B1%DB%8C"},
                {"lang": "en", "title": "Linear algebra", "url": "https://en.wikipedia.org/wiki/Linear_algebra"}
            ]
        },
        {
            "id": "wiki-fields",
            "subject_fa": "میدان و زیرمیدان",
            "subject_en": "Fields & Subfields",
            "matches": lambda tag, fa, en, hid: "تعریف میدان" in fa or "Field" in en,
            "refs": [
                {"lang": "en", "title": "Field (mathematics)", "url": "https://en.wikipedia.org/wiki/Field_(mathematics)"},
                {"lang": "fa", "title": "میدان (ریاضیات)", "url": "https://fa.wikipedia.org/wiki/%D9%85%DB%8C%D8%AF%D8%A7%D9%86_(%D8%B1%DB%8C%D8%A7%D8%B6%DB%8C%D8%A7%D8%AA)"}
            ]
        },
        {
            "id": "wiki-matrices",
            "subject_fa": "ماتریس‌ها و عملیات ماتریسی",
            "subject_en": "Matrix & Matrix Operations",
            "matches": lambda tag, fa, en, hid: "تعریف ماتریس" in fa or "Matrix Operations" in en,
            "refs": [
                {"lang": "en", "title": "Matrix (mathematics)", "url": "https://en.wikipedia.org/wiki/Matrix_(mathematics)"},
                {"lang": "fa", "title": "ماتریس", "url": "https://fa.wikipedia.org/wiki/%D9%85%D8%A7%D8%AA%D8%B1%DB%8C%D8%B3"},
                {"lang": "en", "title": "Matrix multiplication", "url": "https://en.wikipedia.org/wiki/Matrix_multiplication"}
            ]
        },
        {
            "id": "wiki-function-spaces",
            "subject_fa": "فضای توابع و چندجمله‌ای‌ها",
            "subject_en": "Function & Polynomial Spaces",
            "matches": lambda tag, fa, en, hid: "فضای توابع" in fa or "Function Spaces" in en,
            "refs": [
                {"lang": "en", "title": "Function space", "url": "https://en.wikipedia.org/wiki/Function_space"},
                {"lang": "en", "title": "Polynomial ring", "url": "https://en.wikipedia.org/wiki/Polynomial_ring"}
            ]
        },
        {
            "id": "wiki-subspaces",
            "subject_fa": "زیرفضاها و پوشش خطی (اسپن)",
            "subject_en": "Subspaces & Linear Span",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("بخش دوم" in fa or "زیرفضاها" in fa),
            "refs": [
                {"lang": "en", "title": "Linear subspace", "url": "https://en.wikipedia.org/wiki/Linear_subspace"},
                {"lang": "fa", "title": "زیرفضای خطی", "url": "https://fa.wikipedia.org/wiki/%D8%B2%DB%8C%D8%B1%D9%81%D8%B6%D8%A7%DB%8C_%D8%AE%D8%B7%DB%8C"},
                {"lang": "en", "title": "Linear span", "url": "https://en.wikipedia.org/wiki/Linear_span"},
                {"lang": "fa", "title": "پوشش خطی", "url": "https://fa.wikipedia.org/wiki/%D9%BE%D9%88%D8%B4%D8%B4_%D8%AE%D8%B7%DB%8C"}
            ]
        },
        {
            "id": "wiki-linear-independence",
            "subject_fa": "استقلال و وابستگی خطی",
            "subject_en": "Linear Independence & Dependence",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("بخش سوم" in fa or "استقلال خطی" in fa),
            "refs": [
                {"lang": "en", "title": "Linear independence", "url": "https://en.wikipedia.org/wiki/Linear_independence"},
                {"lang": "fa", "title": "استقلال خطی", "url": "https://fa.wikipedia.org/wiki/%D8%A7%D8%B3%D8%AA%D9%82%D9%84%D8%A7%D9%84_%D8%AE%D8%B7%DB%8C"}
            ]
        },
        {
            "id": "wiki-basis-coordinates",
            "subject_fa": "پایه و بردار مختصات",
            "subject_en": "Basis & Coordinates",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("بخش چهارم" in fa or "پایه و مختصات" in fa),
            "refs": [
                {"lang": "en", "title": "Basis (linear algebra)", "url": "https://en.wikipedia.org/wiki/Basis_(linear_algebra)"},
                {"lang": "fa", "title": "پایه (جبر خطی)", "url": "https://fa.wikipedia.org/wiki/%D9%BE%D8%A7%DB%8C%D9%87_(%D8%AC%D8%A8%D8%B1_%D8%AE%D8%B7%DB%8C)"},
                {"lang": "en", "title": "Coordinate vector", "url": "https://en.wikipedia.org/wiki/Coordinate_vector"}
            ]
        },
        {
            "id": "wiki-basis-existence",
            "subject_fa": "قضایای وجود پایه",
            "subject_en": "Basis Existence & Zorn's Lemma",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("وجود پایه" in fa),
            "refs": [
                {"lang": "en", "title": "Basis (linear algebra)", "url": "https://en.wikipedia.org/wiki/Basis_(linear_algebra)"},
                {"lang": "en", "title": "Zorn's lemma", "url": "https://en.wikipedia.org/wiki/Zorn%27s_lemma"}
            ]
        },
        {
            "id": "wiki-dimension",
            "subject_fa": "بُعد و قضیه جایگزینی استاینیتز",
            "subject_en": "Dimension & Steinitz Replacement",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("بعد و قضیه جایگزینی" in fa or "Dimension and Replacement" in en),
            "refs": [
                {"lang": "en", "title": "Dimension (vector space)", "url": "https://en.wikipedia.org/wiki/Dimension_(vector_space)"},
                {"lang": "fa", "title": "بعد (فضای برداری)", "url": "https://fa.wikipedia.org/wiki/%D8%A8%D8%B9%D8%AF_(%D9%81%D8%B6%D8%A7%DB%8C_%D8%A8%D8%B1%D8%AF%D8%A7%D8%B1%DB%8C)"},
                {"lang": "en", "title": "Steinitz exchange lemma", "url": "https://en.wikipedia.org/wiki/Steinitz_exchange_lemma"}
            ]
        },
        {
            "id": "wiki-linear-maps",
            "subject_fa": "تبدیل‌های خطی (نگاشت خطی)",
            "subject_en": "Linear Transformations & Maps",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("تبدیل‌های خطی" in fa and "جبر" not in fa and "نمایش" not in fa),
            "refs": [
                {"lang": "en", "title": "Linear map", "url": "https://en.wikipedia.org/wiki/Linear_map"},
                {"lang": "fa", "title": "تبدیل خطی", "url": "https://fa.wikipedia.org/wiki/%D8%AA%D8%A8%D8%AF%DB%8C%D9%84_%D8%AE%D8%B7%DB%8C"}
            ]
        },
        {
            "id": "wiki-invertibility-isomorphism",
            "subject_fa": "وارون‌پذیری و یکریختی (ایزومورفیسم)",
            "subject_en": "Invertibility & Isomorphism",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("وارون‌پذیری و یکریختی" in fa or "Isomorphism" in en),
            "refs": [
                {"lang": "en", "title": "Invertible matrix", "url": "https://en.wikipedia.org/wiki/Invertible_matrix"},
                {"lang": "en", "title": "Isomorphism", "url": "https://en.wikipedia.org/wiki/Isomorphism"},
                {"lang": "fa", "title": "یک‌ریختی", "url": "https://fa.wikipedia.org/wiki/%DB%8C%DA%A9%E2%80%8C%D8%B1%DB%8C%D8%AE%D8%AA%DB%8C"}
            ]
        },
        {
            "id": "wiki-kernel-image",
            "subject_fa": "هسته، تصویر و قضیه رتبه و پوچی",
            "subject_en": "Kernel, Image & Rank-Nullity",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("هسته و تصویر" in fa or "Kernel and Image" in en),
            "refs": [
                {"lang": "en", "title": "Kernel (linear algebra)", "url": "https://en.wikipedia.org/wiki/Kernel_(linear_algebra)"},
                {"lang": "fa", "title": "هسته (جبر)", "url": "https://fa.wikipedia.org/wiki/%D9%87%D8%B3%D8%AA%D9%87_(%D8%AC%D8%A8%D8%B1)"},
                {"lang": "en", "title": "Rank–nullity theorem", "url": "https://en.wikipedia.org/wiki/Rank%E2%80%93nullity_theorem"},
                {"lang": "fa", "title": "قضیه رتبه و پوچی", "url": "https://fa.wikipedia.org/wiki/%D9%82%D8%B6%DB%8C%D9%87_%D8%B1%D8%AA%D8%A8%D9%87_%D9%88_%D9%BE%D9%88%DA%86%DB%8C"}
            ]
        },
        {
            "id": "wiki-algebra-linear-maps",
            "subject_fa": "جبر تبدیل‌های خطی",
            "subject_en": "Algebra of Linear Transformations",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("جبر تبدیل‌های خطی" in fa or "Algebra of Linear" in en),
            "refs": [
                {"lang": "en", "title": "Associative algebra", "url": "https://en.wikipedia.org/wiki/Associative_algebra"},
                {"lang": "en", "title": "Endomorphism", "url": "https://en.wikipedia.org/wiki/Endomorphism"}
            ]
        },
        {
            "id": "wiki-row-column-null-space",
            "subject_fa": "فضای سطری، ستونی و فضای پوچ",
            "subject_en": "Row, Column & Null Space",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("فضای سطری، فضای ستونی" in fa or "Row Space, Column Space" in en),
            "refs": [
                {"lang": "en", "title": "Row and column spaces", "url": "https://en.wikipedia.org/wiki/Row_and_column_spaces"},
                {"lang": "fa", "title": "فضای سطری و ستونی", "url": "https://fa.wikipedia.org/wiki/%D9%81%D8%B6%D8%A7%DB%8C_%D8%B3%D8%B7%D8%B1%DB%8C_%D9%88_%D8%B3%D8%AA%D9%88%D9%86%DB%8C"},
                {"lang": "en", "title": "Kernel (linear algebra)", "url": "https://en.wikipedia.org/wiki/Kernel_(linear_algebra)"}
            ]
        },
        {
            "id": "wiki-matrix-representation",
            "subject_fa": "نمایش ماتریسی تبدیل‌های خطی و تغییر پایه",
            "subject_en": "Matrix Representation & Change of Basis",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("نمایش ماتریسی تبدیل‌های خطی" in fa or "Matrix Representation" in en),
            "refs": [
                {"lang": "en", "title": "Transformation matrix", "url": "https://en.wikipedia.org/wiki/Transformation_matrix"},
                {"lang": "fa", "title": "ماتریس تبدیل", "url": "https://fa.wikipedia.org/wiki/%D9%85%D8%A7%D8%AA%D8%B1%DB%8C%D8%B3_%D8%AA%D8%A8%D8%AF%DB%8C%D9%84"},
                {"lang": "en", "title": "Change of basis", "url": "https://en.wikipedia.org/wiki/Change_of_basis"}
            ]
        },
        {
            "id": "wiki-row-operations-echelon",
            "subject_fa": "عملیات سطری مقدماتی، فرم پلکانی و رتبه",
            "subject_en": "Row Operations & Echelon Form",
            "matches": lambda tag, fa, en, hid: tag == "h2" and ("صفحه ۷۴" in fa),
            "refs": [
                {"lang": "en", "title": "Row echelon form", "url": "https://en.wikipedia.org/wiki/Row_echelon_form"},
                {"lang": "fa", "title": "ماتریس پلکانی", "url": "https://fa.wikipedia.org/wiki/%D9%85%D8%A7%D8%AA%D8%B1%DB%8C%D8%B3_%D9%BE%D9%84%DA%A9%D8%A7%D9%86%DB%8C"},
                {"lang": "en", "title": "Elementary matrix", "url": "https://en.wikipedia.org/wiki/Elementary_matrix"},
                {"lang": "en", "title": "Rank (linear algebra)", "url": "https://en.wikipedia.org/wiki/Rank_(linear_algebra)"}
            ]
        },
        {
            "id": "wiki-linear-systems",
            "subject_fa": "دستگاه‌های معادلات خطی و حذف گاوسی",
            "subject_en": "Systems of Linear Equations",
            "matches": lambda tag, fa, en, hid: "دستگاه‌های معادلات خطی" in fa or "Systems of Linear Equations" in en,
            "refs": [
                {"lang": "en", "title": "System of linear equations", "url": "https://en.wikipedia.org/wiki/System_of_linear_equations"},
                {"lang": "fa", "title": "دستگاه معادلات خطی", "url": "https://fa.wikipedia.org/wiki/%D8%AF%D8%B3%D8%AA%DA%AF%D8%A7%D9%87_%D9%85%D8%B9%D8%A7%D8%AF%D9%84%D8%A7%D8%AA_%D8%AE%D8%B7%DB%8C"},
                {"lang": "en", "title": "Gaussian elimination", "url": "https://en.wikipedia.org/wiki/Gaussian_elimination"},
                {"lang": "fa", "title": "حذف گاوسی", "url": "https://fa.wikipedia.org/wiki/%D8%AD%D8%B0%D9%81_%DA%AF%D8%A7%D9%88%D8%B3%DB%8C"}
            ]
        },
        {
            "id": "wiki-matrix-inversion",
            "subject_fa": "روش محاسبه وارون ماتریس (گاوس-جردن)",
            "subject_en": "Matrix Inversion & Gauss-Jordan",
            "matches": lambda tag, fa, en, hid: "روش محاسبه وارون یک ماتریس" in fa or "Inverse of an Invertible Matrix" in en,
            "refs": [
                {"lang": "en", "title": "Invertible matrix", "url": "https://en.wikipedia.org/wiki/Invertible_matrix"},
                {"lang": "fa", "title": "ماتریس وارون‌پذیر", "url": "https://fa.wikipedia.org/wiki/%D9%85%D8%A7%D8%AA%D8%B1%DB%8C%D8%B3_%D9%88%D8%A7%D8%B1%D9%88%D9%86%E2%80%8C%D9%BE%D8%B0%DB%8C%D8%B1"},
                {"lang": "en", "title": "Gauss–Jordan elimination", "url": "https://en.wikipedia.org/wiki/Gaussian_elimination#Finding_the_inverse_of_a_matrix"}
            ]
        },
        {
            "id": "wiki-determinants",
            "subject_fa": "دترمینان، فرمول لایبنیتس و قاعده کرامر",
            "subject_en": "Determinant & Cramer's Rule",
            "matches": lambda tag, fa, en, hid: "(۱۸) دترمینان" in fa or ("دترمینان" in fa and "Determinant" in en),
            "refs": [
                {"lang": "en", "title": "Determinant", "url": "https://en.wikipedia.org/wiki/Determinant"},
                {"lang": "fa", "title": "دترمینان", "url": "https://fa.wikipedia.org/wiki/%D8%AF%D8%AA%D8%B1%D9%85%DB%8C%D9%86%D8%A7%D9%86"},
                {"lang": "en", "title": "Leibniz formula for determinants", "url": "https://en.wikipedia.org/wiki/Leibniz_formula_for_determinants"},
                {"lang": "en", "title": "Laplace expansion", "url": "https://en.wikipedia.org/wiki/Laplace_expansion"},
                {"lang": "en", "title": "Cramer's rule", "url": "https://en.wikipedia.org/wiki/Cramer%27s_rule"},
                {"lang": "fa", "title": "قاعده کرامر", "url": "https://fa.wikipedia.org/wiki/%D9%82%D8%A7%D8%B9%D8%AF%D9%87_%DA%A9%D8%B1%D8%A7%D9%85%D8%B1"}
            ]
        }
    ]

    seen_wiki_topics = set()

    def render_wiki_card(topic):
        chips = []
        for ref in topic["refs"]:
            lang = ref["lang"].upper()
            title = html.escape(ref["title"])
            url = ref["url"]
            dir_attr = 'dir="ltr"' if ref["lang"] == "en" else ''
            chip_cls = "en" if ref["lang"] == "en" else "fa"
            lang_label = "ویکی‌پدیای انگلیسی" if ref["lang"] == "en" else "ویکی‌پدیای فارسی"
            aria_label = f'{title} در {lang_label} (باز شدن در برگه جدید)'
            chips.append(f'''<a href="{url}" target="_blank" rel="noopener noreferrer" class="wiki-chip {chip_cls}" aria-label="{aria_label}" title="{aria_label}">
  <span class="wiki-lang">{lang}</span>
  <span class="wiki-chip-title" {dir_attr}>{title}</span>
  <svg class="external-icon" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
</a>''')
        chips_html = "\n    ".join(chips)
        return f'''<div class="subject-wiki-card">
  <div class="wiki-tag">
    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12.09 13.12L9.44 4H7.07L2 20h2.46l1.32-4.24h4.48l1.31 4.24h2.44L12.09 13.12zm-3.03-.92l1.63-5.26 1.63 5.26H9.06zM22 20l-4.57-16h-2.35l-3.32 10.9L10 9.25l1.62-5.25H9.28L6.8 12.38 8.65 18h2.38l2.67-8.82L16.38 18H18.8l3.2-10.45L22 20z"/></svg>
    <span>مراجع دانشنامه‌ای ویکی‌پدیا:</span>
  </div>
  <div class="wiki-chips">
    {chips_html}
  </div>
</div>'''

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
        
        # Check for matching Wikipedia subject
        matched_wiki_html = ""
        for t in WIKIPEDIA_TOPICS:
            if t["id"] not in seen_wiki_topics and t["matches"](tag, fa_title, en_title, hid):
                seen_wiki_topics.add(t["id"])
                matched_wiki_html = "\n" + render_wiki_card(t)
                break
        
        # Render clean heading HTML with isolated parts
        page_badge = f'<span class="page-tag">{page_tag}</span>' if page_tag and tag in ['h2', 'h3'] else ''
        en_badge = f'&lrm;<span class="heading-en" dir="ltr">({en_title})</span>&rlm;' if en_title else ''
        anchor = f'<a class="header-anchor" href="#{hid}" aria-label="پیوند مستقیم">#</a>'
        
        return f'''<{tag} id="{hid}" class="heading-linked">
  <span class="heading-fa">{fa_title}</span>
  {en_badge}
  {page_badge}
  {anchor}
</{tag}>{matched_wiki_html}'''

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

    # Render Wikipedia References Group in Sidebar
    wiki_sidebar_parts = ['''<details class="toc-group" id="group-wiki">
  <summary class="toc-group-header">
    <span class="toc-group-num">W</span>
    <div class="toc-group-meta">
      <span class="toc-group-title">مراجع دانشنامه‌ای ویکی‌پدیا</span>
      <span class="toc-group-pages">۱۹ مبحث درسی</span>
    </div>
    <span class="toc-arrow">›</span>
  </summary>
  <div class="toc-group-body wiki-sidebar-list">''']

    for t in WIKIPEDIA_TOPICS:
        en_links = [r for r in t['refs'] if r['lang'] == 'en']
        fa_links = [r for r in t['refs'] if r['lang'] == 'fa']
        
        links_html = []
        if en_links:
            links_html.append(f'<a href="{en_links[0]["url"]}" target="_blank" rel="noopener noreferrer" class="wiki-sidebar-link en-link" title="{en_links[0]["title"]} (EN)">EN ↗</a>')
        if fa_links:
            links_html.append(f'<a href="{fa_links[0]["url"]}" target="_blank" rel="noopener noreferrer" class="wiki-sidebar-link fa-link" title="{fa_links[0]["title"]} (FA)">FA ↗</a>')
        
        joined_links = ' '.join(links_html)
        wiki_sidebar_parts.append(f'''    <div class="wiki-sidebar-item">
      <div class="wiki-sidebar-header">
        <span class="wiki-sidebar-title">{html.escape(t['subject_fa'])}</span>
        <div class="wiki-sidebar-links">{joined_links}</div>
      </div>
    </div>''')
    wiki_sidebar_parts.append('  </div>\n</details>')
    wiki_sidebar_html = "\n".join(wiki_sidebar_parts)

    toc_html_rendered = "\n".join(toc_parts) + "\n" + wiki_sidebar_html

    # Also add Wikipedia topics to search index
    for t in WIKIPEDIA_TOPICS:
        for ref in t['refs']:
            lang_code = ref['lang'].upper()
            search_index.append({
                'id': t['id'],
                'title': f'{ref["title"]} — {t["subject_fa"]}',
                'level': 'wiki',
                'url': ref['url'],
                'lang': lang_code
            })

    search_index_json = json.dumps(search_index, ensure_ascii=False)

    print("7. Assembling Vercel Geist HTML document...")
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

  <!-- Typography: Geist & Geist Mono (Vercel), Vazirmatn -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@100..900&family=Geist+Mono:wght@100..900&display=swap" rel="stylesheet" />
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
        matchFontHeight: true,
        mtextInheritFont: true
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
       Vercel Geist Design System Theme
       Precision Monochromatic Aesthetic & Modern Typography
       ---------------------------------------------------- */
    :root {{
      color-scheme: dark light;

      /* Geist Dark (Default) Palette */
      --bg-base: #000000;
      --bg-surface: #0a0a0a;
      --bg-surface-elevated: #111111;
      --bg-hover: #171717;
      --bg-active: #222222;

      /* Precision Hairline Borders */
      --border-subtle: #222222;
      --border-base: #333333;
      --border-strong: #444444;

      /* High-contrast Typography */
      --text-main: #ededed;
      --text-secondary: #a1a1a1;
      --text-muted: #707070;
      --text-faint: #444444;

      /* Vercel Geist Accents */
      --accent-primary: #ededed;
      --accent-primary-invert: #000000;
      --accent-blue: #0070f3;
      --accent-blue-hover: #0060df;
      --accent-blue-dim: rgba(0, 112, 243, 0.12);

      --accent-cyan: #00dfd8;
      --accent-cyan-dim: rgba(0, 223, 216, 0.12);

      --accent-purple: #7928ca;
      --accent-purple-dim: rgba(121, 40, 202, 0.12);

      --accent-amber: #f5a623;
      --accent-amber-dim: rgba(245, 166, 35, 0.12);

      --accent-green: #50e3c2;
      --accent-green-dim: rgba(80, 227, 194, 0.12);

      --accent-red: #ee0000;
      --accent-red-dim: rgba(238, 0, 0, 0.12);

      /* Typography tokens */
      --font-sans: 'Geist', 'Vazirmatn', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

      /* Layout & scale */
      --header-h: 52px;
      --sidebar-w: 290px;
      --content-max-w: 840px;
      --font-scale: 15.5px;
      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 8px;
      --radius-xl: 12px;
    }}

    /* Geist Light Mode Fallback */
    :root:has(> head > meta[name="color-scheme"][content="light"]) {{
      --bg-base: #ffffff;
      --bg-surface: #fafafa;
      --bg-surface-elevated: #f5f5f5;
      --bg-hover: #ebebeb;
      --bg-active: #dfdfdf;

      --border-subtle: #eaeaea;
      --border-base: #dcdcdc;
      --border-strong: #aaaaaa;

      --text-main: #000000;
      --text-secondary: #666666;
      --text-muted: #888888;
      --text-faint: #bbbbbb;

      --accent-primary: #000000;
      --accent-primary-invert: #ffffff;
      --accent-blue: #0070f3;
      --accent-blue-hover: #0051b3;
      --accent-blue-dim: rgba(0, 112, 243, 0.08);

      --accent-cyan: #009990;
      --accent-cyan-dim: rgba(0, 153, 144, 0.08);

      --accent-purple: #7928ca;
      --accent-purple-dim: rgba(121, 40, 202, 0.08);

      --accent-amber: #d97706;
      --accent-amber-dim: rgba(217, 119, 6, 0.08);

      --accent-green: #059669;
      --accent-green-dim: rgba(5, 150, 105, 0.08);

      --accent-red: #dc2626;
      --accent-red-dim: rgba(220, 38, 38, 0.08);
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
      overflow-x: hidden;
    }}
    @supports (overflow: clip) {{
      html {{
        overflow-x: clip;
      }}
    }}

    body {{
      direction: rtl;
      text-align: right;
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      background-image: radial-gradient(rgba(255, 255, 255, 0.07) 1px, transparent 1px);
      background-size: 24px 24px;
      color: var(--text-main);
      line-height: 1.9;
      font-size: 1rem;
      min-height: 100vh;
      min-height: 100dvh;
      width: 100%;
      max-width: 100%;
      overflow-x: hidden;
    }}
    @supports (overflow: clip) {{
      body {{
        overflow-x: clip;
      }}
    }}

    /* Reading Progress Line (Vibrant Orange) */
    #progress-bar {{
      position: fixed;
      top: 0;
      left: 0;
      width: 0%;
      height: 2px;
      background: var(--accent-blue);
      z-index: 1000;
      transition: width 0.08s ease-out;
    }}

    /* Minimalist Slim Header */
    .site-header {{
      position: sticky;
      top: 0;
      height: var(--header-h);
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(12px) saturate(180%);
      -webkit-backdrop-filter: blur(12px) saturate(180%);
      border-bottom: 1px solid var(--border-subtle);
      z-index: 900;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.25rem;
      max-width: 100%;
      width: 100%;
      box-sizing: border-box;
    }}

    .brand-wrap {{
      display: flex;
      align-items: center;
      gap: 0.65rem;
      text-decoration: none;
      color: var(--text-main);
    }}

    .brand-glyph {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--text-main);
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      border-radius: var(--radius-md);
      padding: 0.35rem 0.45rem;
      line-height: 1;
      transition: border-color 0.15s ease;
    }}
    .brand-wrap:hover .brand-glyph {{
      border-color: var(--border-strong);
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
      border-radius: var(--radius-md);
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
      font-family: var(--font-mono);
      font-size: 0.7rem;
      border: 1px solid var(--border-base);
      padding: 0 0.35rem;
      border-radius: var(--radius-sm);
      background: var(--bg-surface);
    }}

    .font-stepper {{
      display: flex;
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      overflow: hidden;
    }}

    .font-step-btn {{
      background: transparent;
      border: none;
      padding: 0.25rem 0.5rem;
      font-size: 0.75rem;
      color: var(--text-secondary);
      cursor: pointer;
      font-family: var(--font-mono);
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
      grid-template-columns: var(--sidebar-w) minmax(0, 1fr);
      min-height: calc(100vh - var(--header-h));
      min-height: calc(100dvh - var(--header-h));
      width: 100%;
      max-width: 100%;
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
      border-radius: var(--radius-md);
      outline: none;
      transition: border-color 0.15s;
    }}

    .sidebar-filter:focus {{
      border-color: var(--accent-blue);
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
      border-radius: var(--radius-md);
      transition: background 0.1s;
    }}

    .toc-group-header:hover {{
      background: var(--bg-hover);
    }}

    .toc-group-num {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--accent-amber);
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
      border-radius: var(--radius-sm);
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
      font-family: var(--font-sans);
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
      background: var(--accent-blue-dim);
      border-right-color: var(--accent-blue);
    }}
    .toc-link.active .toc-link-fa {{
      color: var(--accent-blue);
      font-weight: 600;
    }}

    /* Minimalist Content Area */
    .site-content {{
      padding: 2.5rem 3rem 6rem 3rem;
      max-width: var(--content-max-w);
      margin: 0 auto;
      width: 100%;
      min-width: 0;
      box-sizing: border-box;
    }}

    article {{
      width: 100%;
      max-width: 100%;
      min-width: 0;
      box-sizing: border-box;
      overflow-wrap: break-word;
    }}

    /* Minimal Academic Masthead (NO SLOP, NO GLOW) */
    .document-masthead {{
      border-bottom: 1px solid var(--border-base);
      padding-bottom: 2rem;
      margin-bottom: 2.5rem;
    }}

    .masthead-meta {{
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent-amber);
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
      font-family: var(--font-sans);
      font-size: 1.05rem;
      color: var(--accent-blue);
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
      border-radius: var(--radius-md);
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

    /* Contribution Banner */
    .contribution-banner {{
      margin-top: 1rem;
      padding: 0.85rem 1.15rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-right: 3px solid var(--accent-blue);
      border-radius: var(--radius-md);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 0.85rem 1.25rem;
      font-size: 0.8rem;
    }}

    .contribution-banner-content {{
      flex: 1 1 320px;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
    }}

    .contribution-tag {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      color: var(--accent-blue);
      font-weight: 700;
      font-size: 0.74rem;
      letter-spacing: 0.02em;
    }}

    .contribution-desc {{
      color: var(--text-secondary);
      font-size: 0.78rem;
      line-height: 1.6;
      margin: 0;
    }}

    .contribution-btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.38rem 0.85rem;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      border-radius: var(--radius-md);
      color: var(--text-main);
      text-decoration: none;
      font-size: 0.75rem;
      font-weight: 600;
      white-space: nowrap;
      transition: all 0.12s ease;
    }}

    .contribution-btn:hover {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
      background: var(--bg-hover);
    }}

    /* Typography & BiDi Protection */
    h1, h2, h3, h4, h5, h6 {{
      color: var(--text-main);
      font-weight: 700;
      line-height: 1.4;
      position: relative;
      overflow-wrap: break-word;
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
      font-family: var(--font-sans);
    }}

    .page-tag {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--accent-amber);
      background: var(--accent-amber-dim);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 0.05rem 0.45rem;
      border-radius: var(--radius-sm);
      vertical-align: middle;
      margin-right: 0.5rem;
    }}

    .header-anchor {{
      opacity: 0;
      margin-right: 0.4rem;
      color: var(--accent-blue);
      text-decoration: none;
      font-weight: 400;
      transition: opacity 0.12s;
    }}

    .heading-linked:hover .header-anchor {{
      opacity: 1;
    }}

    /* English Term (BiDi Protection - isolated) */
    .en-term {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline !important;
      color: var(--accent-blue);
      font-size: 0.9em;
      font-family: var(--font-sans);
      font-weight: 500;
      padding: 0 0.15rem;
      overflow-wrap: break-word;
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
      font-family: var(--font-mono);
      font-size: 0.85em;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-sm);
      color: var(--accent-amber);
    }}

    pre {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
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
      display: block;
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      border-collapse: collapse;
      margin: 1.75rem 0;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
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
      border-radius: var(--radius-md);
      margin: 1.5rem 0;
      padding: 0.9rem 1.2rem;
    }}

    .callout-header {{
      display: flex;
      align-items: center;
      margin-bottom: 0.4rem;
    }}

    .callout-label {{
      font-family: var(--font-mono);
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
      border-right-color: var(--accent-blue);
    }}
    .callout-def .callout-label {{
      color: var(--accent-blue);
    }}

    .callout-thm {{
      border-right-color: var(--accent-purple);
    }}
    .callout-thm .callout-label {{
      color: var(--accent-purple);
    }}

    .callout-lem {{
      border-right-color: var(--accent-amber);
    }}
    .callout-lem .callout-label {{
      color: var(--accent-amber);
    }}

    .callout-cor {{
      border-right-color: var(--accent-cyan);
    }}
    .callout-cor .callout-label {{
      color: var(--accent-cyan);
    }}

    .callout-example {{
      border-right-color: var(--border-strong);
    }}
    .callout-example .callout-label {{
      color: var(--text-secondary);
    }}

    .callout-note {{
      border-right-color: var(--accent-amber);
      background: var(--accent-amber-dim);
    }}
    .callout-note .callout-label {{
      color: var(--accent-amber);
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
      border-radius: var(--radius-md);
      display: block;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow-x: hidden;
      min-width: 0;
      transition: border-color 0.15s;
    }}

    .math-display-container:hover {{
      border-color: var(--border-base);
    }}

    .math-display-scroll {{
      display: block;
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      overflow-y: hidden;
      text-align: center;
      padding: 0.2rem 0;
      scrollbar-width: thin;
      scrollbar-color: var(--border-base) transparent;
      -webkit-overflow-scrolling: touch;
      box-sizing: border-box;
    }}

    .copy-math-btn {{
      position: absolute;
      top: 6px;
      left: 6px;
      opacity: 0;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      border-radius: var(--radius-sm);
      padding: 0.2rem 0.45rem;
      font-size: 0.7rem;
      color: var(--text-secondary);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.3rem;
      font-family: var(--font-mono);
      transition: all 0.12s ease;
      z-index: 5;
    }}

    .math-display-container:hover .copy-math-btn {{
      opacity: 1;
    }}

    .copy-math-btn:hover {{
      background: var(--accent-blue);
      color: #000;
      border-color: var(--accent-blue);
    }}

    mjx-container {{
      max-width: 100% !important;
      box-sizing: border-box !important;
    }}

    mjx-mtext {{
      font-family: 'Vazirmatn', sans-serif !important;
      direction: rtl;
      unicode-bidi: isolate;
    }}

    .math.inline, mjx-container:not([display="true"]) {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      display: inline-block;
      margin: 0 3px;
      vertical-align: middle;
      max-width: 100%;
    }}

    mjx-container[display="true"] {{
      direction: ltr !important;
      unicode-bidi: isolate !important;
      margin: 0.4em 0 !important;
      display: block !important;
      max-width: 100% !important;
      overflow-x: auto !important;
      overflow-y: hidden !important;
    }}

    math {{
      max-width: 100% !important;
    }}

    /* Back to Top Button */
    #back-to-top {{
      position: fixed;
      bottom: 2rem;
      left: 2rem;
      background: var(--bg-surface-elevated);
      color: var(--accent-blue);
      border: 1px solid var(--border-strong);
      width: 38px;
      height: 38px;
      border-radius: var(--radius-md);
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
      background: var(--accent-blue);
      color: #000;
      border-color: var(--accent-blue);
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
      border-radius: var(--radius-lg);
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
      border-radius: var(--radius-md);
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
      font-family: var(--font-mono);
      font-size: 0.7rem;
      padding: 0.1rem 0.4rem;
      border-radius: var(--radius-sm);
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      color: var(--accent-blue);
      white-space: nowrap;
    }}

    .search-empty {{
      padding: 2rem;
      text-align: center;
      color: var(--text-muted);
      font-size: 0.88rem;
    }}

    @keyframes highlightFlash {{
      0% {{ background-color: var(--accent-blue-dim); }}
      100% {{ background-color: transparent; }}
    }}
    .search-highlighted {{
      animation: highlightFlash 2s ease-out;
    }}

    /* Wikipedia Reference Cards & Chips */
    .subject-wiki-card {{
      margin: 0.75rem 0 1.5rem 0;
      padding: 0.6rem 0.9rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-right: 3px solid var(--accent-amber);
      border-radius: var(--radius-md);
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem 0.75rem;
      font-size: 0.8rem;
    }}

    .wiki-tag {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      color: var(--accent-amber);
      font-weight: 600;
      font-size: 0.76rem;
    }}

    .wiki-chips {{
      display: inline-flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.4rem;
    }}

    .wiki-chip {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.22rem 0.55rem;
      border-radius: var(--radius-sm);
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-base);
      color: var(--text-secondary);
      text-decoration: none;
      font-size: 0.76rem;
      line-height: 1.3;
      transition: all 0.12s ease;
    }}

    .wiki-chip:hover {{
      border-color: var(--accent-blue);
      color: var(--text-main);
      background: var(--bg-hover);
    }}

    .wiki-chip.en .wiki-lang {{
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--accent-blue);
      font-weight: 700;
    }}

    .wiki-chip.fa .wiki-lang {{
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--accent-amber);
      font-weight: 700;
    }}

    .external-icon {{
      color: var(--text-muted);
      opacity: 0.65;
      transition: opacity 0.12s;
    }}

    .wiki-chip:hover .external-icon {{
      opacity: 1;
      color: var(--accent-blue);
    }}

    /* Sidebar Wikipedia Index */
    .wiki-sidebar-list {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      padding: 0.4rem 0.2rem;
    }}

    .wiki-sidebar-item {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding: 0.45rem 0.6rem;
      border-radius: var(--radius-md);
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      transition: border-color 0.12s;
    }}

    .wiki-sidebar-item:hover {{
      border-color: var(--border-base);
      background: var(--bg-hover);
    }}

    .wiki-sidebar-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }}

    .wiki-sidebar-title {{
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-main);
      text-decoration: none;
    }}

    .wiki-sidebar-title:hover {{
      color: var(--accent-blue);
    }}

    .wiki-sidebar-links {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .wiki-sidebar-link {{
      font-size: 0.68rem;
      color: var(--accent-blue);
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.2rem;
      font-family: var(--font-mono);
      border: 1px solid var(--border-subtle);
      padding: 0.1rem 0.35rem;
      border-radius: var(--radius-sm);
      background: var(--bg-surface-elevated);
    }}

    .wiki-sidebar-link.fa-link {{
      color: var(--accent-amber);
    }}

    .wiki-sidebar-link:hover {{
      border-color: var(--accent-blue);
      color: #fff;
    }}

    .search-result-pill.wiki-pill {{
      color: var(--accent-amber);
      border-color: rgba(245, 158, 11, 0.4);
    }}

    /* Mobile Drawer & Responsive Layout */
    @media (max-width: 900px) {{
      .site-layout {{
        display: block;
        width: 100%;
        max-width: 100%;
      }}

      .site-sidebar {{
        position: fixed;
        right: 0;
        top: var(--header-h);
        bottom: 0;
        width: 82%;
        max-width: 300px;
        z-index: 950;
        display: none;
        border-left: 1px solid var(--border-base);
        overscroll-behavior: contain;
      }}

      .site-sidebar.open {{
        display: flex;
        animation: slideInSidebar 0.22s cubic-bezier(0.16, 1, 0.3, 1) forwards;
      }}

      @keyframes slideInSidebar {{
        from {{
          transform: translateX(100%);
        }}
        to {{
          transform: translateX(0);
        }}
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
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        padding: 0;
      }}

      .site-content {{
        padding: 1.25rem 1rem 4rem 1rem;
        max-width: 100%;
        width: 100%;
        min-width: 0;
        box-sizing: border-box;
        overflow-x: clip;
      }}

      .masthead-title {{
        font-size: 1.5rem;
      }}
    }}

    @media (max-width: 768px) {{
      .site-header {{
        padding: 0 0.75rem;
      }}

      .brand-name {{
        font-size: 0.85rem;
        max-width: 160px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }}

      /* Prevent header buttons from overflowing on mobile */
      .search-kbd,
      .search-btn span,
      .font-stepper,
      .header-btn[onclick="window.print()"] {{
        display: none !important;
      }}

      .search-btn {{
        padding: 0;
        width: 34px;
        height: 34px;
        justify-content: center;
      }}

      #theme-toggle-btn {{
        padding: 0;
        width: 34px;
        height: 34px;
        justify-content: center;
      }}

      .header-controls {{
        gap: 0.35rem;
      }}

      .masthead-details-grid {{
        grid-template-columns: 1fr;
        padding: 0.85rem 1rem;
      }}

      .math-display-container {{
        padding: 0.85rem 0.5rem;
      }}

      blockquote, .callout, p, pre {{
        max-width: 100%;
        box-sizing: border-box;
        overflow-wrap: break-word;
      }}

      .search-modal-backdrop {{
        padding-top: 5vh;
      }}

      .search-modal {{
        width: 95%;
        max-height: 85vh;
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
        <span class="brand-glyph" aria-hidden="true">
          <svg width="14" height="12" viewBox="0 0 76 65" fill="currentColor"><path d="M37.5274 0L75.0548 65H0L37.5274 0Z"/></svg>
        </span>
        <span class="brand-name">مبانی ماتریس و جبر خطی</span>
      </a>
    </div>

    <div class="header-controls">
      <!-- GitHub Repo & Contributing -->
      <a href="https://github.com/farnamjhn/linear-algebra-notes" target="_blank" rel="noopener noreferrer" class="header-btn" title="مخزن گیت‌هاب و راهنمای مشارکت" aria-label="گیت‌هاب">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
      </a>

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
          <div class="masthead-detail-item">
            <span class="detail-label">مراجع دانشنامه‌ای</span>
            <span class="detail-value">ویکی‌پدیا فارسی و انگلیسی (تأییدشده)</span>
          </div>
        </div>

        <div class="contribution-banner">
          <div class="contribution-banner-content">
            <span class="contribution-tag">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
              دعوت به مشارکت و بازخوانی
            </span>
            <p class="contribution-desc">
              صفحات ۱ تا ۲۵ توسط نگارنده بازخوانی شده است، اما صفحات ۲۶ تا ۱۱۰ هنوز بازبینی نشده‌اند. همچنین برای اکثر قضایا جای خالی اثبات‌های کلاسی دکتر طوسی احساس می‌شود. شما می‌توانید با فورک کردن مخزن و ارسال Pull Request، در تکمیل و تصحیح این درس‌نامه مشارکت کنید.
            </p>
          </div>
          <a href="https://github.com/farnamjhn/linear-algebra-notes/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener noreferrer" class="contribution-btn">
            <span>راهنمای مشارکت (Fork & PR)</span>
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          </a>
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
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: var(--text-muted);"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
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
        button.style.color = 'var(--accent-blue)';
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
        if (item.level === 'wiki') {{
          const badge = item.lang || 'WIKI';
          html += `<a href="${{item.url}}" target="_blank" rel="noopener noreferrer" class="search-result-item" onclick="closeSearchModal()">
            <span style="display:inline-flex; align-items:center; gap:0.5rem; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
              <span class="wiki-chip ${{badge.toLowerCase()}}" style="padding:0.1rem 0.35rem; font-size:0.65rem; pointer-events:none;"><span class="wiki-lang">${{badge}}</span></span>
              <span>${{item.title}}</span>
            </span>
            <span class="search-result-pill wiki-pill">ویکی‌پدیا ↗</span>
          </a>`;
          return;
        }}

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

    // 9. Auto-close sidebar on mobile when navigating
    document.querySelectorAll('.toc-link').forEach(link => {{
      link.addEventListener('click', () => {{
        if (window.innerWidth <= 900) {{
          const sidebar = document.getElementById('sidebar');
          const backdrop = document.getElementById('sidebar-backdrop');
          if (sidebar && sidebar.classList.contains('open')) {{
            sidebar.classList.remove('open');
            if (backdrop) backdrop.classList.remove('open');
          }}
        }}
      }});
    }});
  </script>
</body>
</html>
'''

    print("8. Writing updated files...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    with open("linear_algebra_notes.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # Determine script location and target paths safely
    script_dir = os.path.dirname(os.path.abspath(__file__))
    is_in_subfolder = os.path.basename(script_dir) == "linear-algebra-notes"
    
    if is_in_subfolder:
        notes_dir = script_dir
        parent_dir = os.path.dirname(script_dir)
    else:
        notes_dir = os.path.join(script_dir, "linear-algebra-notes")
        parent_dir = script_dir

    # Write to notes_dir
    with open(os.path.join(notes_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(full_html)
    with open(os.path.join(notes_dir, "linear_algebra_notes.html"), "w", encoding="utf-8") as f:
        f.write(full_html)

    # Sync to parent_dir if it has linear_algebra_notes.html
    if os.path.exists(os.path.join(parent_dir, "linear_algebra_notes.html")):
        with open(os.path.join(parent_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(full_html)
        with open(os.path.join(parent_dir, "linear_algebra_notes.html"), "w", encoding="utf-8") as f:
            f.write(full_html)

    # Sync generator script safely
    this_script_path = os.path.abspath(__file__)
    other_script_path = os.path.join(parent_dir, "generate_full_site.py") if is_in_subfolder else os.path.join(notes_dir, "generate_full_site.py")
    if os.path.exists(other_script_path) and other_script_path != this_script_path:
        with open(this_script_path, "r", encoding="utf-8") as src, open(other_script_path, "w", encoding="utf-8") as dst:
            dst.write(src.read())

    print(f"SUCCESS! Wrote Vercel Geist website ({len(full_html)} bytes).")

if __name__ == "__main__":
    build()
