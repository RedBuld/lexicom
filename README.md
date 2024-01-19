# Запуск

скачать репозиторий

выполнить `docker-compose up`

# Запросы

## 1 вариант

> при вхождении одного имени в другое с точкой может быть ошибочным
> например record1.121222.mp3 и record1.121222.fixed.mp3
```sql
UPDATE `full_names` fn LEFT JOIN `short_names` sn ON fn.name LIKE CONCAT(sn.name,'.%')  SET fn.`status`=sn.status
```

## 2 вариант

```sql
UPDATE `full_names` fn LEFT JOIN `short_names` sn ON
REVERSE(
	SUBSTRING(
		REVERSE(fn.name),
        INSTR( REVERSE(fn.name), '.' ) + 1,
		CHAR_LENGTH(fn.name)
    )
) = sn.name SET fn.`status`=sn.status
```

## 3 вариант

> если имя содержит несколько точек может быть ошибочным
```sql
UPDATE `full_names` fn LEFT JOIN `short_names` sn ON SUBSTRING_INDEX(fn.name,'.',1) = sn.name SET fn.`status`=sn.status
```