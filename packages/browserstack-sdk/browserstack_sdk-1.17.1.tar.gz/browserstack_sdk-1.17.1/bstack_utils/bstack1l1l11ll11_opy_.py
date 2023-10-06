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
class bstack1l1l1l111l_opy_:
    def __init__(self, handler):
        self._1l1l11lll1_opy_ = None
        self.handler = handler
        self._1l1l11ll1l_opy_ = self.bstack1l1l11llll_opy_()
        self.patch()
    def patch(self):
        self._1l1l11lll1_opy_ = self._1l1l11ll1l_opy_.execute
        self._1l1l11ll1l_opy_.execute = self.bstack1l1l1l1111_opy_()
    def bstack1l1l1l1111_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            response = self._1l1l11lll1_opy_(this, driver_command, *args, **kwargs)
            self.handler(driver_command, response)
            return response
        return execute
    def reset(self):
        self._1l1l11ll1l_opy_.execute = self._1l1l11lll1_opy_
    @staticmethod
    def bstack1l1l11llll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver