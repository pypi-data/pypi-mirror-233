#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3rd party imports
import matplotlib.dates as dates
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseButton
from matplotlib.widgets import Button

from ..plot import plot_line

# Local imports
from .avg_4sc import avg_4sc
from .iso86012unix import iso86012unix
from .resample import resample
from .t_eval import t_eval

__author__ = "Atlas Silverhult"
__email__ = "atlas.silverhult.9977@student.uu.se"
__copyright__ = "Copyright 2020-2023"
__license__ = "MIT"
__version__ = "2.4.2"
__status__ = "Prototype"

__all__ = ["timing_gui"]


def _get_disc_vel(t, tau, r_list):
    # tetrahedron center
    rstar = t_eval(avg_4sc(r_list), t)
    # position vectors with origin in tetrahedron center
    r_list_star = [t_eval(r_, t) - rstar for r_ in r_list]

    # get position tensor Rstar (1)
    r_start = sum([np.outer(r_, r_.T) for r_ in r_list_star])

    # generelazied reciprocal vectors q (3) (q=k)
    q_list = [np.linalg.inv(r_start) @ rstar_.T.data for rstar_ in r_list_star]

    # get slowness vector (17)
    m = sum([q_list[i] * tau[i] for i in range(4)])
    # tidy
    m = m.T[0]

    # normal vector from (9)
    n = m / np.linalg.norm(m)

    # disc vel from (9)
    v = 1 / np.linalg.norm(m)

    return m, n, v


def _print_output(tau, m, n, v, header):
    pad = 15
    topstr = "-" * pad + f"{header}" + "-" * pad
    print("\n" + topstr)
    print(f"time diff from {header} (seconds):\n{tau}")
    print("\nn: ", n)
    print("m [s/km]: ", m)
    print("V [km/s]: ", v)
    print("-" * len(topstr))


def timing_gui(b_list: list, r_list: list, comp: int = 0):
    r"""GUI to perform manual timing analysis by clicking. Limited to 4 spacecraft only.
    The return of this function is a callback to the GUI object and class attributes
    like the slowness vector are accesable through this callback by the methods
    'get_slowness', 'get_normal' and 'get_vel'.

    Usage:
    Before cicking the 'Start timing' button, right clicking will place a vertical
    line to mark a timestamp of interest. After clicking 'Start timing' the four
    signals will be highlighted one at a time, indicating which signal should be
    clicked. For each signal, use RIGHT CLICK to mark the time and move on to the next
    one. By using LEFT CLICK, one can undo the selection for the previously selected
    signal(s). Once the times have been marked for each signal, the 'Calculate normal'
    button will calculate the speed and normal vector based on the input times.

    Parameters
    ----------
    b_list : list of xarray.DataArray
        List of magnetic field time series for each sc.
    r_list : list of xarray.DataArray
        List of coordinate time series for each sc.
    comp : int, Optional
        Component to use. Default uses first component.

    Returns
    -------
    timing_gui_callback : TYPE
        Returns TimingGui object to access attributes. In order to keep
        GUI responsive and interactive, a reference to this object is needed.


    """

    # Resample coordinate time series to magnetic field time line
    r_list = [resample(r_, b_) for r_, b_ in zip(r_list, b_list)]
    b_list_x = [b_[:, comp] for b_ in b_list]

    timing_gui_callback = TimingGui(b_list_x, r_list)

    return timing_gui_callback


class TimingGui:
    def __init__(self, b, r):
        # List of time series data
        self.b = b
        self.r = r

        # Output quantities - to be calculated
        self.n = None
        self.m = None
        self.V = None

        # Figures and GUI
        self.fig = self.init_fig(self.b)
        self.index = 0
        self.timing_started = False

        self.calc_button = Button(
            self.fig.axes[4], "Calculate normal", color="0.85", hovercolor="0.65"
        )
        self.calc_button.on_clicked(self.calc_vel_button)

        self.timing_button = Button(
            self.fig.axes[3], "Begin timing", color="0.85", hovercolor="0.65"
        )
        self.timing_button.on_clicked(self.begin_timing)

        plt.connect("button_press_event", self.onclick)

    @staticmethod
    def init_fig(b_list):
        b1, b2, b3, b4 = b_list

        fig = plt.figure(figsize=(16, 9))
        legend_options = dict(
            ncol=1,
            loc="center left",
            frameon=True,
            framealpha=1,
            bbox_to_anchor=(1, 0.5),
        )

        gs = gridspec.GridSpec(
            3, 5, bottom=0.05, top=0.9, left=0.05, right=0.9, hspace=0.4, wspace=0.35
        )
        # Time series data
        ax1 = fig.add_subplot(gs[0, :])

        # MVA transformed frame
        fig.add_subplot(gs[1, :])

        # Min/Max hodogram
        ax3 = fig.add_subplot(gs[2, :3])
        fig.add_subplot(gs[2, 3:4])
        fig.add_subplot(gs[2, 4:])

        ax1.xaxis.set_major_locator(dates.AutoDateLocator(minticks=30, maxticks=50))
        ax3.axis("off")

        # Plot
        plot_line(ax1, b1, color="black")
        plot_line(ax1, b2)
        plot_line(ax1, b3)
        plot_line(ax1, b4)
        b_labels = ["sc1", "sc2", "sc3", "sc4"]
        ax1.legend(b_labels, **legend_options)

        return fig

    def display_text(self, m, n, v):
        ax3 = self.fig.axes[2]
        for txt in ax3.texts:
            txt.set_visible(False)
        fontsize = 20
        ax3.text(0, 1, f"V [km/s]: {np.round(v ,3)}", fontsize=fontsize, va="top")
        ax3.text(0, 0.5, f"m [s/km]: {np.round(m ,3)}", fontsize=fontsize, va="center")
        ax3.text(0, 0, f"n: {np.round(n ,3)}", fontsize=fontsize, va="bottom")

        self.fig.canvas.draw_idle()

    def begin_timing(self, event):
        # Called if button pressed
        for line in self.fig.axes[1].get_lines():
            line.remove()

        self.timing_started = True
        self.time_list = np.zeros(4)
        self.index = 0
        self.update_selection()
        self.fig.canvas.draw_idle()

    def onclick(self, event):
        # Add time click to list if
        if self.timing_started and event.inaxes == self.fig.axes[0]:
            self.store_t(event)

        # Undo last time click if right mouse button clicked
        elif (
            not self.timing_started
            and event.inaxes == self.fig.axes[0]
            and event.button is MouseButton.RIGHT
        ):
            for line in self.fig.axes[0].lines[4:]:
                line.remove()
            self.fig.axes[0].axvline(
                event.xdata, -1, 1, linestyle="--", linewidth=2, color="black"
            )
            self.fig.canvas.draw_idle()

    def store_t(self, event):
        if event.button is MouseButton.LEFT and event.inaxes == self.fig.axes[0]:
            t_click = event.xdata
            # print("Matplot time: ",t_click)

            if self.index < 4:
                self.time_list[self.index] = t_click
                self.index += 1

            elif self.index >= 4:
                print("Time list full!")

        if event.button is MouseButton.RIGHT and event.inaxes == self.fig.axes[0]:
            if self.index < 1:
                print("List already empty")
            else:
                self.index -= 1
                self.time_list[self.index] = 0

        self.update_selection()

    def update_selection(self):
        """
        Highlight one line at a time untill all four have been clicked and
        the shifted signals are plotted by calling self.plot_shifted.

        """
        current = self.index
        lines = self.fig.axes[0].lines
        if current == 4:
            for line in lines[:4]:
                line.set_alpha(1)
            self.plot_shifted(self.time_list)
            self.timing_started = False

        else:
            for line in lines[:4]:
                line.set_alpha(0.2)
            lines[current].set_alpha(1)

        self.fig.canvas.draw_idle()

    def plot_shifted(self, time_list):
        # Shift time series relative sc1 (t0) and plot it in the second panel

        t0 = np.datetime64(dates.num2date(time_list[0]))
        time_difs = [(t0 - np.datetime64(dates.num2date(t))) for t in time_list]
        # Plot shifted
        legend_options = dict(
            ncol=1,
            loc="center left",
            frameon=True,
            framealpha=1,
            bbox_to_anchor=(1, 0.5),
        )
        ax2 = self.fig.axes[1]
        colors = ["black", "blue", "green", "red"]
        for i, b_ in enumerate(self.b):
            b_shifted = b_.assign_coords(time=b_.time.data + time_difs[i])
            plot_line(ax2, b_shifted, color=colors[i], alpha=1)

        b_labels = ["sc1", "sc2", "sc3", "sc4"]

        ax2.legend(b_labels, **legend_options)

    def calc_vel_button(self, event):
        if self.index < 4:
            raise TypeError(f"Not enough times in time list, {self.index} out of 4")

        else:
            # Convert clicked locations to list of np.datetime64 values
            time_list64 = [(np.datetime64(dates.num2date(t))) for t in self.time_list]

            # Calculate time differences and covert to seconds
            tau = [(t - time_list64[0]).astype("float") * 1e-6 for t in time_list64]

            # Assign copy of list of position time series to new variable
            r_list = self.r.copy()

            # Time of first click
            t = iso86012unix([time_list64[0]])

            # Get disc velocity at time of first click
            m, n, v = _get_disc_vel(t, tau, r_list)

            # Set class variables to access from timing_gui object
            self.m, self.n, self.V = m, n, v

            # Display results in GUI window
            self.display_text(m, n, v)

            # Print to console
            _print_output(tau, m, n, v, "Clicking")

    def get_slowness(self):
        if self.m is None:
            raise Exception("Slowness vector has not been calculated yet")
        else:
            return self.m

    def get_normal(self):
        if self.n is None:
            raise Exception("Normal has not been calculated yet")
        else:
            return self.n

    def get_vel(self):
        if self.V is None:
            raise Exception("Velocity has not been calculated yet")
        else:
            return self.V
