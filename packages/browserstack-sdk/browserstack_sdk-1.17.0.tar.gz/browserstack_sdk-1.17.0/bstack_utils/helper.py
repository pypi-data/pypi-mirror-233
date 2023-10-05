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
import datetime
import json
import os
import re
import subprocess
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll111lll1_opy_, bstack11l1111l1_opy_, bstack1lll11ll1l_opy_, bstack1l111ll11_opy_
from bstack_utils.messages import bstack1lll1lll1_opy_
from bstack_utils.proxy import bstack1l11111ll_opy_
bstack11ll11ll1_opy_ = Config.get_instance()
def bstack1ll11111l1_opy_(config):
    return config[bstack1111ll1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ༅")]
def bstack1l1lllll1l_opy_(config):
    return config[bstack1111ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭༆")]
def bstack1ll1111lll_opy_(obj):
    values = []
    bstack1l1ll1lll1_opy_ = re.compile(bstack1111ll1_opy_ (u"ࡶࠧࡤࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢࡠࡩ࠱ࠤࠣ༇"), re.I)
    for key in obj.keys():
        if bstack1l1ll1lll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1l1lll11ll_opy_(config):
    tags = []
    tag = config.get(bstack1111ll1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡙ࡧࡧࠣ༈")) or os.environ.get(bstack1111ll1_opy_ (u"ࠨࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࠥ༉"))
    if tag:
        tags.append(tag)
    tags.extend(bstack1ll1111lll_opy_(os.environ))
    tags.extend(bstack1ll1111lll_opy_(config))
    return tags
def bstack1ll111111l_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1l1ll1llll_opy_(bstack1l1lll1ll1_opy_):
    if not bstack1l1lll1ll1_opy_:
        return bstack1111ll1_opy_ (u"ࠧࠨ༊")
    return bstack1111ll1_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤ་").format(bstack1l1lll1ll1_opy_.name, bstack1l1lll1ll1_opy_.email)
def bstack1l1ll1ll11_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack1ll111l1l1_opy_ = repo.common_dir
        info = {
            bstack1111ll1_opy_ (u"ࠤࡶ࡬ࡦࠨ༌"): repo.head.commit.hexsha,
            bstack1111ll1_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨ།"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1111ll1_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦ༎"): repo.active_branch.name,
            bstack1111ll1_opy_ (u"ࠧࡺࡡࡨࠤ༏"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1111ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤ༐"): bstack1l1ll1llll_opy_(repo.head.commit.committer),
            bstack1111ll1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣ༑"): repo.head.commit.committed_datetime.isoformat(),
            bstack1111ll1_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣ༒"): bstack1l1ll1llll_opy_(repo.head.commit.author),
            bstack1111ll1_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢ༓"): repo.head.commit.authored_datetime.isoformat(),
            bstack1111ll1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦ༔"): repo.head.commit.message,
            bstack1111ll1_opy_ (u"ࠦࡷࡵ࡯ࡵࠤ༕"): repo.git.rev_parse(bstack1111ll1_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢ༖")),
            bstack1111ll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢ༗"): bstack1ll111l1l1_opy_,
            bstack1111ll1_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴ༘ࠥ"): subprocess.check_output([bstack1111ll1_opy_ (u"ࠣࡩ࡬ࡸ༙ࠧ"), bstack1111ll1_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧ༚"), bstack1111ll1_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨ༛")]).strip().decode(
                bstack1111ll1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ༜")),
            bstack1111ll1_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢ༝"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1111ll1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣ༞"): repo.git.rev_list(
                bstack1111ll1_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢ༟").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack1ll1111ll1_opy_ = []
        for remote in remotes:
            bstack1l1lll111l_opy_ = {
                bstack1111ll1_opy_ (u"ࠣࡰࡤࡱࡪࠨ༠"): remote.name,
                bstack1111ll1_opy_ (u"ࠤࡸࡶࡱࠨ༡"): remote.url,
            }
            bstack1ll1111ll1_opy_.append(bstack1l1lll111l_opy_)
        return {
            bstack1111ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣ༢"): bstack1111ll1_opy_ (u"ࠦ࡬࡯ࡴࠣ༣"),
            **info,
            bstack1111ll1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨ༤"): bstack1ll1111ll1_opy_
        }
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤ༥").format(err))
        return {}
def bstack1l1llll11l_opy_():
    env = os.environ
    if (bstack1111ll1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧ༦") in env and len(env[bstack1111ll1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨ༧")]) > 0) or (
            bstack1111ll1_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣ༨") in env and len(env[bstack1111ll1_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ༩")]) > 0):
        return {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ༪"): bstack1111ll1_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨ༫"),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ༬"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ༭")),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ༮"): env.get(bstack1111ll1_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦ༯")),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ༰"): env.get(bstack1111ll1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥ༱"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࠣ༲")) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦ༳") and env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤ༴")) == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨ༵"):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ༶"): bstack1111ll1_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍ༷ࠧ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ༸"): env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌ༹ࠣ")),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ༺"): env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ༻")),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ༼"): env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ༽"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠥࡇࡎࠨ༾")) == bstack1111ll1_opy_ (u"ࠦࡹࡸࡵࡦࠤ༿") and env.get(bstack1111ll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧཀ")) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦཁ"):
        return {
            bstack1111ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧག"): bstack1111ll1_opy_ (u"ࠣࡖࡵࡥࡻ࡯ࡳࠡࡅࡌࠦགྷ"),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧང"): env.get(bstack1111ll1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡ࡚ࡉࡇࡥࡕࡓࡎࠥཅ")),
            bstack1111ll1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨཆ"): env.get(bstack1111ll1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢཇ")),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ཈"): env.get(bstack1111ll1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨཉ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠣࡅࡌࠦཊ")) == bstack1111ll1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢཋ") and env.get(bstack1111ll1_opy_ (u"ࠥࡇࡎࡥࡎࡂࡏࡈࠦཌ")) == bstack1111ll1_opy_ (u"ࠦࡨࡵࡤࡦࡵ࡫࡭ࡵࠨཌྷ"):
        return {
            bstack1111ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥཎ"): bstack1111ll1_opy_ (u"ࠨࡃࡰࡦࡨࡷ࡭࡯ࡰࠣཏ"),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥཐ"): None,
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥད"): None,
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣདྷ"): None
        }
    if env.get(bstack1111ll1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡓࡃࡑࡇࡍࠨན")) and env.get(bstack1111ll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢཔ")):
        return {
            bstack1111ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥཕ"): bstack1111ll1_opy_ (u"ࠨࡂࡪࡶࡥࡹࡨࡱࡥࡵࠤབ"),
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥབྷ"): env.get(bstack1111ll1_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡌࡏࡔࡠࡊࡗࡘࡕࡥࡏࡓࡋࡊࡍࡓࠨམ")),
            bstack1111ll1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦཙ"): None,
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤཚ"): env.get(bstack1111ll1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨཛ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࠣཛྷ")) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨࠦཝ") and env.get(bstack1111ll1_opy_ (u"ࠢࡅࡔࡒࡒࡊࠨཞ")) == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨཟ"):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢའ"): bstack1111ll1_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤཡ"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢར"): env.get(bstack1111ll1_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣལ")),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣཤ"): None,
            bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨཥ"): env.get(bstack1111ll1_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨས"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࠧཧ")) == bstack1111ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣཨ") and env.get(bstack1111ll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢཀྵ")) == bstack1111ll1_opy_ (u"ࠧࡺࡲࡶࡧࠥཪ"):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦཫ"): bstack1111ll1_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥཬ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ཭"): env.get(bstack1111ll1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣ཮")),
            bstack1111ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ཯"): env.get(bstack1111ll1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ཰")),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵཱࠦ"): env.get(bstack1111ll1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤི"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋཱིࠥ")) == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨུ") and env.get(bstack1111ll1_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍཱུࠧ")) == bstack1111ll1_opy_ (u"ࠥࡸࡷࡻࡥࠣྲྀ"):
        return {
            bstack1111ll1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤཷ"): bstack1111ll1_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧླྀ"),
            bstack1111ll1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤཹ"): env.get(bstack1111ll1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏེࠦ")),
            bstack1111ll1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧཻࠥ"): env.get(bstack1111ll1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋོࠢ")),
            bstack1111ll1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤཽ"): env.get(bstack1111ll1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢཾ"))
        }
    if env.get(bstack1111ll1_opy_ (u"ࠧࡉࡉࠣཿ")) == bstack1111ll1_opy_ (u"ࠨࡴࡳࡷࡨྀࠦ") and env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇཱྀࠥ")) == bstack1111ll1_opy_ (u"ࠣࡶࡵࡹࡪࠨྂ"):
        return {
            bstack1111ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢྃ"): bstack1111ll1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥ࡭࡬ࡸࡪࠨ྄"),
            bstack1111ll1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ྅"): env.get(bstack1111ll1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ྆")),
            bstack1111ll1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ྇"): env.get(bstack1111ll1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡐࡆࡈࡅࡍࠤྈ")) or env.get(bstack1111ll1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦྉ")),
            bstack1111ll1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣྊ"): env.get(bstack1111ll1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧྋ"))
        }
    if env.get(bstack1111ll1_opy_ (u"࡙ࠦࡌ࡟ࡃࡗࡌࡐࡉࠨྌ")) == bstack1111ll1_opy_ (u"࡚ࠧࡲࡶࡧࠥྍ"):
        return {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦྎ"): bstack1111ll1_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢྏ"),
            bstack1111ll1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦྐ"): bstack1ll1111111_opy_ (u"ࠤࡾࡩࡳࡼ࠮ࡨࡧࡷ࡙࡙ࠬࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨࠫࢀࡿࡪࡴࡶ࠯ࡩࡨࡸ࠭࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࡍࡉ࠭ࠩࡾࠤྑ"),
            bstack1111ll1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧྒ"): env.get(bstack1111ll1_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥྒྷ")),
            bstack1111ll1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦྔ"): env.get(bstack1111ll1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨྕ"))
        }
    return {bstack1111ll1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨྖ"): None}
def get_host_info():
    uname = os.uname()
    return {
        bstack1111ll1_opy_ (u"ࠣࡪࡲࡷࡹࡴࡡ࡮ࡧࠥྗ"): uname.nodename,
        bstack1111ll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦ྘"): uname.sysname,
        bstack1111ll1_opy_ (u"ࠥࡸࡾࡶࡥࠣྙ"): uname.machine,
        bstack1111ll1_opy_ (u"ࠦࡻ࡫ࡲࡴ࡫ࡲࡲࠧྚ"): uname.version,
        bstack1111ll1_opy_ (u"ࠧࡧࡲࡤࡪࠥྛ"): uname.machine
    }
def bstack1l1ll1l1ll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1l1llll111_opy_():
    if bstack11ll11ll1_opy_.get_property(bstack1111ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧྜ")):
        return bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ྜྷ")
    return bstack1111ll1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠧྞ")
def bstack1ll1111l11_opy_(driver):
    info = {
        bstack1111ll1_opy_ (u"ࠩࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨྟ"): driver.capabilities,
        bstack1111ll1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠧྠ"): driver.session_id,
        bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬྡ"): driver.capabilities[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪྡྷ")],
        bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨྣ"): driver.capabilities[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྤ")],
        bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪྥ"): driver.capabilities[bstack1111ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨྦ")],
    }
    if bstack1l1llll111_opy_() == bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩྦྷ"):
        info[bstack1111ll1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬྨ")] = bstack1111ll1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫྩ") if bstack11ll11ll1_opy_.get_property(bstack1111ll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬྪ")) else bstack1111ll1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩྫ")
    return info
def bstack1ll1ll1l1l_opy_(bstack1ll11111ll_opy_, url, data, config):
    headers = config.get(bstack1111ll1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩྫྷ"), None)
    proxies = bstack1l11111ll_opy_(config, url)
    auth = config.get(bstack1111ll1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧྭ"), None)
    response = requests.request(
            bstack1ll11111ll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack11l1l11ll_opy_(bstack1llllll1ll_opy_, size):
    bstack11l1ll11_opy_ = []
    while len(bstack1llllll1ll_opy_) > size:
        bstack11lll11l1_opy_ = bstack1llllll1ll_opy_[:size]
        bstack11l1ll11_opy_.append(bstack11lll11l1_opy_)
        bstack1llllll1ll_opy_ = bstack1llllll1ll_opy_[size:]
    bstack11l1ll11_opy_.append(bstack1llllll1ll_opy_)
    return bstack11l1ll11_opy_
def bstack1l1lll1111_opy_(message):
    os.write(1, bytes(message, bstack1111ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩྮ")))
    os.write(1, bytes(bstack1111ll1_opy_ (u"ࠫࡡࡴࠧྯ"), bstack1111ll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫྰ")))
def bstack1l1lll1l11_opy_():
    return os.environ[bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩྱ")].lower() == bstack1111ll1_opy_ (u"ࠧࡵࡴࡸࡩࠬྲ")
def bstack1111llll1_opy_(bstack1l1lllllll_opy_):
    return bstack1111ll1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧླ").format(bstack1ll111lll1_opy_, bstack1l1lllllll_opy_)
def bstack1l11l1l1l_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"ࠩ࡝ࠫྴ")
def bstack1l1ll1ll1l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪྵ")
    else:
        return bstack1111ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫྶ")
def bstack1ll111l1ll_opy_(val):
    return val.__str__().lower() == bstack1111ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪྷ")
def bstack1ll1111l1l_opy_(val):
    return val.__str__().lower() == bstack1111ll1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬྸ")
def bstack1l1lll1lll_opy_(bstack1l1llll1l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack1l1llll1l1_opy_ as e:
                print(bstack1111ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢྐྵ").format(func.__name__, bstack1l1llll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack1l1lllll11_opy_(bstack1ll111l111_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack1ll111l111_opy_(cls, *args, **kwargs)
            except bstack1l1llll1l1_opy_ as e:
                print(bstack1111ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣྺ").format(bstack1ll111l111_opy_.__name__, bstack1l1llll1l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack1l1lllll11_opy_
    else:
        return decorator
def bstack1ll1ll111l_opy_(bstack1ll1l1111l_opy_):
    if bstack1111ll1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ྻ") in bstack1ll1l1111l_opy_ and bstack1ll1111l1l_opy_(bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧྼ")]):
        return False
    if bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭྽") in bstack1ll1l1111l_opy_ and bstack1ll1111l1l_opy_(bstack1ll1l1111l_opy_[bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ྾")]):
        return False
    return True
def bstack1l1llllll1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack11l1111ll_opy_(hub_url):
    if bstack1ll1l11l1l_opy_() <= version.parse(bstack1111ll1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭྿")):
        if hub_url != bstack1111ll1_opy_ (u"ࠧࠨ࿀"):
            return bstack1111ll1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ࿁") + hub_url + bstack1111ll1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ࿂")
        return bstack1lll11ll1l_opy_
    if hub_url != bstack1111ll1_opy_ (u"ࠪࠫ࿃"):
        return bstack1111ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨ࿄") + hub_url + bstack1111ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ࿅")
    return bstack1l111ll11_opy_
def bstack1l1lll1l1l_opy_():
    return isinstance(os.getenv(bstack1111ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡌࡖࡉࡌࡒ࿆ࠬ")), str)
def bstack11l11l11l_opy_(url):
    return urlparse(url).hostname
def bstack1l1l111l1_opy_(hostname):
    for bstack1l1ll111_opy_ in bstack11l1111l1_opy_:
        regex = re.compile(bstack1l1ll111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack1l1lll11l1_opy_(bstack1ll111ll11_opy_, file_name, logger):
    bstack1l1l1l11l_opy_ = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠧࡿࠩ࿇")), bstack1ll111ll11_opy_)
    try:
        if not os.path.exists(bstack1l1l1l11l_opy_):
            os.makedirs(bstack1l1l1l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1111ll1_opy_ (u"ࠨࢀࠪ࿈")), bstack1ll111ll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1111ll1_opy_ (u"ࠩࡺࠫ࿉")):
                pass
            with open(file_path, bstack1111ll1_opy_ (u"ࠥࡻ࠰ࠨ࿊")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1lll1lll1_opy_.format(str(e)))
def bstack1l1llll1ll_opy_(file_name, key, value, logger):
    file_path = bstack1l1lll11l1_opy_(bstack1111ll1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ࿋"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack11l1l1l1l_opy_ = json.load(open(file_path, bstack1111ll1_opy_ (u"ࠬࡸࡢࠨ࿌")))
        else:
            bstack11l1l1l1l_opy_ = {}
        bstack11l1l1l1l_opy_[key] = value
        with open(file_path, bstack1111ll1_opy_ (u"ࠨࡷࠬࠤ࿍")) as outfile:
            json.dump(bstack11l1l1l1l_opy_, outfile)
def bstack111ll11ll_opy_(file_name, logger):
    file_path = bstack1l1lll11l1_opy_(bstack1111ll1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࿎"), file_name, logger)
    bstack11l1l1l1l_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1111ll1_opy_ (u"ࠨࡴࠪ࿏")) as bstack1l11l1ll_opy_:
            bstack11l1l1l1l_opy_ = json.load(bstack1l11l1ll_opy_)
    return bstack11l1l1l1l_opy_
def bstack1l1l1l111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡩ࡫࡬ࡦࡶ࡬ࡲ࡬ࠦࡦࡪ࡮ࡨ࠾ࠥ࠭࿐") + file_path + bstack1111ll1_opy_ (u"ࠪࠤࠬ࿑") + str(e))
def bstack1ll1l11l1l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1111ll1_opy_ (u"ࠦࡁࡔࡏࡕࡕࡈࡘࡃࠨ࿒")
def bstack11ll1l1l_opy_(config):
    if bstack1111ll1_opy_ (u"ࠬ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ࿓") in config:
        del (config[bstack1111ll1_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ࿔")])
        return False
    if bstack1ll1l11l1l_opy_() < version.parse(bstack1111ll1_opy_ (u"ࠧ࠴࠰࠷࠲࠵࠭࿕")):
        return False
    if bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠨ࠶࠱࠵࠳࠻ࠧ࿖")):
        return True
    if bstack1111ll1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩ࿗") in config and config[bstack1111ll1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ࿘")] is False:
        return False
    else:
        return True
def bstack1l1111ll1_opy_(args_list, bstack1ll111l11l_opy_):
    index = -1
    for value in bstack1ll111l11l_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index