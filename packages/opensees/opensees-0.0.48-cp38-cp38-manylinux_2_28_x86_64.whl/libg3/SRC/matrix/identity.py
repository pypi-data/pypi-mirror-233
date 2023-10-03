import numpy as np
import sympy as sp

one3 = 1/3
two3 = 2/3

  # form rank4 IbunI 
IbunI = np.zeros((3,3,3,3))    ; # rank 4 I bun I

IbunI [0][0] [0][0] = 1.0 ;
IbunI [0][0] [1][1] = 1.0 ;
IbunI [0][0] [2][2] = 1.0 ;
IbunI [1][1] [0][0] = 1.0 ;
IbunI [1][1] [1][1] = 1.0 ;
IbunI [1][1] [2][2] = 1.0 ;
IbunI [2][2] [0][0] = 1.0 ;
IbunI [2][2] [1][1] = 1.0 ;
IbunI [2][2] [2][2] = 1.0 ;

# form rank4 IIdev
IIdev = np.zeros((3,3,3,3))   #  rank 4 deviatoric projector
IIdev [0][0] [0][0] =  two3 ; #  0.666667 
IIdev [0][0] [1][1] = -one3 ; # -0.333333 
IIdev [0][0] [2][2] = -one3 ; # -0.333333 

IIdev [0][1] [0][1] = 0.5 ;
IIdev [0][1] [1][0] = 0.5 ;

IIdev [0][2] [0][2] = 0.5 ;
IIdev [0][2] [2][0] = 0.5 ;

IIdev [1][0] [0][1] = 0.5 ;
IIdev [1][0] [1][0] = 0.5 ;
IIdev [1][1] [0][0] = -one3 ; # -0.333333 
IIdev [1][1] [1][1] =  two3 ; #  0.666667 
IIdev [1][1] [2][2] = -one3 ; # -0.333333 
IIdev [1][2] [1][2] = 0.5 ;
IIdev [1][2] [2][1] = 0.5 ;

IIdev [2][0] [0][2] = 0.5 ;
IIdev [2][0] [2][0] = 0.5 ;
IIdev [2][1] [1][2] = 0.5 ;
IIdev [2][1] [2][1] = 0.5 ;
IIdev [2][2] [0][0] = -one3 ; # -0.333333 
IIdev [2][2] [1][1] = -one3 ; # -0.333333 
IIdev [2][2] [2][2] =  two3 ; #  0.666667 

# print(IbunI)
# print(IIdev)
print(np.array2string(IbunI, separator=', ', precision=3))
print(np.array2string(IIdev, separator=', ', precision=3))
