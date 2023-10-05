"""
Screenshot
==========

Make and show a screenshot about AxisVM!

"""

from axisvm.com.client import start_AxisVM
import axisvm.com.tlb as axtlb
from axisvm import examples
import matplotlib.pyplot as plt

axvm = start_AxisVM(visible=True, daemon=True)
axvm.model = examples.download_bernoulli_grid()

axm = axvm.model
axm.Calculation.LinearAnalysis()

# turn off the grid
GridOptions = axtlb.RGridOptions(DisplayGrid=False)
axm.Settings.SetGridOptions(GridOptions)

axvm.BringToFront()
axm.View = axtlb.vFront
axvm.MainFormTab = axtlb.mftGeometry
axm.FitInView()
plt.imshow(axm.Windows[1].screenshot())

# %% [markdown]

axvm.Quit()
