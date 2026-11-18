#ifndef TZWi_TopAnalysis_FCNCTriLeptonCppWorker_H
#define TZWi_TopAnalysis_FCNCTriLeptonCppWorker_H

#include <memory>
#include <string>
#include <vector>
#include <TTree.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TLorentzVector.h>

class FCNCTriLeptonCppWorker {
//190306 KST 15:49 : just copy frome TTbarDouble~.h, changed class name
public:
  enum class MODE {None=0, NANOAOD=100000} mode_ = MODE::None;
//  const bool doNonPromptLepton_;

  typedef TTreeReaderArray<float>* TRAF;
  typedef TTreeReaderArray<int>* TRAI;
  typedef TTreeReaderArray<bool>* TRAB;
  typedef TTreeReaderArray<unsigned char>* TRAC;

//  FCNCTriLeptonCppWorker(const std::string modeName, const bool doNonPromptLepton=false);
  FCNCTriLeptonCppWorker(const std::string modeName);
  ~FCNCTriLeptonCppWorker() = default;

  void setElectrons(TRAF pt, TRAF eta, TRAB isPFcand, TRAC lostHits,
                    TRAF dxy, TRAF dz, TRAF sip3d, TRAF miniPFRelIso_all,
                    TRAF sieie, TRAF hoe, TRAF eInvMinusPInv, TRAB convVeto, TRAF dEtaSC);
  void setMuons(TRAF pt, TRAF eta, TRAB isPFcand, TRAB isTracker, TRAB isGlobal,
                TRAF dxy, TRAF dz, TRAF sip3d, TRAF miniPFRelIso_all, TRAB mediumId);
  void setTaus(TRAF pt, TRAF eta, TRAF dz, TRAI decayMode,
               TRAC DeepTau2017v2p1VSjet, TRAC DeepTau2017v2p1VSe, TRAC DeepTau2017v2p1VSmu);

//  void setRecoElectrons(const unsigned i);
//  void setRecoMuons(const unsigned i);

//  void resetValues();
  bool analyze();

  unsigned get_nGoodLeptonRemake() const { return out_nGoodLeptonRemake; }

private:
//  const double minMuonPt_ = 20, maxMuonEta_ = 2.4; //Signal & veto reco. cuts are same
//  const double minElectronPt_ = 20, maxElectronEta_ = 2.4; //Signal & veto reco. cuts are same
//  const double minJetPt_ = 30, maxJetEta_ = 2.4;
//  const double minBjetBDiscr_ = 0.0490;
//  const double maxMuonRelIso_ = 0.15;
//  const double maxVetoMuonRelIso_ = 0.25;

//  const double minPtLepton1_ = 25, minPtLepton2_ = 20; // Lepton pT selection for the event selection

  bool isGoodMuon(const unsigned i) const;
  bool isGoodElectron(const unsigned i) const;
  bool isGoodTau(const unsigned i) const;

private:

private:
  TRAF in_Electrons_pt = nullptr;
  TRAF in_Electrons_eta = nullptr;
  TRAB in_Electrons_isPFcand = nullptr;
  TRAC in_Electrons_lostHits = nullptr;
  TRAF in_Electrons_dxy = nullptr;
  TRAF in_Electrons_dz = nullptr;
  TRAF in_Electrons_sip3d = nullptr;
  TRAF in_Electrons_miniPFRelIso_all = nullptr;
  TRAF in_Electrons_sieie = nullptr;
  TRAF in_Electrons_hoe = nullptr;
  TRAF in_Electrons_eInvMinusPInv = nullptr;
  TRAB in_Electrons_convVeto = nullptr;
  TRAF in_Electrons_dEtaSC = nullptr;

  TRAF in_Muons_pt = nullptr;
  TRAF in_Muons_eta = nullptr;
  TRAB in_Muons_isPFcand = nullptr;
  TRAB in_Muons_isTracker = nullptr;
  TRAB in_Muons_isGlobal = nullptr;
  TRAF in_Muons_dxy = nullptr;
  TRAF in_Muons_dz = nullptr;
  TRAF in_Muons_sip3d = nullptr;
  TRAF in_Muons_miniPFRelIso_all = nullptr;
  TRAB in_Muons_mediumId = nullptr;

  TRAF in_Taus_pt = nullptr;
  TRAF in_Taus_eta = nullptr;
  TRAF in_Taus_dz = nullptr;
  TRAI in_Taus_decayMode = nullptr;
  TRAC in_Taus_idDeepTau2017v2p1VSjet = nullptr;
  TRAC in_Taus_idDeepTau2017v2p1VSe = nullptr;
  TRAC in_Taus_idDeepTau2017v2p1VSmu = nullptr;

//  std::vector<float> out_Muons_pt;
//  std::vector<float> out_Muons_eta;
//  std::vector<float> out_Muons_phi;
//  std::vector<float> out_Muons_mass;
//  std::vector<int> out_Muons_charge;
//  std::vector<float> out_Muons_relIso;
//  std::vector<int> out_Muons_tightId;
//  std::vector<int> out_Muons_isPFcand;
//  std::vector<int> out_Muons_isGlobal;
//  std::vector<int> out_Muons_isTracker;

//  std::vector<float> out_Electrons_pt;
//  std::vector<float> out_Electrons_eta;
//  std::vector<float> out_Electrons_phi;
//  std::vector<float> out_Electrons_mass;
//  std::vector<int> out_Electrons_charge;
//  std::vector<float> out_Electrons_relIso;
//  std::vector<int> out_Electrons_id;
//  std::vector<float> out_Electrons_dEtaSC;
//  std::vector<int> out_Electrons_vidBitmap;

private:
  bool _doCppOutput = false;

  unsigned short out_nGoodLeptonRemake;

};

#endif
