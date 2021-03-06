function [ P ] = rbfeval( C, W, P0 )
%RBFEVAL Summary of this function goes here
%   Detailed explanation goes here

  % array of output points
  P = zeros(size(P0));

  % h will contain the radial basis function evaluated at each point
  h = zeros(size(W,1),1);
  
  for i=1:size(P,1)
    for j=1:size(C,1)
       h(j) = rbfbasis(norm(P0(i,:) - C(j,:)));
    end
    % reconstruct point i
    P(i,:) = W' * h;
  end 
end

