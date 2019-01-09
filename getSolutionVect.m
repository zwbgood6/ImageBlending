function solVectorb = getSolutionVect(indexes, source, target, offsetX, offsetY)
%% Enter Your Code Here
N = sum(sum(indexes ~= 0));
solVectorb = zeros(1,N);
% Pad zero with the initial one
source = padarray(source, [1,1], 0, 'both');
target = padarray(target, [1,1], 0, 'both');
indexesPad = padarray(indexes, [1,1], 0, 'both');
% define initial value of upside, downside, leftside, and rightside of the
% centered pixel
up = 0;
down = 0;
left = 0;
right = 0;
for i = 1:N
    [m,n] = find(indexesPad == i);
    if indexesPad(m-1, n) == 0
        up = target(m-1,n);
    end
    if indexesPad(m+1, n) == 0
        down = target(m+1,n);
    end
    if indexesPad(m, n-1) == 0
        left = target(m,n-1);
    end
    if indexesPad(m, n+1) == 0
        right = target(m, n+1);
    end
    m1 = m-offsetY;
    n1 = n-offsetX;
    solVectorb(i) = 4*source(m1,n1)-source(m1-1,n1)-source(m1+1,n1)-source(m1,n1-1)-source(m1, n1+1)+up+down+left+right;
    up = 0;
    down = 0;
    left = 0;
    right = 0;
end
end
