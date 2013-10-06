      ! A DFT using the same exact algorithm as dft.py
      ! Im using FORTRAN so it runs faster
      ! Jim Lakowski
      ! 10/04/2013
      ! Its fast (100x faster than dft.py)
      ! TODO :
      ! Change the integration method to 
      ! something more accurate (trapezoid, midpoint)
      ! 
      program dft

      ! Variable Declarations
      
      real, parameter :: Pi = 3.1415927
      integer, parameter :: M = 2000
      integer, parameter :: N = 1000
      
      real t(N)
      real f(N)
      real s(M)
      complex Ft(M)
      
      real dt 
      real to
      real so
      real ds
      real sf
      real etime
      real elapsed(2)
      real ttot
      complex J
      complex arg 
      complex acc 

      dt = 0.01 !timestep
      to = 0 !starting time
      so = -10 !starting frequncy
      ds = 0.01 !frequency step
      j = (0,1) ! the imaginary unit

      open(unit = 2, file="output.txt")
      ! set up the function for transforming
      ! 
      do a=1, N
         t(a) = to + a* dt
         
         !f(a) = cos(5* 2* Pi *t(a)) + cos( 3*2*Pi *t(a))
         !f(a) = exp(j* 5* 2* pi*t(a))
         
         !Unit Impulse
         if (a.lt.100) then
            f(a) = 1
         else
            f(a) = 0
         endif
         
      end do

      do b = 1, M
         acc = 0
         s(b) = so + b*ds
         do k = 1, N
            arg =  2 * Pi* j* s(b) * t(k)
            acc = acc + f(k)*exp(-arg)*dt
            
         end do
         Ft(b) = acc
         !print *,acc
         write(2,*) s(b),char(9),Ft(b)

       end do
       ttot = etime(elapsed)
       print *,'total time in fortran', ttot, 'seconds'
       end program dft
