"""
    Console utilities
"""

import os
import glob
from dtscore import globals as gl

#--------------------------------------------------------------------------------------------------
def getanalysisfolder() -> str:
    print("analysis folder name: ", end='')
    analysisfoldername = input()
    return analysisfoldername

#--------------------------------------------------------------------------------------------------
def getdetailpath(analysisfolder:str) -> str:
    detail_filepattern = 'portfolio_detail_*.csv'
    return _do_glob(analysisfolder, detail_filepattern)

#--------------------------------------------------------------------------------------------------
def getholdingdetailpath(analysisfolder:str) -> str:
    holdingdetail_filepattern = 'portfolio_holdingdetail_*.csv'
    return _do_glob(analysisfolder, holdingdetail_filepattern)

#--------------------------------------------------------------------------------------------------
def getcutoffandplotrange() -> tuple[str,str]:
    print('enter cutoff date (yyyymmdd): ', end='')
    cutoff = input()

    print(f'plot range start date (yyyymmdd) or enter for {cutoff} default: ', end='')
    response = input()
    startdate = response if len(response) > 0 else cutoff
    print(f'plot range end date (yyyymmdd): ', end='')
    enddate = input()
    plotrange = f'{startdate} - {enddate}'
    return cutoff, plotrange

#--------------------------------------------------------------------------------------------------
#   private methods
def _do_glob(analysisfolder:str, pattern:str) -> str:
    globpath = os.path.join(gl.apphome,gl.analysesfolder,analysisfolder, gl.reportsfolder, pattern)
    all_filenames = glob.glob(globpath, recursive=False)
    #   !!proper sorting relies on date stamped file names!!
    all_filenames.sort(reverse=True)
    #   select the latest filename
    return all_filenames[0]
