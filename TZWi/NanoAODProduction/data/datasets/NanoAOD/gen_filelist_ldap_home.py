import sys, os, fnmatch

central = {
"MC2016.DYJetsToLL_M-10to50": "DYJetsToLL_M-10to50",
"MC2016.DYJetsToLL_M-50": "DYJetsToLL_M-50",
"MC2016.STbar_t": "ST_t-channel_antitop",
"MC2016.STbar_tW": "ST_tW_antitop",
"MC2016.ST_s_4f_lepton": "ST_s-channel",
"MC2016.ST_t": "ST_t-channel_top",
"MC2016.ST_tW": "ST_tW_top",
"MC2016.TTToHadronic": "TTToHadronic",
"MC2016.TTToSemiLeptonic": "TTToSemiLeptonic",
"MC2016.TTTo2L2Nu": "TTTo2L2Nu",
"MC2016.WWTo2L2Nu": "WWTo2L2Nu",
"MC2016.WZTo3LNu": "WZTo3LNu",
"MC2016.ZZTo4L": "ZZTo4L"
}
rareprocess = {
"MC2016.ST_FCNC-TLL_zct": "ST_FCNC-TLL_Tleptonic_kappa_zct",
"MC2016.ST_FCNC-TLL_zut": "ST_FCNC-TLL_Tleptonic_kappa_zut",
"MC2016.TT_FCNC-aT2ZJ_zct": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zct",
"MC2016.TT_FCNC-aT2ZJ_zut": "TT_FCNC-aT2ZJ_Tleptonic_ZToll_kappa_zut",
"MC2016.TT_FCNC-T2ZJ_zct": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zct",
"MC2016.TT_FCNC-T2ZJ_zut": "TT_FCNC-T2ZJ_aTleptonic_ZToll_kappa_zut",
"MC2016.ttHTobb": "ttHTobb_M125",
"MC2016.ttHToNonbb": "ttHToNonbb_M125",
"MC2016.TTWJetsToLNu": "TTWJetsToLNu",
"MC2016.TTWJetsToQQ": "TTWJetsToQQ",
"MC2016.TTZToLLNuNu": "TTZToLLNuNu",
"MC2016.TTZToQQ": "TTZToQQ",
"MC2016.tZq_ll": "tZq_ll"
}
data = {
"Run2016.DoubleEG": "DoubleEG",
"Run2016.DoubleMuon": "DoubleMuon"
}

Run2016 = {"MC.RunIISummer16.central": central, "MC.RunIISummer16.rareprocess": rareprocess, "RD.Run2016": data}

dir_xrd = ""
dir_xrootd = ""
dir_store = "/cms/ldap_home/yhoonlee/FCNC/FCNC_20UL16_RemakeNANOAOD_jetmetUncertainties_postVFP/CMSSW_10_2_25/src/TZWi/TopAnalysis/test/fcncTriLepton/ntuple_RunIISummer20UL16NanoAODv9_postVFP_jetmet/reco/NANOAODjetmet"
basedir = dir_xrootd + dir_store

for i in os.listdir(basedir):
    for process in Run2016.values():
        process_key = list(Run2016.keys())[list(Run2016.values()).index(process)]
        if not os.path.exists(process_key):
            os.system("mkdir %s"%process_key)
        for sub_process in process.values():
            sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
            if sub_process in i:
                if not os.path.exists("%s/%s"%(process_key,sub_process_key)):
                    os.system("mkdir %s/%s"%(process_key,sub_process_key))
                os.system("ls %s/%s/*.root > %s/%s/%s.txt"%(basedir,i,process_key,sub_process_key,i))

path = os.path.dirname(os.path.realpath(__file__))
find_str = dir_xrootd
replace_str = dir_xrd
filePattern = "*.txt"

for path, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        with open(filepath) as f:
            s = f.read()
        if s.find(find_str) != -1:
            s = s.replace(find_str, replace_str)
            with open(filepath, 'w') as f:
                f.write(s)

for process in Run2016.values():
    process_key = list(Run2016.keys())[list(Run2016.values()).index(process)]
    process_key_yaml = process_key + ".yaml"
    f = open(process_key_yaml, "w")
    f.write("dataset:\n")
    for sub_process in process.values():
        sub_process_key = list(process.keys())[list(process.values()).index(sub_process)]
        sub_process_key_str = "    " + sub_process_key + ":\n"
        f.write(sub_process_key_str)
        for i in os.listdir(basedir):
            if sub_process in i:
                filekey = "        /" + i + ":\n"
                filekey_mod = filekey.replace(".","/")
                f.write(filekey_mod)
                filedir = "        - " + basedir + "/" + i + "\n"
                f.write(filedir)
    f.close()
