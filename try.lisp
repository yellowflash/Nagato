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


(defn double-all (elems)
  (if (nil? elems)
      (list)
      (cons (* 2 (car elems)) (double-all (cdr elems)))))

(defn printall (elems)
  (if (nil? elems) 1
      (progn 
	(print (car elems))
	(printall (cdr elems)))))

(printall (double-all (list 1 2 3 4)))