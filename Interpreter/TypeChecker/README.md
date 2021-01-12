# Type checker for a statically typed language

### Syntax for language:
```sml
e ::= x | n | true | false | iszero | succ | pred | if e then e else e
        | fn x : t => e | e e | let x = e in e | (e)

t ::= ’a | int | bool | t -> t
```


### Typing Rules:
```sml
        env(x) = t
(ID)    ----------
        env |- x: t
```
