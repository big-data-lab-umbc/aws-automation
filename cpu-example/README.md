### Distributed machine computation on CPUs

1. Follow same steps from 1-4 in single machine computation. Then get VMs' ip address
```bash
ipAll()
```

2. Open new terminals, connect to all VMs
```bash
ssh -i ~/.ssh/id_rsa ubuntu@<VMs_ip_address>
```

3. Run distributed CPU containers on all VMs
```bash
docker run -it --network host -v /home/ubuntu/ML_based_Cloud_Retrieval_Use_Case:/root/ML_based_Cloud_Retrieval_Use_Case starlyxxx/dask-decision-tree-example:latest /bin/bash
```

4. Run Dask cluster on all VMs in background
Primary VM: 
```bash
dask-scheduler & 
dask-worker <your-dask-scheduler-address> &
```

Secondary VMs: 
```bash
dask-worker <your-dask-scheduler-address> &
```

5. Run programs on CPUs
On any VM:
```bash
cd ML_based_Cloud_Retrieval_Use_Case/Code
/usr/bin/python3.6 dask_ml_based_cloud_retrieval_with_data_preprocessing.py <your-dask-scheduler-address>
```

Dask dashbroad can be check on [http://Your_Dask_Scheduler_PublicDNS:8787]()
