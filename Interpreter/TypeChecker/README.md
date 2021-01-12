# Type checker for a statically typed language

### Syntax for language:
```sml
e ::= x | n | true | false | iszero | succ | pred | if e then e else e
        | fn x : t => e | e e | let x = e in e | (e)

t ::= ’a | int | bool | t -> t
```


### Typing Rules:
```sml
(* A variable has the type the environment has stored for it *)
        env(x) = t
(ID)    ----------
        env |- x: t

(* integer literal has type int and a Boolean literal has a type bool  *)
(NUM)   env |- n : int
(TRUE)  env |- true : bool
(FALSE) env |- false : bool

(SUCC)      env |- succ : int -> int
(PRED)      env |- pred : int -> int
(ISZERO)    env |- iszero : int -> bool

(* if else statement *)
        env |- e1 : bool    env |- e2 : t   env |- e3 :
(IF)    ----------------------------------------------
            env |- if e1 then e2 else e3 : t
```
