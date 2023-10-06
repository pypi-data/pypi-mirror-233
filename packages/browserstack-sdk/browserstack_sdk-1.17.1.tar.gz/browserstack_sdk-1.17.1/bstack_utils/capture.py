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
import sys
class bstack1ll11l1lll_opy_:
    def __init__(self, handler):
        self._1ll11l1l11_opy_ = sys.stdout.write
        self._1ll11l1l1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack1ll11l1ll1_opy_
        sys.stdout.error = self.bstack1ll11ll111_opy_
    def bstack1ll11l1ll1_opy_(self, _str):
        self._1ll11l1l11_opy_(_str)
        if self.handler:
            self.handler({bstack1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫೊ"): bstack1_opy_ (u"࠭ࡉࡏࡈࡒࠫೋ"), bstack1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨೌ"): _str})
    def bstack1ll11ll111_opy_(self, _str):
        self._1ll11l1l1l_opy_(_str)
        if self.handler:
            self.handler({bstack1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲ್ࠧ"): bstack1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ೎"), bstack1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ೏"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._1ll11l1l11_opy_
        sys.stderr.write = self._1ll11l1l1l_opy_