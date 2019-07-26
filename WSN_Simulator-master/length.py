import matplotlib.pyplot as plt

with open("length.txt", 'r') as f:
    lengthu = f.read()
    lengthu = lengthu.split()
    lengthu = [int(i) for i in lengthu]

plt.plot(lengthu)
plt.title("Number of nodes alive with iteration")
plt.xlabel("Number of iterations")
plt.ylabel("Number of nodes alive")

plt.show()
