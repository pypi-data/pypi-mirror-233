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
import multiprocessing
import os
from browserstack_sdk.bstack111l11l1_opy_ import *
from bstack_utils.helper import bstack11l1l11ll_opy_
from bstack_utils.messages import bstack1llllll11_opy_
from bstack_utils.constants import bstack1ll1ll11ll_opy_
class bstack11l1l1lll_opy_:
    def __init__(self, args, logger, bstack1ll1l1111l_opy_, bstack1ll1l11l11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1ll1l1111l_opy_ = bstack1ll1l1111l_opy_
        self.bstack1ll1l11l11_opy_ = bstack1ll1l11l11_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111lll11_opy_ = []
        self.bstack1ll1l11111_opy_ = None
        self.bstack1llll111ll_opy_ = []
        self.bstack1ll11lll1l_opy_ = self.bstack1l1111l11_opy_()
        self.bstack1111l1lll_opy_ = -1
    def bstack1l111l11_opy_(self, bstack1ll1l111l1_opy_):
        self.parse_args()
        self.bstack1ll11ll1l1_opy_()
        self.bstack1ll11lll11_opy_(bstack1ll1l111l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1ll11llll1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1111l1lll_opy_ = -1
        if bstack1111ll1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧಷ") in self.bstack1ll1l1111l_opy_:
            self.bstack1111l1lll_opy_ = self.bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಸ")]
        try:
            bstack1ll11ll11l_opy_ = [bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫಹ"), bstack1111ll1_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭಺"), bstack1111ll1_opy_ (u"ࠫ࠲ࡶࠧ಻")]
            if self.bstack1111l1lll_opy_ >= 0:
                bstack1ll11ll11l_opy_.extend([bstack1111ll1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ಼࠭"), bstack1111ll1_opy_ (u"࠭࠭࡯ࠩಽ")])
            for arg in bstack1ll11ll11l_opy_:
                self.bstack1ll11llll1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack1ll11ll1l1_opy_(self):
        bstack1ll1l11111_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1ll1l11111_opy_ = bstack1ll1l11111_opy_
        return bstack1ll1l11111_opy_
    def bstack11lll1111_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack1ll11ll1ll_opy_ = importlib.find_loader(bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩಾ"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llllll11_opy_)
    def bstack1ll11lll11_opy_(self, bstack1ll1l111l1_opy_):
        if bstack1111ll1_opy_ (u"ࠨ࠯࠰ࡧࡦࡩࡨࡦ࠯ࡦࡰࡪࡧࡲࠨಿ") not in self.bstack1ll1l11111_opy_:
            self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠩ࠰࠱ࡨࡧࡣࡩࡧ࠰ࡧࡱ࡫ࡡࡳࠩೀ"))
        if bstack1ll1l111l1_opy_:
            self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧು"))
            self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"࡙ࠫࡸࡵࡦࠩೂ"))
        self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠬ࠳ࡰࠨೃ"))
        self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠫೄ"))
        self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠧ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠩ೅"))
        self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨೆ"))
        if self.bstack1111l1lll_opy_ >= 0:
            self.bstack1ll1l11111_opy_.append(bstack1111ll1_opy_ (u"ࠩ࠰ࡲࠬೇ"))
            self.bstack1ll1l11111_opy_.append(str(self.bstack1111l1lll_opy_))
    def bstack1ll1l111ll_opy_(self):
        bstack1llll111ll_opy_ = []
        for spec in self.bstack111lll11_opy_:
            bstack1l1lllll_opy_ = [spec]
            bstack1l1lllll_opy_ += self.bstack1ll1l11111_opy_
            bstack1llll111ll_opy_.append(bstack1l1lllll_opy_)
        self.bstack1llll111ll_opy_ = bstack1llll111ll_opy_
        return bstack1llll111ll_opy_
    def bstack1l1111l11_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack1ll11lll1l_opy_ = True
            return True
        except Exception as e:
            self.bstack1ll11lll1l_opy_ = False
        return self.bstack1ll11lll1l_opy_
    def bstack111l1l1ll_opy_(self, bstack1ll11lllll_opy_, bstack1l111l11_opy_):
        bstack1l111l11_opy_[bstack1111ll1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪೈ")] = self.bstack1ll1l1111l_opy_
        if bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೉") in self.bstack1ll1l1111l_opy_:
            bstack1lllll111l_opy_ = []
            manager = multiprocessing.Manager()
            bstack1lll11l11_opy_ = manager.list()
            for index, platform in enumerate(self.bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨೊ")]):
                bstack1lllll111l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1ll11lllll_opy_,
                                                           args=(self.bstack1ll1l11111_opy_, bstack1l111l11_opy_)))
            i = 0
            for t in bstack1lllll111l_opy_:
                os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ೋ")] = str(i)
                i += 1
                t.start()
            for t in bstack1lllll111l_opy_:
                t.join()
            return bstack1lll11l11_opy_