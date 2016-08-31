# Sudoku Genetic Algorithm Solver  




## METHOD 
This section is intended to show how the genetic algorithm would be created and used.  

### Gene 
The gene itself was represented by a single array of integers. This meant representing the 9x9 grid as a 1x81 grid.  Upon creation the gene would generate random numbers between 1 and 9 to fill the non-fixed spots. 

### Fitness Function 
The fitness function was created using sets. The code took each row, column, and box separately and added them to a set. The set removed any non-unique numbers and the length of the set was taken.  All the set lengths were summed and the total represented the number of rule violations present in the grid. The fitness function aimed to minimize the fitness value. The equation for this can be seen in Eq. 1.  

Fitness=∑(length({row(x)}+length({column(x)}+length({box(x)}) (1)

### Selection
Overall tournament selection was used. Initially elitism was tried but often left the gene stuck so it was later removed. Two selection methods were tried. The first was single parent tournament select, where a single highest scoring gene was paired with a  random grid. The second was two parent tournament select in which two best parents in a tournament were paired together.  

### Crossover 
Two different methods of crossover was used. It randomly decided between which method would be used. The first was the line method. It would take a single line from the grid of the second parent in two parent select or from a new random grid in single parent select and replace the line in the first parent. The second method used was column method. It would do the same thing as the line method except with a column as the parent.  

### Mutation 
The three decided upon mutation methods were substation, swap and shuffle. Substation involved replacing a random non-fixed number with a new random number. Swap involved switching the places of two random non-fixed numbers. Shuffle involved shuffling the entire board except the non-fixed numbers. Shuffle was included to aid the population in diverging from a local minimum. With those mutation functions, additionally a variable mutation rate was implemented. This involved raising the mutation if the max fitness value stayed constant for a chosen number of generations. This helped the genetic algorithm diverge from local minimum.


## Installing  
This application was written in Python 3 using the Anaconda Suite.  
To install Anaconda visit: https://www.continuum.io/downloads  


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/tylerburnham42/PythonSudokuGASolver/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/tylerburnham42/PythonSudokuGASolver/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc