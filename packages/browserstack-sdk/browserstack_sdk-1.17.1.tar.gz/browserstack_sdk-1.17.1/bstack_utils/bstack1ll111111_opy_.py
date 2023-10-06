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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack1l1lll1111_opy_, bstack1ll111l11l_opy_, get_host_info, bstack1l1lllll11_opy_, bstack1l1llllll1_opy_, bstack1l1lll11l1_opy_, \
    bstack1l1llll11l_opy_, bstack1ll111111l_opy_, bstack1lll11ll1_opy_, bstack1ll1111ll1_opy_, bstack1l1llll1l1_opy_, bstack1ll1111111_opy_
from bstack_utils.bstack1l1l1ll11l_opy_ import bstack1l1l1l1l11_opy_
bstack1l11ll1l11_opy_ = [
    bstack1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧၤ"), bstack1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨၥ"), bstack1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧၦ"), bstack1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧၧ"),
    bstack1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩၨ"), bstack1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩၩ"), bstack1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪၪ")
]
bstack1l11l1l1ll_opy_ = bstack1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪၫ")
logger = logging.getLogger(__name__)
class bstack1l111l1ll_opy_:
    bstack1l1l1ll11l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11l1ll1l_opy_):
        cls.bs_config = bs_config
        if not cls.bstack1l11l1ll11_opy_():
            return
        cls.bstack1l1l1ll11l_opy_ = bstack1l1l1l1l11_opy_(cls.bstack1l11lll1ll_opy_)
        cls.bstack1l1l1ll11l_opy_.start()
        bstack1l11l1l11l_opy_ = bstack1l1lllll11_opy_(bs_config)
        bstack1l1l1111ll_opy_ = bstack1l1llllll1_opy_(bs_config)
        data = {
            bstack1_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫၬ"): bstack1_opy_ (u"ࠬࡰࡳࡰࡰࠪၭ"),
            bstack1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬၮ"): bs_config.get(bstack1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬၯ"), bstack1_opy_ (u"ࠨࠩၰ")),
            bstack1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧၱ"): bs_config.get(bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ၲ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧၳ"): bs_config.get(bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧၴ")),
            bstack1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫၵ"): bs_config.get(bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪၶ"), bstack1_opy_ (u"ࠨࠩၷ")),
            bstack1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡠࡶ࡬ࡱࡪ࠭ၸ"): datetime.datetime.now().isoformat(),
            bstack1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨၹ"): bstack1l1lll11l1_opy_(bs_config),
            bstack1_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧၺ"): get_host_info(),
            bstack1_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭ၻ"): bstack1ll111l11l_opy_(),
            bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ၼ"): os.environ.get(bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ၽ")),
            bstack1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭ၾ"): os.environ.get(bstack1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧၿ"), False),
            bstack1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬႀ"): bstack1l1lll1111_opy_(),
            bstack1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬႁ"): {
                bstack1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬႂ"): bstack1l11l1ll1l_opy_.get(bstack1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧႃ"), bstack1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧႄ")),
                bstack1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫႅ"): bstack1l11l1ll1l_opy_.get(bstack1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ႆ")),
                bstack1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧႇ"): bstack1l11l1ll1l_opy_.get(bstack1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႈ"))
            }
        }
        config = {
            bstack1_opy_ (u"ࠬࡧࡵࡵࡪࠪႉ"): (bstack1l11l1l11l_opy_, bstack1l1l1111ll_opy_),
            bstack1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧႊ"): cls.default_headers()
        }
        response = bstack1lll11ll1_opy_(bstack1_opy_ (u"ࠧࡑࡑࡖࡘࠬႋ"), cls.request_url(bstack1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳࠨႌ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨႍ")] = bstack1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩႎ")
            os.environ[bstack1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬႏ")] = bstack1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ႐")
            os.environ[bstack1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ႑")] = bstack1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ႒")
            os.environ[bstack1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ႓")] = bstack1_opy_ (u"ࠤࡱࡹࡱࡲࠢ႔")
            bstack1l11llll11_opy_ = response.json()
            if bstack1l11llll11_opy_ and bstack1l11llll11_opy_[bstack1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ႕")]:
                error_message = bstack1l11llll11_opy_[bstack1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ႖")]
                if bstack1l11llll11_opy_[bstack1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡘࡾࡶࡥࠨ႗")] == bstack1_opy_ (u"࠭ࡅࡓࡔࡒࡖࡤࡏࡎࡗࡃࡏࡍࡉࡥࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࠫ႘"):
                    logger.error(error_message)
                elif bstack1l11llll11_opy_[bstack1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࡚ࡹࡱࡧࠪ႙")] == bstack1_opy_ (u"ࠨࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠧႚ"):
                    logger.info(error_message)
                elif bstack1l11llll11_opy_[bstack1_opy_ (u"ࠩࡨࡶࡷࡵࡲࡕࡻࡳࡩࠬႛ")] == bstack1_opy_ (u"ࠪࡉࡗࡘࡏࡓࡡࡖࡈࡐࡥࡄࡆࡒࡕࡉࡈࡇࡔࡆࡆࠪႜ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll1llll_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤ࡙࡫ࡳࡵࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨႝ"))
            return [None, None, None]
        os.environ[bstack1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡅࡒࡑࡕࡒࡅࡕࡇࡇࠫ႞")] = bstack1_opy_ (u"࠭ࡴࡳࡷࡨࠫ႟")
        bstack1l11llll11_opy_ = response.json()
        if bstack1l11llll11_opy_.get(bstack1_opy_ (u"ࠧ࡫ࡹࡷࠫႠ")):
            os.environ[bstack1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩႡ")] = bstack1l11llll11_opy_[bstack1_opy_ (u"ࠩ࡭ࡻࡹ࠭Ⴂ")]
            os.environ[bstack1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧႣ")] = json.dumps({
                bstack1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭Ⴄ"): bstack1l11l1l11l_opy_,
                bstack1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧႥ"): bstack1l1l1111ll_opy_
            })
        if bstack1l11llll11_opy_.get(bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨႦ")):
            os.environ[bstack1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭Ⴇ")] = bstack1l11llll11_opy_[bstack1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪႨ")]
        if bstack1l11llll11_opy_.get(bstack1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ⴉ")):
            os.environ[bstack1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫႪ")] = str(bstack1l11llll11_opy_[bstack1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨႫ")])
        return [bstack1l11llll11_opy_[bstack1_opy_ (u"ࠬࡰࡷࡵࠩႬ")], bstack1l11llll11_opy_[bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨႭ")], bstack1l11llll11_opy_[bstack1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫႮ")]]
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩႯ")] == bstack1_opy_ (u"ࠤࡱࡹࡱࡲࠢႰ") or os.environ[bstack1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩႱ")] == bstack1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤႲ"):
            print(bstack1_opy_ (u"ࠬࡋࡘࡄࡇࡓࡘࡎࡕࡎࠡࡋࡑࠤࡸࡺ࡯ࡱࡄࡸ࡭ࡱࡪࡕࡱࡵࡷࡶࡪࡧ࡭ࠡࡔࡈࡕ࡚ࡋࡓࡕࠢࡗࡓ࡚ࠥࡅࡔࡖࠣࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠣ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭Ⴓ"))
            return {
                bstack1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ⴔ"): bstack1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ⴕ"),
                bstack1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩႶ"): bstack1_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧႷ")
            }
        else:
            cls.bstack1l1l1ll11l_opy_.shutdown()
            data = {
                bstack1_opy_ (u"ࠪࡷࡹࡵࡰࡠࡶ࡬ࡱࡪ࠭Ⴘ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬႹ"): cls.default_headers()
            }
            bstack1l1lll1l11_opy_ = bstack1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ࠭Ⴚ").format(os.environ[bstack1_opy_ (u"ࠨࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠧႻ")])
            bstack1l11llll1l_opy_ = cls.request_url(bstack1l1lll1l11_opy_)
            response = bstack1lll11ll1_opy_(bstack1_opy_ (u"ࠧࡑࡗࡗࠫႼ"), bstack1l11llll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢႽ"))
    @classmethod
    def bstack1l11lll111_opy_(cls):
        if cls.bstack1l1l1ll11l_opy_ is None:
            return
        cls.bstack1l1l1ll11l_opy_.shutdown()
    @classmethod
    def bstack1ll11ll1_opy_(cls):
        if cls.on():
            print(
                bstack1_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬႾ").format(os.environ[bstack1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤႿ")]))
    @classmethod
    def bstack1l11ll111l_opy_(cls):
        if cls.bstack1l1l1ll11l_opy_ is not None:
            return
        cls.bstack1l1l1ll11l_opy_ = bstack1l1l1l1l11_opy_(cls.bstack1l11lll1ll_opy_)
        cls.bstack1l1l1ll11l_opy_.start()
    @classmethod
    def bstack1l11l1llll_opy_(cls, bstack1l11ll1l1l_opy_, bstack1l1l111ll1_opy_=bstack1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪჀ")):
        if not cls.on():
            return
        bstack1l1111ll_opy_ = bstack1l11ll1l1l_opy_[bstack1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩჁ")]
        bstack1l11lllll1_opy_ = {
            bstack1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧჂ"): bstack1_opy_ (u"ࠧࡕࡧࡶࡸࡤ࡙ࡴࡢࡴࡷࡣ࡚ࡶ࡬ࡰࡣࡧࠫჃ"),
            bstack1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪჄ"): bstack1_opy_ (u"ࠩࡗࡩࡸࡺ࡟ࡆࡰࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫჅ"),
            bstack1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫ჆"): bstack1_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖ࡯࡮ࡶࡰࡦࡦࡢ࡙ࡵࡲ࡯ࡢࡦࠪჇ"),
            bstack1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ჈"): bstack1_opy_ (u"࠭ࡌࡰࡩࡢ࡙ࡵࡲ࡯ࡢࡦࠪ჉"),
            bstack1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ჊"): bstack1_opy_ (u"ࠨࡊࡲࡳࡰࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬ჋"),
            bstack1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ჌"): bstack1_opy_ (u"ࠪࡌࡴࡵ࡫ࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬჍ"),
            bstack1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ჎"): bstack1_opy_ (u"ࠬࡉࡂࡕࡡࡘࡴࡱࡵࡡࡥࠩ჏")
        }.get(bstack1l1111ll_opy_)
        if bstack1l1l111ll1_opy_ == bstack1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬა"):
            cls.bstack1l11ll111l_opy_()
            cls.bstack1l1l1ll11l_opy_.add(bstack1l11ll1l1l_opy_)
        elif bstack1l1l111ll1_opy_ == bstack1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬბ"):
            cls.bstack1l11lll1ll_opy_([bstack1l11ll1l1l_opy_], bstack1l1l111ll1_opy_)
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def bstack1l11lll1ll_opy_(cls, bstack1l11ll1l1l_opy_, bstack1l1l111ll1_opy_=bstack1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧგ")):
        config = {
            bstack1_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪდ"): cls.default_headers()
        }
        response = bstack1lll11ll1_opy_(bstack1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨე"), cls.request_url(bstack1l1l111ll1_opy_), bstack1l11ll1l1l_opy_, config)
        bstack1l1l111lll_opy_ = response.json()
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def bstack1l1l111l1l_opy_(cls, bstack1l11llllll_opy_):
        bstack1l11ll11ll_opy_ = []
        for log in bstack1l11llllll_opy_:
            bstack1l11ll11ll_opy_.append({
                bstack1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩვ"): bstack1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧზ"),
                bstack1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬთ"): log[bstack1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ი")],
                bstack1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫკ"): log[bstack1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬლ")],
                bstack1_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪმ"): {},
                bstack1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬნ"): log[bstack1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ო")],
                bstack1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭პ"): log[bstack1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧჟ")]
            })
        cls.bstack1l11l1llll_opy_({
            bstack1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬრ"): bstack1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ს"),
            bstack1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨტ"): bstack1l11ll11ll_opy_
        })
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def bstack1l1l111111_opy_(cls, steps):
        bstack1l11lll1l1_opy_ = []
        for step in steps:
            bstack1l11lll11l_opy_ = {
                bstack1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩუ"): bstack1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨფ"),
                bstack1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬქ"): step[bstack1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ღ")],
                bstack1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫყ"): step[bstack1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬშ")],
                bstack1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫჩ"): step[bstack1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬც")],
                bstack1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧძ"): step[bstack1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨწ")]
            }
            if bstack1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧჭ") in step:
                bstack1l11lll11l_opy_[bstack1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨხ")] = step[bstack1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩჯ")]
            elif bstack1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪჰ") in step:
                bstack1l11lll11l_opy_[bstack1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫჱ")] = step[bstack1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬჲ")]
            bstack1l11lll1l1_opy_.append(bstack1l11lll11l_opy_)
        cls.bstack1l11l1llll_opy_({
            bstack1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪჳ"): bstack1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫჴ"),
            bstack1_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ჵ"): bstack1l11lll1l1_opy_
        })
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def bstack1l1l11111l_opy_(cls, screenshot):
        cls.bstack1l11l1llll_opy_({
            bstack1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ჶ"): bstack1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧჷ"),
            bstack1_opy_ (u"ࠫࡱࡵࡧࡴࠩჸ"): [{
                bstack1_opy_ (u"ࠬࡱࡩ࡯ࡦࠪჹ"): bstack1_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨჺ"),
                bstack1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ჻"): datetime.datetime.utcnow().isoformat() + bstack1_opy_ (u"ࠨ࡜ࠪჼ"),
                bstack1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪჽ"): screenshot[bstack1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩჾ")],
                bstack1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫჿ"): screenshot[bstack1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᄀ")]
            }]
        }, bstack1l1l111ll1_opy_=bstack1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᄁ"))
    @classmethod
    @bstack1ll1111111_opy_(class_method=True)
    def bstack1ll111l11_opy_(cls, driver):
        bstack1l11ll1ll1_opy_ = cls.bstack1l11ll1ll1_opy_()
        if not bstack1l11ll1ll1_opy_:
            return
        cls.bstack1l11l1llll_opy_({
            bstack1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᄂ"): bstack1_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᄃ"),
            bstack1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᄄ"): {
                bstack1_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᄅ"): cls.bstack1l11ll1ll1_opy_(),
                bstack1_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᄆ"): cls.bstack1l11l1l1l1_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᄇ"), None) is None or os.environ[bstack1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᄈ")] == bstack1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᄉ"):
            return False
        return True
    @classmethod
    def bstack1l11l1ll11_opy_(cls):
        return bstack1l1llll1l1_opy_(cls.bs_config.get(bstack1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᄊ"), False))
    @staticmethod
    def request_url(url):
        return bstack1_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᄋ").format(bstack1l11l1l1ll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᄌ"): bstack1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᄍ"),
            bstack1_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨᄎ"): bstack1_opy_ (u"࠭ࡴࡳࡷࡨࠫᄏ")
        }
        if os.environ.get(bstack1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᄐ"), None):
            headers[bstack1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᄑ")] = bstack1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬᄒ").format(os.environ[bstack1_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠦᄓ")])
        return headers
    @staticmethod
    def bstack1l11ll1ll1_opy_():
        return getattr(threading.current_thread(), bstack1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᄔ"), None)
    @staticmethod
    def bstack1l11l1l1l1_opy_(driver):
        return {
            bstack1ll111111l_opy_(): bstack1l1llll11l_opy_(driver)
        }
    @staticmethod
    def bstack1l11l1lll1_opy_(exception_info, report):
        return [{bstack1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᄕ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1l1l111l11_opy_(typename):
        if bstack1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤᄖ") in typename:
            return bstack1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᄗ")
        return bstack1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤᄘ")
    @staticmethod
    def bstack1l11l1l111_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l111l1ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1l1111l1_opy_(test):
        bstack1l11ll11l1_opy_ = test.parent
        scope = []
        while bstack1l11ll11l1_opy_ is not None:
            scope.append(bstack1l11ll11l1_opy_.name)
            bstack1l11ll11l1_opy_ = bstack1l11ll11l1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1l11ll1111_opy_(hook_type):
        if hook_type == bstack1_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᄙ"):
            return bstack1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᄚ")
        elif hook_type == bstack1_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᄛ"):
            return bstack1_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᄜ")
    @staticmethod
    def bstack1l11ll1lll_opy_(bstack11l1111l1_opy_):
        try:
            if not bstack1l111l1ll_opy_.on():
                return bstack11l1111l1_opy_
            if os.environ.get(bstack1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᄝ"), None) == bstack1_opy_ (u"ࠢࡵࡴࡸࡩࠧᄞ"):
                tests = os.environ.get(bstack1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᄟ"), None)
                if tests is None or tests == bstack1_opy_ (u"ࠤࡱࡹࡱࡲࠢᄠ"):
                    return bstack11l1111l1_opy_
                bstack11l1111l1_opy_ = tests.split(bstack1_opy_ (u"ࠪ࠰ࠬᄡ"))
                return bstack11l1111l1_opy_
        except Exception as exc:
            print(bstack1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᄢ"), str(exc))
        return bstack11l1111l1_opy_