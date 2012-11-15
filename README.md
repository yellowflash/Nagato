Nagato
------
<img src="http://fc05.deviantart.net/fs71/f/2012/235/e/5/chibi_nagato_uzumaki_by_uchihaclanancestor-d5c7csj.png" width="180px" />


Nagato is a lisp implementation on my own inspired by Peter norvig's post

http://norvig.com/lispy.html

I thought this would help me understand lisp better. 
* ConsCell is composed of car and cdr the cdr can itself be a ConsCell. The cdr can be part of a different ConsCell too. This allows us to have versioned lists.
* Bindings are very important part of lisp. Lisp has a set of root bindings which defines everything that cannot be deined in lisp itself. Can be represented as ConsCell as we may have to add and remove local bindings to a function.
* Functions have bindings when they are created. When a function gets called the bindings of the parameters are added to the definition bindings (ConsCell) and with the resultant binding the function gets called.
