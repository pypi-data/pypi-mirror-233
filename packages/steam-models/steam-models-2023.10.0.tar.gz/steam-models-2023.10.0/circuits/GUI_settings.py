import os
from matplotlib import pyplot as plt
from steam_sdk.builders.BuilderModel import BuilderModel

def STEAM_Library(case_model: str = 'magnet', magnet_name='', software='', flagBuild=False, verbose=False, flag_plot_all=False):
	
	# If the output folder does not exist, make it
	output_folder_parent = os.path.join(magnet_name, 'output')
	if not os.path.isdir(output_folder_parent):
		print("Output folder {} does not exist. Making it now".format(output_folder_parent))
		os.mkdir(output_folder_parent)
	
	file_model_data = os.path.join(magnet_name, 'input', 'modelData_' + magnet_name + '.yaml')
	output_folder   = os.path.join(magnet_name, 'output', software)

	print('case_model:    {}'.format(case_model))
	print('magnet_name:   {}'.format(magnet_name))
	print('software:      {}'.format(software))
	print('flagBuild:     {}'.format(flagBuild))
	print('verbose:       {}'.format(verbose))
	print('flag_plot_all: {}'.format(flag_plot_all))
	
	# Build model
	print('Model generation started.')
	BM = BuilderModel(file_model_data=file_model_data, case_model=case_model, software=[software], flag_build=flagBuild, flag_dump_all=False,
					  output_path=output_folder, verbose=verbose, flag_plot_all=flag_plot_all)
		
	# Assign values
	#magnet_name = magnet_name
	#software    = software
	#flagBuild   = flagBuild
	#verbose     = verbose
	print('Model generation completed.')