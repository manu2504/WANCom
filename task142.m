a = [15 25
    16 5
    17 142
    18 114
    19 55
    20 173
    21 33
    22 94
    23 101
    24 12
    25 71
    26 700
    27 454
    28 21
    29 181
    30 3
    31 2];

b=[];
for i=1:length(a(:,1))
    b=[b;a(i,1).*ones(a(i,2),1)];
end
cdfplot(b)

xlabel('hop distances')
ylabel('CDF')
title('CDF of hop distances among all pairs of source and destination datacenters')

