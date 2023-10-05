# coding: UTF-8
import sys
bstack1lllll1_opy_ = sys.version_info [0] == 2
bstack1l1111_opy_ = 2048
bstack1ll1111_opy_ = 7
def bstack1111ll1_opy_ (bstack11l1lll_opy_):
    global bstack11lll1l_opy_
    bstack111l1ll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l1ll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1ll_opy_)
    bstack1l1_opy_ = bstack1l1l1ll_opy_ [:bstack11ll1l1_opy_] + bstack1l1l1ll_opy_ [bstack11ll1l1_opy_:]
    if bstack1lllll1_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1111_opy_ - (bstack1111ll_opy_ + bstack111l1ll_opy_) % bstack1ll1111_opy_) for bstack1111ll_opy_, char in enumerate (bstack1l1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1l1111_opy_ - (bstack1111ll_opy_ + bstack111l1ll_opy_) % bstack1ll1111_opy_) for bstack1111ll_opy_, char in enumerate (bstack1l1_opy_)])
    return eval (bstack111ll11_opy_)
import sys
class bstack1ll11l1ll1_opy_:
    def __init__(self, handler):
        self._1ll11l1lll_opy_ = sys.stdout.write
        self._1ll11l1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1ll11l1l11_opy_
        sys.stdout.error = self.bstack1ll11ll111_opy_
    def bstack1ll11l1l11_opy_(self, _str):
        self._1ll11l1lll_opy_(_str)
        if self.handler:
            self.handler({bstack1111ll1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ೌ"): bstack1111ll1_opy_ (u"ࠨࡋࡑࡊࡔ್࠭"), bstack1111ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ೎"): _str})
    def bstack1ll11ll111_opy_(self, _str):
        self._1ll11l1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1111ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ೏"): bstack1111ll1_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ೐"), bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭೑"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1ll11l1lll_opy_
        sys.stderr.write = self._1ll11l1l1l_opy_