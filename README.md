Requires Python (minimum 2.4) and modules:
After ensuring Python is installed, use pip to install modules to be sure (probably need to be su to do this):
  pip install os
  pip install paramiko
  pip install time
  pip install re
  pip intall sys
  pip install threading
  pip install datetime
  pip install csv
  pip install getpass
  pip install os.path
  pip install subprocess
  pip install base64




Unzip ConfigGen.zip to your home/ directory
Change ownership of files (if needed)
  cd /home/username
  chown -R username.username /ConfigGen

Directory structure should look like the following:
	/home/username/ConfigGen/
			1parse_csv.py
			2create_configs.py
			3push_configs.py
				/configs	<<< where config files will be written to review before pusing to devices
				/data_csv	<<< your original csv file goes here (discussed later)
				/dumps		<<< on approval, all work files placed here for deletion
				/logs		<<< logs files to read if something goes wrong
				/new_data_csv	<<< parsed csv file for use to push configs to devices
				/post_results	<<< each device's session output as a result from pushing configs to devices
				/templates	<<< where your jinja2 templates reside

First create MS Excel spreadsheet with device headers and data
        - first and second header must be named:
		host_ip <<< fields contain management ip of devices 
		host_name <<< fileds contain hostname of devices
Export Excel spreadsheet as standard MS CSV file - filename is name not important but must have ".csv" extension
Move you exported csv file to the ConfigGen/data_csv directory
	- will be used to create device configuration files
        - directory can contain multiple csv files and option to select your use file offered later

Create and place you jinja2 templates into the ConfigGen/templates directory
        - jinja2 templates use the "{{ headername }}" convention to read your csv and populate your config files with variable from the fileds
	  - for example:
		router {{ host_name }} in your jinja2 template will result in the variable, field,  from the host_name, header, in you csv, to populate your config file with that variable
	- and example jinja2 template, "cisco_tmpl.j2," can be used as a guide to create your own templates



Running the scripts:

	Once your csv(s) and template(s) are in the proper directories, run the following scripts in order:

	- ./1parse_csv.py
		- this script will ask which csv file you wish to work with
		- after selecting your csv, the script will:
			- parse you csv file for only the first two headers and data
			- write a new csv file with only the parsd headers and fields to ConfigGen/new_data_csv/outputdata.csv
			- parse and remove the headers from the new outputdata.csv file
			- write a new file, containg only the first two fields from your original csv, to ConfigGen/new_data_csv/no_header_host_data.csv
			- delete the "ouputdata.csv" file


	- ./2create_configs.py
		- this script will ask which original csv file you want and which template to use for that data
			- once run, your original csv file, at ConfigGen/data_csv/somefile.csv, and chosen template file will be used to generate your device configuration files
			- your configuration files will be placed in ConfigGen/configs and you will be give a chance to review them before moving to the final and optional script

	- ./3push_configs.py  (this script is optional)
		- this script is used to open ssh connections to the devices for which you've created configurations
		###### WARNING!  Once you provide credentials to this script, your condigurations will be        #####
		###### written to your devices, so make sure that you've validate your configs before continuing #####
		- the script will:
			- prompt you for user and password credentials to login to your device via ssh
			- ideally the credentials are the same for all devices
			- the script will use the ConfigGen/new_data_csv/no_header_host_data.csv to determine which configuration files belongs to which device and what ip address to connect and write the configuration to the device
			- the script will write the configurations to ALL your devices
			- the script will also record the session during the config push and write each devices session to the ConfigGen/post_results file (each device filename will be in the format "ip_address_host_name.txt")


Cleanup:

	For now, cleanup of all your files will be manual (this is a work-in-progress).  There is no need to remove any of the files from the "logs" or new_data_csv" directories, these are overwritten for ever run of the scripts,  but you may want to consider deleting files in the /config, /template and data_csv/ files that you no longer need. 
			


TODO:

 - add progress bar to 3push_configs.py script (lengthy run with no user feedback)
 - add delete and/or archive options to deal with created csv and config files
 - add more error handling to 3push_configs.py script

