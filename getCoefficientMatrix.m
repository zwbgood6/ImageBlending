function coeffA = getCoefficientMatrix(indexes)
%% Enter Your Code Here
indexesPad = padarray(indexes,[1 1],0,'both');
N = sum(sum(indexes ~= 0));
coeffA = 4 * eye(N);

for i = 1:N
    [m, n] = find(indexesPad == i); %center
    
    up = indexesPad(m-1,n); % upside of the center
    if up ~= 0
        coeffA(i ,up) = -1;
    end
    
    down = indexesPad(m+1,n); % downside of the center
    if down ~= 0
        coeffA(i ,down) = -1;
    end
    
    left = indexesPad(m,n-1); % leftside of the center
    if left ~= 0
        coeffA(i ,left) = -1;
    end
    
    right = indexesPad(m,n+1); % rightside of the center
    if right ~= 0
        coeffA(i ,right) = -1;
    end
end

end
