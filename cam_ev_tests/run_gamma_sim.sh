#!/bin/bash

~/topas/bin/topas ~/topas/Kepler_Runs/KeplerPETScanner.txt
make reverse_kin
./reverse_kinimatics TruthTuple.phsp DetectorTuple.phsp sim_out 39 100 1
