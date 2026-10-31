# ۱-۲ قضیه (خواص مقدماتی فضای برداری)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد. در این صورت داریم:

**(i) قانون حذفی جمع:** فرض کنید $u, v, w \in V$ به طوری که $u + v = u + w$. در این صورت $v = w$.

**اثبات:**

$$
(-u) + (u + v) = (-u) + (u + w)
$$

$$
\stackrel{\text{شرکت‌پذیری}}{\Longrightarrow} (-u + u) + v = (-u + u) + w
$$

$$
\Longrightarrow 0_V + v = 0_V + w \Longrightarrow v = w
$$

**(ii) الف) بردار صفر یکتا است.**

**برهان (برهان خلف):** فرض کنید دو بردار $0_1$ و $0_2$ وجود داشته باشند که (برای هر $v \in V$):

$$
0_1 + v = v
$$

$$
0_2 + v = v
$$

در نتیجه:

$$
\begin{cases} \text{به ازای } v = 0_2 \implies 0_1 + 0_2 = 0_2 \\ \text{به ازای } v = 0_1 \implies 0_2 + 0_1 = 0_1 \end{cases}
$$

لذا $0_1 = 0_2$.

**(ii) ب) بردار قرینه یکتا است.**

**برهان (برهان خلف):** فرض کنید $u \in V$ و $u_1, u_2 \in V$ به طوری که:

$$
u + u_1 = 0_V \quad , \quad u + u_2 = 0_V
$$

بنابراین:

$$
u + u_1 = u + u_2
$$

و بنابر (i) داریم: $u_1 = u_2$.

**(iii) برای هر** $u \in V$ **داریم** $-(-u) = u$**.**

**برهان:** داریم $u + (-u) = 0_V$ و همچنین $(-(-u)) + (-u) = 0_V$.
یعنی $u$ قرینه‌ی $-u$ است. چون قرینه‌ی $-u$ یکتا است، پس $-(-u)$ برابر $u$ است.

**(iv) برای هر** $u \in V$ **داریم** $0_F \cdot u = 0_V$**.**

**برهان:** فرض کنید $u \in V$. در این صورت:

$$
0_F \cdot u = (0_F + 0_F) \cdot u \stackrel{\text{خواص ضرب اسکالر}}{=} 0_F \cdot u + 0_F \cdot u
$$

$$
\Longrightarrow 0_V + 0_F \cdot u = 0_F \cdot u + 0_F \cdot u \stackrel{\text{طبق (i)}}{\Longrightarrow} 0_F \cdot u = 0_V
$$

**(v) برای هر** $\alpha \in F$ **داریم** $\alpha \cdot 0_V = 0_V$**.**

**برهان:** فرض کنید $\alpha \in F$. در این صورت:

$$
\alpha \cdot (0_V + 0_V) = \alpha \cdot 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} \alpha \cdot 0_V + \alpha \cdot 0_V = \alpha \cdot 0_V = \alpha \cdot 0_V + 0_V
$$

مطابق (i) و خاصیت جمع برداری داریم:

$$
\alpha \cdot 0_V = 0_V
$$

**(vi) برای هر** $\alpha \in F$ **و هر** $u \in V$ **داریم** $(-\alpha)u = -(\alpha u) = \alpha(-u)$**. به ویژه داریم** $(-1_F)u = -u$**.**

**برهان:** فرض کنید $\alpha \in F$ و $u \in V$.

**الف)**

$$
(-\alpha)u + \alpha u \stackrel{\text{خاصیت ضرب اسکالر}}{=} (-\alpha + \alpha)u = 0_F \cdot u \stackrel{\text{(iv)}}{=} 0_V
$$

یعنی $(-\alpha)u$ قرینه‌ی $\alpha u$ است. بنابراین $(-\alpha)u = -(\alpha u)$.

**ب)**

$$
\alpha(-u) + \alpha u = \alpha(-u + u) = \alpha \cdot 0_V \stackrel{\text{(v)}}{=} 0_V
$$

یعنی $\alpha(-u)$ قرینه‌ی $\alpha u$ است. بنابراین $\alpha(-u) = -(\alpha u)$.

**ج) حالت خاص:**

$$
(-1_F)u \stackrel{\text{الف}}{=} -(1_F \cdot u) \stackrel{\text{خاصیت ضرب اسکالر}}{=} -u
$$

**(vii) فرض کنید** $\alpha \in F$ **و** $u \in V$ **به طوری که** $\alpha u = 0_V$**. در این صورت** $\alpha = 0_F$ **یا** $u = 0_V$**.**

**برهان:** فرض کنید $\alpha \neq 0_F$. (اگر $\alpha = 0_F$ باشد که گزاره درست می‌شود.) در این صورت $\alpha$ در $F$ دارای وارون ($\alpha^{-1}$) است. بنابراین:

$$
\alpha^{-1}(\alpha u) = \alpha^{-1}(0_V) \stackrel{\text{خاصیت ضرب اسکالر و (v)}}{\Longrightarrow} (\alpha^{-1}\alpha)u = 0_V
$$

$$
\Longrightarrow 1_F \cdot u = 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} u = 0_V
$$

# ۲-۲ قضیه (محک فشرده زیرفضا)

فرض کنید $W$ زیرمجموعه ناتهی از فضای برداری $V$ روی میدان $F$ باشد. در این صورت $W$ زیرفضای $V$ است اگر و تنها اگر برای هر $u, v \in W$ و هر $c \in F$ داشته باشیم:

$$
cu + v \in W
$$

**برهان:**
$(\Longrightarrow)$ واضح است (از بسته بودن زیرفضا نسبت به جمع و ضرب اسکالر نتیجه می‌شود).

$(\Longleftarrow)$
**(اول)** $W$ **تحت عمل جمع برداری بسته است:**
فرض کنید $u, v \in W$. در این صورت با قرار دادن $c = 1_F$ داریم:

$$
u + v = 1_F \cdot u + v \in W
$$

**(دوم)** $0_V \in W$**:**
چون $W$ ناتهی است، پس $w_0 \in W$ وجود دارد. لذا طبق فرض (به ازای $c = -1_F$) داریم:

$$
(-1_F)w_0 + w_0 \in W \stackrel{(-1_F)w_0 = -w_0}{\Longrightarrow} -w_0 + w_0 \in W \Longrightarrow 0_V \in W
$$

**(سوم) برای هر** $x \in W$ **داریم** $-x \in W$**:**
فرض کنید $x \in W$. در این صورت طبق فرض و (دوم) داریم:

$$
(-1_F)x + 0_V \in W \stackrel{(-1_F)x = -x}{\Longrightarrow} -x \in W
$$

**(چهارم) برای هر** $c \in F$ **و** $x \in W$ **داریم** $cx \in W$**:**
زیرا $cx = cx + 0_V \in W$. همچنین خاصیت شرکت‌پذیری، جابجایی و چهار خاصیت ضرب اسکالر از $V$ به $W$ القا می‌شوند.

### مثال:

مجموعه‌ی $W = \{(x, y) \in \mathbb{R}^2 \mid x \ge 0, y \ge 0\}$ زیرفضای $\mathbb{R}^2$ نیست:

1. $(a, b), (c, d) \in W \implies (a+c, b+d) \in W$ (تحت جمع بسته است).

2. برای هر $\alpha \in \mathbb{R}$ و $(a, b) \in W$، الزاماً $(\alpha a, \alpha b) \in W$ نیست (به ازای $\alpha < 0$ برقرار نیست).

# ۴-۲ تعریف (درجه یک چندجمله‌ای ناصفر)

$$
\deg\left(\sum_{i=0}^{\infty} a_i x^i\right) = \max\{i \mid a_i \neq 0\}
$$

چون چندجمله‌ای ناصفر است، پس مجموعه $\{i \mid a_i \neq 0\}$ ناتهی و متناهی است.
درجه‌ی چندجمله‌ای صفر را $-\infty$ تعریف می‌کنیم (قرارداد: برای هر عدد طبیعی $n$ داریم $-\infty < n$).

# ۵-۲ قضیه

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $\{W_i\}_{i \in I}$ خانواده‌ای از زیرفضاهای $V$ باشد. در این صورت $\bigcap_{i \in I} W_i$ زیرفضای $V$ است.

**برهان:**
توجه کنید برای هر $i \in I$ داریم $0_V \in W_i$، پس $0_V \in \bigcap_{i \in I} W_i \neq \emptyset$.
فرض کنید $u, v \in \bigcap_{i \in I} W_i$ و $c \in F$. در این صورت:

$$
u, v \in W_i \quad (\forall i \in I) \stackrel{W_i \text{ زیرفضای } V}{\Longrightarrow} cu + v \in W_i \quad (\forall i \in I)
$$

$$
\Longrightarrow cu + v \in \bigcap_{i \in I} W_i
$$

حکم از قضیه‌ی محک فشرده نتیجه می‌شود.

# ۶-۲ لم

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $S \subseteq V$. در این صورت:

$$
\text{span}(S) = \bigcap_{\substack{W \le V \\ S \subseteq W}} W
$$

*(که در آن* $W \le V$ *به معنای «*$W$ *زیرفضای* $V$ *است» می‌باشد).*

**برهان:**
قرار دهید $\Sigma = \{W \le V \mid S \subseteq W\}$ (مجموعه زیرفضاهای $V$ شامل $S$).
توجه کنید $V \in \Sigma$ پس $\Sigma \neq \emptyset$. مطابق قضیه بالا (۵-۲)، $\bigcap_{W \in \Sigma} W$ یک زیرفضای $V$ است.
واضح است که این اشتراک شامل $S$ است و کوچک‌ترین زیرفضایی از $V$ است که شامل $S$ می‌باشد (زیرا اگر $W'$ هر زیرفضای شامل $S$ باشد، آنگاه $W' \in \Sigma$ و در نتیجه $\bigcap_{W \in \Sigma} W \subseteq W'$). پس طبق تعریف، برابر $\text{span}(S)$ است.

# ۷-۲ قضیه

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $\emptyset \neq S \subseteq V$. در این صورت:

$$
\text{span}(S) = \left\{ \sum_{i=1}^{n} \alpha_i v_i \;\middle\vert{}\; n \in \mathbb{N}, \alpha_i \in F, v_i \in S \right\}
$$

*(مجموعه همه ترکیب‌های خطی ممکن از بردارهای* $S$*).*

**برهان:** قرار دهید:

$$
\Sigma = \left\{ \sum_{i=1}^{n} \alpha_i v_i \;\middle\vert{}\; n \in \mathbb{N}, \alpha_i \in F, v_i \in S \right\}
$$

**(i)** $\Sigma$ **یک زیرفضای** $V$ **است:**
چون $S \neq \emptyset$، پس $\Sigma \neq \emptyset$. فرض کنید $\sum_{i=1}^{m} \beta_i u_i \in \Sigma$ و $\sum_{i=1}^{n} \alpha_i v_i \in \Sigma$ و $c \in F$. در این صورت:

$$
c\left(\sum_{i=1}^{m} \beta_i u_i\right) + \left(\sum_{i=1}^{n} \alpha_i v_i\right) = \sum_{i=1}^{m} (c\beta_i) u_i + \sum_{i=1}^{n} \alpha_i v_i
$$

این عنصر به شکل عناصر $\Sigma$ است (چرا که $u_i, v_i \in S$ و $\alpha_i, c\beta_i \in F$ و تعداد جملات $n+m \in \mathbb{N}$ است). پس $\Sigma$ زیرفضای $V$ است.

**(ii)** $S \subseteq \Sigma$**:**
فرض کنید $x \in S$. در این صورت $x = 1_F \cdot x \in \Sigma$.

از (i) و (ii) می‌فهمیم که $\Sigma$ زیرفضای شامل $S$ است؛ بنابراین طبق تعریفِ $\text{span}(S)$ (کوچک‌ترین زیرفضای شامل $S$) داریم:

$$
\text{span}(S) \subseteq \Sigma
$$

**(iii) اگر** $W$ **یک زیرفضای** $V$ **باشد که شامل** $S$ **است، آنگاه** $\Sigma \subseteq W$**:**
فرض کنید $x \in \Sigma$. در این صورت عناصر $\alpha_1, \dots, \alpha_n \in F$ و عناصر $v_1, \dots, v_n \in S$ وجود دارند که:

$$
x = \sum_{i=1}^{n} \alpha_i v_i
$$

چون $S \subseteq W$ پس $v_1, \dots, v_n \in W$. بنابراین با توجه به بسته بودن $W$ نسبت به ضرب اسکالر و جمع، داریم:

$$
x = \sum_{i=1}^{n} \alpha_i v_i \in W
$$

از آنجا که $\text{span}(S)$ خود یک زیرفضای شامل $S$ است، با قرار دادن $W = \text{span}(S)$ در (iii) داریم $\Sigma \subseteq \text{span}(S)$.
در نتیجه $\text{span}(S) = \Sigma$.

# ۸-۲ لم (قضیه؟)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد و $X = \{x_1, x_2, \dots, x_r\}$ و $Y = \{y_1, y_2, \dots, y_s\}$ دو زیرمجموعه ناتهی از $V$ باشند. در این صورت:

* **الف)** اگر $X \subseteq \text{span}(Y)$ (یعنی هر عنصر $X$ ترکیب خطی از عناصر $Y$ باشد)، آنگاه $\text{span}(X) \subseteq \text{span}(Y)$.

* **ب)** $\text{span}(X) = \text{span}(Y)$ اگر و تنها اگر هر عنصر $X$ ترکیب خطی از عناصر $Y$ باشد و هر عضو $Y$ ترکیب خطی از عناصر $X$ باشد.

**برهان:**

* **الف)** طبق تعریف، $\text{span}(X)$ کوچک‌ترین زیرفضای $V$ شامل $X$ است. از طرف دیگر، $\text{span}(Y)$ یک زیرفضای $V$ است که طبق فرض شامل $X$ است ($X \subseteq \text{span}(Y)$). در نتیجه:

$$
\text{span}(X) \subseteq \text{span}(Y)
$$

* **ب)** با استفاده از قسمت (الف) به راحتی نتیجه می‌شود.

# ۹-۲ لم

فرض کنید $V$ فضای برداری روی میدان $F$ باشد، $S \subseteq V$ و $u \in S$. در این صورت:

$$
\text{span}(S) = \text{span}(S - \{u\}) \Longleftrightarrow u \text{ ترکیب خطی از عناصر } S - \{u\} \text{ باشد } (u \in \text{span}(S - \{u\}))
$$

**برهان:**
$(\Longrightarrow)$
چون $u \in S$ و $S \subseteq \text{span}(S)$، پس $u \in \text{span}(S)$. طبق فرض $\text{span}(S) = \text{span}(S - \{u\})$، در نتیجه $u \in \text{span}(S - \{u\})$؛ یعنی $u$ ترکیب خطی از عناصر $S - \{u\}$ است.

$(\Longleftarrow)$
**(اول) ثابت می‌کنیم** $\text{span}(S - \{u\}) \subseteq \text{span}(S)$**:**
می‌دانیم $S - \{u\} \subseteq S \subseteq \text{span}(S)$. پس $S - \{u\} \subseteq \text{span}(S)$ و در نتیجه:

$$
\text{span}(S - \{u\}) \subseteq \text{span}(S)
$$

*(نکته کلی:* $X \subseteq Y \implies \text{span}(X) \subseteq \text{span}(Y)$*).*

**(دوم) ثابت می‌کنیم** $\text{span}(S) \subseteq \text{span}(S - \{u\})$**:**
بدین منظور با توجه به قضیه قبل، کافی است ثابت کنیم $S \subseteq \text{span}(S - \{u\})$.
فرض کنید $x \in S$. دو حالت داریم:

1. $x \neq u$: در نتیجه $x \in S - \{u\} \subseteq \text{span}(S - \{u\})$.

2. $x = u$: طبق فرض داریم $x = u \in \text{span}(S - \{u\})$.

در هر دو حالت $x \in \text{span}(S - \{u\})$، پس $\text{span}(S) \subseteq \text{span}(S - \{u\})$.

# ۲-۳ قضیه

فرض کنید $S$ زیرمجموعه‌ای از فضای برداری $V$ روی میدان $F$ باشد. در این صورت بردار $u \in S$ وجود دارد به طوری که می‌توان آن را به شکل ترکیب خطی از بردارهای $S - \{u\}$ بیان کرد اگر و تنها اگر بردارهای متمایز $v_1, \dots, v_m$ متعلق به $S$ و عناصر $\alpha_1, \dots, \alpha_m$ متعلق به $F$ وجود داشته باشند به طوری که همگی $\alpha_i$ ها با هم صفر نباشند و:

$$
\sum_{i=1}^{m} \alpha_i v_i = 0_V
$$

**برهان:**
$(\Longrightarrow)$
فرض کنید $u \in S$ ترکیب خطی از عناصر $S - \{u\}$ باشد. پس عناصر متمایز $w_1, \dots, w_t$ متعلق به $S - \{u\}$ و عناصر $\lambda_1, \dots, \lambda_t$ متعلق به $F$ وجود دارند به طوری که:

$$
\sum_{i=1}^{t} \lambda_i w_i = u \Longrightarrow \sum_{i=1}^{t} \lambda_i w_i + (-1_F)u = 0_V
$$

بنابراین بردارهای متمایز $w_1, \dots, w_t, u$ متعلق به $S$ وجود دارند که یک ترکیب خطی از آن‌ها صفر است، ولی همه ضرایب ترکیب خطی با هم صفر نیستند (چون ضریب $u$ برابر $-1_F \neq 0_F$ است).

$(\Longleftarrow)$
فرض کنید $\sum_{i=1}^{m} \alpha_i v_i = 0_V$ و همه $\alpha_i$ ها صفر نباشند. با تغییر اندیس‌گذاری می‌توان فرض کرد که $\alpha_1 \neq 0_F$. در این صورت:

$$
\alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_m v_m = 0_V
$$

$$
\Longrightarrow \alpha_1^{-1}(\alpha_1 v_1 + \alpha_2 v_2 + \dots + \alpha_m v_m) = \alpha_1^{-1}(0_V) = 0_V
$$

$$
\Longrightarrow \alpha_1^{-1}(\alpha_1 v_1) + \alpha_1^{-1}(\alpha_2 v_2) + \dots + \alpha_1^{-1}(\alpha_m v_m) = 0_V
$$

$$
\Longrightarrow (\alpha_1^{-1}\alpha_1)v_1 + (\alpha_1^{-1}\alpha_2)v_2 + \dots + (\alpha_1^{-1}\alpha_m)v_m = 0_V
$$

$$
\Longrightarrow v_1 + (\alpha_1^{-1}\alpha_2)v_2 + \dots + (\alpha_1^{-1}\alpha_m)v_m = 0_V
$$

$$
\Longrightarrow v_1 = -(\alpha_1^{-1}\alpha_2)v_2 - \dots - (\alpha_1^{-1}\alpha_m)v_m = (-\alpha_1^{-1}\alpha_2)v_2 + \dots + (-\alpha_1^{-1}\alpha_m)v_m
$$

$$
\Longrightarrow v_1 \in \text{span}(S - \{v_1\})
$$

### تعریف (استقلال خطی):

فرض کنید $V$ یک فضای برداری روی میدان $F$ و $S \subseteq V$ باشد. گوییم $S$ **مستقل خطی** است هرگاه در گزاره زیر صدق کند (برای هر زیرمجموعه متناهی از عناصر متمایز $x_1, \dots, x_n \in S$):

$$
\sum_{i=1}^{n} \alpha_i x_i = 0_V \quad (n \in \mathbb{N}, \alpha_i \in F, x_i \in S) \Longrightarrow \alpha_i = 0_F \quad (1 \le i \le n)
$$

### گزاره:

دو بردار متمایز $v_1$ و $v_2$ از فضای برداری $V$ وابسته خطی هستند اگر و تنها اگر یکی از آن‌ها مضرب دیگری باشد.

**برهان:**
$(\Longrightarrow)$
در این صورت اسکالرهای $\alpha_1$ و $\alpha_2$ (نه هر دو صفر) وجود دارند که:

$$
\alpha_1 v_1 + \alpha_2 v_2 = 0_V
$$

فرض کنید $\alpha_1 \neq 0_F$. در این صورت:

$$
\alpha_1^{-1}(\alpha_1 v_1 + \alpha_2 v_2) = \alpha_1^{-1} 0_V \stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} \alpha_1^{-1}(\alpha_1 v_1) + \alpha_1^{-1}(\alpha_2 v_2) = 0_V
$$

$$
\stackrel{\text{خاصیت ضرب اسکالر}}{\Longrightarrow} (\alpha_1^{-1}\alpha_1)v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V \Longrightarrow 1_F v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V
$$

$$
\Longrightarrow v_1 + (\alpha_1^{-1}\alpha_2)v_2 = 0_V \Longrightarrow v_1 = -((\alpha_1^{-1}\alpha_2)v_2) \Longrightarrow v_1 = (-(\alpha_1^{-1}\alpha_2))v_2
$$

$(\Longleftarrow)$
فرض کنید $\beta \in F$ وجود داشته باشد به طوری که $v_1 = \beta v_2$. در این صورت:

$$
1_F v_1 + (-\beta)v_2 = 0_V
$$

در نتیجه یک ترکیب خطی از $v_1$ و $v_2$ داریم که برابر صفر است ولی یکی از ضرایب ($1_F$) مخالف $0_F$ است. پس وابسته خطی هستند.

# ۴-۲ قضیه (مشخصه پایه با نمایش یکتا)

فرض کنید $S = \{v_1, v_2, \dots, v_n\}$ زیرمجموعه فضای برداری $V$ باشد. در این صورت $S$ پایه برای $V$ است اگر و تنها اگر برای هر $x \in V$ اسکالرهای یکتایی $c_1, c_2, \dots, c_n \in F$ وجود داشته باشند به طوری که:

$$
x = \sum_{i=1}^{n} c_i v_i
$$

**برهان:**
$(\Longrightarrow)$
فرض کنید $S$ پایه باشد (یعنی مولد و مستقل خطی است).

* **(وجود):** فرض کنید $v \in V$. چون $S$ مولد $V$ است، پس عناصر $\alpha_1, \dots, \alpha_n$ متعلق به $F$ وجود دارند که $v = \sum_{i=1}^{n} \alpha_i v_i$.

* **(یکتایی):** فرض کنید $v \in V$ و عناصر $a_1, \dots, a_n$ و $b_1, \dots, b_n$ متعلق به $F$ وجود دارند که:

$$
v = \sum_{i=1}^{n} a_i v_i \quad , \quad v = \sum_{i=1}^{n} b_i v_i
$$

در این صورت:

$$
\sum_{i=1}^{n} a_i v_i = \sum_{i=1}^{n} b_i v_i \Longrightarrow \sum_{i=1}^{n} (a_i - b_i) v_i = 0_V
$$

$$
\stackrel{S \text{ مستقل خطی است}}{\Longrightarrow} a_i - b_i = 0_F \quad (1 \le i \le n) \Longrightarrow a_i = b_i \quad (1 \le i \le n)
$$

$(\Longleftarrow)$

* **(اول: مولد بودن):** طبق فرض برای هر $x \in V$ اسکالرهایی وجود دارند که $x = \sum_{i=1}^{n} c_i v_i \in \text{span}(S)$، پس $V = \text{span}(S)$.

* **(دوم: استقلال خطی):** فرض کنید $\beta_1, \dots, \beta_n \in F$ باشند به طوری که:

$$
\sum_{i=1}^{n} \beta_i v_i = 0_V
$$

از طرفی می‌دانیم برای بردار $0_V \in V$ داریم:

$$
\sum_{i=1}^{n} 0_F v_i = 0_V
$$

در این صورت، طبق یکتایی در فرض داریم:

$$
\beta_i = 0_F \quad (1 \le i \le n)
$$

پس $S$ مستقل خطی و در نتیجه پایه است.

# ۱-۵ لم

فرض کنید $S$ یک زیرمجموعه مستقل خطی از فضای برداری $V$ باشد و $v \in V - S$. در این صورت:

$$
S \cup \{v\} \text{ وابسته خطی است} \Longleftrightarrow v \in \text{span}(S)
$$

*(و به طور معادل:* $S \cup \{v\}$ *مستقل خطی است* $\Longleftrightarrow v \notin \text{span}(S)$*).*

**برهان:**
$(\Longleftarrow)$
فرض کنید $v \in \text{span}(S)$. طبق تعریف، عناصر متمایز $x_1, \dots, x_t$ متعلق به $S$ و $\lambda_1, \dots, \lambda_t$ متعلق به $F$ وجود دارند به طوری که:

$$
\sum_{i=1}^{t} \lambda_i x_i = v
$$

در این صورت:

$$
\sum_{i=1}^{t} \lambda_i x_i + (-1_F)v = 0_V
$$

بنابراین یک ترکیب خطی از عناصر $S \cup \{v\}$ وجود دارد که برابر صفر است ولی همه ضرایب آن با هم صفر نیستند (چون ضریب $v$ برابر $-1_F \neq 0_F$ است). یعنی $S \cup \{v\}$ وابسته خطی است.

$(\Longrightarrow)$
فرض کنید $S \cup \{v\}$ وابسته خطی باشد. پس عناصر متمایز $y_1, y_2, \dots, y_s$ متعلق به $S \cup \{v\}$ و عناصر $\mu_1, \mu_2, \dots, \mu_s$ متعلق به $F$ وجود دارند به طوری که:

$$
\sum_{i=1}^{s} \mu_i y_i = 0_V
$$

و همه $\mu_i$ ها با هم صفر نیستند. دو حالت داریم:

* **حالت اول:** $\{y_1, y_2, \dots, y_s\} \subseteq S$**.**
  این حالت امکان ندارد؛ زیرا $S$ مستقل خطی است، پس باید $\mu_1 = \mu_2 = \dots = \mu_s = 0_F$ باشد، در حالی که همه $\mu_i$ ها با هم صفر نیستند.

* **حالت دوم:** $\{y_1, y_2, \dots, y_s\} \not\subseteq S$**.**
  در این صورت یکی از $y_i$ ها با $v$ برابر است. با تغییر اندیس‌گذاری می‌توان فرض کرد که $y_s = v$ (و $y_1, \dots, y_{s-1} \in S$). در نتیجه داریم:

$$
\sum_{i=1}^{s-1} \mu_i y_i + \mu_s v = 0_V
$$

مجدداً دو حالت برای $\mu_s$ داریم:

* **حالت (i):** $\mu_s = 0_F$**.** این حالت امکان ندارد؛ زیرا اگر $\mu_s = 0_F$ باشد، آنگاه:

$$
\sum_{i=1}^{s-1} \mu_i y_i = 0_V \stackrel{S \text{ مستقل خطی است}}{\Longrightarrow} \mu_1 = \mu_2 = \dots = \mu_{s-1} = 0_F
$$

در حالی که همه $\mu_i$ ها با هم صفر نیستند.

* **حالت (ii):** $\mu_s \neq 0_F$**.** در این صورت $\mu_s$ وارون‌پذیر است و داریم:

$$
\mu_s^{-1}\left(\sum_{i=1}^{s-1} \mu_i y_i + \mu_s v\right) = \mu_s^{-1} 0_V \Longrightarrow \sum_{i=1}^{s-1} (\mu_s^{-1}\mu_i) y_i + (\mu_s^{-1}\mu_s)v = 0_V
$$

$$
\Longrightarrow \sum_{i=1}^{s-1} (\mu_s^{-1}\mu_i) y_i + 1_F \cdot v = 0_V \Longrightarrow v = \sum_{i=1}^{s-1} (-(\mu_s^{-1}\mu_i)) y_i
$$

$$
\Longrightarrow v \in \text{span}(S)
$$

# ۲-۵ قضیه (وجود پایه / قضیه توسیع به پایه)

فرض کنید $V$ یک فضای برداری روی میدان $F$ باشد. فرض کنید $X' \subseteq X'' \subseteq V$ به طوری که $\text{span}(X'') = V$ و $X'$ مستقل خطی است. در این صورت یک پایه $X$ برای $V$ وجود دارد به طوری که:

$$
X' \subseteq X \subseteq X''
$$

*(توجه: پایه، مولد مینیمال یا مستقل خطی ماکسیمال است).*

**برهان:**
مجموعه زیر را در نظر بگیرید:

$$
\Sigma = \{ Y \subseteq V \mid X' \subseteq Y \subseteq X'' \text{ و } Y \text{ مستقل خطی است} \}
$$

داریم $X' \in \Sigma$ پس $\Sigma \neq \emptyset$. زوج $(\Sigma, \subseteq)$ یک مجموعه جزئاً مرتب است.

**(۱) با استفاده از لم زورن ثابت می‌کنیم** $(\Sigma, \subseteq)$ **دارای عضو ماکسیمال است:**
بدین منظور باید ثابت کنیم که هر زنجیر در $(\Sigma, \subseteq)$ دارای کران بالا در $\Sigma$ است.
فرض کنید $B$ یک زنجیر ناتهی در $\Sigma$ باشد. قرار دهید:

$$
C = \bigcup_{A \in B} A
$$

ادعا می‌کنیم $C$ یک کران بالای $B$ در $\Sigma$ است؛ زیرا:

* **(i)** به وضوح برای هر $A \in B$ داریم $A \subseteq C$.

* **(ii)** چون برای هر $A \in B$ داریم $X' \subseteq A \subseteq X''$، پس $X' \subseteq C \subseteq X''$.

* **(iii)** $C$ **مستقل خطی است:**

  * **اثباتِ (iii):** فرض کنید $x_1, \dots, x_t$ عناصر متمایز از $C$ و $\lambda_1, \dots, \lambda_t$ عناصر $F$ باشند به طوری که:

$$
\sum_{i=1}^{t} \lambda_i x_i = 0_V
$$

برای هر $1 \le i \le t$، چون $x_i \in C = \bigcup_{A \in B} A$، عنصر $A_i \in B$ وجود دارد که $x_i \in A_i$.
چون $B$ یک زنجیر است، پس اندیس $k$ ($1 \le k \le t$) وجود دارد که:

$$
A_i \subseteq A_k \quad (1 \le i \le t) \quad (*)
$$

*(خارج از برهان: با استقرا روی $t$ حکم $(*)$ را ثابت می‌کنیم:*
*برای $t=1$ حکم واضح است. فرض کنید $s \ge 2$ و حکم برای $s-1$ برقرار باشد. فرض کنید $Y_1, \dots, Y_{s-1}, Y_s \in B$. طبق فرض استقرا $j$ ($1 \le j \le s-1$) وجود دارد که $Y_i \subseteq Y_j$ ($1 \le i \le s-1$). برای $Y_j$ و $Y_s$ (چون $B$ زنجیر است) داریم $Y_j \subseteq Y_s$ یا $Y_s \subseteq Y_j$. اگر $Y_j \subseteq Y_s$ آنگاه $Y_i \subseteq Y_s$ ($1 \le i \le s$)، و اگر $Y_s \subseteq Y_j$ آنگاه $Y_i \subseteq Y_j$ ($1 \le i \le s$)).*

بنابراین $x_1, x_2, \dots, x_t \in A_k$. چون $A_k \in B \subseteq \Sigma$ مستقل خطی است، پس:

$$
\lambda_1 = \lambda_2 = \dots = \lambda_t = 0_F
$$

پس $C$ مستقل خطی است.

از (i)، (ii) و (iii) نتیجه می‌شود که $C \in \Sigma$ و کران بالای $B$ است.
طبق لم زورن $(\Sigma, \subseteq)$ دارای عنصر ماکسیمال است. آن را $X$ می‌نامیم. چون $X \in \Sigma$ مستقل خطی است و $X' \subseteq X \subseteq X''$، پس کافی است ثابت کنیم $\text{span}(X) = V$.

**برهان (خلف):** فرض کنید $\text{span}(X) \neq V$. سعی می‌کنیم به یک تناقض برسیم. داریم:

$$
\text{span}(X) \neq \text{span}(X'') = V \Longrightarrow \text{span}(X'') \not\subseteq \text{span}(X)
$$

$$
\stackrel{\text{لم ۸-۲}}{\Longrightarrow} X'' \not\subseteq \text{span}(X) \Longrightarrow \exists x \in X'' : x \notin \text{span}(X)
$$

چون $x \notin \text{span}(X)$، طبق لم ۱-۵ مجموعه $X \cup \{x\}$ مستقل خطی است. همچنین چون $X \subseteq X''$ و $x \in X''$، داریم $X' \subseteq X \cup \{x\} \subseteq X''$. بنابراین:

$$
X \cup \{x\} \in \Sigma
$$

از طرفی چون $x \notin \text{span}(X)$ پس $x \notin X$ و در نتیجه $X \subsetneq X \cup \{x\}$. این مطلب با ماکسیمال بودن $X$ در $(\Sigma, \subseteq)$ تناقض دارد. بنابراین فرض خلف نادرست است و $\text{span}(X) = V$.

# ۳-۵ نتیجه

فرض کنید $V$ فضای برداری روی میدان $F$ باشد. در این صورت:

* **الف)** $V$ **دارای پایه است:**
  در قضیه قبل (۲-۵) به جای $X'$ مجموعه $\emptyset$ و به جای $X''$ مجموعه $V$ را قرار دهید.

* **ب) هر زیرمجموعه مستقل خطی** $V$ **مشمول در یک پایه** $V$ **است:**
  فرض کنید $Y$ یک زیرمجموعه مستقل خطی از $V$ باشد. در ۲-۵ به جای $X'$ مجموعه $Y$ و به جای $X''$ مجموعه $V$ را قرار دهید.

* **ج) هر زیرمجموعه مولد** $V$ **شامل یک پایه** $V$ **است:**
  فرض کنید $Z$ یک مولد $V$ باشد. در ۲-۵ به جای $X'$ مجموعه $\emptyset$ و به جای $X''$ مجموعه $Z$ را قرار دهید.

* **د)** فرض کنید $V$ یک فضای برداری باشد که دارای مجموعه مولد متناهی است. در این صورت $V$ دارای پایه متناهی است.

# ۱-۶ قضیه جایگذاری (Replacement Theorem)

فرض کنید $V$ فضای برداری روی میدان $F$ باشد. فرض کنید $V$ دارای مولد $n$ عضوی $G$ باشد ($|G| = n \ge 0$ و $\text{span}(G) = V$) و $L$ یک زیرمجموعه مستقل خطی از $V$ باشد که $m$ عضو دارد ($|L| = m \ge 0$). در این صورت:

1. $m \le n$

2. زیرمجموعه $H$ از $G$ وجود دارد که $n - m$ عضو دارد ($|H| = n - m$) و $\text{span}(H \cup L) = V$.

*(که در آن $L = \{l_1, l_2, \dots, l_m\}$ و $G = \{g_1, g_2, \dots, g_n\}$).*

**توجیه برهان (ایده شهودی):**
عناصر $L$ را یکی‌یکی به جای عناصر $G$ جایگذاری می‌کنیم:

* **(قدم اول):** اگر $G = \emptyset$، آنگاه $V = \text{span}(\emptyset) = \{0_V\}$. در این صورت اگر $m \ge 1$ باشد، این حالت امکان ندارد چون $L$ زیرمجموعه مستقل خطی ناتهی از $\{0_V\}$ نخواهد بود. پس اگر $m \ge 1$ باشد، حتماً $n \ge 1$.
  حال چون $l_1 \in V = \text{span}(G)$، داریم:

$$
\exists \lambda_1, \dots, \lambda_n \in F : \sum_{i=1}^{n} \lambda_i g_i = l_1
$$

چون $\{l_1\}$ مستقل خطی است ($l_1 \neq 0_V$)، پس یکی از $\lambda_i$ ها ناصفر است. با تغییر اندیس‌گذاری فرض کنید $\lambda_n \neq 0_F$. در این صورت:

$$
g_n = \sum_{i=1}^{n-1} (-\lambda_n^{-1}\lambda_i) g_i + \lambda_n^{-1} l_1
$$

$$
\Longrightarrow g_n \in \text{span}(\{g_1, g_2, \dots, g_{n-1}, l_1\})
$$

$$
\Longrightarrow \{g_1, g_2, \dots, g_n\} \subseteq \text{span}(\{g_1, g_2, \dots, g_{n-1}, l_1\})
$$

$$
\Longrightarrow V = \text{span}(G) \subseteq \text{span}(\{g_1, g_2, \dots, g_{n-1}, l_1\}) \Longrightarrow V = \text{span}(\{g_1, \dots, g_{n-1}, l_1\})
$$

* **(قدم دوم):** حال $l_2 \in V = \text{span}(\{g_1, g_2, \dots, g_{n-1}, l_1\})$، پس:

$$
\exists \mu_1, \dots, \mu_{n-1}, \mu \in F : \sum_{i=1}^{n-1} \mu_i g_i + \mu l_1 = l_2
$$

اگر $n - 1 = 0$ باشد، آنگاه $\mu l_1 = l_2$ و در نتیجه $\{l_1, l_2\}$ وابسته خطی است، در حالی که $L$ مستقل خطی است. بنابراین $n - 1 > 0$ (یعنی $n \ge 2$). همچنین یکی از $\mu_i$ ها ($1 \le i \le n-1$) ناصفر است، زیرا در غیر این صورت مجدداً $\mu l_1 = l_2$ که تناقض است.
با تغییر اندیس‌گذاری می‌توان فرض کرد که $\mu_{n-1} \neq 0_F$. در این صورت:

$$
g_{n-1} = \sum_{i=1}^{n-2} (-\mu_{n-1}^{-1}\mu_i) g_i + (-\mu_{n-1}^{-1}\mu) l_1 + \mu_{n-1}^{-1} l_2
$$

$$
\Longrightarrow g_{n-1} \in \text{span}(\{g_1, g_2, \dots, g_{n-2}, l_1, l_2\})
$$

$$
\Longrightarrow \{g_1, g_2, \dots, g_{n-1}, l_1\} \subseteq \text{span}(\{g_1, \dots, g_{n-2}, l_1, l_2\})
$$

$$
\Longrightarrow V = \text{span}(\{g_1, \dots, g_{n-1}, l_1\}) \subseteq \text{span}(\{g_1, \dots, g_{n-2}, l_1, l_2\}) \Longrightarrow V = \text{span}(\{g_1, \dots, g_{n-2}, l_1, l_2\})
$$

و به همین ترتیب ادامه می‌دهیم.

**برهان دقیق (با استقرا روی $m$):**
با استقرا روی $m$ حکم را ثابت می‌کنیم.

* **پایه استقرا:** فرض کنید $m = 0$ ($L = \emptyset$). در این صورت به وضوح $0 = m \le n$ و $H$ را می‌توان همان $G$ در نظر گرفت ($|H| = n - 0 = n$ و $\text{span}(G \cup \emptyset) = V$).

* **گام استقرا:** فرض کنید $m \ge 1$ و حکم برای حالت $m - 1$ برقرار باشد؛ یعنی:
  *(فرض استقرا: اگر $L'$ یک مجموعه مستقل خطی $m-1$ عضوی از $V$ باشد، آنگاه $m - 1 \le n$ و $\exists H' \subseteq G$ به طوری که $\text{span}(H' \cup L') = V$ و $|H'| = n - m + 1$).*

حال فرض کنید $L = \{l_1, \dots, l_m\}$ یک زیرمجموعه مستقل خطی $m$ عضوی از $V$ باشد و $G = \{g_1, g_2, \dots, g_n\}$. قرار دهید $L' = \{l_1, \dots, l_{m-1}\}$ که زیرمجموعه مستقل خطی $m-1$ عضوی از $V$ است. در نتیجه طبق فرض استقرا داریم:

$$
m - 1 \le n \quad \text{و} \quad \exists H' \subseteq G : \text{span}(H' \cup L') = V, \quad |H'| = n - m + 1
$$

فرض کنید $H' = \{h_1, \dots, h_{n-m+1}\}$. چون $l_m \in V = \text{span}(H' \cup L')$، داریم:

$$
\exists \lambda_1, \dots, \lambda_{n-m+1}, \mu_1, \dots, \mu_{m-1} \in F : \sum_{i=1}^{n-m+1} \lambda_i h_i + \sum_{i=1}^{m-1} \mu_i l_i = l_m
$$

اگر $n - m + 1 = 0$ باشد، آنگاه $l_m = \sum_{i=1}^{m-1} \mu_i l_i$، پس $\{l_1, \dots, l_m\}$ وابسته خطی است، در حالی که $L$ مستقل خطی است. پس $n - m + 1 > 0$ و بنابراین $m \le n$.
به همین ترتیب چون $L$ مستقل خطی است، پس یکی از $\lambda_i$ ها ناصفر است (وگرنه $l_m \in \text{span}(L')$). با تغییر اندیس‌گذاری می‌توان آن را $\lambda_{n-m+1} \neq 0_F$ فرض کرد. داریم:

$$
h_{n-m+1} = \sum_{i=1}^{n-m} (-\lambda_{n-m+1}^{-1}\lambda_i) h_i + \sum_{i=1}^{m-1} (-\lambda_{n-m+1}^{-1}\mu_i) l_i + \lambda_{n-m+1}^{-1} l_m
$$

$$
\Longrightarrow h_{n-m+1} \in \text{span}(\{h_1, \dots, h_{n-m}, l_1, \dots, l_m\})
$$

$$
\Longrightarrow H' \cup L' = \{h_1, \dots, h_{n-m+1}, l_1, \dots, l_{m-1}\} \subseteq \text{span}(\{h_1, \dots, h_{n-m}, l_1, \dots, l_m\})
$$

$$
\Longrightarrow V = \text{span}(H' \cup L') \subseteq \text{span}(\{h_1, \dots, h_{n-m}, l_1, \dots, l_m\})
$$

قرار دهید $H = \{h_1, \dots, h_{n-m}\} \subseteq G$. در این صورت $|H| = n - m$ و $\text{span}(H \cup L) = V$.

# ۲-۶ نتیجه (خوش‌تعریفی بُعد)

فرض کنید $V$ فضای برداری روی میدان $F$ و $X$ و $Y$ دو پایه $V$ باشند. در این صورت $|X| = |Y|$ (یک تناظر دو سویه بین $X$ و $Y$ وجود دارد).

**برهان:**

* **حالت اول:** فرض کنید $V$ دارای یک پایه نامتناهی $Z$ باشد. در این صورت برای هر پایه دیگر $V$ مانند $W$ داریم $|W| = |Z|$ (و هیچ پایه متناهی نمی‌تواند وجود داشته باشد، زیرا طبق قضیه جایگذاری اگر پایه متناهی $n$ عضوی وجود داشت، هیچ مجموعه مستقل خطی نمی‌توانست بیش از $n$ عضو داشته باشد).

* **حالت دوم:** $X$ و $Y$ هر دو متناهی هستند. فرض کنید $|Y| = s$ و $|X| = t$.

$$
\begin{cases} X \text{ مستقل خطی و } Y \text{ مولد است} \stackrel{\text{قضیه ۱-۶}}{\Longrightarrow} t \le s \\ Y \text{ مستقل خطی و } X \text{ مولد است} \stackrel{\text{قضیه ۱-۶}}{\Longrightarrow} s \le t \end{cases} \Longrightarrow s = t
$$

# ۵-۶ نتیجه

فرض کنید $V$ فضای برداری روی میدان $F$ و $\dim(V) = n$ باشد. در این صورت:

* **الف) (ماکسیمم تعداد بردارهای مستقل خطی از $V$ برابر $n$ است):**
  اگر $\{v_1, \dots, v_m\}$ یک مجموعه مستقل خطی از $V$ باشد، آنگاه $m \le n$. به علاوه اگر $m = n$ باشد، آنگاه $\{v_1, \dots, v_m\}$ یک پایه $V$ است.

  * **برهان:** طبق قضیه ۲-۵ (نتیجه ۳-۵ ب)، یک پایه $X$ برای $V$ وجود دارد که $\{v_1, \dots, v_m\} \subseteq X$. طبق قضیه ۲-۶ داریم $|X| = n$. در نتیجه $m \le n$. همچنین اگر $m = n$ باشد، چون $\{v_1, \dots, v_m\} \subseteq X$ و هر دو متناهی و هم‌اندازه‌اند، پس $\{v_1, \dots, v_m\} = X$ یک پایه است.

* **ب) (مینیمم تعداد مولدهای $V$ برابر $n$ است):**
  اگر $\{v_1, \dots, v_m\}$ یک مجموعه مولد $V$ باشد، آنگاه $n \le m$. به علاوه اگر $m = n$ باشد، آنگاه $\{v_1, \dots, v_m\}$ یک پایه $V$ است.

  * **برهان:** طبق قضیه ۲-۵ (نتیجه ۳-۵ ج)، یک پایه $X$ برای $V$ وجود دارد که $X \subseteq \{v_1, \dots, v_m\}$. طبق قضیه ۲-۶ داریم $|X| = n$، در نتیجه $n \le m$. اگر $m = n$ باشد، آنگاه $\{v_1, \dots, v_m\} = X$ یک پایه است.

# ۶-۶ قضیه (بُعد زیرفضا)

فرض کنید $V$ یک فضای برداری با بعد متناهی و $W$ یک زیرفضای $V$ باشد. در این صورت:

* **الف)** $W$ با بعد متناهی است و $\dim(W) \le \dim(V)$.

* **ب)** اگر $\dim(W) = \dim(V)$، آنگاه $W = V$.

**برهان:**

* **الف)** فرض کنید $X$ یک پایه $W$ باشد. در این صورت $X$ زیرمجموعه مستقل خطی از $W$ و در نتیجه مستقل خطی از $V$ است. لذا طبق ۵-۶ داریم $|X| \le \dim(V)$. از طرف دیگر داریم $|X| = \dim(W)$، پس $\dim(W) \le \dim(V)$.

* **ب)** فرض کنید $|X| = \dim(W) = \dim(V)$. چون $X$ مجموعه مستقل خطی در $V$ با اندازه $\dim(V)$ است، از ۵-۶ (الف) نتیجه می‌شود که $X$ یک پایه برای $V$ است. در نتیجه $\text{span}(X) = V$. از طرف دیگر چون $X$ پایه $W$ است داریم $\text{span}(X) = W$، در نتیجه $V = W$.

### مثال (زیرفضاهای $\mathbb{R}^3$ بر حسب بعد):

* **بعد صفر:** $\{0\}$ (مبدأ)

* **بعد یک:** خط‌های گذرنده از مبدأ

* **بعد دو:** صفحه‌های گذرنده از مبدأ

* **بعد سه:** $\mathbb{R}^3$

# ۳-۷ لم (خواص مقدماتی تبدیل خطی)

فرض کنید $T: V \to W$ یک تبدیل خطی باشد. در این صورت:

* **الف)** $T(0_V) = 0_W$

  * **برهان:**

$$
T(0_V + 0_V) = T(0_V) \stackrel{T \text{ خطی است}}{\Longrightarrow} T(0_V) + T(0_V) = T(0_V) = 0_W + T(0_V) \stackrel{\text{قانون حذفی}}{\Longrightarrow} T(0_V) = 0_W
$$

* **ب)** برای هر $v \in V$ داریم: $T(-v) = -T(v)$.

  * **برهان:**

$$
T(v + (-v)) = T(0_V) = 0_W \Longrightarrow T(v) + T(-v) = 0_W \stackrel{\text{یکتایی قرینه}}{\Longrightarrow} T(-v) = -T(v)
$$

* **ج)** برای هر $x_1, x_2 \in V$ و هر $\alpha, \beta \in F$ داریم: $T(\alpha x_1 + \beta x_2) = \alpha T(x_1) + \beta T(x_2)$.

  * **برهان:**

$$
T(\alpha x_1 + \beta x_2) \stackrel{\text{تعریف تبدیل خطی}}{=} T(\alpha x_1) + T(\beta x_2) \stackrel{\text{تعریف تبدیل خطی}}{=} \alpha T(x_1) + \beta T(x_2)
$$

* **د)** برای هر $x_1, \dots, x_n \in V$ و هر $\alpha_1, \dots, \alpha_n \in F$ داریم:

$$
T\left(\sum_{i=1}^{n} \alpha_i x_i\right) = \sum_{i=1}^{n} \alpha_i T(x_i)
$$

*(اثبات با استفاده از (ج) و استقرا روی $n$).*

# ۴-۷ لم

فرض کنید $T: V \to W$ یک تبدیل خطی باشد. در این صورت:

$$
T \text{ یک به یک است} \Longleftrightarrow T \text{ هر زیرمجموعه مستقل خطی از } V \text{ را به یک زیرمجموعه مستقل خطی از } W \text{ ببرد.}
$$

*(منظور این است که اگر $X \subseteq V$ مستقل خطی باشد، عناصر $T(x)$ به ازای $x \in X$ متمایز و در $W$ مستقل خطی هستند).*

**برهان:**
$(\Longrightarrow)$
فرض کنید $T$ یک به یک باشد و $X$ یک زیرمجموعه مستقل خطی از $V$ باشد. فرض کنید $y_1, \dots, y_t \in T(X)$ متمایز باشند و $\alpha_1, \dots, \alpha_t \in F$ به طوری که:

$$
\sum_{i=1}^{t} \alpha_i y_i = 0_W
$$

در این صورت عناصر متمایز $x_1, \dots, x_t$ متعلق به $X$ وجود دارند که $y_i = T(x_i)$ ($1 \le i \le t$). بنابراین داریم:

$$
\sum_{i=1}^{t} \alpha_i T(x_i) = 0_W \Longrightarrow T\left(\sum_{i=1}^{t} \alpha_i x_i\right) = T(0_V)
$$

$$
\stackrel{T \text{ یک به یک است}}{\Longrightarrow} \sum_{i=1}^{t} \alpha_i x_i = 0_V \stackrel{X \text{ مستقل خطی است}}{\Longrightarrow} \alpha_1 = \alpha_2 = \dots = \alpha_t = 0_F
$$

$(\Longleftarrow)$
**(برهان خلف):** فرض کنید $T$ یک به یک نباشد؛ پس $x_1, x_2 \in V$ متمایز ($x_1 \neq x_2$) وجود دارند به طوری که $T(x_1) = T(x_2)$.
در این صورت $x_1 - x_2 \neq 0_V$، پس مجموعه تک‌عضوی $\{x_1 + (-x_2)\}$ در $V$ مستقل خطی است *(توجه کنید اگر $v \neq 0_V$ آنگاه $\{v\}$ مستقل خطی است)*.
اما داریم:

$$
T(x_1 + (-x_2)) = T(x_1) - T(x_2) = 0_W
$$

و مجموعه $\{0_W\}$ در $W$ مستقل خطی نیست، که با فرض خلف تناقض دارد.

# ۵-۷ لم

فرض کنید $T: V \to W$ یک تبدیل خطی باشد و $v_1, \dots, v_n$ عناصری از $V$ باشند ($\{v_1, \dots, v_n\} \subseteq V$). در این صورت:

* **الف)** $T(\text{span}(\{v_1, \dots, v_n\})) = \text{span}(\{T(v_1), T(v_2), \dots, T(v_n)\})$.

* **ب)** اگر $V = \text{span}(\{v_1, \dots, v_n\})$، آنگاه $T(V) = \text{span}(\{T(v_1), \dots, T(v_n)\})$.
  *(به بیان دیگر: اگر $V = \text{span}(\{v_1, \dots, v_n\})$، آنگاه $T$ پوشا است $\Longleftrightarrow$ هر مجموعه مولد $V$ را به یک مجموعه مولد $W$ ببرد).*

**برهان:**

* **الف)**

$$
y \in T(\text{span}(\{v_1, \dots, v_n\})) \Longleftrightarrow \exists x \in \text{span}(\{v_1, \dots, v_n\}) : T(x) = y
$$

$$
\Longleftrightarrow \exists \alpha_1, \dots, \alpha_n \in F : T\left(\sum_{i=1}^{n} \alpha_i v_i\right) = y
$$

$$
\Longleftrightarrow \exists \alpha_1, \dots, \alpha_n \in F : \sum_{i=1}^{n} \alpha_i T(v_i) = y
$$

$$
\Longleftrightarrow y \in \text{span}(\{T(v_1), \dots, T(v_n)\})
$$

* **ب)** به راحتی از (الف) نتیجه می‌شود.

# ۶-۷ قضیه (قضیه اساسی وجود و یکتایی تبدیل خطی روی پایه)

فرض کنید $V$ و $W$ دو فضای برداری روی میدان $F$ باشند و فرض کنید $\{v_1, \dots, v_n\}$ پایه‌ای برای $V$ و $w_1, \dots, w_n$ بردارهایی دلخواه از $W$ باشند. در این صورت:

* **الف)** یک و تنها یک تبدیل خطی $T: V \to W$ وجود دارد که:

$$
T(v_i) = w_i \quad (1 \le i \le n)
$$

* **ب)** $T$ یک به یک است $\Longleftrightarrow$ $w_1, \dots, w_n$ متمایز و $\{w_1, \dots, w_n\}$ در $W$ مستقل خطی باشند.

* **ج)** $T$ پوشا است $\Longleftrightarrow$ $\text{span}(\{w_1, \dots, w_n\}) = W$.

* **د)** $T$ دو سویه (ایزومورفیسم) است $\Longleftrightarrow$ $\{w_1, \dots, w_n\}$ پایه‌ای برای $W$ است.

**برهان:**

* **الف)** تابع $T: V \to W$ را به صورت زیر تعریف می‌کنیم:

$$
T\left(\sum_{i=1}^{n} \alpha_i v_i\right) = \sum_{i=1}^{n} \alpha_i w_i
$$

  * **(اول: خوش‌تعریفی و خطی بودن):** فرض کنید $x = \sum_{i=1}^{n} \alpha_i v_i \in V$ و $x = \sum_{i=1}^{n} \beta_i v_i$. در این صورت مطابق قضیه ۴-۲ (یکتایی نمایش در پایه) داریم $\alpha_i = \beta_i$ ($1 \le i \le n$). بنابراین:

$$
\sum_{i=1}^{n} \alpha_i w_i = \sum_{i=1}^{n} \beta_i w_i
$$

پس $T$ خوش‌تعریف است (خطی بودن آن نیز به سادگی از تعریف نتیجه می‌شود).

  * **(دوم):** طبق تعریف برای هر $1 \le i \le n$ داریم $T(v_i) = T(1_F v_i) = 1_F w_i = w_i$.

  * **(سوم: یکتایی):** فرض کنید $U: V \to W$ یک تبدیل خطی باشد که $U(v_i) = w_i$ ($1 \le i \le n$). فرض کنید $x \in V$. در این صورت $\alpha_1, \dots, \alpha_n$ متعلق به $F$ وجود دارند به طوری که $x = \sum_{i=1}^{n} \alpha_i v_i$. داریم:

$$
U(x) = U\left(\sum_{i=1}^{n} \alpha_i v_i\right) \stackrel{U \text{ خطی است}}{=} \sum_{i=1}^{n} \alpha_i U(v_i) \stackrel{U(v_i) = w_i}{=} \sum_{i=1}^{n} \alpha_i w_i = T\left(\sum_{i=1}^{n} \alpha_i v_i\right) = T(x)
$$

پس $U = T$.

* **ب)**
  $(\Longrightarrow)$ چون $\{v_1, \dots, v_n\}$ مستقل خطی است و $T$ یک به یک است، بنابر لم ۴-۷ عناصر $T(v_1), \dots, T(v_n)$ متمایزند و مجموعه $\{T(v_1), \dots, T(v_n)\} = \{w_1, \dots, w_n\}$ در $W$ مستقل خطی است.

  $(\Longleftarrow)$ فرض کنید $x, y \in V$ به طوری که $T(x) = T(y)$. عناصر $\alpha_1, \dots, \alpha_n$ و $\beta_1, \dots, \beta_n$ متعلق به $F$ وجود دارند به طوری که $x = \sum_{i=1}^{n} \alpha_i v_i$ و $y = \sum_{i=1}^{n} \beta_i v_i$. در نتیجه:

$$
T\left(\sum_{i=1}^{n} \alpha_i v_i\right) = T\left(\sum_{i=1}^{n} \beta_i v_i\right) \Longrightarrow \sum_{i=1}^{n} \alpha_i T(v_i) = \sum_{i=1}^{n} \beta_i T(v_i)
$$

$$
\Longrightarrow \sum_{i=1}^{n} \alpha_i w_i = \sum_{i=1}^{n} \beta_i w_i \Longrightarrow \sum_{i=1}^{n} (\alpha_i - \beta_i) w_i = 0_W
$$

$$
\stackrel{\{w_1, \dots, w_n\} \text{ مستقل خطی}}{\Longrightarrow} \alpha_i = \beta_i \quad (1 \le i \le n) \Longrightarrow x = \sum_{i=1}^{n} \alpha_i v_i = \sum_{i=1}^{n} \beta_i v_i = y
$$

* **ج)**

$$
T \text{ پوشا است} \Longleftrightarrow T(V) = W \Longleftrightarrow T(\text{span}(\{v_1, \dots, v_n\})) = W
$$

$$
\stackrel{\text{لم ۵-۷}}{\Longleftrightarrow} \text{span}(\{T(v_1), \dots, T(v_n)\}) = W \Longleftrightarrow \text{span}(\{w_1, \dots, w_n\}) = W
$$

* **د)** از (ب) و (ج) به راحتی نتیجه می‌شود.

# ۷-۷ نتیجه

فرض کنید $V$ و $W$ دو فضای برداری روی میدان $F$ باشند و $V$ دارای پایه متناهی $\{v_1, \dots, v_n\}$ باشد. در این صورت هرگاه $T, U: V \to W$ دو تبدیل خطی باشند که:

$$
T(v_i) = U(v_i) \quad (1 \le i \le n)
$$

آنگاه $T = U$.

**برهان:** از قضیه ۶-۷ قسمت (الف) نتیجه می‌شود.

# ۸-۷ قضیه

فرض کنید $V$ و $W$ دو فضای برداری روی میدان $F$ با بعد متناهی باشند به طوری که $\dim(V) = \dim(W) = n$. فرض کنید $T: V \to W$ یک تبدیل خطی باشد. در این صورت احکام زیر معادل‌اند:

* **(i)** $T$ دو سویه است.

* **(ii)** $T$ یک به یک است.

* **(iii)** $T$ پوشا است.

* **(iv)** برای هر پایه $\{v_1, \dots, v_n\}$ از $V$، مجموعه $\{T(v_1), \dots, T(v_n)\}$ پایه‌ای برای $W$ است (و عناصر آن متمایزند).

* **(v)** پایه‌ای چون $\{v_1, \dots, v_n\}$ برای $V$ وجود دارد که $\{T(v_1), \dots, T(v_n)\}$ پایه‌ای برای $W$ است.

**برهان:**
ثابت می‌کنیم:

$$
(i) \Longrightarrow (ii) \Longrightarrow (iv) \Longrightarrow (v) \Longrightarrow (i) \quad \text{و همچنین} \quad (i) \Longrightarrow (iii) \Longrightarrow (iv) \Longrightarrow (iii)
$$

* **(i) $\Longrightarrow$ (ii):** واضح است.

* **(ii) $\Longrightarrow$ (iv):** فرض کنید $\{v_1, \dots, v_n\}$ یک پایه برای $V$ باشد؛ پس مستقل خطی است. چون $T$ یک به یک است، طبق ۶-۷ (ب)، عناصر $T(v_1), \dots, T(v_n)$ متمایزند و $\{T(v_1), \dots, T(v_n)\}$ در $W$ مستقل خطی است. چون $\dim(W) = n$ و این مجموعه $n$ عضو دارد، طبق نتیجه ۵-۶ (الف) مجموعه $\{T(v_1), \dots, T(v_n)\}$ یک پایه برای $W$ است.

* **(iv) $\Longrightarrow$ (v):** فضاهای برداری دارای پایه هستند؛ پس $V$ دارای یک پایه مانند $Y = \{v_1, \dots, v_n\}$ است. طبق فرض (iv)، مجموعه $\{T(v_1), \dots, T(v_n)\}$ یک پایه برای $W$ است.

* **(v) $\Longrightarrow$ (i):** مستقیماً از قضیه ۶-۷ قسمت (د) نتیجه می‌شود.

* **(i) $\Longrightarrow$ (iii):** واضح است.

* **(iii) $\Longleftrightarrow$ (iv):** فرض کنید $\{v_1, \dots, v_n\}$ پایه‌ای برای $V$ باشد؛ پس مولد $V$ است. داریم:

$$
T \text{ پوشا است و } \{v_1, \dots, v_n\} \text{ مولد } V \text{ است} \stackrel{\text{قضیه ۶-۷ (ج)}}{\Longleftrightarrow} \{T(v_1), \dots, T(v_n)\} \text{ مولد } W \text{ است}
$$

$$
\stackrel{\dim(W) = n \text{ و نتیجه ۵-۶ (ب)}}{\Longleftrightarrow} \{T(v_1), \dots, T(v_n)\} \text{ پایه‌ای برای } W \text{ است.}
$$