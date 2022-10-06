#!/bin/python3                                                                                                                                                                                                                                
import os
import json

import argparse
parser = argparse.ArgumentParser(description='')

parser.add_argument('--run_number',type=int,default=9,help='ID number for this run.')
parser.add_argument('--batch_job' ,type=int,default=2, help='Batch ID Number in the bsub system.')

args = parser.parse_args()

from LDMX.Framework import ldmxcfg
from LDMX.Biasing import util

p=ldmxcfg.Process("sim")
p.run = args.run_number
#p.maxEvents = 1
p.maxEvents = 50000 #  20k

from LDMX.Ecal import EcalGeometry
geom = EcalGeometry.EcalGeometryProvider.getInstance()
import LDMX.Ecal.ecal_hardcoded_conditions

from LDMX.Hcal import HcalGeometry
geom = HcalGeometry.HcalGeometryProvider.getInstance()
import LDMX.Hcal.hcal_hardcoded_conditions

from LDMX.Ecal import digi as ecal_digi
from LDMX.Hcal import digi as hcal_digi

from LDMX.SimCore import simulator
from LDMX.SimCore import generators
p.libraries.append("libSimCore.so")

# gps
emin = 100 # 100 MeV
emax = 2000 # 2 GeV
gpsCmds=[
    "/gps/particle kaon+",
    "/gps/direction 0 0 1",
    "/gps/ene/type Lin",
    "/gps/ene/min %.2f MeV"%emin, 
    "/gps/ene/max %.2f MeV"%emax,
    "/gps/ene/gradient 0.",
    "/gps/ene/intercept 2.",
    "/gps/pos/type Point",
    "/gps/ang/type iso",
    "/gps/pos/centre 0 0 1.2 mm", # just after target
]

myGPS = generators.gps( 'myGPS' , gpsCmds )

sim = simulator.simulator("SingleGPS")
sim.setDetector( 'ldmx-det-v12' , True )
sim.runNumber = 0
sim.description = "Single kaon gps"
sim.beamSpotSmear = [20., 80., 0.] #mm
sim.generators.append(myGPS)
sim.actions.extend([
     util.DecayChildrenKeeper([2212,211,-211])
])

p.sequence=[ sim,
             ecal_digi.EcalDigiProducer(),
             ecal_digi.EcalRecProducer(),
             hcal_digi.HcalDigiProducer(),
             hcal_digi.HcalRecProducer(),
             ]

p.termLogLevel = 0
p.logFrequency = 1000
p.outputFiles = [ 'gps_kplus_%.2f-%.2fMeV_50k_target_events_r%04d_b%d_104.root'%(emin,emax,p.run,args.batch_job) ]
