(*  Concrete syntax
e :: x | n | true | false | succ | pred | iszero | if e then e else e
       | fn x => e | e e | (e) | let x = e in e
*)
use "parser.sml";

datatype term = AST_ID of string | AST_NUM of int | AST_BOOL of bool
  | AST_SUCC | AST_PRED | AST_ISZERO | AST_IF of (term * term * term)
  | AST_FUN of (string * term) | AST_APP of (term * term)
  | AST_LET of (string * term * term)
  | AST_ERROR of string
 
datatype result = RES_ERROR of string | RES_NUM of int| RES_BOOL  of bool
                | RES_SUCC | RES_PRED | RES_ISZERO | RES_FUN of (string * term)
 
exception UnboundID
datatype env = Env of (string -> term)
fun emptyenvFun  (x : string) : term = raise UnboundID;
val emptyenv = Env emptyenvFun

fun update (Env e) (x : string) (ty : term) = fn y => if x = y then ty else e y
 
fun lookup (Env f) i = f i

exception Not_implemented_yet
exception Error of string

fun interp_lazy (env, AST_ID i)          = interp_lazy(env, lookup env i) 
  | interp_lazy (env, AST_NUM n)         = RES_NUM n
  | interp_lazy (env, AST_BOOL b)        = RES_BOOL b
  | interp_lazy (env, AST_FUN (i,e))     = RES_FUN (i,e)
  | interp_lazy (env, AST_APP (e1,e2))   = (case interp_lazy (env, e1) of
         RES_FUN (x, body)  => interp_lazy( Env (update env x e2 ), body)
       | RES_SUCC => (case interp_lazy(env, e2) of
                          RES_NUM 0 => RES_NUM(0)
                        | RES_NUM n => RES_NUM(n+1)
                        | _         => RES_ERROR "cannot increment non intenger")
       | RES_PRED   => (case interp_lazy(env, e2) of
                          RES_NUM 0 => RES_NUM(0)
                        | RES_NUM n => RES_NUM(n-1)
                        | _         => RES_ERROR "cannot decrement non integer" ) 
       | RES_ISZERO => (case interp_lazy(env, e2) of
                          RES_NUM 0 => RES_BOOL true
                        | RES_NUM n => RES_BOOL false
                        | _         => RES_ERROR "not a zero")
       | _ => RES_ERROR "apply non-function"
                                      )
  | interp_lazy (env, AST_SUCC)          = RES_SUCC
  | interp_lazy (env, AST_PRED)          = RES_PRED
  | interp_lazy (env, AST_ISZERO)        = RES_ISZERO
  | interp_lazy (env, AST_IF (e1,e2,e3)) =  (case interp_lazy (env,e1) of
                                     RES_BOOL(false) => interp_lazy (env,e3)
                                   | RES_BOOL(true)  => interp_lazy (env,e2)
                                   | _               => RES_ERROR "case on non-bool on e1")

  | interp_lazy (env, AST_LET (x,e1,e2)) = let val v1 = interp_lazy(env, e1)
                                                in case v1 of
                                                    RES_ERROR string => v1
                                                  | _ => interp_lazy(env,e2)
                                                end
                                     
  | interp_lazy (env, AST_ERROR s)       = raise Error s

fun interp_lazy_static (env, AST_ID i)          = interp_lazy_static (env, lookup env i) 
  | interp_lazy_static (env, AST_NUM n)         = RES_NUM n
  | interp_lazy_static (env, AST_BOOL b)        = RES_BOOL b
  | interp_lazy_static (env, AST_FUN (i,e))     = RES_FUN (i,e)
  | interp_lazy_static (env, AST_APP (e1,e2))   = (case interp_lazy_static (env, e1) of
         RES_SUCC => (case interp_lazy_static(env, e2) of 
                          RES_NUM n => RES_NUM(n+1)
                        | _         => RES_ERROR "not valid")
       | RES_PRED => (case interp_lazy_static(env, e2) of
                          RES_NUM 0 => RES_NUM 0
                        | RES_NUM n => RES_NUM (n-1)
                        | _         => RES_ERROR "not valid")
       | RES_ISZERO => (case interp_lazy_static(env, e2) of
                          RES_NUM 0 => RES_BOOL true
                        | RES_NUM n => RES_BOOL false
                        | _         => RES_ERROR "not valid")
       | _ => raise Error "apply non-function")
  | interp_lazy_static (env, AST_SUCC)          = RES_SUCC
  | interp_lazy_static (env, AST_PRED)          = RES_PRED
  | interp_lazy_static (env, AST_ISZERO)        = RES_ISZERO
  | interp_lazy_static (env, AST_IF (e1,e2,e3)) =  (case interp_lazy_static (env,e1) of
                                     RES_BOOL true  => interp_lazy_static (env,e2)
                                   | RES_BOOL false => interp_lazy_static (env,e3)
                                   | _              => raise Error  "case on non-bool")

  | interp_lazy_static (env, AST_LET (x,e1,e2)) = let val v1 = interp_lazy(env, e1)
                                                in case v1 of
                                                    RES_ERROR string => v1
                                                  | _ => interp_lazy(env,e2)
                                                end

  | interp_lazy_static (env, AST_ERROR s)       = raise Error s

val test4 = "let f = fn g => let x = 3 in g 2 end \
\             in let x = 4 \
\                in let h = fn y=> + x y \
\                    in f h \
\                   end \
\                end \
\              end";

