# Boto Based Execution with Docker

## Command line automation via Boto
Follow steps below for automating single machine computation. For distributed machine computation, see README on each example's sub-folder.  

### Prerequisites:  
```bash
pip3 install boto fabric2 scanf IPython invoke
pip3 install Werkzeug --upgrade
```

### Run single machine computation: 
1. Configuration

Use your customized configurations. Replace default values in <./config/config.ini>  

2. Start IPython   
```bash
python3 run_interface.py 
```

3. Launch VMs on EC2 and wait for initializing
```bash
LaunchInstances()
```
4. Install required packages on VMs
```bash
InstallDeps() 
```

5. Automatically run Single VM ML Computing 
```bash
RunSingleVMComputing() 
```

6. Terminate all VMs on EC2 when finishing experiments.
```bash
TerminateAll() 
```