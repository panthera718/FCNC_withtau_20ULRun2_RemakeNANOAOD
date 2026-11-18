#ifndef PhysicsTools_NanoAODTools_LeptonEfficiencyCorrector_h
#define PhysicsTools_NanoAODTools_LeptonEfficiencyCorrector_h

#include <iostream>
#include <string>
#include <vector>
#include <TH2.h>
#include <TFile.h>
#include <cmath>

#include "PhysicsTools/NanoAODTools/src/WeightCalculatorFromHistogram.cc"

class LeptonEfficiencyCorrector {
 public:

  LeptonEfficiencyCorrector() {effmaps_.clear();}
  LeptonEfficiencyCorrector(std::vector<std::string> files, std::vector<std::string> histos);
  ~LeptonEfficiencyCorrector() {}

  void setLeptons(int nLep, int *lepPdgId, float *lepPt, float *lepEta);

  float getSF(int pdgid, float pt, float eta);
  float getTrigSF(float pt, float eta);
  float getSFErr(int pdgid, float pt, float eta);
  const std::vector<float> & run();

private:
  std::vector<TH2F*> effmaps_;
  std::vector<float> ret_;
  int nLep_;
  float *Lep_eta_, *Lep_pt_;
  int *Lep_pdgId_;
};

LeptonEfficiencyCorrector:: LeptonEfficiencyCorrector(std::vector<std::string> files, std::vector<std::string> histos) {
  effmaps_.clear();
  if(files.size()!=histos.size()) {
    std::cout << "ERROR! There should be one histogram per input file! Returning 0 as SF." << std::endl;
    return;
  }

  for(int i=0; i<(int)files.size();++i) {
    TFile *f = TFile::Open(files[i].c_str(),"read");
    if(!f) {
      std::cout << "WARNING! File " << files[i] << " cannot be opened. Skipping this scale factor " << std::endl;
      continue;
    }
    TH2F *hist = (TH2F*)(f->Get(histos[i].c_str()))->Clone(("eff_"+histos[i]).c_str());
    hist->SetDirectory(0);
    if(!hist) {
      std::cout << "ERROR! Histogram " << histos[i] << " not in file " << files[i] << ". Not considering this SF. " << std::endl;
      continue;
    } else {
      std::cout << "Loading histogram " << histos[i] << " from file " << files[i] << "... " << std::endl;
    }
    effmaps_.push_back(hist);
    f->Close();
  }
}

void LeptonEfficiencyCorrector::setLeptons(int nLep, int *lepPdgId, float *lepPt, float *lepEta) {
  nLep_ = nLep; Lep_pdgId_ = lepPdgId; Lep_pt_ = lepPt; Lep_eta_ = lepEta;
}

float LeptonEfficiencyCorrector::getSF(int pdgid, float pt, float eta) {
  float out=1.;

  if ( abs(pdgid)==13 ) {
    if (pt >= 120.) { pt = 119.; }
    else if (pt <= 15.) { pt = 16.; }
  } else {
    if (pt >= 500.) { pt = 499.; }
    else if (pt <= 10.) { pt = 11.; }
  }

  float x = abs(pdgid)==13 ? fabs(eta) : eta;
//  float y = abs(pdgid)==13 ? fabs(eta) : pt;
  float y = pt;
  for(std::vector<TH2F*>::iterator hist=effmaps_.begin(); hist<effmaps_.end(); ++hist) {
    WeightCalculatorFromHistogram wc(*hist);
    out *= wc.getWeight(x,y);
  }
  return out;
}

//float LeptonEfficiencyCorrector::getTrigSF(float pt, float eta) {
//  float out=1.;
//  float x = eta;
//  if (pt >= 200.) { pt = 199.; }
//  else if (pt <= 26.) { pt = 27.; }
//  float y = pt;
//  for(std::vector<TH2F*>::iterator hist=effmaps_.begin(); hist<effmaps_.end(); ++hist) {
//    WeightCalculatorFromHistogram wc(*hist);
//    out *= wc.getWeight(x,y);
//  }
//  return out;
//}

float LeptonEfficiencyCorrector::getTrigSF(float lep1_pt, float lep2_pt) {
  float out=1.;
  if (lep1_pt >= 500.) { lep1_pt = 499.; }
  else if (lep1_pt <= 20.) { lep1_pt = 19.; }
  float x = lep1_pt;
  if (lep2_pt >= 500.) { lep2_pt = 499.; }
  else if (lep2_pt <= 20.) { lep2_pt = 19.; }
  float y = lep2_pt;
  for(std::vector<TH2F*>::iterator hist=effmaps_.begin(); hist<effmaps_.end(); ++hist) {
    WeightCalculatorFromHistogram wc(*hist);
    out *= wc.getWeight(x,y);
  }
  return out;
}

float LeptonEfficiencyCorrector::getSFErr(int pdgid, float pt, float eta) {
  float out=0.;

  if ( abs(pdgid)==13 ) {
    if (pt >= 120.) { pt = 119.; }
    else if (pt <= 15.) { pt = 16.; }
  } else {
    if (pt >= 500.) { pt = 499.; }
    else if (pt <= 10.) { pt = 11.; }
  }

  //float x = pt;
  //float y = abs(pdgid)==13 ? fabs(eta) : eta;
  float x = abs(pdgid)==13 ? fabs(eta) : eta;
//  float y = abs(pdgid)==13 ? fabs(eta) : pt;
  float y = pt;
  for(std::vector<TH2F*>::iterator hist=effmaps_.begin(); hist<effmaps_.end(); ++hist) {
    WeightCalculatorFromHistogram wc(*hist);
    out += pow(wc.getWeightErr(x,y), 2.0);
  }
  return sqrt(out);
}

const std::vector<float> & LeptonEfficiencyCorrector::run() {
  ret_.clear();
  for (int iL = 0, nL = nLep_; iL < nL; ++iL) {
    ret_.push_back(getSF((Lep_pdgId_)[iL], (Lep_pt_)[iL], (Lep_eta_)[iL]));
  }
  return ret_;
}

#endif
