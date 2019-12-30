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





- [ ] Complete the EDA as a comparison method
- [ ] 
- [ ] 



## The most important thing which I need to handle right now is how to design an efficient local search method.



To do list:

- [ ] check whether the fitness decreases as  generations of the algorithm monotonically or not. 
- [ ] Many genotypes may correspond a same **Phenotype**. So in the local search process, the neighbourhood may be defined by the phenotype. Thus, the _VINSERT method may have some good performance, is there some wrong of my experiments?
- [ ] the probability of the local search method 
- [ ] How to define a neighbour of a solution. And find how many LS solution of an Individual.
- [ ] Complete the hybrid local search method to promote the efficiency of the propose algorithm. Maybe at the begining, we can use the TRI method, and then we use the insert or swap method to promote the efficiency of my algorithm. Refer to the Mei's paper.
- [ ] Why is the **_VINSERT** method so worse. The performance of it even worse than the SWAP AND INSERT METHOD?   Because the _VINSERT maybe change the solution too much so that like a mutant process.
- [ ] But I still think the _VINSERT method which has some advantages. Because it find a real neighbour, comparing to the  _SWAP AND _INSERT method which find a virtual neighbour and maybe need to evaluate a same solution.
- [ ] Read more paper about the local search. 
- [ ]  resolve the problem (that the algorithm is convergencing so quickly)  methods (the **selection method and the restart method**)
- [ ] the time complexity  of decoding method need to be analyzed
- [ ] The selection method need to be reviesed.
- [ ] So the key idea of my local search method is hybrid of _TRI and some search method on phenotypes.
- [ ] The infeasiable solution which should be used during the search processs.



Why do we add the local search leading to decrease the efficiency  of algorithm?

1. maybe the population converges so quick so that the local search method only computates invalidly.
2. the local search method can not  a better solution easily. 



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

The restart method need to be revised.









#### The local search method maybe need to revised , the clone method will cost too many time 

