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
import multiprocessing
import os
from browserstack_sdk.bstack1llll11ll_opy_ import *
from bstack_utils.helper import bstack11l111ll1_opy_
from bstack_utils.messages import bstack1lll111l_opy_
from bstack_utils.constants import bstack111l1l1l1_opy_
class bstack1lll1l1lll_opy_:
    def __init__(self, args, logger, bstack1ll1l111ll_opy_, bstack1ll11ll1l1_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1l111ll_opy_ = bstack1ll1l111ll_opy_
        self.bstack1ll11ll1l1_opy_ = bstack1ll11ll1l1_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1111l1_opy_ = []
        self.bstack1ll11ll11l_opy_ = None
        self.bstack1l1111l1l_opy_ = []
        self.bstack1ll11lll1l_opy_ = self.bstack1111l1lll_opy_()
        self.bstack111l1ll1l_opy_ = -1
    def bstack1lll1llll1_opy_(self, bstack1ll1l111l1_opy_):
        self.parse_args()
        self.bstack1ll11ll1ll_opy_()
        self.bstack1ll1l11l11_opy_(bstack1ll1l111l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1ll11lll11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111l1ll1l_opy_ = -1
        if bstack1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧಷ") in self.bstack1ll1l111ll_opy_:
            self.bstack111l1ll1l_opy_ = self.bstack1ll1l111ll_opy_[bstack1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಸ")]
        try:
            bstack1ll1l11111_opy_ = [bstack1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫಹ"), bstack1_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭಺"), bstack1_opy_ (u"ࠫ࠲ࡶࠧ಻")]
            if self.bstack111l1ll1l_opy_ >= 0:
                bstack1ll1l11111_opy_.extend([bstack1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ಼࠭"), bstack1_opy_ (u"࠭࠭࡯ࠩಽ")])
            for arg in bstack1ll1l11111_opy_:
                self.bstack1ll11lll11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11ll1ll_opy_(self):
        bstack1ll11ll11l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
        return bstack1ll11ll11l_opy_
    def bstack1lll111111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1ll11lllll_opy_ = importlib.find_loader(bstack1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩಾ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1lll111l_opy_)
    def bstack1ll1l11l11_opy_(self, bstack1ll1l111l1_opy_):
        if bstack1ll1l111l1_opy_:
            self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠨ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬಿ"))
            self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠩࡗࡶࡺ࡫ࠧೀ"))
        self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠪ࠱ࡵ࠭ು"))
        self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠩೂ"))
        self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧೃ"))
        self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ೄ"))
        if self.bstack111l1ll1l_opy_ > 1:
            self.bstack1ll11ll11l_opy_.append(bstack1_opy_ (u"ࠧ࠮ࡰࠪ೅"))
            self.bstack1ll11ll11l_opy_.append(str(self.bstack111l1ll1l_opy_))
    def bstack1ll11llll1_opy_(self):
        bstack1l1111l1l_opy_ = []
        for spec in self.bstack11l1111l1_opy_:
            bstack1l1l11l11_opy_ = [spec]
            bstack1l1l11l11_opy_ += self.bstack1ll11ll11l_opy_
            bstack1l1111l1l_opy_.append(bstack1l1l11l11_opy_)
        self.bstack1l1111l1l_opy_ = bstack1l1111l1l_opy_
        return bstack1l1111l1l_opy_
    def bstack1111l1lll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11lll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11lll1l_opy_ = False
        return self.bstack1ll11lll1l_opy_
    def bstack11lllll1l_opy_(self, bstack1ll1l1111l_opy_, bstack1lll1llll1_opy_):
        bstack1lll1llll1_opy_[bstack1_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨೆ")] = self.bstack1ll1l111ll_opy_
        if bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬೇ") in self.bstack1ll1l111ll_opy_:
            bstack1111l1l11_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lllllll1_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1ll1l111ll_opy_[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ೈ")]):
                bstack1111l1l11_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1ll1l1111l_opy_,
                                                           args=(self.bstack1ll11ll11l_opy_, bstack1lll1llll1_opy_)))
            i = 0
            for t in bstack1111l1l11_opy_:
                os.environ[bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ೉")] = str(i)
                i += 1
                t.start()
            for t in bstack1111l1l11_opy_:
                t.join()
            return bstack1lllllll1_opy_