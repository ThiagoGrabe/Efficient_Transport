# Efficient Transport - Graphs


Using Dijkstra as min-path algorithm in this project we used an ideia of a container with maximum nine positions and given a start and final configuration we want to stablish the mininmun changes between each position of the container.

This project is part of PAA class at Departamento de Ciência da Computação - UFMG (Master degree program).

The algorithm will compute the changes between the container positions using the cost list `C(x,y)` given. Every change has one associated cost and can be evaluated following the formula:
```
C(x,y) = W(x) + W(y)
```
Where the `x` and `y` are the positions to be changed and the function `W(x), W(y)` is simply find the `x` and `y` associated cost in the weight list.

## Input

The input consist in 3 main parts.

1. First line is the container configuration - lenght and height;
2. Second line is the weight value for each postion. The second line is a list of where each position of the list mean the respective weight of the container;
3. After the first and second line we have the initial and final configuration. If the container is 3x3, the next 3 lines will be the initial configuration and the last 3 the final configuration.

3 3  
1 2 3 4 5 9 7 8 9  
1 2 3  
4 5 6  
7 8 9  
9 8 7  
6 5 4  
3 2 1  

## Output

The output is a file containing the minimum cost from initial configuration until final.

## How to

`./executar.sh input_file output_file`
