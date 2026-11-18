import ROOT
import os
from math import sqrt
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class lepSFProducer(Module):
    def __init__(self, muonSelectionTag, electronSelectionTag, mode):
        if muonSelectionTag=="TightWP_2018":
            mu_f_BF = ["Efficiencies_muon_generalTracks_Z_Run2018_UL_ID.root","Efficiencies_muon_generalTracks_Z_Run2018_UL_ISO.root"]
            mu_f_GH = ["Efficiencies_muon_generalTracks_Z_Run2018_UL_ID.root","Efficiencies_muon_generalTracks_Z_Run2018_UL_ISO.root"]
            mu_h = ["NUM_TightID_DEN_TrackerMuons_abseta_pt",
                    "NUM_TightRelIso_DEN_TightIDandIPCut_abseta_pt"]
        if electronSelectionTag=="TightWP_2018":
            el_f_BF = ["egammaEffi.txt_Ele_Tight_EGM2D.root"]
            el_f_GH = ["egammaEffi.txt_Ele_Tight_EGM2D.root"]
            el_h = ["EGamma_SF2D"]
#        if mode=="ElElEl":
#            self.TrigSF = [0.9026, 0.9392, 1.0032, 1.0366]
#        elif mode=="MuElEl":
#            self.TrigSF = [0.9665, 0.9498, 1.0307, 1.0472]
#        elif mode=="ElMuMu":
#            self.TrigSF = [0.9785, 0.9714, 0.8809, 1.0669]
#        elif mode=="MuMuMu":
#            self.TrigSF = [1.0022, 1.0023, 1.0012, 1.0041]
#        else:
#            self.TrigSF = [1., 1., 1., 1.]
        tri_f_BF = ["TriggerSF_2018_UL.root"]
        tri_f_GH = ["TriggerSF_2018_UL.root"]
        tri_h = ["h2D_SF_ee_lepABpt_FullError","h2D_SF_mumu_lepABpt_FullError","h2D_SF_emu_lepABpt_FullError"]
        mu_f_BF = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_BF]
        mu_f_GH = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in mu_f_GH]
        el_f_BF = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in el_f_BF]
        el_f_GH = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in el_f_GH]
        tri_f_BF = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in tri_f_BF]
        tri_f_GH = ["%s/src/TZWi/TopAnalysis/data/leptonSF/" % os.environ['CMSSW_BASE'] + f for f in tri_f_GH]

        mu_f_ID_BF = [mu_f_BF[0]]
        mu_f_ID_GH = [mu_f_GH[0]]
        mu_h_ID = [mu_h[0]]
        mu_f_ISO_BF = [mu_f_BF[1]]
        mu_f_ISO_GH = [mu_f_GH[1]]
        mu_h_ISO = [mu_h[1]]

        tri_h_ElEl = [tri_h[0]]
        tri_h_MuMu = [tri_h[1]]
        tri_h_ElMu = [tri_h[2]]

        self.mu_f_BF = ROOT.std.vector(str)(len(mu_f_BF))
        self.mu_f_GH = ROOT.std.vector(str)(len(mu_f_GH))
        self.mu_h = ROOT.std.vector(str)(len(mu_f_BF))
        for i in range(len(mu_f_BF)): self.mu_f_BF[i] = mu_f_BF[i]; self.mu_h[i] = mu_h[i];
        for i in range(len(mu_f_GH)): self.mu_f_GH[i] = mu_f_GH[i];
        self.el_f_BF = ROOT.std.vector(str)(len(el_f_BF))
        self.el_f_GH = ROOT.std.vector(str)(len(el_f_GH))
        self.el_h = ROOT.std.vector(str)(len(el_f_BF))
        for i in range(len(el_f_BF)): self.el_f_BF[i] = el_f_BF[i]; self.el_h[i] = el_h[i];
        for i in range(len(el_f_GH)): self.el_f_GH[i] = el_f_GH[i];
#        self.tri_f_BF = ROOT.std.vector(str)(len(tri_f_BF))
#        self.tri_f_GH = ROOT.std.vector(str)(len(tri_f_GH))
#        self.tri_h = ROOT.std.vector(str)(len(tri_f_BF))
#        for i in range(len(tri_f_BF)): self.tri_f_BF[i] = tri_f_BF[i]; self.tri_h[i] = tri_h[i];
#        for i in range(len(tri_f_GH)): self.tri_f_GH[i] = tri_f_GH[i];
        self.mu_f_ID_BF = ROOT.std.vector(str)(len(mu_f_ID_BF))
        self.mu_f_ID_GH = ROOT.std.vector(str)(len(mu_f_ID_GH))
        self.mu_h_ID = ROOT.std.vector(str)(len(mu_f_ID_BF))
        for i in range(len(mu_f_ID_BF)): self.mu_f_ID_BF[i] = mu_f_ID_BF[i]; self.mu_h_ID[i] = mu_h_ID[i];
        for i in range(len(mu_f_ID_GH)): self.mu_f_ID_GH[i] = mu_f_ID_GH[i];
        self.mu_f_ISO_BF = ROOT.std.vector(str)(len(mu_f_ISO_BF))
        self.mu_f_ISO_GH = ROOT.std.vector(str)(len(mu_f_ISO_GH))
        self.mu_h_ISO = ROOT.std.vector(str)(len(mu_f_ISO_BF))
        for i in range(len(mu_f_ISO_BF)): self.mu_f_ISO_BF[i] = mu_f_ISO_BF[i]; self.mu_h_ISO[i] = mu_h_ISO[i];
        for i in range(len(mu_f_ISO_GH)): self.mu_f_ISO_GH[i] = mu_f_ISO_GH[i];

        self.tri_f_BF = ROOT.std.vector(str)(len(tri_f_BF))
        self.tri_f_GH = ROOT.std.vector(str)(len(tri_f_GH))
        self.tri_h_ElEl = ROOT.std.vector(str)(len(tri_f_BF))
        self.tri_h_MuMu = ROOT.std.vector(str)(len(tri_f_BF))
        self.tri_h_ElMu = ROOT.std.vector(str)(len(tri_f_BF))
        for i in range(len(tri_f_BF)):
            self.tri_f_BF[i] = tri_f_BF[i];
            self.tri_h_ElEl[i] = tri_h_ElEl[i];
            self.tri_h_MuMu[i] = tri_h_MuMu[i];
            self.tri_h_ElMu[i] = tri_h_ElMu[i];
        for i in range(len(tri_f_GH)):
            self.tri_f_GH[i] = tri_f_GH[i];

        if "/LeptonEfficiencyCorrector_cc.so" not in ROOT.gSystem.GetLibraries():
            print "Load C++ Worker"
            ROOT.gROOT.ProcessLine(".L %s/src/TZWi/TopAnalysis/python/postprocessing/helpers/LeptonEfficiencyCorrector.cc+" % os.environ['CMSSW_BASE'])
    def beginJob(self):
        self._worker_mu_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_BF,self.mu_h)
        self._worker_mu_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_GH,self.mu_h)
        self._worker_el_BF = ROOT.LeptonEfficiencyCorrector(self.el_f_BF,self.el_h)
        self._worker_el_GH = ROOT.LeptonEfficiencyCorrector(self.el_f_GH,self.el_h)
#        self._worker_tri_BF = ROOT.LeptonEfficiencyCorrector(self.tri_f_BF,self.tri_h)
#        self._worker_tri_GH = ROOT.LeptonEfficiencyCorrector(self.tri_f_GH,self.tri_h)
        self._worker_muID_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_BF,self.mu_h_ID)
        self._worker_muID_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ID_GH,self.mu_h_ID)
        self._worker_muISO_BF = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_BF,self.mu_h_ISO)
        self._worker_muISO_GH = ROOT.LeptonEfficiencyCorrector(self.mu_f_ISO_GH,self.mu_h_ISO)
        self._worker_tri_BF_ElEl = ROOT.LeptonEfficiencyCorrector(self.tri_f_BF,self.tri_h_ElEl)
        self._worker_tri_GH_ElEl = ROOT.LeptonEfficiencyCorrector(self.tri_f_GH,self.tri_h_ElEl)
        self._worker_tri_BF_MuMu = ROOT.LeptonEfficiencyCorrector(self.tri_f_BF,self.tri_h_MuMu)
        self._worker_tri_GH_MuMu = ROOT.LeptonEfficiencyCorrector(self.tri_f_GH,self.tri_h_MuMu)
        self._worker_tri_BF_ElMu = ROOT.LeptonEfficiencyCorrector(self.tri_f_BF,self.tri_h_ElMu)
        self._worker_tri_GH_ElMu = ROOT.LeptonEfficiencyCorrector(self.tri_f_GH,self.tri_h_ElMu)
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("Lepton_SF", "F")
        self.out.branch("Lepton_SFerr", "F")
        self.out.branch("Electron_SF", "F")
        self.out.branch("Electron_SFerr", "F")
        self.out.branch("Muon_SF", "F")
        self.out.branch("Muon_SFerr", "F")
        self.out.branch("MuonID_SF", "F")
        self.out.branch("MuonID_SFerr", "F")
        self.out.branch("MuonISO_SF", "F")
        self.out.branch("MuonISO_SFerr", "F")
        self.out.branch("Trigger_SF", "F")
        #self.out.branch("Trigger_SFerr", "F")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        muons = Collection(event, "Muon")
        electrons = Collection(event, "Electron")

        sf_el_BF, sf_elerr_BF = [], []
        sf_el_GH, sf_elerr_GH = [], []
        sf_mu_BF, sf_muerr_BF = [], []
        sf_mu_GH, sf_muerr_GH = [], []
        sf_mu_ID_BF, sf_muerr_ID_BF = [], []
        sf_mu_ID_GH, sf_muerr_ID_GH = [], []
        sf_mu_ISO_BF, sf_muerr_ISO_BF = [], []
        sf_mu_ISO_GH, sf_muerr_ISO_GH = [], []
        el_pt, mu_pt = [], []
        el_eta, mu_eta = [], []

        for el in electrons:
            if el.pt < 20 or abs(el.eta) > 2.4 : continue
            if abs(el.eta + el.deltaEtaSC) > 1.4442 and abs(el.eta + el.deltaEtaSC) < 1.566 : continue
#            if el.cutBased_Sum16 != 4 : continue
            if el.cutBased != 4 : continue
   
            sf_el_BF.append(self._worker_el_BF.getSF(el.pdgId,el.pt,el.eta+el.deltaEtaSC))
            sf_el_GH.append(self._worker_el_GH.getSF(el.pdgId,el.pt,el.eta+el.deltaEtaSC))
            sf_elerr_BF.append(self._worker_el_BF.getSFErr(el.pdgId,el.pt,el.eta+el.deltaEtaSC))
            sf_elerr_GH.append(self._worker_el_GH.getSFErr(el.pdgId,el.pt,el.eta+el.deltaEtaSC))

            el_pt.append(el.pt)
            el_eta.append(el.eta)

        for mu in muons:
            if mu.pt < 20 or abs(mu.eta) > 2.4 : continue
            if mu.tightId == 0 : continue
            if mu.pfRelIso04_all > 0.15 : continue

            sf_mu_BF.append(self._worker_mu_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_GH.append(self._worker_mu_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_BF.append(self._worker_mu_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_GH.append(self._worker_mu_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))

            sf_mu_ID_BF.append(self._worker_muID_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ID_GH.append(self._worker_muID_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ID_BF.append(self._worker_muID_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ID_GH.append(self._worker_muID_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ISO_BF.append(self._worker_muISO_BF.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_mu_ISO_GH.append(self._worker_muISO_GH.getSF(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ISO_BF.append(self._worker_muISO_BF.getSFErr(mu.pdgId,mu.pt,mu.eta))
            sf_muerr_ISO_GH.append(self._worker_muISO_GH.getSFErr(mu.pdgId,mu.pt,mu.eta))

            mu_pt.append(mu.pt)
            mu_eta.append(mu.pt)
    
#        sf_el = [ self._worker_el.getSF(el.pdgId,el.pt,el.eta+el.deltaEtaSC) for el in electrons ]
#        sf_elerr = [ self._worker_el.getSFErr(el.pdgId,el.pt,el.eta+el.deltaEtaSC) for el in electrons ]
#
#        sf_mu_BF = [ self._worker_mu_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_GH = [ self._worker_mu_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_BF = [ self._worker_mu_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_GH = [ self._worker_mu_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#
#        sf_mu_ID_BF = [ self._worker_muID_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ID_GH = [ self._worker_muID_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ID_BF = [ self._worker_muID_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ID_GH = [ self._worker_muID_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ISO_BF = [ self._worker_muISO_BF.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_mu_ISO_GH = [ self._worker_muISO_GH.getSF(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ISO_BF = [ self._worker_muISO_BF.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#        sf_muerr_ISO_GH = [ self._worker_muISO_GH.getSFErr(mu.pdgId,mu.pt,mu.eta) for mu in muons ]
#
#        el_pt = [ el.pt for el in electrons ]
#        mu_pt = [ mu.pt for mu in muons ]

#        lep_pt = el_pt + mu_pt
#        lep_eta = el_eta + mu_eta
#        Leadinglep_pt = max(lep_pt)
#        Leadinglep_index = lep_pt.index(Leadinglep_pt)
#        Leadinglep_eta = lep_eta[Leadinglep_index]
##        if Leadinglep_pt >= 0 and Leadinglep_pt < 100 : sf_Trig = self.TrigSF[0]
##        elif Leadinglep_pt >= 100 and Leadinglep_pt < 200 : sf_Trig = self.TrigSF[1]
##        elif Leadinglep_pt >= 200 and Leadinglep_pt < 300 : sf_Trig = self.TrigSF[2]
##        elif Leadinglep_pt >= 300 : sf_Trig = self.TrigSF[3]
##        else : sf_Trig = 1
##        sf_Trig = 1
#        sf_tri_BF = self._worker_tri_BF.getTrigSF(Leadinglep_pt,Leadinglep_eta)
#        sf_tri_GH = self._worker_tri_GH.getTrigSF(Leadinglep_pt,Leadinglep_eta)

        lep_pt = el_pt + mu_pt
        sort_lep_pt = sorted(lep_pt, reverse=True)
        sort_el_pt = sorted(el_pt, reverse=True)
        sort_mu_pt = sorted(mu_pt, reverse=True)
        sf_tri_BF = 1.
        sf_tri_GH = 1.
        if len(sort_el_pt)>=2 and len(sort_lep_pt)>=2:
            if sort_el_pt[1] >= sort_lep_pt[1]:
                sf_tri_BF = self._worker_tri_BF_ElEl.getTrigSF(sort_el_pt[0],sort_el_pt[1])
                sf_tri_GH = self._worker_tri_GH_ElEl.getTrigSF(sort_el_pt[0],sort_el_pt[1])
        if len(sort_mu_pt)>=2 and len(sort_lep_pt)>=2:
            if sort_mu_pt[1] >= sort_lep_pt[1]:
                sf_tri_BF = self._worker_tri_BF_MuMu.getTrigSF(sort_mu_pt[0],sort_mu_pt[1])
                sf_tri_GH = self._worker_tri_GH_MuMu.getTrigSF(sort_mu_pt[0],sort_mu_pt[1])
        if len(sort_el_pt)>=1 and len(sort_mu_pt)>=1:
#            if sort_el_pt[0] == sort_lep_pt[1] or sort_mu_pt[0] == sort_lep_pt[1]:
            if sort_el_pt[0] >= sort_lep_pt[1] and sort_mu_pt[0] >= sort_lep_pt[1]:
                sf_tri_BF = self._worker_tri_BF_ElMu.getTrigSF(sort_el_pt[0],sort_mu_pt[0])
                sf_tri_GH = self._worker_tri_GH_ElMu.getTrigSF(sort_el_pt[0],sort_mu_pt[0])

        sf_mu, sf_muerr = [], []
        sf_mu_ID, sf_muerr_ID = [], []
        sf_mu_ISO, sf_muerr_ISO = [], []
        sf_el, sf_elerr = [], []
        for i in range(len(sf_mu_BF)):
#            sf_mu.append(0.54822 * sf_mu_BF[i] + 0.45178 * sf_mu_GH[i])
#            sf_mu_ID.append(0.54822 * sf_mu_ID_BF[i] + 0.45178 * sf_mu_ID_GH[i])
#            sf_mu_ISO.append(0.54822 * sf_mu_ISO_BF[i] + 0.45178 * sf_mu_ISO_GH[i])
#            sf_muerr.append(sqrt(0.54822**2 * sf_muerr_BF[i]**2 + 0.45178**2 * sf_muerr_GH[i]**2))
#            sf_muerr_ID.append(sqrt(0.54822**2 * sf_muerr_ID_BF[i]**2 + 0.45178**2 * sf_muerr_ID_GH[i]**2))
#            sf_muerr_ISO.append(sqrt(0.54822**2 * sf_muerr_ISO_BF[i]**2 + 0.45178**2 * sf_muerr_ISO_GH[i]**2))
            sf_mu.append(sf_mu_GH[i])
            sf_mu_ID.append(sf_mu_ID_GH[i])
            sf_mu_ISO.append(sf_mu_ISO_GH[i])
            sf_muerr.append(sf_muerr_GH[i])
            sf_muerr_ID.append(sf_muerr_ID_GH[i])
            sf_muerr_ISO.append(sf_muerr_ISO_GH[i])

        for i in range(len(sf_el_BF)):
#            sf_el.append(0.54822 * sf_el_BF[i] + 0.45178 * sf_el_GH[i])
#            sf_elerr.append(sqrt(0.54822**2 * sf_elerr_BF[i]**2 + 0.45178**2 * sf_elerr_GH[i]**2))
            sf_el.append(sf_el_GH[i])
            sf_elerr.append(sf_elerr_GH[i])

#        sf_Trig = 0.54822 * sf_tri_BF + 0.45178 * sf_tri_GH
        sf_Trig = sf_tri_GH

        leptonSFset = sf_el + sf_mu
        leptonSFerrset = sf_elerr + sf_muerr
        leptonSFval = 1.
        leptonSFerrval = 0
        for sfval in leptonSFset:
            leptonSFval *= sfval
        for sferrval in leptonSFerrset:
            leptonSFerrval += sferrval**2

        elSFval = 1.
        elSFerrval = 0
        for sfval in sf_el:
            elSFval *= sfval
        for sferrval in sf_elerr:
            elSFerrval += sferrval**2

        if elSFerrval > 1:
            print elSFerrval, sf_elerr

        muonSFval = 1.
        muonSFerrval = 0
        for sfval in sf_mu:
            muonSFval *= sfval
        for sferrval in sf_muerr:
            muonSFerrval += sferrval**2

        muonIDSFval = 1.
        muonIDSFerrval = 0
        for sfval in sf_mu_ID:
            muonIDSFval *= sfval
        for sferrval in sf_muerr_ID:
            muonIDSFerrval += sferrval**2

        muonISOSFval = 1.
        muonISOSFerrval = 0
        for sfval in sf_mu_ISO:
            muonISOSFval *= sfval
        for sferrval in sf_muerr_ISO:
            muonISOSFerrval += sferrval**2
	
        self.out.fillBranch("Lepton_SF", leptonSFval)
        self.out.fillBranch("Lepton_SFerr", sqrt(leptonSFerrval))
        self.out.fillBranch("Electron_SF", elSFval)
        self.out.fillBranch("Electron_SFerr", sqrt(elSFerrval))
        self.out.fillBranch("Muon_SF", muonSFval)
        self.out.fillBranch("Muon_SFerr", sqrt(muonSFerrval))
        self.out.fillBranch("MuonID_SF", muonIDSFval)
        self.out.fillBranch("MuonID_SFerr", sqrt(muonIDSFerrval))
        self.out.fillBranch("MuonISO_SF", muonISOSFval)
        self.out.fillBranch("MuonISO_SFerr", sqrt(muonISOSFerrval))
        self.out.fillBranch("Trigger_SF", sf_Trig)
        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

lepSF_ElElEl = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "ElElEl")
lepSF_MuElEl = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "MuElEl")
lepSF_ElMuMu = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "ElMuMu")
lepSF_MuMuMu = lambda : lepSFProducer("TightWP_2016", "TightWP_2016", "MuMuMu")

lepSF_ElElEl = lambda : lepSFProducer("TightWP_2018", "TightWP_2018", "ElElEl")
lepSF_MuElEl = lambda : lepSFProducer("TightWP_2018", "TightWP_2018", "MuElEl")
lepSF_ElMuMu = lambda : lepSFProducer("TightWP_2018", "TightWP_2018", "ElMuMu")
lepSF_MuMuMu = lambda : lepSFProducer("TightWP_2018", "TightWP_2018", "MuMuMu")
