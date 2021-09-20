## Distributed machine computation on CPUs

- [Web based Approach to run the example on a single CPU](Web-based-CPU-example-with-script.md)
- [Web based Approach to run the example on a single CPU with docker](Web-based-CPU-example-with-docker.md)


### Prerequisites:
- Web based: follow all steps in [web based cloud computation](https://github.com/AI-4-atmosphere-remote-sensing/aws-automation#web-based). Make sure you have installed docker and all source code/data in your VMs.

- Boto: follow same steps from 1-4 in [boto single machine computation](https://github.com/AI-4-atmosphere-remote-sensing/aws-automation/blob/main/README.md#run-single-machine-computation). Then get VMs' ip address
```bash
ipAll()
```

### Run distributed programs on CPUs:
1. Open new terminals, connect to all VMs
```bash
ssh -i ~/.ssh/id_rsa ubuntu@<VMs_ip_address>
```

2. Run distributed CPU containers on all VMs
```bash
docker run -it --network host -v /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case:/root/ML_based_Cloud_Retrieval_Use_Case starlyxxx/dask-decision-tree-example:latest /bin/bash
```

3. Run Dask cluster on all VMs in background
- Primary VM: 
```bash
dask-scheduler & 
dask-worker <your-dask-scheduler-address> &
```

- Secondary VMs: 
```bash
dask-worker <your-dask-scheduler-address> &
```

4. Run programs on CPUs
On any VM:
```bash
cd ML_based_Cloud_Retrieval_Use_Case/Code
/usr/bin/python3.6 dask_ml_based_cloud_retrieval_with_data_preprocessing.py <your-dask-scheduler-address>
```

Dask dashbroad can be check on [http://Your_VM_PublicDNS:8787]()

5. Terminate all VMs on EC2 when finishing experiments.
