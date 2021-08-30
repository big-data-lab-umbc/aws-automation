# MultiGpus-Domain-Adaptation
Fork from https://github.com/jindongwang/transferlearning/tree/master/code/DeepDA  

Need download dataset from orignal repositery. For not crashing your local machine, you can set "backbone: dann" on DeepCoral.yaml. It’s a small model.  

Run code:  
$python3 main.py --config DeepCoral/DeepCoral.yaml --data_dir office31 --src_domain webcam --tgt_domain amazon
