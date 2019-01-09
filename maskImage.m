function mask = maskImage(Img)
%% Enter Your Code Here
imshow(Img);
h = imfreehand;
mask = createMask(h);
end

