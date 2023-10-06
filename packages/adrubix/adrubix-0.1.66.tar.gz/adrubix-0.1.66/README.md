[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/complex)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
[![push-pypi](https://github.com/Advestis/adrubix/actions/workflows/push-pypi.yml/badge.svg)](https://github.com/Advestis/adrubix/actions/workflows/push-pypi.yml)
[![push-doc](https://github.com/Advestis/adrubix/actions/workflows/push-doc.yml/badge.svg)](https://github.com/Advestis/adrubix/actions/workflows/push-doc.yml)


![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
[![issues](https://img.shields.io/github/issues/Advestis/adrubix.svg)](https://github.com/Advestis/adrubix/issues)
[![pr](https://img.shields.io/github/issues-pr/Advestis/adrubix.svg)](https://github.com/Advestis/adrubix/pulls)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/adrubix)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:afedorov@advestis.com)


## AdRubix

Package allowing to create **RubixHeatmap** objects for plotting complex, highly customizable heatmaps with metadata.

The interest of such a visualization is to highlight clusters in data and to track any patterns vis-à-vis metadata.

&#9658; _You can easily test AdRubix tool on your data with this [friendly Streamlit GUI](https://adrubix.streamlit.app/)
before integrating it into your projects code-wise._

Example of a heatmap created using AdRubix:

![<img src="https://i.ibb.co/yVyGBbR/Ad-Rubix-advanced-JMP-sep.png" width="700">](https://i.ibb.co/yVyGBbR/Ad-Rubix-advanced-JMP-sep.png)


### Input

Three input files (CSV) or pandas DataFrames (in any combination) are expected:

- **Main data**
  
   Generally comes clusterized: for example, by applying [AdNMTF](https://pypi.org/project/adnmtf/) to raw data.
  
  - _Example A (see figure above) : rows = genes, columns = cell groups for each patient_
  - _Example B : rows = biomarkers at different timepoints, columns = patients_


- **Metadata for rows**

  Index of these metadata should correspond to the **index** of main data
  (at least partially, in which case the plot will only keep the matching rows).

  - _Example A : column 1 = gene group, column 2 = gene_
  - _Example B : column 1 = timepoint, column 2 = biomarker_


- **Metadata for columns**

  Index of these metadata should correspond to the **columns** of main data
  (at least partially, in which case the plot will only keep the matching columns).

  - _Example A : column 1 = patient, column 2 = cell type_
  - _Example B : column 1 = score (Y/N), column 2 = treatment, column 3 = cluster_


The resulting plot layout is composed of the following elements, all rendered using `holoviews.HeatMap()`
and fine-tuned via Bokeh plot parameters :

```
####  [CA]  ####

[RA]  [MP]  [RL]

####  [CL]  ####
```

- `[MP]` _main plot_ (with colorbar on the right)
- `[RA]` _row annotations_ (from metadata for rows)
- `[CA]` _column annotations_ (from metadata for columns) : can be duplicated under the main plot for long DFs
- `[RL]` _row legend_ (RA explained) : optional
- `[CL]` _column legend_ (CA explained) : optional
- `####` white space filler


### Output

`plot()` method of the class will save :
- **HTML plot** with an interactive toolbar enabling zooming into main heatmap and metadata
- **PNG image** corresponding to the HTML plot (without toolbar) : if `save_png` evaluates to True

With `plot_save_path` specified, HTML and PNG are saved according to it,
otherwise, HTML only is saved in current working directory to be able to show the plot.


### HTML toolbar

![toolbar](https://i.ibb.co/QKc2662/rubix-heatmap-toolbar.png)

The image above gives an example of toolbar for **AdRubix** HTML plot.
It comprises the following Bokeh tools, top to bottom:

* **Box Zoom** (activated by default) : drag & drop to select a rectangular area for zooming in
* **Pan** : drag to move a zoomed-in image around
* **Wheel Zoom** : zoom in or out with your mouse wheel
* **Reset** to the initial view (after any combination of zoom and pan)
* **Crosshairs** from mouse location (activated by default)

You can activate/deactivate any zoom, pan or crosshairs tool by clicking on it.

**WARNING.** When using `row_labels_for_highlighting` parameter, zoom can only work linked between
main data and column annotations. With `row_labels_for_highlighting=None`, zoom is always linked between main data
and both row and column annotations.

### Requirements for saving PNG

To be able to save plots as PNG files, ideally you should have :
* [Firefox web browser](https://www.mozilla.org/en-US/firefox/new/) and [geckodriver](https://github.com/mozilla/geckodriver/releases) installed on your machine
* Folders with the executables of Firefox and geckodriver added to your system PATH environment variable
  - [Adding new locations to system PATH on a Windows machine](https://www.howtogeek.com/118594/how-to-edit-your-system-path-for-easy-command-line-access/)
  - [Adding new locations to system PATH on a Linux machine](https://www.computerhope.com/issues/ch001647.htm)


### Main parameters

Default values are bolded, where applicable.

1. **Data input and plot output**
   - `data` (DF) or `data_file` (CSV file name)
   - `metadata_rows` (DF) or `metadata_rows_file` (CSV file name)
   - `metadata_cols` (DF) or `metadata_cols_file` (CSV file name)
   - `data_path` required if any of `[...]_file` parameters are used. **Do not forget a slash at the end of the path**.
     Also, _if you work on a Windows machine, be sure to use double backslashes `\\` instead of single slashes_.
   - [ optional ] `plot_save_path` = path to HTML file to be saved, **including its name**.
     If **None** is provided, HTML is saved in current working directory
     under the name `<your_python_script_name>.html` and automatically opened in a web browser.
   - [ optional ] `save_png` = True/**False** or 1/0. PNG image will be saved in the same folder as HTML
     under the same name except for the extension .png


2. **Data scaling and normalization + Dataprep**

   **NB.** It is still preferred that you do data scaling and/or normalization externally before using `RubixHeatmap`
   in order to have more control and transparency over your data.

   **NB.** If you go for it, for one axis you must choose between `scale_along` and `normalize_along`.
   You cannot use both simultaneously along the same axis.

   - [ optional ] `color_scaling_quantile` = quantile for getting rid of outliers (in %), default **95**,
     accepted 80...100. Applied both to `scale_along` and `normalize_along` options.
     - When applied to `scale_along`, `color_scaling_quantile=95` will cap top (> 95% quantile) values.
     - When applied to `normalize_along`, `color_scaling_quantile=95` will cap both top (> 97.5% quantile)
       and bottom (<2.5% quantile) values before normalizing data (see below).
   - [ optional ] `scale_along` = "columns"/"rows" or 0/1 for scaling and capping data along the specified axis.
     Default : **None** = do nothing.
   - [ optional ] `normalize_along` = "columns"/"rows" or 0/1 for scaling and capping + normalizing data
     along the specified axis : `(x - median(x) by column or row) / MAD(x) by column or row`,
     where `MAD` is median average deviation. Default : **None** = do nothing.
   - [ optional ] `data_rows_to_drop`, `data_cols_to_drop` = lists of the names of rows/columns in main data not intended
     to be plotted. Nonexistent names will be skipped without raising an error.


3. **Colorbar**
   - [ optional ] `colorbar_title` (**no title** by default)
   - [ optional ] `colorbar_height`, `colorbar_location` = "top"/"center"/"**bottom**"
     (always to the right of the main plot)
   - [ optional ] `show_colorbar` = **True**/False


4. **Metadata**
   - [ optional ] `show_metadata_rows` = **True**/False
   - [ optional ] `show_metadata_rows_labels` = True/**False**
     (font size is adapted to main dataframe length and to heatmap height, between 5pt and 10pt)
   - [ optional ] `show_metadata_cols` = **True**/False
   - [ optional ] `duplicate_metadata_cols` = True/False/**None**
     (if None, set automatically to True for DFs longer that 70 rows)


5. **Legends**
   - [ optional ] `show_rows_legend` = **True**/False
   - [ optional ] `show_cols_legend` = **True**/False


6. **Plot dimensions** (in terms of the main heatmap)
   - [ optional ] `heatmap_width`, `heatmap_height` : either sizes in pixels, or one size and the other "proportional".
     If neither is specified, plot dimensions will be proportional to the DF size (6 screen pixels per row or column).


7. **Colormaps** (must be known by **holoviews**)

   **NB.** A _separator_ is a row or column or a group of rows or columns (depending on the DF size and heatmap size)
    inserted in the main dataframe to be plotted in a specified color in order to visually separate meaningful blocks
    of data.

   - [ optional ] `colormap_main` (default "**coolwarm**" / "**YlOrRd**" for non-negative data)
   - [ optional ] `colormap_metarows` (default "**Glasbey**")
   - [ optional ] `colormap_metacols` (default "**Category20**")
   - [ optional ] `nan_color` (default "**black**") = hex color string "#xxxxxx" or named HTML color
     for filling NaN values in the main heatmap
   - [ optional ] `sep_color` (default "**white**") = hex color string "#xxxxxx" or named HTML color
     for filling separators in the main heatmap
   - [ optional ] `sep_value` = **None** / "min" / "median" / "adapt"
     = plot separators filled with `sep_color` / with color corresponding to the mininum value of the DF /
     with color corresponding to the median value of the DF, respectively. "adapt" will try to choose between
     "min" and "median", depending on data range and normalization.


8. **Plot enhancement**
   - [ optional ] `metadata_rows_sep` = insert row separators in the main DF and the metadata-rows DF
     before plotting, according to the specified column (between groups of labels with identical values).
   - [ optional ] `metadata_cols_sep` = insert column separators in the main DF and the metadata-cols DF
     before plotting, according to the specified rows (between groups of labels with identical values).
   - [ optional ] `row_labels_for_highlighting` = list of keywords for identifying row labels to be highlighted
     (in red and italic to the right of the heatmap). See WARNING in **Toolbar** section.


### Example of usage

```python
from adrubix import RubixHeatmap
import pandas as pd

main_data = pd.DataFrame(index=[...], columns=[...], data=[...])

hm = RubixHeatmap(
    data_path="/home/user/myproject/data/",
    data=main_data,
    metadata_rows_file="meta_rows.csv",
    metadata_cols_file="meta_cols.csv",
    plot_save_path="/home/user/myproject/output/plot.html",
    save_png=True,
    scale_along="columns",
    colorbar_title="my colorbar",
    colorbar_location="top",
    show_metadata_rows_labels=True,
    show_rows_legend=False,
    # duplicate_metadata_cols=False,
    colormap_main="fire",
    heatmap_width=1500,
    heatmap_height="proportional",
    data_rows_to_drop=["useless_row_1", "useless_row_2"],
    row_labels_for_highlighting=["row_keyword_A", "row_keyword_B"],
    metadata_rows_sep="Group",
    metadata_cols_sep="Subject",
    nan_color="orange",
    sep_color="green",
    # sep_value="median"
)
hm.plot()
```