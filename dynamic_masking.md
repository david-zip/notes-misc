# Dynamic Data Masking in Snowflake

## What is Dynamic Data Masking?

Dynamic data masking is a column-level security feature which allows you to alter data for anonymity using predefined masking policies.

In Snowflake, as masking policies are schema-level objects, databases and schemas must be defined first in order to create or apply a masking policy.

Another form of data masking is known as **Static Data Masking**. This differs from dyanmic data masking as data will always be censored regardless of the party querying it. In dyanmic data masking, the amount of data censor is dependant on the role/

There are various benefits to dynamic data masking:

- Ease of use
  - Can apply a single policy to numerous rows with ease
  - Highly reusable

- Data administration and segragation of duties
  - Security or privacy officer will decided what to protect, not the object (data) owner
  - Easy to manage and support centralized and decentralized administration models

- Data authorization and governance
  - Contextual data access by role
  - Supports data governance as implemented by security or privacy officers and can prohibit privileged users with the ACCOUNTADMIN or SECURITYADMIN role from unnecessarily viewing data

- Data sharing
  - Easily mask data prior to sharing it

- Change management
  - Easily change masking policy content without having to reapply the masking policy to thousands of columns

## Dynamic Masking Main Clauses

`CREATE` - Creates the new masking policy in a schema
`APPLY` - Allows the SET and UNSET operations for a masking policy on a column
`OWNERSHIP` - Provides full control over the masking policy (only one role can hold this privilege)

## Masking Policy Implementation

In the following example, we will create a masking policy for a table so that it will show all PII to the ACCOUNTADMIN role, hide most of the data to the DATAENGINEER role, and hide everything for all other roles.

``` sQL
CREATE MASKING POLICY columnMask AS
  (val string) RETURNS string ->
    CASE
      WHEN CURRENT_ROLE() IN (ACCOUNTADMIN) THEN val
      WHEN CURRENT_ROLE() IN (DATAENGINEER) THEN masking_code
      ELSE '*****' 
    END;
```

There are multiple ways one write the masking code. The following example will showcase three types of possible options (there are more than just the following three):

1. Mask only desired string before seperator (example will use email and show only the domain)

```sql
REGEXP_REPLACE(val, '.+\@', '*****@')
```

2. Mask everything but the first three characters

```sql
SUBSTR(val, 1, 3) || '***'
```

3. Mask everything but the last three characters

```sql
'***' || SUBSTR(VAL, -9, 9)
```

Once the masking policy has been created, it can be added onto the table via the following code:

```sql
ALTER TABLE IF EXIST tableName MODIFY COLUMN columnNAME SET MASKING POLICY columnMask;
```

### Remove Masking Policy

Masking policies can be removed from a table using the following code:

```sql
ALTER TABLE IF EXIST tableName MODIFY COLUMN columnNAME UNSET MASKING POLICY;
```

Once the masking policy has been removed, it can be deleted as shown below:

```sql
DROP MASKING POLICY columnMask;
```

## Conditinal Masking Policy

There are scenarios in which data masking should be dependant on other column values instead of the user role. This is known as **Conditional Data Masking** and Snowflakes supports the implementation of it.

THe following code will demonstrate how a user can showcase specific data whilst hiding everything else.

```sql
CREATE OR REPLACE MASKING POLICY exampleDb.exampleScm.exampleTable AS 
(dataColumn string, visibility boolean)
RETURNS string ->
  CASE
    WHEN visibility = true
      THEN dataColumn
```