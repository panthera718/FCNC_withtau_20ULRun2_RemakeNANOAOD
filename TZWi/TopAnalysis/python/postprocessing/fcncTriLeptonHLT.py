import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

###2016
setFile = "fcncTriLepton/2016.yaml"
hlt_MC2016 = lambda f=setFile: CombineHLT(fileName=f, hltSet="RunIISummer16")
for dataset in ['DoubleEG', 'SingleElectron', 'DoubleMuon', 'SingleMuon', 'MuonEG', 'Tau']:
    for e in "FGH":
        vars()['hlt_Run2016%s_%s' % (e, dataset)] = lambda x=dataset, f=setFile: CombineHLT(fileName=f, hltSet="Run2016.%s" % x, doFilter=True)
