# Решения к теме 12

## Создание таблиц

```sql
CREATE TABLE orders (
    order_id INT,
    user_id  INT,
    city     TEXT,
    amount   INT,
    promo    TEXT
);

INSERT INTO orders VALUES
(1, 10, 'Москва', 500, 'SALE'),
(2, 10, 'Москва', 300, NULL),
(3, 20, 'Казань', 700, 'SALE'),
(4, 30, 'Москва', NULL, NULL),
(5, 20, 'Казань', 200, 'VIP'),
(6, 40, 'Сочи',   150, NULL);

CREATE TABLE users (user_id INT);
INSERT INTO users VALUES (10), (20), (30), (40), (50);

CREATE TABLE blocked_users (user_id INT);
INSERT INTO blocked_users VALUES (30), (NULL);
```

---

## Задача 1

```sql
SELECT user_id, COUNT(*) AS orders_cnt, COUNT(promo) AS promo_cnt, SUM(amount) AS revenue
FROM orders
GROUP BY user_id
HAVING COUNT(*) >= 2
ORDER BY revenue DESC;
```

---

## Задача 2

```sql
-- (а) заказы, у которых сумма со скидкой 20% больше 300
SELECT order_id, amount * 0.8 AS discounted
FROM orders
WHERE amount * 0.8 > 300;

-- (б) для каждого города — сколько в нём разных покупателей
SELECT city, COUNT(DISTINCT user_id)
FROM orders
GROUP BY city;

-- (в) города с выручкой больше 500
SELECT city, SUM(amount) AS revenue
FROM orders
GROUP BY city
HAVING SUM(amount) > 500;

-- (г) города, где хотя бы 2 заказа
SELECT city, COUNT(*) AS cnt
FROM orders
GROUP BY city
HAVING COUNT(*) >= 2;
```

---

## Задача 3

```sql
SELECT
    COUNT(*)                 AS total_orders,
    COUNT(amount)            AS known_amount,
    COUNT(promo)             AS with_promo,
    COUNT(DISTINCT promo)    AS promo_kinds,
    COUNT(DISTINCT user_id)  AS buyers,
    AVG(amount)              AS avg_known,
    AVG(COALESCE(amount, 0)) AS avg_all
FROM orders;
```

---

## Задача 4

Способ 1: убрать NULL из подзапроса.

```sql
SELECT user_id
FROM users
WHERE user_id NOT IN (SELECT user_id FROM blocked_users WHERE user_id IS NOT NULL);
```

Способ 2: `NOT EXISTS`.

```sql
SELECT user_id
FROM users
WHERE NOT EXISTS (SELECT 1 FROM blocked_users WHERE users.user_id = blocked_users.user_id);
```

---

## Задача 5

```python
def sql_eq(a, b):          # сравнение a = b по правилам SQL
    if a == None or b == None:
        return None
    else:
        return a == b
def sql_not(a):            # NOT
    if a == None:
        return None
    return not a

def sql_and(a, b):         # AND
    if a is not None and b is not None:
        return a and b
    if a is None:
        a, b = b, a        # неизвестное теперь в b
    with_true, with_false = a and True, a and False
    return with_true if with_true == with_false else None
def sql_or(a, b):          # OR
    if a is not None and b is not None:
        return a or b
    if a is None:
        a, b = b, a
    with_true, with_false = a or True, a or False
    return with_true if with_true == with_false else None
def sql_not_in(x, values): # x NOT IN (values)
    result = True
    for v in values:
        result = sql_and(result, sql_not(sql_eq(x, v)))
    return result
def where_filter(rows, cond):  # оставить элементы rows, для которых cond(элемент) вернула True
    return [row for row in rows if cond(row) is True]
```

---

## Задача 6

Заказы: Москва — 500, 300, NULL; Казань — 700, 200; Сочи — 150.

### Порог 250

**Запрос А** (сначала WHERE, потом раскладка):

1. `WHERE amount > 250` проверяет каждую строку: 500 — проходит, 300 — проходит, NULL — UNKNOWN, выброшена, 700 — проходит, 200 — выброшена, 150 — выброшена.
2. Остались заказы 1, 2, 3. Кучки: Москва = 500 + 300 = 800, Казань = 700.

**Запрос Б** (сначала раскладка, потом HAVING):

1. Кучки по всем строкам: Москва = 500 + 300 (NULL игнорируется в SUM) = 800, Казань = 700 + 200 = 900, Сочи = 150.
2. `HAVING SUM(amount) > 250`: Москва 800 — проходит, Казань 900 — проходит, Сочи 150 — выброшена.

| | А | Б |
|---|---|---|
| Москва | 800 | 800 |
| Казань | **700** | **900** |

### Почему на 180 совпало

На пороге 180 WHERE выбросил только заказ Сочи (150) и NULL-строку Москвы. Заказ на 150 был единственным в своей кучке, поэтому в Б эту кучку выкинул HAVING (150 < 180). NULL в сумму всё равно не входит. Состав кучек Москвы и Казани не изменился, значит суммы те же.

### Что делает запросы разными

WHERE работает до раскладки и меняет состав кучек: выброшенные заказы не попадают в сумму. HAVING работает после раскладки и состав не меняет, он только выкидывает кучки целиком по итогу агрегата. Запросы совпадают лишь тогда, когда WHERE выбрасывает только целые кучки (или строки, не влияющие на сумму).

### Свой порог: 350

**А:** `amount > 350` оставляет 500 (Москва) и 700 (Казань). WHERE выбросил 300 в Москве и 200 в Казани.

**Б:** суммы 800, 900, 150, порог проходят Москва и Казань.

| city | А | Б |
|---|--:|--:|
| Москва | 500 | 800 |
| Казань | 700 | 900 |

---

## Задача 7

### (а)

Запрос коллеги вернёт **пустой результат**: `promo = NULL` всегда даёт UNKNOWN, ни одна строка не проходит.

```sql
SELECT order_id FROM orders WHERE promo IS NULL;   -- 2, 4, 6
```

### (б)

Запрос коллеги вернёт 1, 3, 5, 6: для заказа 4 `NULL <> 300` — UNKNOWN, строка пропадает.

```sql
SELECT order_id FROM orders WHERE amount <> 300 OR amount IS NULL;   -- 1, 3, 4, 5, 6
```

### (в)

Условие не всегда истинно. Запрос коллеги вернёт 5: у заказа 4 оба сравнения UNKNOWN, а `UNKNOWN OR UNKNOWN` — UNKNOWN, строка пропадает.

```sql
SELECT COUNT(*) FROM orders WHERE amount > 250 OR amount <= 250 OR amount IS NULL;   -- 6
```

### Вслух: почему `GROUP BY promo` собирает 2, 4, 6 в одну кучку

Стандарт для `GROUP BY` и `DISTINCT` считает NULL «не различимыми» между собой (not distinct), хотя `NULL = NULL` в WHERE даёт UNKNOWN. Для раскладки по кучкам и удаления повторов действует это правило, а не оператор `=`.

---

## Задача 8

### 1. Что вернёт запрос коллеги

- **PostgreSQL:** NULL считается больше любого значения, поэтому при `DESC` стоит первым. Результат: заказ 4 (NULL), 3 (700), 1 (500). Нужных трёх заказов нет.
- **MySQL:** NULL считается меньше любого значения, при `DESC` оказывается в конце. Результат: 3 (700), 1 (500), 2 (300).

Разница в том, что СУБД по-разному решают, где NULL в порядке сортировки.

### 2–3. Правильные запросы (PostgreSQL)

Способ 1: явно поставить NULL в конец.

```sql
SELECT order_id, amount
FROM orders
ORDER BY amount DESC NULLS LAST, order_id
LIMIT 3;
```

Способ 2: выкинуть NULL до сортировки.

```sql
SELECT order_id, amount
FROM orders
WHERE amount IS NOT NULL
ORDER BY amount DESC, order_id
LIMIT 3;
```

Второй ключ `order_id` разрешает ничью: при равных суммах выше стоит заказ с меньшим номером.

### 4. Вслух

- Для **всего списка** без `LIMIT`: в способе 1 заказ 4 с неизвестной суммой остаётся в конце списка, в способе 2 его в результате нет совсем.
- `LIMIT` без `ORDER BY` опасен тем, что без явной сортировки порядок строк не гарантирован: какие именно строки попадут в «первые N», зависит от плана запроса и может меняться между запусками.
