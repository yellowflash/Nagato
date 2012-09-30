Nagato
------

Nagato is a lisp implementation on my own inspired by Peter norvig's post

http://norvig.com/lispy.html

I thought this would help me understand lisp better. Key learnings were
1. ConsCell is composed of car and cdr the cdr can itself be a ConsCell. The cdr can be part of a different ConsCell too. This allows us to have versioned lists.
2. Bindings are very important part of lisp. Lisp has a set of root bindings which defines everything that cannot be deined in lisp itself. Can be represented as ConsCell as we may have to add and remove local bindings to a function.
3. Functions have 2 bindings. Definition bindings and Execution bindings which helps to form closures (Have to clarify this with the implementation TODO).
