% read the images
sourceImg = im2double(imread('SourceImage.png'));
targetImg = im2double(imread('TargetImage.png'));
% get the mask logical value
mask = maskImage(sourceImg);
% input offsetX and offsetY
offsetX = input('Please imput the offsetX');
offsetY = input('Please imput the offsetY');
resultImg = seamlessCloningPoisson(sourceImg, targetImg, mask, offsetX, offsetY);
imshow(resultImg);