import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

###2018
setFile = "fcncTriLepton/2018.yaml"
hlt_MC2018 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer18")
for dataset in ['EGamma', 'DoubleMuon', 'SingleMuon', 'MuonEG', 'Tau']:
    for e in "ABCD":
        vars()['hlt_Run2018%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2018.%s" % x, doFilter=True)
