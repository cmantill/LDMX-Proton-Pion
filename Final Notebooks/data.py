import uproot
import awkward as ak
import os
import psutil

SimParticle_attrs = ['pdgID','trkID','px','py','pz','e','mass','vx','vy','vz','electrone']
SimParticle_dau_attrs = ['pdgID','z','px','py','pz','e','mompdgID','mome','momdecay', 'electrone']

branches = {
    "n": ['Sim_PNParticle'], 
    "Sim_PNParticle": SimParticle_attrs,
    "Sim_PNParticle_dau1": SimParticle_dau_attrs,
    "Sim_PNParticle_dau2": SimParticle_dau_attrs,
}

def getData(fnames="", treeName="Events", chunks=False):
    branchlist = []
    for collection, attrs in branches.items():
        branchlist += [collection+"_"+attr for attr in attrs]
    if chunks: ldmx_dict = uproot.iterate(fnames+":"+treeName, branchlist)
    else: ldmx_dict = uproot.lazy(fnames+":"+treeName, branchlist)
    return ldmx_dict

def repackage(ldmx_dict):
    evt_dict={}
    for collection in branches:    
        coll_dict={}
        for attr in branches[collection]:
            bname = "{}_{}".format(collection, attr)
            coll_dict[attr] = ldmx_dict[bname]
        evt_dict[collection] = ak.zip(coll_dict)        
    ldmx_events = ak.zip(evt_dict, depth_limit=1)
    return ldmx_events
