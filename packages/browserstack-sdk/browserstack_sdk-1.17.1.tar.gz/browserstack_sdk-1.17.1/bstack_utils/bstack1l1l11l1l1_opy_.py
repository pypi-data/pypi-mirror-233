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
import json
import os
from bstack_utils.helper import bstack1l1ll1ll11_opy_, bstack1l1lll1l_opy_, bstack11lll1ll_opy_, \
    bstack1l1lllll1l_opy_
def bstack1lll1l1l1l_opy_(bstack1l1l11l1ll_opy_):
    for driver in bstack1l1l11l1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll1ll_opy_(type, name, status, reason, bstack1lllll1l11_opy_, bstack1l11l11l1_opy_):
    bstack1111l1ll_opy_ = {
        bstack1_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ၂"): type,
        bstack1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ၃"): {}
    }
    if type == bstack1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨ၄"):
        bstack1111l1ll_opy_[bstack1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ၅")][bstack1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ၆")] = bstack1lllll1l11_opy_
        bstack1111l1ll_opy_[bstack1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ၇")][bstack1_opy_ (u"ࠪࡨࡦࡺࡡࠨ၈")] = json.dumps(str(bstack1l11l11l1_opy_))
    if type == bstack1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ၉"):
        bstack1111l1ll_opy_[bstack1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ၊")][bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ။")] = name
    if type == bstack1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪ၌"):
        bstack1111l1ll_opy_[bstack1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ၍")][bstack1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ၎")] = status
        if status == bstack1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ၏"):
            bstack1111l1ll_opy_[bstack1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧၐ")][bstack1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬၑ")] = json.dumps(str(reason))
    bstack11l11ll1_opy_ = bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫၒ").format(json.dumps(bstack1111l1ll_opy_))
    return bstack11l11ll1_opy_
def bstack1llllll1ll_opy_(url, config, logger, bstack1lll111l1_opy_=False):
    hostname = bstack1l1lll1l_opy_(url)
    is_private = bstack11lll1ll_opy_(hostname)
    try:
        if is_private or bstack1lll111l1_opy_:
            file_path = bstack1l1ll1ll11_opy_(bstack1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧၓ"), bstack1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧၔ"), logger)
            if os.environ.get(bstack1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧၕ")) and eval(
                    os.environ.get(bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨၖ"))):
                return
            if (bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨၗ") in config and not config[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩၘ")]):
                os.environ[bstack1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫၙ")] = str(True)
                bstack1l1l11l11l_opy_ = {bstack1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩၚ"): hostname}
                bstack1l1lllll1l_opy_(bstack1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧၛ"), bstack1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧၜ"), bstack1l1l11l11l_opy_, logger)
    except Exception as e:
        pass
def bstack11ll1l11l_opy_(caps, bstack1l1l11l111_opy_):
    if bstack1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫၝ") in caps:
        caps[bstack1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬၞ")][bstack1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫၟ")] = True
        if bstack1l1l11l111_opy_:
            caps[bstack1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧၠ")][bstack1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩၡ")] = bstack1l1l11l111_opy_
    else:
        caps[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ၢ")] = True
        if bstack1l1l11l111_opy_:
            caps[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪၣ")] = bstack1l1l11l111_opy_