# Using Reportr

To use reportr you can either use the CLI or the GUI to run the CLI simply run

        cd ./CLI

And then run the script with

       py main.py

To run the GUI it can be a bit harder. if you are running windows you should be able to go to the GUI folder and then the build folder then the folder inside of there and run the reportr.exe file. If that does not work you can follow the next steps

To run the source code locally you will need to install some dependencies. sv_ttk, darkdetect and bcrypt you can do this with the following command

       pip install sv_ttk darkdetect bcrypt

If you want to use a virtual environment you can do the following

    	python -m venv venv

and then activate the virtual environment with this command

    	\venv\Scripts\activate

Once activated you can install the packages

    	pip install sv_ttk darkdetect bcrypt

Once everything is installed you can simply run the python script with the following commands

    	cd ./GUI
    	------------------------------------------------------------------------------------------
    	py main.py

and you should now be able to use the reportr app!
