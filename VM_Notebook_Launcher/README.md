
This set of scripts allows you to set up a personal Juypter Notebook server running on a Google Cloud VM. While
similar in function to Google Cloud Datalab, this approach does not require you to run a gcloud command on your
desktop. Once it is up and running, there is no more desktop code component. The notebook server requires a password you
provide as part of the setup, and also installs a GCP firewall rule to only accept traffic from the IP range you
specify in the setEnvVars.sh file.

1) Edit the setEnvVars.sh file to personalize your installation
2) Run ./startAndLaunch.sh
3) Browser will (eventaully) open to the new VM. Since the certificate is self-signed, you will be required to
   accept the certificate you just created when you first hit the VM.
4) Start a notebook. Note that the system creates five distinct virtualenvs you can choose from to customize your
   environment for each notebook.
5) Alternately, upload a notebook. If you upload an existing notebook, it will select the virtualenv it was
   created with if a matching name exists.
6) The notebook server will start automatically when the VM is started up. CURRENTLY *YOU* must shut the
   VM down from the console when you are done!
7) You are also responsible for deleting the VM, releasing the static IP address, and deleting the firewall rule when you
   retire the VM.
8) You can launch your browser to the server anytime using the run_browser.sh command. It pulls the static IP and
   port you specified from the setEnvVars.sh. Be sure to remember your password!
8) The get_pass.py script this directory supports the startAndLaunch.sh script. It is basically the snippet of code in the
   Jupyter server code base that generates password hashes. The install_script.sh is what is uploaded to the VM to
   get the server installed and running. The only files that need to remain after you have created the VM are the
   run_browser.sh and setEnvVars.sh scripts.