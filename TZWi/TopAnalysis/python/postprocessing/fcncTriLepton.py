import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCTriLepton(Module, object):
    def __init__(self, *args, **kwargs):
        #super(FCNCTriLepton, self).__init__(*args, **kwargs)
        self.mode = kwargs.get("mode")
#        self.eleIdName = kwargs.get("eleId") if "eleId" in kwargs else "cutBased"
#        self.eleVidMap = kwargs.get("eleVidMap") if "eleVidMap" in kwargs else "vidNestedWPBitmap"
#        self.doNonPromptLepton = kwargs.get("doNonPromptLepton") if "doNonPromptLepton" in kwargs else False

        if "/FCNCTriLeptonCppWorker_cc.so" not in  ROOT.gSystem.GetLibraries():
            print "Load C++ FCNCTriLepton worker module"
            base = os.getenv("NANOAODTOOLS_BASE")
            if base:
                ROOT.gROOT.ProcessLine(".L %s/src/FCNCTriLeptonCppWorker.cc+O" % base)
            else:
                base = "%s/src/TZWi/TopAnalysis"%os.getenv("CMSSW_BASE")
                ROOT.gSystem.Load("libPhysicsToolsNanoAODTools.so")
                ROOT.gSystem.Load("libTZWiTopAnalysis.so")
                ROOT.gROOT.ProcessLine(".L %s/interface/FCNCTriLeptonCppWorker.h" % base)
        pass
    def beginJob(self):
#        self.worker = ROOT.FCNCTriLeptonCppWorker(self.mode, self.doNonPromptLepton)
        self.worker = ROOT.FCNCTriLeptonCppWorker(self.mode)
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
#        for objName in ["Reco_Electron"]:
#            for varName in ["pt", "eta", "phi", "mass", "pfRelIso03_all", "deltaEtaSC"]:
#                self.out.branch("%s_%s" % (objName, varName), "F", lenVar="nRecoElectron")
#            for varName in ["charge", self.eleIdName, self.eleVidMap]:
#                self.out.branch("%s_%s" % (objName, varName), "I", lenVar="nRecoElectron")
#        for objName in ["Reco_Muon"]:
#            for varName in ["pt", "eta", "phi", "mass", "pfRelIso04_all"]:
#                self.out.branch("%s_%s" % (objName, varName), "F", lenVar="nRecoMuon")
#            for varName in ["charge"]:
#                self.out.branch("%s_%s" % (objName, varName), "I", lenVar="nRecoMuon")
#            for varName in ["tightId", "isGlobal", "isPFcand", "isTracker"]:
#                self.out.branch("%s_%s" % (objName, varName), "O", lenVar="nRecoMuon")

#        for objName in ["Reco_Electron"]:
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "F", lenVar="nRecoElectron")
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "I", lenVar="nRecoElectron")
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "O", lenVar="nRecoElectron")
#        for objName in ["Reco_Muon"]:
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "F", lenVar="nRecoMuon")
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "I", lenVar="nRecoMuon")
#            for varName in []:
#                self.out.branch("%s_%s" % (objName, varName), "O", lenVar="nRecoMuon")

#        self.out.branch("MET_pt", "F")
#        self.out.branch("MET_phi", "F")
#        self.out.branch("Electron1_pdgId", "I")
#        self.out.branch("Electron2_pdgId", "I")
#        self.out.branch("Electron3_pdgId", "I")
#        self.out.branch("Muon1_pdgId", "I")
#        self.out.branch("Muon2_pdgId", "I")
#        self.out.branch("Muon3_pdgId", "I")
#        self.out.branch("LeadingLepton_pt", "F")
#        self.out.branch("TriLepton_mass", "F")
#        self.out.branch("TriLepton_pt", "F")
#        self.out.branch("TriLepton_WleptonZdPhi", "F")
#        self.out.branch("TriLepton_WleptonZdR", "F")
#        self.out.branch("Z_charge", "I")
#        self.out.branch("nVetoLepton", "i")
        self.out.branch("nGoodLeptonRemake", "i")
#        self.out.branch("GoodElectronCode", "I")
#        self.out.branch("GoodMuonCode", "I")
#        self.out.branch("nGoodElectron", "i")
#        self.out.branch("nGoodMuon", "i")
#        #self.out.branch("nGoodJet", "i")
#        self.out.branch("GoodJet_index", "i", lenVar="nGoodJet")
#        for varName in ["pt", "eta", "phi", "mass", "DeepFlavB"]:
#            self.out.branch("GoodJet_%s" % varName, "F", lenVar="nGoodJet")
#        self.out.branch("nBjet", "i")
#        self.out.branch("W_MT", "F")

        self.initReaders(inputTree)
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def initReaders(self,tree):

#        self.b_MET_pt = tree.valueReader("MET_pt")
#        self.b_MET_phi = tree.valueReader("MET_phi")

#        objName = "Electron"
#        for varName in ["pt", "eta", "phi", "mass", "pfRelIso03_all", "deltaEtaSC", "charge", self.eleIdName, self.eleVidMap]:
#            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))
        objName = "Electron"
        for varName in ["pt", "eta", "isPFcand", "lostHits", "dxy", "dz", "sip3d",
                        "miniPFRelIso_all", "sieie", "hoe", "eInvMinusPInv", "convVeto", "deltaEtaSC"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

#        objName = "Muon"
#        for varName in ["pt", "eta", "phi", "mass", "pfRelIso04_all", "charge", "tightId", "isGlobal", "isPFcand", "isTracker"]:
#            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))
        objName = "Muon"
        for varName in ["pt", "eta", "isPFcand", "isTracker", "isGlobal", "dxy", "dz", "sip3d",
                        "miniPFRelIso_all", "mediumId"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

#        objName = "Jet"
#        setattr(self, "b_n%s" % objName, tree.valueReader("n%s" % objName))
#        for varName in ["pt", "eta", "phi", "mass",
#                        "jetId", "puId", "btagDeepFlavB",]:
#            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

        objName = "Tau"
        for varName in ["pt", "eta", "dz", "decayMode",
                        "idDeepTau2017v2p1VSjet", "idDeepTau2017v2p1VSe", "idDeepTau2017v2p1VSmu"]:
            setattr(self, "b_%s_%s" % (objName, varName), tree.arrayReader("%s_%s" % (objName, varName)))

#        self.worker.setMET(self.b_MET_pt, self.b_MET_phi)
#        self.worker.setElectrons(self.b_Electron_pt, self.b_Electron_eta, self.b_Electron_phi, self.b_Electron_mass,
#                                 self.b_Electron_pfRelIso03_all, self.b_Electron_deltaEtaSC,
#                                 self.b_Electron_charge, getattr(self, 'b_Electron_%s' % self.eleIdName), getattr(self, 'b_Electron_%s' % self.eleVidMap))
        self.worker.setElectrons(self.b_Electron_pt, self.b_Electron_eta, self.b_Electron_isPFcand, self.b_Electron_lostHits,
                                 self.b_Electron_dxy, self.b_Electron_dz, self.b_Electron_sip3d, self.b_Electron_miniPFRelIso_all,
                                 self.b_Electron_sieie, self.b_Electron_hoe, self.b_Electron_eInvMinusPInv, self.b_Electron_convVeto,
                                 self.b_Electron_deltaEtaSC)
#        self.worker.setMuons(self.b_Muon_pt, self.b_Muon_eta, self.b_Muon_phi, self.b_Muon_mass, self.b_Muon_pfRelIso04_all,
#                             self.b_Muon_charge,
#                             self.b_Muon_tightId, self.b_Muon_isGlobal, self.b_Muon_isPFcand, self.b_Muon_isTracker)
        self.worker.setMuons(self.b_Muon_pt, self.b_Muon_eta, self.b_Muon_isPFcand, self.b_Muon_isTracker, self.b_Muon_isGlobal,
                             self.b_Muon_dxy, self.b_Muon_dz, self.b_Muon_sip3d, self.b_Muon_miniPFRelIso_all, self.b_Muon_mediumId)
#        self.worker.setJets(self.b_Jet_pt, self.b_Jet_eta, self.b_Jet_phi, self.b_Jet_mass,
#                            self.b_Jet_jetId, self.b_Jet_btagDeepFlavB)
        self.worker.setTaus(self.b_Tau_pt, self.b_Tau_eta, self.b_Tau_dz, self.b_Tau_decayMode,
                            self.b_Tau_idDeepTau2017v2p1VSjet, self.b_Tau_idDeepTau2017v2p1VSe, self.b_Tau_idDeepTau2017v2p1VSmu)
        self._ttreereaderversion = tree._ttreereaderversion

        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if event._tree._ttreereaderversion > self._ttreereaderversion:
            self.initReaders(event._tree)
        self.worker.analyze()

        for varName in ["nGoodLeptonRemake"]:
            setattr(event._tree, "b_out_%s" % (varName), getattr(self.worker, 'get_%s' % (varName))())
            self.out.fillBranch(varName, getattr(event._tree, "b_out_%s" % varName))

#        for objName in ["Reco_Electron"]:
#            for varName in ["pt", "eta", "phi", "mass", "pfRelIso03_all", "deltaEtaSC", "charge", self.eleIdName, self.eleVidMap]:
#                setattr(event._tree, "b_out_%s_%s" % (objName, varName), getattr(self.worker, 'get_%s_%s' % (objName, varName))())
#                self.out.fillBranch("%s_%s" % (objName, varName), getattr(event._tree, 'b_out_%s_%s' % (objName, varName)))
#        for objName in ["Reco_Muon"]:
#            for varName in ["pt", "eta", "phi", "mass", "pfRelIso04_all", "charge", "tightId", "isGlobal", "isPFcand", "isTracker"]:
#                setattr(event._tree, "b_out_%s_%s" % (objName, varName), getattr(self.worker, 'get_%s_%s' % (objName, varName))())
#                self.out.fillBranch("%s_%s" % (objName, varName), getattr(event._tree, 'b_out_%s_%s' % (objName, varName)))
#        ## Special care for nGoodJet
#        setattr(event._tree, "b_out_nGoodJet", self.worker.get_nGoodJet())

        return True

#fcnc_NANOAOD_2016 = lambda : FCNCTriLepton(mode="NANOAOD", eleId="cutBased", eleVidMap="vidNestedWPBitmap")
fcnc_NANOAOD_2016 = lambda : FCNCTriLepton(mode="NANOAOD")
