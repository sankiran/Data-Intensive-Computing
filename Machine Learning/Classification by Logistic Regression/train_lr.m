d0 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/0.txt');
d1 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/1.txt');
d2 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/2.txt');
d3 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/3.txt');
d4 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/4.txt');
d5 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/5.txt');
d6 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/6.txt');
d7 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/7.txt');
d8 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/8.txt');
d9 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_train/9.txt');

len_vect = [];

len_vect = [d0;d1;d2;d3;d4;d5;d6;d7;d8;d9];

size_d0 = size(d0);
size_d1 = size(d1);
size_d2 = size(d2);
size_d3 = size(d3);
size_d4 = size(d4);
size_d5 = size(d5);
size_d6 = size(d6);
size_d7 = size(d7);
size_d8 = size(d8);
size_d9 = size(d9);

y = zeros(size(len_vect,1),10);
y(1:2000,1) = 1;
y(2001:3979,2) = 1;
y(3980:5978,3) = 1;
y(5979:7978,4) = 1;
y(7979:9978,5) = 1;
y(9979:11978,6) = 1;
y(11979:13978,7) = 1;
y(13979:15978,8) = 1;
y(15979:17978,9) = 1;
y(17979:19978,10) = 1;

bias_mat = ones(19978,1);

inp_vect = horzcat(bias_mat, len_vect);

wgt_mat = rand(513, 10);

new_wgt = inp_vect * wgt_mat;

exp_wgt = exp(new_wgt);
learnrate = 0.001;
for i = 1:size(exp_wgt,1)
    y_mat(i,:) = exp_wgt(i,:)./sum(exp_wgt(i,:));
end 
    grad_mat = inp_vect' * (y_mat - y);
    
    [max1,ind_max1] = max(y_mat,[],2);
    [max2,ind_max2] = max(y,[],2);
    
    count = 0;
    for j = 1:19978
        if ind_max1(j) == ind_max2(j)
            count = count + 1;
        end
    end 
        accu_old = count/19978;
        
        for k = 1:100
    
            fin_wgt = wgt_mat - learnrate * grad_mat;
            wgt_mat = fin_wgt;
            tmp_mat = inp_vect * fin_wgt;
            actn_wgt = exp(tmp_mat);
         
            for i = 1:size(actn_wgt,1)
                
                y_mat(i,:) = actn_wgt(i,:)./sum(actn_wgt(i,:));
            end 
    
    grad_mat = inp_vect' * (y_mat - y);
    
    [max1,ind_max1] = max(y_mat,[],2);
    [max2,ind_max2] = max(y,[],2);
    
    count =0;
    for j = 1:19978
        if ind_max1(j) == ind_max2(j)
            count = count + 1;
        end
    end 
        dlmwrite('classes_lr.txt', y_mat, ' ');
        accu_new = count/19978;
        
        if(accu_new > accu_old) 
            learnrate = learnrate * 1.2;
        else
            learnrate = learnrate / 2;
        end
            
        accu_old = accu_new;
        end 
        
        
[acc] = lr_test(fin_wgt);




