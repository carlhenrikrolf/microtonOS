# systemd
systemd is a system for managing applications that start automatically at boot and run in the background (d=daemon, common name for such background software).
There aren't as many resources explainign well and briefly how to use it as, say, Python, so I'm making a short introduction.

**Test the commandline argument.**
You can both open a window and let it run headless.
For headless, you usually just have to add the `--headless` option, otherwise, check `--help`.
systemd does not run in the same *environment* as the terminal.
This means that some variables may not be defined for example.
Therefore, to test whether the commandline argument would work in systemd, run
```bash
sudo --user <username> <commandline>
```
If you want to run the argument as root, simply use `sudo <commandline>`.
If no (fatal) error occurs, you can move ahead.
One common error is that some environment variable is not defined.
In that case, test `sudo --user <username> <definition>; <commandline>`.
Another common problem is that the commandline may be waiting for input.
This may not throw an error, but is often indicated by the `>` symbol on a new line.
In that case, try to find an option to disable inputs from `--help`.

**Create the .service file.**
Create a file with the name `<name>.service`.
Fill it with the following template:
```
[Unit]
Description=<arbitrary summary>
After=graphical.target

[Service]
User=<username>
ExecStart=<commandline>
Restart=always
RestartSec=2s
TimeoutSec=infinity

[Install]
WantedBy=graphical.target
```
Explanation. The `<arbitrary summary>` can be whatever you want.
It's useful to remind you what is happeing while debugging.
`graphical.target` refers to the part of the boot process where the screen is loaded.
This is the last part of the boot process.
We want the musical applications to start when everything else is done and that's why this term arises.
`<username>` can be replaced by `root` if appropriate.
The rest of the `[service]` section says that if the application fails to start or gets shut down, it should reload.
The reload should happen every 2s. The `s` is not mandatory as the unit is assumed to be seconds unless otherwise specified and should go on forever.

Additional options.
If the application requires that another application is running, you can use the `Requires=<another -service file>` option under `[Unit]`.
You can use this repeatedly if several other applications are necessary.
If you need to define a variable before running `<commandline>`, you can add `Environment=<definition>` under `[Service]`.
If you instead need to run another command, you can use `ExecStartPre=<other command>`or `ExecStartPost=<other command>` for running it before or after, respectively.

**Installing the .service file.**
Copy or move the file to `/lib/systemd/system/`.
Run
```bash
sudo systemctl enable <name>.service
sudo systemctl start <name>.service
```
To check whether things are working correctly, run `systemctl status <name>.service`.
If something is wrong with the application, run `sudo systemctl restart <name>.service` after fixing it.
If something is wrong with the .service file, run
```bash
sudo systemctl stop <name>.service
sudo systemctl disable <name>.service
```
Replace the .service file with the fixed .service file and start this step all over.

