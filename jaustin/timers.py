import time
import math

# MIT License
# https://github.com/chrischoy/SpatioTemporalSegmentation/blob/master/lib/utils.py
class Timer(object):
    """A simple timer."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.total_time = 0
        self.calls = 0
        self.start_time = 0
        self.diff = 0
        self.average_time = 0

    def tic(self):
        self.start_time = time.time()

    def toc(self, average=True):
        self.diff = time.time() - self.start_time
        self.total_time += self.diff
        self.calls += 1
        self.average_time = self.total_time / self.calls

        return self.average_time if average else self.diff

    @property
    def avg(self):
        return self.average_time

    def __repr__(self):
        return f"Timer(average time: {self.avg})"

# MIT License
# https://github.com/chrischoy/SpatioTemporalSegmentation/blob/master/lib/utils.py
class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def stats(self):
        return {
            'avg' : self.avg,
            'count' : self.count,
            'val' : self.val,
        }

    def __repr__(self):
        return f"AverageMeter(avg: {self.avg}, count: {self.count})"


# https://github.com/mlb2251/mlb
class ProgressBar:
    def __init__(self, num_steps, num_dots=10):
        self.num_steps = num_steps
        self.num_dots = num_dots
        self.curr_step = 0
        self.dots_printed = 0

    def step(self):
        expected_dots = math.ceil(self.curr_step / self.num_steps * self.num_dots)
        dots_to_print = expected_dots - self.dots_printed
        if dots_to_print > 0:
            print('.'*dots_to_print, end='', flush=True)
        self.dots_printed = expected_dots
        self.curr_step += 1
        if self.curr_step == self.num_steps:
            print('!\n', end='', flush=True)
