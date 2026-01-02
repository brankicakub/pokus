program csv_plotter
  implicit none
  character(len=512) :: filename
  integer :: iargc
  character(len=2048) :: header_line
  logical :: ok
  character(len=:), allocatable :: header
  character(len=256), allocatable :: names(:)
  integer :: ncols, i
  character(len=256) :: answer
  integer :: xcol, ycol
  logical :: auto
  character(len=64) :: arg2

  call get_command_argument(1, filename)
  if (len_trim(filename) == 0) then
    write(*,*) 'Enter path to CSV file:'
    read(*,'(A)') filename
  end if

  open(unit=10, file=trim(filename), status='old', action='read', iostat=i)
  if (i /= 0) then
    write(*,'(A)') 'Error: cannot open file '//trim(filename)
    stop 1
  end if

  read(10,'(A)', iostat=i) header_line
  if (i /= 0) then
    write(*,'(A)') 'Error: cannot read header'
    stop 1
  end if

  call split_csv_header(header_line, names, ncols)
  call get_command_argument(2, arg2)
  auto = .false.
  if (len_trim(arg2) > 0) then
    if (trim(arg2) == '--auto' .or. trim(arg2) == '-a') auto = .true.
  end if
  write(*,*) 'Found columns:'
  do i=1,ncols
    write(*,'(I3,2X,A)') i, trim(names(i))
  end do

  if (auto) then
    xcol = 1
    if (ncols >= 2) then
      ycol = 2
    else
      ycol = 1
    end if
    write(*,'(A,I0,A,I0)') 'Auto mode: using columns ', xcol, ' (X) and ', ycol, ' (Y)'
  else
    write(*,*) 'Enter X column (name or index):'
    read(*,'(A)') answer
    call select_column(answer, names, ncols, xcol)

    write(*,*) 'Enter Y column (name or index):'
    read(*,'(A)') answer
    call select_column(answer, names, ncols, ycol)
  end if

  call write_two_column_data(10, xcol, ycol)

  close(10)

  call write_gnuplot_script('output/plot.plt', 'output/tmpdata.dat', trim(names(xcol)), trim(names(ycol)))

  write(*,'(A)') 'Wrote output/tmpdata.dat and output/plot.plt. Run fortran/run_plot.sh to render PDF and PNG.'
contains

  subroutine split_csv_header(line, names, n)
    character(len=*), intent(in) :: line
    character(len=256), allocatable, intent(out) :: names(:)
    integer, intent(out) :: n
    integer :: pos, start, lenl, idx
    character(len=256) :: token
    lenl = len_trim(line)
    start = 1
    idx = 0
    do
      pos = index(line(start:lenl), ',')
      if (pos == 0) then
        token = adjustl(line(start:lenl))
        idx = idx + 1
        call add_name(token, names, idx)
        exit
      else
        token = adjustl(line(start:start+pos-2))
        idx = idx + 1
        call add_name(token, names, idx)
        start = start + pos
      end if
    end do
    n = idx
  end subroutine split_csv_header

  subroutine add_name(token, names, idx)
    character(len=*), intent(in) :: token
    character(len=256), allocatable, intent(inout) :: names(:)
    integer, intent(in) :: idx
    if (.not. allocated(names)) then
      allocate(names(1))
    else
      if (size(names) < idx) then
        call resize_names(names, idx)
      end if
    end if
    names(idx) = trim(adjustl(token))
  end subroutine add_name

  subroutine resize_names(names, newsize)
    character(len=256), allocatable, intent(inout) :: names(:)
    integer, intent(in) :: newsize
    character(len=256), allocatable :: tmp(:)
    integer :: old
    if (.not. allocated(names)) then
      allocate(names(newsize))
      names = ''
      return
    end if
    old = size(names)
    allocate(tmp(newsize))
    tmp = ''
    tmp(1:old) = names
    names = tmp
  end subroutine resize_names

  subroutine select_column(answer, names, n, col)
    character(len=*), intent(in) :: answer
    character(len=256), intent(in) :: names(:)
    integer, intent(in) :: n
    integer, intent(out) :: col
    integer :: i, val, ios
    character(len=256) :: a
    a = adjustl(trim(answer))
    read(a,*,iostat=ios) val
    if (ios == 0) then
      if (val >=1 .and. val <= n) then
        col = val
        return
      end if
    end if
    do i=1,n
      if (trim(names(i)) == trim(a)) then
        col = i
        return
      end if
    end do
    write(*,*) 'Could not parse column; defaulting to 1'
    col = 1
  end subroutine select_column

  subroutine write_two_column_data(unit_in, xcol, ycol)
    integer, intent(in) :: unit_in, xcol, ycol
    character(len=1024) :: line
    integer :: ios
    character(len=32) :: tok
    integer :: i, start, pos, n
    real :: xv, yv
    integer :: outu
    integer :: row
    logical :: okx, oky
    call execute_command_line('mkdir -p output')
    open(unit=20, file='output/tmpdata.dat', status='replace', action='write', iostat=ios)
    if (ios /= 0) then
      write(*,'(A)') 'Error: cannot open output/tmpdata.dat for writing'
      stop 1
    end if
    row = 0
    do
      read(unit_in,'(A)',iostat=ios) line
      if (ios /= 0) exit
      row = row + 1
      call get_token(line, xcol, xv, okx)
      call get_token(line, ycol, yv, oky)
      if (.not. oky) cycle
      if (.not. okx) then
        xv = real(row)
      end if
      write(20,'(F12.6,1X,F12.6)') xv, yv
    end do
    close(20)
  end subroutine write_two_column_data

  subroutine get_token(line, idx, val, ok)
    character(len=*), intent(in) :: line
    integer, intent(in) :: idx
    real, intent(out) :: val
    logical, intent(out) :: ok
    integer :: i, start, pos, lenl, count
    character(len=256) :: token
    lenl = len_trim(line)
    start = 1
    count = 0
    ok = .false.
    do i=1,lenl
      if (line(i:i) == ',') then
        count = count + 1
      end if
    end do
    ! simple extract
    start = 1
    count = 0
    do i=1,idx-1
      pos = index(line(start:lenl), ',')
      if (pos == 0) then
        start = lenl+1
        exit
      else
        start = start + pos
      end if
    end do
    if (start > lenl) then
      ok = .false.
      return
    end if
    pos = index(line(start:lenl), ',')
    if (pos == 0) then
      token = adjustl(line(start:lenl))
    else
      token = adjustl(line(start:start+pos-2))
    end if
    read(token,*,iostat=i) val
    if (i == 0) then
      ok = .true.
    else
      ok = .false.
    end if
  end subroutine get_token

  subroutine write_gnuplot_script(outplt, datafile, xname, yname)
    character(len=*), intent(in) :: outplt, datafile, xname, yname
    integer :: u, ios
    open(unit=30, file=outplt, status='replace', action='write', iostat=ios)
    if (ios /= 0) then
      write(*,'(A)') 'Error: cannot write gnuplot script'
      return
    end if
    write(30,'(A)') "set terminal pdfcairo size 11in,8in font 'Helvetica,12'"
    write(30,'(A)') "set output 'output/plot.pdf'"
    write(30,'(A)') "set datafile separator whitespace"
    write(30,'(A)') "set title '"//trim(xname)//" vs "//trim(yname)//"'"
    write(30,'(A)') "plot '"//trim(datafile)//"' using 1:2 with lines lw 2 title '"//trim(yname)//"'"
    write(30,'(A)') "set terminal pngcairo size 1200,600" 
    write(30,'(A)') "set output 'output/plot.png'"
    write(30,'(A)') "replot"
    close(30)
  end subroutine write_gnuplot_script

end program csv_plotter
