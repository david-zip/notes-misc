# Dynamic Data Masking in Snowflake

## What is Dynamic Data Masking?

Dynamic data masking is a column-level security feature which allows you to alter data for anonymity using predefined masking policies. Column-level security is a type of masking policy that is applied to all values of a column within a table or view.

Masking policies are schema-level objects whihc can protect sensitive data from being viewed by unautorized roles. Data is not being modified, but rather hidden from the user. There are vaious forms of masking:

- Masked
- Partially masked
- Obfuscated
- Tokenized

In Snowflake, as masking policies are schema-level objects, databases and schemas must be defined first in order to create or apply a masking policy.

Another form of data masking is known as **Static Data Masking**. This differs from dyanmic data masking as data will always be censored regardless of the party querying it. In dyanmic data masking, the amount of data censor is dependant on the role.

There are various benefits to dynamic data masking:

- New masking policies can be made with ease and without any overhead of historic loading of data
- Policies can be written once and be applied to various columns across databases and schemas
- Masking policies are easy to manage and support centralized and decentralized administration models
- Data can be easily masked before being shared
- Easily change masking policy with having to reapply a new policy on multiple columns

## Dynamic Masking Main Clauses

{::comment}
  refine this
{:/comment}

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
ALTER TABLE IF EXIST exampleDb.exampleScm.exampleTable 
  MODIFY COLUMN columnName
  SET MASKING POLICY columnMask;
```

### Remove Masking Policy

Masking policies can be removed from a table using the following code:

```sql
ALTER TABLE IF EXIST exampleDb.exampleScm.exampleTable 
  MODIFY COLUMN columnName
  UNSET MASKING POLICY;
```

Once the masking policy has been removed, it can be deleted as shown below:

```sql
DROP MASKING POLICY columnMask;
```

## Alternative Masking Methods

### Conditinal Masking Policy

There are scenarios in which data masking should be dependant on other column values instead of the user role. This is known as **Conditional Data Masking** and Snowflakes supports the implementation of it.

THe following code will demonstrate how a user can showcase specific data whilst hiding everything else.

```sql
CREATE OR REPLACE MASKING POLICY maskColumn AS 
(dataColumn string, visibility boolean)
RETURNS string ->
  CASE
    WHEN visibility = true
      THEN dataColumn
    ELSE '*****'
  END;
```

Applying the mask is done similar to dynamic data masking.

```sql
ALTER TABLE IF EXIST exampleDb.exampleScm.exampleTable
  MODIFY COLUMN dataColumn
  SET MASKING POLICY maskColumn
  USING (dataColumn, visibility);
```

### Hash Data Masking

One can return a hash value to mask columns for unauthorized users. One drawback of hash masking is that the results may cause collisions (check what this is). The two functions are synonymous.

```sql
SHA2(dataColumn, digest_size)

SHA2_HEX(dataColumn, digest_size)
```

`digest_size` is an optional parameter which specifies the type of `SHA-2` function will be used to encrypt the string. Possible inputs are listed below

- 224 = `SHA-224`
- 256 = `SHA-256` (default)
- 384 = `SHA-384`
- 512 = `SHA-512`
