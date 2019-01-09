function resultImg = reconstructImg(indexes, red, green, blue, targetImg)
%% Enter Your Code Here
N = sum(sum(indexes ~= 0));
target_red = targetImg(:,:,1);
target_green = targetImg(:,:,2);
target_blue = targetImg(:,:,3);
%red = red';
%green = green';
%blue = blue';
for i = 1:N
    [m, n] = find(indexes == i);
    target_red(m,n) = red(i);
    target_green(m,n) = green(i);
    target_blue(m,n) = blue(i);
end
resultImg = cat(3,target_red,target_green,target_blue);
end