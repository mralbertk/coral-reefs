"""Configuration file"""

# Import all existing filters TODO: Make less clunky
import models.uwiColorRestore.dcp as dcp
import models.uwiColorRestore.gbdehazingrcorrection as gbdehaze
import models.uwiColorRestore.lowComplexityDcp as lcdcp
import models.uwiEnhance.CLAHE as clahe
import models.uwiEnhance.GC as gc
import models.uwiEnhance.HE as he
import models.uwiEnhance.ICM as icm
import models.uwiEnhance.RayleighDistribution as rayleigh
import models.uwiEnhance.RGHS as rghs
import models.uwiEnhance.UCM as ucm

# Application paths
paths = {'export': '../storage/export/',
         'preview': '../storage/preview/'}

# Command pattern. The backend uses this dictionary
# to tell the frontend what filters are available.
models = {"DCP":
              {"func": dcp.dcp,
               "params": {
                   "omega": {"type": "slider", "min": 0.01, "max": 1.00,
                             "default": 0.01, "step": 0.01},
                   "t0": {"type": "slider", "min": 0.1, "max": 1.0,
                          "default": 0.1, "step": 0.1},
                   "blockSize": {"type": "slider", "min": 3, "max": 25,
                                 "default": 15, "step": 2},
                   "percent": {"type": "slider", "min": 0.001, "max": 0.1,
                               "default": 0.001, "step": 0.001},
                   "meanMode": {"type": "selectbox", "options": ("True", "False"),
                                "default": 1}
               }
               },
          "CLAHE":
              {"func": clahe.clahe, "params": {}},
          "GBDehazingRCorrection":
              {"func": gbdehaze.gbdehazingrcoorection, "params": {}},
          "LowComplexityDCP":
              {"func": lcdcp.low_complexity_dcp, "params": {}},
          "GC":
              {"func": gc.gc, "params": {}},
          "HE":
              {"func": he.he, "params": {}},
          "ICM":
              {"func": icm.icm, "params": {}},
          "RayleighDistribution":
              {"func": rayleigh.rayleigh_distribution, "params": {}},
          "RGHS":
              {"func": rghs.rghs, "params": {}},
          "UCM":
              {"func": ucm.ucm, "params": {}}
          }
