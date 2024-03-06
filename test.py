import matplotlib.pyplot as plt

input_values = [1,2,3,4,5]
square=[1,4,9,16,25]

fig,ax = plt.subplots()
ax.plot(input_values, square,linewidth = 3)

ax.set_title("Square Numbers", fontsize = 24)
ax.set_xlabel("value", fontsize = 24)
ax.set_ylabel("Square of Value", fontsize = 24)

ax.tick_params(labelsize = 14)
plt.show()