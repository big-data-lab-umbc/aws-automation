### Distributed machine computation on GPUs

1. Follow same steps from 1-4 in single machine computation. Then get VMs' ip address
```bash
ipAll()
```

2. Open new terminals, connect to all VMs
```bash
ssh -i ~/.ssh/id_rsa ubuntu@<VMs_ip_address>
```

3. Add primary VM's public key to all secondary VMs' authorized_keys file in <~/.ssh/authorized_keys>. (If key pair does not exsit, use $ssh-keygen to generate a key pair.) Check if primary VM can ssh into Secondary VMs by using $ ssh -o "StrictHostKeyChecking no" <Secondary-VMs-ip-address>. Then generate a shared file system in </mnt/share/>
```bash
sudo mkdir -p /mnt/share/ssh && sudo cp ~/.ssh/* /mnt/share/ssh
```

4. Run distributed GPU containers on all VMs
Primary VM: 
```bash
nvidia-docker run -it --network=host -v /mnt/share/ssh:/root/.ssh -v /home/ubuntu/MultiGpus-Domain-Adaptation-main:/root/MultiGpus-Domain-Adaptation-main -v /home/ubuntu/office31:/root/office31 starlyxxx/horovod-pytorch-cuda10.1-cudnn7:latest /bin/bash
```
Secondary VMs: 
```bash
nvidia-docker run -it --network=host -v /mnt/share/ssh:/root/.ssh -v /home/ubuntu/MultiGpus-Domain-Adaptation-main:/root/MultiGpus-Domain-Adaptation-main -v /home/ubuntu/office31:/root/office31 starlyxxx/horovod-pytorch-cuda10.1-cudnn7:latest bash -c "/usr/sbin/sshd -p 12345; sleep infinity"
```

5. Run programs on GPUs

On primary VM: 
```bash
cd MultiGpus-Domain-Adaptation-main
horovodrun --verbose -np 2 -H <machine1-address>:1,<machine2-address>:1 -p 12345 /usr/bin/python3.6 main.py --config DeepCoral/DeepCoral.yaml --data_dir ../office31 --src_domain webcam --tgt_domain amazon
```
