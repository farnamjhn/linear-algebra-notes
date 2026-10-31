# ۱-۲ قضیه (خواص مقدماتی فضای برداری)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد. در این صورت داریم:

**(i) قانون حذفی جمع:** فرض کنید $u, v, w \in V$ به طوری که $u + v = u + w$. در این صورت $v = w$.

**اثبات:**
$$(-u) + (u + v) = (-u) + (u + w)$$
$$\stackrel{\text{شرکت‌پذیری}}{\Longrightarrow} (-u + u) + v = (-u + u) + w$$
$$\Longrightarrow 0_V + v = 0_V + w \Longrightarrow v = w$$

---

**(ii) الف) بردار صفر یکتا است.**

**برهان (برهان خلف):** فرض کنید دو بردار $0_1$ و $0_2$ وجود داشته باشند که (برای هر $v \in V$):
$$0_1 + v = v$$
$$0_2 + v = v$$
در نتیجه:
$$\begin{cases} \text{به ازای } v = 0_2 \implies 0_1 + 0_2 = 0_2 \\ \text{به ازای } v = 0_1 \implies 0_2 + 0_1 = 0_1 \end{cases}$$
لذا $0_1 = 0_2$.

---

**(ii) ب) بردار قرینه یکتا است.**

**برهان (برهان خلف):** فرض کنید $u \in V$ و $u_1, u_2 \in V$ به طوری که:
$$u + u_1 = 0_V \quad , \quad u + u_2 = 0_V$$
بنابراین:
$$u + u_1 = u + u_2$$
و بنابر (i) داریم: $u_1 = u_2$.

---

**(iii) برای هر $u \in V$ داریم $-(-u) = u$.**

**برهان:** داریم $u + (-u) = 0_V$ و همچنین $(-(-u)) + (-u) = 0_V$. 
یعنی $u$ قرینه‌ی $-u$ است. چون قرینه‌ی $-u$ یکتا است، پس $-(-u)$ برابر $u$ است.

---

**(iv) برای هر $u \in V$ داریم $0_F \cdot u = 0_V$.**

**برهان:** فرض کنید $u \in V$. در این صورت:
$$0_F \cdot u = (0_F + 0_F) \cdot u \stackrel{\text{خواص ضرب اسکالر}}{=} 0_F \cdot u + 0_F \cdot u$$
$$\Longrightarrow 0_V + 0_F \cdot u = 0_F \cdot u + 0_F \cdot u \stackrel{\text{طبق (i)}}{\Longrightarrow} 0_F \cdot u = 0_V$$

---

**(v) برای هر $\alpha \in F$ داریم $\alpha \cdot 0_V = 0_V$.**

**برهان:** فرض کنید $\alpha \in F$. در این صورت:
$$\alpha \cdot (0_V + 0_V) = \alpha \cdot 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} \alpha \cdot 0_V + \alpha \cdot 0_V = \alpha \cdot 0_V = \alpha \cdot 0_V + 0_V$$
مطابق (i) و خاصیت جمع برداری داریم:
$$\alpha \cdot 0_V = 0_V$$

---

**(vi) برای هر $\alpha \in F$ و هر $u \in V$ داریم $(-\alpha)u = -(\alpha u) = \alpha(-u)$. به ویژه داریم $(-1_F)u = -u$.**

**برهان:** فرض کنید $\alpha \in F$ و $u \in V$.

**الف)** 
$$(-\alpha)u + \alpha u \stackrel{\text{خاصیت ضرب اسکالر}}{=} (-\alpha + \alpha)u = 0_F \cdot u \stackrel{\text{(iv)}}{=} 0_V$$
یعنی $(-\alpha)u$ قرینه‌ی $\alpha u$ است. بنابراین $(-\alpha)u = -(\alpha u)$.

**ب)** 
$$\alpha(-u) + \alpha u = \alpha(-u + u) = \alpha \cdot 0_V \stackrel{\text{(v)}}{=} 0_V$$
یعنی $\alpha(-u)$ قرینه‌ی $\alpha u$ است. بنابراین $\alpha(-u) = -(\alpha u)$.

**ج) حالت خاص:**
$$(-1_F)u \stackrel{\text{الف}}{=} -(1_F \cdot u) \stackrel{\text{خاصیت ضرب اسکالر}}{=} -u$$

---

**(vii) فرض کنید $\alpha \in F$ و $u \in V$ به طوری که $\alpha u = 0_V$. در این صورت $\alpha = 0_F$ یا $u = 0_V$.**

**برهان:** فرض کنید $\alpha \neq 0_F$. (اگر $\alpha = 0_F$ باشد که گزاره درست می‌شود.) در این صورت $\alpha$ در $F$ دارای وارون ($\alpha^{-1}$) است. بنابراین:
$$\alpha^{-1}(\alpha u) = \alpha^{-1}(0_V) \stackrel{\text{خاصیت ضرب اسکالر و (v)}}{\Longrightarrow} (\alpha^{-1}\alpha)u = 0_V$$
$$\Longrightarrow 1_F \cdot u = 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} u = 0_V$$

---

# ۲-۲ قضیه (محک فشرده زیرفضا)

فرض کنید $W$ زیرمجموعه ناتهی از فضای برداری $V$ روی میدان $F$ باشد. در این صورت $W$ زیرفضای $V$ است اگر و تنها اگر برای هر $u, v \in W$ و هر $c \in F$ داشته باشیم:
$$cu + v \in W$$

**برهان:** 
$(\Longrightarrow)$ واضح است (از بسته بودن زیرفضا نسبت به جمع و ضرب اسکالر نتیجه می‌شود).

$(\Longleftarrow)$ 
**(اول) $W$ تحت عمل جمع برداری بسته است:**
فرض کنید $u, v \in W$. در این صورت با قرار دادن $c = 1_F$ داریم:
$$u + v = 1_F \cdot u + v \in W$$

**(دوم) $0_V \in W$:**
چون $W$ ناتهی است، پس $w_0 \in W$ وجود دارد. لذا طبق فرض (به ازای $c = -1_F$) داریم:
$$(-1_F)w_0 + w_0 \in W \stackrel{(-1_F)w_0 = -w_0}{\Longrightarrow} -w_0 + w_0 \in W \Longrightarrow 0_V \in W$$

**(سوم) برای هر $x \in W$ داریم $-x \in W$:**
فرض کنید $x \in W$. در این صورت طبق فرض و (دوم) داریم:
$$(-1_F)x + 0_V \in W \stackrel{(-1_F)x = -x}{\Longrightarrow} -x \in W$$

**(چهارم) برای هر $c \in F$ و $x \in W$ داریم $cx \in W$:**
زیرا $cx = cx + 0_V \in W$. همچنین خاصیت شرکت‌پذیری، جابجایی و چهار خاصیت ضرب اسکالر از $V$ به $W$ القا می‌شوند.

---

### مثال:
مجموعه‌ی $W = \{(x, y) \in \mathbb{R}^2 \mid x \ge 0, y \ge 0\}$ زیرفضای $\mathbb{R}^2$ نیست:
1. $(a, b), (c, d) \in W \implies (a+c, b+d) \in W$ (تحت جمع بسته است).
2. برای هر $\alpha \in \mathbb{R}$ و $(a, b) \in W$، الزاماً $(\alpha a, \alpha b) \in W$ نیست (به ازای $\alpha < 0$ برقرار نیست).

---

# ۴-۲ تعریف (درجه یک چندجمله‌ای ناصفر)

$$\deg\left(\sum_{i=0}^{\infty} a_i x^i\right) = \max\{i \mid a_i \neq 0\}$$
چون چندجمله‌ای ناصفر است، پس مجموعه $\{i \mid a_i \neq 0\}$ ناتهی و متناهی است.
درجه‌ی چندجمله‌ای صفر را $-\infty$ تعریف می‌کنیم (قرارداد: برای هر عدد طبیعی $n$ داریم $-\infty < n$).

---

# ۵-۲ قضیه

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $\{W_i\}_{i \in I}$ خانواده‌ای از زیرفضاهای $V$ باشد. در این صورت $\bigcap_{i \in I} W_i$ زیرفضای $V$ است.

**برهان:** 
توجه کنید برای هر $i \in I$ داریم $0_V \in W_i$، پس $0_V \in \bigcap_{i \in I} W_i \neq \emptyset$.
فرض کنید $u, v \in \bigcap_{i \in I} W_i$ و $c \in F$. در این صورت:
$$u, v \in W_i \quad (\forall i \in I) \stackrel{W_i \text{ زیرفضای } V}{\Longrightarrow} cu + v \in W_i \quad (\forall i \in I)$$
$$\Longrightarrow cu + v \in \bigcap_{i \in I} W_i$$
حکم از قضیه‌ی محک فشرده نتیجه می‌شود.

---

# ۶-۲ لم

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $S \subseteq V$. در این صورت:
$$\text{span}(S) = \bigcap_{\substack{W \le V \\ S \subseteq W}} W$$
*(که در آن $W \le V$ به معنای «$W$ زیرفضای $V$ است» می‌باشد).*

**برهان:** 
قرار دهید $\Sigma = \{W \le V \mid S \subseteq W\}$ (مجموعه زیرفضاهای $V$ شامل $S$). 
توجه کنید $V \in \Sigma$ پس $\Sigma \neq \emptyset$. مطابق قضیه بالا (۵-۲)، $\bigcap_{W \in \Sigma} W$ یک زیرفضای $V$ است. 
واضح است که این اشتراک شامل $S$ است و کوچک‌ترین زیرفضایی از $V$ است که شامل $S$ می‌باشد (زیرا اگر $W'$ هر زیرفضای شامل $S$ باشد، آنگاه $W' \in \Sigma$ و در نتیجه $\bigcap_{W \in \Sigma} W \subseteq W'$). پس طبق تعریف، برابر $\text{span}(S)$ است.

---

# ۷-۲ قضیه

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $\emptyset \neq S \subseteq V$. در این صورت:
$$\text{span}(S) = \left\{ \sum_{i=1}^{n} \alpha_i v_i \;\middle|\; n \in \mathbb{N}, \alpha_i \in F, v_i \in S \right\}$$
*(مجموعه همه ترکیب‌های خطی ممکن از بردارهای $S$).*

**برهان:** قرار دهید:
$$\Sigma = \left\{ \sum_{i=1}^{n} \alpha_i v_i \;\middle|\; n \in \mathbb{N}, \alpha_i \in F, v_i \in S \right\}$$

**(i) $\Sigma$ یک زیرفضای $V$ است:**
چون $S \neq \emptyset$، پس $\Sigma \neq \emptyset$. فرض کنید $\sum_{i=1}^{m} \beta_i u_i \in \Sigma$ و $\sum_{i=1}^{n} \alpha_i v_i \in \Sigma$ و $c \in F$. در این صورت:
$$c\left(\sum_{i=1}^{m} \beta_i u_i\right) + \left(\sum_{i=1}^{n} \alpha_i v_i\right) = \sum_{i=1}^{m} (c\beta_i) u_i + \sum_{i=1}^{n} \alpha_i v_i$$
این عنصر به شکل عناصر $\Sigma$ است (چرا که $u_i, v_i \in S$ و $\alpha_i, c\beta_i \in F$ و تعداد جملات $n+m \in \mathbb{N}$ است). پس $\Sigma$ زیرفضای $V$ است.

**(ii) $S \subseteq \Sigma$:**
فرض کنید $x \in S$. در این صورت $x = 1_F \cdot x \in \Sigma$.

از (i) و (ii) می‌فهمیم که $\Sigma$ زیرفضای شامل $S$ است؛ بنابراین طبق تعریفِ $\text{span}(S)$ (کوچک‌ترین زیرفضای شامل $S$) داریم:
$$\text{span}(S) \subseteq \Sigma$$

**(iii) اگر $W$ یک زیرفضای $V$ باشد که شامل $S$ است، آنگاه $\Sigma \subseteq W$:**
فرض کنید $x \in \Sigma$. در این صورت عناصر $\alpha_1, \dots, \alpha_n \in F$ و عناصر $v_1, \dots, v_n \in S$ وجود دارند که:
$$x = \sum_{i=1}^{n} \alpha_i v_i$$
چون $S \subseteq W$ پس $v_1, \dots, v_n \in W$. بنابراین با توجه به بسته بودن $W$ نسبت به ضرب اسکالر و جمع، داریم:
$$x = \sum_{i=1}^{n} \alpha_i v_i \in W$$
از آنجا که $\text{span}(S)$ خود یک زیرفضای شامل $S$ است، با قرار دادن $W = \text{span}(S)$ در (iii) داریم $\Sigma \subseteq \text{span}(S)$. 
در نتیجه $\text{span}(S) = \Sigma$.

---

# ۸-۲ لم (قضیه؟)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $X = \{x_1, x_2, \dots, x_r\}$ و $Y = \{y_1, y_2, \dots, y_s\}$ دو زیرمجموعه ناتهی از $V$ باشند. در این صورت:
* **الف)** اگر $X \subseteq \text{span}(Y)$ (یعنی هر عنصر $X$ ترکیب خطی از عناصر $Y$ باشد)، آنگاه $\text{span}(X) \subseteq \text{span}(Y)$.
* **ب)** $\text{span}(X) = \text{span}(Y)$ اگر و تنها اگر هر عنصر $X$ ترکیب خطی از عناصر $Y$ باشد و هر عضو $Y$ ترکیب خطی از عناصر $X$ باشد.

**برهان:**
* **الف)** طبق تعریف، $\text{span}(X)$ کوچک‌ترین زیرفضای $V$ شامل $X$ است. از طرف دیگر، $\text{span}(Y)$ یک زیرفضای $V$ است که طبق فرض شامل $X$ است ($X \subseteq \text{span}(Y)$). در نتیجه:
$$\text{span}(X) \subseteq \text{span}(Y)$$
* **ب)** با استفاده از قسمت (الف) به راحتی نتیجه می‌شود.

---

# ۹-۲ لم

فرض کنید $V$ فضای برداری روی میدان $F$ باشد، $S \subseteq V$ و $u \in S$. در این صورت:
$$\text{span}(S) = \text{span}(S - \{u\}) \Longleftrightarrow u \text{ ترکیب خطی از عناصر } S - \{u\} \text{ باشد } (u \in \text{span}(S - \{u\}))$$

**برهان:**
$(\Longrightarrow)$ 
چون $u \in S$ و $S \subseteq \text{span}(S)$، پس $u \in \text{span}(S)$. طبق فرض $\text{span}(S) = \text{span}(S - \{u\})$، در نتیجه $u \in \text{span}(S - \{u\})$؛ یعنی $u$ ترکیب خطی از عناصر $S - \{u\}$ است.

$(\Longleftarrow)$ 
**(اول) ثابت می‌کنیم $\text{span}(S - \{u\}) \subseteq \text{span}(S)$:**
می‌دانیم $S - \{u\} \subseteq S \subseteq \text{span}(S)$. پس $S - \{u\} \subseteq \text{span}(S)$ و در نتیجه:
$$\text{span}(S - \{u\}) \subseteq \text{span}(S)$$
*(نکته کلی: $X \subseteq Y \implies \text{span}(X) \subseteq \text{span}(Y)$).*

**(دوم) ثابت می‌کنیم $\text{span}(S) \subseteq \text{span}(S - \{u\})$:**
بدین منظور با توجه به قضیه قبل، کافی است ثابت کنیم $S \subseteq \text{span}(S - \{u\})$.
فرض کنید $x \in S$. دو حالت داریم:
1. $x \neq u$: در نتیجه $x \in S - \{u\} \subseteq \text{span}(S - \{u\})$.
2. $x = u$: طبق فرض داریم $x = u \in \text{span}(S - \{u\})$.

در هر دو حالت $x \in \text{span}(S - \{u\})$، پس $\text{span}(S) \subseteq \text{span}(S - \{u\})$.

---

# ۲-۳ قضیه

فرض کنید $S$ زیرمجموعه‌ای از فضای برداری $V$ روی میدان $F$ باشد. در این صورت بردار $u \in S$ وجود دارد به طوری که می‌توان آن را به شکل ترکیب خطی از بردارهای $S - \{u\}$ بیان کرد اگر و تنها اگر بردارهای متمایز $v_1, \dots, v_m$ متعلق به $S$ و عناصر $\alpha_1, \dots, \alpha_m$ متعلق به $F$ وجود داشته باشند به طوری که همگی $\alpha_i$ ها با هم صفر نباشند و:
$$\sum_{i=1}^{m} \alpha_i v_i = 0_V$$

**برهان:**
$(\Longrightarrow)$ 
فرض کنید $u \in S$ ترکیب خطی از عناصر $S - \{u\}$ باشد. پس عناصر متمایز $w_1, \dots, w_t$ متعلق به $S - \{u\}$ و عناصر $\lambda_1, \dots, \lambda_t$ متعلق به $F$ وجود دارند به طوری که:
$$\sum_{i=1}^{t} \lambda_i w_i = u \Longrightarrow \sum_{i=1}^{t} \lambda_i w_i + (-1_F)u = 0_V$$
بنابراین بردارهای متمایز $w_1, \dots, w_t, u$ متعلق به $S$ وجود دارند که یک ترکیب خطی از آن‌ها صفر است، ولی همه ضرایب ترکیب خطی با هم صفر نیستند (چون ضریب $u$ برابر $-1_F \neq 0_F$ است).

$(\Longleftarrow)$ 
فرض کنید $\sum_{i=1}^{m} \alpha_i v_i = 0_V$ و همه $\alpha_i$ ها صفر نباشند. با تغییر اندیس‌گذاری می‌توان فرض کرد که $\alpha_1 \neq 0_F$. در این صورت:
$$\alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_m v_m = 0_V$$
$$\Longrightarrow \alpha_1^{-1}(\alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_m v_m) = \alpha_1^{-1}(0_V) = 0_V$$
$$\Longrightarrow \alpha_1^{-1}(\alpha_1 v_1) + \alpha_1^{-1}(\alpha_2 v_2) + \dots + \alpha_1^{-1}(\alpha_m v_m) = 0_V$$
$$\Longrightarrow (\alpha_1^{-1}\alpha_1)v_1 + (\alpha_1^{-1}\alpha_2)v_2 + \dots + (\alpha_1^{-1}\alpha_m)v_m = 0_V$$
$$\Longrightarrow v_1 + (\alpha_1^{-1}\alpha_2)v_2 + \dots + (\alpha_1^{-1}\alpha_m)v_m = 0_V$$
$$\Longrightarrow v_1 = -(\alpha_1^{-1}\alpha_2)v_2 - \dots - (\alpha_1^{-1}\alpha_m)v_m = (-\alpha_1^{-1}\alpha_2)v_2 + \dots + (-\alpha_1^{-1}\alpha_m)v_m$$
$$\Longrightarrow v_1 \in \text{span}(S - \{v_1\})$$

---

### تعریف (استقلال خطی):
فرض کنید $V$ یک فضای برداری روی میدان $F$ و $S \subseteq V$ باشد. گوییم $S$ **مستقل خطی** است هرگاه در گزاره زیر صدق کند (برای هر زیرمجموعه متناهی از عناصر متمایز $x_1, \dots, x_n \in S$):
$$\sum_{i=1}^{n} \alpha_i x_i = 0_V \quad (n \in \mathbb{N}, \alpha_i \in F, x_i \in S) \Longrightarrow \alpha_i = 0_F \quad (1 \le i \le n)$$

---

### گزاره:
دو بردار متمایز $v_1$ و $v_2$ از فضای برداری $V$ وابسته خطی هستند اگر و تنها اگر یکی از آن‌ها مضرب دیگری باشد.

**برهان:**
$(\Longrightarrow)$ 
در این صورت اسکالرهای $\alpha_1$ و $\alpha_2$ (نه هر دو صفر) وجود دارند که:
$$\alpha_1 v_1 + \alpha_2 v_2 = 0_V$$
فرض کنید $\alpha_1 \neq 0_F$. در این صورت:
$$\alpha_1^{-1}(\alpha_1 v_1 + \alpha_2 v_2) = \alpha_1^{-1} 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} \alpha_1^{-1}(\alpha_1 v_1) + \alpha_1^{-1}(\alpha_2 v_2) = 0_V$$
$$\stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} (\alpha_1^{-1}\alpha_1)v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V \Longrightarrow 1_F v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V$$
$$\Longrightarrow v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V \Longrightarrow v_1 = -((\alpha_1^{-1}\alpha_2)v_2) \Longrightarrow v_1 = (-(\alpha_1^{-1}\alpha_2))v_2$$

$(\Longleftarrow)$ 
فرض کنید $\beta \in F$ وجود داشته باشد به طوری که $v_1 = \beta v_2$. در این صورت:
$$1_F v_1 + (-\beta)v_2 = 0_V$$
در نتیجه یک ترکیب خطی از $v_1$ و $v_2$ داریم که برابر صفر است ولی یکی از ضرایب ($1_F$) مخالف $0_F$ است. پس وابسته خطی هستند.

---

# ۴-۲ قضیه (مشخصه پایه با نمایش یکتا)

فرض کنید $S = \{v_1, v_2, \dots, v_n\}$ زیرمجموعه فضای برداری $V$ باشد. در این صورت $S$ پایه برای $V$ است اگر و تنها اگر برای هر $x \in V$ اسکالرهای یکتایی $c_1, c_2, \dots, c_n \in F$ وجود داشته باشند به طوری که:
$$x = \sum_{i=1}^{n} c_i v_i$$

**برهان:**
$(\Longrightarrow)$ 
فرض کنید $S$ پایه باشد (یعنی مولد و مستقل خطی است).
* **(وجود):** فرض کنید $v \in V$. چون $S$ مولد $V$ است، پس عناصر $\alpha_1, \dots, \alpha_n$ متعلق به $F$ وجود دارند که $v = \sum_{i=1}^{n} \alpha_i v_i$.
* **(یکتایی):** فرض کنید $v \in V$ و عناصر $a_1, \dots, a_n$ و $b_1, \dots, b_n$ متعلق به $F$ وجود دارند که:
$$v = \sum_{i=1}^{n} a_i v_i \quad , \quad v = \sum_{i=1}^{n} b_i v_i$$
در این صورت:
$$\sum_{i=1}^{n} a_i v_i = \sum_{i=1}^{n} b_i v_i \Longrightarrow \sum_{i=1}^{n} (a_i - b_i) v_i = 0_V$$
$$\stackrel{S \text{ مستقل خطی است}}{\Longrightarrow} a_i - b_i = 0_F \quad (1 \le i \le n) \Longrightarrow a_i = b_i \quad (1 \le i \le n)$$

$(\Longleftarrow)$
* **(اول: مولد بودن):** طبق فرض برای هر $x \in V$ اسکالرهایی وجود دارند که $x = \sum_{i=1}^{n} c_i v_i \in \text{span}(S)$، پس $V = \text{span}(S)$.
* **(دوم: استقلال خطی):** فرض کنید $\beta_1, \dots, \beta_n \in F$ باشند به طوری که:
$$\sum_{i=1}^{n} \beta_i v_i = 0_V$$
از طرفی می‌دانیم برای بردار $0_V \in V$ داریم:
$$\sum_{i=1}^{n} 0_F v_i = 0_V$$
در این صورت، طبق یکتایی در فرض داریم:
$$\beta_i = 0_F \quad (1 \le i \le n)$$
پس $S$ مستقل خطی و در نتیجه پایه است.

---

# ۱-۵ لم

فرض کنید $S$ یک زیرمجموعه مستقل خطی از فضای برداری $V$ باشد و $v \in V - S$. در این صورت:
$$S \cup \{v\} \text{ وابسته خطی است} \Longleftrightarrow v \in \text{span}(S)$$
*(و به طور معادل: $S \cup \{v\}$ مستقل خطی است $\Longleftrightarrow v \notin \text{span}(S)$).*

**برهان:**
$(\Longleftarrow)$ 
فرض کنید $v \in \text{span}(S)$. طبق تعریف، عناصر متمایز $x_1, \dots, x_t$ متعلق به $S$ و $\lambda_1, \dots, \lambda_t$ متعلق به $F$ وجود دارند به طوری که:
$$\sum_{i=1}^{t} \lambda_i x_i = v$$
در این صورت:
$$\sum_{i=1}^{t} \lambda_i x_i + (-1_F)v = 0_V$$
بنابراین یک ترکیب خطی از عناصر $S \cup \{v\}$ وجود دارد که برابر صفر است ولی همه ضرایب آن با هم صفر نیستند (چون ضریب $v$ برابر $-1_F \neq 0_F$ است). یعنی $S \cup \{v\}$ وابسته خطی است.

$(\Longrightarrow)$ 
فرض کنید $S \cup \{v\}$ وابسته خطی باشد. پس عناصر متمایز $y_1, y_2, \dots, y_s$ متعلق به $S \cup \{v\}$ و عناصر $\mu_1, \mu_2, \dots, \mu_s$ متعلق به $F$ وجود دارند به طوری که:
$$\sum_{i=1}^{s} \mu_i y_i = 0_V$$
و همه $\mu_i$ ها با هم صفر نیستند. دو حالت داریم:

* **حالت اول: $\{y_1, y_2, \dots, y_s\} \subseteq S$.**
این حالت امکان ندارد؛ زیرا $S$ مستقل خطی است، پس باید $\mu_1 = \mu_2 = \dots = \mu_s = 0_F$ باشد، در حالی که همه $\mu_i$ ها با هم صفر نیستند.

* **حالت دوم: $\{y_1, y_2, \dots, y_s\} \not\subseteq S$.**
در این صورت یکی از $y_i$ ها با $v$ برابر است. با تغییر اندیس‌گذاری می‌توان فرض کرد که $y_s = v$ (و $y_1, \dots, y_{s-1} \in S$). در نتیجه داریم:
$$\sum_{i=1}^{s-1} \mu_i y_i + \mu_s v = 0_V$$
مجدداً دو حالت برای $\mu_s$ داریم:
  * **حالت (i): $\mu_s = 0_F$.** این حالت امکان ندارد؛ زیرا اگر $\mu_s = 0_F$ باشد، آنگاه:
  $$\sum_{i=1}^{s-1} \mu_i y_i = 0_V \stackrel{S \text{ مستقل خطی است}}{\Longrightarrow} \mu_1 = \mu_2 = \dots = \mu_{s-1} = 0_F$$
  در حالی که همه $\mu_i$ ها با هم صفر نیستند.
  
  * **حالت (ii): $\mu_s \neq 0_F$.** در این صورت $\mu_s$ وارون‌پذیر است و داریم:
  $$\mu_s^{-1}\left(\sum_{i=1}^{s-1} \mu_i y_i + \mu_s v\right) = \mu_s^{-1} 0_V \Longrightarrow \sum_{i=1}^{s-1} (\mu_s^{-1}\mu_i) y_i + (\mu_s^{-1}\mu_s)v = 0_V$$
  $$\Longrightarrow \sum_{i=1}^{s-1} (\mu_s^{-1}\mu_i) y_i + 1_F \cdot v = 0_V \Longrightarrow v = \sum_{i=1}^{s-1} (-(\mu_s^{-1}\mu_i)) y_i$$
  $$\Longrightarrow v \in \text{span}(S)$$

---

# ۲-۵ قضیه (وجود پایه / قضیه توسیع به پایه)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد. فرض کنید $X' \subseteq X'' \subseteq V$ به طوری که $\text{span}(X'') = V$ و $X'$ مستقل خطی است. در این صورت یک پایه $X$ برای $V$ وجود دارد به طوری که:
$$X' \subseteq X \subseteq X''$$
*(توجه: پایه، مولد مینیمال یا مستقل خطی ماکسیمال است).*

**برهان:** 
مجموعه زیر را در نظر بگیرید:
$$\Sigma = \{ Y \subseteq V \mid X' \subseteq Y \subseteq X'' \text{ و } Y \text{ مستقل خطی است} \}$$
داریم $X' \in \Sigma$ پس $\Sigma \neq \emptyset$. زوج $(\Sigma, \subseteq)$ یک مجموعه جزئاً مرتب است.

**(۱) با استفاده از لم زورن ثابت می‌کنیم $(\Sigma, \subseteq)$ دارای عضو ماکسیمال است:**
بدین منظور باید ثابت کنیم که هر زنجیر در $(\Sigma, \subseteq)$ دارای کران بالا در $\Sigma$ است. 
فرض کنید $B$ یک زنجیر ناتهی در $\Sigma$ باشد. قرار دهید:
$$C = \bigcup_{A \in B} A$$
ادعا می‌کنیم $C$ یک کران بالای $B$ در $\Sigma$ است؛ زیرا:
* **(i)** به وضوح برای هر $A \in B$ داریم $A \subseteq C$.
* **(ii)** چون برای هر $A \in B$ داریم $X' \subseteq A \subseteq X''$، پس $X' \subseteq C \subseteq X''$.
* **(iii) $C$ مستقل خطی است:**
  * **اثباتِ (iii):** فرض کنید $x_1, \dots, x_t$ عناصر متمایز از $C$ و $\alpha_1, \dots, \alpha_t$ عناصر $F$ باشند به طوری که:
  $$\sum_{i=1}^{t} \alpha_i x_i = 0_V$$
  برای هر $1 \le i \le t$، چون $x_i \in C = \bigcup_{A \in B} A$، عنصر $A_i \in B$ وجود دارد که $x_i \in A_i$. 
  چون $B$ یک زنجیر است (یعنی هر دو عضو آن با رابطه $\subseteq$ قابل مقایسه‌اند) و تعداد $A_i$ ها متناهی است، پس اندیس $k$ ($1 \le k \le t$) وجود دارد که:
  $$A_i \subseteq A_k \quad (1 \le i \le t)$$
  *(ادامه اثبات در صفحات بعدی جزوه قرار دارد: از این رابطه نتیجه می‌شود که همه $x_1, \dots, x_t \in A_k$ و چون $A_k \in \Sigma$ مستقل خطی است، پس $\alpha_1 = \dots = \alpha_t = 0_F$ و لذا $C \in \Sigma$).*