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
import os
from urllib.parse import urlparse
from bstack_utils.messages import bstack1l1ll11ll1_opy_
def bstack1l1ll1111l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1l1ll111l1_opy_(bstack1l1l1llll1_opy_, bstack1l1ll111ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1l1l1llll1_opy_):
        with open(bstack1l1l1llll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1l1ll1111l_opy_(bstack1l1l1llll1_opy_):
        pac = get_pac(url=bstack1l1l1llll1_opy_)
    else:
        raise Exception(bstack1111ll1_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪသ").format(bstack1l1l1llll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1111ll1_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧဟ"), 80))
        bstack1l1ll11l11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1l1ll11l11_opy_ = bstack1111ll1_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ဠ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1l1ll111ll_opy_, bstack1l1ll11l11_opy_)
    return proxy_url
def bstack1lll1l1ll1_opy_(config):
    return bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩအ") in config or bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫဢ") in config
def bstack1llll11l11_opy_(config):
    if not bstack1lll1l1ll1_opy_(config):
        return
    if config.get(bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫဣ")):
        return config.get(bstack1111ll1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬဤ"))
    if config.get(bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧဥ")):
        return config.get(bstack1111ll1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨဦ"))
def bstack1l11111ll_opy_(config, bstack1l1ll111ll_opy_):
    proxy = bstack1llll11l11_opy_(config)
    proxies = {}
    if config.get(bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨဧ")) or config.get(bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪဨ")):
        if proxy.endswith(bstack1111ll1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬဩ")):
            proxies = bstack1ll111l11_opy_(proxy, bstack1l1ll111ll_opy_)
        else:
            proxies = {
                bstack1111ll1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧဪ"): proxy
            }
    return proxies
def bstack1ll111l11_opy_(bstack1l1l1llll1_opy_, bstack1l1ll111ll_opy_):
    proxies = {}
    global bstack1l1l1lllll_opy_
    if bstack1111ll1_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬါ") in globals():
        return bstack1l1l1lllll_opy_
    try:
        proxy = bstack1l1ll111l1_opy_(bstack1l1l1llll1_opy_, bstack1l1ll111ll_opy_)
        if bstack1111ll1_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥာ") in proxy:
            proxies = {}
        elif bstack1111ll1_opy_ (u"ࠦࡍ࡚ࡔࡑࠤိ") in proxy or bstack1111ll1_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦီ") in proxy or bstack1111ll1_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧု") in proxy:
            bstack1l1ll11111_opy_ = proxy.split(bstack1111ll1_opy_ (u"ࠢࠡࠤူ"))
            if bstack1111ll1_opy_ (u"ࠣ࠼࠲࠳ࠧေ") in bstack1111ll1_opy_ (u"ࠤࠥဲ").join(bstack1l1ll11111_opy_[1:]):
                proxies = {
                    bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩဳ"): bstack1111ll1_opy_ (u"ࠦࠧဴ").join(bstack1l1ll11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫဵ"): str(bstack1l1ll11111_opy_[0]).lower() + bstack1111ll1_opy_ (u"ࠨ࠺࠰࠱ࠥံ") + bstack1111ll1_opy_ (u"့ࠢࠣ").join(bstack1l1ll11111_opy_[1:])
                }
        elif bstack1111ll1_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢး") in proxy:
            bstack1l1ll11111_opy_ = proxy.split(bstack1111ll1_opy_ (u"ࠤ္ࠣࠦ"))
            if bstack1111ll1_opy_ (u"ࠥ࠾࠴࠵်ࠢ") in bstack1111ll1_opy_ (u"ࠦࠧျ").join(bstack1l1ll11111_opy_[1:]):
                proxies = {
                    bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫြ"): bstack1111ll1_opy_ (u"ࠨࠢွ").join(bstack1l1ll11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ှ"): bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤဿ") + bstack1111ll1_opy_ (u"ࠤࠥ၀").join(bstack1l1ll11111_opy_[1:])
                }
        else:
            proxies = {
                bstack1111ll1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩ၁"): proxy
            }
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣ၂"), bstack1l1ll11ll1_opy_.format(bstack1l1l1llll1_opy_, str(e)))
    bstack1l1l1lllll_opy_ = proxies
    return proxies