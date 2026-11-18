from TZWi.TopAnalysis.postprocessing.CombineHLT import CombineHLT

flags_MC2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="RunIISummer17", doFilter=True)
flags_Run2017 = lambda : CombineHLT(outName="Flag", fileName="flags/2017.yaml", hltSet="Run2017", doFilter=True)
