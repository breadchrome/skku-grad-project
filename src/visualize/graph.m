x = []
y = []
z = []
s = []
for i = 0:29
    T = csvread(sprintf("%s.scs/a0.s%d.csv", argv(){1}, i))
    x = [x; T(:,1)]
    y = [y; T(:,2)]
    z = [z; T(:,3)]
    s = [s; ones(size(T)(1,1), 1) * i]
end
scatter3(x, y, z, 10, s, "filled")
input("Paused...")