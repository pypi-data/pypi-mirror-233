"""
Plot Domain Stresses with `Matplotlib`
======================================

Make a 2d contour plot about the stresses of a domain.

"""
# %% [markdown]
# This example requires matplotlib to be installed

from axisvm.com.client import start_AxisVM
import axisvm.com.tlb as axtlb
from axisvm import examples
import matplotlib.pyplot as plt

axvm = start_AxisVM(visible=False, daemon=True)
axvm.model = examples.download_plate_ss()

axm = axvm.model
axm.Calculation.LinearAnalysis()

fig, ax = plt.subplots(figsize=(20, 4))

mpl_kw = dict(
    nlevels=15,
    cmap="rainbow",
    axis="on",
    offset=0.0,
    cbpad=0.5,
    cbsize=0.3,
    cbpos="right",
    fig=fig,
    ax=ax,
)

axm.Domains[1].plot_dof_solution(component="uz", mpl_kw=mpl_kw, case=1)

# %% [markdown]

axvm.Quit()
