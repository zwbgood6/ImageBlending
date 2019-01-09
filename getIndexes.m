function indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY)
%% Enter Your Code Here
indexes = zeros(targetH,targetW);
sourceH = size(mask,1);
sourceW = size(mask,2);
p = 1; % count the number
for i = 1+offsetY:sourceH+offsetY
    for j = 1+offsetX:sourceW+offsetX
        if mask(i-offsetY,j-offsetX) ~= 0
            indexes(i,j) = p;
            p = p + 1;
        end        
    end
end
end