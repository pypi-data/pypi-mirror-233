from .plots import barplot, cluster_embedding, embedding_with_binding, hist_lvst_dist, length_distribution, \
    logo_plot, plt_heatmap, relative_sequence_abundance, stacked_aa_distribution, usq_plot, levenshtein_clustering
import matplotlib.pyplot as plt
from .augment_data.binding_data import collect_binding_data
from .augment_data.uploader import upload
from ast import literal_eval
import pandas as pd
import pickle
import os
from ExpoSeq.augment_data.randomizer import create_sequencing_report, create_binding_report
from .design.multi_seq_align import MSA
from ExpoSeq.settings import change_settings, change_save_settings, reports, plot_styler
from tkinter import filedialog
import subprocess
import glob
from ExpoSeq.augment_data.uploader import create_alignment_report

class MyFigure:
    def __init__(self):
        self.fig = plt.figure(1)
        self.ax = self.fig.gca()
        self.plot_type = "multi"

    def check_fig(self, ):
        if not plt.fignum_exists(1):
            self.fig = plt.figure(1)

    def clear_fig(self):
        self.fig.clear()
        if self.plot_type == "single":
            self.ax = self.fig.gca()

    def update_plot(self):
        self.ax = self.fig.gca()
        self.style = plot_styler.PlotStyle(self.ax, self.plot_type)
       # figManager = plt.get_current_fig_manager()
      #  figManager.window.showMaximized()
        self.tighten()

    def tighten(self):
        plt.tight_layout()


def save_matrix(matrix):
    while True:
        save_matrix = input("Do you want to save the generated data? (Y/n)")
        if save_matrix in ["Y", "y", "N", "n"]:
            break
        else:
            print("Please enter Y or n")
    if save_matrix.lower() in ["Y", "y"]:
        while True:
            filename_matrix = input("Enter a name for the file. The file will be saved locally in your IDE.")
            if not os.path.isfile(filename_matrix):
                break
            else:
                print("This file already exists. Please choose another name.")

        matrix.to_excel(filename_matrix + ".xlsx")


class Directories:
    def __init__(self):
        self.module_dir = os.path.abspath("")
        self.common_vars = os.path.join(self.module_dir, "settings", "global_vars.txt")
        self.font_settings_path = os.path.join(self.module_dir, "settings", "font_settings.txt")
        self.legend_settings_path = os.path.join(self.module_dir,
                                                 "settings",
                                                 "legend_settings.txt")
        self.colorbar_path = os.path.join(self.module_dir,
                                          "settings",
                                          "colorbar.txt")

    def check_dirs(self):
        if not os.path.isdir(os.path.join(self.module_dir, "my_experiments")):
            print("create my_experiments directory")
            os.mkdir(os.path.join(self.module_dir, "my_experiments"))
        if not os.path.isdir(os.path.join(self.module_dir, "temp")):
            print("create temp directory")
            os.mkdir(os.path.join(self.module_dir, "temp"))
        if not os.path.isdir(os.path.join(self.module_dir, "settings")):
            print("create settings directory")
            os.mkdir(os.path.join(self.module_dir, "settings"))

    def create_global_params(self):
        common_vars = {'mixcr_path': '', 'last_experiment': '', 'api_gpt3': '', 'region_of_interest': '', 'RAM': '',
                       'clustalw_path': ''}
        with open(self.common_vars, "w") as f:
            f.write(str(common_vars))

    def create_font_settings(self):
        font_settings = {'fontfamily': 'serif', 'fontsize': '18', 'fontstyle': 'normal', 'fontweight': 'bold'}
        with open(os.path.join(self.module_dir, "settings", "font_settings.txt"), "w") as f:
            f.write(str(font_settings))

    def create_legend_settings(self):
        legend_settings = {'loc': 'upper right', 'bbox_to_anchor': (1, 1), 'ncols': 1, 'fontsize': 16, 'frameon': True,
                           'framealpha': 1, 'facecolor': 'white', 'mode': None, 'title_fontsize': 'small'}
        with open(os.path.join(self.module_dir, "settings", "legend_settings.txt"), "w") as f:
            f.write(str(legend_settings))

    def create_colorbar_settings(self):
        colorbar = {'cmap': 'inferno', 'orientation': 'vertical', 'spacing': 'proportional', 'extend': 'neither'}
        with open(self.colorbar_path, "w") as f:
            f.write(str(colorbar))

    def read_global_params(self):
        if not os.path.isfile(self.common_vars):
            self.create_global_params()
        with open(self.common_vars, "r") as f:
            global_params = f.read()
        global_params = literal_eval(global_params)
        return global_params

    def read_font_settings(self):
        if not os.path.isfile(self.font_settings_path):
            self.create_font_settings()
        with open(self.font_settings_path, "r") as f:
            font_settings = f.read()
        font_settings = literal_eval(font_settings)
        return font_settings

    def read_legend_settings(self):
        if not os.path.isfile(self.legend_settings_path):
            self.create_legend_settings()
        with open(self.legend_settings_path, "r") as f:
            legend_settings = f.read()
        legend_settings = literal_eval(legend_settings)
        return legend_settings

    def read_colorbar_settings(self):
        if not os.path.isfile(self.colorbar_path):
            self.create_colorbar_settings()
        with open(self.colorbar_path, "r") as f:
            colorbar_settings = f.read()
        colorbar_settings = literal_eval(colorbar_settings)
        return colorbar_settings

    def get_experiment_path(self, experiment):
        experiment_path = os.path.join(self.module_dir,
                                       "my_experiments",
                                       experiment,
                                       "experiment_names.pickle")
        return experiment_path


def print_instructions():
    instructions = '''

-----------------------
General Instructions
-----------------------
All plots can be called with 'plot' followed by the name of the plot, separated by a dot.
To analyze a specific sample or investigate possible options, use 'help()' and 'plot' followed by the name of the plot.

-----------------------
Plot Commands
-----------------------
- plot.alignment_quality(): 
    Creates a figure showing the Overall Reads per sample and the number of aligned reads.

- plot.aa_distribution(): 
    Returns a plot showing the amino acid distribution in the given sequence range.

- plot.rarefraction_curves(): 
    Shows the rarefraction curves for the given samples.

- plot.logoPlot_single(): 
    A logo Plot showing the composition of amino acids per position.

- plot.logoPlot_multiple(): 
    A logo Plot showing the composition of amino acids per position for multiple samples.

- plot.lengthDistribution_single(): 
    Shows the length distribution of the given sample.

- plot.relative_abundance_multi(): 
    Shows the relative abundance of the given samples.

- plot.lengthDistribution_multi(): 
    Shows the length distribution of the given samples.

- plot.rel_seq_abundance(): 
    Shows a bar plot of the frequencies of the most abundant sequences with optional Levenshtein distance.

- plot.basic_cluster(): 
    Clusters a batch of sequences based on a threshold for the Levenshtein distance.

- plot.cluster_one_AG(): 
    Clusters sequences based on Levenshtein distance and shows binding data against a specific antigen.

- plot.tsne_cluster_AG(): 
    Embeds sequences in a vector space, reduces dimensions, and clusters them. Also plots binding data.

- plot.embedding_tsne(): 
    Transforms sequences into a vector space and uses PCA and t-SNE for dimensionality reduction.

- plot.morosita_horn(): 
    Returns a matrix of the identity between your samples based on the Morosita Horn Index.

- plot.jaccard(): 
    Returns a matrix of the identity between your samples based on the Jaccard Index.

- plot.sorensen(): 
    Returns a matrix of the identity between your samples based on the Sorensen Index.

- plot.relative(): 
    Returns a matrix of the identity between your samples based on the Relative Index.

- plot.levenshtein_dendrogram(): 
    Returns a dendrogram of the sequences based on the Levenshtein distance.

- plot.dendro_bind(): 
    Shows a dendrogram based on Levenshtein distance and a bar plot with binding data.

- plot.MSA_design(): 
    Creates a multiple sequence alignment and offers an interface for sequence design.

-----------------------
Non-Plot Commands
-----------------------
- plot.add_binding_data(): 
    Allows you to add more binding data to the pipeline.

- plot.change_preferred_antigen(): 
    Sets the antigen you'd like to analyze in the plots.

- plot.change_preferred_sample(): 
    Sets the sample you'd like to analyze in the plots.

- plot.change_preferred_region(): 
    Sets the region you'd like to analyze in the plots.

- plot.change_filter(): 
    Adjusts the thresholds for filtering sequences in your analysis.

- plot.discard_samples(): 
    Allows you to remove samples from the analysis.

- plot.merge_bind_seq_report(): 
    Merges binding data with NGS data.

- plot.print_antigens(): 
    Shows the available antigen names in your data.

- plot.print_samples(): 
    Shows the available samples in your data.

- plot.save(): 
    Allows you to save a plot.

- plot.change_experiment_names(): 
    Allows you to change the names of the samples.
'''
    print(instructions)


# Call the function to print the instructions

class PlotManager:
    def __init__(self,experiment = None, test_version=False, test_exp_num=3, test_panrou_num=1, divisible_by=3, length_threshold=9,
                 min_read_count=3):
        self.is_test = test_version
        self.Settings = change_settings.Settings()
        self.Settings.check_dirs()
        self.global_params = self.Settings.read_global_vars()


        self.module_dir = self.Settings.module_dir
        if test_version == True:
            self.experiment = "Test"
            self.sequencing_report = create_sequencing_report(num_experiments=test_exp_num,
                                                              panning_rounds=test_panrou_num,
                                                              )
            self.alignment_report = None
            self.binding_data = create_binding_report(self.sequencing_report,
                                                      num_antigen=test_panrou_num)
            self.region_string = "CDR3"
        else:
            if experiment == None:
                self.sequencing_report, self.alignment_report, self.experiment = upload()
            else:
                self.sequencing_report  = pd.read_csv(os.path.join(self.module_dir,
                                                                   "my_experiments",
                                                                   experiment,
                                                                   "sequencing_report.csv"))
                self.alignment_report = create_alignment_report(self.module_dir, experiment)
                self.experiment = experiment
            self.region_string = self.global_params["region_of_interest"]
            if self.region_string == '':
                self.region_string = "CDR3"
            binding_report = reports.BindingReport(self.module_dir,
                                                   self.experiment)
            self.binding_data = binding_report.ask_binding_data()
        self.Report = reports.SequencingReport(self.sequencing_report)
        experiment_path = self.Settings.get_experiment_path(self.experiment)
        self.unique_experiments = self.Report.get_exp_names(experiment_path)
        self.Report.prepare_seq_report(self.region_string,
                                       divisible_by=divisible_by,
                                       length_threshold=length_threshold,
                                       min_read_count=min_read_count)
        self.Report.map_exp_names(self.unique_experiments)
        self.avail_regions = self.Report.get_fragment()

        self.sequencing_report = self.Report.sequencing_report
        self.font_settings = self.Settings.read_font_settings()
        self.legend_settings = self.Settings.read_legend_settings()
        self.colorbar_settings = self.Settings.read_colorbar_settings()
        self.ControlFigure = MyFigure()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax, self.ControlFigure.plot_type)
        # self.settings_saver = change_save_settings.Change_save_settings()
        self.experiments_list = list(self.unique_experiments.values())
        self.region_of_interest = "aaSeq" + self.region_string
        self.preferred_sample = self.experiments_list[0]
        self.change_preferred_antigen()
        print_instructions()
        self.plot_path = os.path.join(self.module_dir, "my_experiments", self.experiment, "plots")
        if not os.path.isdir(self.plot_path):
            os.mkdir(self.plot_path)
            self.quality_analysis()


    def save_in_plots(self, enter_filename):
        plt.savefig(fname = os.path.join(self.plot_path, enter_filename + f".png"), dpi = 300,  format="png")

    def quality_analysis(self):
        """
        :return: returns some plots about quality in /my_experiments/YOUR_EXPERIMENT_NAME/plots. Is called automatically when launching the pipeline.
        """
        self.morosita_horn()
        plt.tight_layout()
        self.save_in_plots("morosita_horn")
        self.lengthDistribution_multi()
        plt.tight_layout()
        self.save_in_plots("length_distribution_multi")
        try:
            self.export_mixcr_quality()
            plt.tight_layout()
        except:
            print(f".clns files could not be found. Most certainly, you have uploaded the sequencing report.")
        try:
            self.alignment_quality()
            plt.tight_layout()
            self.save_in_plots("alignment_quality")
        except:
            print("Alignment reports could not be found")
        for i in self.experiments_list:
            self.rarefraction_curves(samples = [i])
            plt.tight_layout()
            self.save_in_plots("rarefraction_curves_"+i)
        self.relative_abundance_multi()
        plt.tight_layout()
        self.save_in_plots("relative_sequence_abundance_multi")
        self.logoPlot_multi()
        plt.tight_layout()
        self.save_in_plots("logo_plot_multi")
        print(f"The pipeline has created some plots to evaluate the quality of your sequencing in: {self.plot_path}")

    def change_preferred_antigen(self, antigen=None):
        if self.binding_data is not None:
            columns_bind_data = self.binding_data.columns.to_list()
            self.preferred_antigen = columns_bind_data[1]
        else:
            self.preferred_antigen = None

    def change_preferred_sample(self, sample):
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        self.preferred_sample = sample

    def change_filter(self, divisible_by=3, length_threshold=9, min_read_count=0):
        """
        :param divisible_by: filter all sequences which are not divisible by this value
        :param length_threshold: filter out all sequences which are shorter than this value
        :min_read_count: filter out all sequences which have less clones/reads than this value
        """
        self.Report.prepare_seq_report(self.region_string, divisible_by, length_threshold, min_read_count)
        self.sequencing_report = self.Report.sequencing_report

    def change_region(self):
        """
        :return: changes the region you want to analyse
        """
        intermediate = self.region_of_interest
        possible_regions = self.avail_regions + ["all"]
        region_string = input(
            f"Which region do you want to plot? ExpoSeq could find the following regions: {self.avail_regions}. If you want to merge your sequences and analyse the longest possible consecutive sequences your dataset offers type 'all'")
        if region_string in possible_regions:
            if not region_string == "all":
                region_string = region_string.replace("nSeq", "")
                self.Report.prepare_seq_report(region_string, divisible_by=3, length_threshold=9, min_read_count=0)
            else:
                self.Report.filter_longest_sequence()

            self.sequencing_report = self.Report.sequencing_report
            self.region_of_interest = "aaSeq" + region_string
        else:
            print(f"The region you want to plot is not valid. The options are: {self.avail_regions}")
            self.region_of_interest = intermediate

    def discard_samples(self, samples_to_discard):
        """

        :param samples_to_discard: the name of the samples in a list which you want to delete from your further analysis
        :return: updates the sequencing report where the values for the given samples do not exist anymore

        """
        assert type(samples_to_discard) == list, "You have to give a list with the samples you want to discard"
        self.sequencing_report = self.sequencing_report[~self.sequencing_report['Experiment'].isin(samples_to_discard)]

    def add_binding_data(self):
        """"
        :return: adds binding data to your analysis. You can add mutliple files with the filechooser or a given path to the file. For more information about the necessary file structure, check the supplementary information.
        """
        self.binding_data = collect_binding_data(binding_data=self.binding_data)

        self.change_preferred_antigen(self.binding_data.columns.to_list()[1])

        # self.binding_data.to_csv("binding_data.csv")

    def merge_bind_seq_report(self):
        """
        :return: merges the binding data with the sequencing report.
        """
        assert self.binding_data is not None, "You have not given binding data. You can add it with the add_binding_data function"

        merged_reports = pd.merge(self.sequencing_report, self.binding_data, on="aaSeqCDR3", how="outer")
        return merged_reports

    def print_antigens(self):
        """
        :return: prints the antigens (columns) of your binding data
        """
        try:
            print(self.binding_data.columns.to_list()[1:])
        except:
            print("You have not given binding data.")

    def print_samples(self):
        """
        :return: prints the names of your samples, so you can insert them in lists or similar for the analysis with some plots
        """
        print(list(self.unique_experiments.values()))

    def save(self, enter_filename, dpi=300, format="png"):
        """
        :return: can be used to save your plots. It will ask you automatically for the directory where you want to save it
        """
        print("Choose the directory where you want to save your plot with the filechooser")
        try:
            from tkinter import filedialog
            save_dir = filedialog.askdirectory()
        except:
            save_dir = ""

        plt.savefig(fname=os.path.join(save_dir, enter_filename + f".{format}"), dpi=dpi, format=format)

    def close(self):
        plt.close()

    def change_experiment_names(self, specific=None, change_whole_dic=False):
        """
        :param specific: optional parameter. You can use this function to change the names of a specific sample.
        :param change_whole_dic: optional Parameter. The renaming can be done by using a dictionary and map it to the labels. You can change multiple or all labels by adding the new dictionary for this parameter.
        :return:You can use this function to change the name of your samples. Thus, you can change the labels of your plots.
        """

        self.unique_experiments = self.sequencing_report["Experiment"].unique().tolist()
        self.unique_experiments = dict(zip(self.unique_experiments, self.unique_experiments))
        if specific != None:
            assert type(
                specific) == str, "You have to give a string (inside: "") as input for the specific sample you want to change"
        if change_whole_dic != False:
            assert type(
                change_whole_dic) == dict, "You have to give a dictionary as input for the specific sample you want to change"
        if change_whole_dic == False:
            if specific == None:
                print(
                    "You will no go through all your samples and you will be able to change their names. If you want to skip a samples, just press enter.")
                for key in self.unique_experiments:
                    print(f"Current value for {key}: {self.unique_experiments[key]}")
                    new_value = input("Enter a new value or press any key to skip")
                    if len(new_value) > 1:
                        self.unique_experiments[key] = new_value
                    else:
                        pass
            else:
                new_value = input("Enter the new name for " + specific)
                self.unique_experiments[specific] = new_value
            self.sequencing_report["Experiment"] = self.sequencing_report["Experiment"].map(self.unique_experiments)
        else:
            with open("test_data" + "/experiment_names.pickle", "wb") as f:
                pickle.dump(change_whole_dic, f)

    def alignment_quality(self, log_transformation=False):
        """

        :param log_transformation: optional parameter. You can set it to True if you want to log transform your data
        :return: Creates a figure where you can see the Overall Reads per sample and the number of reads which could be aligned.
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        assert log_transformation in [True, False], "You have to give True or False as input for the log transformation"
        self.ControlFigure.clear_fig()
        try:
            barplot.barplot(self.ControlFigure.ax,
                            self.alignment_report,
                            self.sequencing_report,
                            self.font_settings,
                            self.legend_settings,
                            apply_log=log_transformation)

            self.ControlFigure.update_plot()
            self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                               self.ControlFigure.plot_type)
        except:
            print("Currenlty you do not have loaded an alignment report.")

    def aa_distribution(self, sample=None, region=[3, 7], protein=True):
        """
        :param sample: The sample you would like to analyze
        :param region: The input is a list and you can specify with the first value the beginning region and with the second value the end region within your sequences for which you want to know the amino acid composition. For instance: [3,7]
        :param protein: Default True. If you would like to analyze nucleotide sequences, set it to False
        :return: Returns a plot which shows the amino acid distribution in the given sequence range.
        """
        if sample == None:
            sample = self.preferred_sample
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(sample), "You have to give a string as input for the sample"
        assert type(
            region), "You have to give a list with the start and end position of the region you want to analyze. For instance: [3,7]"
        assert protein in [True, False], "You have to give True or False as input for the protein parameter"
        self.ControlFigure.clear_fig()
        stacked_aa_distribution.stacked_aa_distr(self.ControlFigure.ax,
                                                 self.sequencing_report,
                                                 sample,
                                                 region,
                                                 protein,
                                                 self.font_settings,
                                                 self.region_of_interest)

        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def rarefraction_curves(self, samples=None):
        """
        :param samples: you insert a list which contains the sample names
        :return: Shows your the rarefraction curves for the given samples.
        """
        if samples == None:
            samples = [self.experiments_list[0]]
        incorrect_samples = [x for x in samples if x not in self.experiments_list]
        assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"

        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        if type(samples) != list:
            print(
                "You have to give the sample names in the list, also if it is only one! A list is a container which is marked through:[] . Please try again.")
        else:
            self.ControlFigure.clear_fig()
            usq_plot.plot_USQ(fig=self.ControlFigure.fig,
                              sequencing_report=self.sequencing_report,
                              samples=samples,
                              font_settings=self.font_settings,
                              legend_settings=self.legend_settings)

            self.ControlFigure.update_plot()
            self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                               self.ControlFigure.plot_type)

    def logoPlot_single(self,
                        sample=None,
                        highlight_specific_pos=False,
                        method="proportion",
                        chosen_seq_length=16):
        """
        :param sample: insert the sample name
        :param highlight_specific_pos: optional. you can highlight a specific position. For instance if you want to highlight the 3rd position, you insert 3.
        :param method: You can specify whether you want to have on your y axis the frequency of the amino acids or the information content in bits. The default is proportion. If you want to have the information content, insert "bits"
        :param chosen_seq_length: 16 per default. You always analyze online one sequence length! You can change it if you would like to.
        :return: A logo Plot which shows you the composition of aminoacids per position
        """
        if sample == None:
            sample = self.preferred_sample
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(sample) == str, "You have to give a string as input for the sample"
        if highlight_specific_pos != False:
            assert type(
                highlight_specific_pos) == int, "You have to give an integer as input for the specific position you want to highlight"
        assert type(
            chosen_seq_length) == int, "You have to give an integer as input for the sequence length you want to analyze"
        self.ControlFigure.clear_fig()
        logo_plot.plot_logo_single(self.ControlFigure.ax,
                                   self.sequencing_report,
                                   sample,
                                   self.font_settings,
                                   highlight_specific_pos,
                                   self.region_of_interest,
                                   method,
                                   chosen_seq_length)

        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def logoPlot_multi(self,
                       samples="all",
                       chosen_seq_length=16,
                       method="proportion",
                       ):
        """
        :param samples: You analyze all samples per default. If you want to analyze specific samples it has to be a list with the corresponding sample names
        :param chosen_seq_length: 16 per default. You always analyze online one sequence length! You can change it if you would like
        :return: Gives you in one figure one logoPlot per sample.
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"
        if samples != "all":
            assert type(samples) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in samples if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(
            chosen_seq_length) == int, "You have to give an integer as input for the sequence length you want to analyze"
        self.ControlFigure.clear_fig()
        logo_plot.plot_logo_multi(self.ControlFigure.fig,
                                  self.sequencing_report,
                                  samples,
                                  self.font_settings,
                                  self.region_of_interest,
                                  method,
                                  chosen_seq_length,
                                  )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        self.ControlFigure.tighten()

    def lengthDistribution_single(self, sample=None):
        """

        :param sample: name of the sample from which you would like to see the length distribution
        :return: Shows you the length Distribution of your sequences of the given sample
        """
        if sample == None:
            sample = self.preferred_sample
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        assert type(sample) == str, "You have to give a string as input for the sample"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        length_distribution.length_distribution_single(self.ControlFigure.fig,
                                                       self.ControlFigure.ax,
                                                       self.sequencing_report,
                                                       sample,
                                                       self.font_settings,
                                                       self.region_of_interest)

        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def relative_abundance_multi(self, samples="all"):
        """
        :param samples: You analyze all samples per default. If you want to analyze specific samples it has to be a list with the corresponding sample names
        :return: Outputs a figure which shows the fractions per clones for each sample in the dataset
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"

        if samples != "all":
            assert type(samples) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in samples if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        else:
            samples = self.experiments_list
        self.ControlFigure.clear_fig()
        relative_sequence_abundance.relative_sequence_abundance_all(self.ControlFigure.fig,
                                                                    self.sequencing_report,
                                                                    samples,
                                                                    self.font_settings,
                                                                    self.region_of_interest)
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        self.ControlFigure.tighten()

    def lengthDistribution_multi(self, samples="all"):
        """
        :param samples: You analyze all samples per default. If you want to analyze specific samples it has to be a list with the corresponding sample names
        :return: Outputs one figure with one subplot per sample which shows you the distribution of the sequence length
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"
        if samples != "all":
            assert type(samples) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in samples if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        length_distribution.length_distribution_multi(self.ControlFigure.fig,
                                                      self.sequencing_report,
                                                      samples,
                                                      self.font_settings,
                                                      self.region_of_interest,
                                                      test_version=self.is_test)
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        self.ControlFigure.tighten()

    def rel_seq_abundance(self, samples=None, max_levenshtein_distance=0, length_filter=0, batch=3000):
        """

        :param samples: For a qualitative analysis choose samples from the same panning experiment. Input is a list
        :param max_levenshtein_distance: Default is 0. You can change it to see increased fraction with increased variability of certain sequences
        :param length_filter: Default is 0. You should change it if you change the levenshtein distance. Otherwise your results will be biased.
        :param batch: Default is 3000. The size of the sample which is chosen. The higher it is, the more computational intense.
        :return: Shows you a bar plot of the frequencies of the most abundant sequences. You can introduce the levenshtein distance to see how the frequency changes with higher variability of the sequences.
        """
        if samples == None:
            samples = [self.experiments_list[0]]
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        incorrect_samples = [x for x in samples if x not in self.experiments_list]
        assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(samples) == list, "You have to give a list with the samples you want to analyze"
        assert type(
            max_levenshtein_distance), "You have to give an integer as input for the maximum levenshtein distance"
        assert type(length_filter), "You have to give an integer as input for the length filter"
        assert type(batch) == int, "You have to give an integer as input for the batch size"
        self.ControlFigure.clear_fig()
        relative_sequence_abundance.relative_sequence_abundance(self.ControlFigure.ax,
                                                                self.sequencing_report,
                                                                samples,
                                                                max_levenshtein_distance,
                                                                length_filter,
                                                                batch,
                                                                self.region_of_interest,
                                                                self.font_settings,
                                                                self.legend_settings)

        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def basic_cluster(self, sample=None, max_ld=1, min_ld=0, second_figure=False, batch_size=300):
        """
        :param sample: type in a sample name you want to analyze
        :max_ld: optional Parameter where its default is 1. Is the maximum Levenshtein distance you allow per cluster
        :min_ld: optional Parameter where its default is 0. Is the minimum Levenshtein distance between sequences you allow
        :second_figure: optional Parameter. Default is False. If you want to see the a histogram with the levenshtein distances, set it to True
        :return:
        """
        if sample == None:
            sample = self.preferred_sample
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(sample) == str, "You have to give a string as input for the sample"
        assert type(max_ld) == int, "You have to give an integer as input for the maximum levenshtein distance"
        assert type(min_ld) == int, "You have to give an integer as input for the minimum levenshtein distance"
        assert type(second_figure) == bool, "You have to give True or False as input for the second figure"
        self.ControlFigure.clear_fig()
        fig2 = levenshtein_clustering.clusterSeq(
            self.ControlFigure.ax,
            self.sequencing_report,
            sample,
            max_ld,
            min_ld,
            batch_size,
            self.font_settings,
            second_figure,
            self.region_of_interest)

        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

        if second_figure == True:
            print("close the second window before you continue")

    def cluster_one_AG(self, antigen=None, max_ld=1, min_ld=0, batch_size=1000, specific_experiments=False):
        """

        :param antigen: is the name of the antigen you would like to analyze
        :param max_ld: optional Parameter where its default is 1. Is the maximum Levenshtein distance you allow per cluster
        :param min_ld: optional Parameter where its default is 0. Is the minimum Levenshtein distance between sequences you allow
        :param batch_size: optional Parameter where its default is 1000. Is the batch size you want to use for the analysis
        :param specific_experiments: optional Parameter. You can give the names of specific samples in a list if you want
        :return: Creates a figure where sequences are clustered based on Levenshtein distance. Additionally the binding data of the sequences against a specific antigen is given.
        """

        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"
        assert self.binding_data is not None, "You have not given binding data. You can add it with the add_binding_data function"
        if antigen == None:
            antigen = self.preferred_antigen
        assert type(antigen) == str, "You have to give a string as input for the antigen"
        assert type(max_ld) == int, "You have to give an integer as input for the maximum levenshtein distance"
        assert type(min_ld) == int, "You have to give an integer as input for the minimum levenshtein distance"
        assert type(specific_experiments) == list, "You have to give a list with the samples you want to analyze"
        self.ControlFigure.clear_fig()
        levenshtein_clustering.cluster_single_AG(self.ControlFigure.fig,
                                                 self.sequencing_report,
                                                 antigen,
                                                 self.binding_data,
                                                 max_ld,
                                                 min_ld,
                                                 batch_size,
                                                 self.region_of_interest,
                                                 specific_experiments,
                                                 )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def tsne_cluster_AG(self, sample=None, antigen=None, antigen_names=True, pca_components=70, perplexity=25,
                        iterations_tsne=2500):
        """
        :param sample: the sample you would like to analyze
        :param antigen: the toxins you would like to cluster
        :param antigen_names: Default is True. Prints the name of the toxin for the corresponding embedded sequence in the plot
        :param pca_components: optional. Default is 70
        :param perplexity: optional. Default 25
        :param iterations_tsne: optional. Default is 2500
        :return: It first embeds the sequences in a vector space and then reduces the dimensions and clusters them with PCA and TSNE. The sequences with the binding data are processed with the input sequences, to enable the plotting of the binding data.
        """
        if sample == None:
            sample = self.preferred_sample
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"
        assert self.binding_data is not None, "You have not given binding data. You can add it with the add_binding_data function"
        if antigen == None:
            antigen = [self.preferred_antigen]
        assert type(sample) == str, "You have to give a string as input for the sample"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert antigen_names in [True, False], "You have to give True or False as input for the antigen_names parameter"
        assert type(pca_components) == int, "You have to give an integer as input for the pca_components"
        assert type(perplexity) == int, "You have to give an integer as input for the perplexity"
        assert type(iterations_tsne) == int, "You have to give an integer as input for the iterations_tsne"
        assert type(antigen) == list, "You have to give a list with the antigens you want to analyze"

        self.ControlFigure.clear_fig()
        tsne_results = embedding_with_binding.cluster_toxins_tsne(self.ControlFigure.fig,
                                                                  self.sequencing_report,
                                                                  sample,
                                                                  antigen,
                                                                  self.binding_data,
                                                                  antigen_names,
                                                                  pca_components,
                                                                  perplexity,
                                                                  iterations_tsne,
                                                                  self.font_settings,
                                                                  self.colorbar_settings,
                                                                  False,
                                                                  self.region_of_interest)
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        save_matrix(tsne_results)

    def embedding_tsne(self,
                       samples=None,
                       strands=True,
                       pca_components=80,
                       perplexity=30,
                       iterations_tsne=2500,
                       batch_size=1000):
        """
        :param samples: the samples you would like to compare towards their sequences
        :param strands: Default is True. It means that you will plot a batch of the strands in your plot
        :param pca_components: Default is 80. Has to be applied for better accuracy of t-SNE. You can indirectly change the described variance with this.
        :param perplexity: Default is 30. It roughly determines the number of nearest neighbors that are considered in the embedding. A higher perplexity value results in a more global structure in the low-dimensional embedding, while a lower perplexity value emphasizes local structure. The optimal perplexity value for a given dataset depends on the dataset's intrinsic dimensionality, and it is usually determined by trial and err
        :param iterations_tsne: Default is 2500. number of times that the algorithm will repeat the optimization process for reducing the cost function. The optimization process aims to minimize the difference between the high-dimensional and low-dimensional representations of the data. More iterations result in a more optimized low-dimensional representation, but also increases the computational cost.
        :param batch_size: Default is 1000. The size of the sample which is chosen. The higher it is, the more computational intense.
        :return: Returns a plot where the sequences of the input samples are transformed in a vector space. Dimension reduction such as PCA and following t-SNE is used to plot it on a two dimensional space. The different colors indicate the different samples.
        """
        if samples == None:
            samples = [self.experiments_list[0]]
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        incorrect_samples = [x for x in samples if x not in self.experiments_list]
        assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(samples) == list, "You have to give a list with the samples you want to analyze"
        assert type(strands) == bool, "You have to give True or False as input for the strands parameter"
        assert type(pca_components) == int, "You have to give an integer as input for the pca_components"
        assert type(perplexity) == int, "You have to give an integer as input for the perplexity"
        assert type(iterations_tsne) == int, "You have to give an integer as input for the iterations_tsne"
        self.ControlFigure.clear_fig()
        cluster_embedding.show_difference(self.sequencing_report,
                                          samples,
                                          strands,
                                          batch_size,
                                          pca_components,
                                          perplexity,
                                          iterations_tsne,
                                          self.region_of_interest,
                                          self.ControlFigure.ax,
                                          self.legend_settings,
                                          self.font_settings)
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def morosita_horn(self, annotate_cells=False, specific_experiments=False):
        """
        :param annotate_cells: Default is False. If you want to see the values of the matrix, set it to True.
        :param specific_experiments: you can give a list with specific experiments
        :return: Returns a matrix of the identity between your samples based on the Morosita Horn Index
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        if specific_experiments != False:
            assert type(specific_experiments) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in specific_experiments if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        matrix = plt_heatmap.plot_heatmap(self.sequencing_report,
                                          True,
                                          "morosita_horn",
                                          self.ControlFigure.ax,
                                          self.colorbar_settings,
                                          self.font_settings,
                                          annotate_cells,
                                          self.region_of_interest,
                                          specific_experiments=specific_experiments,
                                          )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        save_matrix(matrix)

    def jaccard(self, annotate_cells=False, specific_experiments=False):
        """
        :param annotate_cells: Default is False. If you want to see the values of the matrix, set it to True.
        :param specific_experiments: give a list with specific samples you would like to analyze
        :return: Returns a matrix of the identity between your samples based on the Jaccard Index
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        if specific_experiments != False:
            assert type(specific_experiments) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in specific_experiments if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        matrix = plt_heatmap.plot_heatmap(self.sequencing_report,
                                          True,
                                          "jaccard",
                                          self.ControlFigure.ax,
                                          self.colorbar_settings,
                                          self.font_settings,
                                          annotate_cells,
                                          self.region_of_interest,
                                          specific_experiments=specific_experiments,
                                          )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        save_matrix(matrix)

    def sorensen(self, annotate_cells=False, specific_experiments=False):
        """
        :param annotate_cells: Default is False. If you want to see the values of the matrix, set it to True.
        :param specific_samples: give a list with specific samples you would like to analyze
        :return: Returns a matrix of the identity between your samples based on the Sorensen Dice Index
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        if specific_experiments != False:
            assert type(specific_experiments) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in specific_experiments if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        matrix = plt_heatmap.plot_heatmap(self.sequencing_report,
                                          True,
                                          "sorensen",
                                          self.ControlFigure.ax,
                                          self.colorbar_settings,
                                          self.font_settings,
                                          annotate_cells,
                                          self.region_of_interest,
                                          specific_experiments=specific_experiments,
                                          )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        save_matrix(matrix)

    def relative(self, annotate_cells=False, specific_experiments=False):
        """
        :param annotate_cells: Default is False. If you want to see the values of the matrix, set it to True.
        :param specific_samples: give a list with specific samples you would like to analyze
        :return: Returns a matrix of the identity between your samples based on the proportion of identical sequences
        """
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        if specific_experiments != False:
            assert type(specific_experiments) == list, "You have to give a list with the samples you want to analyze"
            incorrect_samples = [x for x in specific_experiments if x not in self.experiments_list]
            assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"
        self.ControlFigure.clear_fig()
        matrix = plt_heatmap.plot_heatmap(self.sequencing_report,
                                          True,
                                          "relative",
                                          self.ControlFigure.ax,
                                          self.colorbar_settings,
                                          self.font_settings,
                                          annotate_cells,
                                          self.region_of_interest,
                                          specific_experiments=specific_experiments,
                                          )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        save_matrix(matrix)

    def levenshtein_dendrogram(self, sample=None, max_cluster_dist=2, batch_size=1000):
        """
        :params sample: the sample you would like to analyze
        :max_cluster_dist: Default is 2. Maximum levenshtein distance between sequences within a cluster.
        :params batch_size: Default is 1000. The size of the sample which is chosen.
        :return: Returns a dendrogram of the sequences based on the Levenshtein distance
        """
        if sample == None:
            sample = self.preferred_sample
        assert type(sample) == str, "You have to give a string as input for the sample"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(
            max_cluster_dist) == int, "You have to give an integer as input for the maximum levenshtein distance"
        assert type(batch_size) == int, "You have to give an integer as input for the batch size"
        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "single"
        self.ControlFigure.clear_fig()
        hist_lvst_dist.levenshtein_dend(self.ControlFigure.ax,
                                        self.sequencing_report,
                                        sample,
                                        batch_size,
                                        max_cluster_dist,
                                        self.font_settings,
                                        self.region_of_interest
                                        )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)

    def dendro_bind(self, sample=None, antigens=None, max_cluster_dist=2, batch_size=1000, ascending=True):
        """
        :params sample: the sample you would like to analyze
        :params antigens: the antigens you would like to analyze. The input is a list.
        :max_cluster_dist: Default is 2. Maximum levenshtein distance between sequences within a cluster. The higher this number the bigger the dendrogram
        :params batch_size: Default is 1000. The number of sequences starting with the highest fractions which are used for the analysis from the sample
        :params ascending: Default is True. If you want to see the highest fractions first, set it to False
        :return: Creates a dendrogram which shows the realtionship between your sequences in the sample and your sequences with binding data based on levenshtein distance. Additionally a barplot with the binding data of the found sequences is given.
        """
        if sample == None:
            sample = self.preferred_sample
        assert self.binding_data is not None, "You have not given binding data. You can add it with the add_binding_data function"
        if antigens == None:
            antigens = [self.preferred_antigen]
        assert type(sample) == str, "You have to give a string as input for the sample"
        assert sample in self.experiments_list, "The provided sample name is not in your sequencing report. Please check the spelling or use the print_samples function to see the names of your samples"
        assert type(
            max_cluster_dist) == int, "You have to give an integer as input for the maximum levenshtein distance"
        assert type(batch_size) == int, "You have to give an integer as input for the batch size"
        assert type(ascending) == bool, "You have to give True or False as input for the ascending parameter"

        self.ControlFigure.check_fig()
        self.ControlFigure.plot_type = "multi"
        self.ControlFigure.clear_fig()
        hist_lvst_dist.dendo_binding(self.ControlFigure.fig,
                                     self.sequencing_report,
                                     self.binding_data,
                                     sample,
                                     antigens,
                                     batch_size,
                                     max_cluster_dist,
                                     self.font_settings,
                                     self.region_of_interest,
                                     ascending
                                     )
        self.ControlFigure.update_plot()
        self.style = plot_styler.PlotStyle(self.ControlFigure.ax,
                                           self.ControlFigure.plot_type)
        self.ControlFigure.tighten()

    def MSA_design(self, samples=None, batch_size=500):
        """
        :params samples: the samples you would like to analyze. The input is a list.
        :params batch_size: Default is 1000. The number of sequences starting with the highest fractions which are used for the analysis from the sample
        :return: Creates a multiple sequence alignment of the sequences of the samples you have chosen. The sequences are ordered by their frequency and they are chosen equally based on the given batch size from the different samples. The output is an interface with an overview of the MSA and the option to design a sequence based on the MSA and the findings of the analysis.
        """
        if samples == None:
            samples = [self.experiments_list[0]]
        assert type(samples) == list, "You have to give a list with the samples you want to analyze"
        incorrect_samples = [x for x in samples if x not in self.experiments_list]
        assert not incorrect_samples, f"The following sample(s) are not in your sequencing report: {', '.join(incorrect_samples)}. Please check the spelling or use the print_samples function to see the names of your samples"

        msa = MSA(self.region_of_interest,
                  self.Report,
                  self.Settings,
                  self.module_dir)
        msa = msa.run_MSA(batch_size, samples)

    def create_parser(self):
        path_to_mixcr = self.global_params["mixcr_path"]
        commands = []
        commands.extend(["java", f"-Xms{500}M", "-jar"])  # enable change of para
        commands.extend([path_to_mixcr])
        return commands

    def export_mixcr_quality(self,save_dir = None, specific_chain=None, metric=None, plot_type=None):
        if save_dir == None:
            save_dir = self.plot_path
        output_file = os.path.join(save_dir, self.experiment + "_alignQc.pdf")
        path_to_tables = os.path.join(self.module_dir, "my_experiments", self.experiment, "clones_result", "*.clns")
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["exportQc"])
        export_plots_commands.extend(["align"])
        export_plots_commands.extend([path_to_tables])
        export_plots_commands.extend([output_file])
        export_plots_commands.extend(["--force-overwrite"])
        subprocess.run(export_plots_commands)
        print(f"You can find the result file at: {output_file}")

        for i in glob.glob(path_to_tables):

            name=os.path.basename(i).split(".")[0]
            output_file = os.path.join(save_dir, name + "_tags.pdf")
            export_plots_commands = self.create_parser()
            export_plots_commands.extend(["exportQc"])
            export_plots_commands.extend(["tags"])
            export_plots_commands.extend([i])
            export_plots_commands.extend([output_file])
            export_plots_commands.extend(["--force-overwrite"])
            subprocess.run(export_plots_commands)
            print(f"You can find the result file at: {output_file}")
            name = os.path.basename(i).split(".")[0]
            output_file = os.path.join(save_dir, name + "chainUsage.pdf")
            export_plots_commands = self.create_parser()
            export_plots_commands.extend(["exportQc"])
            export_plots_commands.extend(["chainUsage"])
            export_plots_commands.extend(["--hide-non-functional"])
            export_plots_commands.extend([i])
            export_plots_commands.extend([output_file])
            export_plots_commands.extend(["--force-overwrite"])
            subprocess.run(export_plots_commands)
            print(f"You can find the result file at: {output_file}")
        output_file = os.path.join(save_dir, self.experiment + "_coverage.pdf")
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["exportQc"])
        export_plots_commands.extend(["coverage"])
        export_plots_commands.extend([path_to_tables])
        export_plots_commands.extend([output_file])
        export_plots_commands.extend(["--force-overwrite"])
        subprocess.run(export_plots_commands)
        print(f"You can find the result file at: {output_file}")

        if specific_chain != None:
            export_plots_commands.extend(["--chains", specific_chain])
        if metric != None:
            export_plots_commands.extend(["--metrics", metric])
        if plot_type != None:
            export_plots_commands.extend(["--plotType", plot_type])


    def mixcr_explain_diversity(self,plot_save_dir = None, metric = "cdr3metrics",chains = None, plot_type = "violin", output_type = "pdf"):
        """
        :param: metric: Default is cdr3metrics. You can choose between cdr3metrics and diversity. If you choose diversity you will focus on the clone fractions whereas with cdr3metrics you will focus on certain aspects of these chains such as length (https://mixcr.com/mixcr/reference/mixcr-postanalysis/#diversity-measures)
        :param: chains: Default is None. Possible inputs are : IGH, IGL, IGK, TRA, TRB, TRG, TRD, IG. You will choose a specific chain for the analysis.
        :param: plot_type: Default is violin. You can choose between: boxplot, boxplot-bindot, boxplot-jitter, violin, violin-bindot, barplot, barplot-stacked, lineplot, lineplot-jitter, lineplot-bindot, scatter
        :param: output_type: Default is pdf. Allows you to control the file type of your output. Possible values are: pdf, jpeg, png, svg, eps,
        """
        if metric in ["cdr3metrics", "diversity"]:
            pass
        else:
            print("Please choose a correct value for the metric. Pipeline continues with:\ncdr3metrics and cdr3lenAA for metric_type")
            metric = "cdr3metrics"
            metric_type = "cdr3lenAA"

        chains_values = [None, "IGH", "IGL", "IGK", "TRA", "TRB", "TRG", "TRD", "IG"]
        if chains not in chains_values:
            print("Please enter a correct shortcut for the chain preferred chain. These are: ")
            [print(i) for i in chains_values]
        plot_type_values = ["boxplot", "boxplot-bindot", "boxplot-jitter", "violin", "violin-bindot", "barplot", "barplot-stacked", "lineplot", "lineplot-jitter", "lineplot-bindot", "scatter"]
        if plot_type not in plot_type_values:
            print("Please enter a correct shortcut for the chain plot type. These are: ")
            [print(i) for i in plot_type_values]


        print(f"To be able to understand the following processing go to: https://mixcr.com/mixcr/reference/mixcr-postanalysis/#overlap-postanalysis")
        plot_name = input("How do you want to call your plot")

        if plot_save_dir == None:
            plot_save_dir = self.plot_path
        save_dir = os.path.join(self.module_dir, "my_experiments", self.experiment)
        json_dir = os.path.join(save_dir, "pa_individual.json")
        path_to_tables = os.path.join(self.module_dir, "my_experiments", self.experiment, "clones_result", "*.clns")
        if not os.path.isfile(json_dir):
            export_plots_commands = self.create_parser()
            export_plots_commands.extend(["postanalysis"])
            export_plots_commands.extend(["individual"])
            export_plots_commands.extend(["--default-downsampling", "none"])
            export_plots_commands.extend(["--default-weight-function", "none"])
            export_plots_commands.extend([path_to_tables])
            export_plots_commands.extend([json_dir])
            subprocess.run(export_plots_commands)
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["exportPlots"])
        export_plots_commands.extend([metric])
      #  export_plots_commands.extend(["--metric",metric_type])
      #  export_plots_commands.extend(["-f"])
        if not chains == None:
            export_plots_commands.extend(["--chains", chains])
        export_plots_commands.extend(["--plot-type", plot_type])
        export_plots_commands.extend([json_dir])
        export_plots_commands.extend([os.path.join(plot_save_dir, plot_name + "." + output_type)])
        subprocess.run(export_plots_commands)



    def mixcr_vdj_usage(self,chains = None, bar_plot = False,bar_plot_by_sample = False, no_genes_dendro = False, no_samples_dendro = False, ):
        save_dir = os.path.join(self.module_dir, "my_experiments", experiment)
        json_dir = os.path.join(save_dir, "pa_individual.json")
        if not os.path.isfile(json_dir):
            export_plots_commands = self.create_parser()
            export_plots_commands.extend(["postanalysis"])
            export_plots_commands.extend(["individual"])
            export_plots_commands.extend(["--default-downsampling"])
            export_plots_commands.extend(["--default-weight-function"])
            export_plots_commands.extend([path_to_tables])
            export_plots_commands.extend([json_dir])
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["vUsage"])
        export_plots_commands.extend(["-f"])
        export_plots_commands.extend([json_dir])
        export_plots_commands.extend([os.path.join(save_dir, "vUsage_heatmap.pdf")])
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["jUsage"])
        export_plots_commands.extend(["-f"])
        export_plots_commands.extend([json_dir])
        export_plots_commands.extend([os.path.join(save_dir, "jUsage_heatmap.pdf")])
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["vjUsage"])
        export_plots_commands.extend(["-f"])
        export_plots_commands.extend([json_dir])
        export_plots_commands.extend([os.path.join(save_dir, "vjUsage_heatmap.pdf")])
        export_plots_commands = self.create_parser()
        export_plots_commands.extend(["isotypeUsage"])
        export_plots_commands.extend(["-f"])
        export_plots_commands.extend([json_dir])
        export_plots_commands.extend([os.path.join(save_dir, "isotypeUsage_heatmap.pdf")])











