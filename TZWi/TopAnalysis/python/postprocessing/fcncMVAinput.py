import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

import yaml
from glob import *
import os
from ROOT import TLorentzVector
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class FCNCMVAinput(Module, object):
    def __init__(self, *args, **kwargs):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        # Basic input variables
        self.out.branch("MVAinput_Status", "i")
        self.out.branch("MVAinput_WLZL1_dPhi", "F")
        self.out.branch("MVAinput_WLZL1_dR", "F")
        self.out.branch("MVAinput_WLZL2_dPhi", "F")
        self.out.branch("MVAinput_WLZL2_dR", "F")
        self.out.branch("MVAinput_ZL1ZL2_dPhi", "F")
        self.out.branch("MVAinput_ZL1ZL2_dR", "F")
        self.out.branch("MVAinput_Wlepchapt", "F")
        self.out.branch("MVAinput_Wlepchaeta", "F")
        # Inputs for WZCR
        self.out.branch("MVAinput_J1_DeepJetB", "F")
        self.out.branch("MVAinput_J1_pt", "F")
        self.out.branch("MVAinput_ZL1J1_dPhi", "F")
        self.out.branch("MVAinput_ZL1J1_dR", "F")
        self.out.branch("MVAinput_ZL2J1_dPhi", "F")
        self.out.branch("MVAinput_ZL2J1_dR", "F")
        self.out.branch("MVAinput_WLJ1_dPhi", "F")
        self.out.branch("MVAinput_WLJ1_dR", "F")
        # Inputs for ST/TTCR
        self.out.branch("MVAinput_bJ_DeepJetB", "F")
        self.out.branch("MVAinput_qJ_DeepJetB", "F")
        self.out.branch("MVAinput_bJ_pt", "F")
        self.out.branch("MVAinput_qJ_pt", "F")
        self.out.branch("MVAinput_bJqJ_dPhi", "F")
        self.out.branch("MVAinput_bJqJ_dR", "F")
        self.out.branch("MVAinput_WLbJ_dPhi", "F")
        self.out.branch("MVAinput_WLbJ_dR", "F")
        self.out.branch("MVAinput_WLqJ_dPhi", "F")
        self.out.branch("MVAinput_WLqJ_dR", "F")
        self.out.branch("MVAinput_ZL1bJ_dPhi", "F")
        self.out.branch("MVAinput_ZL1bJ_dR", "F")
        self.out.branch("MVAinput_ZL1qJ_dPhi", "F")
        self.out.branch("MVAinput_ZL1qJ_dR", "F")
        self.out.branch("MVAinput_ZL2bJ_dPhi", "F")
        self.out.branch("MVAinput_ZL2bJ_dR", "F")
        self.out.branch("MVAinput_ZL2qJ_dPhi", "F")
        self.out.branch("MVAinput_ZL2qJ_dR", "F")
        self.out.branch("MVAinput_Z_bJ_dPhi", "F")
        self.out.branch("MVAinput_Z_bJ_dR", "F")
        self.out.branch("MVAinput_Z_qJ_dPhi", "F")
        self.out.branch("MVAinput_Z_qJ_dR", "F")
        self.out.branch("xsecNorm", "F")

        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):

        ## initialize ##
        info = {}
        xsecfile = "%s/src/TZWi/TopAnalysis/test/fcncTriLepton/config/crosssection.yaml" % os.environ["CMSSW_BASE"]
        info.update(yaml.load(open(xsecfile)))
        info.update(yaml.load(open("%s/src/TZWi/TopAnalysis/test/fcncTriLepton/NanoAOD/2018/MC.RunIISummer18.central.yaml" % os.environ["CMSSW_BASE"])))
        info['dataset'].update(yaml.load(open("%s/src/TZWi/TopAnalysis/test/fcncTriLepton/NanoAOD/2018/MC.RunIISummer18.rareprocess.yaml" % os.environ["CMSSW_BASE"]))['dataset'])
        info['dataset'].update(yaml.load(open("%s/src/TZWi/TopAnalysis/test/fcncTriLepton/NanoAOD/2018/MC.RunIISummer18.syst.yaml" % os.environ["CMSSW_BASE"]))['dataset'])

        rootpath = ROOT.gDirectory.GetPath()
        rootsample1 = rootpath.split('/')[3]
        rootsample = rootsample1.split('.')[0]

        xsecitem = info['crosssection'].items()
        entryitem = info['Entries'].items()
        dataitem = info['dataset'].items()

        fileset = []
        fileroute = []

        for i, items in enumerate(dataitem):
            fileset0 = items[0]
            fileset1 = fileset0.split('.')[1]
            fileset.append(fileset1)
            fileroutekey0 = items[1].keys()
            fileroute.append(fileroutekey0)

        for j, routes in enumerate(fileroute):
            for k, routeitem in enumerate(routes):
                if rootsample in routeitem:
                    findsample = fileset[j]

        targetxsecweight = 1.0
        targetentry = 1
        if ( ( rootsample == "EGamma" ) or ( rootsample == "DoubleMuon" ) ):
            targetxsecweight = 1.0
        else:
            for i, xsecslot in enumerate(xsecitem):
                if ( findsample == xsecslot[0] ):
                    targetxsec = xsecslot[1]
            for i, entryslot in enumerate(entryitem):
                if ( findsample == entryslot[0] ):
                    targetentry = entryslot[1]

            targetxsecweight = (float(targetxsec)/float(targetentry))*59830 #16810 #35918 #59970

        # Variables initialize
        Status = 0
        WLZL1_dPhi, WLZL1_dR = 0, 0
        WLZL2_dPhi, WLZL2_dR = 0, 0
        ZL1ZL2_dPhi, ZL1ZL2_dR = 0, 0
        Wlepchapt, Wlepchaeta = 0, 0
        J1_DeepJetB, J1_pt = 0, 0
        ZL1J1_dPhi, ZL1J1_dR = 0, 0
        ZL2J1_dPhi, ZL2J1_dR = 0, 0
        WLJ1_dPhi, WLJ1_dR = 0, 0
        bJ_DeepJetB, qJ_DeepJetB = 0, 0
        bJ_pt, qJ_pt = 0, 0
        bJqJ_dPhi, bJqJ_dR = 0, 0
        WLbJ_dPhi, WLbJ_dR = 0, 0
        WLqJ_dPhi, WLqJ_dR = 0, 0
        ZL1bJ_dPhi, ZL1bJ_dR = 0, 0
        ZL1qJ_dPhi, ZL1qJ_dR = 0, 0
        ZL2bJ_dPhi, ZL2bJ_dR = 0, 0
        ZL2qJ_dPhi, ZL2qJ_dR = 0, 0
        Z_bJ_dPhi, Z_bJ_dR = 0, 0
        Z_qJ_dPhi, Z_qJ_dR = 0, 0

        # Basic event selection for WZCR/TTCR
        if ( ( event._tree.b_out_GoodLeptonCode != 111 ) or ( event._tree.b_out_nGoodLepton > 3 ) or ( event._tree.b_out_W_MT > 300 ) ):
            self.out.fillBranch("MVAinput_Status", 0)
            self.out.fillBranch("MVAinput_WLZL1_dPhi", 0)
            self.out.fillBranch("MVAinput_WLZL1_dR", 0)
            self.out.fillBranch("MVAinput_WLZL2_dPhi", 0)
            self.out.fillBranch("MVAinput_WLZL2_dR", 0)
            self.out.fillBranch("MVAinput_ZL1ZL2_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1ZL2_dR", 0)
            self.out.fillBranch("MVAinput_Wlepchapt", 0)
            self.out.fillBranch("MVAinput_Wlepchaeta", 0)
            self.out.fillBranch("MVAinput_J1_DeepJetB", 0)
            self.out.fillBranch("MVAinput_J1_pt", 0)
            self.out.fillBranch("MVAinput_ZL1J1_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1J1_dR", 0)
            self.out.fillBranch("MVAinput_ZL2J1_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2J1_dR", 0)
            self.out.fillBranch("MVAinput_WLJ1_dPhi", 0)
            self.out.fillBranch("MVAinput_WLJ1_dR", 0)
            self.out.fillBranch("MVAinput_bJ_DeepJetB", 0)
            self.out.fillBranch("MVAinput_qJ_DeepJetB", 0)
            self.out.fillBranch("MVAinput_bJ_pt", 0)
            self.out.fillBranch("MVAinput_qJ_pt", 0)
            self.out.fillBranch("MVAinput_bJqJ_dPhi", 0)
            self.out.fillBranch("MVAinput_bJqJ_dR", 0)
            self.out.fillBranch("MVAinput_WLbJ_dPhi", 0)
            self.out.fillBranch("MVAinput_WLbJ_dR", 0)
            self.out.fillBranch("MVAinput_WLqJ_dPhi", 0)
            self.out.fillBranch("MVAinput_WLqJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL1bJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1bJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL1qJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL1qJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL2bJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2bJ_dR", 0)
            self.out.fillBranch("MVAinput_ZL2qJ_dPhi", 0)
            self.out.fillBranch("MVAinput_ZL2qJ_dR", 0)
            self.out.fillBranch("MVAinput_Z_bJ_dPhi", 0)
            self.out.fillBranch("MVAinput_Z_bJ_dR", 0)
            self.out.fillBranch("MVAinput_Z_qJ_dPhi", 0)
            self.out.fillBranch("MVAinput_Z_qJ_dR", 0)
            self.out.fillBranch("xsecNorm", targetxsecweight)

            return True
        else:

            # Booking and filling variables for basic variables
            
            Z1Lepton = TLorentzVector()
            Z2Lepton = TLorentzVector()
            WLepton = TLorentzVector()
            ConstZ = TLorentzVector()
            Jet1 = TLorentzVector() # For WZCR
            bJet = TLorentzVector() # For TTCR
            qJet = TLorentzVector() # For TTCR

            WLepton.SetPtEtaPhiM(event._tree.b_out_Lepton1_pt, event._tree.b_out_Lepton1_eta, event._tree.b_out_Lepton1_phi, event._tree.b_out_Lepton1_mass)
            Z1Lepton.SetPtEtaPhiM(event._tree.b_out_Lepton2_pt, event._tree.b_out_Lepton2_eta, event._tree.b_out_Lepton2_phi, event._tree.b_out_Lepton2_mass)
            Z2Lepton.SetPtEtaPhiM(event._tree.b_out_Lepton3_pt, event._tree.b_out_Lepton3_eta, event._tree.b_out_Lepton3_phi, event._tree.b_out_Lepton3_mass)
            ConstZ.SetPtEtaPhiM(event._tree.b_out_Z_pt, event._tree.b_out_Z_eta, event._tree.b_out_Z_phi, event._tree.b_out_Z_mass)
            
            if ( event._tree.b_out_Lepton1_pdgId > 0 ): WlepCha = -1
            else: WlepCha = 1

            WLZL1_dPhi  = abs(WLepton.DeltaPhi(Z1Lepton))
            WLZL1_dR    = abs(WLepton.DeltaR(Z1Lepton))
            WLZL2_dPhi  = abs(WLepton.DeltaPhi(Z2Lepton))
            WLZL2_dR    = abs(WLepton.DeltaR(Z2Lepton))
            ZL1ZL2_dPhi = abs(Z1Lepton.DeltaPhi(Z2Lepton))
            ZL1ZL2_dR   = abs(Z1Lepton.DeltaR(Z2Lepton))
            Wlepchapt   = WlepCha * event._tree.b_out_Lepton1_pt
            Wlepchaeta  = WlepCha * abs(event._tree.b_out_Lepton1_eta)
            Status      = 1

            # For WZCR case

            if ( ( abs( ConstZ.M() - 91.2) < 7.5 ) and ( event._tree.b_out_nGoodJet >= 1 ) and ( event._tree.b_out_W_MT <= 300) and\
               ( event._tree.b_out_nBjet == 0 ) and ( event._tree.b_out_LeadingLepton_pt > 25 ) and ( event._tree.b_out_Z_charge == 0 ) ):

                Jet1.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])

                J1_DeepJetB = event._tree.b_out_GoodJet_DeepFlavB[0]
                J1_pt       = Jet1.Pt()
                ZL1J1_dPhi  = abs(Z1Lepton.DeltaPhi(Jet1))
                ZL1J1_dR    = abs(Z1Lepton.DeltaR(Jet1))
                ZL2J1_dPhi  = abs(Z2Lepton.DeltaPhi(Jet1))
                ZL2J1_dR    = abs(Z2Lepton.DeltaR(Jet1))
                WLJ1_dPhi   = abs(WLepton.DeltaPhi(Jet1))
                WLJ1_dR     = abs(WLepton.DeltaR(Jet1))
                Status      = 2
                
            # For STCR/STSR case
            elif (  ( event._tree.b_out_nGoodJet == 1) and ( event._tree.b_out_W_MT <= 300) and\
                    ( event._tree.b_out_nBjet == 1 ) and ( event._tree.b_out_LeadingLepton_pt > 25 ) and ( event._tree.b_out_Z_charge == 0 ) ):
                BJet = TLorentzVector()
                BJet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])
                btagBj = event._tree.b_out_GoodJet_DeepFlavB[0] # Should be changed to DeepJet b tagger

                bJ_DeepJetB = btagBj
                bJ_pt       = BJet.Pt()
                WLbJ_dPhi   = abs(WLepton.DeltaPhi(BJet))
                WLbJ_dR     = abs(WLepton.DeltaR(BJet))
                ZL1bJ_dPhi  = abs(Z1Lepton.DeltaPhi(BJet))
                ZL1bJ_dR    = abs(Z1Lepton.DeltaR(BJet))
                ZL2bJ_dPhi  = abs(Z2Lepton.DeltaPhi(BJet))
                ZL2bJ_dR    = abs(Z2Lepton.DeltaR(BJet))
                Z_bJ_dPhi   = abs(ConstZ.DeltaPhi(BJet))
                Z_bJ_dR     = abs(ConstZ.DeltaR(BJet))
                Status      = 3

            # For TTCR/TTSR case

            elif (  ( 2 <= event._tree.b_out_nGoodJet <= 3) and ( event._tree.b_out_W_MT <= 300) and\
                    ( event._tree.b_out_nBjet >= 1 ) and ( event._tree.b_out_LeadingLepton_pt > 25 ) and ( event._tree.b_out_Z_charge == 0 ) ):

                BJet = TLorentzVector()
                Q1Jet = TLorentzVector()
                Q2Jet = TLorentzVector()  ## Pt_sorted yet
                QJet = TLorentzVector() ## Q jet slot for u/c jet
                BJet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[0], event._tree.b_out_GoodJet_eta[0], event._tree.b_out_GoodJet_phi[0], event._tree.b_out_GoodJet_mass[0])
                Q1Jet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[1], event._tree.b_out_GoodJet_eta[1], event._tree.b_out_GoodJet_phi[1], event._tree.b_out_GoodJet_mass[1])
                    
                btagBj = event._tree.b_out_GoodJet_DeepFlavB[0]
                btagQ1j = event._tree.b_out_GoodJet_DeepFlavB[1]
                btagQj = 0. ## Slot for b-jet discriminator of u/c jet

                if ( event._tree.b_out_nGoodJet == 2 ):
                    if ( btagBj < btagQ1j ): 
                        BJet, QJet = Q1Jet, BJet
                        btagBj, btagQj = btagQ1j, btagBj
                    else:
                        BJet, QJet = BJet, Q1Jet
                        btagBj, btagQj = btagBj, btagQ1j # Btag sorted

                elif ( event._tree.b_out_nGoodJet == 3 ):
                    Q2Jet.SetPtEtaPhiM(event._tree.b_out_GoodJet_pt[2], event._tree.b_out_GoodJet_eta[2], event._tree.b_out_GoodJet_phi[2], event._tree.b_out_GoodJet_mass[2])
                    btagQ2j = event._tree.b_out_GoodJet_DeepFlavB[2]

                    if ( btagBj > btagQ1j ):
                        if ( btagQ1j > btagQ2j ):
                            BJet, QJet = BJet, Q1Jet
                            btagBj, btagQj = btagBj, btagQ1j
                        else:
                            if ( btagBj > btagQ2j ):
                                BJet, QJet = BJet, Q2Jet
                                btagBj, btagQj = btagBj, btagQ2j
                            else:
                                BJet, QJet = Q2Jet, BJet
                                btagBj, btagQj = btagQ2j, btagBj
                    else:
                        if ( btagBj > btagQ2j ):
                            BJet, QJet = Q1Jet, BJet
                            btagBj, btagQj = btagQ1j, btagBj
                        else:
                            if ( btagQ1j > btagQ2j ):    
                                BJet, QJet = Q1Jet, Q2Jet
                                btagBj, btagQj = btagQ1j, btagQ2j
                            else:
                                BJet, QJet = Q2Jet, Q1Jet
                                btagBj, btagQj = btagQ2j, btagQ1j # Btag sorted

                bJ_DeepJetB = btagBj
                qJ_DeepJetB = btagQj
                bJ_pt       = BJet.Pt()
                qJ_pt       = QJet.Pt()
                bJqJ_dPhi   = abs(BJet.DeltaPhi(QJet))
                bJqJ_dR     = abs(BJet.DeltaR(QJet))
                WLbJ_dPhi   = abs(WLepton.DeltaPhi(BJet))
                WLbJ_dR     = abs(WLepton.DeltaR(BJet))
                WLqJ_dPhi   = abs(WLepton.DeltaPhi(QJet))
                WLqJ_dR     = abs(WLepton.DeltaR(QJet))
                ZL1bJ_dPhi  = abs(Z1Lepton.DeltaPhi(BJet))
                ZL1bJ_dR    = abs(Z1Lepton.DeltaR(BJet))
                ZL1qJ_dPhi  = abs(Z1Lepton.DeltaPhi(QJet))
                ZL1qJ_dR    = abs(Z1Lepton.DeltaR(QJet))
                ZL2bJ_dPhi  = abs(Z2Lepton.DeltaPhi(BJet))
                ZL2bJ_dR    = abs(Z2Lepton.DeltaR(BJet))
                ZL2qJ_dPhi  = abs(Z2Lepton.DeltaPhi(QJet))
                ZL2qJ_dR    = abs(Z2Lepton.DeltaR(QJet))
                Z_bJ_dPhi   = abs(ConstZ.DeltaPhi(BJet))
                Z_bJ_dR     = abs(ConstZ.DeltaR(BJet))
                Z_qJ_dPhi   = abs(ConstZ.DeltaPhi(QJet))
                Z_qJ_dR     = abs(ConstZ.DeltaR(QJet))
                Status      = 4

        self.out.fillBranch("MVAinput_Status", Status)
        self.out.fillBranch("MVAinput_WLZL1_dPhi", WLZL1_dPhi)
        self.out.fillBranch("MVAinput_WLZL1_dR", WLZL1_dR)
        self.out.fillBranch("MVAinput_WLZL2_dPhi", WLZL2_dPhi)
        self.out.fillBranch("MVAinput_WLZL2_dR", WLZL2_dR)
        self.out.fillBranch("MVAinput_ZL1ZL2_dPhi", ZL1ZL2_dPhi)
        self.out.fillBranch("MVAinput_ZL1ZL2_dR", ZL1ZL2_dR)
        self.out.fillBranch("MVAinput_Wlepchapt", Wlepchapt)
        self.out.fillBranch("MVAinput_Wlepchaeta", Wlepchaeta)
        self.out.fillBranch("MVAinput_J1_DeepJetB", J1_DeepJetB)
        self.out.fillBranch("MVAinput_J1_pt", J1_pt)
        self.out.fillBranch("MVAinput_ZL1J1_dPhi", ZL1J1_dPhi)
        self.out.fillBranch("MVAinput_ZL1J1_dR", ZL1J1_dR)
        self.out.fillBranch("MVAinput_ZL2J1_dPhi", ZL2J1_dPhi)
        self.out.fillBranch("MVAinput_ZL2J1_dR", ZL2J1_dR)
        self.out.fillBranch("MVAinput_WLJ1_dPhi", WLJ1_dPhi)
        self.out.fillBranch("MVAinput_WLJ1_dR", WLJ1_dR)
        self.out.fillBranch("MVAinput_bJ_DeepJetB", bJ_DeepJetB)
        self.out.fillBranch("MVAinput_qJ_DeepJetB", qJ_DeepJetB)
        self.out.fillBranch("MVAinput_bJ_pt", bJ_pt)
        self.out.fillBranch("MVAinput_qJ_pt", qJ_pt)
        self.out.fillBranch("MVAinput_bJqJ_dPhi", bJqJ_dPhi)
        self.out.fillBranch("MVAinput_bJqJ_dR", bJqJ_dR)
        self.out.fillBranch("MVAinput_WLbJ_dPhi", WLbJ_dPhi)
        self.out.fillBranch("MVAinput_WLbJ_dR", WLbJ_dR)
        self.out.fillBranch("MVAinput_WLqJ_dPhi", WLqJ_dPhi)
        self.out.fillBranch("MVAinput_WLqJ_dR", WLqJ_dR)
        self.out.fillBranch("MVAinput_ZL1bJ_dPhi", ZL1bJ_dPhi)
        self.out.fillBranch("MVAinput_ZL1bJ_dR", ZL1bJ_dR)
        self.out.fillBranch("MVAinput_ZL1qJ_dPhi", ZL1qJ_dPhi)
        self.out.fillBranch("MVAinput_ZL1qJ_dR", ZL1qJ_dR)
        self.out.fillBranch("MVAinput_ZL2bJ_dPhi", ZL2bJ_dPhi)
        self.out.fillBranch("MVAinput_ZL2bJ_dR", ZL2bJ_dR)
        self.out.fillBranch("MVAinput_ZL2qJ_dPhi", ZL2qJ_dPhi)
        self.out.fillBranch("MVAinput_ZL2qJ_dR", ZL2qJ_dR)
        self.out.fillBranch("MVAinput_Z_bJ_dPhi", Z_bJ_dPhi)
        self.out.fillBranch("MVAinput_Z_bJ_dR", Z_bJ_dR)
        self.out.fillBranch("MVAinput_Z_qJ_dPhi", Z_qJ_dPhi)
        self.out.fillBranch("MVAinput_Z_qJ_dR", Z_qJ_dR)
        self.out.fillBranch("xsecNorm", targetxsecweight)

        return True

fcncMVAinput = lambda: FCNCMVAinput()
