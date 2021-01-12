# Interpreter for a lazy (call by name) language

### Syntax for language:
```sml
e ::= x | n | true | false | iszero | succ | pred | if e then e else e
        | fn x : t => e | e e | let x = e in e | (e)

t ::= ’a | int | bool | t -> t
```


### Typing Rules:
```sml
(* A variable has the type the environment has stored for it *)
                    env(x) = e  env |- e --> v
(Dynamic Scope)     --------------------------
                    env |- x -> v

                    env |- e1 --> (fn x => e3) env, (x, e2) |- e3 --> v3
                    ----------------------------------------------------
                                env |- e1 e2 --> e3


(Static Scope)      env(x) = (e, env1)  env1 |- e --> v
                    -----------------------------------
                            env |-x --> v

                    env |- (fn x => e) --> (fn x => e, env)

                    env |- e1 --> (fn x => e3, env1) env1, (x, (e2, env)) |- e3 --> v3
                    -----------------------------------------------------------------
                                        env |- e1 e2 -> v3 


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

(* (-> INTRO) rule uses the notation env[x : t1] to denote an updated environment *)
                env[x : t1] |- e : t2
(-> INTRO)  ---------------------------------
            env |- fn x : t1 => e : t1 -> t2

            env | -e e1 : t1    env[x : t1] |- e2: t2
(-> LET)    -----------------------------------------
                env |- let x=e1 in e2 : t2
```
