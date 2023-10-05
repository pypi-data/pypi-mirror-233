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
conf = {
    bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ೒"): False,
    bstack1111ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ೓"): True,
}
class Config(object):
    instance = None
    def __init__(self):
        self._1ll11l11ll_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._1ll11l11ll_opy_.get(property_name, None)
    def bstack1lllll1ll1_opy_(self, property_name, bstack1ll11l11l1_opy_):
        self._1ll11l11ll_opy_[property_name] = bstack1ll11l11l1_opy_