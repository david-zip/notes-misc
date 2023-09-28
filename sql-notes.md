# SQL Notes

SQL stands for **Structed Query Language**. Developed by IBM, it is a relatively simple and easy to learn language that can be used for creating or collecting data from relational databases.

Relataional databases are a collection of data stored in tables. Each table will consist of multiple columns or rows. Each table will be defined by a name and the name must be *unique*. Columns will typicall have a name in ALLCAPS, whilst row will not have names and their position is not fixed. Rows are identified by the data within them.

## Basic Queries

### SELECT Query

The most basic query is the SELECT clause. It can be used to selected columns from a table and display them.

``` sql
SELECT *
FROM table1;
```

FROM can be used to specify which table to collect the columns from.

The asterisk (*) means all columns.

If multiple specific columns are meant to be selected, commas (,) can be used to specify the different columns.

``` sql
SELECT column1, column2
FROM table1;
```

### Selecting Specific Rows

As rows are identified by the values contained in them, it is imperative to know what data types can be stored in rows:

* NUMERIC
  * Positive numbers
  * Negative numbers
  * Decimal numbers
* Non-numeric
  * Single word
  * Multiple words
  * Single quotes
* Date
  * yyyy-mm-dd format

Non-numeric variables shoud be stored in single-quotes ('). 

In order to select specific rows, comparisons must be made. This can be done using the following operators.

Operators | Meaning
--------- | --------
=         | equal to
<>        | not equal to
<         | less than
<=        | less than or equal to
\>        | more than
\>=       | more than or equal to

Examples of specifying rows:

``` sql
SELECT column1, column2
FROM table1
WHERE column2 > 3000;
```

### Sorting Rows

Once the rows have been selected, they can be sorted using the ORDER clause.

``` sql
SELECT column1, column2
FROM table1
ORDER BY column2;
```

If it should be ordered in descending order, add the DESC clause.

``` sql
SELECT column1, column2
FROM table1
ORDER BY column2 DESC;
```

If it should be ordered first by column1 and then column2, commas(,) can be used.

``` sql
SELECT column1, column2
FROM table1
ORDER BY column1, column2;
```

### Eliminating Duplicat Rows

Using DISTINCT clause after the SELECT clause will prevent showing duplicate rows.

``` sql
SELECT DISTINCT column1
FROM table1
```

## Advanced Operators

### LIKE Operator

LIKE operator is used to find rows that following a similar pattern to the provided search.Patterns are always enclosed in single-quotations (').

Percent (%) is used as aplaceholder for zero or more characters.

Underscore (_) is used as a placeholder for single characters.

``` sql
SELECT column1, column2
FROM table1
WHERE column1 LIKE '%ample%';
```

``` sql
SELECT column1, column2
FROM table1
WHERE column1 LIKE 'exam__e';
```

### AND Operator

AND operator is used to combine two comparisons, creating a compound comparison.

``` sql
SELECT column1, column2
FROM table1
WHERE column1 LIKE '%mple' AND column2 > 3000;
```

### BETWEEN Operator

BETWEEN operator is similar to the AND operator but it compares for values within a specified range.

``` sql
SELECT column1, column2
FROM table1
WHERE column1 BETWEEN 3000 AND 6000;
```

### OR Operator

Similar to AND operator but only one of the comparisons have to return as TRUE.

``` sql
SELECT column1, column2
FROM table1
WHERE column1 LIKE '%mple' OR column2 > 3000;
```

### IN Operator

Similar to OR operator but compares for values provided in a list

``` sql
SELECT column1, column2
FROM table1
WHERE column1 IN ('example1', 'example2', 'example3');
```

### IS NULL Operator

Null is a missing value in a column. It means 'nothing' or 'does not apply'. This operator will located all null rows in a given column.

``` sql
SELECT column1, column2
FROM table1
WHERE column2 IS NULL;
```

### Precedence and Negation

Parentheses can be used to emphasise what should be evaluated first. NOT operator can be used to negate, or reverse the result of a comparison.

``` sql
SELECT column1, column2
FROM table1
WHERE column2 LIKE 'example' AND (column2 BETWEEN 3000 AND 5000)
ORDER BY column1, column2;
```

``` sql
SELECT column1, column2
FROM table1
WHERE column2 LIKE 'example' AND NOT (column2 BETWEEN 3000 AND 5000)
ORDER BY column1, column2;
```

## Expressions

### Arithmetic Expressions

Operator | Meaning
-------- | ---------
\+       | Addition
\-       | Subtract
\*       | Miltiply
/        | Division
()       | Precedence

``` sql
SELECT column1, column2/column3
FROM table1;
```

### Column Alias

Temporarily rename the column when displaying the table. Will not change the actual column name.

``` sql
SELECT column1, column2/column3 AS aliasname
FROM table1;
```

## Functions

### Statistical Funtcions

Statistical functions are built-in functions that can perform statistical task. There are five supported by default SQL.

Functions                   | Meaning 
--------------------------- | ---------------------------
`COUNT(*)`                  | Count all rows
`COUNT(column1)`            | Count non-null rows
`COUNT(DISTINCT column1)`   | Count all unique rows
`SUM()`                     | Total value
`MIN()`                     | Smallest value
`MAX()`                     | Largest value
`AVG()`                     | Average value

``` sql
SELECT AVG(column2)
FROM table1;
```

Functions can also be used in the ORDER BY clause. It cannot be used in the in the WHERE clause so HAVING can be used instead.

``` sql
SELECT column1, SUM(column2) AS total
FROM table1
WHERE column1 = 'example'
HAVING total > 5000;
```

### Grouping

SQL can separate tables into groups using the GROUP BY clause.

``` sql
SELECT column1, column2
FROM table1
WHERE column1 = 'example'
GROUP BY column1, column2;
```

## Multi-Table Queries

### Joins

Columns of two or more results can be joined together into a single result using a technique known as joining. Tables can be joined via the following steps:

1. List all required tables in the FROM clause
2. Enter the appropiate comparisons in the WHERE clause
3. Specify which columns should appear in the results in the SELECT clause

``` sql
SELECT column1, column2, table1.column3, column4
FROM table1, table2
WHERE table1.column3 = table2.column3;
```

### Table Alias

Tables can be given aliases so they are easier to call.

``` sql
SELECT column1, column2, t1.column3, column4
FROM table1 AS t1, table2 AS t2
WHERE t1.column3 = t2.column3;
```

### Unions

A union combines the rows of two similar queries into a single result with no duplicates. It is typically placed between two queries.

``` sql
SELECT column1
FROM table1
WHERE criteria1 > 1000;

UNION

SELECT column2
FROM table2
WHERE criteria2 > 4000;
```

## Queries within Queries

### Single-Valued Subqueries

A single-valued subquery is a query that produces a result with a single column and a single row; and is nested in the WHERE clause of another query.

``` sql
SELECT column1, column2
FROM table1
WHERE column2 > (
  SELECT AVG(column2)
  FROM table1
);
```

### Multi-Variable Subqueries

A multi-valued subquery is a query that returns a single-column with zero or more rows; and is nested in the WHERE clause of another query. Multi-valued subqueries always followthe IN operator.

``` sql
SELECT column1, column2
FROM table1
WHERE NOT column1 IN (
  SELECT DISTINCT column1
  FROM table2
  WHERE column3 = 'example'
);
```

### Correlated Subqueries

A correlated subquery is a single- or multi-valued subquery that references the outer query via a table alias defined in the outer query's FROM clause. The subqueryis executed once for each row of the outer query.

```sql 
SELECT column1, column2
FROM table1 as t1
WHERE criteria = (
  SELECT MIN(column3)
  FROM table1
  WHERE column1 = t1.column1
)
```