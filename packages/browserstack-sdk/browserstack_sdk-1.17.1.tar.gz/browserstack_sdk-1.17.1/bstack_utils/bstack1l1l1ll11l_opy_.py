# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack11l1ll_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1_opy_ (bstack111ll_opy_):
    global bstack1l1l1l1_opy_
    bstackl_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l1_opy_ = bstack111ll_opy_ [:-1]
    bstack1l1ll1_opy_ = bstackl_opy_ % len (bstack1l1_opy_)
    bstack1ll111_opy_ = bstack1l1_opy_ [:bstack1l1ll1_opy_] + bstack1l1_opy_ [bstack1l1ll1_opy_:]
    if bstack1l11111_opy_:
        bstack111ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1ll_opy_ - (bstack111l1_opy_ + bstackl_opy_) % bstack11l11ll_opy_) for bstack111l1_opy_, char in enumerate (bstack1ll111_opy_)])
    else:
        bstack111ll1_opy_ = str () .join ([chr (ord (char) - bstack11l1ll_opy_ - (bstack111l1_opy_ + bstackl_opy_) % bstack11l11ll_opy_) for bstack111l1_opy_, char in enumerate (bstack1ll111_opy_)])
    return eval (bstack111ll1_opy_)
import threading
bstack1l1l1l11ll_opy_ = 10
bstack1l1l1lll1l_opy_ = 5
bstack1l1l1l1l1l_opy_ = 30
bstack1l1l1ll1l1_opy_ = 2
class bstack1l1l1l1l11_opy_:
    def __init__(self, handler, bstack1l1l1l1ll1_opy_=bstack1l1l1l11ll_opy_, bstack1l1l1ll1ll_opy_=bstack1l1l1lll1l_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1l1l1l1ll1_opy_ = bstack1l1l1l1ll1_opy_
        self.bstack1l1l1ll1ll_opy_ = bstack1l1l1ll1ll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1l1l1l1lll_opy_()
    def bstack1l1l1l1lll_opy_(self):
        self.timer = threading.Timer(self.bstack1l1l1ll1ll_opy_, self.bstack1l1l1ll111_opy_)
        self.timer.start()
    def bstack1l1l1lll11_opy_(self):
        self.timer.cancel()
    def bstack1l1l1l11l1_opy_(self):
        self.bstack1l1l1lll11_opy_()
        self.bstack1l1l1l1lll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1l1l1l1ll1_opy_:
                t = threading.Thread(target=self.bstack1l1l1ll111_opy_)
                t.start()
                self.bstack1l1l1l11l1_opy_()
    def bstack1l1l1ll111_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1l1l1l1ll1_opy_]
        del self.queue[:self.bstack1l1l1l1ll1_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1l1l1lll11_opy_()
        while len(self.queue) > 0:
            self.bstack1l1l1ll111_opy_()