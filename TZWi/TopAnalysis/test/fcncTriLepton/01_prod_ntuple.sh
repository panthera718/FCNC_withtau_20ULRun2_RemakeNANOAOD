#!/bin/bash

if [ $# != 4 ]; then
    echo $#
    echo "Usage: $0 MuElEl MC2016.WW.txt 10 5 ## process WW sample assuming muee channel, split by 10 files and run 5th section"
    echo "Usage: $0 ElElEl MC2017.TT_powheg.txt 1 0 ## process TTbar sample assuming eee channel, one file per each section and run 0th one."
    echo "Usage: $0 MuMuMu Run2016B.DoubleMuon.txt 1 0"
    exit 1
fi

eval `scram runtime -sh`

CHANNEL=$1
FILELIST=$2
MAXFILES=$3
JOBNUMBER=$4

case $CHANNEL in
  ElElMu|ElMuEl)
    CHANNEL=MuElEl
    ;;
  MuMuEl|MuElMu)
    CHANNEL=ElMuMu
    ;;
esac

DATASET0=`basename $FILELIST | sed -e 's;.txt;;g'`
DATASET='/'`echo $DATASET0 | sed -e 's;\.;/;g'`
ERA=$(echo $DATASET0 | cut -d. -f2 | cut -d- -f1 | sed -e 's;NanoAOD;;g')

DATATYPE=$(basename $(dirname $FILELIST) | cut -d. -f1)
YEAR=${DATATYPE:(-4)}
if [ ${DATATYPE::3} == "Run" ]; then
  HLTMODULE=${ERA::8}_$(echo $DATASET | cut -d/ -f2)
else
  HLTMODULE=$(echo $DATATYPE | cut -d_ -f1)
fi

FILENAMES=$(cat $FILELIST | xargs -n$MAXFILES | sed -n "$(($JOBNUMBER+1)) p" | sed 's;^/xrootd/;root://cms-xrdr.private.lo:2094//xrd/;g')

ARGS=""
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.flags flags_${DATATYPE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonHLT hlt_${HLTMODULE}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLepton fcnc_${CHANNEL}_${YEAR}"
ARGS="$ARGS -I TZWi.TopAnalysis.postprocessing.fcncTriLeptonCutFlow cutFlow_${CHANNEL}"
ARGS="$ARGS -I PhysicsTools.nanoSkimming.processing.leptonvariables leptonvariables"
ARGS="$ARGS -I PhysicsTools.nanoSkimming.processing.topleptonmva topleptonmva_${YEAR}_ULv1"

if [ $DATATYPE == "Run2018" ]; then
    if [[ A =~ ${ERA:7:8} ]];then
        ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertaintiesNew19UL${YEAR}DataA"
    elif [[ B =~ ${ERA:7:8} ]];then
        ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertaintiesNew19UL${YEAR}DataB"
    elif [[ C =~ ${ERA:7:8} ]];then
        ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertaintiesNew19UL${YEAR}DataC"
    elif [[ D =~ ${ERA:7:8} ]];then
        ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertaintiesNew19UL${YEAR}DataD"
    fi
elif [ ${DATATYPE::2} == "MC" ]; then
    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties jetmetUncertaintiesNew19UL${YEAR}MC"
    ARGS="$ARGS -I PhysicsTools.NanoAODTools.postprocessing.modules.jme.jecUncertainties jecUncertAll_19UL${YEAR}MC"
fi

BRANCHSEL="$CMSSW_BASE/src/TZWi/NanoAODProduction/data/branchsel.txt"
CMD="nano_postproc.py --bo $BRANCHSEL"

OUTPATH=ntuple_$YEAR/reco/$CHANNEL/$DATASET0
[ ! -d $OUTPATH ] && mkdir -p $OUTPATH
if [ ${DATATYPE::2} == "MC" ]; then
    ARGS="-I PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule countHistogramsModule $ARGS"
fi
echo $CMD $ARGS $OUTPATH $FILENAMES
$CMD $ARGS $OUTPATH $FILENAMES
[ $? -eq 0 ] || echo $CMD $ARGS $OUTPATH $FILENAMES >> failed.txt

