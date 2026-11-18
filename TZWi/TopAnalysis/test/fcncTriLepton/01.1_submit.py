#!/usr/bin/env python
import os
modes = ["NANOAOD"]
baseDir = "NanoAOD/2018"

nFilePerJob = int(os.environ["NFILE"]) if "NFILE" in os.environ else 1
if not os.path.exists("submit_2018"): os.mkdir("submit_2018")

import yaml
from glob import glob
procInfo = yaml.load(open("config/grouping.yaml").read())["processes"]
datasetInfo = {}
for f in glob("%s/*.yaml" % baseDir):
    for datasetGroup, dataset in yaml.load(open(f).read())['dataset'].iteritems():
        datasetInfo[datasetGroup] = dataset.keys()

fLists = []
toSubmit = {}
for proc in procInfo:
    for datasetGroup in procInfo[proc]['datasets']:
        if datasetGroup not in datasetInfo: continue

        for dataset in datasetInfo[datasetGroup]:
            fLists = glob("%s/*/%s/%s.txt" % (baseDir, datasetGroup, dataset.replace('/','.')[1:]))
            for fList in fLists:
                if fList not in toSubmit: toSubmit[fList] = []
                toSubmit[fList].extend(procInfo[proc]['modes'] if 'modes' in procInfo[proc] else modes)
for v in toSubmit.values(): v = set(v)

from math import ceil
for fList, modes in toSubmit.iteritems():
    for mode in modes:
        nFiles = len([x for x in open(fList).readlines() if len(x) != 0 and x[0] != '#'])
        nJobs = ceil(1.*nFiles/nFilePerJob)

        jobName = "%s.%s" % (mode, os.path.basename(fList)[:-4])
        cmd = "cd submit_2018; create-batch_mine bash ../01_prod_ntuple.sh %s ../%s %d --jobName %s -T --nJobs %d" % (mode, fList, nFilePerJob, jobName, nJobs)
        os.system(cmd)

