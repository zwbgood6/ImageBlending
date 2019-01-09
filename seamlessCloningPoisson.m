function resultImg = seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY)
%% Enter Your Code Here
% get the H and W
targetH = size(targetImg,1);
targetW = size(targetImg,2);
% color from source image
source_red = sourceImg(:,:,1);
source_green = sourceImg(:,:,2);
source_blue = sourceImg(:,:,3);
% color from target image
target_red = targetImg(:,:,1);
target_green = targetImg(:,:,2);
target_blue = targetImg(:,:,3);
% get index
indexes = getIndexes(mask, targetH, targetW, offsetX, offsetY);
% get three channel solution vectors b
solVectorb_red = getSolutionVect(indexes, source_red, target_red, offsetX, offsetY); % get b_red
solVectorb_green = getSolutionVect(indexes, source_green, target_green, offsetX, offsetY); % get b_green
solVectorb_blue = getSolutionVect(indexes, source_blue, target_blue, offsetX, offsetY); % get b_blue
% get A
coeffA = getCoefficientMatrix(indexes); 
% get f (Af = b)
f_red = solVectorb_red/coeffA;
f_green = solVectorb_green/coeffA;
f_blue = solVectorb_blue/coeffA;
% get the result image
resultImg = reconstructImg(indexes, f_red, f_green, f_blue, targetImg);

end