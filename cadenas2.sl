(set-logic SLIA)

(synth-fun f ((_arg_0 String)) Int
    ((Start Int) (ntString String) (ntInt Int) (ntBool Bool))
    ((Start Int (ntInt))
    (ntString String (_arg_0 "a" "b" (str.++ ntString ntString) (str.replace ntString ntString ntString) (str.at ntString ntInt)  (ite ntBool ntString ntString) (str.substr ntString ntInt ntInt)))
    (ntInt Int (1 0 (+ ntInt ntInt) (- ntInt ntInt) (str.len ntString)  (ite ntBool ntInt ntInt) (str.indexof ntString ntString ntInt)))
    (ntBool Bool (true false (= ntInt ntInt) (str.prefixof ntString ntString) (str.suffixof ntString ntString) (str.contains ntString ntString)))))

(constraint (= (f "Stately, plump Buck Mulligan came from the stairhead,") 5))
(constraint (= (f "bearing a bowl of lather on which a mirror and a razor lay crossed.") 10))
(constraint (= (f "A yellow dressinggown, ungirdled, was sustained gently behind him on the mild morning air.") 4))
(constraint (= (f "He held the bowl aloft and intoned:") 3))

(check-synth)
