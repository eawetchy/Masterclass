x = 0:0.1:2*pi;
P0 = [cos(x)',sin(x)']; %original points
P = size(P0)
KP0 = [P0(1,:);P0(20,:);P0(40,:);P0(50,:)]; %key points
%KP1 = KP0 + [1,0;0,0;0,0;0,0];

hold on;
axis equal;
plot(P0(:,1),P0(:,2),'-g');
plot(KP0(:,1),KP0(:,2),'xr');

H = zeros(size(P0,1),size(KP0,1)); %number of original points (rows) x number of keypoints (columns)
for i=1:size(P0,1)
    for j=1:size(KP0,1)
        H(i,j)=rbfbasis(norm(P0(i,:)-KP0(j,:)));%evaluate all points' distances to key points
    end
end

% Solve for the weights w_i
w = inv(H'*H)*H'*P0;%"fake" inverse because matrix isn't square


% This is flawed! You need to replace P0 with the points in the target
% model
P1 = rbfeval(KP1, w, P0);

plot(P1(:,1),P1(:,2),'-r');
plot(KP1(:,1),KP1(:,2),'ob');
hold off;

