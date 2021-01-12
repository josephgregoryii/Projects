use "type.sml";

Control.Print.printDepth:= 100;

(* A term datatype with typed function arguments to allow type checking *)
datatype term
  = AST_ID of string
  | AST_NUM of int
  | AST_BOOL of bool
  | AST_FUN of (string * typ * term)
  | AST_SUCC
  | AST_PRED
  | AST_ISZERO
  | AST_IF of (term * term * term)
  | AST_APP of (term * term)
  | AST_LET of (string * term * term)

exception Unimplemented
exception TypeError

(* typeOf : term * env -> typ *)
fun typeOf (Env env) (AST_ID s)    = env s 
  | typeOf env (AST_NUM n)         = INT
  | typeOf env (AST_BOOL b)        = BOOL 
  | typeOf env (AST_FUN (i,t,e))   = ARROW(t, typeOf(Env (update env i t)) e) 
  | typeOf env AST_SUCC            = ARROW (INT,INT) 
  | typeOf env AST_PRED            = ARROW (INT, INT) 
  | typeOf env AST_ISZERO          = ARROW (INT,BOOL)
  | typeOf env (AST_IF (e1,e2,e3)) =
    let val t1 = typeOf env e1
        val t2 = typeOf env e2
        val t3 = typeOf env e3
    in
        case (t1 = BOOL) andalso (t2 = t3) of
            true => t3
          | false => raise TypeError
    end
  | typeOf env (AST_APP (e1,e2))   = 
    let val typ1 = typeOf env e1
        val typ2 = typeOf env e2
    in
        case typ1 of
            ARROW(t1, t2) =>
                if t1 = t2
                        then t2
                        else raise TypeError
    end
  | typeOf env (AST_LET (x,e1,e2)) = 
    let val t1 = typeOf env e1
        val t2 = typeOf(Env (update env x t1)) (*t2 : e2*)
    in
        case typeOf env e2 of 
            ARROW(t1, t2) =>
                if t1 = t2
                    then t2
                    else raise TypeError
    end
       
            
  (* if given some e1 type t1
    from that we get e2 type t2
    then we have a well typed let x=e1 in e2 : t2
    *)
(* 
ML types 

1)
(a) int : INT
(b) int -> bool " ARROW(INT,BOOL)
(c) (a' -> b') -> ('a -> 'b): ARROW(ARROW(VAR "a", VAR "b"), ARROW("VAR "a", VAR "b"))

2)
(a) succ (pred 5) : AST_APP (AST_SUCC, AST_APP (AST_PRED, AST_NUM 5))
(b) if 7 then true else 5: AST_IF (AST_NUM 7, AST_BOOL true, AST_NUM 5)
(c) fn a : int => f a a: AST_FUN ("a", INT, AST_APP (AST_ID "f", AST_APP (AST_ID "a", AST_ID "a")))


PART 2

*************************************
1. fun f (g,h) = g (h 0)

f   : 'a1 * 'a2 -> 'a3
f   : 'a1 : ('a -> 'b) * 'a2 -> 'a3
f   : 'a1 : ('a -> 'b) * (int -> 'a) -> 'a3
f   : 'a1 : ('a -> 'b) * (int -> 'a) -> 'b

'a1 : ('a -> 'b)
'a2 : (int -> 'a)
'a3 : 'b

f: ('a -> 'b) * (int -> 'a) -> 'b

*************************************

2. fun apply (f,x) = f x

apply : 'a1 * 'a2 -> 'a3
apply : 'a1   : ('a -> 'b) * 'a2 -> 'a3
apply : 'a1   : ('a -> 'b) * 'a2 -> 'a -> b'
apply : 'a1   : ('a -> 'b) * 'a  -> 'a -> 'b

'a1 : ('a -> 'b)
'a2 : 'a
'a3 : 'a -> 'b

apply : (a' -> b') * 'a -> 'a' -> b'

*************************************
3. fun reverse nil      = nil
    | reverse (x::xs)   = reverse xs

reverse : 'a list -> 'b list

Since it is a general type used, reversing a list
should not change the type of list. 


*************************************

4. fun f(g,h) = g h + 2
f   : 'a1 * 'a -> 'a2
f   : 'a1 * 'a -> 'a2
f   : 'a1 * 'a -> 'a -> int

'a1 : ('a -> int) * 'a -> 'a -> int
'a2 : 'a -> int

f   : ('a -> int) * 'a -> int 

*************************************

5. fun f g = g(g) + 2

f: 'a1 -> int
g: 'a1 : (('a2 -> int) -> int) -> int
this would cause the inference engine to look forever

*************************************

6.
fun ff f x y = if (f x y) then (f 3 y) else (f x "zero")
ff: 'a1 -> 'a2 ->'a3 -> 'a4
f:  'a1 :  'a2 -> 'a3 -> bool
f:  'a1 :  int -> 'a3 -> 'a4
f:  'a1 :  'a2 -> string -> bool
f:  'a1 :  int -> string -> bool

'a4 : bool
'a3 : int
'a2 : string

'a1 : int -> string -> bool

ff : (int -> string -> bool) -> int -> string -> bool

*************************************

7. fun gg f x y = if (f x y) then (f 3 y) else (f x "zero)
gg : 'a1 -> 'a2 -> 'a3 -> 'a4
f  : 'a1 :  'a2 -> 'a3 -> 'a4
f  : 'a1 :  'a2 -> 'a3 -> bool
f  : 'a1 :  'int -> 'a3 -> bool
f  : 'a1 :  'int -> string -> bool

'a1 : int -> string -> bool
gg  : (int -> string -> bool) -> int -> string -> bool


*************************************

8. fun hh f x y = if (f x y) then (f x y) else (f x "zero")
hh : 'a1 -> 'a2 -> 'a3 -> 'a4
hh : 'a1  : 'a2 -> 'a3 -> 'a4
hh : 'a1  : 'a2 -> 'a3 -> bool 
hh : 'a1  : 'a2 -> string -> bool 
hh : 'a1  : 'a -> string -> bool 
'a1 : 'a -> string -> bool

hh : ('a -> string -> bool) -> 'a -> string -> bool

*************************************
*)

(*
Some sample functions translated into abstract syntax for you to test
your typechecker on:
*)

(* fn (f : a -> a) => fn (x : a) => f (f x) *)
val test1 = AST_FUN("f", ARROW(VAR "a", VAR "a"),
                AST_FUN("x", VAR "a",
                    AST_APP(AST_ID "f",
                        AST_APP(AST_ID "f", AST_ID "x"))));

(* fn (f : 'b -> 'c) => fn (g : 'a -> 'b) => fn (x : 'a) => f (g x) *)
val test2 = AST_FUN("f", ARROW(VAR "b", VAR "c"),
                AST_FUN("g", ARROW(VAR "a", VAR "b"),
                    AST_FUN("x", VAR "a",
                        AST_APP(AST_ID "f",
                            AST_APP(AST_ID "g", AST_ID "x")))));

(* (* fn (b : bool) => if b then 1 else 0 *) *)
val test3 = AST_FUN("b", BOOL,
                AST_IF(AST_ID "b", AST_NUM 1, AST_NUM 0));

val t1 = (typeOf emptyenv test1);
typ2str(t1);
val t3 = (typeOf emptyenv test3);
typ2str(t3);
