import flet as ft
import pandas as pd
from matplotlib.colors import LogNorm
from matplotlib import pyplot as plt
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text,
    AlertDialog,
    
)
import matplotlib
matplotlib.use('agg')
from flet.matplotlib_chart import MatplotlibChart
plt.rcParams['font.family'] = 'Arial'

class PlotParameters:
    def __init__(self):
        self.width: int = 10
        self.height: int = 5
        self.count: int = 25
        self.plotsize: int = 3
        self.vmax: float = 1e-2
        self.vmin: float = 1e-20
        self.fontsize: int = 10
        self.xmin: int = 2
        self.xmax: int = 12
        self.n: int = 3
        self.label_y_position: float = -0.13
        self.save: bool = False
        self.output_dir: str = ""

def generate_matplotlib_figure(go_data: str, params: PlotParameters) -> plt.Figure:
    try:
        txt = go_data.splitlines()
        txt = [s.split("\t") for s in txt]
        data = pd.DataFrame(txt[1:], columns=txt[0])
        h = data.iloc[0]
        data.columns = h
        data = data.drop(data.index[0])
        data = data.reset_index(drop=True)
        data.columns = ['GO term', 'REFLIST (27430)', "number_in_list",
                        "expected count", "(over/under)", "fold_enrichment", "pValue"]
        data = data[data["(over/under)"] == "+"].copy()
        data = data[data["GO term"] != "Unclassified (UNCLASSIFIED)"].copy()

        fig, ax = plt.subplots(figsize=(params.width, params.height))
        module_GO_top = data.sort_values(by='fold_enrichment', ascending=False).head(params.count)
        module_GO_top = module_GO_top.sort_values(by='fold_enrichment', ascending=True)
        y = module_GO_top['GO term']
        x = module_GO_top['fold_enrichment'].astype(float)
        c = module_GO_top['pValue'].astype(float)
        size = module_GO_top['number_in_list'].astype(int)

        ax.scatter(x, y, c=c, s=size * params.plotsize, linewidths=0.5, edgecolors='black', cmap='Spectral',
                    norm=LogNorm(vmax=params.vmax, vmin=params.vmin))

        ax.set_xlabel('Fold enrichment', fontsize=params.fontsize)
        ax.set_ylabel('GO term', fontsize=params.fontsize)
        ax.set_xlim(params.xmin, params.xmax)
        ax.tick_params(axis='x', labelsize=params.fontsize)
        ax.tick_params(axis='y', labelsize=params.fontsize)

        colorbar = plt.colorbar(ax.collections[0], ax=ax)
        colorbar.set_label(label=r'$P$ value', rotation=-90, labelpad=15, fontsize=params.fontsize)
        colorbar.ax.tick_params(labelsize=params.fontsize)

        for i in range(1, params.n + 1):
            size_i = size.max() * params.plotsize * i / params.n
            label = round(size.max() * i / params.n)
            ax.scatter([], [], c='k', s=size_i, label=label)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, params.label_y_position),
                   frameon=False, ncol=6, title='Gene count', fontsize=params.fontsize, title_fontsize=params.fontsize)

        fig.tight_layout(pad=2)
        if params.save:
            fig.savefig(f"{params.output_dir}/GOgraph.png", dpi=800, transparent=True)
        return fig

    except Exception as e:
        raise ValueError(f"Error generating plot: {e}")

def main(page: ft.Page):
    page.title = "GO Term Enrichment Visualizer"
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window_position = (0, 0)
    page.window.width = 1200  
    page.window.height = 600  

    plot_params = PlotParameters()
    output_container = ft.Container(expand=True)
    dir_picker = FilePicker()
    page.overlay.append(dir_picker)

    def select_output_dir(e):
        dir_picker.get_directory_path()
    
    def dir_picker_result(e: FilePickerResultEvent):
        if e.path:
            output_path = e.path
            output_path_text.value = output_path
        else:
            output_path_text.value = ""
        page.update()
   
    dir_picker.on_result = dir_picker_result
        
    save_var = False
    def save_changed(e):
        nonlocal save_var
        save_var = e.control.value

    def generate_plot(e):
        go_data = GO_result.value
        if not go_data:
            page.overlay.append(AlertDialog(title=Text(f"Error: no File"), open=True))
            page.update()
            return

        try:
            plot_params.width = int(width_input.value) if width_input.value else plot_params.width
            plot_params.height = int(height_input.value) if height_input.value else plot_params.height
            plot_params.count = int(count_input.value) if count_input.value else plot_params.count
            plot_params.plotsize = int(plotsize_input.value) if plotsize_input.value else plot_params.plotsize
            plot_params.vmax = float(vmax_input.value) if vmax_input.value else plot_params.vmax
            plot_params.vmin = float(vmin_input.value) if vmin_input.value else plot_params.vmin
            plot_params.fontsize = int(fontsize_input.value) if fontsize_input.value else plot_params.fontsize
            plot_params.xmin = int(xmin_input.value) if xmin_input.value else plot_params.xmin
            plot_params.xmax = int(xmax_input.value) if xmax_input.value else plot_params.xmax
            plot_params.n = int(n_input.value) if n_input.value else plot_params.n
            plot_params.label_y_position = float(label_y_position_input.value) if label_y_position_input.value else plot_params.label_y_position
            plot_params.save = save_var
            plot_params.output_dir = output_path_text.value if output_path_text.value else ""

            fig = generate_matplotlib_figure(go_data, plot_params)
            output_container.content = MatplotlibChart(fig, expand=True)
            page.update()
            plt.close(fig)
        except Exception as e:
            page.overlay.append(AlertDialog(title=Text(f"Error: {str(e)}"), open=True))
            page.update()

    GO_result = ft.TextField(label="GO result", multiline=True, min_lines=10, max_lines=10)
    width_input = ft.TextField(label="Width (inches)", value=str(plot_params.width))
    height_input = ft.TextField(label="Height (inches)", value=str(plot_params.height))
    count_input = ft.TextField(label="Top GO Terms", value=str(plot_params.count))
    plotsize_input = ft.TextField(label="Point Size Multiplier", value=str(plot_params.plotsize))
    vmax_input = ft.TextField(label="P-value Max (e.g., 1e-2)", value=str(plot_params.vmax))
    vmin_input = ft.TextField(label="P-value Min (e.g., 1e-20)", value=str(plot_params.vmin))
    fontsize_input = ft.TextField(label="Font Size", value=str(plot_params.fontsize))
    xmin_input = ft.TextField(label="X-axis Min", value=str(plot_params.xmin))
    xmax_input = ft.TextField(label="X-axis Max", value=str(plot_params.xmax))
    n_input = ft.TextField(label="Legend Entries", value=str(plot_params.n))
    label_y_position_input = ft.TextField(label="Legend Y Position", value=str(plot_params.label_y_position))
    output_folder = ft.ElevatedButton(text="Select output folder", on_click=select_output_dir)
    output_path_text = ft.TextField(label="Output Path", read_only=True, expand=True)
    save_button = ft.Checkbox(label="Save Plot", on_change=save_changed)
    plot_button = ft.ElevatedButton("Plot", on_click=generate_plot)

    input_area = ft.Column([
        GO_result,
        width_input,
        height_input,
        count_input,
        plotsize_input,
        vmax_input,
        vmin_input,
        fontsize_input,
        xmin_input,
        xmax_input,
        n_input,
        label_y_position_input,
        output_path_text,
        output_folder,
        save_button,
        plot_button,
    ], scroll=ft.ScrollMode.ADAPTIVE, tight=True)

    output_container.content = None

    page.add(
        ft.Row(
            [
                ft.Container(input_area, expand=False, width=400),
                output_container,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)