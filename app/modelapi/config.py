"""Configuration file"""

# Application paths
paths = {'export': '../storage/export/',
         'preview': '../storage/preview/'

}

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

# Command pattern. The backend uses this dictionary to
# tell the frontend what filters are available, and to
# call filters selected by users.
models = {"DCP": dcp.dcp,
          "CLAHE": clahe.clahe,
          "GBDehazingRCorrection": gbdehaze.gbdehazingrcoorection,
          "LowComplexityDCP": lcdcp.low_complexity_dcp,
          "GC": gc.gc,
          "HE": he.he,
          "ICM": icm.icm,
          "RayleighDistribution": rayleigh.rayleigh_distribution,
          "RGHS": rghs.rghs,
          "UCM": ucm.ucm}
