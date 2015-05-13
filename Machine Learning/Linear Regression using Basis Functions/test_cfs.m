function [Erms] = test_cfs(phi,tgt,w_gd)
MatrixX=phi(62660:69623,:);
MatrixY=tgt(62660:69623,:);
predicttgt=w_gd'*MatrixX';
error=predicttgt-MatrixY';
temp=error*error';
Errmean=temp/length(MatrixY);
Erms=sqrt(Errmean);
end