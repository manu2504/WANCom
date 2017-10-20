figure

subplot(4,5,1)
x = [23 24 25];
y = [19 1 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Ireland - Tokyo')

subplot(4,5,2)
x = [25 26 28];
y = [24 1 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Ireland - Oregon')

subplot(4,5,3)
x = [20 21 22 24];
y = [38 2 1 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Ireland - Seoul')

subplot(4,5,4)
x = [22 23 24];
y = [29 37 2];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Ireland - N.Virginia')

subplot(4,5,5)
x = [25 26 27];
y = [43 624 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Tokyo - Ireland')

subplot(4,5,6)
x = [22 24];
y = [21 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Tokyo - Oregon')

subplot(4,5,7)
x = [15 16 17];
y = [7 3 8];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Tokyo - Seoul')

subplot(4,5,8)
x = [17 18 19];
y = [93 36 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Tokyo - N.Virginia')

subplot(4,5,9)
x = [26 27];
y = [38 26];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Oregon - Ireland')

subplot(4,5,10)
x = [21 22 23];
y = [24 2 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Oregon - Tokyo')

subplot(4,5,11)
x = [20 21 22];
y = [17 6 11];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Oregon - Seoul')

subplot(4,5,12)
x = [19 20];
y = [51 105];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Oregon - N.Virginia')

subplot(4,5,13)
x = [24 26 27 28 29 30 31];
y = [1 37 427 20 181 3 2];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Seoul - Ireland')

subplot(4,5,14)
x = [15 16 17];
y = [18 2 6];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Seoul - Tokyo')

subplot(4,5,15)
x = [23 24 25];
y = [11 1 2];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Seoul - Oregon')

subplot(4,5,16)
x = [17 18 19];
y = [13 77 2];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('Seoul - N.Virginia')

subplot(4,5,17)
x = [18 23 24 25];
y = [1 33 4 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('N.Virginia - Ireland')

subplot(4,5,18)
x = [17 20 21];
y = [1 13 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('N.Virginia - Tokyo')

subplot(4,5,19)
x = [22 24];
y = [30 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('N.Virginia - Oregon')

subplot(4,5,20)
x = [17 19];
y = [21 1];
bar(x,y,0.5)
xlabel('number of network hops')
ylabel('number of path')
title ('N.Virginia - Seoul')
