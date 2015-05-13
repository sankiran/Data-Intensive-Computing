function [wgd,phi,variance,M] = train_gd(X,tgt)
M = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18];
M = M/18;
variance = 2;
lambda = 100;
%phipart = exp(-((X-mean)*(X-mean))/(2*var*var));
phi = ones(length(X),length(M)*46+1);
for n = 1:length(X);
    for k = 1:length(M);
        for l = 1:46
            phi(n, 1+k*l) = exp(-((X(n,l) - M(k))^2)/variance);
        end
    end
end

eta = 0.0002;
wgd = zeros(length(M)*46+1,1);
for m = 1:8000
    wgd = wgd+eta*transpose(phi(m,:))*(tgt(m,:)-(transpose(wgd)*transpose(phi(m,:))));
end 
        
temperr = transpose(wgd)*transpose(phi)-transpose(tgt);
err = sqrt((temperr*temperr')/length(tgt));
fprintf('the model complexity M gd is %d\n',length(M));
fprintf('the regularization parameters lambda gd is %4.2f\n',lambda);
fprintf('the root mean square error for the gradient descent method is %4.2f\n',err);
%ermsforplot = [0.632843,0.609998,0.631387,0.643331,0.649231];
%etaforplot = [0.0001,0.0002,0.0003,0.0004,0.0005];
%plot(etaforplot,ermsforplot);
%ermsnew = [0.649231,0.651628,0.653667,0.653266,0.652321];
%Mforplot = [10,12,14,16,18];
%plot(Mforplot,ermsnew);
