function [accu_new] = lr_test(fin_wgt)

d10 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/0.txt');
d11 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/1.txt');
d12 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/2.txt');
d13 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/3.txt');
d14 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/4.txt');
d15 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/5.txt');
d16 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/6.txt');
d17 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/7.txt');
d18 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/8.txt');
d19 = importdata('/Users/sankiran/Documents/Study/UB/Machine_Learning/Project_2/feature/features_test/9.txt');

len_vect = [];

len_vect = [d10;d11;d12;d13;d14;d15;d16;d17;d18;d19];

size_d10 = size(d10);
size_d11 = size(d11);
size_d12 = size(d12);
size_d13 = size(d13);
size_d14 = size(d14);
size_d15 = size(d15);
size_d16 = size(d16);
size_d17 = size(d17);
size_d18 = size(d18);
size_d19 = size(d19);

y = zeros(size(len_vect,1),10);
y(1:150,1) = 1;
y(151:300,2) = 1;
y(301:450,3) = 1;
y(451:600,4) = 1;
y(601:750,5) = 1;
y(751:900,6) = 1;
y(901:1050,7) = 1;
y(1051:1200,8) = 1;
y(1201:1350,9) = 1;
y(1351:1500,10) = 1;

            bias_mat = ones(1500,1);

            inp_vect_test = horzcat(bias_mat, len_vect);


            tmp_mat = inp_vect_test * fin_wgt;
            actn_wgt = exp(tmp_mat);
         
            for i = 1:size(actn_wgt,1)
                
                y_mat(i,:) = actn_wgt(i,:)./sum(actn_wgt(i,:));
            end
            
            [max1,ind_max1] = max(y_mat,[],2);
            [max2,ind_max2] = max(y,[],2);
    
    count =0;
    for j = 1:1500
        if ind_max1(j) == ind_max2(j)
            count = count + 1;
        end
    end 
        
        accu_new = count/1500;

end


