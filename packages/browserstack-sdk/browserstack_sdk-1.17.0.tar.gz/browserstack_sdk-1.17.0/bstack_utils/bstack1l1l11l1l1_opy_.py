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
import json
import os
from bstack_utils.helper import bstack1l1lll11l1_opy_, bstack11l11l11l_opy_, bstack1l1l111l1_opy_, \
    bstack1l1llll1ll_opy_
def bstack11lll1l1l_opy_(bstack1l1l11l1ll_opy_):
    for driver in bstack1l1l11l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l1l11ll_opy_(type, name, status, reason, bstack1ll1l1ll_opy_, bstack1ll1llll1l_opy_):
    bstack1l1l1ll1_opy_ = {
        bstack1111ll1_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬ၃"): type,
        bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ၄"): {}
    }
    if type == bstack1111ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ၅"):
        bstack1l1l1ll1_opy_[bstack1111ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ၆")][bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ၇")] = bstack1ll1l1ll_opy_
        bstack1l1l1ll1_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭၈")][bstack1111ll1_opy_ (u"ࠫࡩࡧࡴࡢࠩ၉")] = json.dumps(str(bstack1ll1llll1l_opy_))
    if type == bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭၊"):
        bstack1l1l1ll1_opy_[bstack1111ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ။")][bstack1111ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ၌")] = name
    if type == bstack1111ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ၍"):
        bstack1l1l1ll1_opy_[bstack1111ll1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ၎")][bstack1111ll1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ၏")] = status
        if status == bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫၐ"):
            bstack1l1l1ll1_opy_[bstack1111ll1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨၑ")][bstack1111ll1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ၒ")] = json.dumps(str(reason))
    bstack1l1lllll1_opy_ = bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬၓ").format(json.dumps(bstack1l1l1ll1_opy_))
    return bstack1l1lllll1_opy_
def bstack1ll1ll1l_opy_(url, config, logger, bstack1111111l_opy_=False):
    hostname = bstack11l11l11l_opy_(url)
    is_private = bstack1l1l111l1_opy_(hostname)
    try:
        if is_private or bstack1111111l_opy_:
            file_path = bstack1l1lll11l1_opy_(bstack1111ll1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨၔ"), bstack1111ll1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨၕ"), logger)
            if os.environ.get(bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨၖ")) and eval(
                    os.environ.get(bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩၗ"))):
                return
            if (bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩၘ") in config and not config[bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪၙ")]):
                os.environ[bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬၚ")] = str(True)
                bstack1l1l11l111_opy_ = {bstack1111ll1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪၛ"): hostname}
                bstack1l1llll1ll_opy_(bstack1111ll1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨၜ"), bstack1111ll1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨၝ"), bstack1l1l11l111_opy_, logger)
    except Exception as e:
        pass
def bstack1l11llll1_opy_(caps, bstack1l1l11l11l_opy_):
    if bstack1111ll1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬၞ") in caps:
        caps[bstack1111ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ၟ")][bstack1111ll1_opy_ (u"࠭࡬ࡰࡥࡤࡰࠬၠ")] = True
        if bstack1l1l11l11l_opy_:
            caps[bstack1111ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨၡ")][bstack1111ll1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪၢ")] = bstack1l1l11l11l_opy_
    else:
        caps[bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧၣ")] = True
        if bstack1l1l11l11l_opy_:
            caps[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫၤ")] = bstack1l1l11l11l_opy_