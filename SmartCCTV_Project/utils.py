from collections import deque
import numpy as np

class TrackHistory:
    def __init__(self, maxlen=20):
        self.data = {}
        self.maxlen = maxlen

    def update(self, tid, c):
        dq = self.data.get(tid)
        if dq is None:
            dq = deque(maxlen=self.maxlen)
            self.data[tid] = dq
        dq.append(c)

    def speed(self, tid):
        dq = self.data.get(tid)
        if not dq or len(dq) < 2:
            return 0.0
        pts = np.array(dq, dtype=np.float32)
        diffs = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        return float(np.mean(diffs))
