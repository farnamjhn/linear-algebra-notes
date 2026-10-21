این متنِ پیاده‌سازی‌شده و تصحیح‌شدهٔ جزوهٔ دترمینان (Determinant) در قالب مارک‌داون (Markdown) به همراه فرمول‌های ریاضی و ترجمهٔ انگلیسی اصطلاحات تخصصی ریاضی است:

  

  

  

## صفحه ۹۵

  

  

به ازای $n=2$، دترمینان (Determinant) هر ماتریس (Matrix) $2 \times 2$ به صورت زیر تعریف می‌شود:

  

$$\det\left(\begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}\right) = a_{11}a_{22} - a_{21}a_{12}$$

  

در هندسه دوبعدی (Two-dimensional Geometry) ثابت می‌شود که $\vert{}\det(A)\vert{}$ برابر است با مساحت (Area) متوازی‌الاضلاعی (Parallelogram) که بردارهای ستونی (Column Vectors) یا سطری $A$ یعنی $(a_{11}, a_{12})$ و $(a_{21}, a_{22})$ ضلع‌های مجاورش هستند.

  

می‌خواهیم از مثال‌های فوق، ویژگی‌هایی از دترمینان (Determinant) را استخراج کنیم که ما را در فرمول‌بندی تعریفی برای $\det(A)$، که در آن $A$ هر ماتریس مربعی (Square Matrix) دلخواه است، راهنمایی کند.

  

به این نکته توجه کنیم که دترمینان (Determinant) همواره یک تابع اسکالر مقدار (Scalar-valued Function) است که روی مجموعهٔ همهٔ ماتریس‌های (Matrices) $n \times n$ تعریف می‌شود؛ یعنی اگر $A$ هر ماتریس $n \times n$ باشد، $\det(A)$ یک اسکالر (Scalar) است.

  

ویژگی‌های زیر انتظارات معقولی هستند:

  

- **(الف)** اگر ضلعی از متوازی‌الاضلاعی (Parallelogram) را در اسکالر (Scalar) $k$ ضرب کنیم، مساحت (Area) آن در $k$ضرب می‌شود:
    
      
    
    $$\text{Area}\begin{pmatrix} ku \\ v \end{pmatrix} = k \cdot \text{Area}\begin{pmatrix} u \\ v \end{pmatrix} \quad \text{و همچنین} \quad \text{Area}\begin{pmatrix} u \\ kv \end{pmatrix} = k \cdot \text{Area}\begin{pmatrix} u \\ v \end{pmatrix}$$
    
      
    

  

  

## صفحه ۹۶

  

  

- **(ب)** مساحت $\begin{pmatrix} u \\ v_1 + v_2 \end{pmatrix}$ برابر با $\text{Area}\begin{pmatrix} u \\ v_1 \end{pmatrix} + \text{Area}\begin{pmatrix} u \\ v_2 \end{pmatrix}$ است. همچنین مساحت $\begin{pmatrix} u_1 + u_2 \\ v \end{pmatrix}$ برابر با $\text{Area}\begin{pmatrix} u_1 \\ v \end{pmatrix} + \text{Area}\begin{pmatrix} u_2 \\ v \end{pmatrix}$ است.
    
      
    
- **(ج)** همچنین $\text{Area}\begin{pmatrix} u \\ u \end{pmatrix}$ برابر صفر (Zero) است.
    
      
    
- **(د)** اگر $u=(1,0)$ و $v=(0,1)$، آنگاه $\text{Area}\begin{pmatrix} u \\ v \end{pmatrix}$ برابر یک است.
    
      
    

فرمول صریح (Explicit Formula) دترمینان (Determinant) ساده نیست، اما خواص آن ساده‌اند. این نقطهٔ طبیعیِ شروع کار است. دترمینان (Determinant) را می‌توان با سه خاصیت مقدماتی‌اش تعریف کرد:

  

1. $\det(I) = 1$ (که در آن $I$ ماتریس همانی (Identity Matrix) است).
    
      
    
2. وقتی دو سطر (Row) مساوی باشند، دترمینان (Determinant) صفر شود.
    
      
    
3. دترمینان (Determinant) نسبت به هر سطرش خطی (Linear) است.
    
      
    

نشان داده خواهد شد که تنها یک تابع (Function) $\det: M_{n \times n}(F) \to F$ با سه خاصیت بالا وجود دارد.

  

**۱۸-۱- تعریف (Definition):** تابع $\delta: M_{n \times n}(F) \to F$ را یک تابع $n$-خطی ($n$-linear Function / Multilinear Function) گوییم هرگاه به ازای هر $i$ ($1 \le i \le n$)، $\delta$ تابعی خطی (Linear Function) از سطر $i$-ام با ثابت نگه داشتن $(n-1)$ سطر دیگر باشد. به عبارت دیگر، برای هر $i$ داشته باشیم:

  

  

  

## صفحه ۹۷

  

  

$$\delta\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ u + kv \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix} = \delta\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ u \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix} + k\delta\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ v \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix}$$

  

که در آن $a_i$ها و $u, v$ بردارهایی (Vectors) در $F^n$ هستند و $k$ یک اسکالر (Scalar) است.

  

**۱۸-۲- مثال (Example):**

  

- **الف)** تابع صفر (Zero Function) $\delta: M_{n \times n}(F) \to F$ با ضابطهٔ $A \mapsto 0_F$ یک تابع $n$-خطی ($n$-linear Function) است.
    
      
    
- **ب)** برای هر $1 \le j \le n$، تابع زیر یک تابع $n$-خطی ($n$-linear Function) است:
    
      
    
    $$\delta_j: M_{n \times n}(F) \to F$$
    
      
    
    $$A \mapsto A_{1j}A_{2j}\dots A_{nj} \quad (\text{ضرب درایه‌های واقع در ستون } j\text{-ام ماتریس } A)$$
    
      
    
    **برهان (Proof):** فرض کنید $a_i = (a_{i1}, a_{i2}, \dots, a_{in})$ برای $i \ne k$ و $u = (b_1, b_2, \dots, b_n) \in F^n$ و $v = (c_1, c_2, \dots, c_n) \in F^n$ سطرهای ماتریس (Matrix Rows) $A$ باشند. در این صورت:
    
      
    
    $$\delta_j\begin{pmatrix} a_1 \\ \vdots \\ u + kv \\ \vdots \\ a_n \end{pmatrix} = A_{1j}\dots A_{k-1,j}(b_j + kc_j)A_{k+1,j}\dots A_{nj} = (A_{1j}\dots A_{k-1,j}b_j A_{k+1,j}\dots A_{nj}) + k(A_{1j}\dots A_{k-1,j}c_j A_{k+1,j}\dots A_{nj})$$
    
      
    

  

  

## صفحه ۹۸

  

  

$$= \delta_j\begin{pmatrix} a_1 \\ \vdots \\ u \\ \vdots \\ a_n \end{pmatrix} + k\delta_j\begin{pmatrix} a_1 \\ \vdots \\ v \\ \vdots \\ a_n \end{pmatrix}$$

  

- **ج)** تابع $\delta: M_{n \times n}(F) \to F$ با ضابطهٔ $A \mapsto A_{11}A_{22}\dots A_{nn}$ (ضرب درایه‌های واقع در قطر اصلی (Main Diagonal) ماتریس $A$) یک تابع $n$-خطی ($n$-linear Function) است.
    
      
    

**۱۸-۳- تعریف (Definition):** تابع $n$-خطی $\delta: M_{n \times n}(F) \to F$ را متناوب (Alternating) گوییم هرگاه برای هر $A \in M_{n \times n}(F)$ که دو سطر مجاور (Adjacent Rows) آن مساوی باشند، آنگاه $\delta(A) = 0$.

  

**۱۸-۴- قضیه (Theorem):** فرض کنید $\delta: M_{n \times n}(F) \to F$ یک تابع $n$-خطی متناوب (Alternating $n$-linear Function) باشد.

  

- **الف)** هرگاه $A \in M_{n \times n}(F)$ و $B$ ماتریسی باشد که از جابه‌جایی (Row Swap) دو سطر $A$ به دست آمده باشد، آنگاه $\delta(B) = -\delta(A)$.
    
      
    
- **ب)** اگر دو سطر از $A \in M_{n \times n}(F)$ مساوی باشند، آنگاه $\delta(A) = 0$. (توجه کنید: ۱۸-۴(ب) تعمیمی از تعریف ۱۸-۳ است).
    
      
    

**۱۸-۵- قضیه (Theorem):** فرض کنید $\delta: M_{n \times n}(F) \to F$ یک تابع $n$-خطی متناوب (Alternating $n$-linear Function) باشد که $\delta(I_n) = 1$. در این صورت برای هر $A \in M_{n \times n}(F)$ داریم:

  

$$\delta(A) = \sum_{\sigma \in S_n} \text{sgn}(\sigma) A_{1\sigma(1)}A_{2\sigma(2)}\dots A_{n\sigma(n)} \quad (*)$$

  

  

  

## صفحه ۹۹

  

  

که در آن $S_n$ مجموعهٔ توابع دوسویی (Bijective Functions / Bijections) از $\{1, 2, \dots, n\}$ به $\{1, 2, \dots, n\}$ است. عناصر $S_n$ را جایگشت (Permutation) می‌نامند.

  

حکم بنیادین در مورد جایگشت‌ها (Permutations) به شرح زیر است: اگر $\sigma \in S_n$، می‌توان از دنبالهٔ (Sequence) $(1, 2, \dots, n)$ با تعویض‌های متوالی از جفت‌ها (Transpositions) به دنبالهٔ $(\sigma(1), \sigma(2), \dots, \sigma(n))$ رسید. گرچه این امر می‌تواند به طرق گوناگون انجام شود، ولی بدون توجه به چگونگی انجام آن، تعداد تعویض‌های به کار رفته یا همواره زوج (Even) است یا همواره فرد (Odd). در این صورت جایگشت (Permutation) به ترتیب زوج یا فرد نامیده می‌شود.

  

علامت جایگشت (Sign of a Permutation) $\sigma$ توسط تابع زیر تعریف می‌شود:

  

$$\text{sgn}(\sigma) = \begin{cases} 1 & \text{هرگاه } \sigma \text{ زوج باشد (Even)} \\ -1 & \text{هرگاه } \sigma \text{ فرد باشد (Odd)} \end{cases}$$

  

در اینجا نماد $n!$ (فاکتوریل / Factorial) تعداد عناصر $S_n$ را نشان می‌دهد.

  

**۱۸-۶- تعریف (Definition):** تابع $\delta: M_{n \times n}(F) \to F$ را تابع دترمینان (Determinant Function) گویند هرگاه $n$-خطی ($n$-linear) و متناوب (Alternating) باشد و $\delta(I_n) = 1$. این تابع را با $\det$ نمایش می‌دهیم.

  

قضیهٔ ۱۸-۵ را نباید برای محاسبهٔ تابع $\det$ وقتی $n > 3$ به کار برد، زیرا از لحاظ محاسبه کارا (Efficient) نیست. ولی این قضیه مهم است؛ زیرا نشان می‌دهد که اگر تابع دترمینان (Determinant Function) برای ماتریس‌های $n \times n$ وجود داشته باشد، آنگاه تنها یک چنین تابعی وجود دارد (یکتایی / Uniqueness) و آن توسط فرمول $(*)$ مشخص می‌شود.

  

  

  

## صفحه ۱۰۰

  

  

در نتیجه، اگر وجود (Existence) تابع دترمینان (Determinant Function) را ثابت کنیم، مسئلهٔ یکتایی (Uniqueness) آن حل شده است. می‌توانیم ثابت کنیم که تابع دترمینان در حالت $n=1$ وجود دارد و حالت کلی را با استقرای ریاضی (Mathematical Induction) به دست می‌آوریم. فرض می‌کنیم یک تابع دترمینان برای ماتریس‌های $(n-1) \times (n-1)$ وجود دارد و با استفاده از آن، تابع دترمینان را برای ماتریس‌های $n \times n$ تعریف می‌کنیم.

  

**۱۸-۷- تعریف و نمادگذاری (Definition and Notation):** فرض کنید $n \ge 2$ و $A \in M_{n \times n}(F)$. ماتریس $(n-1) \times (n-1)$ که از حذف سطر $i$-ام و ستون $j$-ام به دست می‌آید (زیرماتریس / Submatrix) را با $\overline{A}_{ij}$ نشان می‌دهیم.

  

**مثال (Example):** اگر $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$ باشد، آنگاه:

  

$$\overline{A}_{11} = \begin{pmatrix} 5 & 6 \\ 8 & 9 \end{pmatrix}, \quad \overline{A}_{13} = \begin{pmatrix} 4 & 5 \\ 7 & 8 \end{pmatrix}, \quad \overline{A}_{32} = \begin{pmatrix} 1 & 3 \\ 4 & 6 \end{pmatrix}$$

  

و اگر $B = \begin{pmatrix} 1 & -1 & 2 & -1 \\ -3 & 4 & 1 & -1 \\ 2 & -5 & -3 & 8 \\ -2 & 6 & -4 & 1 \end{pmatrix}$باشد، آنگاه:

  

$$\overline{B}_{23} = \begin{pmatrix} 1 & -1 & -1 \\ 2 & -5 & 8 \\ -2 & 6 & 1 \end{pmatrix}, \quad \overline{B}_{42} = \begin{pmatrix} 1 & 2 & -1 \\ -3 & 1 & -1 \\ 2 & -3 & 8 \end{pmatrix}$$

  

**۱۸-۸- قضیه (Theorem):** فرض کنید $n \ge 2$ و $D: M_{(n-1) \times (n-1)}(F) \to F$ یک تابع $(n-1)$-خطی متناوب (Alternating $(n-1)$-linear Function) باشد. در این صورت، به ازای هر $j$ ($1 \le j \le n$)، تابع:

  

$$E_j: M_{n \times n}(F) \to F, \quad A \mapsto \sum_{i=1}^n (-1)^{i+j} A_{ij} D(\overline{A}_{ij})$$

  

یک تابع $n$-خطی متناوب است. اگر $D$ یک تابع دترمینان (Determinant Function) باشد، هر یک از $E_j$ها نیز یک تابع دترمینان است.

  

  

  

## صفحه ۱۰۱

  

  

**۱۸-۹- نتیجه (Corollary):** فرض کنید $n$ عدد صحیح مثبت (Positive Integer) باشد. در این صورت حداقل یک تابع دترمینان $\det: M_{n \times n}(F) \to F$ وجود دارد.

  

**برهان (Proof):** تابع $D: M_{1 \times 1}(F) \to F$ با ضابطهٔ $A=(a) \mapsto a$ یک تابع دترمینان است. قضیهٔ ۱۸-۸ به وضوح نشان می‌دهد که با در دست داشتن یک تابع دترمینان روی ماتریس‌های $(n-1) \times (n-1)$ چگونه می‌توان یک تابع دترمینان روی ماتریس‌های $n \times n$ را ساخت. حال اثبات این نتیجه با استقرا (Induction) تکمیل می‌شود.

  

**۱۸-۱۰- مثال (Example):**

  

- **الف)** فرض کنید $A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}$. در این صورت:
    
      
    
    $$\det(A) = (-1)^{1+1} a_{11} \det(\overline{A}_{11}) + (-1)^{2+1} a_{21} \det(\overline{A}_{21}) = a_{11}a_{22} - a_{21}a_{12}$$
    
      
    
- **ب)** فرض کنید $A = \begin{pmatrix} A_{11} & A_{12} & A_{13} \\ A_{21} & A_{22} & A_{23} \\ A_{31} & A_{32} & A_{33} \end{pmatrix}$. در این صورت (بسط لاپلاس روی ستون‌ها / Cofactor Expansion along Columns):
    
      
    
    $$E_1(A) = A_{11} \begin{vmatrix} A_{22} & A_{23} \\ A_{32} & A_{33} \end{vmatrix} - A_{21} \begin{vmatrix} A_{12} & A_{13} \\ A_{32} & A_{33} \end{vmatrix} + A_{31} \begin{vmatrix} A_{12} & A_{13} \\ A_{22} & A_{23} \end{vmatrix}$$
    
      
    

  

  

## صفحه ۱۰۲

  

  

$$E_2(A) = -A_{12} \begin{vmatrix} A_{21} & A_{23} \\ A_{31} & A_{33} \end{vmatrix} + A_{22} \begin{vmatrix} A_{11} & A_{13} \\ A_{31} & A_{33} \end{vmatrix} - A_{32} \begin{vmatrix} A_{11} & A_{13} \\ A_{21} & A_{23} \end{vmatrix}$$

  

$$E_3(A) = A_{13} \begin{vmatrix} A_{21} & A_{22} \\ A_{31} & A_{32} \end{vmatrix} - A_{23} \begin{vmatrix} A_{11} & A_{12} \\ A_{31} & A_{32} \end{vmatrix} + A_{33} \begin{vmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{vmatrix}$$

  

از قضیهٔ ۱۸-۸ نتیجه می‌شود که $E_1, E_2, E_3$ توابع دترمینان (Determinant Functions) هستند. از قضیهٔ ۱۸-۵ نتیجه می‌شود که $E_1 = E_2 = E_3 = \det$.

  

- **ج)** فرض کنید:
    
      
    
    $$C = \begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ -2 & -3 & -5 & 2 \\ 4 & -4 & 4 & -6 \end{pmatrix}$$
    
      
    
    در این صورت (بسط روی ستون اول):
    
      
    
    $$\begin{aligned} \det(C) &= (-1)^{1+1}(2)\det(\overline{C}_{11}) + (-1)^{2+1}(0)\det(\overline{C}_{21}) + (-1)^{3+1}(-2)\det(\overline{C}_{31}) + (-1)^{4+1}(4)\det(\overline{C}_{41}) \\ &= (-1)^2 \times 2 \times \det\begin{pmatrix} 1 & 3 & -3 \\ -3 & -5 & 2 \\ -4 & 4 & -6 \end{pmatrix} + (-1)^3 \times 0 \times \det\begin{pmatrix} 0 & 0 & 1 \\ -3 & -5 & 2 \\ -4 & 4 & -6 \end{pmatrix} \\ &\quad + (-1)^4 \times (-2) \times \det\begin{pmatrix} 0 & 0 & 1 \\ 1 & 3 & -3 \\ -4 & 4 & -6 \end{pmatrix} + (-1)^5 \times 4 \times \det\begin{pmatrix} 0 & 0 & 1 \\ 1 & 3 & -3 \\ -3 & -5 & 2 \end{pmatrix} \end{aligned}$$
    
      
    
    روی هر ستون (Column) دیگر نیز می‌توانست عملیات انجام گیرد.
    
      
    

  

  

## صفحه ۱۰۳

  

  

**۱۸-۱۱- قضیه (Theorem):** فرض کنید $A = (A_{ij}) \in M_{n \times n}(F)$. در این صورت برای هر $i$ ($1 \le i \le n$) داریم (بسط دترمینان روی سطر $i$-ام / Cofactor Expansion along the $i$-th Row):

  

$$\det(A) = \sum_{j=1}^n (-1)^{i+j} A_{ij} \det(\overline{A}_{ij})$$

  

**۱۸-۱۲- مثال (Example):**

  

- **الف)** فرض کنید:
    
      
    
    $$C = \begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ -2 & -3 & -5 & 2 \\ 4 & -4 & 4 & -6 \end{pmatrix}$$
    
      
    
    در این صورت (بسط روی سطر اول):
    
      
    
    $$\begin{aligned} \det(C) &= (-1)^2 \times 2 \times \det(\overline{C}_{11}) + (-1)^3 \times 0 \times \det(\overline{C}_{12}) + (-1)^4 \times 0 \times \det(\overline{C}_{13}) + (-1)^5 \times 1 \times \det(\overline{C}_{14}) \\ &= (-1)^2 \times 2 \times \det\begin{pmatrix} 1 & 3 & -3 \\ -3 & -5 & 2 \\ -4 & 4 & -6 \end{pmatrix} + (-1)^3 \times 0 \times \det\begin{pmatrix} 0 & 3 & -3 \\ -2 & -5 & 2 \\ 4 & 4 & -6 \end{pmatrix} \\ &\quad + (-1)^4 \times 0 \times \det\begin{pmatrix} 0 & 1 & -3 \\ -2 & -3 & 2 \\ 4 & -4 & -6 \end{pmatrix} + (-1)^5 \times 1 \times \det\begin{pmatrix} 0 & 1 & 3 \\ -2 & -3 & -5 \\ 4 & -4 & 4 \end{pmatrix} \end{aligned}$$
    
      
    
    عملیات روی هر سطر دیگر نیز می‌توانست انجام شود.
    
      
    
- **ب) انتخاب هوشمندانهٔ سطر یا ستون:** فرض کنید:
    
      
    
    $$A = \begin{pmatrix} 1 & 0 & 0 & -1 \\ 3 & 1 & 2 & 2 \\ 1 & 0 & -2 & 1 \\ 2 & 0 & 0 & 1 \end{pmatrix}$$
    
      
    
    برای پیدا کردن $\det(A)$ راحت‌تر است که روی ستون دوم عمل کنیم، زیرا بیشترین صفر (Zero) روی این ستون قرار دارد.
    
      
    

  

  

## صفحه ۱۰۴

  

  

$$\det(A) = (-1)^{2+2} \times 1 \times \det\begin{pmatrix} 1 & 0 & -1 \\ 1 & -2 & 1 \\ 2 & 0 & 1 \end{pmatrix} = (-1)^{2+2} \times (-2) \times \det\begin{pmatrix} 1 & -1 \\ 2 & 1 \end{pmatrix} = -2(1 - (-2)) = -6$$

  

محاسبهٔ دترمینان (Determinant) با روش‌های بالا حتی برای ماتریس‌های با ابعاد کوچک بسیار سخت است. در آینده روش مؤثرتری برای محاسبهٔ دترمینان خواهیم گفت. بدین منظور باید اطلاعات بیشتری از آن داشته باشیم.

  

**۱۸-۱۳- خواص دترمینان (Properties of Determinants):**

  

- **(الف)** فرض کنید $u, v, a_1, \dots, a_n$ بردارهایی (Vectors) از $F^n$ باشند و $k$ یک اسکالر (Scalar) باشد. در این صورت برای هر $i$ داریم:
    
      
    
    $$\det\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ u + kv \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix} = \det\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ u \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix} + k\det\begin{pmatrix} a_1 \\ \vdots \\ a_{i-1} \\ v \\ a_{i+1} \\ \vdots \\ a_n \end{pmatrix}$$
    
      
    
- **(ب)** فرض کنید $A \in M_{n \times n}(F)$ به طوری که یک سطر (یا یک ستون) صفر (Zero Row/Column) دارد. در این صورت $\det(A) = 0$.
    
      
    
- **(ج)** فرض کنید $A \in M_{n \times n}(F)$ به طوری که دارای دو سطر (یا دو ستون) مساوی باشد. در این صورت $\det(A) = 0$.
    
      
    
- **(د)** فرض کنید $A \in M_{n \times n}(F)$ و $B$ ماتریس به دست آمده از $A$ به وسیلهٔ تعویض دو سطر (یا دو ستون) باشد. در این صورت $\det(B) = -\det(A)$.
    
      
    

  

  

## صفحه ۱۰۵

  

  

- **(هـ)** فرض کنید $A, B \in M_{n \times n}(F)$. در این صورت (خاصیت ضربی دترمینان / Multiplicative Property):
    
      
    
    $$\det(AB) = \det(A)\det(B)$$
    
      
    
- **(و)** برای هر ماتریس $A \in M_{n \times n}(F)$ داریم (دترمینان ترانهادهٔ ماتریس / Determinant of a Transpose):
    
      
    
    $$\det(A^t) = \det(A)$$
    
      
    

**۱۸-۱۴- کاربردهای دترمینان (Applications of Determinants):**

  

- **(الف)** فرض کنید $A \in M_{n \times n}(F)$.
    
      
    - **(i) تعریف (Definition):** ماتریس
        
          
        
        $$C = \begin{bmatrix} c_{11} & c_{12} & \dots & c_{1n} \\ c_{21} & c_{22} & \dots & c_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ c_{n1} & c_{n2} & \dots & c_{nn} \end{bmatrix}$$
        
          
        
        که در آن $c_{ij} = (-1)^{i+j}\det(\overline{A}_{ij})$ را ماتریس همسازه‌های (Cofactor Matrix) $A$ می‌نامند. ترانهادهٔ آن یعنی ماتریس $C^t$ را ماتریس الحاقی (Adjugate Matrix / Classical Adjoint) $A$ می‌نامند و با $\text{adj}(A)$نشان می‌دهند.
        
          
        
    - **(ii)** ضرب $A \cdot \text{adj}(A)$ را در نظر بگیرید:
        
          
        
        $$A \cdot \text{adj}(A) = \begin{pmatrix} a_{11} & a_{12} & \dots & a_{1n} \\ \vdots & \vdots & & \vdots \\ a_{i1} & a_{i2} & \dots & a_{in} \\ \vdots & \vdots & & \vdots \\ a_{n1} & a_{n2} & \dots & a_{nn} \end{pmatrix} \begin{pmatrix} c_{11} & \dots & c_{j1} & \dots & c_{n1} \\ c_{12} & \dots & c_{j2} & \dots & c_{n2} \\ \vdots & & \vdots & & \vdots \\ c_{1n} & \dots & c_{jn} & \dots & c_{nn} \end{pmatrix}$$
        
          
        
        درایهٔ (Entry) حاصل از ضرب سطر $i$-ام در ستون $j$-ام عبارت است از:
        
          
        

  

  

## صفحه ۱۰۶

  

  

$$a_{i1}c_{j1} + a_{i2}c_{j2} + \dots + a_{in}c_{jn}$$

  

دو حالت داریم:

  

- **حالت اول ($i = j$):** در این صورت عبارت بالا برابر است با $a_{i1}c_{i1} + a_{i2}c_{i2} + \dots + a_{in}c_{in}$ که طبق قضیهٔ ۱۸-۱۱ برابر $\det(A)$ است.
    
      
    
- **حالت دوم ($i \ne j$):** در این صورت عبارت بالا برابر دترمینان ماتریس زیر است (که در آن سطر $i$-ام و سطر $j$-ام هر دو برابر $(a_{i1}, a_{i2}, \dots, a_{in})$ هستند):
    
      
    
    $$\begin{matrix} \text{سطر } i\text{-ام} \to \\ \text{سطر } j\text{-ام} \to \end{matrix} \begin{pmatrix} a_{11} & a_{12} & \dots & a_{1n} \\ \vdots & \vdots & & \vdots \\ a_{i1} & a_{i2} & \dots & a_{in} \\ \vdots & \vdots & & \vdots \\ a_{i1} & a_{i2} & \dots & a_{in} \\ \vdots & \vdots & & \vdots \\ a_{n1} & a_{n2} & \dots & a_{nn} \end{pmatrix}$$
    
      
    
    در نتیجه طبق ۱۸-۱۳(ج) عبارت بالا برابر صفر است. بنابراین:
    
      
    
    $$A \cdot \text{adj}(A) = \begin{pmatrix} \det(A) & 0 & \dots & 0 \\ 0 & \det(A) & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & \det(A) \end{pmatrix} = \det(A) I_n$$
    
      
    
- **(ب)** فرض کنید $A \in M_{n \times n}(F)$. در این صورت:
    
      
    - **(i)** هرگاه $A$ وارون‌پذیر (Invertible) باشد، آنگاه $\det(A) \ne 0$ و $\det(A^{-1}) = (\det(A))^{-1}$.
        
          
        
    - **(ii)** اگر $\det(A) \ne 0$، آنگاه $A$ وارون‌پذیر (Invertible) است و وارون ماتریس (Matrix Inverse) برابر است با:
        
          
        
        $$A^{-1} = \frac{1}{\det(A)} \text{adj}(A)$$
        
          
        

  

  

## صفحه ۱۰۷

  

  

**برهان (Proof):**

  

- **(i)** با توجه به ۱۸-۱۳(هـ) داریم:
    
      
    
    $$AA^{-1} = I_n \implies \det(AA^{-1}) = \det(I_n) \implies \det(A)\det(A^{-1}) = 1$$
    
      
    
    $$\implies \det(A) \ne 0 \quad \text{و} \quad \det(A^{-1}) = \frac{1}{\det(A)}$$
    
      
    
- **(ii)** از رابطهٔ $A \cdot \text{adj}(A) = \det(A)I_n$ به دست می‌آید که:
    
      
    
    $$A \left( \frac{1}{\det(A)} \text{adj}(A) \right) = I_n$$
    
      
    
    در نتیجه $A$ وارون‌پذیر است و $A^{-1} = \frac{1}{\det(A)}\text{adj}(A)$.
    
      
    
- **(iii) مثال (Example):** ماتریس روبه‌رو را در نظر بگیرید:
    
      
    
    $$A = \begin{bmatrix} 3 & 2 & -1 \\ 1 & 6 & 3 \\ 2 & -4 & 0 \end{bmatrix}$$
    
      
    
    همسازه‌های (Cofactors) ماتریس $A$ عبارت‌اند از:
    
      
    
    $$\begin{cases} c_{11} = 12, & c_{12} = 6, & c_{13} = -16 \\ c_{21} = 4, & c_{22} = 2, & c_{23} = 16 \\ c_{31} = 12, & c_{32} = -10, & c_{33} = 16 \end{cases}$$
    
      
    
    در نتیجه ماتریس الحاقی (Adjugate Matrix) برابر است با:
    
      
    
    $$\text{adj}(A) = \begin{bmatrix} 12 & 4 & 12 \\ 6 & 2 & -10 \\ -16 & 16 & 16 \end{bmatrix}$$
    
      
    

  

  

## صفحه ۱۰۸

  

  

یک روش برای محاسبهٔ دترمینان (Determinant) ارائه می‌کنیم که محاسبهٔ کمتری از بسط همسازه‌ها (Cofactor Expansion) دارد. ایدهٔ این روش این است که با اعمال سطری مقدماتی (Elementary Row Operations) ماتریس داده شده را به یک ماتریس بالامثلثی (Upper Triangular Matrix) تبدیل کنیم و دترمینان ماتریس بالامثلثی را به دست آوریم (که به راحتی به دست می‌آید) و سپس ارتباط آن را با دترمینان ماتریس اصلی بیان کنیم. قبل از آن باید بدانیم که اعمال سطری مقدماتی چه اثری روی دترمینان می‌گذارند.

  

**۱۸-۱۵- قضیه (Theorem):** فرض کنید $A = (a_{ij}) \in M_{n \times n}(F)$ یک ماتریس پایین‌مثلثی (Lower Triangular Matrix) یا بالامثلثی (Upper Triangular Matrix) باشد. در این صورت، دترمینان برابر است با حاصل‌ضرب درایه‌های قطر اصلی (Main Diagonal Entries):

  

$$\det(A) = a_{11} \times a_{22} \times \dots \times a_{nn}$$

  

**مثال (Example):** (برای یک ماتریس پایین‌مثلثی $4 \times 4$):

  

$$\det\begin{pmatrix} a_{11} & 0 & 0 & 0 \\ a_{21} & a_{22} & 0 & 0 \\ a_{31} & a_{32} & a_{33} & 0 \\ a_{41} & a_{42} & a_{43} & a_{44} \end{pmatrix} = a_{11}a_{22}\det\begin{pmatrix} a_{33} & 0 \\ a_{43} & a_{44} \end{pmatrix} = a_{11}a_{22}a_{33}a_{44}$$

  

**۱۸-۱۶- قضیه (Theorem):** فرض کنید $A \in M_{n \times n}(F)$.

  

- **الف)** اگر $B$ از تعویض دو سطر (یا ستون) (Row/Column Swap) ماتریس $A$ به دست آید، آنگاه $\det(B) = -\det(A)$.
    
      
    
- **ب)** اگر $B$ از ضرب یک سطر (یا ستون) (Row/Column Scaling) ماتریس $A$ در یک اسکالر ناصفر (Non-zero Scalar) $\alpha$ به دست آید، آنگاه $\det(B) = \alpha\det(A)$.
    
      
    
- **ج)** اگر $B$ از جمع مضربی از یک سطر (یا ستون) به سطر (یا ستون) دیگر (Row/Column Addition) ماتریس $A$ به دست آید، آنگاه $\det(B) = \det(A)$.
    
      
    

  

  

## صفحه ۱۰۹

  

  

**۱۸-۱۷- روش محاسبهٔ دترمینان (Method for Computing Determinants):** برای محاسبهٔ دترمینان به روش زیر عمل می‌کنیم:

  

1. با استفاده از اعمال سطری مقدماتی (Elementary Row Operations) ماتریس را به یک ماتریس بالامثلثی (Upper Triangular Matrix) تبدیل می‌کنیم.
    
      
    
2. دترمینان ماتریس بالامثلثی را محاسبه می‌کنیم (عناصر روی قطر اصلی را در هم ضرب می‌کنیم).
    
      
    
3. با استفاده از قضیهٔ ۱۸-۱۶ دترمینان ماتریس داده شده را به دست می‌آوریم.
    
      
    

**مثال ۱ (Example 1):**

  

$$\begin{aligned} \det\begin{pmatrix} 0 & 2 & -4 & 5 \\ 2 & -2 & -5 & 4 \\ 0 & 1 & 4 & 1 \\ -2 & 4 & 2 & 8 \end{pmatrix} &\xrightarrow[\text{(نوع سوم: } R_4 + R_2 \to R_4\text{)}]{\text{عمل سطری مقدماتی}} \det\begin{pmatrix} 0 & 2 & -4 & 5 \\ 2 & -2 & -5 & 4 \\ 0 & 1 & 4 & 1 \\ 0 & 2 & -3 & 12 \end{pmatrix} \\ &\xrightarrow[\text{(نوع اول: } R_1 \leftrightarrow R_2\text{)}]{\text{عمل سطری مقدماتی}} -\det\begin{pmatrix} 2 & -2 & -5 & 4 \\ 0 & 2 & -4 & 5 \\ 0 & 1 & 4 & 1 \\ 0 & 2 & -3 & 12 \end{pmatrix} \\ &\xrightarrow[\text{(نوع اول: } R_2 \leftrightarrow R_3\text{)}]{\text{عمل سطری مقدماتی}} \det\begin{pmatrix} 2 & -2 & -5 & 4 \\ 0 & 1 & 4 & 1 \\ 0 & 2 & -4 & 5 \\ 0 & 2 & -3 & 12 \end{pmatrix} \\ &\xrightarrow[\text{(نوع سوم: } R_3 - 2R_2, \, R_4 - 2R_2\text{)}]{\text{اعمال سطری مقدماتی}} \det\begin{pmatrix} 2 & -2 & -5 & 4 \\ 0 & 1 & 4 & 1 \\ 0 & 0 & -12 & 3 \\ 0 & 0 & -11 & 10 \end{pmatrix} \end{aligned}$$

  

(نکته: در خط آخرِ دست‌نویس، سطرها دوباره جابه‌جا و ساده شده‌اند تا ماتریس کاملاً بالامثلثی شود و حاصل‌ضرب قطر اصلی محاسبه گردد).

  

  

  

## صفحه ۱۱۰

  

  

**مثال ۲ (Example 2):** (محاسبهٔ دترمینان ماتریس $C$ از صفحات قبل با روش کاهش سطری / Row Reduction):

  

$$\begin{aligned} \det\begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ -2 & -3 & -5 & 2 \\ 4 & -4 & 4 & -6 \end{pmatrix} &\xrightarrow[\text{(نوع سوم: } R_3 + R_1, \, R_4 - 2R_1\text{)}]{\text{اعمال سطری مقدماتی}} \det\begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ 0 & -3 & -5 & 3 \\ 0 & -4 & 4 & -8 \end{pmatrix} \\ &\xrightarrow[\text{(نوع سوم: } R_3 + 3R_2, \, R_4 + 4R_2\text{)}]{\text{اعمال سطری مقدماتی}} \det\begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ 0 & 0 & 4 & -6 \\ 0 & 0 & 16 & -20 \end{pmatrix} \\ &\xrightarrow[\text{(نوع سوم: } R_4 - 4R_3\text{)}]{\text{عمل سطری مقدماتی}} \det\begin{pmatrix} 2 & 0 & 0 & 1 \\ 0 & 1 & 3 & -3 \\ 0 & 0 & 4 & -6 \\ 0 & 0 & 0 & 4 \end{pmatrix} \\ &= 2 \times 1 \times 4 \times 4 = 32 \end{aligned}$$