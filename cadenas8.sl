(set-logic SLIA)

(synth-fun f ((_arg_0 String)) Int
    ((Start Int) (ntString String) (ntInt Int) (ntBool Bool))
    ((Start Int (ntInt))
    (ntString String (_arg_0 "a" "b" "c" "d" "e" "f" "g" "h" (str.++ ntString ntString) (str.replace ntString ntString ntString) (str.at ntString ntInt)  (ite ntBool ntString ntString) (str.substr ntString ntInt ntInt)))
    (ntInt Int (1 0 (+ ntInt ntInt) (- ntInt ntInt) (str.len ntString)  (ite ntBool ntInt ntInt) (str.indexof ntString ntString ntInt)))
    (ntBool Bool (true false (= ntInt ntInt) (str.prefixof ntString ntString) (str.suffixof ntString ntString) (str.contains ntString ntString)))))

(constraint (= (f "Stately, plump Buck Mulligan came from the stairhead,") 16))
(constraint (= (f "bearing a bowl of lather on which a mirror and a razor lay crossed.") 22))
(constraint (= (f "A yellow dressinggown, ungirdled, was sustained gently behind him on the mild morning air.") 25))
(constraint (= (f "He held the bowl aloft and intoned:") 14))
(constraint (= (f "Solemnly he came forward and mounted the round gunrest.") 18))
(constraint (= (f "He faced about and blessed gravely thrice the tower, the surrounding land and the awaking mountains") 37))
(constraint (= (f "Then, catching sight of Stephen Dedalus") 15))
(constraint (= (f "he bent towards him and made rapid crosses in the air, gurgling in his throat and shaking his head.") 35))



(check-synth)
