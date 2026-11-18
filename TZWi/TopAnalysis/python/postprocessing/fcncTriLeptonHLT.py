import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

###2017
setFile = "fcncTriLepton/2017.yaml"
hlt_MC2017 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer17")
for dataset in ['DoubleEG', 'SingleElectron', 'DoubleMuon', 'SingleMuon', 'MuonEG', 'Tau']:
    for e in "BCDEF":
        vars()['hlt_Run2017%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2017.%s" % x, doFilter=True)
