#include "../interface/FCNCTriLeptonCppWorker.h"
#include <iostream>
#include <cmath>
#include <algorithm>

//190306 KST 15:44 : just copy this code from FCNCTriLeptonCppWorker.cc
//
using namespace std;

//FCNCTriLeptonCppWorker::FCNCTriLeptonCppWorker(const std::string modeName, const bool doNonPromptLepton):
//  doNonPromptLepton_(doNonPromptLepton)
FCNCTriLeptonCppWorker::FCNCTriLeptonCppWorker(const std::string modeName)
{
  if ( modeName == "NANOAOD" ) mode_ = MODE::NANOAOD;
  else {
    cerr << "Mode name \"" << modeName << "\" is not available. " << endl;
    mode_ = MODE::None;//This should be changed kind of 'return false...'(do not run this worker)
  }
}

typedef FCNCTriLeptonCppWorker::TRAF TRAF;
typedef FCNCTriLeptonCppWorker::TRAI TRAI;
typedef FCNCTriLeptonCppWorker::TRAB TRAB;
typedef FCNCTriLeptonCppWorker::TRAC TRAC;

void FCNCTriLeptonCppWorker::setElectrons(TRAF pt, TRAF eta, TRAB isPFcand, TRAC lostHits,
                                          TRAF dxy, TRAF dz, TRAF sip3d, TRAF miniPFRelIso_all,
                                          TRAF sieie, TRAF hoe, TRAF eInvMinusPInv, TRAB convVeto, TRAF dEtaSC) {
  in_Electrons_pt = pt;
  in_Electrons_eta = eta;
  in_Electrons_isPFcand = isPFcand;
  in_Electrons_lostHits = lostHits;
  in_Electrons_dxy = dxy;
  in_Electrons_dz = dz;
  in_Electrons_sip3d = sip3d;
  in_Electrons_miniPFRelIso_all = miniPFRelIso_all;
  in_Electrons_sieie = sieie;
  in_Electrons_hoe = hoe;
  in_Electrons_eInvMinusPInv = eInvMinusPInv;
  in_Electrons_convVeto = convVeto;
  in_Electrons_dEtaSC = dEtaSC;
}

void FCNCTriLeptonCppWorker::setMuons(TRAF pt, TRAF eta, TRAB isPFcand, TRAB isTracker, TRAB isGlobal,
                                      TRAF dxy, TRAF dz, TRAF sip3d, TRAF miniPFRelIso_all, TRAB mediumId) {
  in_Muons_pt = pt;
  in_Muons_eta = eta;
  in_Muons_isPFcand = isPFcand;
  in_Muons_isTracker = isTracker;
  in_Muons_isGlobal = isGlobal;
  in_Muons_dxy = dxy;
  in_Muons_dz = dz;
  in_Muons_sip3d = sip3d;
  in_Muons_miniPFRelIso_all = miniPFRelIso_all;
  in_Muons_mediumId = mediumId;
}

void FCNCTriLeptonCppWorker::setTaus(TRAF pt, TRAF eta, TRAF dz, TRAI decayMode,
                                     TRAC DeepTau2017v2p1VSjet, TRAC DeepTau2017v2p1VSe, TRAC DeepTau2017v2p1VSmu) {
  in_Taus_pt = pt;
  in_Taus_eta = eta;
  in_Taus_dz = dz;
  in_Taus_decayMode = decayMode;
  in_Taus_idDeepTau2017v2p1VSjet = DeepTau2017v2p1VSjet;
  in_Taus_idDeepTau2017v2p1VSe = DeepTau2017v2p1VSe;
  in_Taus_idDeepTau2017v2p1VSmu = DeepTau2017v2p1VSmu;
}

/*
void FCNCTriLeptonCppWorker::resetValues() {

  out_Muons_pt.clear();
  out_Muons_eta.clear();
  out_Muons_phi.clear();
  out_Muons_mass.clear();
  out_Muons_charge.clear();
  out_Muons_relIso.clear();
  out_Muons_tightId.clear();
  out_Muons_isPFcand.clear();
  out_Muons_isGlobal.clear();
  out_Muons_isTracker.clear();

  out_Electrons_pt.clear();
  out_Electrons_eta.clear();
  out_Electrons_phi.clear();
  out_Electrons_mass.clear();
  out_Electrons_charge.clear();
  out_Electrons_relIso.clear();
  out_Electrons_id.clear();
  out_Electrons_dEtaSC.clear();
  out_Electrons_vidBitmap.clear();

  out_Taus_pt.clear();
  out_Taus_idDeepTau2017v2p1VSjet.clear();
  out_Taus_idDeepTau2017v2p1VSe.clear();
  out_Taus_idDeepTau2017v2p1VSmu.clear();
}
*/
//signal electrons
bool FCNCTriLeptonCppWorker::isGoodElectron(const unsigned i) const {
  if ( !( in_Electrons_pt->At(i) > 10 ) ) return false;
  if ( !( std::abs(in_Electrons_eta->At(i)) < 2.5 ) ) return false;
  const double scEta = in_Electrons_eta->At(i) + in_Electrons_dEtaSC->At(i);
  if ( std::abs(scEta) > 1.4442 and std::abs(scEta) < 1.566 ) return false;
  if ( !( in_Electrons_isPFcand->At(i) ) ) return false;
  if ( !( in_Electrons_lostHits->At(i) < 2 ) ) return false;
  if ( !( std::abs(in_Electrons_dxy->At(i)) < 0.05 ) ) return false;
  if ( !( std::abs(in_Electrons_dz->At(i)) < 0.1 ) ) return false;
  if ( !( in_Electrons_sip3d->At(i) < 8 ) ) return false;
  if ( !( in_Electrons_miniPFRelIso_all->At(i) < 0.4 ) ) return false;
  if ( !( ((std::abs(in_Electrons_eta->At(i)) < 1.479) && (in_Electrons_sieie->At(i) < 0.011))
          || ((std::abs(in_Electrons_eta->At(i)) >= 1.479) && (in_Electrons_sieie->At(i) < 0.030)) ) ) return false;
  if ( !( in_Electrons_hoe->At(i) < 0.10 ) ) return false;
  if ( !( in_Electrons_eInvMinusPInv->At(i) > -0.04 ) ) return false;
  if ( !( in_Electrons_convVeto->At(i) ) ) return false;

  return true;
}

//signal muons
bool FCNCTriLeptonCppWorker::isGoodMuon(const unsigned i) const {
  if ( !( in_Muons_pt->At(i) > 10 ) ) return false;
  if ( !( std::abs(in_Muons_eta->At(i)) < 2.4 ) ) return false;
  if ( !( in_Muons_isPFcand->At(i) ) ) return false;
  if ( !( in_Muons_isTracker->At(i) || in_Muons_isGlobal->At(i) ) ) return false;
  if ( !( std::abs(in_Muons_dxy->At(i)) < 0.05 ) ) return false;
  if ( !( std::abs(in_Muons_dz->At(i)) < 0.1 ) ) return false;
  if ( !( in_Muons_sip3d->At(i) < 8 ) ) return false;
  if ( !( in_Muons_miniPFRelIso_all->At(i) < 0.4 ) ) return false;
  if ( !( in_Muons_mediumId->At(i) ) ) return false;

  return true;
}

////signal taus
//bool FCNCTriLeptonCppWorker::isGoodTau(const unsigned i) const {
//  if ( !( in_Taus_pt->At(i) > 15 ) ) return false;
//  if ( !( in_Taus_eta->At(i) < 2.3 ) ) return false;
//  if ( !( in_Taus_dz->At(i) < 0.2 ) ) return false;
//  if ( ( in_Taus_decayMode->At(i) == 5 ) or ( in_Taus_decayMode->At(i) == 6 ) ) return false;
////  if ( !( in_Taus_idDeepTau2017v2p1VSjet->At(i) > 1 ) ) return false;
////  if ( !( in_Taus_idDeepTau2017v2p1VSe->At(i) > 0 ) ) return false;
////  if ( !( in_Taus_idDeepTau2017v2p1VSmu->At(i) > 0 ) ) return false;
//
//  return true;
//}
//signal taus
bool FCNCTriLeptonCppWorker::isGoodTau(const unsigned i) const {
  if ( !( in_Taus_pt->At(i) > 15 ) ) return false;
  if ( !( in_Taus_eta->At(i) < 2.3 ) ) return false;
  if ( !( in_Taus_dz->At(i) < 0.2 ) ) return false;
  if ( ( in_Taus_decayMode->At(i) == 5 ) || ( in_Taus_decayMode->At(i) == 6 ) ) return false;

  if ( !( in_Taus_idDeepTau2017v2p1VSjet->At(i) & 2 ) ) return false;
  if ( !( in_Taus_idDeepTau2017v2p1VSe->At(i) & 1 ) ) return false;
  if ( !( in_Taus_idDeepTau2017v2p1VSmu->At(i) & 1 ) ) return false;

  return true;
}

/*
void FCNCTriLeptonCppWorker::setRecoElectrons(const unsigned i) {
  out_Electrons_pt.push_back( in_Electrons_pt->At(i) );
  out_Electrons_eta.push_back( in_Electrons_eta->At(i) );
  out_Electrons_phi.push_back( in_Electrons_phi->At(i) );
  out_Electrons_mass.push_back( in_Electrons_mass->At(i) );
  out_Electrons_relIso.push_back( in_Electrons_relIso->At(i) );
  out_Electrons_dEtaSC.push_back( in_Electrons_dEtaSC->At(i) );
  out_Electrons_charge.push_back( in_Electrons_charge->At(i) );
  out_Electrons_id.push_back( in_Electrons_id->At(i) );
  out_Electrons_vidBitmap.push_back( in_Electrons_vidBitmap->At(i) );
}

void FCNCTriLeptonCppWorker::setRecoMuons(const unsigned i) {
  out_Muons_pt.push_back( in_Muons_pt->At(i) );
  out_Muons_eta.push_back( in_Muons_eta->At(i) );
  out_Muons_phi.push_back( in_Muons_phi->At(i) );
  out_Muons_mass.push_back( in_Muons_mass->At(i) );
  out_Muons_relIso.push_back( in_Muons_relIso->At(i) );
  out_Muons_charge.push_back( in_Muons_charge->At(i) );
  out_Muons_tightId.push_back( in_Muons_tightId->At(i) );
  out_Muons_isPFcand.push_back( in_Muons_isPFcand->At(i) );
  out_Muons_isGlobal.push_back( in_Muons_isGlobal->At(i) );
  out_Muons_isTracker.push_back( in_Muons_isTracker->At(i) );
}

void FCNCTriLeptonCppWorker::setRecoTaus(const unsigned i) {
  out_Taus_pt.push_back( in_Taus_pt->At(i) );
  out_Taus_idDeepTau2017v2p1VSjet.push_back( in_Taus_idDeepTau2017v2p1VSjet->At(i) );
  out_Taus_idDeepTau2017v2p1VSje.push_back( in_Taus_idDeepTau2017v2p1VSe->At(i) );
  out_Taus_idDeepTau2017v2p1VSjmu.push_back( in_Taus_idDeepTau2017v2p1VSmu->At(i) );
}
*/
bool FCNCTriLeptonCppWorker::analyze() {
//  resetValues();

  // Select leptons
  std::vector<unsigned> muonIdxs;
  std::vector<unsigned> electronIdxs;
  std::vector<unsigned> tauIdxs;
  for ( unsigned i=0, n=in_Muons_pt->GetSize(); i<n; ++i ) {
    if ( isGoodMuon(i) ) muonIdxs.push_back(i);
  }
  for ( unsigned i=0, n=in_Electrons_pt->GetSize(); i<n; ++i ) {
    if ( isGoodElectron(i) ) electronIdxs.push_back(i);
  }
  for ( unsigned i=0, n=in_Taus_pt->GetSize(); i<n; ++i ) {
    if ( isGoodTau(i) ) tauIdxs.push_back(i);
  }

  std::sort(muonIdxs.begin(), muonIdxs.end(), [&](const int i, const int j){
            return in_Muons_pt->At(i) > in_Muons_pt->At(j);});
  std::sort(electronIdxs.begin(), electronIdxs.end(), [&](const int i, const int j){
            return in_Electrons_pt->At(i) > in_Electrons_pt->At(j);});
  std::sort(tauIdxs.begin(), tauIdxs.end(), [&](const int i, const int j){
            return in_Taus_pt->At(i) > in_Taus_pt->At(j);});

  const int nGoodLeptonRemake = electronIdxs.size() + muonIdxs.size() + tauIdxs.size();
  out_nGoodLeptonRemake = nGoodLeptonRemake;
/*
  auto actualMode = mode_;
  if ( actualMode == MODE::NANOAOD ) {
    if ( electronIdxs.size() + muonIdxs.size() >= 3 ) {
      if ( electronIdxs.size() >= 1 ) {
        setRecoElectrons( electronIdxs[0] );
      }
      if ( electronIdxs.size() >= 2 ) {
        setRecoElectrons( electronIdxs[1] );
      }
      if ( electronIdxs.size() >= 3 ) {
        setRecoElectrons( electronIdxs[2] );
      }
      if ( muonIdxs.size() >= 1 ) {
        setRecoMuons( muonIdxs[0] );
      }
      if ( muonIdxs.size() >= 2 ) {
        setRecoMuons( muonIdxs[1] );
      }
      if ( muonIdxs.size() >= 3 ) {
        setRecoMuons( muonIdxs[2] );
      }
    }
  }
*/
  return true;
}

