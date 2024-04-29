# Type Safety

**Definition** >> An abstract concept that enables the language to avoid type errors

Every language has some sort of type safety implemented. An error will be thrown if we assign the wrong type to a variable.

Errors can occur in any language if the code does not appropiately deal with it. There are two possible types:
* Trapped >> Causes computation to stop
* Untrapped >> Can got unnoticed and later cause some arbitrary behavior

A program can be considered safe if it does not cause any untrapped errors. There is also an additional subset of errors that can be identifed as **forbidden error**. These are all the *untrapped* errors plus a subset of *trapped* errors.  A **well-behaved** code is defined as one without any forbidden errors.

Lastly, code can be defined as **strongly checked** if all legal programs ares **well-behaved**.

**Strongly-checked** code exhibits the following properties:
* No untrapped errors occur (safety)
* No trapped errors belonging to forbidden errors occur
* Other trapped errors may occur

The process of checking types is known as **typechecking**. A programmed that passes the **typechecker** is known to be **well-typed**; otherwise, it is **ill-typed**.

## Concept of Type Safety

Type safety ensures that any variable accesses only its authorized memory locations in a well-defined and permissible wat. It ensures that the code does not perform any invalid operations on the underlying object.

### Type Error

**Type error** is when a program attempts to operate on a value on which the operation is undefined. For example, performing an addition operation on a boolean. The language will raise no error and still perform the action. The results will be undefined.

### Type Safety Control

These are lines of code implemented to prevent type errors from stopping runtime. It ensures that only vaild variable types are inputted into the algorithm/code so it can complete compiling.

## Type Safety and Type Checking

The broad concept of type checking can be split up into **static** and **dynamic** type checking based on their operations.

**Static type** programming languages are generally faster than **dynamically type** languages. This is because the languages checks the exact data types prior to running the compiler. This results in code that runs faster and uses less memory.

**Static** or **Dynamic** type is independent of **strong** and **weak** type

### Static Type

A complier that performs **static type checking** does type check the operation at compile time. This means the variable is checked before running the operation.

### Dynamic Type

A language that performs type checking operations only at runtime. The type of a variable will only be checked while executing it.

Python is an example of a **dynamically type** language as it allows variables to change types over its lifetime.

This results in slower code and possible runtime error raises.

### Strong Type

**Strongly typed** languages are when the type of variable is strongly bonded to a specific data type. Most **statically yped** languages are **strongly bonded**. These languages define datatypes at initialiation only.

### Weak Type

**Weakly typed** languages are when the variable type is not bounded to a specific data type. The variable has a type but its type constant is lower than that of the strongly typed programming langauge.

**Strongly typed** languages have a greater degree of type safety.

## Type Safety in Modern Programming Languages

### C++

C++ has a lot of type safety features but is not completely type safe. A variable can exhibit a certain type but be temporarily changed using a `cast` statement.  The problem with this is that the is not dynamically checked for *type truthfullness* (type compatibility).

If the values are incompatible, then the compiler will reinterpret the in-memory bit pattern of the expression being cast as if it belonged to the type being casted to.

### Python

Python is a *semi-type safe* language. It is dynamically and strongly typed language that has a high degree of type safety built-in. Type checking is only done during run-time.

### Java

By design, Java enforces type saftey. Java prevents programs from accessing memory that is inappropiate by controlling the memory access of each object. Java does this by using objects to perform operations.

## Drawbacks of Type Safety

### Memory Access

A type safe language maintains data truthfulness from the cradle to the grave. It will not allow an int (or other data types) to be inserted into a char at runtime. It will likely throw an out-of-memory exception.

Type unsafe languages will allow the insertion of other types into a variable by overwriting exisiting data.

### Speed vs. Safety

Type unsfafe languages are generally faster and result in efficient code but are prone to memory leaks and security holes. In many situations, overriding type saftey constructs in C/C++ help the compiler generate CPU-efficient code.

### Datatype

The main issue here is how the language interprets the datatype without considering their allocated memory. Let’s consider a signed int vs. an unsigned int. Both of them use 32 bits but signed int uses one bit to store the sign. So, in essence, we can have a maximum value of 2,147,483,647 (2 <sup>32</sup> – 1).

In a type unsafe language, we can perform the read operation on all 32 bits. Hence, we’ll get undefined behavior when we read an unsigned integer as a signed integer.
