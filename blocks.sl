;;
;; Blocksword planning domain theory
;;
(set-logic ALL)
(set-option :produce-models true)

;;; Auxiliary functions
(define-fun getBitAt1D ((bvector (_ BitVec 3)) (x Int)) Bool
 (ite (= x 0) 
      (= (bvand bvector #b001) #b001)
      (ite (= x 1) 
           (= (bvand bvector #b010) #b010)
           (ite (= x 2) (= (bvand bvector #b100) #b100) 
                false))))

(define-fun getBitAt2D ((bvector (_ BitVec 9)) (x Int) (y Int)) Bool
 (ite (= x 0) 
      (ite (= y 0) 
           (= (bvand bvector #b000000001) #b000000001)
           (ite (= y 1) 
                (= (bvand bvector #b000000010) #b000000010)
                (ite (= y 2) 
                     (= (bvand bvector #b000000100) #b000000100)
                     false)))
      (ite (= x 1) 
           (ite (= y 0) 
                (= (bvand bvector #b000001000) #b000001000)
                (ite (= y 1) 
                     (= (bvand bvector #b000010000) #b000010000)
                     (ite (= y 2) 
                          (= (bvand bvector #b000100000) #b000100000)
                          false)))
           (ite (= x 2) 
                (ite (= y 0) 
                     (= (bvand bvector #b001000000) #b001000000)
                     (ite (= y 1) 
                          (= (bvand bvector #b010000000) #b010000000)
                          (ite (= y 2)
                               (= (bvand bvector #b100000000) #b100000000)
                               false)))
                false))))


 (define-fun setBitAt1D ((bvector (_ BitVec 3)) (x Int)) (_ BitVec 3)
  (ite (= x 0) 
       (bvor bvector #b001)
       (ite (= x 1) 
            (bvor bvector #b010) 
            (ite (= x 2) (bvor bvector #b100)
                 bvector)))) 

 (define-fun setBitAt2D ((bvector (_ BitVec 9)) (x Int) (y Int)) (_ BitVec 9)
 (ite (= x 0) 
      (ite (= y 0) 
           (bvor bvector #b000000001)
           (ite (= y 1) 
                (bvor bvector #b000000010) 
                (ite (= y 2) 
                     (bvor bvector #b000000100) 
                     bvector)))
      (ite (= x 1) 
           (ite (= y 0) 
                (bvor bvector #b000001000) 
                (ite (= y 1) 
                     (bvor bvector #b000010000) 
                     (ite (= y 2) 
                          (bvor bvector #b000100000) 
                          bvector)))
           (ite (= x 2) 
                (ite (= y 0) 
                     (bvor bvector #b001000000) 
                     (ite (= y 1) 
                          (bvor bvector #b010000000) 
                          (ite (= y 2)
                               (bvor bvector #b100000000) 
                               bvector)))
                bvector))))


(define-fun unsetBitAt1D ((bvector (_ BitVec 3)) (x Int)) (_ BitVec 3)
 (ite (= x 0) 
      (bvand bvector #b110)
      (ite (= x 1) 
           (bvand bvector #b101) 
           (ite (= x 2) 
                (bvand bvector #b011)
                bvector)))) 

 (define-fun unsetBitAt2D ((bvector (_ BitVec 9)) (x Int) (y Int)) (_ BitVec 9)
 (ite (= x 0) 
      (ite (= y 0) 
           (bvand bvector #b111111110)
           (ite (= y 1) 
                (bvand bvector #b111111101) 
                (ite (= y 2) 
                     (bvand bvector #b111111011) 
                     bvector)))
      (ite (= x 1) 
           (ite (= y 0) 
                (bvand bvector #b111110111) 
                (ite (= y 1) 
                     (bvand bvector #b111101111) 
                     (ite (= y 2) 
                          (bvand bvector #b111011111) 
                          bvector)))
           (ite (= x 2) 
                (ite (= y 0) 
                     (bvand bvector #b110111111) 
                     (ite (= y 1) 
                          (bvand bvector #b101111111) 
                          (ite (= y 2)
                               (bvand bvector #b011111111) 
                               bvector)))
                bvector))))


;;;
;; Structure of the Blocksword states 
(declare-datatypes ((PlanningState 0))
   (((rec (handempty Bool) 
          (holding (_ BitVec 3))
          (clear (_ BitVec 3))
          (ontable (_ BitVec 3))
          (on (_ BitVec 9))))))

;;;
;; The Blocksword action schemes
(define-fun putdown ((s PlanningState) (x Int)) PlanningState
 (ite (and (getBitAt1D (holding s) x))
      (rec 
           true
           (unsetBitAt1D (holding s) x)
           (setBitAt1D (clear s) x)  
           (setBitAt1D (ontable s) x)  
           (on s))
      s))

(define-fun pickup ((s PlanningState) (x Int)) PlanningState
 (ite (and (handempty s)
           (getBitAt1D (ontable s) x)
           (getBitAt1D (clear s) x))
      (rec false
           (setBitAt1D (holding s) x)
           (unsetBitAt1D (clear s) x)  
           (unsetBitAt1D (ontable s) x)  
           (on s))
      s))

(define-fun unstack ((s PlanningState) (x Int) (y Int)) PlanningState
  (ite (and (handempty s) 
            (getBitAt1D (clear s) x)
            (getBitAt2D (on s) x y))
       (rec false 
            (setBitAt1D (holding s) x)
            (setBitAt1D (unsetBitAt1D (clear s) x) y)
            (ontable s)
            (unsetBitAt2D (on s) x y))
       s))

(define-fun stack ((s PlanningState) (x Int) (y Int)) PlanningState
  (ite (and (getBitAt1D (holding s) x)
            (getBitAt1D (clear s) y)            
            )
       (rec true
            (unsetBitAt1D (holding s) x)
            (unsetBitAt1D (setBitAt1D (clear s) x) y)
            (ontable s)
            (setBitAt2D (on s) x y))
        s))

;;; syntactic constraints
(synth-fun plan ((s PlanningState)) PlanningState
 ((Start PlanningState) (I1 Int ) (I2 Int ))
 ((Start PlanningState (s (unstack Start I1 I2) (putdown Start I1)))
  (I1 Int (0 1 2))
  (I2 Int (0 1 2))
  ))

;;;
;; The classical planning problem
(declare-var initialState PlanningState)
(constraint (= (handempty initialState) true))
(constraint (= (holding initialState) #b000))
(constraint (= (clear initialState) #b001))
(constraint (= (ontable initialState) #b100))
(constraint (= (on initialState) #b000100010))

(declare-var goalState PlanningState)
(constraint (= (handempty goalState) true))
(constraint (= (holding goalState) #b000))
(constraint (= (clear goalState) #b001))
(constraint (= (ontable goalState) #b100))
(constraint (= (on goalState) #b000100010))


(constraint (= goalState (plan initialState)))

(check-synth)