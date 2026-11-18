from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

flags_MC2018 = lambda : CombineHLT(outName="Flag", fileName="flags/2018.yaml", hltSet="RunIISummer18", doFilter=True)
flags_Run2018 = lambda : CombineHLT(outName="Flag", fileName="flags/2018.yaml", hltSet="Run2018", doFilter=True)
