# MPDA_conf

1. the event of arrive and departure immediately need to be found and eliminated. (Local search )
2. The very excuting time need to be revised. (Local search )
3. Some departure time can be advanced for a little while. (Local search)





The mutation method will adopt the classical methods.

The selection method also will adopt the classical methods







12 Dec 

- [x] Write a normal GA

- [x] Fix the decoding bug about the stuck condition (the random search method best solution is 841.7637188557708)

  ```python
  [[6 1 0 7 5 4 2 3]
   [6 4 7 0 5 3 2 1]
   [3 0 4 2 6 7 5 1]
   [3 5 6 0 2 7 1 4]
   [4 5 1 0 6 7 3 2]
   [6 3 4 0 7 5 1 2]
   [1 0 3 6 7 4 5 2]
   [1 4 7 0 2 3 6 5]]
  ```

- [x] Record the result of random search method

13 Dec

- [ ] The disturb method as a local search method.
- [x] implementation on the grid.



Some notes:
You are exactly correct. In Python 3, map returns an iterator, which you can only iterate over once. If you iterate over an iterator a second time, it will raise StopIteration immediately, as though it were empty. max consumes the whole thing, and min sees the iterator as empty. If you need to use the elements more than once, you need to call list to get a list instead of an iterator.




The crossover methods need to be revised.
Some problem needs to revised
contributions are the decoding method and the better performance
Comparison methods is the EDA.

The convergence time is so quick, so I need some methods to 
change the character of the convergence. (Maybe we can add some restart mechanism)

TRDIAGNLE localsearch method may promote the fitnees of MPDA GA search process.




1. The very small excuting time need to be found and revised.







#### The local search method maybe need to revised , the clone method will cost too many time 


