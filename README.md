# FCNC with tau for UL Run 2

Use CMSSW_10_2_25. From its empty `src` directory, run
`git clone -b <era> <repository-url> .`

Available branches: `20UL16APV`, `20UL16`, `20UL17`, `20UL18`.

## Produce the analysis NanoAOD samples

This is the first stage of the FCNC analysis. It adds the TopLeptonMVA scores to the NanoAOD samples used as input to the main analysis. The example below uses the [`20UL18` branch](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/tree/20UL18). The other Run 2 eras follow the same workflow with their corresponding branches.

### Build the code

After cloning, both `PhysicsTools/` and `TZWi/` should be directly under `CMSSW_10_2_25/src/`. From that `src/` directory, set up the CMSSW environment and build the code:

```bash
cmsenv
scram b -j 4
```

### Prepare the dataset file lists

The datasets required for 2018 are listed in the YAML files under [`2018_ExactlySameSamples_v16/`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/tree/20UL18/TZWi/NanoAODProduction/data/datasets/NanoAOD/2018_ExactlySameSamples_v16). From that directory, run [`tzwi-updatedataset_mine`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/TZWi/NanoAODProduction/scripts/tzwi-updatedataset_mine) to generate the list of input ROOT file paths for each dataset:

```bash
cd "$CMSSW_BASE/src/TZWi/NanoAODProduction/data/datasets/NanoAOD/2018_ExactlySameSamples_v16"
tzwi-updatedataset_mine *.yaml
```

Return to the [parent `NanoAOD/` directory](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/tree/20UL18/TZWi/NanoAODProduction/data/datasets/NanoAOD). Move aside or remove the existing `2018/` directory first, then copy `2018_ExactlySameSamples_v16/` to `2018/`:

```bash
cd "$CMSSW_BASE/src/TZWi/NanoAODProduction/data/datasets/NanoAOD"
cp -r 2018_ExactlySameSamples_v16 2018
```

### Processing sequence and TopLeptonMVA

The production script [`01_prod_ntuple.sh`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/TZWi/TopAnalysis/test/fcncTriLepton/01_prod_ntuple.sh) defines the order in which the modules run. It first applies a preselection to reduce the dataset size. The selection at this stage is looser than the selection used in the main analysis.

```bash
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.flags flags_${DATATYPE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonHLT hlt_${HLTMODULE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLepton fcnc_${CHANNEL}_${YEAR}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonCutFlow cutFlow_${CHANNEL}"
```

The script then runs [`leptonvariables.py`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/PhysicsTools/nanoSkimming/python/processing/leptonvariables.py) to calculate the input variables, followed by [`topleptonmva.py`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/PhysicsTools/nanoSkimming/python/processing/topleptonmva.py) to compute the TopLeptonMVA scores. This analysis uses **TopLeptonMVA ULv1**, the same version used in the two CMS analysis notes I consulted. I checked this by reproducing the control plots.

### Submit the jobs and collect the output

From `TZWi/TopAnalysis/test/fcncTriLepton/`, run [`01.1_submit.py`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/TZWi/TopAnalysis/test/fcncTriLepton/01.1_submit.py) to submit the production jobs:

```bash
cd "$CMSSW_BASE/src/TZWi/TopAnalysis/test/fcncTriLepton"
./01.1_submit.py
```

Once the batch jobs have finished, run [`01.2_checkFailed_2018.sh`](https://github.com/panthera718/FCNC_withtau_20ULRun2_RemakeNANOAOD/blob/20UL18/TZWi/TopAnalysis/test/fcncTriLepton/01.2_checkFailed_2018.sh) from the same directory to check for reported failures:

```bash
./01.2_checkFailed_2018.sh
```

After checking the jobs, enter `submit_2018/` and run `makentuple2018` to extract the output ROOT files:

```bash
cd submit_2018
makentuple2018
```

The output is organized by dataset under `submit_2018/`:

```text
ntuple_2018/reco/NANOAOD/<dataset>/<ROOT files>
```

These ROOT files contain the electron and muon TopLeptonMVA scores and serve as input to the main analysis.
