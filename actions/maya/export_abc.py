
param_string = "-frameRange " + {0} + " -root " + {1} + " -file " + {2}

import pymel.core as pm
pm.AbcExport(j=param_string)
