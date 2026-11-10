Задача 1

```SQL
WITH web_orders AS (
	SELECT * FROM orders
 	WHERE amount >= 60
  	AND channel = 'web'
) 
SELECT order_id, amount
FROM orders
WHERE amount > (
	SELECT AVG(amount) FROM web_orders
)
```

Задача 2

```SQL
SELECT order_id, amount
FROM orders AS o1
WHERE amount > (
  SELECT AVG(amount)
  FROM orders AS o2
  WHERE o2.user_id = o1.user_id)
```

Задача 3

```SQL
SELECT user_id
FROM users
WHERE EXISTS(
	SELECT 1 FROM visits
	WHERE users.user_id = visits.user_id
  	AND minutes > 5
)

SELECT user_id
FROM users
WHERE users.user_id IN (
	SELECT user_id
  	FROM visits
  	WHERE minutes > 5
  	AND user_id IS NOT NULL
)
```


Задача 4

```SQL
SELECT user_id FROM users
WHERE NOT EXISTS (
	SELECT 1 FROM payments
	WHERE payments.user_id = users.user_id
  	AND payments.amount >= 100
)
```


Задача 5

```SQL

```


Задача 6

```SQL

```


Задача 7

```SQL

```


Задача 8

```SQL

```