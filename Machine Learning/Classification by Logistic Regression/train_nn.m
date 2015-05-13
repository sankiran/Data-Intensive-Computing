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

trainSizemax=15982;

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

    lbl = zeros(size(y,1),10);
for i=1:size(y)
    lbl(i,y(i)+1) = 1;
end

r = randperm(size(len_vect,1));

%Here, we divide input data into training, and validation sets.
trnlbl = lbl(r(1:15982),:);
trn_data = len_vect(r(1:15982),:);

trn_size=size(trn_data,1);

val_lbl = lbl(r(15983:end),:);
val_data= len_vect(r(15983:end),:);

ip_node = size(trn_data, 2); 
hid_node = 200;		   
op_node = 10;		   
 
trn_data = [(ones(size(trn_data,1),1)), trn_data];

w1 = rand(hid_node, ip_node + 1) * 2* 0.1 - 0.1;

w2 = rand(op_node, hid_node + 1) * 2* 0.25 - 0.25;


%Here, we define the parameters.
alpha = 0.15;

lambda = 0;

count_epoch = 100;

m=0;

while m <= count_epoch
        
        hid_out=double(1./(1.0+exp(-1*(trn_data*transpose(w1)))));
        hid_count = size(hid_out,1);
        bias = ones(size(hid_out,1),1);
        z = [bias hid_out];
        z_prod = double(1./(1.0+exp(-1*(z*transpose(w2)))));
        
        grad_2 = ((transpose(z_prod - trnlbl))*z)/trn_size;
        product_del_w1=(z_prod - trnlbl)*w2;
        prod_hidden_out= (1-z).*z;
        prod1_out=(prod_hidden_out).*(product_del_w1);
        gradient_weight1_int = (transpose(prod1_out))*trn_data;
        grad1_1 = transpose(((1-z).*z).*product_del_w1)*trn_data;
        grad_1=(grad1_1(1:(size(grad1_1,1)-1),:))/trn_size;
        w2=(w2-alpha*grad_2);
        w1=(w1-alpha*grad_1); 
        m=m+1;
        

end
    %%Validation is performed here.
       [testaccuracy]=nntest(val_data,w1,w2,val_lbl);
       
        
        
        
     
     