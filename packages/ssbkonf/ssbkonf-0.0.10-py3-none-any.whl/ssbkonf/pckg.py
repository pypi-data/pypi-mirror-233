from rpy2.robjects.packages import importr

utils = importr("utils")


def importr_tryhard(packname):
    try:
        rpack = importr(packname)
    except:
        utils.chooseCRANmirror(ind=1)
        utils.install_packages(packname)
        rpack = importr(packname)
    return rpack


__ssbtools = importr_tryhard("SSBtools")
