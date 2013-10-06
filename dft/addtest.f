      program addtest
      
     
      real a
      real dt
      real timestart
      real timestop
      complex arg
      complex ans
      complex J
      parameter xI = (0,1)     
      parameter Pi = 3.141592653589
      dt = 0.78539816339
      a = 0
      J = (0,1)

      timestart = system_clock()

      do i=1, 8
         a = i * dt
         print *,a
         ans = cexp( J* a)
         print *,ans
      end do
      timestop = system
      end program addtest
