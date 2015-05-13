function[testaccuracy]=nntest(test_data,w1,w2,val_lbl)
        test_data = [ones(size(test_data,1),1), test_data];
        hidden_Layer = test_data*(transpose(w1));
        hid_out=double(1./(1.0+exp(-1*hidden_Layer)));
        
        test_bias = ones(size(hid_out,1),1);
        b = [test_bias hid_out];
        
        output_Layer_prod = b*(transpose(w2));
        out_Prod_test=double(1./(1.0+exp(-1*output_Layer_prod)));
        
        predLbl_test=[];
        
        success = 0;
        for e=1:size(test_data,1)
            class=out_Prod_test(e,:);
            lbl_class = find(class==(max(max(class))));
            if val_lbl(e,lbl_class) == 1
                success = success + 1;
            end
        end
        testaccuracy = (success/size(val_lbl,1))*100;
        dlmwrite('classes_nn.txt', out_Prod_test, ' ');        
end