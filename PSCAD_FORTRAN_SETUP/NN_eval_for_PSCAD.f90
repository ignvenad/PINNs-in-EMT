! Define component with PSCAD's component wizard and add the file name input as FNAME
 #STORAGE RTCF:460
 #LOCAL REAL Scaler 5
 #LOCAL REAL Shifter 5
 #LOCAL REAL W1_1 56
 #LOCAL REAL W1_2 56
 #LOCAL REAL W1_3 56
 #LOCAL REAL W1_4 56
 #LOCAL REAL W1_5 56
 #LOCAL REAL B1 56
 #LOCAL REAL W2_1 56
 #LOCAL REAL W2_2 56
 #LOCAL REAL B2 2

 #STORAGE REAL:3
 #LOCAL INTEGER MY_STORF 1
 #LOCAL REAL x1_prev 1
 #LOCAL REAL x2_prev 1
 #LOCAL REAL vq_prev 1

 #LOCAL INTEGER I_sweep1 1
 #LOCAL INTEGER I_gather 1
 #LOCAL REAL valpha 1
 #LOCAL REAL vbeta 1
 #LOCAL REAL x1_0_n 1
 #LOCAL REAL x2_0_n 1
 #LOCAL REAL vq_0_n 1
 #LOCAL REAL val_n 1
 #LOCAL REAL vbe_n 1

 #LOCAL REAL sweep1 56
 #LOCAL REAL L1 56

 #LOCAL REAL gather_x1 1
 #LOCAL REAL gather_x2 1
 #LOCAL REAL cumin_x1 1
 #LOCAL REAL cumin_x2 1

 #BEGIN
      DO I_BEGIN = 0, 459
       RTCF(NRTCF+I_BEGIN) = 0.0
      ENDDO
      OPEN(UNIT=9, FILE='C:\PSCAD_projects\NNETs\$(FNAME)\NN_PSCAD_params.txt', STATUS='OLD', ACTION='READ')
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=0,4)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=5,9)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=10,65)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=66,121)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=122,177)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=178,233)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=234,289)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=290,345)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=346,401)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=402,457)
      READ(UNIT=9, FMT=*) (RTCF(NRTCF+I_BEGIN), I_BEGIN=458,459)
      CLOSE(UNIT=9)
      NRTCF = NRTCF + 460
 #ENDBEGIN

 Scaler(1:5) = RTCF(NRTCF+0 : NRTCF+4)
 Shifter(1:5) = RTCF(NRTCF+5 : NRTCF+9)
 W1_1(1:56) = RTCF(NRTCF+10 : NRTCF+65)
 W1_2(1:56) = RTCF(NRTCF+66 : NRTCF+121)
 W1_3(1:56) = RTCF(NRTCF+122 : NRTCF+177)
 W1_4(1:56) = RTCF(NRTCF+178 : NRTCF+233)
 W1_5(1:56) = RTCF(NRTCF+234 : NRTCF+289)
 B1(1:56) = RTCF(NRTCF+290 : NRTCF+345)
 W2_1(1:56) = RTCF(NRTCF+346 : NRTCF+401)
 W2_2(1:56) = RTCF(NRTCF+402 : NRTCF+457)
 B2(1) = RTCF(NRTCF+458)
 B2(2) = RTCF(NRTCF+459)
 NRTCF = NRTCF + 460

 MY_STORF = NSTORF
 NSTORF   = NSTORF + 3

 IF (TIMEZERO) THEN
      $x1 = 0.0
      $x2 = 0.0
      $vq = 0.0
 ELSE
      valpha = TWO_3RD * ($va - $vb/2.0 - $vc/2.0)
      vbeta  = TWO_3RD * (SQRT_3/2.0*$vb - SQRT_3/2.0*$vc)
      x1_prev = STORF(MY_STORF)
      x2_prev = STORF(MY_STORF+1)
      vq_prev = STORF(MY_STORF+2)
      x1_0_n = Scaler(1) * x1_prev + Shifter(1)
      x2_0_n = Scaler(2) * x2_prev + Shifter(2)
      vq_0_n = Scaler(3) * vq_prev + Shifter(3)
      val_n  = Scaler(4) * valpha + Shifter(4)
      vbe_n  = Scaler(5) * vbeta + Shifter(5)

            DO I_sweep1 = 1, 56
       sweep1(I_sweep1) = W1_1(I_sweep1) * x1_0_n + &
               W1_2(I_sweep1) * x2_0_n + &
               W1_3(I_sweep1) * vq_0_n + &
               W1_4(I_sweep1) * val_n  + &
               W1_5(I_sweep1) * vbe_n
            ENDDO

      L1(1:56) = TANH( sweep1(1:56) + B1(1:56) )

      gather_x1 = 0.0
      gather_x2 = 0.0
      DO I_gather = 1, 56
       gather_x1 = gather_x1 + W2_1(I_gather) * L1(I_gather)
       gather_x2 = gather_x2 + W2_2(I_gather) * L1(I_gather)
      ENDDO
      cumin_x1 = gather_x1 + B2(1)
      cumin_x2 = gather_x2 + B2(2)
      $x1 = cumin_x1 * $step + x1_prev
      $x2 = MOD(cumin_x2 * $step + x2_prev, TWO_PI)
      $vq = -SIN($x2)*valpha + COS($x2)*vbeta
 ENDIF

            STORF(MY_STORF) = $x1
            STORF(MY_STORF+1) = $x2
            STORF(MY_STORF+2) = $vq
