#!/bin/python3                                                                                                                                                                                                                                
import os
import json

import argparse
parser = argparse.ArgumentParser(description='')

parser.add_argument('--run_number',type=int,default=6,help='ID number for this run.')
parser.add_argument('--batch_job' ,type=int,default=2, help='Batch ID Number in the bsub system.')

args = parser.parse_args()

from LDMX.Framework import ldmxcfg
from LDMX.Biasing import util

p=ldmxcfg.Process("sim")
p.run = args.run_number
p.maxEvents = 20000 #  20k                                                                                                                                                                                                                       

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

myGun = generators.gun('myGun')
myGun.particle = 'pi+'
#myGun.position = [ 0., 0., 220.5 ] # mm - front of the Ecal
myGun.position = [ 0., 0., 1.2] # mm - target
myGun.direction = [ 0., 0., 1]
#myGun.energy = 2.0 # GeV
#myGun.energy = 1.0 # GeV
myGun.energy = 0.1
sim = simulator.simulator("SingleGun")
sim.setDetector( 'ldmx-det-v12' , True )
sim.runNumber = 0
sim.description = "Single pi+ gun"
sim.beamSpotSmear = [20., 80., 0.] #mm                                                                                                                                                                                                        
sim.generators.append(myGun)
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
p.outputFiles = [ 'gun_pion_%.2f-GeV_20k_target_events_r%04d_b%d_104.root'%(myGun.energy,p.run,args.batch_job) ]
