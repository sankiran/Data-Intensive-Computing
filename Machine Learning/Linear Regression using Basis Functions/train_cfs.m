function [w,phi,variance,M] = train_cfs(X,tgt)
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
w = pinv(lambda*eye(length(phi'*phi))+phi'*phi)*phi'*tgt;%pinv(lambda*eye(length(transpose(dgn)*dgn))+transpose(dgn)*dgn)*transpose(dgn)*tgt;
temperr = transpose(w)*transpose(phi)-transpose(tgt);
err = sqrt((temperr*temperr')/length(tgt));
%err2=validation(w,tgt,phi);
%err3=testing(w,tgt,phi);
fprintf('the model complexity M cfs is %d\n', length(M));
fprintf('the regularization parameters lambda cfs is %4.2f\n',lambda);
fprintf('the root mean square error for the closed form solution is %4.2f\n',err);
%fprintf('the root mean square error for the linear regression model validation is is %f\n',err2);
%fprintf('the root mean square error for the linear regression model testing is is %f\n',err3);
%h = histogram(X);
%P = [3,5,7,9,10,12,13,15,18,20,22,25];
%S = [0.548892,0.548549,0.548077,0.547992,0.548174,0.547875,0.547756,0.547751,0.542,0.547715,0.547665,0.547769];
%T = [0.534075,0.533688,0.533235,0.533100,0.533362,0.533072,0.533180,0.532835,0.532471,0.532760,0.532618,0.532999];
%U = [0.617872,0.617440,0.616943,0.616938,0.616972,0.616722,0.616545,0.616607,0.616597,0.616899,0.616773,0.616680];
%plot(P,S,'b',P,T,'-g',P,U,'o');
%plot(P,S);
%lambdaforplot = [100,150,200,250,300,350,400,450,500,550,600];
%Ermsforplot = [0.5481,0.5477,0.5473,0.5470,0.5473,0.5476,0.5479,0.5483,0.5486,0.5489,0.5491];
%plot(lambdaforplot,Ermsforplot);

