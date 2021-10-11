import os, sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("../../atlastk")

import atlastk

import matplotlib.pyplot as plt
from io import StringIO
from mpl_toolkits.mplot3d import axes3d
import numpy as np
from cycler import cycler
import matplotlib as mpl
import matplotlib.tri as tri
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import collections, colors, transforms
# plt.xkcd()  # XKCD-like ploting.

BODY = """
<iframe style="border: none;" src="FaaSDesc.php?text=R3JhcGhpY3MgZHJhd24gd2l0aCBbKm1hdHBsb3RsaWIqXShodHRwczovL21hdHBsb3RsaWIub3JnLykgY2FuIGJlIHVzZWQgd2l0aCB0aGUgKkF0bGFzKiAqVG9vbGtpdCou"></iframe>
<fieldset id="Plots"></fieldset>
<fieldset id="Buttons"></fieldset>
<fieldset>
 <span>Due to a limitation of <a href="https://en.wikipedia.org/wiki/Matplotlib" target="_blank" style="font-style: oblique;">matplotlib</a>, opening </span>
 <br/>
 <span>more then one session with this application</span>
 <br/>
 <span>may probably lead to a crash.</span>
</fieldset>
"""

HEAD = """
<title>MatPlotLib with the Atlas Toolkit</title>
<style>
  fieldset {margin: auto; text-align: center;}
  #Buttons {display: none;}
</style>
<style id="Ready">
 .hide {display: none;}
  #Buttons {display: block;}
</style>
"""

AMOUNT = 10

def getSVG(plt):
  figfile = StringIO()
  plt.savefig(figfile, format='svg')

  svg = figfile.getvalue();

  plt.close()

  return svg

def run(example):
  return eval(f"example{example}()")

def example1():
  labels = ['G1', 'G2', 'G3', 'G4', 'G5']
  men_means = [20, 34, 30, 35, 27]
  women_means = [25, 32, 34, 20, 25]

  x = np.arange(len(labels))  # the label locations
  width = 0.35  # the width of the bars

  fig, ax = plt.subplots()
  rects1 = ax.bar(x - width/2, men_means, width, label='Men')
  rects2 = ax.bar(x + width/2, women_means, width, label='Women')

  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel('Scores')
  ax.set_title('Scores by group and gender')
  ax.set_xticks(x)
  ax.set_xticklabels(labels)
  ax.legend()


  def autolabel(rects):
      """Attach a text label above each bar in *rects*, displaying its height."""
      for rect in rects:
          height = rect.get_height()
          ax.annotate('{}'.format(height),
                      xy=(rect.get_x() + rect.get_width() / 2, height),
                      xytext=(0, 3),  # 3 points vertical offset
                      textcoords="offset points",
                      ha='center', va='bottom')


  autolabel(rects1)
  autolabel(rects2)

  fig.tight_layout()

  return getSVG(plt)

def example2():
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  # Grab some test data.
  X, Y, Z = axes3d.get_test_data(0.05)

  # Plot a basic wireframe.
  ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10) 

  return getSVG(plt)


def example3():
 # prepare some coordinates
  x, y, z = np.indices((8, 8, 8))

  # draw cuboids in the top left and bottom right corners, and a link between them
  cube1 = (x < 3) & (y < 3) & (z < 3)
  cube2 = (x >= 5) & (y >= 5) & (z >= 5)
  link = abs(x - y) + abs(y - z) + abs(z - x) <= 2

  # combine the objects into a single boolean array
  voxels = cube1 | cube2 | link

  # set the colors of each object
  colors = np.empty(voxels.shape, dtype=object)
  colors[link] = 'red'
  colors[cube1] = 'blue'
  colors[cube2] = 'green'

  # and plot everything
  fig = plt.figure()
  ax = fig.gca(projection='3d')
  ax.voxels(voxels, facecolors=colors, edgecolor='k')

  return getSVG(plt)

def example4():
  fig = plt.figure()
  ax = fig.gca(projection='3d')

  X, Y = np.mgrid[0:6*np.pi:0.25, 0:4*np.pi:0.25]
  Z = np.sqrt(np.abs(np.cos(X) + np.cos(Y)))

  ax.plot_surface(X + 1e5, Y + 1e5, Z, cmap='autumn', cstride=2, rstride=2)

  ax.set_xlabel("X label")
  ax.set_ylabel("Y label")
  ax.set_zlabel("Z label")
  ax.set_zlim(0, 2)

  return getSVG(plt)

def example5():
  category_names = ['Strongly disagree', 'Disagree',
                    'Neither agree nor disagree', 'Agree', 'Strongly agree']
  results = {
      'Question 1': [10, 15, 17, 32, 26],
      'Question 2': [26, 22, 29, 10, 13],
      'Question 3': [35, 37, 7, 2, 19],
      'Question 4': [32, 11, 9, 15, 33],
      'Question 5': [21, 29, 5, 5, 40],
      'Question 6': [8, 19, 5, 30, 38]
  }


  def survey(results, category_names):
      """
      Parameters
      ----------
      results : dict
          A mapping from question labels to a list of answers per category.
          It is assumed all lists contain the same number of entries and that
          it matches the length of *category_names*.
      category_names : list of str
          The category labels.
      """
      labels = list(results.keys())
      data = np.array(list(results.values()))
      data_cum = data.cumsum(axis=1)
      category_colors = plt.get_cmap('RdYlGn')(
          np.linspace(0.15, 0.85, data.shape[1]))

      fig, ax = plt.subplots(figsize=(9.2, 5))
      ax.invert_yaxis()
      ax.xaxis.set_visible(False)
      ax.set_xlim(0, np.sum(data, axis=1).max())

      for i, (colname, color) in enumerate(zip(category_names, category_colors)):
          widths = data[:, i]
          starts = data_cum[:, i] - widths
          ax.barh(labels, widths, left=starts, height=0.5,
                  label=colname, color=color)
          xcenters = starts + widths / 2

          r, g, b, _ = color
          text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
          for y, (x, c) in enumerate(zip(xcenters, widths)):
              ax.text(x, y, str(int(c)), ha='center', va='center',
                      color=text_color)
      ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='small')

      return fig, ax


  survey(results, category_names)

  return getSVG(plt)

def example6():
  # Define a list of markevery cases and color cases to plot
  cases = [None,
          8,
          (30, 8),
          [16, 24, 30],
          [0, -1],
          slice(100, 200, 3),
          0.1,
          0.3,
          1.5,
          (0.0, 0.1),
          (0.45, 0.1)]

  colors = ['#1f77b4',
            '#ff7f0e',
            '#2ca02c',
            '#d62728',
            '#9467bd',
            '#8c564b',
            '#e377c2',
            '#7f7f7f',
            '#bcbd22',
            '#17becf',
            '#1a55FF']

  # Configure rcParams axes.prop_cycle to simultaneously cycle cases and colors.
  mpl.rcParams['axes.prop_cycle'] = cycler(markevery=cases, color=colors)

  # Create data points and offsets
  x = np.linspace(0, 2 * np.pi)
  offsets = np.linspace(0, 2 * np.pi, 11, endpoint=False)
  yy = np.transpose([np.sin(x + phi) for phi in offsets])

  # Set the plot curve with markers and a title
  fig = plt.figure()
  ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])

  for i in range(len(cases)):
      ax.plot(yy[:, i], marker='o', label=str(cases[i]))
      ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

  plt.title('Support for axes.prop_cycle cycler with markevery')  

  return getSVG(plt)

def example7():
  #-----------------------------------------------------------------------------
  # Analytical test function
  #-----------------------------------------------------------------------------
  def function_z(x, y):
      r1 = np.sqrt((0.5 - x)**2 + (0.5 - y)**2)
      theta1 = np.arctan2(0.5 - x, 0.5 - y)
      r2 = np.sqrt((-x - 0.2)**2 + (-y - 0.2)**2)
      theta2 = np.arctan2(-x - 0.2, -y - 0.2)
      z = -(2 * (np.exp((r1 / 10)**2) - 1) * 30. * np.cos(7. * theta1) +
            (np.exp((r2 / 10)**2) - 1) * 30. * np.cos(11. * theta2) +
            0.7 * (x**2 + y**2))
      return (np.max(z) - z) / (np.max(z) - np.min(z))

  #-----------------------------------------------------------------------------
  # Creating a Triangulation
  #-----------------------------------------------------------------------------
  # First create the x and y coordinates of the points.
  n_angles = 20
  n_radii = 10
  min_radius = 0.15
  radii = np.linspace(min_radius, 0.95, n_radii)

  angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
  angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
  angles[:, 1::2] += np.pi / n_angles

  x = (radii * np.cos(angles)).flatten()
  y = (radii * np.sin(angles)).flatten()
  z = function_z(x, y)

  # Now create the Triangulation.
  # (Creating a Triangulation without specifying the triangles results in the
  # Delaunay triangulation of the points.)
  triang = tri.Triangulation(x, y)

  # Mask off unwanted triangles.
  triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                          y[triang.triangles].mean(axis=1))
                  < min_radius)

  #-----------------------------------------------------------------------------
  # Refine data
  #-----------------------------------------------------------------------------
  refiner = tri.UniformTriRefiner(triang)
  tri_refi, z_test_refi = refiner.refine_field(z, subdiv=3)

  #-----------------------------------------------------------------------------
  # Plot the triangulation and the high-res iso-contours
  #-----------------------------------------------------------------------------
  fig, ax = plt.subplots()
  ax.set_aspect('equal')
  ax.triplot(triang, lw=0.5, color='white')

  levels = np.arange(0., 1., 0.025)
  cmap = cm.get_cmap(name='terrain', lut=None)
  ax.tricontourf(tri_refi, z_test_refi, levels=levels, cmap=cmap)
  ax.tricontour(tri_refi, z_test_refi, levels=levels,
                colors=['0.25', '0.5', '0.5', '0.5', '0.5'],
                linewidths=[1.0, 0.5, 0.5, 0.5, 0.5])

  ax.set_title("High-resolution tricontouring")

  return getSVG(plt)

def example8():
  fig, axs = plt.subplots(2, 2)
  cm = ['RdBu_r', 'viridis']
  for col in range(2):
      for row in range(2):
          ax = axs[row, col]
          pcm = ax.pcolormesh(np.random.random((20, 20)) * (col + 1),
                              cmap=cm[col])
          fig.colorbar(pcm, ax=ax)

  return getSVG(plt)          

def example9():
  # Fixing random state for reproducibility
  np.random.seed(19680801)

  n = 100000
  x = np.random.standard_normal(n)
  y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
  xmin = x.min()
  xmax = x.max()
  ymin = y.min()
  ymax = y.max()

  fig, axs = plt.subplots(ncols=2, sharey=True, figsize=(7, 4))
  fig.subplots_adjust(hspace=0.5, left=0.07, right=0.93)
  ax = axs[0]
  hb = ax.hexbin(x, y, gridsize=50, cmap='inferno')
  ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
  ax.set_title("Hexagon binning")
  cb = fig.colorbar(hb, ax=ax)
  cb.set_label('counts')

  ax = axs[1]
  hb = ax.hexbin(x, y, gridsize=50, bins='log', cmap='inferno')
  ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
  ax.set_title("With a log color scale")
  cb = fig.colorbar(hb, ax=ax)
  cb.set_label('log10(N)')

  return getSVG(plt) 

def example10():
  X = np.arange(-5, 5, 0.25)
  Y = np.arange(-5, 5, 0.25)
  X, Y = np.meshgrid(X, Y)
  R = np.sqrt(X**2 + Y**2)
  Z = np.sin(R)

  fig = plt.figure()
  ax = Axes3D(fig)
  ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.viridis)

  return getSVG(plt)


def ac_connect(dom):
  dom.inner("", BODY)
  dom.disable_element("Ready")

  for example in range(1,AMOUNT+1):
    dom.end("Plots", f'<fieldset class="hide" id="example{example}">Please wait ({example}/{AMOUNT})…</fieldset>')
    dom.inner(f"example{example}", f"<legend>Example {example}</legend>{run(example)}")
    dom.flush()
    dom.scroll_to(f'example{example}')
    dom.end("Buttons",f'<button id="{example}" xdh:onevent="Display">{example}</button>')

  dom.enable_element("Ready")
  dom.remove_class(f"example1", "hide")

def ac_display(dom,id):
  dom.add_classes(_hiding)
  dom.remove_class(f"example{id}","hide")


_hiding = {}

for i in range(1, AMOUNT+1):
  _hiding[f"example{i}"] = "hide"

atlastk.launch({"": ac_connect, "Display": ac_display},None,HEAD)