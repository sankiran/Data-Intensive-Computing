fprintf('My ubit name is %s\n','sankiran');
fprintf('My student number is %d \n',50134545);
input=load('project1_data.mat');
X=input.input_matrix;
tgt=input.target;
[W_cfs,phi,variance,M]=train_cfs(X,tgt);
test_cfs(phi,tgt,W_cfs);
[W_gd,phi]=train_gd(X,tgt);
test_gd(phi,tgt,W_gd);