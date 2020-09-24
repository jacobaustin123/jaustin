from jaustin.timers import ProgressBar

bar = ProgressBar(100,50)

for i in range(100):
    bar.step()
