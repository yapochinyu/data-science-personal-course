задача 1

```sql
SELECT u.user_id, u.name
FROM users AS u
LEFT JOIN orders AS o
	ON u.user_id = o.user_id
WHERE o.order_Id IS NULL
ORDER BY u.user_id
```

задача 2

```sql
SELECT u.user_id, u.name, COALESCE(COUNT(o.amount > 1000), 0), COALESCE(SUM(o.amount), 0)
FROM users AS u
LEFT JOIN orders AS o
	ON u.user_id = o.user_id
    AND o.amount > 1000
GROUP BY u.user_id, u.name
ORDER BY u.user_id
```

задача 3

| значение ключа | строк слева | строк справа | пар |
|---|---|---|---|
| 1 | 3 | 2 | 3 × 2 = 6 |
| 2 | 1 | 0 | 0 |
| 3 | 0 | 1 | 0 |
| NULL | 1 | 1 | 0 |
| **итого** | 5 | 4 | 6 |

Строки без пары: слева — `2` и `NULL` (2 строки), справа — `3` и `NULL` (2 строки).

| JOIN | расчёт | строк |
|---|---|---|
| INNER | только пары: 6 | 6 |
| LEFT | 6 пар + 2 левые без пары (`2`, `NULL`) | 8 |
| RIGHT | 6 пар + 2 правые без пары (`3`, `NULL`) | 8 |
| FULL | 6 пар + 2 левые + 2 правые без пары | 10 |
| CROSS | 5 × 4, условия нет | 20 |

Почему каждая из трёх единиц слева сочетается с обеими единицами справа: база проверяет условие для каждой пары строк отдельно, а не выбирает одну пару. Для любой пары «единица слева — единица справа» условие `1 = 1` даёт «истину», поэтому все 3 × 2 = 6 пар проходят и каждая становится отдельной строкой.

Почему NULL слева не сочетается с NULL справа: `NULL = NULL` даёт «неизвестно», а ON пропускает только «истину». Поэтому обе NULL-строки остаются без пары, и сохраняются только в тех JOIN, которые сохраняют строки без пары (LEFT, RIGHT, FULL). В CROSS JOIN условия нет, поэтому NULL-строки участвуют в парах наравне с остальными.

задача 4

```sql
SELECT u.user_id, u.name,
       COALESCE(r.revenue, 0)      AS revenue,
       COALESCE(s.sessions_cnt, 0) AS sessions_cnt
FROM users AS u
LEFT JOIN (SELECT user_id, SUM(amount) AS revenue
           FROM orders
           GROUP BY user_id) AS r
    ON u.user_id = r.user_id
LEFT JOIN (SELECT user_id, COUNT(*) AS sessions_cnt
           FROM sessions
           GROUP BY user_id) AS s
    ON u.user_id = s.user_id
ORDER BY u.user_id;
```