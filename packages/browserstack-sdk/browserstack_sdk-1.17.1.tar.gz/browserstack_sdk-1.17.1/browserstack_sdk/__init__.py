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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from bstack_utils.constants import *
import time
import requests
def bstack1111lllll_opy_():
  global CONFIG
  headers = {
        bstack1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡵ"): bstack1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡶ"),
      }
  proxies = bstack1111111l1_opy_(CONFIG, bstack1l1lll11_opy_)
  try:
    response = requests.get(bstack1l1lll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack111lll11l_opy_ = response.json()[bstack1_opy_ (u"ࠫ࡭ࡻࡢࡴࠩࡷ")]
      logger.debug(bstack1llll11111_opy_.format(response.json()))
      return bstack111lll11l_opy_
    else:
      logger.debug(bstack1l1lll111_opy_.format(bstack1_opy_ (u"ࠧࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡋࡕࡒࡒࠥࡶࡡࡳࡵࡨࠤࡪࡸࡲࡰࡴࠣࠦࡸ")))
  except Exception as e:
    logger.debug(bstack1l1lll111_opy_.format(e))
def bstack1ll11llll_opy_(hub_url):
  global CONFIG
  url = bstack1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣࡹ")+  hub_url + bstack1_opy_ (u"ࠢ࠰ࡥ࡫ࡩࡨࡱࠢࡺ")
  headers = {
        bstack1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧࡻ"): bstack1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬࡼ"),
      }
  proxies = bstack1111111l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1l1ll1lll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11l111111_opy_.format(hub_url, e))
def bstack11lll1l11_opy_():
  try:
    global bstack111111l1l_opy_
    bstack111lll11l_opy_ = bstack1111lllll_opy_()
    bstack111l1l111_opy_ = []
    results = []
    for bstack11ll111l1_opy_ in bstack111lll11l_opy_:
      bstack111l1l111_opy_.append(bstack111l111l1_opy_(target=bstack1ll11llll_opy_,args=(bstack11ll111l1_opy_,)))
    for t in bstack111l1l111_opy_:
      t.start()
    for t in bstack111l1l111_opy_:
      results.append(t.join())
    bstack111ll1l11_opy_ = {}
    for item in results:
      hub_url = item[bstack1_opy_ (u"ࠪ࡬ࡺࡨ࡟ࡶࡴ࡯ࠫࡽ")]
      latency = item[bstack1_opy_ (u"ࠫࡱࡧࡴࡦࡰࡦࡽࠬࡾ")]
      bstack111ll1l11_opy_[hub_url] = latency
    bstack1lll11ll11_opy_ = min(bstack111ll1l11_opy_, key= lambda x: bstack111ll1l11_opy_[x])
    bstack111111l1l_opy_ = bstack1lll11ll11_opy_
    logger.debug(bstack1l1ll1l1_opy_.format(bstack1lll11ll11_opy_))
  except Exception as e:
    logger.debug(bstack11l11l1l_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll11ll1_opy_, bstack11l11l111_opy_, bstack11l1lllll_opy_, Notset, bstack1111llll1_opy_, \
  bstack11lllll1_opy_, bstack11111lll_opy_, bstack1111l11l1_opy_
from bstack_utils.bstack1ll111111_opy_ import bstack1l111l1ll_opy_
from bstack_utils.proxy import bstack1lll1lll1l_opy_, bstack1111111l1_opy_, bstack1lll11lll_opy_, bstack11ll11l1l_opy_
from browserstack_sdk.bstack1l1ll1ll_opy_ import *
from browserstack_sdk.bstack1llll11ll_opy_ import *
bstack1llllllll1_opy_ = bstack1_opy_ (u"ࠬࠦࠠ࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠥࠦࡩࡧࠪࡳࡥ࡬࡫ࠠ࠾࠿ࡀࠤࡻࡵࡩࡥࠢ࠳࠭ࠥࢁ࡜࡯ࠢࠣࠤࡹࡸࡹࡼ࡞ࡱࠤࡨࡵ࡮ࡴࡶࠣࡪࡸࠦ࠽ࠡࡴࡨࡵࡺ࡯ࡲࡦࠪ࡟ࠫ࡫ࡹ࡜ࠨࠫ࠾ࡠࡳࠦࠠࠡࠢࠣࡪࡸ࠴ࡡࡱࡲࡨࡲࡩࡌࡩ࡭ࡧࡖࡽࡳࡩࠨࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷ࡬࠱ࠦࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡱࡡ࡬ࡲࡩ࡫ࡸࠪࠢ࠮ࠤࠧࡀࠢࠡ࠭ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࠪࡤࡻࡦ࡯ࡴࠡࡰࡨࡻࡕࡧࡧࡦ࠴࠱ࡩࡻࡧ࡬ࡶࡣࡷࡩ࠭ࠨࠨࠪࠢࡀࡂࠥࢁࡽࠣ࠮ࠣࡠࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧ࡭ࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡆࡨࡸࡦ࡯࡬ࡴࠤࢀࡠࠬ࠯ࠩࠪ࡝ࠥ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩࠨ࡝ࠪࠢ࠮ࠤࠧ࠲࡜࡝ࡰࠥ࠭ࡡࡴࠠࠡࠢࠣࢁࡨࡧࡴࡤࡪࠫࡩࡽ࠯ࡻ࡝ࡰࠣࠤࠥࠦࡽ࡝ࡰࠣࠤࢂࡢ࡮ࠡࠢ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࠬࡿ")
bstack1llll1111_opy_ = bstack1_opy_ (u"࠭࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠸ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡣࡵࡷࡥࡨࡱ࡟ࡤࡣࡳࡷࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠲࡟࡟ࡲࡨࡵ࡮ࡴࡶࠣࡴࡤ࡯࡮ࡥࡧࡻࠤࡂࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺࡠࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠲࡞࡞ࡱࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡷࡱ࡯ࡣࡦࠪ࠳࠰ࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡱ࡫࡮ࡨࡶ࡫ࠤ࠲ࠦ࠳ࠪ࡞ࡱࡧࡴࡴࡳࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣࠫ࠾ࡠࡳ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡲࡡࡶࡰࡦ࡬ࠥࡃࠠࡢࡵࡼࡲࡨࠦࠨ࡭ࡣࡸࡲࡨ࡮ࡏࡱࡶ࡬ࡳࡳࡹࠩࠡ࠿ࡁࠤࢀࡢ࡮࡭ࡧࡷࠤࡨࡧࡰࡴ࠽࡟ࡲࡹࡸࡹࠡࡽ࡟ࡲࡨࡧࡰࡴࠢࡀࠤࡏ࡙ࡏࡏ࠰ࡳࡥࡷࡹࡥࠩࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸ࠯࡜࡯ࠢࠣࢁࠥࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࠡࡽ࡟ࡲࠥࠦࠠࠡࡿ࡟ࡲࠥࠦࡲࡦࡶࡸࡶࡳࠦࡡࡸࡣ࡬ࡸࠥ࡯࡭ࡱࡱࡵࡸࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠶ࡢࡦࡸࡺࡡࡤ࡭࠱ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ࠳ࡩ࡯࡯ࡰࡨࡧࡹ࠮ࡻ࡝ࡰࠣࠤࠥࠦࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶ࠽ࠤࡥࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠤࡼࡧࡱࡧࡴࡪࡥࡖࡔࡌࡇࡴࡳࡰࡰࡰࡨࡲࡹ࠮ࡊࡔࡑࡑ࠲ࡸࡺࡲࡪࡰࡪ࡭࡫ࡿࠨࡤࡣࡳࡷ࠮࠯ࡽࡡ࠮࡟ࡲࠥࠦࠠࠡ࠰࠱࠲ࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶࡠࡳࠦࠠࡾࠫ࡟ࡲࢂࡢ࡮࠰ࠬࠣࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃࠠࠫ࠱࡟ࡲࠬࢀ")
from ._version import __version__
bstack1llllll11l_opy_ = None
CONFIG = {}
bstack1l11l111_opy_ = {}
bstack1lllll1ll1_opy_ = {}
bstack1l11l1ll_opy_ = None
bstack11lll111_opy_ = None
bstack1l11l1lll_opy_ = None
bstack1l111l11_opy_ = -1
bstack111l1llll_opy_ = bstack1llll111l1_opy_
bstack111111ll1_opy_ = 1
bstack1l111111l_opy_ = False
bstack1lll1lll1_opy_ = False
bstack11ll11ll1_opy_ = bstack1_opy_ (u"ࠧࠨࢁ")
bstack1ll1l111l_opy_ = bstack1_opy_ (u"ࠨࠩࢂ")
bstack11111111_opy_ = False
bstack1ll1l11l_opy_ = True
bstack1ll1lll1l_opy_ = bstack1_opy_ (u"ࠩࠪࢃ")
bstack1111ll111_opy_ = []
bstack111111l1l_opy_ = bstack1_opy_ (u"ࠪࠫࢄ")
bstack1llll1111l_opy_ = False
bstack1l11l1ll1_opy_ = None
bstack11l11llll_opy_ = None
bstack1ll1ll111l_opy_ = -1
bstack11111l111_opy_ = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠫࢃ࠭ࢅ")), bstack1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࢆ"), bstack1_opy_ (u"࠭࠮ࡳࡱࡥࡳࡹ࠳ࡲࡦࡲࡲࡶࡹ࠳ࡨࡦ࡮ࡳࡩࡷ࠴ࡪࡴࡱࡱࠫࢇ"))
bstack11111ll11_opy_ = []
bstack1lll1111l1_opy_ = []
bstack1llllll1l_opy_ = False
bstack1lllll1l1l_opy_ = False
bstack1111ll1l_opy_ = None
bstack11l11l1ll_opy_ = None
bstack111l1l1l_opy_ = None
bstack1ll1l1l1ll_opy_ = None
bstack11l111l1l_opy_ = None
bstack11ll1l1l1_opy_ = None
bstack111l11l11_opy_ = None
bstack1l111llll_opy_ = None
bstack11l11lll1_opy_ = None
bstack1ll1lll1_opy_ = None
bstack11l11l11l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack111l1l11l_opy_ = None
bstack111llll1l_opy_ = None
bstack1lllll11l1_opy_ = None
bstack1lll1ll1l_opy_ = None
bstack1l1111111_opy_ = None
bstack11ll11l1_opy_ = None
bstack1ll111l1_opy_ = bstack1_opy_ (u"ࠢࠣ࢈")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack111l1llll_opy_,
                    format=bstack1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ࢉ"),
                    datefmt=bstack1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫࢊ"),
                    stream=sys.stdout)
bstack1ll1l11l1_opy_ = Config.get_instance()
def bstack1l1l11ll1_opy_():
  global CONFIG
  global bstack111l1llll_opy_
  if bstack1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬࢋ") in CONFIG:
    bstack111l1llll_opy_ = bstack11l1l111_opy_[CONFIG[bstack1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ࢌ")]]
    logging.getLogger().setLevel(bstack111l1llll_opy_)
def bstack1111ll11_opy_():
  global CONFIG
  global bstack1llllll1l_opy_
  bstack11ll1ll1_opy_ = bstack11l1l111l_opy_(CONFIG)
  if (bstack1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ") in bstack11ll1ll1_opy_ and str(bstack11ll1ll1_opy_[bstack1_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨࢎ")]).lower() == bstack1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࢏")):
    bstack1llllll1l_opy_ = True
def bstack1111l111_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1ll111ll1_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111111lll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack1ll1lll1l_opy_
      bstack1ll1lll1l_opy_ += bstack1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1llll11l_opy_ = re.compile(bstack1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack11ll11111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1llll11l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1ll1l1l1_opy_():
  bstack11lll111l_opy_ = bstack111111lll_opy_()
  if bstack11lll111l_opy_ and os.path.exists(os.path.abspath(bstack11lll111l_opy_)):
    fileName = bstack11lll111l_opy_
  if bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11111l1_opy_ = os.path.abspath(fileName)
  else:
    bstack11111l1_opy_ = bstack1_opy_ (u"࢛ࠬ࠭")
  bstack111ll1ll_opy_ = os.getcwd()
  bstack1ll1lll11l_opy_ = bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1llll1l1ll_opy_ = bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11111l1_opy_)) and bstack111ll1ll_opy_ != bstack1_opy_ (u"ࠣࠤ࢞"):
    bstack11111l1_opy_ = os.path.join(bstack111ll1ll_opy_, bstack1ll1lll11l_opy_)
    if not os.path.exists(bstack11111l1_opy_):
      bstack11111l1_opy_ = os.path.join(bstack111ll1ll_opy_, bstack1llll1l1ll_opy_)
    if bstack111ll1ll_opy_ != os.path.dirname(bstack111ll1ll_opy_):
      bstack111ll1ll_opy_ = os.path.dirname(bstack111ll1ll_opy_)
    else:
      bstack111ll1ll_opy_ = bstack1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11111l1_opy_):
    bstack11lllllll_opy_(
      bstack1l11lllll_opy_.format(os.getcwd()))
  try:
    with open(bstack11111l1_opy_, bstack1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1llll11l_opy_)
      yaml.add_constructor(bstack1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack11ll11111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11111l1_opy_, bstack1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11lllllll_opy_(bstack1ll1lll111_opy_.format(str(exc)))
def bstack11lll11l1_opy_(config):
  bstack1llllllll_opy_ = bstack1l11l1l1l_opy_(config)
  for option in list(bstack1llllllll_opy_):
    if option.lower() in bstack1ll11l11_opy_ and option != bstack1ll11l11_opy_[option.lower()]:
      bstack1llllllll_opy_[bstack1ll11l11_opy_[option.lower()]] = bstack1llllllll_opy_[option]
      del bstack1llllllll_opy_[option]
  return config
def bstack11llll11l_opy_():
  global bstack1lllll1ll1_opy_
  for key, bstack1l1l1l11_opy_ in bstack1llll11ll1_opy_.items():
    if isinstance(bstack1l1l1l11_opy_, list):
      for var in bstack1l1l1l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lllll1ll1_opy_[key] = os.environ[var]
          break
    elif bstack1l1l1l11_opy_ in os.environ and os.environ[bstack1l1l1l11_opy_] and str(os.environ[bstack1l1l1l11_opy_]).strip():
      bstack1lllll1ll1_opy_[key] = os.environ[bstack1l1l1l11_opy_]
  if bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1lllll1ll1_opy_[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1lllll1ll1_opy_[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1ll1111ll_opy_():
  global bstack1l11l111_opy_
  global bstack1ll1lll1l_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l11l111_opy_[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l11l111_opy_[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11lll1l1_opy_ in bstack11111111l_opy_.items():
    if isinstance(bstack11lll1l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11lll1l1_opy_:
          if idx < len(sys.argv) and bstack1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l11l111_opy_:
            bstack1l11l111_opy_[key] = sys.argv[idx + 1]
            bstack1ll1lll1l_opy_ += bstack1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack11lll1l1_opy_.lower() == val.lower() and not key in bstack1l11l111_opy_:
          bstack1l11l111_opy_[key] = sys.argv[idx + 1]
          bstack1ll1lll1l_opy_ += bstack1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack11lll1l1_opy_ + bstack1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1l111l1l_opy_(config):
  bstack1lllllllll_opy_ = config.keys()
  for bstack1ll1lllll1_opy_, bstack1llll1ll1_opy_ in bstack1l11l11l_opy_.items():
    if bstack1llll1ll1_opy_ in bstack1lllllllll_opy_:
      config[bstack1ll1lllll1_opy_] = config[bstack1llll1ll1_opy_]
      del config[bstack1llll1ll1_opy_]
  for bstack1ll1lllll1_opy_, bstack1llll1ll1_opy_ in bstack1ll1ll1111_opy_.items():
    if isinstance(bstack1llll1ll1_opy_, list):
      for bstack1l111l111_opy_ in bstack1llll1ll1_opy_:
        if bstack1l111l111_opy_ in bstack1lllllllll_opy_:
          config[bstack1ll1lllll1_opy_] = config[bstack1l111l111_opy_]
          del config[bstack1l111l111_opy_]
          break
    elif bstack1llll1ll1_opy_ in bstack1lllllllll_opy_:
      config[bstack1ll1lllll1_opy_] = config[bstack1llll1ll1_opy_]
      del config[bstack1llll1ll1_opy_]
  for bstack1l111l111_opy_ in list(config):
    for bstack111llllll_opy_ in bstack11llll111_opy_:
      if bstack1l111l111_opy_.lower() == bstack111llllll_opy_.lower() and bstack1l111l111_opy_ != bstack111llllll_opy_:
        config[bstack111llllll_opy_] = config[bstack1l111l111_opy_]
        del config[bstack1l111l111_opy_]
  bstack1lll1l11_opy_ = []
  if bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1lll1l11_opy_ = config[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1lll1l11_opy_:
    for bstack1l111l111_opy_ in list(platform):
      for bstack111llllll_opy_ in bstack11llll111_opy_:
        if bstack1l111l111_opy_.lower() == bstack111llllll_opy_.lower() and bstack1l111l111_opy_ != bstack111llllll_opy_:
          platform[bstack111llllll_opy_] = platform[bstack1l111l111_opy_]
          del platform[bstack1l111l111_opy_]
  for bstack1ll1lllll1_opy_, bstack1llll1ll1_opy_ in bstack1ll1ll1111_opy_.items():
    for platform in bstack1lll1l11_opy_:
      if isinstance(bstack1llll1ll1_opy_, list):
        for bstack1l111l111_opy_ in bstack1llll1ll1_opy_:
          if bstack1l111l111_opy_ in platform:
            platform[bstack1ll1lllll1_opy_] = platform[bstack1l111l111_opy_]
            del platform[bstack1l111l111_opy_]
            break
      elif bstack1llll1ll1_opy_ in platform:
        platform[bstack1ll1lllll1_opy_] = platform[bstack1llll1ll1_opy_]
        del platform[bstack1llll1ll1_opy_]
  for bstack1111lll11_opy_ in bstack1llll111ll_opy_:
    if bstack1111lll11_opy_ in config:
      if not bstack1llll111ll_opy_[bstack1111lll11_opy_] in config:
        config[bstack1llll111ll_opy_[bstack1111lll11_opy_]] = {}
      config[bstack1llll111ll_opy_[bstack1111lll11_opy_]].update(config[bstack1111lll11_opy_])
      del config[bstack1111lll11_opy_]
  for platform in bstack1lll1l11_opy_:
    for bstack1111lll11_opy_ in bstack1llll111ll_opy_:
      if bstack1111lll11_opy_ in list(platform):
        if not bstack1llll111ll_opy_[bstack1111lll11_opy_] in platform:
          platform[bstack1llll111ll_opy_[bstack1111lll11_opy_]] = {}
        platform[bstack1llll111ll_opy_[bstack1111lll11_opy_]].update(platform[bstack1111lll11_opy_])
        del platform[bstack1111lll11_opy_]
  config = bstack11lll11l1_opy_(config)
  return config
def bstack1l11111ll_opy_(config):
  global bstack1ll1l111l_opy_
  if bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack111ll111_opy_ = datetime.datetime.now()
      bstack1l1l11lll_opy_ = bstack111ll111_opy_.strftime(bstack1_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1llll11l11_opy_ = bstack1_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack1l1l11lll_opy_, hostname, bstack1llll11l11_opy_)
      config[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack1ll1l111l_opy_ = config[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack11ll11lll_opy_():
  if (
          isinstance(os.getenv(bstack1_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨࣃ")), str) and len(os.getenv(bstack1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠩࣄ"))) > 0
  ) or (
          isinstance(os.getenv(bstack1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫࣅ")), str) and len(os.getenv(bstack1_opy_ (u"࠭ࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠬࣆ"))) > 0
  ):
    return os.getenv(bstack1_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭ࣇ"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠨࡅࡌࠫࣈ"))).lower() == bstack1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࣉ") and str(os.getenv(bstack1_opy_ (u"ࠪࡇࡎࡘࡃࡍࡇࡆࡍࠬ࣊"))).lower() == bstack1_opy_ (u"ࠫࡹࡸࡵࡦࠩ࣋"):
    return os.getenv(bstack1_opy_ (u"ࠬࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠨ࣌"), 0)
  if str(os.getenv(bstack1_opy_ (u"࠭ࡃࡊࠩ࣍"))).lower() == bstack1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣎") and str(os.getenv(bstack1_opy_ (u"ࠨࡖࡕࡅ࡛ࡏࡓࠨ࣏"))).lower() == bstack1_opy_ (u"ࠩࡷࡶࡺ࡫࣐ࠧ"):
    return os.getenv(bstack1_opy_ (u"ࠪࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓ࣑ࠩ"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠫࡈࡏ࣒ࠧ"))).lower() == bstack1_opy_ (u"ࠬࡺࡲࡶࡧ࣓ࠪ") and str(os.getenv(bstack1_opy_ (u"࠭ࡃࡊࡡࡑࡅࡒࡋࠧࣔ"))).lower() == bstack1_opy_ (u"ࠧࡤࡱࡧࡩࡸ࡮ࡩࡱࠩࣕ"):
    return 0
  if os.getenv(bstack1_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠫࣖ")) and os.getenv(bstack1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠬࣗ")):
    return os.getenv(bstack1_opy_ (u"ࠪࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬࣘ"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠫࡈࡏࠧࣙ"))).lower() == bstack1_opy_ (u"ࠬࡺࡲࡶࡧࠪࣚ") and str(os.getenv(bstack1_opy_ (u"࠭ࡄࡓࡑࡑࡉࠬࣛ"))).lower() == bstack1_opy_ (u"ࠧࡵࡴࡸࡩࠬࣜ"):
    return os.getenv(bstack1_opy_ (u"ࠨࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗ࠭ࣝ"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠩࡆࡍࠬࣞ"))).lower() == bstack1_opy_ (u"ࠪࡸࡷࡻࡥࠨࣟ") and str(os.getenv(bstack1_opy_ (u"ࠫࡘࡋࡍࡂࡒࡋࡓࡗࡋࠧ࣠"))).lower() == bstack1_opy_ (u"ࠬࡺࡲࡶࡧࠪ࣡"):
    return os.getenv(bstack1_opy_ (u"࠭ࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠩ࣢"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠧࡄࡋࣣࠪ"))).lower() == bstack1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ࣤ") and str(os.getenv(bstack1_opy_ (u"ࠩࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠬࣥ"))).lower() == bstack1_opy_ (u"ࠪࡸࡷࡻࡥࠨࣦ"):
    return os.getenv(bstack1_opy_ (u"ࠫࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠧࣧ"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠬࡉࡉࠨࣨ"))).lower() == bstack1_opy_ (u"࠭ࡴࡳࡷࡨࣩࠫ") and str(os.getenv(bstack1_opy_ (u"ࠧࡃࡗࡌࡐࡉࡑࡉࡕࡇࠪ࣪"))).lower() == bstack1_opy_ (u"ࠨࡶࡵࡹࡪ࠭࣫"):
    return os.getenv(bstack1_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫ࣬"), 0)
  if str(os.getenv(bstack1_opy_ (u"ࠪࡘࡋࡥࡂࡖࡋࡏࡈ࣭ࠬ"))).lower() == bstack1_opy_ (u"ࠫࡹࡸࡵࡦ࣮ࠩ"):
    return os.getenv(bstack1_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈ࣯ࠬ"), 0)
  return -1
def bstack11111l11l_opy_(bstack11l11l1l1_opy_):
  global CONFIG
  if not bstack1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨࣰ") in CONFIG[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣱࠩ")]:
    return
  CONFIG[bstack1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣲࠪ")] = CONFIG[bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣳ")].replace(
    bstack1_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣴ"),
    str(bstack11l11l1l1_opy_)
  )
def bstack1l11lll11_opy_():
  global CONFIG
  if not bstack1_opy_ (u"ࠫࠩࢁࡄࡂࡖࡈࡣ࡙ࡏࡍࡆࡿࠪࣵ") in CONFIG[bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࣶࠧ")]:
    return
  bstack111ll111_opy_ = datetime.datetime.now()
  bstack1l1l11lll_opy_ = bstack111ll111_opy_.strftime(bstack1_opy_ (u"࠭ࠥࡥ࠯ࠨࡦ࠲ࠫࡈ࠻ࠧࡐࠫࣷ"))
  CONFIG[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣸ")] = CONFIG[bstack1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࣹࠪ")].replace(
    bstack1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣺ"),
    bstack1l1l11lll_opy_
  )
def bstack1lll11l111_opy_():
  global CONFIG
  if bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣻ") in CONFIG and not bool(CONFIG[bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣼ")]):
    del CONFIG[bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣽ")]
    return
  if not bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣾ") in CONFIG:
    CONFIG[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣿ")] = bstack1_opy_ (u"ࠨࠥࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫऀ")
  if bstack1_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨँ") in CONFIG[bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬं")]:
    bstack1l11lll11_opy_()
    os.environ[bstack1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨः")] = CONFIG[bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧऄ")]
  if not bstack1_opy_ (u"࠭ࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨअ") in CONFIG[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩआ")]:
    return
  bstack11l11l1l1_opy_ = bstack1_opy_ (u"ࠨࠩइ")
  bstack1lll1ll1_opy_ = bstack11ll11lll_opy_()
  if bstack1lll1ll1_opy_ != -1:
    bstack11l11l1l1_opy_ = bstack1_opy_ (u"ࠩࡆࡍࠥ࠭ई") + str(bstack1lll1ll1_opy_)
  if bstack11l11l1l1_opy_ == bstack1_opy_ (u"ࠪࠫउ"):
    bstack1l11l1l11_opy_ = bstack1lll1l111l_opy_(CONFIG[bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧऊ")])
    if bstack1l11l1l11_opy_ != -1:
      bstack11l11l1l1_opy_ = str(bstack1l11l1l11_opy_)
  if bstack11l11l1l1_opy_:
    bstack11111l11l_opy_(bstack11l11l1l1_opy_)
    os.environ[bstack1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩऋ")] = CONFIG[bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨऌ")]
def bstack1ll1l1111_opy_(bstack1llll1ll11_opy_, bstack1ll1111l_opy_, path):
  bstack1ll1llll1_opy_ = {
    bstack1_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫऍ"): bstack1ll1111l_opy_
  }
  if os.path.exists(path):
    bstack11llll1l1_opy_ = json.load(open(path, bstack1_opy_ (u"ࠨࡴࡥࠫऎ")))
  else:
    bstack11llll1l1_opy_ = {}
  bstack11llll1l1_opy_[bstack1llll1ll11_opy_] = bstack1ll1llll1_opy_
  with open(path, bstack1_opy_ (u"ࠤࡺ࠯ࠧए")) as outfile:
    json.dump(bstack11llll1l1_opy_, outfile)
def bstack1lll1l111l_opy_(bstack1llll1ll11_opy_):
  bstack1llll1ll11_opy_ = str(bstack1llll1ll11_opy_)
  bstack11l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠪࢂࠬऐ")), bstack1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫऑ"))
  try:
    if not os.path.exists(bstack11l1l1l1_opy_):
      os.makedirs(bstack11l1l1l1_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠬࢄࠧऒ")), bstack1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ओ"), bstack1_opy_ (u"ࠧ࠯ࡤࡸ࡭ࡱࡪ࠭࡯ࡣࡰࡩ࠲ࡩࡡࡤࡪࡨ࠲࡯ࡹ࡯࡯ࠩऔ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1_opy_ (u"ࠨࡹࠪक")):
        pass
      with open(file_path, bstack1_opy_ (u"ࠤࡺ࠯ࠧख")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1_opy_ (u"ࠪࡶࠬग")) as bstack111l11111_opy_:
      bstack11ll11l11_opy_ = json.load(bstack111l11111_opy_)
    if bstack1llll1ll11_opy_ in bstack11ll11l11_opy_:
      bstack11l1ll11l_opy_ = bstack11ll11l11_opy_[bstack1llll1ll11_opy_][bstack1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨघ")]
      bstack1l111ll1l_opy_ = int(bstack11l1ll11l_opy_) + 1
      bstack1ll1l1111_opy_(bstack1llll1ll11_opy_, bstack1l111ll1l_opy_, file_path)
      return bstack1l111ll1l_opy_
    else:
      bstack1ll1l1111_opy_(bstack1llll1ll11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1lll111lll_opy_.format(str(e)))
    return -1
def bstack1l111lll_opy_(config):
  if not config[bstack1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧङ")] or not config[bstack1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩच")]:
    return True
  else:
    return False
def bstack11l11l11_opy_(config, index=0):
  global bstack11111111_opy_
  bstack1lll1lll11_opy_ = {}
  caps = bstack1lll1l1l_opy_ + bstack111lllll1_opy_
  if bstack11111111_opy_:
    caps += bstack111111111_opy_
  for key in config:
    if key in caps + [bstack1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪछ")]:
      continue
    bstack1lll1lll11_opy_[key] = config[key]
  if bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज") in config:
    for bstack1lll1l1l1_opy_ in config[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬझ")][index]:
      if bstack1lll1l1l1_opy_ in caps + [bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨञ"), bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬट")]:
        continue
      bstack1lll1lll11_opy_[bstack1lll1l1l1_opy_] = config[bstack1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨठ")][index][bstack1lll1l1l1_opy_]
  bstack1lll1lll11_opy_[bstack1_opy_ (u"࠭ࡨࡰࡵࡷࡒࡦࡳࡥࠨड")] = socket.gethostname()
  if bstack1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨढ") in bstack1lll1lll11_opy_:
    del (bstack1lll1lll11_opy_[bstack1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩण")])
  return bstack1lll1lll11_opy_
def bstack1111l1ll1_opy_(config):
  global bstack11111111_opy_
  bstack1ll1l1l11l_opy_ = {}
  caps = bstack111lllll1_opy_
  if bstack11111111_opy_:
    caps += bstack111111111_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1l11l_opy_[key] = config[key]
  return bstack1ll1l1l11l_opy_
def bstack1ll1l1ll1_opy_(bstack1lll1lll11_opy_, bstack1ll1l1l11l_opy_):
  bstack11llllll1_opy_ = {}
  for key in bstack1lll1lll11_opy_.keys():
    if key in bstack1l11l11l_opy_:
      bstack11llllll1_opy_[bstack1l11l11l_opy_[key]] = bstack1lll1lll11_opy_[key]
    else:
      bstack11llllll1_opy_[key] = bstack1lll1lll11_opy_[key]
  for key in bstack1ll1l1l11l_opy_:
    if key in bstack1l11l11l_opy_:
      bstack11llllll1_opy_[bstack1l11l11l_opy_[key]] = bstack1ll1l1l11l_opy_[key]
    else:
      bstack11llllll1_opy_[key] = bstack1ll1l1l11l_opy_[key]
  return bstack11llllll1_opy_
def bstack11ll1l1l_opy_(config, index=0):
  global bstack11111111_opy_
  config = copy.deepcopy(config)
  caps = {}
  bstack1ll1l1l11l_opy_ = bstack1111l1ll1_opy_(config)
  bstack1l11lll1_opy_ = bstack111lllll1_opy_
  bstack1l11lll1_opy_ += bstack1lll1ll11l_opy_
  if bstack11111111_opy_:
    bstack1l11lll1_opy_ += bstack111111111_opy_
  if bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬत") in config:
    if bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨथ") in config[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧद")][index]:
      caps[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪध")] = config[bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩन")][index][bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬऩ")]
    if bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩप") in config[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬफ")][index]:
      caps[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫब")] = str(config[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧभ")][index][bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭म")])
    bstack1l1ll111l_opy_ = {}
    for bstack1ll1ll11ll_opy_ in bstack1l11lll1_opy_:
      if bstack1ll1ll11ll_opy_ in config[bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩय")][index]:
        if bstack1ll1ll11ll_opy_ == bstack1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩर"):
          try:
            bstack1l1ll111l_opy_[bstack1ll1ll11ll_opy_] = str(config[bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऱ")][index][bstack1ll1ll11ll_opy_] * 1.0)
          except:
            bstack1l1ll111l_opy_[bstack1ll1ll11ll_opy_] = str(config[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬल")][index][bstack1ll1ll11ll_opy_])
        else:
          bstack1l1ll111l_opy_[bstack1ll1ll11ll_opy_] = config[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ळ")][index][bstack1ll1ll11ll_opy_]
        del (config[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऴ")][index][bstack1ll1ll11ll_opy_])
    bstack1ll1l1l11l_opy_ = update(bstack1ll1l1l11l_opy_, bstack1l1ll111l_opy_)
  bstack1lll1lll11_opy_ = bstack11l11l11_opy_(config, index)
  for bstack1l111l111_opy_ in bstack111lllll1_opy_ + [bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪव"), bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧश")]:
    if bstack1l111l111_opy_ in bstack1lll1lll11_opy_:
      bstack1ll1l1l11l_opy_[bstack1l111l111_opy_] = bstack1lll1lll11_opy_[bstack1l111l111_opy_]
      del (bstack1lll1lll11_opy_[bstack1l111l111_opy_])
  if bstack1111llll1_opy_(config):
    bstack1lll1lll11_opy_[bstack1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧष")] = True
    caps.update(bstack1ll1l1l11l_opy_)
    caps[bstack1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩस")] = bstack1lll1lll11_opy_
  else:
    bstack1lll1lll11_opy_[bstack1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩह")] = False
    caps.update(bstack1ll1l1ll1_opy_(bstack1lll1lll11_opy_, bstack1ll1l1l11l_opy_))
    if bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऺ") in caps:
      caps[bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬऻ")] = caps[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧ़ࠪ")]
      del (caps[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫऽ")])
    if bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨा") in caps:
      caps[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪि")] = caps[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪी")]
      del (caps[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫु")])
  return caps
def bstack1lll1l1111_opy_():
  global bstack111111l1l_opy_
  if bstack1ll111ll1_opy_() <= version.parse(bstack1_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫू")):
    if bstack111111l1l_opy_ != bstack1_opy_ (u"ࠬ࠭ृ"):
      return bstack1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢॄ") + bstack111111l1l_opy_ + bstack1_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦॅ")
    return bstack11lll1lll_opy_
  if bstack111111l1l_opy_ != bstack1_opy_ (u"ࠨࠩॆ"):
    return bstack1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦे") + bstack111111l1l_opy_ + bstack1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦै")
  return bstack1l1lll1l1_opy_
def bstack1l1l11111_opy_(options):
  return hasattr(options, bstack1_opy_ (u"ࠫࡸ࡫ࡴࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠬॉ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1lllll111l_opy_(options, bstack1llll11l1_opy_):
  for bstack1ll1l1ll_opy_ in bstack1llll11l1_opy_:
    if bstack1ll1l1ll_opy_ in [bstack1_opy_ (u"ࠬࡧࡲࡨࡵࠪॊ"), bstack1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪो")]:
      continue
    if bstack1ll1l1ll_opy_ in options._experimental_options:
      options._experimental_options[bstack1ll1l1ll_opy_] = update(options._experimental_options[bstack1ll1l1ll_opy_],
                                                         bstack1llll11l1_opy_[bstack1ll1l1ll_opy_])
    else:
      options.add_experimental_option(bstack1ll1l1ll_opy_, bstack1llll11l1_opy_[bstack1ll1l1ll_opy_])
  if bstack1_opy_ (u"ࠧࡢࡴࡪࡷࠬौ") in bstack1llll11l1_opy_:
    for arg in bstack1llll11l1_opy_[bstack1_opy_ (u"ࠨࡣࡵ࡫ࡸ्࠭")]:
      options.add_argument(arg)
    del (bstack1llll11l1_opy_[bstack1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧॎ")])
  if bstack1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧॏ") in bstack1llll11l1_opy_:
    for ext in bstack1llll11l1_opy_[bstack1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨॐ")]:
      options.add_extension(ext)
    del (bstack1llll11l1_opy_[bstack1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ॑")])
def bstack1lll11l1_opy_(options, bstack1l111l11l_opy_):
  if bstack1_opy_ (u"࠭ࡰࡳࡧࡩࡷ॒ࠬ") in bstack1l111l11l_opy_:
    for bstack1llll111l_opy_ in bstack1l111l11l_opy_[bstack1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭॓")]:
      if bstack1llll111l_opy_ in options._preferences:
        options._preferences[bstack1llll111l_opy_] = update(options._preferences[bstack1llll111l_opy_], bstack1l111l11l_opy_[bstack1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ॔")][bstack1llll111l_opy_])
      else:
        options.set_preference(bstack1llll111l_opy_, bstack1l111l11l_opy_[bstack1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨॕ")][bstack1llll111l_opy_])
  if bstack1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨॖ") in bstack1l111l11l_opy_:
    for arg in bstack1l111l11l_opy_[bstack1_opy_ (u"ࠫࡦࡸࡧࡴࠩॗ")]:
      options.add_argument(arg)
def bstack11111l11_opy_(options, bstack11l111lll_opy_):
  if bstack1_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭क़") in bstack11l111lll_opy_:
    options.use_webview(bool(bstack11l111lll_opy_[bstack1_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧख़")]))
  bstack1lllll111l_opy_(options, bstack11l111lll_opy_)
def bstack1ll11l1l1_opy_(options, bstack1ll1lll11_opy_):
  for bstack1l111ll11_opy_ in bstack1ll1lll11_opy_:
    if bstack1l111ll11_opy_ in [bstack1_opy_ (u"ࠧࡵࡧࡦ࡬ࡳࡵ࡬ࡰࡩࡼࡔࡷ࡫ࡶࡪࡧࡺࠫग़"), bstack1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ज़")]:
      continue
    options.set_capability(bstack1l111ll11_opy_, bstack1ll1lll11_opy_[bstack1l111ll11_opy_])
  if bstack1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧड़") in bstack1ll1lll11_opy_:
    for arg in bstack1ll1lll11_opy_[bstack1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨढ़")]:
      options.add_argument(arg)
  if bstack1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨफ़") in bstack1ll1lll11_opy_:
    options.bstack1llll1l1_opy_(bool(bstack1ll1lll11_opy_[bstack1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩय़")]))
def bstack11l1l1111_opy_(options, bstack11l11ll11_opy_):
  for bstack1ll11ll11_opy_ in bstack11l11ll11_opy_:
    if bstack1ll11ll11_opy_ in [bstack1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॠ"), bstack1_opy_ (u"ࠧࡢࡴࡪࡷࠬॡ")]:
      continue
    options._options[bstack1ll11ll11_opy_] = bstack11l11ll11_opy_[bstack1ll11ll11_opy_]
  if bstack1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॢ") in bstack11l11ll11_opy_:
    for bstack11l1lll11_opy_ in bstack11l11ll11_opy_[bstack1_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ॣ")]:
      options.bstack1ll11l1l_opy_(
        bstack11l1lll11_opy_, bstack11l11ll11_opy_[bstack1_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ।")][bstack11l1lll11_opy_])
  if bstack1_opy_ (u"ࠫࡦࡸࡧࡴࠩ॥") in bstack11l11ll11_opy_:
    for arg in bstack11l11ll11_opy_[bstack1_opy_ (u"ࠬࡧࡲࡨࡵࠪ०")]:
      options.add_argument(arg)
def bstack1l11l1111_opy_(options, caps):
  if not hasattr(options, bstack1_opy_ (u"࠭ࡋࡆ࡛ࠪ१")):
    return
  if options.KEY == bstack1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ२") and options.KEY in caps:
    bstack1lllll111l_opy_(options, caps[bstack1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭३")])
  elif options.KEY == bstack1_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧ४") and options.KEY in caps:
    bstack1lll11l1_opy_(options, caps[bstack1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨ५")])
  elif options.KEY == bstack1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬ६") and options.KEY in caps:
    bstack1ll11l1l1_opy_(options, caps[bstack1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭७")])
  elif options.KEY == bstack1_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ८") and options.KEY in caps:
    bstack11111l11_opy_(options, caps[bstack1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ९")])
  elif options.KEY == bstack1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ॰") and options.KEY in caps:
    bstack11l1l1111_opy_(options, caps[bstack1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨॱ")])
def bstack11l111ll_opy_(caps):
  global bstack11111111_opy_
  if isinstance(os.environ.get(bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫॲ")), str):
    bstack11111111_opy_ = eval(os.getenv(bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬॳ")))
  if bstack11111111_opy_:
    if bstack1111l111_opy_() < version.parse(bstack1_opy_ (u"ࠬ࠸࠮࠴࠰࠳ࠫॴ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ॵ")
    if bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬॶ") in caps:
      browser = caps[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ॷ")]
    elif bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॸ") in caps:
      browser = caps[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫॹ")]
    browser = str(browser).lower()
    if browser == bstack1_opy_ (u"ࠫ࡮ࡶࡨࡰࡰࡨࠫॺ") or browser == bstack1_opy_ (u"ࠬ࡯ࡰࡢࡦࠪॻ"):
      browser = bstack1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ॼ")
    if browser == bstack1_opy_ (u"ࠧࡴࡣࡰࡷࡺࡴࡧࠨॽ"):
      browser = bstack1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨॾ")
    if browser not in [bstack1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩॿ"), bstack1_opy_ (u"ࠪࡩࡩ࡭ࡥࠨঀ"), bstack1_opy_ (u"ࠫ࡮࡫ࠧঁ"), bstack1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬং"), bstack1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧঃ")]:
      return None
    try:
      package = bstack1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶ࠳ࢁࡽ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ঄").format(browser)
      name = bstack1_opy_ (u"ࠨࡑࡳࡸ࡮ࡵ࡮ࡴࠩঅ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l1l11111_opy_(options):
        return None
      for bstack1l111l111_opy_ in caps.keys():
        options.set_capability(bstack1l111l111_opy_, caps[bstack1l111l111_opy_])
      bstack1l11l1111_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1111_opy_(options, bstack1l11ll1ll_opy_):
  if not bstack1l1l11111_opy_(options):
    return
  for bstack1l111l111_opy_ in bstack1l11ll1ll_opy_.keys():
    if bstack1l111l111_opy_ in bstack1lll1ll11l_opy_:
      continue
    if bstack1l111l111_opy_ in options._caps and type(options._caps[bstack1l111l111_opy_]) in [dict, list]:
      options._caps[bstack1l111l111_opy_] = update(options._caps[bstack1l111l111_opy_], bstack1l11ll1ll_opy_[bstack1l111l111_opy_])
    else:
      options.set_capability(bstack1l111l111_opy_, bstack1l11ll1ll_opy_[bstack1l111l111_opy_])
  bstack1l11l1111_opy_(options, bstack1l11ll1ll_opy_)
  if bstack1_opy_ (u"ࠩࡰࡳࡿࡀࡤࡦࡤࡸ࡫࡬࡫ࡲࡂࡦࡧࡶࡪࡹࡳࠨআ") in options._caps:
    if options._caps[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨই")] and options._caps[bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩঈ")].lower() != bstack1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭উ"):
      del options._caps[bstack1_opy_ (u"࠭࡭ࡰࡼ࠽ࡨࡪࡨࡵࡨࡩࡨࡶࡆࡪࡤࡳࡧࡶࡷࠬঊ")]
def bstack1l1ll11ll_opy_(proxy_config):
  if bstack1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫঋ") in proxy_config:
    proxy_config[bstack1_opy_ (u"ࠨࡵࡶࡰࡕࡸ࡯ࡹࡻࠪঌ")] = proxy_config[bstack1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭঍")]
    del (proxy_config[bstack1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ঎")])
  if bstack1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧএ") in proxy_config and proxy_config[bstack1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨঐ")].lower() != bstack1_opy_ (u"࠭ࡤࡪࡴࡨࡧࡹ࠭঑"):
    proxy_config[bstack1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪ঒")] = bstack1_opy_ (u"ࠨ࡯ࡤࡲࡺࡧ࡬ࠨও")
  if bstack1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡂࡷࡷࡳࡨࡵ࡮ࡧ࡫ࡪ࡙ࡷࡲࠧঔ") in proxy_config:
    proxy_config[bstack1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭ক")] = bstack1_opy_ (u"ࠫࡵࡧࡣࠨখ")
  return proxy_config
def bstack111l111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫগ") in config:
    return proxy
  config[bstack1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬঘ")] = bstack1l1ll11ll_opy_(config[bstack1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ঙ")])
  if proxy == None:
    proxy = Proxy(config[bstack1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧচ")])
  return proxy
def bstack1l1l1ll11_opy_(self):
  global CONFIG
  global bstack11l11l11l_opy_
  try:
    proxy = bstack1lll11lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧছ")):
        proxies = bstack1lll1lll1l_opy_(proxy, bstack1lll1l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1ll11_opy_ = proxies.popitem()
          if bstack1_opy_ (u"ࠥ࠾࠴࠵ࠢজ") in bstack111l1ll11_opy_:
            return bstack111l1ll11_opy_
          else:
            return bstack1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧঝ") + bstack111l1ll11_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡲࡵࡳࡽࡿࠠࡶࡴ࡯ࠤ࠿ࠦࡻࡾࠤঞ").format(str(e)))
  return bstack11l11l11l_opy_(self)
def bstack1l11111l_opy_():
  global CONFIG
  return bstack11ll11l1l_opy_(CONFIG) and bstack1ll111ll1_opy_() >= version.parse(bstack1l11ll11l_opy_)
def bstack1l11l1l1l_opy_(config):
  bstack1llllllll_opy_ = {}
  if bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪট") in config:
    bstack1llllllll_opy_ = config[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫঠ")]
  if bstack1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧড") in config:
    bstack1llllllll_opy_ = config[bstack1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨঢ")]
  proxy = bstack1lll11lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨণ")) and os.path.isfile(proxy):
      bstack1llllllll_opy_[bstack1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧত")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪথ")):
        proxies = bstack1111111l1_opy_(config, bstack1lll1l1111_opy_())
        if len(proxies) > 0:
          protocol, bstack111l1ll11_opy_ = proxies.popitem()
          if bstack1_opy_ (u"ࠨ࠺࠰࠱ࠥদ") in bstack111l1ll11_opy_:
            parsed_url = urlparse(bstack111l1ll11_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1_opy_ (u"ࠢ࠻࠱࠲ࠦধ") + bstack111l1ll11_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1llllllll_opy_[bstack1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫন")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1llllllll_opy_[bstack1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬ঩")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1llllllll_opy_[bstack1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭প")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1llllllll_opy_[bstack1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧফ")] = str(parsed_url.password)
  return bstack1llllllll_opy_
def bstack11l1l111l_opy_(config):
  if bstack1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪব") in config:
    return config[bstack1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫভ")]
  return {}
def bstack11ll1l11l_opy_(caps):
  global bstack1ll1l111l_opy_
  if bstack1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨম") in caps:
    caps[bstack1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩয")][bstack1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨর")] = True
    if bstack1ll1l111l_opy_:
      caps[bstack1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ঱")][bstack1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ল")] = bstack1ll1l111l_opy_
  else:
    caps[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ঳")] = True
    if bstack1ll1l111l_opy_:
      caps[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঴")] = bstack1ll1l111l_opy_
def bstack1l1ll1l1l_opy_():
  global CONFIG
  if bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ঵") in CONFIG and CONFIG[bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬশ")]:
    bstack1llllllll_opy_ = bstack1l11l1l1l_opy_(CONFIG)
    bstack11ll1l111_opy_(CONFIG[bstack1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬষ")], bstack1llllllll_opy_)
def bstack11ll1l111_opy_(key, bstack1llllllll_opy_):
  global bstack1llllll11l_opy_
  logger.info(bstack11l1ll11_opy_)
  try:
    bstack1llllll11l_opy_ = Local()
    bstack111l1111l_opy_ = {bstack1_opy_ (u"ࠪ࡯ࡪࡿࠧস"): key}
    bstack111l1111l_opy_.update(bstack1llllllll_opy_)
    logger.debug(bstack11l1111l_opy_.format(str(bstack111l1111l_opy_)))
    bstack1llllll11l_opy_.start(**bstack111l1111l_opy_)
    if bstack1llllll11l_opy_.isRunning():
      logger.info(bstack1ll111ll_opy_)
  except Exception as e:
    bstack11lllllll_opy_(bstack1l111lll1_opy_.format(str(e)))
def bstack11l1111ll_opy_():
  global bstack1llllll11l_opy_
  if bstack1llllll11l_opy_.isRunning():
    logger.info(bstack11lll1ll1_opy_)
    bstack1llllll11l_opy_.stop()
  bstack1llllll11l_opy_ = None
def bstack11l111l1_opy_(bstack1ll1ll1lll_opy_=[]):
  global CONFIG
  bstack1lllllll11_opy_ = []
  bstack1llll1l1l_opy_ = [bstack1_opy_ (u"ࠫࡴࡹࠧহ"), bstack1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ঺"), bstack1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ঻"), bstack1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯়ࠩ"), bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ঽ"), bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪা")]
  try:
    for err in bstack1ll1ll1lll_opy_:
      bstack1ll111lll_opy_ = {}
      for k in bstack1llll1l1l_opy_:
        val = CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ি")][int(err[bstack1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪী")])].get(k)
        if val:
          bstack1ll111lll_opy_[k] = val
      bstack1ll111lll_opy_[bstack1_opy_ (u"ࠬࡺࡥࡴࡶࡶࠫু")] = {
        err[bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫূ")]: err[bstack1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ৃ")]
      }
      bstack1lllllll11_opy_.append(bstack1ll111lll_opy_)
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪࡴࡸ࡭ࡢࡶࡷ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠻ࠢࠪৄ") + str(e))
  finally:
    return bstack1lllllll11_opy_
def bstack1lll1l1l1l_opy_():
  global bstack1ll111l1_opy_
  global bstack1111ll111_opy_
  global bstack11111ll11_opy_
  if bstack1ll111l1_opy_:
    logger.warning(bstack111l11ll1_opy_.format(str(bstack1ll111l1_opy_)))
  else:
    try:
      bstack11llll1l1_opy_ = bstack11lllll1_opy_(bstack1_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨ৅"), logger)
      if bstack11llll1l1_opy_.get(bstack1_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨ৆")) and bstack11llll1l1_opy_.get(bstack1_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩে")).get(bstack1_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧৈ")):
        logger.warning(bstack111l11ll1_opy_.format(str(bstack11llll1l1_opy_[bstack1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫ৉")][bstack1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩ৊")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1llll1l1l1_opy_)
  global bstack1llllll11l_opy_
  if bstack1llllll11l_opy_:
    bstack11l1111ll_opy_()
  try:
    for driver in bstack1111ll111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1lll1l11ll_opy_)
  bstack111llll1_opy_()
  if len(bstack11111ll11_opy_) > 0:
    message = bstack11l111l1_opy_(bstack11111ll11_opy_)
    bstack111llll1_opy_(message)
  else:
    bstack111llll1_opy_()
  bstack11111lll_opy_(bstack111lllll_opy_, logger)
def bstack1lllll11l_opy_(self, *args):
  logger.error(bstack1lll1llll_opy_)
  bstack1lll1l1l1l_opy_()
  sys.exit(1)
def bstack11lllllll_opy_(err):
  logger.critical(bstack1ll1ll11l1_opy_.format(str(err)))
  bstack111llll1_opy_(bstack1ll1ll11l1_opy_.format(str(err)))
  atexit.unregister(bstack1lll1l1l1l_opy_)
  sys.exit(1)
def bstack11111l1ll_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111llll1_opy_(message)
  atexit.unregister(bstack1lll1l1l1l_opy_)
  sys.exit(1)
def bstack1111llll_opy_():
  global CONFIG
  global bstack1l11l111_opy_
  global bstack1lllll1ll1_opy_
  global bstack1ll1l11l_opy_
  CONFIG = bstack1ll1l1l1_opy_()
  bstack11llll11l_opy_()
  bstack1ll1111ll_opy_()
  CONFIG = bstack1l111l1l_opy_(CONFIG)
  update(CONFIG, bstack1lllll1ll1_opy_)
  update(CONFIG, bstack1l11l111_opy_)
  CONFIG = bstack1l11111ll_opy_(CONFIG)
  bstack1ll1l11l_opy_ = bstack11l1lllll_opy_(CONFIG)
  bstack1ll1l11l1_opy_.bstack1ll1l1l1l1_opy_(bstack1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩো"), bstack1ll1l11l_opy_)
  if (bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬৌ") in CONFIG and bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ্࠭") in bstack1l11l111_opy_) or (
          bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧৎ") in CONFIG and bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ৏") not in bstack1lllll1ll1_opy_):
    if os.getenv(bstack1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ৐")):
      CONFIG[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৑")] = os.getenv(bstack1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬ৒"))
    else:
      bstack1lll11l111_opy_()
  elif (bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৓") not in CONFIG and bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔") in CONFIG) or (
          bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ৕") in bstack1lllll1ll1_opy_ and bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ৖") not in bstack1l11l111_opy_):
    del (CONFIG[bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨৗ")])
  if bstack1l111lll_opy_(CONFIG):
    bstack11lllllll_opy_(bstack111l11l1l_opy_)
  bstack1ll11l11l_opy_()
  bstack11lll11l_opy_()
  if bstack11111111_opy_:
    CONFIG[bstack1_opy_ (u"ࠧࡢࡲࡳࠫ৘")] = bstack1l1l1ll1l_opy_(CONFIG)
    logger.info(bstack1lll11l1l1_opy_.format(CONFIG[bstack1_opy_ (u"ࠨࡣࡳࡴࠬ৙")]))
def bstack11ll1lll_opy_(config, bstack11l11111_opy_):
  global CONFIG
  global bstack11111111_opy_
  CONFIG = config
  bstack11111111_opy_ = bstack11l11111_opy_
def bstack11lll11l_opy_():
  global CONFIG
  global bstack11111111_opy_
  if bstack1_opy_ (u"ࠩࡤࡴࡵ࠭৚") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack1ll1l11ll_opy_)
    bstack11111111_opy_ = True
    bstack1ll1l11l1_opy_.bstack1ll1l1l1l1_opy_(bstack1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ৛"), True)
def bstack1l1l1ll1l_opy_(config):
  bstack11l1llll1_opy_ = bstack1_opy_ (u"ࠫࠬড়")
  app = config[bstack1_opy_ (u"ࠬࡧࡰࡱࠩঢ়")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll1l111_opy_:
      if os.path.exists(app):
        bstack11l1llll1_opy_ = bstack1l1l11l1_opy_(config, app)
      elif bstack1l1ll11l1_opy_(app):
        bstack11l1llll1_opy_ = app
      else:
        bstack11lllllll_opy_(bstack1l11ll1l_opy_.format(app))
    else:
      if bstack1l1ll11l1_opy_(app):
        bstack11l1llll1_opy_ = app
      elif os.path.exists(app):
        bstack11l1llll1_opy_ = bstack1l1l11l1_opy_(app)
      else:
        bstack11lllllll_opy_(bstack1l1111l11_opy_)
  else:
    if len(app) > 2:
      bstack11lllllll_opy_(bstack111ll1111_opy_)
    elif len(app) == 2:
      if bstack1_opy_ (u"࠭ࡰࡢࡶ࡫ࠫ৞") in app and bstack1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦࠪয়") in app:
        if os.path.exists(app[bstack1_opy_ (u"ࠨࡲࡤࡸ࡭࠭ৠ")]):
          bstack11l1llll1_opy_ = bstack1l1l11l1_opy_(config, app[bstack1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧৡ")], app[bstack1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ৢ")])
        else:
          bstack11lllllll_opy_(bstack1l11ll1l_opy_.format(app))
      else:
        bstack11lllllll_opy_(bstack111ll1111_opy_)
    else:
      for key in app:
        if key in bstack1ll1l1l1l_opy_:
          if key == bstack1_opy_ (u"ࠫࡵࡧࡴࡩࠩৣ"):
            if os.path.exists(app[key]):
              bstack11l1llll1_opy_ = bstack1l1l11l1_opy_(config, app[key])
            else:
              bstack11lllllll_opy_(bstack1l11ll1l_opy_.format(app))
          else:
            bstack11l1llll1_opy_ = app[key]
        else:
          bstack11lllllll_opy_(bstack111lll1ll_opy_)
  return bstack11l1llll1_opy_
def bstack1l1ll11l1_opy_(bstack11l1llll1_opy_):
  import re
  bstack11l11ll1l_opy_ = re.compile(bstack1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧ৤"))
  bstack1llllll1l1_opy_ = re.compile(bstack1_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮࠴ࡡࡡ࠮ࡼࡄ࠱࡟࠶࠭࠺࡞ࡢ࠲ࡡ࠳࡝ࠫࠦࠥ৥"))
  if bstack1_opy_ (u"ࠧࡣࡵ࠽࠳࠴࠭০") in bstack11l1llll1_opy_ or re.fullmatch(bstack11l11ll1l_opy_, bstack11l1llll1_opy_) or re.fullmatch(bstack1llllll1l1_opy_, bstack11l1llll1_opy_):
    return True
  else:
    return False
def bstack1l1l11l1_opy_(config, path, bstack1ll1lll1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1_opy_ (u"ࠨࡴࡥࠫ১")).read()).hexdigest()
  bstack1ll11ll1l_opy_ = bstack1ll1l11lll_opy_(md5_hash)
  bstack11l1llll1_opy_ = None
  if bstack1ll11ll1l_opy_:
    logger.info(bstack11ll111ll_opy_.format(bstack1ll11ll1l_opy_, md5_hash))
    return bstack1ll11ll1l_opy_
  bstack1111lll1_opy_ = MultipartEncoder(
    fields={
      bstack1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࠧ২"): (os.path.basename(path), open(os.path.abspath(path), bstack1_opy_ (u"ࠪࡶࡧ࠭৩")), bstack1_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱ࡳࡰࡦ࡯࡮ࠨ৪")),
      bstack1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨ৫"): bstack1ll1lll1ll_opy_
    }
  )
  response = requests.post(bstack1ll1ll1ll1_opy_, data=bstack1111lll1_opy_,
                           headers={bstack1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ৬"): bstack1111lll1_opy_.content_type},
                           auth=(config[bstack1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ৭")], config[bstack1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ৮")]))
  try:
    res = json.loads(response.text)
    bstack11l1llll1_opy_ = res[bstack1_opy_ (u"ࠩࡤࡴࡵࡥࡵࡳ࡮ࠪ৯")]
    logger.info(bstack11l1l11l1_opy_.format(bstack11l1llll1_opy_))
    bstack111l1ll1_opy_(md5_hash, bstack11l1llll1_opy_)
  except ValueError as err:
    bstack11lllllll_opy_(bstack1l11l111l_opy_.format(str(err)))
  return bstack11l1llll1_opy_
def bstack1ll11l11l_opy_():
  global CONFIG
  global bstack111111ll1_opy_
  bstack1lll111l11_opy_ = 0
  bstack1l11111l1_opy_ = 1
  if bstack1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৰ") in CONFIG:
    bstack1l11111l1_opy_ = CONFIG[bstack1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫৱ")]
  if bstack1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৲") in CONFIG:
    bstack1lll111l11_opy_ = len(CONFIG[bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৳")])
  bstack111111ll1_opy_ = int(bstack1l11111l1_opy_) * int(bstack1lll111l11_opy_)
def bstack1ll1l11lll_opy_(md5_hash):
  bstack1ll1ll1l11_opy_ = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠧࡿࠩ৴")), bstack1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ৵"), bstack1_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ৶"))
  if os.path.exists(bstack1ll1ll1l11_opy_):
    bstack1lll11llll_opy_ = json.load(open(bstack1ll1ll1l11_opy_, bstack1_opy_ (u"ࠪࡶࡧ࠭৷")))
    if md5_hash in bstack1lll11llll_opy_:
      bstack1l1ll11l_opy_ = bstack1lll11llll_opy_[md5_hash]
      bstack1lll1111_opy_ = datetime.datetime.now()
      bstack1ll1l1lll_opy_ = datetime.datetime.strptime(bstack1l1ll11l_opy_[bstack1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ৸")], bstack1_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ৹"))
      if (bstack1lll1111_opy_ - bstack1ll1l1lll_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1ll11l_opy_[bstack1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ৺")]):
        return None
      return bstack1l1ll11l_opy_[bstack1_opy_ (u"ࠧࡪࡦࠪ৻")]
  else:
    return None
def bstack111l1ll1_opy_(md5_hash, bstack11l1llll1_opy_):
  bstack11l1l1l1_opy_ = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠨࢀࠪৼ")), bstack1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৽"))
  if not os.path.exists(bstack11l1l1l1_opy_):
    os.makedirs(bstack11l1l1l1_opy_)
  bstack1ll1ll1l11_opy_ = os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠪࢂࠬ৾")), bstack1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ৿"), bstack1_opy_ (u"ࠬࡧࡰࡱࡗࡳࡰࡴࡧࡤࡎࡆ࠸ࡌࡦࡹࡨ࠯࡬ࡶࡳࡳ࠭਀"))
  bstack11ll1ll1l_opy_ = {
    bstack1_opy_ (u"࠭ࡩࡥࠩਁ"): bstack11l1llll1_opy_,
    bstack1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪਂ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗࠬਃ")),
    bstack1_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ਄"): str(__version__)
  }
  if os.path.exists(bstack1ll1ll1l11_opy_):
    bstack1lll11llll_opy_ = json.load(open(bstack1ll1ll1l11_opy_, bstack1_opy_ (u"ࠪࡶࡧ࠭ਅ")))
  else:
    bstack1lll11llll_opy_ = {}
  bstack1lll11llll_opy_[md5_hash] = bstack11ll1ll1l_opy_
  with open(bstack1ll1ll1l11_opy_, bstack1_opy_ (u"ࠦࡼ࠱ࠢਆ")) as outfile:
    json.dump(bstack1lll11llll_opy_, outfile)
def bstack1ll1l1l111_opy_(self):
  return
def bstack1l1l1lll1_opy_(self):
  return
def bstack1lll1ll1ll_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1lll1lll_opy_(self):
  global bstack11ll11ll1_opy_
  global bstack1l11l1ll_opy_
  global bstack11l11l1ll_opy_
  try:
    if bstack1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਇ") in bstack11ll11ll1_opy_ and self.session_id != None:
      bstack11l1ll1ll_opy_ = bstack1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ਈ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧਉ")
      bstack11111llll_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫਊ"), bstack1_opy_ (u"ࠩࠪ਋"), bstack11l1ll1ll_opy_, bstack1_opy_ (u"ࠪ࠰ࠥ࠭਌").join(
        threading.current_thread().bstackTestErrorMessages), bstack1_opy_ (u"ࠫࠬ਍"), bstack1_opy_ (u"ࠬ࠭਎"))
      if self != None:
        self.execute_script(bstack11111llll_opy_)
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢਏ") + str(e))
  bstack11l11l1ll_opy_(self)
  self.session_id = None
def bstack1l11llll_opy_(self, *args, **kwargs):
  bstack1l1l111ll_opy_ = bstack1111ll1l_opy_(self, *args, **kwargs)
  bstack1l111l1ll_opy_.bstack1ll111l11_opy_(self)
  return bstack1l1l111ll_opy_
def bstack1l1l1l111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11l1ll_opy_
  global bstack1l111l11_opy_
  global bstack1l11l1lll_opy_
  global bstack1l111111l_opy_
  global bstack1lll1lll1_opy_
  global bstack11ll11ll1_opy_
  global bstack1111ll1l_opy_
  global bstack1111ll111_opy_
  global bstack1ll1ll111l_opy_
  CONFIG[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩਐ")] = str(bstack11ll11ll1_opy_) + str(__version__)
  command_executor = bstack1lll1l1111_opy_()
  logger.debug(bstack1l111ll1_opy_.format(command_executor))
  proxy = bstack111l111l_opy_(CONFIG, proxy)
  bstack11l1ll111_opy_ = 0 if bstack1l111l11_opy_ < 0 else bstack1l111l11_opy_
  try:
    if bstack1l111111l_opy_ is True:
      bstack11l1ll111_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1lll1_opy_ is True:
      bstack11l1ll111_opy_ = int(threading.current_thread().name)
  except:
    bstack11l1ll111_opy_ = 0
  bstack1l11ll1ll_opy_ = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll111_opy_)
  logger.debug(bstack1lllll1111_opy_.format(str(bstack1l11ll1ll_opy_)))
  if bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ਑") in CONFIG and CONFIG[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭਒")]:
    bstack11ll1l11l_opy_(bstack1l11ll1ll_opy_)
  if desired_capabilities:
    bstack1lll1l1ll_opy_ = bstack1l111l1l_opy_(desired_capabilities)
    bstack1lll1l1ll_opy_[bstack1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪਓ")] = bstack1111llll1_opy_(CONFIG)
    bstack1llll1l11l_opy_ = bstack11ll1l1l_opy_(bstack1lll1l1ll_opy_)
    if bstack1llll1l11l_opy_:
      bstack1l11ll1ll_opy_ = update(bstack1llll1l11l_opy_, bstack1l11ll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1111_opy_(options, bstack1l11ll1ll_opy_)
  if not options:
    options = bstack11l111ll_opy_(bstack1l11ll1ll_opy_)
  if proxy and bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਔ")):
    options.proxy(proxy)
  if options and bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫਕ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1ll111ll1_opy_() < version.parse(bstack1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਖ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1l11ll1ll_opy_)
  logger.info(bstack1l1lll1ll_opy_)
  if bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਗ")):
    bstack1111ll1l_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧਘ")):
    bstack1111ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਙ")):
    bstack1111ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1111ll1l_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1llll1llll_opy_ = bstack1_opy_ (u"ࠪࠫਚ")
    if bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬਛ")):
      bstack1llll1llll_opy_ = self.caps.get(bstack1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਜ"))
    else:
      bstack1llll1llll_opy_ = self.capabilities.get(bstack1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਝ"))
    if bstack1llll1llll_opy_:
      if bstack1ll111ll1_opy_() <= version.parse(bstack1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧਞ")):
        self.command_executor._url = bstack1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤਟ") + bstack111111l1l_opy_ + bstack1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨਠ")
      else:
        self.command_executor._url = bstack1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧਡ") + bstack1llll1llll_opy_ + bstack1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਢ")
      logger.debug(bstack111l11lll_opy_.format(bstack1llll1llll_opy_))
    else:
      logger.debug(bstack11lll1111_opy_.format(bstack1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਣ")))
  except Exception as e:
    logger.debug(bstack11lll1111_opy_.format(e))
  if bstack1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਤ") in bstack11ll11ll1_opy_:
    bstack1ll1ll11_opy_(bstack1l111l11_opy_, bstack1ll1ll111l_opy_)
  bstack1l11l1ll_opy_ = self.session_id
  if bstack1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧਥ") in bstack11ll11ll1_opy_ or bstack1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in bstack11ll11ll1_opy_:
    threading.current_thread().bstack1lll11ll_opy_ = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l111l1ll_opy_.bstack1ll111l11_opy_(self)
  bstack1111ll111_opy_.append(self)
  if bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬਧ") in CONFIG and bstack1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਨ") in CONFIG[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਩")][bstack11l1ll111_opy_]:
    bstack1l11l1lll_opy_ = CONFIG[bstack1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਪ")][bstack11l1ll111_opy_][bstack1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫਫ")]
  logger.debug(bstack1111ll11l_opy_.format(bstack1l11l1ll_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1lllll111_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1llll1111l_opy_
      if(bstack1_opy_ (u"ࠢࡪࡰࡧࡩࡽ࠴ࡪࡴࠤਬ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠨࢀࠪਭ")), bstack1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩਮ"), bstack1_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬਯ")), bstack1_opy_ (u"ࠫࡼ࠭ਰ")) as fp:
          fp.write(bstack1_opy_ (u"ࠧࠨ਱"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣਲ")))):
          with open(args[1], bstack1_opy_ (u"ࠧࡳࠩਲ਼")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1_opy_ (u"ࠨࡣࡶࡽࡳࡩࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡢࡲࡪࡽࡐࡢࡩࡨࠬࡨࡵ࡮ࡵࡧࡻࡸ࠱ࠦࡰࡢࡩࡨࠤࡂࠦࡶࡰ࡫ࡧࠤ࠵࠯ࠧ਴") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1llllllll1_opy_)
            lines.insert(1, bstack1llll1111_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦਵ")), bstack1_opy_ (u"ࠪࡻࠬਸ਼")) as bstack111l1l11_opy_:
              bstack111l1l11_opy_.writelines(lines)
        CONFIG[bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਷")] = str(bstack11ll11ll1_opy_) + str(__version__)
        bstack11l1ll111_opy_ = 0 if bstack1l111l11_opy_ < 0 else bstack1l111l11_opy_
        try:
          if bstack1l111111l_opy_ is True:
            bstack11l1ll111_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1lll1_opy_ is True:
            bstack11l1ll111_opy_ = int(threading.current_thread().name)
        except:
          bstack11l1ll111_opy_ = 0
        CONFIG[bstack1_opy_ (u"ࠧࡻࡳࡦ࡙࠶ࡇࠧਸ")] = False
        CONFIG[bstack1_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧਹ")] = True
        bstack1l11ll1ll_opy_ = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll111_opy_)
        logger.debug(bstack1lllll1111_opy_.format(str(bstack1l11ll1ll_opy_)))
        if CONFIG[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫ਺")]:
          bstack11ll1l11l_opy_(bstack1l11ll1ll_opy_)
        if bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਻") in CONFIG and bstack1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫਼ࠧ") in CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack11l1ll111_opy_]:
          bstack1l11l1lll_opy_ = CONFIG[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਾ")][bstack11l1ll111_opy_][bstack1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਿ")]
        args.append(os.path.join(os.path.expanduser(bstack1_opy_ (u"࠭ࡾࠨੀ")), bstack1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧੁ"), bstack1_opy_ (u"ࠨ࠰ࡶࡩࡸࡹࡩࡰࡰ࡬ࡨࡸ࠴ࡴࡹࡶࠪੂ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1l11ll1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1_opy_ (u"ࠤ࡬ࡲࡩ࡫ࡸࡠࡤࡶࡸࡦࡩ࡫࠯࡬ࡶࠦ੃"))
      bstack1llll1111l_opy_ = True
      return bstack111llll1l_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1ll1ll1l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l111l11_opy_
    global bstack1l11l1lll_opy_
    global bstack1l111111l_opy_
    global bstack1lll1lll1_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ੄")] = str(bstack11ll11ll1_opy_) + str(__version__)
    bstack11l1ll111_opy_ = 0 if bstack1l111l11_opy_ < 0 else bstack1l111l11_opy_
    try:
      if bstack1l111111l_opy_ is True:
        bstack11l1ll111_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1lll1_opy_ is True:
        bstack11l1ll111_opy_ = int(threading.current_thread().name)
    except:
      bstack11l1ll111_opy_ = 0
    CONFIG[bstack1_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ੅")] = True
    bstack1l11ll1ll_opy_ = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll111_opy_)
    logger.debug(bstack1lllll1111_opy_.format(str(bstack1l11ll1ll_opy_)))
    if CONFIG[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ੆")]:
      bstack11ll1l11l_opy_(bstack1l11ll1ll_opy_)
    if bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ") in CONFIG and bstack1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ") in CONFIG[bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")][bstack11l1ll111_opy_]:
      bstack1l11l1lll_opy_ = CONFIG[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੊")][bstack11l1ll111_opy_][bstack1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨੋ")]
    import urllib
    import json
    bstack1l1llll1_opy_ = bstack1_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭ੌ") + urllib.parse.quote(json.dumps(bstack1l11ll1ll_opy_))
    browser = self.connect(bstack1l1llll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1lllll1_opy_():
    global bstack1llll1111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1ll1l1_opy_
        bstack1llll1111l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1lllll111_opy_
      bstack1llll1111l_opy_ = True
    except Exception as e:
      pass
def bstack1l1l1l1ll_opy_(context, bstack1lll111l1l_opy_):
  try:
    context.page.evaluate(bstack1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨ੍"), bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪ੎")+ json.dumps(bstack1lll111l1l_opy_) + bstack1_opy_ (u"ࠢࡾࡿࠥ੏"))
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨ੐"), e)
def bstack111ll1l1l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥੑ"), bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ੒") + json.dumps(message) + bstack1_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧ੓") + json.dumps(level) + bstack1_opy_ (u"ࠬࢃࡽࠨ੔"))
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤ੕"), e)
def bstack11llll1l_opy_(context, status, message = bstack1_opy_ (u"ࠢࠣ੖")):
  try:
    if(status == bstack1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ੗")):
      context.page.evaluate(bstack1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ੘"), bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫਖ਼") + json.dumps(bstack1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨਗ਼") + str(message)) + bstack1_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩਜ਼") + json.dumps(status) + bstack1_opy_ (u"ࠨࡽࡾࠤੜ"))
    else:
      context.page.evaluate(bstack1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣ੝"), bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩਫ਼") + json.dumps(status) + bstack1_opy_ (u"ࠤࢀࢁࠧ੟"))
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢ੠"), e)
def bstack11ll1l1ll_opy_(self, url):
  global bstack111l1l11l_opy_
  try:
    bstack1llllll1ll_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1l11ll_opy_.format(str(err)))
  try:
    bstack111l1l11l_opy_(self, url)
  except Exception as e:
    try:
      bstack111lll111_opy_ = str(e)
      if any(err_msg in bstack111lll111_opy_ for err_msg in bstack11ll1ll11_opy_):
        bstack1llllll1ll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1l11ll_opy_.format(str(err)))
    raise e
def bstack11ll111l_opy_(self):
  global bstack11l11llll_opy_
  bstack11l11llll_opy_ = self
  return
def bstack1lll1lllll_opy_(self):
  global bstack1l11l1ll1_opy_
  bstack1l11l1ll1_opy_ = self
  return
def bstack1ll11lll_opy_(self, test):
  global CONFIG
  global bstack1l11l1ll1_opy_
  global bstack11l11llll_opy_
  global bstack1l11l1ll_opy_
  global bstack11lll111_opy_
  global bstack1l11l1lll_opy_
  global bstack111l1l1l_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack11l111l1l_opy_
  global bstack1111ll111_opy_
  try:
    if not bstack1l11l1ll_opy_:
      with open(os.path.join(os.path.expanduser(bstack1_opy_ (u"ࠫࢃ࠭੡")), bstack1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ੢"), bstack1_opy_ (u"࠭࠮ࡴࡧࡶࡷ࡮ࡵ࡮ࡪࡦࡶ࠲ࡹࡾࡴࠨ੣"))) as f:
        bstack1ll11lll1_opy_ = json.loads(bstack1_opy_ (u"ࠢࡼࠤ੤") + f.read().strip() + bstack1_opy_ (u"ࠨࠤࡻࠦ࠿ࠦࠢࡺࠤࠪ੥") + bstack1_opy_ (u"ࠤࢀࠦ੦"))
        bstack1l11l1ll_opy_ = bstack1ll11lll1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1111ll111_opy_:
    for driver in bstack1111ll111_opy_:
      if bstack1l11l1ll_opy_ == driver.session_id:
        if test:
          bstack111111l11_opy_ = str(test.data)
        if not bstack1llllll1l_opy_ and bstack111111l11_opy_:
          bstack1111l1ll_opy_ = {
            bstack1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪ੧"): bstack1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੨"),
            bstack1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੩"): {
              bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੪"): bstack111111l11_opy_
            }
          }
          bstack11l11ll1_opy_ = bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੫").format(json.dumps(bstack1111l1ll_opy_))
          driver.execute_script(bstack11l11ll1_opy_)
        if bstack11lll111_opy_:
          bstack11l1l1l1l_opy_ = {
            bstack1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੬"): bstack1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੭"),
            bstack1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੮"): {
              bstack1_opy_ (u"ࠫࡩࡧࡴࡢࠩ੯"): bstack111111l11_opy_ + bstack1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧੰ"),
              bstack1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬੱ"): bstack1_opy_ (u"ࠧࡪࡰࡩࡳࠬੲ")
            }
          }
          bstack1111l1ll_opy_ = {
            bstack1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨੳ"): bstack1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬੴ"),
            bstack1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ੵ"): {
              bstack1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੶"): bstack1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ੷")
            }
          }
          if bstack11lll111_opy_.status == bstack1_opy_ (u"࠭ࡐࡂࡕࡖࠫ੸"):
            bstack1lll111ll1_opy_ = bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack11l1l1l1l_opy_))
            driver.execute_script(bstack1lll111ll1_opy_)
            bstack11l11ll1_opy_ = bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭੺").format(json.dumps(bstack1111l1ll_opy_))
            driver.execute_script(bstack11l11ll1_opy_)
          elif bstack11lll111_opy_.status == bstack1_opy_ (u"ࠩࡉࡅࡎࡒࠧ੻"):
            reason = bstack1_opy_ (u"ࠥࠦ੼")
            bstack11l1l11l_opy_ = bstack111111l11_opy_ + bstack1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬ੽")
            if bstack11lll111_opy_.message:
              reason = str(bstack11lll111_opy_.message)
              bstack11l1l11l_opy_ = bstack11l1l11l_opy_ + bstack1_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ੾") + reason
            bstack11l1l1l1l_opy_[bstack1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੿")] = {
              bstack1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭઀"): bstack1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧઁ"),
              bstack1_opy_ (u"ࠩࡧࡥࡹࡧࠧં"): bstack11l1l11l_opy_
            }
            bstack1111l1ll_opy_[bstack1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ઃ")] = {
              bstack1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ઄"): bstack1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬઅ"),
              bstack1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭આ"): reason
            }
            bstack1lll111ll1_opy_ = bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬઇ").format(json.dumps(bstack11l1l1l1l_opy_))
            driver.execute_script(bstack1lll111ll1_opy_)
            bstack11l11ll1_opy_ = bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ઈ").format(json.dumps(bstack1111l1ll_opy_))
            driver.execute_script(bstack11l11ll1_opy_)
  elif bstack1l11l1ll_opy_:
    try:
      data = {}
      bstack111111l11_opy_ = None
      if test:
        bstack111111l11_opy_ = str(test.data)
      if not bstack1llllll1l_opy_ and bstack111111l11_opy_:
        data[bstack1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧઉ")] = bstack111111l11_opy_
      if bstack11lll111_opy_:
        if bstack11lll111_opy_.status == bstack1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨઊ"):
          data[bstack1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઋ")] = bstack1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬઌ")
        elif bstack11lll111_opy_.status == bstack1_opy_ (u"࠭ࡆࡂࡋࡏࠫઍ"):
          data[bstack1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ઎")] = bstack1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨએ")
          if bstack11lll111_opy_.message:
            data[bstack1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩઐ")] = str(bstack11lll111_opy_.message)
      user = CONFIG[bstack1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬઑ")]
      key = CONFIG[bstack1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ઒")]
      url = bstack1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪઓ").format(user, key, bstack1l11l1ll_opy_)
      headers = {
        bstack1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬઔ"): bstack1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪક"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1l1ll11_opy_.format(str(e)))
  if bstack1l11l1ll1_opy_:
    bstack1ll1l1l1ll_opy_(bstack1l11l1ll1_opy_)
  if bstack11l11llll_opy_:
    bstack11l111l1l_opy_(bstack11l11llll_opy_)
  bstack111l1l1l_opy_(self, test)
def bstack1111l1l1l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack11ll1l1l1_opy_
  bstack11ll1l1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11lll111_opy_
  bstack11lll111_opy_ = self._test
def bstack111ll11l_opy_():
  global bstack11111l111_opy_
  try:
    if os.path.exists(bstack11111l111_opy_):
      os.remove(bstack11111l111_opy_)
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡨࡪࡲࡥࡵ࡫ࡱ࡫ࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫખ") + str(e))
def bstack1ll1llll11_opy_():
  global bstack11111l111_opy_
  bstack11llll1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack11111l111_opy_):
      with open(bstack11111l111_opy_, bstack1_opy_ (u"ࠩࡺࠫગ")):
        pass
      with open(bstack11111l111_opy_, bstack1_opy_ (u"ࠥࡻ࠰ࠨઘ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11111l111_opy_):
      bstack11llll1l1_opy_ = json.load(open(bstack11111l111_opy_, bstack1_opy_ (u"ࠫࡷࡨࠧઙ")))
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡳࡧࡤࡨ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧચ") + str(e))
  finally:
    return bstack11llll1l1_opy_
def bstack1ll1ll11_opy_(platform_index, item_index):
  global bstack11111l111_opy_
  try:
    bstack11llll1l1_opy_ = bstack1ll1llll11_opy_()
    bstack11llll1l1_opy_[item_index] = platform_index
    with open(bstack11111l111_opy_, bstack1_opy_ (u"ࠨࡷࠬࠤછ")) as outfile:
      json.dump(bstack11llll1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡺࡶ࡮ࡺࡩ࡯ࡩࠣࡸࡴࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠥ࡬ࡩ࡭ࡧ࠽ࠤࠬજ") + str(e))
def bstack1llll1ll_opy_(bstack1ll1llll1l_opy_):
  global CONFIG
  bstack1l11l11ll_opy_ = bstack1_opy_ (u"ࠨࠩઝ")
  if not bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬઞ") in CONFIG:
    logger.info(bstack1_opy_ (u"ࠪࡒࡴࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠢࡳࡥࡸࡹࡥࡥࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡳࡧࡳࡳࡷࡺࠠࡧࡱࡵࠤࡗࡵࡢࡰࡶࠣࡶࡺࡴࠧટ"))
  try:
    platform = CONFIG[bstack1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧઠ")][bstack1ll1llll1l_opy_]
    if bstack1_opy_ (u"ࠬࡵࡳࠨડ") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"࠭࡯ࡴࠩઢ")]) + bstack1_opy_ (u"ࠧ࠭ࠢࠪણ")
    if bstack1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫત") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬથ")]) + bstack1_opy_ (u"ࠪ࠰ࠥ࠭દ")
    if bstack1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨધ") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩન")]) + bstack1_opy_ (u"࠭ࠬࠡࠩ઩")
    if bstack1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩપ") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪફ")]) + bstack1_opy_ (u"ࠩ࠯ࠤࠬબ")
    if bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨભ") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩમ")]) + bstack1_opy_ (u"ࠬ࠲ࠠࠨય")
    if bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧર") in platform:
      bstack1l11l11ll_opy_ += str(platform[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ઱")]) + bstack1_opy_ (u"ࠨ࠮ࠣࠫલ")
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠩࡖࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡷࡶ࡮ࡴࡧࠡࡨࡲࡶࠥࡸࡥࡱࡱࡵࡸࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡯࡯ࠩળ") + str(e))
  finally:
    if bstack1l11l11ll_opy_[len(bstack1l11l11ll_opy_) - 2:] == bstack1_opy_ (u"ࠪ࠰ࠥ࠭઴"):
      bstack1l11l11ll_opy_ = bstack1l11l11ll_opy_[:-2]
    return bstack1l11l11ll_opy_
def bstack1lll11lll1_opy_(path, bstack1l11l11ll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack111lll1l1_opy_ = ET.parse(path)
    bstack11llll11_opy_ = bstack111lll1l1_opy_.getroot()
    bstack1ll1l11ll1_opy_ = None
    for suite in bstack11llll11_opy_.iter(bstack1_opy_ (u"ࠫࡸࡻࡩࡵࡧࠪવ")):
      if bstack1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬશ") in suite.attrib:
        suite.attrib[bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫષ")] += bstack1_opy_ (u"ࠧࠡࠩસ") + bstack1l11l11ll_opy_
        bstack1ll1l11ll1_opy_ = suite
    bstack1111l11l_opy_ = None
    for robot in bstack11llll11_opy_.iter(bstack1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧહ")):
      bstack1111l11l_opy_ = robot
    bstack1111lll1l_opy_ = len(bstack1111l11l_opy_.findall(bstack1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ઺")))
    if bstack1111lll1l_opy_ == 1:
      bstack1111l11l_opy_.remove(bstack1111l11l_opy_.findall(bstack1_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ઻"))[0])
      bstack11ll1llll_opy_ = ET.Element(bstack1_opy_ (u"ࠫࡸࡻࡩࡵࡧ઼ࠪ"), attrib={bstack1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪઽ"): bstack1_opy_ (u"࠭ࡓࡶ࡫ࡷࡩࡸ࠭ા"), bstack1_opy_ (u"ࠧࡪࡦࠪિ"): bstack1_opy_ (u"ࠨࡵ࠳ࠫી")})
      bstack1111l11l_opy_.insert(1, bstack11ll1llll_opy_)
      bstack1ll1lll1l1_opy_ = None
      for suite in bstack1111l11l_opy_.iter(bstack1_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨુ")):
        bstack1ll1lll1l1_opy_ = suite
      bstack1ll1lll1l1_opy_.append(bstack1ll1l11ll1_opy_)
      bstack1llll1lll_opy_ = None
      for status in bstack1ll1l11ll1_opy_.iter(bstack1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪૂ")):
        bstack1llll1lll_opy_ = status
      bstack1ll1lll1l1_opy_.append(bstack1llll1lll_opy_)
    bstack111lll1l1_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡢࡴࡶ࡭ࡳ࡭ࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡰࡨࡶࡦࡺࡩ࡯ࡩࠣࡶࡴࡨ࡯ࡵࠢࡵࡩࡵࡵࡲࡵࠩૃ") + str(e))
def bstack1ll1llllll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1111111_opy_
  global CONFIG
  if bstack1_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤૄ") in options:
    del options[bstack1_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳࡶࡡࡵࡪࠥૅ")]
  bstack1ll1llll1_opy_ = bstack1ll1llll11_opy_()
  for bstack1l1llll11_opy_ in bstack1ll1llll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1_opy_ (u"ࠧࡱࡣࡥࡳࡹࡥࡲࡦࡵࡸࡰࡹࡹࠧ૆"), str(bstack1l1llll11_opy_), bstack1_opy_ (u"ࠨࡱࡸࡸࡵࡻࡴ࠯ࡺࡰࡰࠬે"))
    bstack1lll11lll1_opy_(path, bstack1llll1ll_opy_(bstack1ll1llll1_opy_[bstack1l1llll11_opy_]))
  bstack111ll11l_opy_()
  return bstack1l1111111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1llll11l1l_opy_(self, ff_profile_dir):
  global bstack111l11l11_opy_
  if not ff_profile_dir:
    return None
  return bstack111l11l11_opy_(self, ff_profile_dir)
def bstack1ll1l1l11_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1l111l_opy_
  bstack11lllll11_opy_ = []
  if bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬૈ") in CONFIG:
    bstack11lllll11_opy_ = CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ૉ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ૊")],
      pabot_args[bstack1_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨો")],
      argfile,
      pabot_args.get(bstack1_opy_ (u"ࠨࡨࡪࡸࡨࠦૌ")),
      pabot_args[bstack1_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵ્ࠥ")],
      platform[0],
      bstack1ll1l111l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣ૎")] or [(bstack1_opy_ (u"ࠤࠥ૏"), None)]
    for platform in enumerate(bstack11lllll11_opy_)
  ]
def bstack11l1l1ll1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1111l1l1_opy_=bstack1_opy_ (u"ࠪࠫૐ")):
  global bstack11l11lll1_opy_
  self.platform_index = platform_index
  self.bstack1l11llll1_opy_ = bstack1111l1l1_opy_
  bstack11l11lll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11111ll1l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lll1_opy_
  global bstack1ll1lll1l_opy_
  if not bstack1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૑") in item.options:
    item.options[bstack1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ૒")] = []
  for v in item.options[bstack1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૓")]:
    if bstack1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭૔") in v:
      item.options[bstack1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૕")].remove(v)
    if bstack1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔࠩ૖") in v:
      item.options[bstack1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૗")].remove(v)
  item.options[bstack1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૘")].insert(0, bstack1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡕࡒࡁࡕࡈࡒࡖࡒࡏࡎࡅࡇ࡛࠾ࢀࢃࠧ૙").format(item.platform_index))
  item.options[bstack1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૚")].insert(0, bstack1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡄࡆࡈࡏࡓࡈࡇࡌࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕ࠾ࢀࢃࠧ૛").format(item.bstack1l11llll1_opy_))
  if bstack1ll1lll1l_opy_:
    item.options[bstack1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૜")].insert(0, bstack1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡅࡏࡍࡆࡘࡇࡔ࠼ࡾࢁࠬ૝").format(bstack1ll1lll1l_opy_))
  return bstack1ll1lll1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1111l111l_opy_(command, item_index):
  global bstack1ll1lll1l_opy_
  if bstack1ll1lll1l_opy_:
    command[0] = command[0].replace(bstack1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ૞"), bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡷࡩࡱࠠࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠡ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠠࠨ૟") + str(
      item_index) + bstack1_opy_ (u"ࠬࠦࠧૠ") + bstack1ll1lll1l_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬૡ"),
                                    bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠤ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠣࠫૢ") + str(item_index), 1)
def bstack1ll11111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1l111llll_opy_
  bstack1111l111l_opy_(command, item_index)
  return bstack1l111llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll11l1ll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1l111llll_opy_
  bstack1111l111l_opy_(command, item_index)
  return bstack1l111llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1llll11lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1l111llll_opy_
  bstack1111l111l_opy_(command, item_index)
  return bstack1l111llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack11l11lll_opy_(self, runner, quiet=False, capture=True):
  global bstack111l11ll_opy_
  bstack1ll1l1ll1l_opy_ = bstack111l11ll_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨૣ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭૤")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1ll1l1ll1l_opy_
def bstack1ll111l1l_opy_(self, name, context, *args):
  global bstack1ll1111l1_opy_
  if name == bstack1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ૥"):
    bstack1ll1111l1_opy_(self, name, context, *args)
    try:
      if not bstack1llllll1l_opy_:
        bstack11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll11ll_opy_(bstack1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ૦")) else context.browser
        bstack1lll111l1l_opy_ = str(self.feature.name)
        bstack1l1l1l1ll_opy_(context, bstack1lll111l1l_opy_)
        bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ૧") + json.dumps(bstack1lll111l1l_opy_) + bstack1_opy_ (u"࠭ࡽࡾࠩ૨"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧ૩").format(str(e)))
  elif name == bstack1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૪"):
    bstack1ll1111l1_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૫")):
        self.driver_before_scenario = True
      if (not bstack1llllll1l_opy_):
        scenario_name = args[0].name
        feature_name = bstack1lll111l1l_opy_ = str(self.feature.name)
        bstack1lll111l1l_opy_ = feature_name + bstack1_opy_ (u"ࠪࠤ࠲ࠦࠧ૬") + scenario_name
        bstack11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll11ll_opy_(bstack1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ૭")) else context.browser
        if self.driver_before_scenario:
          bstack1l1l1l1ll_opy_(context, bstack1lll111l1l_opy_)
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ૮") + json.dumps(bstack1lll111l1l_opy_) + bstack1_opy_ (u"࠭ࡽࡾࠩ૯"))
    except Exception as e:
      logger.debug(bstack1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ૰").format(str(e)))
  elif name == bstack1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ૱"):
    try:
      bstack1l111111_opy_ = args[0].status.name
      bstack11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ૲") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1l111111_opy_).lower() == bstack1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ૳"):
        bstack11l11111l_opy_ = bstack1_opy_ (u"ࠫࠬ૴")
        bstack11ll1111_opy_ = bstack1_opy_ (u"ࠬ࠭૵")
        bstack1ll1l1llll_opy_ = bstack1_opy_ (u"࠭ࠧ૶")
        try:
          import traceback
          bstack11l11111l_opy_ = self.exception.__class__.__name__
          bstack11111lll1_opy_ = traceback.format_tb(self.exc_traceback)
          bstack11ll1111_opy_ = bstack1_opy_ (u"ࠧࠡࠩ૷").join(bstack11111lll1_opy_)
          bstack1ll1l1llll_opy_ = bstack11111lll1_opy_[-1]
        except Exception as e:
          logger.debug(bstack1llll1ll1l_opy_.format(str(e)))
        bstack11l11111l_opy_ += bstack1ll1l1llll_opy_
        bstack111ll1l1l_opy_(context, json.dumps(str(args[0].name) + bstack1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢ૸") + str(bstack11ll1111_opy_)),
                            bstack1_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣૹ"))
        if self.driver_before_scenario:
          bstack11llll1l_opy_(context, bstack1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥૺ"), bstack11l11111l_opy_)
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩૻ") + json.dumps(str(args[0].name) + bstack1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦૼ") + str(bstack11ll1111_opy_)) + bstack1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭૽"))
        if self.driver_before_scenario:
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡳࡵࡣࡷࡹࡸࠨ࠺ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ࠮ࠣࠦࡷ࡫ࡡࡴࡱࡱࠦ࠿ࠦࠧ૾") + json.dumps(bstack1_opy_ (u"ࠣࡕࡦࡩࡳࡧࡲࡪࡱࠣࡪࡦ࡯࡬ࡦࡦࠣࡻ࡮ࡺࡨ࠻ࠢ࡟ࡲࠧ૿") + str(bstack11l11111l_opy_)) + bstack1_opy_ (u"ࠩࢀࢁࠬ଀"))
      else:
        bstack111ll1l1l_opy_(context, bstack1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦଁ"), bstack1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଂ"))
        if self.driver_before_scenario:
          bstack11llll1l_opy_(context, bstack1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧଃ"))
        bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଄") + json.dumps(str(args[0].name) + bstack1_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦଅ")) + bstack1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧଆ"))
        if self.driver_before_scenario:
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭ଇ"))
    except Exception as e:
      logger.debug(bstack1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଈ").format(str(e)))
  elif name == bstack1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫଉ"):
    try:
      bstack11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll11ll_opy_(bstack1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫଊ")) else context.browser
      if context.failed is True:
        bstack111l1lll_opy_ = []
        bstack1111111ll_opy_ = []
        bstack111l1111_opy_ = []
        bstack1ll1ll11l_opy_ = bstack1_opy_ (u"࠭ࠧଋ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack111l1lll_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack11111lll1_opy_ = traceback.format_tb(exc_tb)
            bstack1lll11l1l_opy_ = bstack1_opy_ (u"ࠧࠡࠩଌ").join(bstack11111lll1_opy_)
            bstack1111111ll_opy_.append(bstack1lll11l1l_opy_)
            bstack111l1111_opy_.append(bstack11111lll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack1llll1ll1l_opy_.format(str(e)))
        bstack11l11111l_opy_ = bstack1_opy_ (u"ࠨࠩ଍")
        for i in range(len(bstack111l1lll_opy_)):
          bstack11l11111l_opy_ += bstack111l1lll_opy_[i] + bstack111l1111_opy_[i] + bstack1_opy_ (u"ࠩ࡟ࡲࠬ଎")
        bstack1ll1ll11l_opy_ = bstack1_opy_ (u"ࠪࠤࠬଏ").join(bstack1111111ll_opy_)
        if not self.driver_before_scenario:
          bstack111ll1l1l_opy_(context, bstack1ll1ll11l_opy_, bstack1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥଐ"))
          bstack11llll1l_opy_(context, bstack1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧ଑"), bstack11l11111l_opy_)
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ଒") + json.dumps(bstack1ll1ll11l_opy_) + bstack1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧଓ"))
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠤࡩࡥ࡮ࡲࡥࡥࠤ࠯ࠤࠧࡸࡥࡢࡵࡲࡲࠧࡀࠠࠨଔ") + json.dumps(bstack1_opy_ (u"ࠤࡖࡳࡲ࡫ࠠࡴࡥࡨࡲࡦࡸࡩࡰࡵࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡡࡴࠢକ") + str(bstack11l11111l_opy_)) + bstack1_opy_ (u"ࠪࢁࢂ࠭ଖ"))
      else:
        if not self.driver_before_scenario:
          bstack111ll1l1l_opy_(context, bstack1_opy_ (u"ࠦࡋ࡫ࡡࡵࡷࡵࡩ࠿ࠦࠢଗ") + str(self.feature.name) + bstack1_opy_ (u"ࠧࠦࡰࡢࡵࡶࡩࡩࠧࠢଘ"), bstack1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦଙ"))
          bstack11llll1l_opy_(context, bstack1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଚ"))
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଛ") + json.dumps(bstack1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧଜ") + str(self.feature.name) + bstack1_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧଝ")) + bstack1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪଞ"))
          bstack11l1llll_opy_.execute_script(bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡰࡢࡵࡶࡩࡩࠨࡽࡾࠩଟ"))
    except Exception as e:
      logger.debug(bstack1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨଠ").format(str(e)))
  else:
    bstack1ll1111l1_opy_(self, name, context, *args)
  if name in [bstack1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧଡ"), bstack1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩଢ")]:
    bstack1ll1111l1_opy_(self, name, context, *args)
    if (name == bstack1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪଣ") and self.driver_before_scenario) or (
            name == bstack1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪତ") and not self.driver_before_scenario):
      try:
        bstack11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack111ll11ll_opy_(bstack1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଥ")) else context.browser
        bstack11l1llll_opy_.quit()
      except Exception:
        pass
def bstack111l11l1_opy_(config, startdir):
  return bstack1_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࠱ࡿࠥଦ").format(bstack1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧଧ"))
notset = Notset()
def bstack111ll1lll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1lllll11l1_opy_
  if str(name).lower() == bstack1_opy_ (u"ࠧࡥࡴ࡬ࡺࡪࡸࠧନ"):
    return bstack1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠢ଩")
  else:
    return bstack1lllll11l1_opy_(self, name, default, skip)
def bstack1l1l11l1l_opy_(item, when):
  global bstack1lll1ll1l_opy_
  try:
    bstack1lll1ll1l_opy_(item, when)
  except Exception as e:
    pass
def bstack1lll1111ll_opy_():
  return
def bstack1lllll1ll_opy_(type, name, status, reason, bstack1lllll1l11_opy_, bstack1l11l11l1_opy_):
  bstack1111l1ll_opy_ = {
    bstack1_opy_ (u"ࠩࡤࡧࡹ࡯࡯࡯ࠩପ"): type,
    bstack1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଫ"): {}
  }
  if type == bstack1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ବ"):
    bstack1111l1ll_opy_[bstack1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨଭ")][bstack1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬମ")] = bstack1lllll1l11_opy_
    bstack1111l1ll_opy_[bstack1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪଯ")][bstack1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ର")] = json.dumps(str(bstack1l11l11l1_opy_))
  if type == bstack1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ଱"):
    bstack1111l1ll_opy_[bstack1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଲ")][bstack1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩଳ")] = name
  if type == bstack1_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ଴"):
    bstack1111l1ll_opy_[bstack1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଵ")][bstack1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧଶ")] = status
    if status == bstack1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଷ"):
      bstack1111l1ll_opy_[bstack1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬସ")][bstack1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪହ")] = json.dumps(str(reason))
  bstack11l11ll1_opy_ = bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ଺").format(json.dumps(bstack1111l1ll_opy_))
  return bstack11l11ll1_opy_
def bstack11l1lll1l_opy_(item, call, rep):
  global bstack11ll11l1_opy_
  global bstack1111ll111_opy_
  global bstack1llllll1l_opy_
  name = bstack1_opy_ (u"ࠬ࠭଻")
  try:
    if rep.when == bstack1_opy_ (u"࠭ࡣࡢ࡮࡯଼ࠫ"):
      bstack1l11l1ll_opy_ = threading.current_thread().bstack1lll11ll_opy_
      try:
        if not bstack1llllll1l_opy_:
          name = str(rep.nodeid)
          bstack11111llll_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨଽ"), name, bstack1_opy_ (u"ࠨࠩା"), bstack1_opy_ (u"ࠩࠪି"), bstack1_opy_ (u"ࠪࠫୀ"), bstack1_opy_ (u"ࠫࠬୁ"))
          for driver in bstack1111ll111_opy_:
            if bstack1l11l1ll_opy_ == driver.session_id:
              driver.execute_script(bstack11111llll_opy_)
      except Exception as e:
        logger.debug(bstack1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬୂ").format(str(e)))
      try:
        status = bstack1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ୃ") if rep.outcome.lower() == bstack1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୄ") else bstack1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ୅")
        reason = bstack1_opy_ (u"ࠩࠪ୆")
        if (reason != bstack1_opy_ (u"ࠥࠦେ")):
          try:
            if (threading.current_thread().bstackTestErrorMessages == None):
              threading.current_thread().bstackTestErrorMessages = []
          except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(str(reason))
        if status == bstack1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫୈ"):
          reason = rep.longrepr.reprcrash.message
          if (not threading.current_thread().bstackTestErrorMessages):
            threading.current_thread().bstackTestErrorMessages = []
          threading.current_thread().bstackTestErrorMessages.append(reason)
        level = bstack1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ୉") if status == bstack1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୊") else bstack1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ୋ")
        data = name + bstack1_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪୌ") if status == bstack1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ୍ࠩ") else name + bstack1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭୎") + reason
        bstack1111ll1l1_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭୏"), bstack1_opy_ (u"ࠬ࠭୐"), bstack1_opy_ (u"࠭ࠧ୑"), bstack1_opy_ (u"ࠧࠨ୒"), level, data)
        for driver in bstack1111ll111_opy_:
          if bstack1l11l1ll_opy_ == driver.session_id:
            driver.execute_script(bstack1111ll1l1_opy_)
      except Exception as e:
        logger.debug(bstack1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୓").format(str(e)))
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭୔").format(str(e)))
  bstack11ll11l1_opy_(item, call, rep)
def bstack11l111l11_opy_(framework_name):
  global bstack11ll11ll1_opy_
  global bstack1llll1111l_opy_
  global bstack1lllll1l1l_opy_
  bstack11ll11ll1_opy_ = framework_name
  logger.info(bstack1l11ll111_opy_.format(bstack11ll11ll1_opy_.split(bstack1_opy_ (u"ࠪ࠱ࠬ୕"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1l11l_opy_:
      Service.start = bstack1ll1l1l111_opy_
      Service.stop = bstack1l1l1lll1_opy_
      webdriver.Remote.get = bstack11ll1l1ll_opy_
      WebDriver.close = bstack1lll1ll1ll_opy_
      WebDriver.quit = bstack1lll1lll_opy_
      webdriver.Remote.__init__ = bstack1l1l1l111_opy_
    if not bstack1ll1l11l_opy_ and bstack1l111l1ll_opy_.on():
      webdriver.Remote.__init__ = bstack1l11llll_opy_
    bstack1llll1111l_opy_ = True
  except Exception as e:
    pass
  bstack1l1lllll1_opy_()
  if not bstack1llll1111l_opy_:
    bstack11111l1ll_opy_(bstack1_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨୖ"), bstack1llllll11_opy_)
  if bstack1l11111l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l1l1ll11_opy_
    except Exception as e:
      logger.error(bstack1l11l1l1_opy_.format(str(e)))
  if (bstack1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫୗ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1llll11l1l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1lll1lllll_opy_
      except Exception as e:
        logger.warn(bstack11lll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11ll111l_opy_
      except Exception as e:
        logger.debug(bstack1ll1l1lll1_opy_ + str(e))
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11lll1l1l_opy_)
    Output.end_test = bstack1ll11lll_opy_
    TestStatus.__init__ = bstack1111l1l1l_opy_
    QueueItem.__init__ = bstack11l1l1ll1_opy_
    pabot._create_items = bstack1ll1l1l11_opy_
    try:
      from pabot import __version__ as bstack11llllll_opy_
      if version.parse(bstack11llllll_opy_) >= version.parse(bstack1_opy_ (u"࠭࠲࠯࠳࠸࠲࠵࠭୘")):
        pabot._run = bstack1llll11lll_opy_
      elif version.parse(bstack11llllll_opy_) >= version.parse(bstack1_opy_ (u"ࠧ࠳࠰࠴࠷࠳࠶ࠧ୙")):
        pabot._run = bstack1ll11l1ll_opy_
      else:
        pabot._run = bstack1ll11111l_opy_
    except Exception as e:
      pabot._run = bstack1ll11111l_opy_
    pabot._create_command_for_execution = bstack11111ll1l_opy_
    pabot._report_results = bstack1ll1llllll_opy_
  if bstack1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ୚") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11llll1ll_opy_)
    Runner.run_hook = bstack1ll111l1l_opy_
    Step.run = bstack11l11lll_opy_
  if bstack1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ୛") in str(framework_name).lower():
    if not bstack1ll1l11l_opy_:
      return
    try:
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111l11l1_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1lll1111ll_opy_
      Config.getoption = bstack111ll1lll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1lll1l_opy_
    except Exception as e:
      pass
def bstack1lllllll1l_opy_():
  global CONFIG
  if bstack1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪଡ଼") in CONFIG and int(CONFIG[bstack1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫଢ଼")]) > 1:
    logger.warn(bstack11l1lll1_opy_)
def bstack11ll1l11_opy_(arg, bstack1lll1llll1_opy_):
  global CONFIG
  global bstack111111l1l_opy_
  global bstack11111111_opy_
  global bstack1ll1l11l_opy_
  bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୞")
  if bstack1lll1llll1_opy_ and isinstance(bstack1lll1llll1_opy_, str):
    bstack1lll1llll1_opy_ = eval(bstack1lll1llll1_opy_)
  CONFIG = bstack1lll1llll1_opy_[bstack1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭ୟ")]
  bstack111111l1l_opy_ = bstack1lll1llll1_opy_[bstack1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨୠ")]
  bstack11111111_opy_ = bstack1lll1llll1_opy_[bstack1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪୡ")]
  bstack1ll1l11l_opy_ = bstack1lll1llll1_opy_[bstack1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬୢ")]
  os.environ[bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬୣ")] = bstack1lll1l1l11_opy_
  os.environ[bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࠪ୤")] = json.dumps(CONFIG)
  os.environ[bstack1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬ୥")] = bstack111111l1l_opy_
  os.environ[bstack1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ୦")] = str(bstack11111111_opy_)
  os.environ[bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭୧")] = str(True)
  if bstack1111l11l1_opy_(arg, [bstack1_opy_ (u"ࠨ࠯ࡱࠫ୨"), bstack1_opy_ (u"ࠩ࠰࠱ࡳࡻ࡭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ୩")]) != -1:
    os.environ[bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫ୪")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1l111l_opy_)
    return
  bstack111111ll_opy_()
  global bstack111111ll1_opy_
  global bstack1l111l11_opy_
  global bstack1ll1l111l_opy_
  global bstack1ll1lll1l_opy_
  global bstack1lll1111l1_opy_
  global bstack1lllll1l1l_opy_
  global bstack1l111111l_opy_
  arg.append(bstack1_opy_ (u"ࠦ࠲࡝ࠢ୫"))
  arg.append(bstack1_opy_ (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ࠿ࡓ࡯ࡥࡷ࡯ࡩࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡮ࡲࡲࡶࡹ࡫ࡤ࠻ࡲࡼࡸࡪࡹࡴ࠯ࡒࡼࡸࡪࡹࡴࡘࡣࡵࡲ࡮ࡴࡧࠣ୬"))
  arg.append(bstack1_opy_ (u"ࠨ࠭ࡘࠤ୭"))
  arg.append(bstack1_opy_ (u"ࠢࡪࡩࡱࡳࡷ࡫࠺ࡕࡪࡨࠤ࡭ࡵ࡯࡬࡫ࡰࡴࡱࠨ୮"))
  global bstack1111ll1l_opy_
  global bstack11l11l1ll_opy_
  global bstack11ll1l1l1_opy_
  global bstack111l11l11_opy_
  global bstack11l11lll1_opy_
  global bstack1ll1lll1_opy_
  global bstack1ll1ll111_opy_
  global bstack111l1l11l_opy_
  global bstack11l11l11l_opy_
  global bstack1lllll11l1_opy_
  global bstack1lll1ll1l_opy_
  global bstack11ll11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111ll1l_opy_ = webdriver.Remote.__init__
    bstack11l11l1ll_opy_ = WebDriver.quit
    bstack1ll1ll111_opy_ = WebDriver.close
    bstack111l1l11l_opy_ = WebDriver.get
  except Exception as e:
    pass
  if bstack11ll11l1l_opy_(CONFIG):
    if bstack1ll111ll1_opy_() < version.parse(bstack1l11ll11l_opy_):
      logger.error(bstack11l1l1l11_opy_.format(bstack1ll111ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l11l11l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1l1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1lllll11l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1lll1ll1l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1lll111l_opy_)
  try:
    from pytest_bdd import reporting
    bstack11ll11l1_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩ୯"))
  bstack1ll1l111l_opy_ = CONFIG.get(bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭୰"), {}).get(bstack1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬୱ"))
  bstack1l111111l_opy_ = True
  bstack11l111l11_opy_(bstack111l1l1l1_opy_)
  os.environ[bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ୲")] = CONFIG[bstack1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ୳")]
  os.environ[bstack1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩ୴")] = CONFIG[bstack1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ୵")]
  os.environ[bstack1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫ୶")] = bstack1ll1l11l_opy_.__str__()
  from _pytest.config import main as bstack1lll11l11l_opy_
  bstack1lll11l11l_opy_(arg)
def bstack1ll1lllll_opy_(arg):
  bstack11l111l11_opy_(bstack1lll111ll_opy_)
  from behave.__main__ import main as bstack11l1l1lll_opy_
  bstack11l1l1lll_opy_(arg)
def bstack11ll1111l_opy_():
  logger.info(bstack111ll111l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ୷"), help=bstack1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡨࡵ࡮ࡧ࡫ࡪࠫ୸"))
  parser.add_argument(bstack1_opy_ (u"ࠫ࠲ࡻࠧ୹"), bstack1_opy_ (u"ࠬ࠳࠭ࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ୺"), help=bstack1_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬ୻"))
  parser.add_argument(bstack1_opy_ (u"ࠧ࠮࡭ࠪ୼"), bstack1_opy_ (u"ࠨ࠯࠰࡯ࡪࡿࠧ୽"), help=bstack1_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡡࡤࡥࡨࡷࡸࠦ࡫ࡦࡻࠪ୾"))
  parser.add_argument(bstack1_opy_ (u"ࠪ࠱࡫࠭୿"), bstack1_opy_ (u"ࠫ࠲࠳ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ஀"), help=bstack1_opy_ (u"ࠬ࡟࡯ࡶࡴࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஁"))
  bstack1lll1ll1l1_opy_ = parser.parse_args()
  try:
    bstack1lllll1l1_opy_ = bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡭ࡥ࡯ࡧࡵ࡭ࡨ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஂ")
    if bstack1lll1ll1l1_opy_.framework and bstack1lll1ll1l1_opy_.framework not in (bstack1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧஃ"), bstack1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠴ࠩ஄")):
      bstack1lllll1l1_opy_ = bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨஅ")
    bstack1ll1ll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lllll1l1_opy_)
    bstack1lllll11_opy_ = open(bstack1ll1ll1l_opy_, bstack1_opy_ (u"ࠪࡶࠬஆ"))
    bstack1lll1l111_opy_ = bstack1lllll11_opy_.read()
    bstack1lllll11_opy_.close()
    if bstack1lll1ll1l1_opy_.username:
      bstack1lll1l111_opy_ = bstack1lll1l111_opy_.replace(bstack1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫஇ"), bstack1lll1ll1l1_opy_.username)
    if bstack1lll1ll1l1_opy_.key:
      bstack1lll1l111_opy_ = bstack1lll1l111_opy_.replace(bstack1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧஈ"), bstack1lll1ll1l1_opy_.key)
    if bstack1lll1ll1l1_opy_.framework:
      bstack1lll1l111_opy_ = bstack1lll1l111_opy_.replace(bstack1_opy_ (u"࡙࠭ࡐࡗࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧஉ"), bstack1lll1ll1l1_opy_.framework)
    file_name = bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪஊ")
    file_path = os.path.abspath(file_name)
    bstack1lll1l1ll1_opy_ = open(file_path, bstack1_opy_ (u"ࠨࡹࠪ஋"))
    bstack1lll1l1ll1_opy_.write(bstack1lll1l111_opy_)
    bstack1lll1l1ll1_opy_.close()
    logger.info(bstack11111l1l1_opy_)
    try:
      os.environ[bstack1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫ஌")] = bstack1lll1ll1l1_opy_.framework if bstack1lll1ll1l1_opy_.framework != None else bstack1_opy_ (u"ࠥࠦ஍")
      config = yaml.safe_load(bstack1lll1l111_opy_)
      config[bstack1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫஎ")] = bstack1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲ࡹࡥࡵࡷࡳࠫஏ")
      bstack1lll11ll1l_opy_(bstack11ll11ll_opy_, config)
    except Exception as e:
      logger.debug(bstack11111l1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1l1ll1ll1_opy_.format(str(e)))
def bstack1lll11ll1l_opy_(bstack1l1111ll_opy_, config, bstack1llllll111_opy_={}):
  global bstack1ll1l11l_opy_
  if not config:
    return
  bstack111l1l1ll_opy_ = bstack1l1l1l1l1_opy_ if not bstack1ll1l11l_opy_ else (
    bstack111111l1_opy_ if bstack1_opy_ (u"࠭ࡡࡱࡲࠪஐ") in config else bstack1llll1l111_opy_)
  data = {
    bstack1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ஑"): config[bstack1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪஒ")],
    bstack1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬஓ"): config[bstack1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ஔ")],
    bstack1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨக"): bstack1l1111ll_opy_,
    bstack1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ஖"): {
      bstack1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஗"): str(config[bstack1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ஘")]) if bstack1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨங") in config else bstack1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥச"),
      bstack1_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬ஛"): bstack1111l11ll_opy_(os.getenv(bstack1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨஜ"), bstack1_opy_ (u"ࠧࠨ஝"))),
      bstack1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨஞ"): bstack1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧட"),
      bstack1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ஠"): bstack111l1l1ll_opy_,
      bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ஡"): config[bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭஢")] if config[bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧண")] else bstack1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨத"),
      bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ஥"): str(config[bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ஦")]) if bstack1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ஧") in config else bstack1_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࠥந"),
      bstack1_opy_ (u"ࠪࡳࡸ࠭ன"): sys.platform,
      bstack1_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ப"): socket.gethostname()
    }
  }
  update(data[bstack1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨ஫")], bstack1llllll111_opy_)
  try:
    response = bstack1lll11ll1_opy_(bstack1_opy_ (u"࠭ࡐࡐࡕࡗࠫ஬"), bstack11l11l111_opy_(bstack111ll1l1_opy_), data, {
      bstack1_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ஭"): (config[bstack1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪம")], config[bstack1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬய")])
    })
    if response:
      logger.debug(bstack11111ll1_opy_.format(bstack1l1111ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1lll11l_opy_.format(str(e)))
def bstack1111l11ll_opy_(framework):
  return bstack1_opy_ (u"ࠥࡿࢂ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࢀࢃࠢர").format(str(framework), __version__) if framework else bstack1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧற").format(
    __version__)
def bstack111111ll_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  try:
    bstack1111llll_opy_()
    logger.debug(bstack1l1111lll_opy_.format(str(CONFIG)))
    bstack1l1l11ll1_opy_()
    bstack1111ll11_opy_()
  except Exception as e:
    logger.error(bstack1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡨࡸࡺࡶࠬࠡࡧࡵࡶࡴࡸ࠺ࠡࠤல") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll11l11_opy_
  atexit.register(bstack1lll1l1l1l_opy_)
  signal.signal(signal.SIGINT, bstack1lllll11l_opy_)
  signal.signal(signal.SIGTERM, bstack1lllll11l_opy_)
def bstack1lll11l11_opy_(exctype, value, traceback):
  global bstack1111ll111_opy_
  try:
    for driver in bstack1111ll111_opy_:
      driver.execute_script(
        bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡹࡴࡢࡶࡸࡷࠧࡀࠢࡧࡣ࡬ࡰࡪࡪࠢ࠭ࠢࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠥ࠭ள") + json.dumps(
          bstack1_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥழ") + str(value)) + bstack1_opy_ (u"ࠨࡿࢀࠫவ"))
  except Exception:
    pass
  bstack111llll1_opy_(value)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111llll1_opy_(message=bstack1_opy_ (u"ࠩࠪஶ")):
  global CONFIG
  try:
    if message:
      bstack1llllll111_opy_ = {
        bstack1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩஷ"): str(message)
      }
      bstack1lll11ll1l_opy_(bstack111lll11_opy_, CONFIG, bstack1llllll111_opy_)
    else:
      bstack1lll11ll1l_opy_(bstack111lll11_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1ll11111_opy_.format(str(e)))
def bstack11l111ll1_opy_(bstack1l1l1l11l_opy_, size):
  bstack1lll11111l_opy_ = []
  while len(bstack1l1l1l11l_opy_) > size:
    bstack1l1l1llll_opy_ = bstack1l1l1l11l_opy_[:size]
    bstack1lll11111l_opy_.append(bstack1l1l1llll_opy_)
    bstack1l1l1l11l_opy_ = bstack1l1l1l11l_opy_[size:]
  bstack1lll11111l_opy_.append(bstack1l1l1l11l_opy_)
  return bstack1lll11111l_opy_
def bstack1lll11l1ll_opy_(args):
  if bstack1_opy_ (u"ࠫ࠲ࡳࠧஸ") in args and bstack1_opy_ (u"ࠬࡶࡤࡣࠩஹ") in args:
    return True
  return False
def run_on_browserstack(bstack1lll1l11l1_opy_=None, bstack11l1l1ll_opy_=None, bstack1l11ll11_opy_=False):
  global CONFIG
  global bstack111111l1l_opy_
  global bstack11111111_opy_
  bstack1lll1l1l11_opy_ = bstack1_opy_ (u"࠭ࠧ஺")
  bstack11111lll_opy_(bstack111lllll_opy_, logger)
  if bstack1lll1l11l1_opy_ and isinstance(bstack1lll1l11l1_opy_, str):
    bstack1lll1l11l1_opy_ = eval(bstack1lll1l11l1_opy_)
  if bstack1lll1l11l1_opy_:
    CONFIG = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠧࡄࡑࡑࡊࡎࡍࠧ஻")]
    bstack111111l1l_opy_ = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠨࡊࡘࡆࡤ࡛ࡒࡍࠩ஼")]
    bstack11111111_opy_ = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠩࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ஽")]
    bstack1ll1l11l1_opy_.bstack1ll1l1l1l1_opy_(bstack1_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬா"), bstack11111111_opy_)
    bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫி")
  if not bstack1l11ll11_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1l111l_opy_)
      return
    if sys.argv[1] == bstack1_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨீ") or sys.argv[1] == bstack1_opy_ (u"࠭࠭ࡷࠩு"):
      logger.info(bstack1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧூ").format(__version__))
      return
    if sys.argv[1] == bstack1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ௃"):
      bstack11ll1111l_opy_()
      return
  args = sys.argv
  bstack111111ll_opy_()
  global bstack111111ll1_opy_
  global bstack1l111111l_opy_
  global bstack1lll1lll1_opy_
  global bstack1l111l11_opy_
  global bstack1ll1l111l_opy_
  global bstack1ll1lll1l_opy_
  global bstack11111ll11_opy_
  global bstack1lll1111l1_opy_
  global bstack1lllll1l1l_opy_
  if not bstack1lll1l1l11_opy_:
    if args[1] == bstack1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௄") or args[1] == bstack1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ௅"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫெ")
      args = args[2:]
    elif args[1] == bstack1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫே"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬை")
      args = args[2:]
    elif args[1] == bstack1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௉"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧொ")
      args = args[2:]
    elif args[1] == bstack1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪோ"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫௌ")
      args = args[2:]
    elif args[1] == bstack1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ்ࠫ"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ௎")
      args = args[2:]
    elif args[1] == bstack1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௏"):
      bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧௐ")
      args = args[2:]
    else:
      if not bstack1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௑") in CONFIG or str(CONFIG[bstack1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௒")]).lower() in [bstack1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௓"), bstack1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ௔")]:
        bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௕")
        args = args[1:]
      elif str(CONFIG[bstack1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ௖")]).lower() == bstack1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ௗ"):
        bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ௘")
        args = args[1:]
      elif str(CONFIG[bstack1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ௙")]).lower() == bstack1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ௚"):
        bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ௛")
        args = args[1:]
      elif str(CONFIG[bstack1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௜")]).lower() == bstack1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௝"):
        bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ௞")
        args = args[1:]
      elif str(CONFIG[bstack1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௟")]).lower() == bstack1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ௠"):
        bstack1lll1l1l11_opy_ = bstack1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௡")
        args = args[1:]
      else:
        os.environ[bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭௢")] = bstack1lll1l1l11_opy_
        bstack11lllllll_opy_(bstack1llll111_opy_)
  global bstack111llll1l_opy_
  if bstack1lll1l11l1_opy_:
    try:
      os.environ[bstack1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ௣")] = bstack1lll1l1l11_opy_
      bstack1lll11ll1l_opy_(bstack1l11ll1l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll11111_opy_.format(str(e)))
  global bstack1111ll1l_opy_
  global bstack11l11l1ll_opy_
  global bstack111l1l1l_opy_
  global bstack11l111l1l_opy_
  global bstack1ll1l1l1ll_opy_
  global bstack11ll1l1l1_opy_
  global bstack111l11l11_opy_
  global bstack1l111llll_opy_
  global bstack11l11lll1_opy_
  global bstack1ll1lll1_opy_
  global bstack1ll1ll111_opy_
  global bstack1ll1111l1_opy_
  global bstack111l11ll_opy_
  global bstack111l1l11l_opy_
  global bstack11l11l11l_opy_
  global bstack1lllll11l1_opy_
  global bstack1lll1ll1l_opy_
  global bstack1l1111111_opy_
  global bstack11ll11l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1111ll1l_opy_ = webdriver.Remote.__init__
    bstack11l11l1ll_opy_ = WebDriver.quit
    bstack1ll1ll111_opy_ = WebDriver.close
    bstack111l1l11l_opy_ = WebDriver.get
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111llll1l_opy_ = Popen.__init__
  except Exception as e:
    pass
  if bstack11ll11l1l_opy_(CONFIG):
    if bstack1ll111ll1_opy_() < version.parse(bstack1l11ll11l_opy_):
      logger.error(bstack11l1l1l11_opy_.format(bstack1ll111ll1_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11l11l11l_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1l11l1l1_opy_.format(str(e)))
  if bstack1lll1l1l11_opy_ != bstack1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭௤") or (bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ௥") and not bstack1lll1l11l1_opy_):
    bstack11lll1l11_opy_()
  if (bstack1lll1l1l11_opy_ in [bstack1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧ௦"), bstack1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ௧"), bstack1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ௨")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1llll11l1l_opy_
        bstack1ll1l1l1ll_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11lll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack11l111l1l_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l1lll1_opy_ + str(e))
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11lll1l1l_opy_)
    if bstack1lll1l1l11_opy_ != bstack1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ௩"):
      bstack111ll11l_opy_()
    bstack111l1l1l_opy_ = Output.end_test
    bstack11ll1l1l1_opy_ = TestStatus.__init__
    bstack1l111llll_opy_ = pabot._run
    bstack11l11lll1_opy_ = QueueItem.__init__
    bstack1ll1lll1_opy_ = pabot._create_command_for_execution
    bstack1l1111111_opy_ = pabot._report_results
  if bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௪"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11llll1ll_opy_)
    bstack1ll1111l1_opy_ = Runner.run_hook
    bstack111l11ll_opy_ = Step.run
  if bstack1lll1l1l11_opy_ == bstack1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭௫"):
    try:
      bstack1l111l1ll_opy_.launch(CONFIG, {
        bstack1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ௬"): bstack1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ௭"),
        bstack1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭௮"): bstack1lll1l1lll_opy_.version(),
        bstack1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ௯"): __version__
      })
      from _pytest.config import Config
      bstack1lllll11l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1lll1ll1l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1lll111l_opy_)
    try:
      from pytest_bdd import reporting
      bstack11ll11l1_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ௰"))
  if bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ௱"):
    bstack1l111111l_opy_ = True
    if bstack1lll1l11l1_opy_ and bstack1l11ll11_opy_:
      bstack1ll1l111l_opy_ = CONFIG.get(bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௲"), {}).get(bstack1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௳"))
      bstack11l111l11_opy_(bstack1lll1ll111_opy_)
    elif bstack1lll1l11l1_opy_:
      bstack1ll1l111l_opy_ = CONFIG.get(bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ௴"), {}).get(bstack1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ௵"))
      global bstack1111ll111_opy_
      try:
        if bstack1lll11l1ll_opy_(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௶")]) and multiprocessing.current_process().name == bstack1_opy_ (u"ࠫ࠵࠭௷"):
          bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ௸")].remove(bstack1_opy_ (u"࠭࠭࡮ࠩ௹"))
          bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ௺")].remove(bstack1_opy_ (u"ࠨࡲࡧࡦࠬ௻"))
          bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ௼")] = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭௽")][0]
          with open(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ௾")], bstack1_opy_ (u"ࠬࡸࠧ௿")) as f:
            bstack1l111l1l1_opy_ = f.read()
          bstack1ll1l11l1l_opy_ = bstack1_opy_ (u"ࠨࠢࠣࡨࡵࡳࡲࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤࡹࡤ࡬ࠢ࡬ࡱࡵࡵࡲࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡀࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࠪࡾࢁ࠮ࡁࠠࡧࡴࡲࡱࠥࡶࡤࡣࠢ࡬ࡱࡵࡵࡲࡵࠢࡓࡨࡧࡁࠠࡰࡩࡢࡨࡧࠦ࠽ࠡࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱ࠻ࠋࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࡷࡶࡾࡀࠊࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࡧࡻࡧࡪࡶࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡦࡹࠠࡦ࠼ࠍࠤࠥࠦࠠࡱࡣࡶࡷࠏࠦࠠࡰࡩࡢࡨࡧ࠮ࡳࡦ࡮ࡩ࠰ࡦࡸࡧ࠭ࡶࡨࡱࡵࡵࡲࡢࡴࡼ࠭ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࡓࡨࡧ࠮ࠩ࠯ࡵࡨࡸࡤࡺࡲࡢࡥࡨࠬ࠮ࡢ࡮ࠣࠤࠥఀ").format(str(bstack1lll1l11l1_opy_))
          bstack1lll1111l_opy_ = bstack1ll1l11l1l_opy_ + bstack1l111l1l1_opy_
          bstack1l11lll1l_opy_ = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪఁ")] + bstack1_opy_ (u"ࠨࡡࡥࡷࡹࡧࡣ࡬ࡡࡷࡩࡲࡶ࠮ࡱࡻࠪం")
          with open(bstack1l11lll1l_opy_, bstack1_opy_ (u"ࠩࡺࠫః")):
            pass
          with open(bstack1l11lll1l_opy_, bstack1_opy_ (u"ࠥࡻ࠰ࠨఄ")) as f:
            f.write(bstack1lll1111l_opy_)
          import subprocess
          bstack111ll1ll1_opy_ = subprocess.run([bstack1_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࠦఅ"), bstack1l11lll1l_opy_])
          if os.path.exists(bstack1l11lll1l_opy_):
            os.unlink(bstack1l11lll1l_opy_)
          os._exit(bstack111ll1ll1_opy_.returncode)
        else:
          if bstack1lll11l1ll_opy_(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఆ")]):
            bstack1lll1l11l1_opy_[bstack1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩఇ")].remove(bstack1_opy_ (u"ࠧ࠮࡯ࠪఈ"))
            bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫఉ")].remove(bstack1_opy_ (u"ࠩࡳࡨࡧ࠭ఊ"))
            bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఋ")] = bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧఌ")][0]
          bstack11l111l11_opy_(bstack1lll1ll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ఍")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1_opy_ (u"࠭࡟ࡠࡰࡤࡱࡪࡥ࡟ࠨఎ")] = bstack1_opy_ (u"ࠧࡠࡡࡰࡥ࡮ࡴ࡟ࡠࠩఏ")
          mod_globals[bstack1_opy_ (u"ࠨࡡࡢࡪ࡮ࡲࡥࡠࡡࠪఐ")] = os.path.abspath(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ఑")])
          exec(open(bstack1lll1l11l1_opy_[bstack1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ఒ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1_opy_ (u"ࠫࡈࡧࡵࡨࡪࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠫఓ").format(str(e)))
          for driver in bstack1111ll111_opy_:
            bstack11l1l1ll_opy_.append({
              bstack1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪఔ"): bstack1lll1l11l1_opy_[bstack1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩక")],
              bstack1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ఖ"): str(e),
              bstack1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧగ"): multiprocessing.current_process().name
            })
            driver.execute_script(
              bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡪࡦ࡯࡬ࡦࡦࠥ࠰ࠥࠨࡲࡦࡣࡶࡳࡳࠨ࠺ࠡࠩఘ") + json.dumps(
                bstack1_opy_ (u"ࠥࡗࡪࡹࡳࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨఙ") + str(e)) + bstack1_opy_ (u"ࠫࢂࢃࠧచ"))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1111ll111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      bstack1l1ll1l1l_opy_()
      bstack1lllllll1l_opy_()
      bstack1lll1llll1_opy_ = {
        bstack1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨఛ"): args[0],
        bstack1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭జ"): CONFIG,
        bstack1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨఝ"): bstack111111l1l_opy_,
        bstack1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪఞ"): bstack11111111_opy_
      }
      if bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬట") in CONFIG:
        bstack1111l1l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1lllllll1_opy_ = manager.list()
        if bstack1lll11l1ll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ఠ")]):
            if index == 0:
              bstack1lll1llll1_opy_[bstack1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧడ")] = args
            bstack1111l1l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll1llll1_opy_, bstack1lllllll1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨఢ")]):
            bstack1111l1l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1lll1llll1_opy_, bstack1lllllll1_opy_)))
        for t in bstack1111l1l11_opy_:
          t.start()
        for t in bstack1111l1l11_opy_:
          t.join()
        bstack11111ll11_opy_ = list(bstack1lllllll1_opy_)
      else:
        if bstack1lll11l1ll_opy_(args):
          bstack1lll1llll1_opy_[bstack1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩణ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1lll1llll1_opy_,))
          test.start()
          test.join()
        else:
          bstack11l111l11_opy_(bstack1lll1ll111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1_opy_ (u"ࠧࡠࡡࡱࡥࡲ࡫࡟ࡠࠩత")] = bstack1_opy_ (u"ࠨࡡࡢࡱࡦ࡯࡮ࡠࡡࠪథ")
          mod_globals[bstack1_opy_ (u"ࠩࡢࡣ࡫࡯࡬ࡦࡡࡢࠫద")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩధ") or bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪన"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11lll1l1l_opy_)
    bstack1l1ll1l1l_opy_()
    bstack11l111l11_opy_(bstack1ll1ll1ll_opy_)
    if bstack1_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪ఩") in args:
      i = args.index(bstack1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫప"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack111111ll1_opy_))
    args.insert(0, str(bstack1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬఫ")))
    pabot.main(args)
  elif bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩబ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11lll1l1l_opy_)
    for a in args:
      if bstack1_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡒࡏࡅ࡙ࡌࡏࡓࡏࡌࡒࡉࡋࡘࠨభ") in a:
        bstack1l111l11_opy_ = int(a.split(bstack1_opy_ (u"ࠪ࠾ࠬమ"))[1])
      if bstack1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨయ") in a:
        bstack1ll1l111l_opy_ = str(a.split(bstack1_opy_ (u"ࠬࡀࠧర"))[1])
      if bstack1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡉࡌࡊࡃࡕࡋࡘ࠭ఱ") in a:
        bstack1ll1lll1l_opy_ = str(a.split(bstack1_opy_ (u"ࠧ࠻ࠩల"))[1])
    bstack1ll1llll_opy_ = None
    if bstack1_opy_ (u"ࠨ࠯࠰ࡦࡸࡺࡡࡤ࡭ࡢ࡭ࡹ࡫࡭ࡠ࡫ࡱࡨࡪࡾࠧళ") in args:
      i = args.index(bstack1_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨఴ"))
      args.pop(i)
      bstack1ll1llll_opy_ = args.pop(i)
    if bstack1ll1llll_opy_ is not None:
      global bstack1ll1ll111l_opy_
      bstack1ll1ll111l_opy_ = bstack1ll1llll_opy_
    bstack11l111l11_opy_(bstack1ll1ll1ll_opy_)
    run_cli(args)
  elif bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪవ"):
    bstack1l1lllll_opy_ = bstack1lll1l1lll_opy_(args, logger, CONFIG, bstack1ll1l11l_opy_)
    bstack1l1lllll_opy_.bstack1lll111111_opy_()
    bstack1l1ll1l1l_opy_()
    bstack1lll1lll1_opy_ = True
    bstack1lllll1l1l_opy_ = bstack1l1lllll_opy_.bstack1111l1lll_opy_()
    bstack1l1lllll_opy_.bstack1lll1llll1_opy_(bstack1llllll1l_opy_)
    bstack1lll1111l1_opy_ = bstack1l1lllll_opy_.bstack11lllll1l_opy_(bstack11ll1l11_opy_, {
      bstack1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬశ"): bstack111111l1l_opy_,
      bstack1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧష"): bstack11111111_opy_,
      bstack1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩస"): bstack1ll1l11l_opy_
    })
  elif bstack1lll1l1l11_opy_ == bstack1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧహ"):
    try:
      from behave.__main__ import main as bstack11l1l1lll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11111l1ll_opy_(e, bstack11llll1ll_opy_)
    bstack1l1ll1l1l_opy_()
    bstack1lll1lll1_opy_ = True
    bstack111l1ll1l_opy_ = 1
    if bstack1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ఺") in CONFIG:
      bstack111l1ll1l_opy_ = CONFIG[bstack1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ఻")]
    bstack1l1111ll1_opy_ = int(bstack111l1ll1l_opy_) * int(len(CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ఼࠭")]))
    config = Configuration(args)
    bstack1lll1l11l_opy_ = config.paths
    if len(bstack1lll1l11l_opy_) == 0:
      import glob
      pattern = bstack1_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪఽ")
      bstack11ll1lll1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11ll1lll1_opy_)
      config = Configuration(args)
      bstack1lll1l11l_opy_ = config.paths
    bstack11l1111l1_opy_ = [os.path.normpath(item) for item in bstack1lll1l11l_opy_]
    bstack1l1ll1l11_opy_ = [os.path.normpath(item) for item in args]
    bstack1l1l1ll1_opy_ = [item for item in bstack1l1ll1l11_opy_ if item not in bstack11l1111l1_opy_]
    import platform as pf
    if pf.system().lower() == bstack1_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ా"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11l1111l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1111l1_opy_)))
                    for bstack1l1111l1_opy_ in bstack11l1111l1_opy_]
    bstack1l1111l1l_opy_ = []
    for spec in bstack11l1111l1_opy_:
      bstack1l1l11l11_opy_ = []
      bstack1l1l11l11_opy_ += bstack1l1l1ll1_opy_
      bstack1l1l11l11_opy_.append(spec)
      bstack1l1111l1l_opy_.append(bstack1l1l11l11_opy_)
    execution_items = []
    for bstack1l1l11l11_opy_ in bstack1l1111l1l_opy_:
      for index, _ in enumerate(CONFIG[bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩి")]):
        item = {}
        item[bstack1_opy_ (u"ࠧࡢࡴࡪࠫీ")] = bstack1_opy_ (u"ࠨࠢࠪు").join(bstack1l1l11l11_opy_)
        item[bstack1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨూ")] = index
        execution_items.append(item)
    bstack1lllll1lll_opy_ = bstack11l111ll1_opy_(execution_items, bstack1l1111ll1_opy_)
    for execution_item in bstack1lllll1lll_opy_:
      bstack1111l1l11_opy_ = []
      for item in execution_item:
        bstack1111l1l11_opy_.append(bstack111l111l1_opy_(name=str(item[bstack1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩృ")]),
                                             target=bstack1ll1lllll_opy_,
                                             args=(item[bstack1_opy_ (u"ࠫࡦࡸࡧࠨౄ")],)))
      for t in bstack1111l1l11_opy_:
        t.start()
      for t in bstack1111l1l11_opy_:
        t.join()
  else:
    bstack11lllllll_opy_(bstack1llll111_opy_)
  if not bstack1lll1l11l1_opy_:
    bstack1llll1l11_opy_()
def browserstack_initialize(bstack1l1ll111_opy_=None):
  run_on_browserstack(bstack1l1ll111_opy_, None, True)
def bstack1llll1l11_opy_():
  bstack1l111l1ll_opy_.stop()
  bstack1l111l1ll_opy_.bstack1ll11ll1_opy_()
  [bstack1ll11l111_opy_, bstack11l1ll1l1_opy_] = bstack1l1l11ll_opy_()
  if bstack1ll11l111_opy_ is not None and bstack11ll11lll_opy_() != -1:
    sessions = bstack111ll11l1_opy_(bstack1ll11l111_opy_)
    bstack1111l1111_opy_(sessions, bstack11l1ll1l1_opy_)
def bstack1lll1ll11_opy_(bstack1l1l111l1_opy_):
  if bstack1l1l111l1_opy_:
    return bstack1l1l111l1_opy_.capitalize()
  else:
    return bstack1l1l111l1_opy_
def bstack1l1llll1l_opy_(bstack111lll1l_opy_):
  if bstack1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ౅") in bstack111lll1l_opy_ and bstack111lll1l_opy_[bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫె")] != bstack1_opy_ (u"ࠧࠨే"):
    return bstack111lll1l_opy_[bstack1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ై")]
  else:
    bstack111111l11_opy_ = bstack1_opy_ (u"ࠤࠥ౉")
    if bstack1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪొ") in bstack111lll1l_opy_ and bstack111lll1l_opy_[bstack1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫో")] != None:
      bstack111111l11_opy_ += bstack111lll1l_opy_[bstack1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬౌ")] + bstack1_opy_ (u"ࠨࠬࠡࠤ్")
      if bstack111lll1l_opy_[bstack1_opy_ (u"ࠧࡰࡵࠪ౎")] == bstack1_opy_ (u"ࠣ࡫ࡲࡷࠧ౏"):
        bstack111111l11_opy_ += bstack1_opy_ (u"ࠤ࡬ࡓࡘࠦࠢ౐")
      bstack111111l11_opy_ += (bstack111lll1l_opy_[bstack1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ౑")] or bstack1_opy_ (u"ࠫࠬ౒"))
      return bstack111111l11_opy_
    else:
      bstack111111l11_opy_ += bstack1lll1ll11_opy_(bstack111lll1l_opy_[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭౓")]) + bstack1_opy_ (u"ࠨࠠࠣ౔") + (
              bstack111lll1l_opy_[bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ౕࠩ")] or bstack1_opy_ (u"ࠨౖࠩ")) + bstack1_opy_ (u"ࠤ࠯ࠤࠧ౗")
      if bstack111lll1l_opy_[bstack1_opy_ (u"ࠪࡳࡸ࠭ౘ")] == bstack1_opy_ (u"ࠦ࡜࡯࡮ࡥࡱࡺࡷࠧౙ"):
        bstack111111l11_opy_ += bstack1_opy_ (u"ࠧ࡝ࡩ࡯ࠢࠥౚ")
      bstack111111l11_opy_ += bstack111lll1l_opy_[bstack1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ౛")] or bstack1_opy_ (u"ࠧࠨ౜")
      return bstack111111l11_opy_
def bstack1l1l1111l_opy_(bstack1lll11111_opy_):
  if bstack1lll11111_opy_ == bstack1_opy_ (u"ࠣࡦࡲࡲࡪࠨౝ"):
    return bstack1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾࡬ࡸࡥࡦࡰ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦ࡬ࡸࡥࡦࡰࠥࡂࡈࡵ࡭ࡱ࡮ࡨࡸࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬ౞")
  elif bstack1lll11111_opy_ == bstack1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ౟"):
    return bstack1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡲࡦࡦ࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡷ࡫ࡤࠣࡀࡉࡥ࡮ࡲࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧౠ")
  elif bstack1lll11111_opy_ == bstack1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧౡ"):
    return bstack1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡒࡤࡷࡸ࡫ࡤ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ౢ")
  elif bstack1lll11111_opy_ == bstack1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨౣ"):
    return bstack1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡅࡳࡴࡲࡶࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪ౤")
  elif bstack1lll11111_opy_ == bstack1_opy_ (u"ࠤࡷ࡭ࡲ࡫࡯ࡶࡶࠥ౥"):
    return bstack1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࠩࡥࡦࡣ࠶࠶࠻ࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࠤࡧࡨࡥ࠸࠸࠶ࠣࡀࡗ࡭ࡲ࡫࡯ࡶࡶ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨ౦")
  elif bstack1lll11111_opy_ == bstack1_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠧ౧"):
    return bstack1_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࡓࡷࡱࡲ࡮ࡴࡧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౨")
  else:
    return bstack1_opy_ (u"࠭࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࠪ౩") + bstack1lll1ll11_opy_(
      bstack1lll11111_opy_) + bstack1_opy_ (u"ࠧ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭౪")
def bstack1l1ll1111_opy_(session):
  return bstack1_opy_ (u"ࠨ࠾ࡷࡶࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡸ࡯ࡸࠤࡁࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠥࡹࡥࡴࡵ࡬ࡳࡳ࠳࡮ࡢ࡯ࡨࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࡼࡿࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄࡻࡾ࠾࠲ࡥࡃࡂ࠯ࡵࡦࡁࡿࢂࢁࡽ࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿࠳ࡹࡸ࠾ࠨ౫").format(
    session[bstack1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤࡡࡸࡶࡱ࠭౬")], bstack1l1llll1l_opy_(session), bstack1l1l1111l_opy_(session[bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡸࡦࡺࡵࡴࠩ౭")]),
    bstack1l1l1111l_opy_(session[bstack1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ౮")]),
    bstack1lll1ll11_opy_(session[bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭౯")] or session[bstack1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭౰")] or bstack1_opy_ (u"ࠧࠨ౱")) + bstack1_opy_ (u"ࠣࠢࠥ౲") + (session[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ౳")] or bstack1_opy_ (u"ࠪࠫ౴")),
    session[bstack1_opy_ (u"ࠫࡴࡹࠧ౵")] + bstack1_opy_ (u"ࠧࠦࠢ౶") + session[bstack1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ౷")], session[bstack1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ౸")] or bstack1_opy_ (u"ࠨࠩ౹"),
    session[bstack1_opy_ (u"ࠩࡦࡶࡪࡧࡴࡦࡦࡢࡥࡹ࠭౺")] if session[bstack1_opy_ (u"ࠪࡧࡷ࡫ࡡࡵࡧࡧࡣࡦࡺࠧ౻")] else bstack1_opy_ (u"ࠫࠬ౼"))
def bstack1111l1111_opy_(sessions, bstack11l1ll1l1_opy_):
  try:
    bstack1l1l1l1l_opy_ = bstack1_opy_ (u"ࠧࠨ౽")
    if not os.path.exists(bstack1lllll11ll_opy_):
      os.mkdir(bstack1lllll11ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1_opy_ (u"࠭ࡡࡴࡵࡨࡸࡸ࠵ࡲࡦࡲࡲࡶࡹ࠴ࡨࡵ࡯࡯ࠫ౾")), bstack1_opy_ (u"ࠧࡳࠩ౿")) as f:
      bstack1l1l1l1l_opy_ = f.read()
    bstack1l1l1l1l_opy_ = bstack1l1l1l1l_opy_.replace(bstack1_opy_ (u"ࠨࡽࠨࡖࡊ࡙ࡕࡍࡖࡖࡣࡈࡕࡕࡏࡖࠨࢁࠬಀ"), str(len(sessions)))
    bstack1l1l1l1l_opy_ = bstack1l1l1l1l_opy_.replace(bstack1_opy_ (u"ࠩࡾࠩࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠥࡾࠩಁ"), bstack11l1ll1l1_opy_)
    bstack1l1l1l1l_opy_ = bstack1l1l1l1l_opy_.replace(bstack1_opy_ (u"ࠪࡿࠪࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠧࢀࠫಂ"),
                                              sessions[0].get(bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡲࡦࡳࡥࠨಃ")) if sessions[0] else bstack1_opy_ (u"ࠬ࠭಄"))
    with open(os.path.join(bstack1lllll11ll_opy_, bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡸࡥࡱࡱࡵࡸ࠳࡮ࡴ࡮࡮ࠪಅ")), bstack1_opy_ (u"ࠧࡸࠩಆ")) as stream:
      stream.write(bstack1l1l1l1l_opy_.split(bstack1_opy_ (u"ࠨࡽࠨࡗࡊ࡙ࡓࡊࡑࡑࡗࡤࡊࡁࡕࡃࠨࢁࠬಇ"))[0])
      for session in sessions:
        stream.write(bstack1l1ll1111_opy_(session))
      stream.write(bstack1l1l1l1l_opy_.split(bstack1_opy_ (u"ࠩࡾࠩࡘࡋࡓࡔࡋࡒࡒࡘࡥࡄࡂࡖࡄࠩࢂ࠭ಈ"))[1])
    logger.info(bstack1_opy_ (u"ࠪࡋࡪࡴࡥࡳࡣࡷࡩࡩࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡨࡵࡪ࡮ࡧࠤࡦࡸࡴࡪࡨࡤࡧࡹࡹࠠࡢࡶࠣࡿࢂ࠭ಉ").format(bstack1lllll11ll_opy_));
  except Exception as e:
    logger.debug(bstack1ll1ll1l1l_opy_.format(str(e)))
def bstack111ll11l1_opy_(bstack1ll11l111_opy_):
  global CONFIG
  try:
    host = bstack1_opy_ (u"ࠫࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪࠧಊ") if bstack1_opy_ (u"ࠬࡧࡰࡱࠩಋ") in CONFIG else bstack1_opy_ (u"࠭ࡡࡱ࡫ࠪಌ")
    user = CONFIG[bstack1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ಍")]
    key = CONFIG[bstack1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫಎ")]
    bstack1111111l_opy_ = bstack1_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨಏ") if bstack1_opy_ (u"ࠪࡥࡵࡶࠧಐ") in CONFIG else bstack1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭಑")
    url = bstack1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࢁࡽ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡪࡹࡳࡪࡱࡱࡷ࠳ࡰࡳࡰࡰࠪಒ").format(user, key, host, bstack1111111l_opy_,
                                                                                bstack1ll11l111_opy_)
    headers = {
      bstack1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬಓ"): bstack1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪಔ"),
    }
    proxies = bstack1111111l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ಕ")], response.json()))
  except Exception as e:
    logger.debug(bstack1llll1lll1_opy_.format(str(e)))
def bstack1l1l11ll_opy_():
  global CONFIG
  try:
    if bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬಖ") in CONFIG:
      host = bstack1_opy_ (u"ࠪࡥࡵ࡯࠭ࡤ࡮ࡲࡹࡩ࠭ಗ") if bstack1_opy_ (u"ࠫࡦࡶࡰࠨಘ") in CONFIG else bstack1_opy_ (u"ࠬࡧࡰࡪࠩಙ")
      user = CONFIG[bstack1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨಚ")]
      key = CONFIG[bstack1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪಛ")]
      bstack1111111l_opy_ = bstack1_opy_ (u"ࠨࡣࡳࡴ࠲ࡧࡵࡵࡱࡰࡥࡹ࡫ࠧಜ") if bstack1_opy_ (u"ࠩࡤࡴࡵ࠭ಝ") in CONFIG else bstack1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬಞ")
      url = bstack1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࢁࡽ࠻ࡽࢀࡄࢀࢃ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠴ࡪࡴࡱࡱࠫಟ").format(user, key, host, bstack1111111l_opy_)
      headers = {
        bstack1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫಠ"): bstack1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩಡ"),
      }
      if bstack1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩಢ") in CONFIG:
        params = {bstack1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಣ"): CONFIG[bstack1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬತ")], bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ಥ"): CONFIG[bstack1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ದ")]}
      else:
        params = {bstack1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪಧ"): CONFIG[bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩನ")]}
      proxies = bstack1111111l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack11lll11ll_opy_ = response.json()[0][bstack1_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡧࡻࡩ࡭ࡦࠪ಩")]
        if bstack11lll11ll_opy_:
          bstack11l1ll1l1_opy_ = bstack11lll11ll_opy_[bstack1_opy_ (u"ࠨࡲࡸࡦࡱ࡯ࡣࡠࡷࡵࡰࠬಪ")].split(bstack1_opy_ (u"ࠩࡳࡹࡧࡲࡩࡤ࠯ࡥࡹ࡮ࡲࡤࠨಫ"))[0] + bstack1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡵ࠲ࠫಬ") + bstack11lll11ll_opy_[
            bstack1_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧಭ")]
          logger.info(bstack11l1ll1l_opy_.format(bstack11l1ll1l1_opy_))
          bstack1111ll1ll_opy_ = CONFIG[bstack1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨಮ")]
          if bstack1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨಯ") in CONFIG:
            bstack1111ll1ll_opy_ += bstack1_opy_ (u"ࠧࠡࠩರ") + CONFIG[bstack1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪಱ")]
          if bstack1111ll1ll_opy_ != bstack11lll11ll_opy_[bstack1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧಲ")]:
            logger.debug(bstack1l1l1lll_opy_.format(bstack11lll11ll_opy_[bstack1_opy_ (u"ࠪࡲࡦࡳࡥࠨಳ")], bstack1111ll1ll_opy_))
          return [bstack11lll11ll_opy_[bstack1_opy_ (u"ࠫ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ಴")], bstack11l1ll1l1_opy_]
    else:
      logger.warn(bstack1l1llllll_opy_)
  except Exception as e:
    logger.debug(bstack111l1lll1_opy_.format(str(e)))
  return [None, None]
def bstack1llllll1ll_opy_(url, bstack1lll111l1_opy_=False):
  global CONFIG
  global bstack1ll111l1_opy_
  if not bstack1ll111l1_opy_:
    hostname = bstack1l1lll1l_opy_(url)
    is_private = bstack11lll1ll_opy_(hostname)
    if (bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩವ") in CONFIG and not CONFIG[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪಶ")]) and (is_private or bstack1lll111l1_opy_):
      bstack1ll111l1_opy_ = hostname
def bstack1l1lll1l_opy_(url):
  return urlparse(url).hostname
def bstack11lll1ll_opy_(hostname):
  for bstack111llll11_opy_ in bstack111l111ll_opy_:
    regex = re.compile(bstack111llll11_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111ll11ll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False