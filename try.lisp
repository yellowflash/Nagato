(defn double (a) (+ a a))

(defn multiply-if-non-zero (a b)
  (if b 
      (* a b) 
    a))

(defn add-n (n)
  (fn (a) (+ a n)))

(print ((add-n 100) 200))


(print (double 100))

(print (+ 1 (* 2 3)))
(print (+ 2 2))

(print (multiply-if-non-zero 100 100))

(print (multiply-if-non-zero 100 0))
