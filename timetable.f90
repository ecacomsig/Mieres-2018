! schedule sessions at a conference such that there are few conflicting choices
! data from github.com/ecacomsig/Mieres-2018/ ->projects ->timetable_problem
! timetable_selection_fixed.txt
! compile with     gfortran -O timetable.f90 -o timetable

IMPLICIT NONE
INTEGER :: i,j,k,npart, mchoice, parallel, slots, votes,conflicts,itry,bestconflicts
INTEGER, ALLOCATABLE :: ivote(:,:),place(:),sindex(:),final(:)
REAL, ALLOCATABLE :: r(:)
CHARACTER :: name*8

CALL random_init_by_time
OPEN(1,file='data')
PRINT*,'number of participants, choices, parallel sessions, slots, votes?'
READ(1,*) npart, mchoice, parallel, slots, votes
PRINT '(a,5(i0,x))',' npart, mchoice, parallel, slots, votes= ',npart, mchoice, parallel, slots, votes

i=MAX(parallel,mchoice-parallel*slots)  ! storage for numbers in result lines
ALLOCATE(ivote(votes,npart),place(mchoice),sindex(mchoice),r(2),final(i))

PRINT '(a,i0,a,i0,a)',' for each participant, read ',votes,' numbers between 1 and ',mchoice,' from ''data'''

! read data and make sure there are no duplicate votes, and no votes outside range

DO i=1,npart
  READ(1,*) name,ivote(:,i)
!  PRINT*,ivote(:,i)
  IF (ANY(ivote(:,i)<1).OR.ANY(ivote(:,i)>mchoice)) PRINT*,'invalid',ivote(:,i)
  DO j=1,votes-1
    DO k=j+1,votes
      IF (ivote(j,i)==ivote(k,i)) PRINT*,'duplicate; i, votes=',i,ivote(:,i)
    END DO
  END DO
END DO

! 
! 1. starting configuration: assign sessions to the parallel*slots
! 2. count how many of the votes cannot be satisfied because some sessions are parallel, or unscheduled
! 3. randomly swap two sessions and check if this reduces the conflicts

! 1. starting configuration and assignment to slots:

place=(/(i,i=1,mchoice)/)
  
DO i=1,mchoice
  IF (i>parallel*slots) THEN            ! session not to be scheduled
    sindex(i)=0                                
  ELSE
    sindex(i)=(i-1)/parallel+1          ! which slot?
  END IF
END DO

! 2. evaluate conflicts:

CALL countconflicts(npart,votes,mchoice,sindex,ivote,conflicts)
PRINT*,'starting number of conflicts:',conflicts
bestconflicts=conflicts

! 3. try to improve by random swaps

itry=1
DO
  CALL RANDOM_NUMBER(r)
  i=r(1)*mchoice+1
  j=r(2)*mchoice+1
  IF (sindex(i)==sindex(j)) CYCLE  ! no point in swapping if same slot
  CALL swap(place(i),place(j))     ! swap position of i and j
  CALL swap(sindex(i),sindex(j))   ! ... and their slots 
!print*,i,j,place(i),place(j),sindex(i),sindex(j)
! if the runtime is a concern, then the countconflicts routine could be optimized
! to account for the fact that below only two sessions changed, rather than all.
  CALL countconflicts(npart,votes,mchoice,sindex,ivote,conflicts)
  itry=itry+1
  IF (conflicts<bestconflicts) THEN
    bestconflicts=conflicts
    PRINT*,'improved solution - ntry, conflicts:',itry,conflicts
  ELSE IF (conflicts==bestconflicts) THEN
! this is equally good - keep the new order and go on from there. This avoids local minima.
  ELSE                  ! if worse, swap back
    CALL swap(place(i),place(j))
    CALL swap(sindex(i),sindex(j))
  END IF

  IF (itry==100000) EXIT
END DO
PRINT*
PRINT*,'done 100000 trials. Result:'
! output of results:
DO i=0,slots
  k=0
  DO j=1,mchoice
    IF (sindex(place(j))==i) THEN
      k=k+1
      final(k)=place(j)
    END IF
  END DO
  IF (i==0) THEN
    PRINT '(a,10000(x,i0))',' unscheduled:',final(:k)
  ELSE 
    PRINT '(a,i4,a,1000i5)',' slot',i,':',final(:k)
  END IF
END DO    

END

SUBROUTINE swap(i,j)
INTEGER i,j,k
k=i
i=j
j=k
END SUBROUTINE swap

SUBROUTINE countconflicts(npart,votes,mchoice,sindex,ivote,conflicts)
IMPLICIT NONE
INTEGER, INTENT(IN) :: npart,votes,mchoice,sindex(mchoice),ivote(votes,npart)
INTEGER, INTENT(OUT) :: conflicts
INTEGER :: i,j,k

conflicts=0
DO i=1,npart
  DO j=1,votes
    IF (sindex(ivote(j,i))==0) THEN   ! has this session been scheduled at all?
      conflicts=conflicts+1
      CYCLE
    END IF
    DO k=j+1,votes   ! is there a conflict with another session we want to see?
      IF (sindex(ivote(j,i))==sindex(ivote(k,i))) conflicts=conflicts+1
    END DO
  END DO
END DO
END SUBROUTINE countconflicts

SUBROUTINE random_init_by_time
IMPLICIT NONE
INTEGER :: size,values(8)
INTEGER, ALLOCATABLE :: seed(:)

CALL RANDOM_SEED(SIZE=size)
ALLOCATE(seed(size))
seed=1
CALL DATE_AND_TIME(VALUES=values)
seed(1)=values(8)
seed(size)=values(8)*values(7)*values(6)
CALL RANDOM_SEED(PUT=seed)
END SUBROUTINE random_init_by_time
