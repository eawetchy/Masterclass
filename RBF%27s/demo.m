x = 0:0.1:2*pi;
x2 = 0:0.05:2*pi;
kpidx = [1,20,25,30,38,40,45,50,55];
kpidx2 = 2*kpidx;
% Create a perturbation which modifies the radius in each timestep
perturb = repmat([1.01;0.99], (size(x,2)+1)/2, 2);
perturb = perturb(1:size(x,2),:);
P0 = perturb .* [cos(x)',sin(x)'];
P1 = [cos(x2)',0.5*sin(x2)'];


% The key points
KP0 = P0(kpidx,:);
KP1 = P1(kpidx2,:);

% Perturbed keypoints

% Plot the data
hold on;
axis equal;
plot(P0(:,1),P0(:,2),'-g');
plot(KP0(:,1),KP0(:,2),'xg');
plot(KP1(:,1),KP1(:,2),'xb');

% Fill up the matrix H with the RBF data
%H = zeros(size(P0,1),size(KP0,1));
%for i=1:size(P0,1)
%    for j=1:size(KP0,1)
 %       H(i,j)=rbfbasis(norm(P0(i,:)-KP0(j,:)));
 %   end
%end

H = zeros(size(KP1,1));
for i=1:size(KP1,1)
 for j=1:size(KP1,1)
  H(i,j)=rbfbasis(norm(KP0(i,:)-KP0(j,:)));
 end
end

% Solve for the weights w_i
w = inv(H'*H)*H'*KP1;
 
% I think this deformation is actually correct
P2 = rbfeval(KP0, w, P0);

% plot the resulting reconstruction
plot(P2(:,1),P2(:,2),'-r');
plot(KP1(:,1),KP1(:,2),'or');
hold off;
