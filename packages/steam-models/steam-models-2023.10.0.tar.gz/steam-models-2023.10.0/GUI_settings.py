import os
from pathlib import Path
from matplotlib import pyplot as plt
import ipywidgets as widgets

from steam_sdk.builders.BuilderModel import BuilderModel

def STEAM_Library(case_model: str = 'magnet', model_name='', software='', flagBuild=False, verbose=False, flag_plot_all=False):
	
	# If the output folder does not exist, make it
	output_folder_parent = os.path.join(case_model +'s', model_name, 'output')
	if not os.path.isdir(output_folder_parent):
		print("Output folder {} does not exist. Making it now".format(output_folder_parent))
		Path(output_folder_parent).mkdir(parents=True)
	
	file_model_data = os.path.join(case_model +'s', model_name, 'input', 'modelData_' + model_name + '.yaml')
	output_folder   = os.path.join(case_model +'s', model_name, 'output', software)

    # Set relative path for settings file
	relative_path_settings = Path('settings', 'user_settings' ).resolve()
    
	print('case_model:    {}'.format(case_model))
	print('model_name:    {}'.format(model_name))
	print('software:      {}'.format(software))
	print('flagBuild:     {}'.format(flagBuild))
	print('verbose:       {}'.format(verbose))
	print('flag_plot_all: {}'.format(flag_plot_all))
	print('relative_path_settings: {}'.format(relative_path_settings))
	
	# Build model
	print('Model generation started.')
	BM = BuilderModel(file_model_data=file_model_data, case_model=case_model, software=[software], 
						output_path=output_folder, relative_path_settings=relative_path_settings,
						flag_build=flagBuild, flag_dump_all=False, verbose=verbose, flag_plot_all=flag_plot_all
						)
		
	# Assign values
	#model_name  = model_name
	#software    = software
	#flagBuild   = flagBuild
	#verbose     = verbose
	print('Model generation completed.')
    
def find_all_magnet_models():
    list_subfolders = next(os.walk('magnets'))[1]  # List all subfolders
    list_subfolders = [x for x in list_subfolders if not ".sys" in x]  # Remove entries with ".sys"
    list_subfolders = [x for x in list_subfolders if not "__pycache__" in x]  # Remove entries with "__pycache__"
    return list_subfolders

def find_all_circuit_models():
    list_subfolders = next(os.walk('circuits'))[1]  # List all subfolders
    list_subfolders = [x for x in list_subfolders if not ".sys" in x]  # Remove entries with ".sys"
    list_subfolders = [x for x in list_subfolders if not "__pycache__" in x]  # Remove entries with "__pycache__"
    return list_subfolders
