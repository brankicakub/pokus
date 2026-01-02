BINDIR = bin
FC = gfortran
FFLAGS = -std=f2008 -O2
SRC = src

.PHONY: all build run clean

all: build

build:
	mkdir -p $(BINDIR)
	$(FC) $(FFLAGS) -o $(BINDIR)/plotter $(SRC)/main.f90

run: build
	mkdir -p ../output
	$(BINDIR)/plotter ../data/sample.csv --auto
	bash run_plot.sh output/plot.plt

clean:
	rm -f $(BINDIR)/plotter
