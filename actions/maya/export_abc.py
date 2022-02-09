export_params = {"frameRange": {0},
                 "root": {1},
                 "file": {2}}

param_string = ""
for (k, v) in export_params.items():
    param_string += "-" + str(k) + " " + str(v) + " "

import pymel.core as pm
pm.AbcExport(j=param_string)
