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
import atexit
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll111l_opy_, bstack11lll11ll_opy_, update, bstack111llll11_opy_,
                                       bstack1l1l1l1ll_opy_, bstack11111l11_opy_, bstack111lllll1_opy_, bstack1llll11l_opy_,
                                       bstack1ll11lll_opy_, bstack111111111_opy_, bstack1lll1ll1l1_opy_, bstack1lll1lll1l_opy_,
                                       bstack11ll1l1ll_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1ll11l1ll1_opy_
from bstack_utils.constants import bstack1l111ll1_opy_, bstack1l11lll1_opy_, bstack1ll1l1l11l_opy_, bstack1lll11lll1_opy_, \
    bstack1ll1ll11ll_opy_
from bstack_utils.helper import bstack1l1ll1l1ll_opy_, bstack1l1lll1l11_opy_, bstack1l11l1l1l_opy_, bstack1l1ll1ll1l_opy_, \
    bstack1ll111111l_opy_, bstack1ll1l11l1l_opy_, bstack11l1111ll_opy_, bstack1l1lll1l1l_opy_, bstack1l1llllll1_opy_, Notset, \
    bstack11ll1l1l_opy_, bstack1l1lll1111_opy_
from bstack_utils.messages import bstack1l1llll11_opy_, bstack1llll1111l_opy_, bstack1l11l111_opy_, bstack111ll1l1_opy_, bstack1llllll11_opy_, \
    bstack1lllllll1_opy_, bstack1l1ll1l11_opy_, bstack1l11ll111_opy_, bstack1l11l11l1_opy_, bstack1ll1l111l_opy_, \
    bstack11111l1l1_opy_, bstack1ll1ll1lll_opy_
from bstack_utils.proxy import bstack1llll11l11_opy_, bstack1ll111l11_opy_
from bstack_utils.bstack1l1l1l1111_opy_ import bstack1l1l1l111l_opy_
from bstack_utils.bstack1l1l11l1l1_opy_ import bstack1l1l11ll_opy_, bstack1ll1ll1l_opy_, bstack1l11llll1_opy_
from bstack_utils.bstack11111ll1l_opy_ import bstack1llll11lll_opy_
bstack1lll1l11ll_opy_ = None
bstack11ll1l111_opy_ = None
bstack1111ll1l_opy_ = None
bstack1111l111l_opy_ = None
bstack1ll1lll1l1_opy_ = None
bstack1l11lllll_opy_ = None
bstack11lllll1_opy_ = None
bstack1l111lll_opy_ = None
bstack11llllll1_opy_ = None
bstack11l1llll_opy_ = None
bstack1lll11l11l_opy_ = None
bstack111111ll_opy_ = None
bstack11llll1ll_opy_ = None
bstack1l1l1111l_opy_ = bstack1111ll1_opy_ (u"࠭ࠧᄤ")
CONFIG = {}
bstack1llllll1l_opy_ = False
bstack1ll1111l1_opy_ = bstack1111ll1_opy_ (u"ࠧࠨᄥ")
bstack11l1l1ll_opy_ = bstack1111ll1_opy_ (u"ࠨࠩᄦ")
bstack1llll1ll_opy_ = False
bstack1l1l1111_opy_ = []
bstack1111ll1ll_opy_ = bstack1l11lll1_opy_
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1111ll1ll_opy_,
                    format=bstack1111ll1_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᄧ"),
                    datefmt=bstack1111ll1_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᄨ"),
                    stream=sys.stdout)
def bstack11l11ll1l_opy_():
    global CONFIG
    global bstack1111ll1ll_opy_
    if bstack1111ll1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᄩ") in CONFIG:
        bstack1111ll1ll_opy_ = bstack1l111ll1_opy_[CONFIG[bstack1111ll1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᄪ")]]
        logging.getLogger().setLevel(bstack1111ll1ll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111l1l1l_opy_ = {}
bstack1l11l1llll_opy_ = None
_1l111l11ll_opy_ = {}
def bstack1ll1llll1_opy_(page, bstack1lll11lll_opy_):
    try:
        page.evaluate(bstack1111ll1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᄫ"),
                      bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᄬ") + json.dumps(
                          bstack1lll11lll_opy_) + bstack1111ll1_opy_ (u"ࠣࡿࢀࠦᄭ"))
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᄮ"), e)
def bstack11ll111ll_opy_(page, message, level):
    try:
        page.evaluate(bstack1111ll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᄯ"), bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩᄰ") + json.dumps(
            message) + bstack1111ll1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨᄱ") + json.dumps(level) + bstack1111ll1_opy_ (u"࠭ࡽࡾࠩᄲ"))
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥᄳ"), e)
def bstack1ll1llll11_opy_(page, status, message=bstack1111ll1_opy_ (u"ࠣࠤᄴ")):
    try:
        if (status == bstack1111ll1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᄵ")):
            page.evaluate(bstack1111ll1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᄶ"),
                          bstack1111ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡶࡪࡧࡳࡰࡰࠥ࠾ࠬᄷ") + json.dumps(
                              bstack1111ll1_opy_ (u"࡙ࠧࡣࡦࡰࡤࡶ࡮ࡵࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦࠢᄸ") + str(message)) + bstack1111ll1_opy_ (u"࠭ࠬࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪᄹ") + json.dumps(status) + bstack1111ll1_opy_ (u"ࠢࡾࡿࠥᄺ"))
        else:
            page.evaluate(bstack1111ll1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᄻ"),
                          bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠪᄼ") + json.dumps(
                              status) + bstack1111ll1_opy_ (u"ࠥࢁࢂࠨᄽ"))
    except Exception as e:
        print(bstack1111ll1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠣᄾ"), e)
def pytest_configure(config):
    config.args = bstack1llll11lll_opy_.bstack1l11l1l11l_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l11l11111_opy_ = item.config.getoption(bstack1111ll1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᄿ"))
    plugins = item.config.getoption(bstack1111ll1_opy_ (u"ࠨࡰ࡭ࡷࡪ࡭ࡳࡹࠢᅀ"))
    report = outcome.get_result()
    bstack1l111l1ll1_opy_(item, call, report)
    if bstack1111ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡶ࡬ࡶࡩ࡬ࡲࠧᅁ") not in plugins or bstack1l1llllll1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1111ll1_opy_ (u"ࠣࡡࡧࡶ࡮ࡼࡥࡳࠤᅂ"), None)
    page = getattr(item, bstack1111ll1_opy_ (u"ࠤࡢࡴࡦ࡭ࡥࠣᅃ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1l11l1111l_opy_(item, report, summary, bstack1l11l11111_opy_)
    if (page is not None):
        bstack1l111ll1ll_opy_(item, report, summary, bstack1l11l11111_opy_)
def bstack1l11l1111l_opy_(item, report, summary, bstack1l11l11111_opy_):
    if report.when in [bstack1111ll1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᅄ"), bstack1111ll1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᅅ")]:
        return
    if not bstack1l1lll1l11_opy_():
        return
    if (str(bstack1l11l11111_opy_).lower() != bstack1111ll1_opy_ (u"ࠬࡺࡲࡶࡧࠪᅆ")):
        item._driver.execute_script(
            bstack1111ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫᅇ") + json.dumps(
                report.nodeid) + bstack1111ll1_opy_ (u"ࠧࡾࡿࠪᅈ"))
    passed = report.passed or (report.failed and hasattr(report, bstack1111ll1_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᅉ")))
    bstack11llll111_opy_ = bstack1111ll1_opy_ (u"ࠤࠥᅊ")
    if not passed:
        try:
            bstack11llll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᅋ").format(e)
            )
    if (bstack11llll111_opy_ != bstack1111ll1_opy_ (u"ࠦࠧᅌ")):
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11llll111_opy_))
    try:
        if (passed):
            item._driver.execute_script(
                bstack1111ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡤࡢࡶࡤࠦ࠿ࠦࠧᅍ")
                + json.dumps(bstack1111ll1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢᅎ"))
                + bstack1111ll1_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤᅏ")
            )
        else:
            item._driver.execute_script(
                bstack1111ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᅐ")
                + json.dumps(str(bstack11llll111_opy_))
                + bstack1111ll1_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࠦᅑ")
            )
    except Exception as e:
        summary.append(bstack1111ll1_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣᅒ").format(e))
def bstack1l111ll1ll_opy_(item, report, summary, bstack1l11l11111_opy_):
    if report.when in [bstack1111ll1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᅓ"), bstack1111ll1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴࠢᅔ")]:
        return
    if (str(bstack1l11l11111_opy_).lower() != bstack1111ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫᅕ")):
        bstack1ll1llll1_opy_(item._page, report.nodeid)
    passed = report.passed or (report.failed and hasattr(report, bstack1111ll1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᅖ")))
    bstack11llll111_opy_ = bstack1111ll1_opy_ (u"ࠣࠤᅗ")
    if not passed:
        try:
            bstack11llll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1111ll1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᅘ").format(e)
            )
    try:
        if passed:
            bstack1ll1llll11_opy_(item._page, bstack1111ll1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥᅙ"))
        else:
            if bstack11llll111_opy_:
                bstack11ll111ll_opy_(item._page, str(bstack11llll111_opy_), bstack1111ll1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥᅚ"))
                bstack1ll1llll11_opy_(item._page, bstack1111ll1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᅛ"), str(bstack11llll111_opy_))
            else:
                bstack1ll1llll11_opy_(item._page, bstack1111ll1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᅜ"))
    except Exception as e:
        summary.append(bstack1111ll1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᅝ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1111ll1_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᅞ"), default=bstack1111ll1_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᅟ"), help=bstack1111ll1_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᅠ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1111ll1_opy_ (u"ࠦ࠲࠳ࡤࡳ࡫ࡹࡩࡷࠨᅡ"), action=bstack1111ll1_opy_ (u"ࠧࡹࡴࡰࡴࡨࠦᅢ"), default=bstack1111ll1_opy_ (u"ࠨࡣࡩࡴࡲࡱࡪࠨᅣ"),
                         help=bstack1111ll1_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠࡵࡱࠣࡶࡺࡴࠠࡵࡧࡶࡸࡸࠨᅤ"))
def bstack1l11l11l1l_opy_(log):
    if log[bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅥ")] == bstack1111ll1_opy_ (u"ࠩ࡟ࡲࠬᅦ"):
        return
    bstack1llll11lll_opy_.bstack1l11ll1ll1_opy_([{
        bstack1111ll1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᅧ"): log[bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᅨ")],
        bstack1111ll1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᅩ"): datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"࡚࠭ࠨᅪ"),
        bstack1111ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅫ"): log[bstack1111ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᅬ")],
        bstack1111ll1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᅭ"): bstack1l11l1llll_opy_
    }])
bstack1l11l111l1_opy_ = bstack1ll11l1ll1_opy_(bstack1l11l11l1l_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack1llll11lll_opy_.on():
            return
        global bstack1l11l1llll_opy_, bstack1l11l111l1_opy_
        bstack1l11l111l1_opy_.start()
        bstack1l11l111ll_opy_ = {
            bstack1111ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᅮ"): uuid4().__str__(),
            bstack1111ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᅯ"): datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"ࠬࡠࠧᅰ")
        }
        bstack1l11l1llll_opy_ = bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᅱ")]
        threading.current_thread().bstack1l11l1llll_opy_ = bstack1l11l1llll_opy_
        _1l111l1l1l_opy_[item.nodeid] = {**_1l111l1l1l_opy_[item.nodeid], **bstack1l11l111ll_opy_}
        bstack1l11l11l11_opy_(item, _1l111l1l1l_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᅲ"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡳࡷࡱࡸࡪࡹࡴࡠࡥࡤࡰࡱࡀࠠࡼࡿࠪᅳ"), str(err))
def pytest_runtest_setup(item):
    if bstack1l1lll1l1l_opy_():
        atexit.register(bstack11lll1l1l_opy_)
    try:
        if not bstack1llll11lll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1l11l111ll_opy_ = {
            bstack1111ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᅴ"): uuid,
            bstack1111ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᅵ"): datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"ࠫ࡟࠭ᅶ"),
            bstack1111ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᅷ"): bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᅸ"),
            bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᅹ"): bstack1111ll1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᅺ")
        }
        threading.current_thread().bstack1l11l11lll_opy_ = uuid
        if not _1l111l1l1l_opy_.get(item.nodeid, None):
            _1l111l1l1l_opy_[item.nodeid] = {bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᅻ"): []}
        _1l111l1l1l_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᅼ")].append(bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᅽ")])
        _1l111l1l1l_opy_[item.nodeid + bstack1111ll1_opy_ (u"ࠬ࠳ࡳࡦࡶࡸࡴࠬᅾ")] = bstack1l11l111ll_opy_
        bstack1l111ll11l_opy_(item, bstack1l11l111ll_opy_, bstack1111ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᅿ"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᆀ"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack1llll11lll_opy_.on():
            return
        bstack1l11l111ll_opy_ = {
            bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᆁ"): uuid4().__str__(),
            bstack1111ll1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᆂ"): datetime.datetime.utcnow().isoformat() + bstack1111ll1_opy_ (u"ࠪ࡞ࠬᆃ"),
            bstack1111ll1_opy_ (u"ࠫࡹࡿࡰࡦࠩᆄ"): bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᆅ"),
            bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᆆ"): bstack1111ll1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᆇ")
        }
        _1l111l1l1l_opy_[item.nodeid + bstack1111ll1_opy_ (u"ࠨ࠯ࡷࡩࡦࡸࡤࡰࡹࡱࠫᆈ")] = bstack1l11l111ll_opy_
        bstack1l111ll11l_opy_(item, bstack1l11l111ll_opy_, bstack1111ll1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᆉ"))
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲ࠿ࠦࡻࡾࠩᆊ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef):
    start_time = datetime.datetime.now()
    outcome = yield
    try:
        if not bstack1llll11lll_opy_.on():
            return
        bstack1l111lllll_opy_ = threading.current_thread().bstack1l11l11lll_opy_
        log = {
            bstack1111ll1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᆋ"): bstack1111ll1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᆌ"),
            bstack1111ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᆍ"): fixturedef.argname,
            bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᆎ"): threading.current_thread().bstack1l11l11lll_opy_,
            bstack1111ll1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᆏ"): bstack1l11l1l1l_opy_(),
            bstack1111ll1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᆐ"): bstack1l1ll1ll1l_opy_(outcome),
            bstack1111ll1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᆑ"): (datetime.datetime.now() - start_time).total_seconds() * 1000,
        }
        if log[bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᆒ")] == bstack1111ll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᆓ"):
            log[bstack1111ll1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᆔ")] = bstack1111ll1_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᆕ")
            log[bstack1111ll1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᆖ")] = outcome.exception.__str__()
        if not _1l111l11ll_opy_.get(bstack1l111lllll_opy_, None):
            _1l111l11ll_opy_[bstack1l111lllll_opy_] = []
        _1l111l11ll_opy_[bstack1l111lllll_opy_].append(log)
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᆗ"), str(err))
@bstack1llll11lll_opy_.bstack1l11ll1lll_opy_
def bstack1l111l1ll1_opy_(item, call, report):
    try:
        if report.when == bstack1111ll1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᆘ"):
            bstack1l11l111l1_opy_.reset()
        if report.when == bstack1111ll1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᆙ"):
            _1l111l1l1l_opy_[item.nodeid][bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᆚ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1111ll1_opy_ (u"࡚࠭ࠨᆛ")
            bstack1l11l11l11_opy_(item, _1l111l1l1l_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᆜ"), report, call)
        elif report.when in [bstack1111ll1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᆝ"), bstack1111ll1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᆞ")]:
            bstack1l111l1lll_opy_ = item.nodeid + bstack1111ll1_opy_ (u"ࠪ࠱ࠬᆟ") + report.when
            if report.skipped:
                hook_type = bstack1111ll1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᆠ") if report.when == bstack1111ll1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᆡ") else bstack1111ll1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᆢ")
                _1l111l1l1l_opy_[bstack1l111l1lll_opy_] = {
                    bstack1111ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᆣ"): uuid4().__str__(),
                    bstack1111ll1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᆤ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1111ll1_opy_ (u"ࠩ࡝ࠫᆥ"),
                    bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᆦ"): hook_type
                }
            _1l111l1l1l_opy_[bstack1l111l1lll_opy_][bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᆧ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1111ll1_opy_ (u"ࠬࡠࠧᆨ")
            if report.when == bstack1111ll1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᆩ"):
                bstack1l111lllll_opy_ = _1l111l1l1l_opy_[bstack1l111l1lll_opy_][bstack1111ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᆪ")]
                if _1l111l11ll_opy_.get(bstack1l111lllll_opy_, None):
                    bstack1llll11lll_opy_.bstack1l11ll1l11_opy_(_1l111l11ll_opy_[bstack1l111lllll_opy_])
            bstack1l111ll11l_opy_(item, _1l111l1l1l_opy_[bstack1l111l1lll_opy_], bstack1111ll1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᆫ"), report, call)
            if report.when == bstack1111ll1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᆬ"):
                if report.outcome == bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᆭ"):
                    bstack1l11l111ll_opy_ = {
                        bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᆮ"): uuid4().__str__(),
                        bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᆯ"): bstack1l11l1l1l_opy_(),
                        bstack1111ll1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᆰ"): bstack1l11l1l1l_opy_()
                    }
                    _1l111l1l1l_opy_[item.nodeid] = {**_1l111l1l1l_opy_[item.nodeid], **bstack1l11l111ll_opy_}
                    bstack1l11l11l11_opy_(item, _1l111l1l1l_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᆱ"))
                    bstack1l11l11l11_opy_(item, _1l111l1l1l_opy_[item.nodeid], bstack1111ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᆲ"), report, call)
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡤࡲࡩࡲࡥࡠࡱ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࢃࠧᆳ"), str(err))
def bstack1l111ll111_opy_(test, bstack1l11l111ll_opy_, result=None, call=None, bstack11l1ll1l_opy_=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111llll1_opy_ = {
        bstack1111ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᆴ"): bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠫࡺࡻࡩࡥࠩᆵ")],
        bstack1111ll1_opy_ (u"ࠬࡺࡹࡱࡧࠪᆶ"): bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࠫᆷ"),
        bstack1111ll1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᆸ"): test.name,
        bstack1111ll1_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᆹ"): {
            bstack1111ll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᆺ"): bstack1111ll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᆻ"),
            bstack1111ll1_opy_ (u"ࠫࡨࡵࡤࡦࠩᆼ"): inspect.getsource(test.obj)
        },
        bstack1111ll1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᆽ"): test.name,
        bstack1111ll1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᆾ"): test.name,
        bstack1111ll1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᆿ"): bstack1llll11lll_opy_.bstack1l1l111l1l_opy_(test),
        bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᇀ"): file_path,
        bstack1111ll1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᇁ"): file_path,
        bstack1111ll1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᇂ"): bstack1111ll1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᇃ"),
        bstack1111ll1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᇄ"): file_path,
        bstack1111ll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᇅ"): bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᇆ")],
        bstack1111ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᇇ"): bstack1111ll1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᇈ"),
        bstack1111ll1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᇉ"): {
            bstack1111ll1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᇊ"): test.nodeid
        },
        bstack1111ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪᇋ"): bstack1ll111111l_opy_(test.own_markers)
    }
    if bstack11l1ll1l_opy_ == bstack1111ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᇌ"):
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᇍ")] = bstack1111ll1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᇎ")
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᇏ")] = bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᇐ")]
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᇑ")] = bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᇒ")]
    if result:
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᇓ")] = result.outcome
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᇔ")] = result.duration * 1000
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᇕ")] = bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᇖ")]
        if result.failed:
            bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᇗ")] = bstack1llll11lll_opy_.bstack1l11lll111_opy_(call.excinfo.typename)
            bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᇘ")] = bstack1llll11lll_opy_.bstack1l1l1111ll_opy_(call.excinfo, result)
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᇙ")] = bstack1l11l111ll_opy_[bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᇚ")]
    return bstack1l111llll1_opy_
def bstack1l11l11ll1_opy_(test, bstack1l111l11l1_opy_, bstack11l1ll1l_opy_, result, call):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᇛ")]
    hook_data = {
        bstack1111ll1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇜ"): bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᇝ")],
        bstack1111ll1_opy_ (u"ࠪࡸࡾࡶࡥࠨᇞ"): bstack1111ll1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᇟ"),
        bstack1111ll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᇠ"): bstack1111ll1_opy_ (u"࠭ࡻࡾࠢࡩࡳࡷࠦࡻࡾࠩᇡ").format(bstack1llll11lll_opy_.bstack1l11l1lll1_opy_(hook_type), test.name),
        bstack1111ll1_opy_ (u"ࠧࡣࡱࡧࡽࠬᇢ"): {
            bstack1111ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᇣ"): bstack1111ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᇤ"),
            bstack1111ll1_opy_ (u"ࠪࡧࡴࡪࡥࠨᇥ"): None
        },
        bstack1111ll1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᇦ"): test.name,
        bstack1111ll1_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᇧ"): bstack1llll11lll_opy_.bstack1l1l111l1l_opy_(test),
        bstack1111ll1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᇨ"): file_path,
        bstack1111ll1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᇩ"): file_path,
        bstack1111ll1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᇪ"): bstack1111ll1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᇫ"),
        bstack1111ll1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᇬ"): file_path,
        bstack1111ll1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᇭ"): bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᇮ")],
        bstack1111ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᇯ"): bstack1111ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧᇰ"),
        bstack1111ll1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᇱ"): bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᇲ")]
    }
    if _1l111l1l1l_opy_.get(test.nodeid, None) is not None and _1l111l1l1l_opy_[test.nodeid].get(bstack1111ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᇳ"), None):
        hook_data[bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᇴ")] = _1l111l1l1l_opy_[test.nodeid][bstack1111ll1_opy_ (u"ࠬࡻࡵࡪࡦࠪᇵ")]
    if result:
        hook_data[bstack1111ll1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᇶ")] = result.outcome
        hook_data[bstack1111ll1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᇷ")] = result.duration * 1000
        hook_data[bstack1111ll1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᇸ")] = bstack1l111l11l1_opy_[bstack1111ll1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᇹ")]
        if result.failed:
            hook_data[bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᇺ")] = bstack1llll11lll_opy_.bstack1l11lll111_opy_(call.excinfo.typename)
            hook_data[bstack1111ll1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᇻ")] = bstack1llll11lll_opy_.bstack1l1l1111ll_opy_(call.excinfo, result)
    return hook_data
def bstack1l11l11l11_opy_(test, bstack1l11l111ll_opy_, bstack11l1ll1l_opy_, result=None, call=None):
    bstack1l111llll1_opy_ = bstack1l111ll111_opy_(test, bstack1l11l111ll_opy_, result, call, bstack11l1ll1l_opy_)
    driver = getattr(test, bstack1111ll1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᇼ"), None)
    if bstack11l1ll1l_opy_ == bstack1111ll1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᇽ") and driver:
        bstack1l111llll1_opy_[bstack1111ll1_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᇾ")] = bstack1llll11lll_opy_.bstack1l1l111111_opy_(driver)
    if bstack11l1ll1l_opy_ == bstack1111ll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᇿ"):
        bstack11l1ll1l_opy_ = bstack1111ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫሀ")
    bstack1l111lll11_opy_ = {
        bstack1111ll1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧሁ"): bstack11l1ll1l_opy_,
        bstack1111ll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ሂ"): bstack1l111llll1_opy_
    }
    bstack1llll11lll_opy_.bstack1l1l11111l_opy_(bstack1l111lll11_opy_)
def bstack1l111ll11l_opy_(test, bstack1l11l111ll_opy_, bstack11l1ll1l_opy_, result=None, call=None):
    hook_data = bstack1l11l11ll1_opy_(test, bstack1l11l111ll_opy_, bstack11l1ll1l_opy_, result, call)
    bstack1l111lll11_opy_ = {
        bstack1111ll1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩሃ"): bstack11l1ll1l_opy_,
        bstack1111ll1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨሄ"): hook_data
    }
    bstack1llll11lll_opy_.bstack1l1l11111l_opy_(bstack1l111lll11_opy_)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1llll11lll_opy_.on():
            return
        records = caplog.get_records(bstack1111ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬህ"))
        bstack1l11l1ll11_opy_ = []
        for record in records:
            if record.message == bstack1111ll1_opy_ (u"ࠨ࡞ࡱࠫሆ"):
                continue
            bstack1l11l1ll11_opy_.append({
                bstack1111ll1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬሇ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1111ll1_opy_ (u"ࠪ࡞ࠬለ"),
                bstack1111ll1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪሉ"): record.levelname,
                bstack1111ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ሊ"): record.message,
                bstack1111ll1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ላ"): _1l111l1l1l_opy_.get(request.node.nodeid).get(bstack1111ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬሌ"))
            })
        bstack1llll11lll_opy_.bstack1l11ll1ll1_opy_(bstack1l11l1ll11_opy_)
    except Exception as err:
        print(bstack1111ll1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡦࡳࡳࡪ࡟ࡧ࡫ࡻࡸࡺࡸࡥ࠻ࠢࡾࢁࠬል"), str(err))
def bstack1l111l1l11_opy_(driver_command, response):
    if driver_command == bstack1111ll1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ሎ"):
        bstack1llll11lll_opy_.bstack1l11l1l1ll_opy_({
            bstack1111ll1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩሏ"): response[bstack1111ll1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪሐ")],
            bstack1111ll1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬሑ"): bstack1l11l1llll_opy_
        })
@bstack1llll11lll_opy_.bstack1l11ll1lll_opy_
def bstack1l111ll1l1_opy_():
    if bstack1l1ll1l1ll_opy_():
        bstack1l1l1l111l_opy_(bstack1l111l1l11_opy_)
bstack1l111ll1l1_opy_()
def bstack11lll1l1l_opy_():
    global bstack1l1l1111_opy_
    bstack1llll11lll_opy_.bstack1l11llll1l_opy_()
    for driver in bstack1l1l1111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll1111l_opy_(self, *args, **kwargs):
    bstack111l1111_opy_ = bstack1lll1l11ll_opy_(self, *args, **kwargs)
    bstack1llll11lll_opy_.bstack1l11l1l11_opy_(self)
    return bstack111l1111_opy_
def bstack1lll11ll_opy_(framework_name):
    global bstack1l1l1111l_opy_
    global bstack1lllll1l1_opy_
    bstack1l1l1111l_opy_ = framework_name
    logger.info(bstack1ll1ll1lll_opy_.format(bstack1l1l1111l_opy_.split(bstack1111ll1_opy_ (u"࠭࠭ࠨሒ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1l1lll1l11_opy_():
            Service.start = bstack111lllll1_opy_
            Service.stop = bstack1llll11l_opy_
            webdriver.Remote.__init__ = bstack1lll1l1l11_opy_
            webdriver.Remote.get = bstack111l1ll1l_opy_
            if not isinstance(os.getenv(bstack1111ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨሓ")), str):
                return
            WebDriver.close = bstack1ll11lll_opy_
            WebDriver.quit = bstack1l1llllll_opy_
        if not bstack1l1lll1l11_opy_() and bstack1llll11lll_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1111l_opy_
        bstack1lllll1l1_opy_ = True
    except Exception as e:
        pass
    bstack11ll11l1l_opy_()
    if os.environ.get(bstack1111ll1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ሔ")):
        bstack1lllll1l1_opy_ = eval(os.environ.get(bstack1111ll1_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧሕ")))
    if not bstack1lllll1l1_opy_:
        bstack1lll1ll1l1_opy_(bstack1111ll1_opy_ (u"ࠥࡔࡦࡩ࡫ࡢࡩࡨࡷࠥࡴ࡯ࡵࠢ࡬ࡲࡸࡺࡡ࡭࡮ࡨࡨࠧሖ"), bstack11111l1l1_opy_)
    if bstack1ll111l1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l111lll1_opy_
        except Exception as e:
            logger.error(bstack1lllllll1_opy_.format(str(e)))
    if bstack1111ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫሗ") in str(framework_name).lower():
        if not bstack1l1lll1l11_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1l1l1ll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack11111l11_opy_
            Config.getoption = bstack1lllll1111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11l11ll1_opy_
        except Exception as e:
            pass
def bstack1l1llllll_opy_(self):
    global bstack1l1l1111l_opy_
    global bstack1ll1llllll_opy_
    global bstack11ll1l111_opy_
    try:
        if bstack1111ll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬመ") in bstack1l1l1111l_opy_ and self.session_id != None:
            bstack111111lll_opy_ = bstack1111ll1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ሙ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧሚ")
            bstack1l1ll1l1_opy_ = bstack1l1l11ll_opy_(bstack1111ll1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫማ"), bstack1111ll1_opy_ (u"ࠩࠪሜ"), bstack111111lll_opy_, bstack1111ll1_opy_ (u"ࠪ࠰ࠥ࠭ም").join(
                threading.current_thread().bstackTestErrorMessages), bstack1111ll1_opy_ (u"ࠫࠬሞ"), bstack1111ll1_opy_ (u"ࠬ࠭ሟ"))
            if self != None:
                self.execute_script(bstack1l1ll1l1_opy_)
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࠢሠ") + str(e))
    bstack11ll1l111_opy_(self)
    self.session_id = None
def bstack1lll1l1l11_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1llllll_opy_
    global bstack1l111l1l1_opy_
    global bstack1llll1ll_opy_
    global bstack1l1l1111l_opy_
    global bstack1lll1l11ll_opy_
    global bstack1l1l1111_opy_
    global bstack1ll1111l1_opy_
    global bstack11l1l1ll_opy_
    CONFIG[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩሡ")] = str(bstack1l1l1111l_opy_) + str(__version__)
    command_executor = bstack11l1111ll_opy_(bstack1ll1111l1_opy_)
    logger.debug(bstack111ll1l1_opy_.format(command_executor))
    proxy = bstack11ll1l1ll_opy_(CONFIG, proxy)
    bstack1ll1l1lll_opy_ = 0
    try:
        if bstack1llll1ll_opy_ is True:
            bstack1ll1l1lll_opy_ = int(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨሢ")))
    except:
        bstack1ll1l1lll_opy_ = 0
    bstack1111l111_opy_ = bstack1lll111l_opy_(CONFIG, bstack1ll1l1lll_opy_)
    logger.debug(bstack1l11ll111_opy_.format(str(bstack1111l111_opy_)))
    if bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ሣ") in CONFIG and CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧሤ")]:
        bstack1l11llll1_opy_(bstack1111l111_opy_, bstack11l1l1ll_opy_)
    if desired_capabilities:
        bstack1llllll111_opy_ = bstack11lll11ll_opy_(desired_capabilities)
        bstack1llllll111_opy_[bstack1111ll1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫሥ")] = bstack11ll1l1l_opy_(CONFIG)
        bstack1ll11llll_opy_ = bstack1lll111l_opy_(bstack1llllll111_opy_)
        if bstack1ll11llll_opy_:
            bstack1111l111_opy_ = update(bstack1ll11llll_opy_, bstack1111l111_opy_)
        desired_capabilities = None
    if options:
        bstack111111111_opy_(options, bstack1111l111_opy_)
    if not options:
        options = bstack111llll11_opy_(bstack1111l111_opy_)
    if proxy and bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬሦ")):
        options.proxy(proxy)
    if options and bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬሧ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1l11l1l_opy_() < version.parse(bstack1111ll1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ረ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1111l111_opy_)
    logger.info(bstack1l11l111_opy_)
    if bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨሩ")):
        bstack1lll1l11ll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨሪ")):
        bstack1lll1l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪራ")):
        bstack1lll1l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1lll1l11ll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack11ll1ll1_opy_ = bstack1111ll1_opy_ (u"ࠫࠬሬ")
        if bstack1ll1l11l1l_opy_() >= version.parse(bstack1111ll1_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ር")):
            bstack11ll1ll1_opy_ = self.caps.get(bstack1111ll1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨሮ"))
        else:
            bstack11ll1ll1_opy_ = self.capabilities.get(bstack1111ll1_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢሯ"))
        if bstack11ll1ll1_opy_:
            if bstack1ll1l11l1l_opy_() <= version.parse(bstack1111ll1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨሰ")):
                self.command_executor._url = bstack1111ll1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥሱ") + bstack1ll1111l1_opy_ + bstack1111ll1_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢሲ")
            else:
                self.command_executor._url = bstack1111ll1_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨሳ") + bstack11ll1ll1_opy_ + bstack1111ll1_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨሴ")
            logger.debug(bstack1llll1111l_opy_.format(bstack11ll1ll1_opy_))
        else:
            logger.debug(bstack1l1llll11_opy_.format(bstack1111ll1_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢስ")))
    except Exception as e:
        logger.debug(bstack1l1llll11_opy_.format(e))
    bstack1ll1llllll_opy_ = self.session_id
    if bstack1111ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧሶ") in bstack1l1l1111l_opy_:
        threading.current_thread().bstack1llll1l1_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1llll11lll_opy_.bstack1l11l1l11_opy_(self)
    bstack1l1l1111_opy_.append(self)
    if bstack1111ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫሷ") in CONFIG and bstack1111ll1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧሸ") in CONFIG[bstack1111ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ሹ")][bstack1ll1l1lll_opy_]:
        bstack1l111l1l1_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧሺ")][bstack1ll1l1lll_opy_][bstack1111ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪሻ")]
    logger.debug(bstack1ll1l111l_opy_.format(bstack1ll1llllll_opy_))
def bstack111l1ll1l_opy_(self, url):
    global bstack11llllll1_opy_
    global CONFIG
    try:
        bstack1ll1ll1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l11l11l1_opy_.format(str(err)))
    try:
        bstack11llllll1_opy_(self, url)
    except Exception as e:
        try:
            bstack1lll1ll111_opy_ = str(e)
            if any(err_msg in bstack1lll1ll111_opy_ for err_msg in bstack1lll11lll1_opy_):
                bstack1ll1ll1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l11l11l1_opy_.format(str(err)))
        raise e
def bstack1111l1111_opy_(item, when):
    global bstack111111ll_opy_
    try:
        bstack111111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack11l11ll1_opy_(item, call, rep):
    global bstack11llll1ll_opy_
    global bstack1l1l1111_opy_
    name = bstack1111ll1_opy_ (u"࠭ࠧሼ")
    try:
        if rep.when == bstack1111ll1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬሽ"):
            bstack1ll1llllll_opy_ = threading.current_thread().bstack1llll1l1_opy_
            bstack1l11l11111_opy_ = item.config.getoption(bstack1111ll1_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪሾ"))
            try:
                if (str(bstack1l11l11111_opy_).lower() != bstack1111ll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧሿ")):
                    name = str(rep.nodeid)
                    bstack1l1ll1l1_opy_ = bstack1l1l11ll_opy_(bstack1111ll1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫቀ"), name, bstack1111ll1_opy_ (u"ࠫࠬቁ"), bstack1111ll1_opy_ (u"ࠬ࠭ቂ"), bstack1111ll1_opy_ (u"࠭ࠧቃ"), bstack1111ll1_opy_ (u"ࠧࠨቄ"))
                    for driver in bstack1l1l1111_opy_:
                        if bstack1ll1llllll_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack1111ll1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨቅ").format(str(e)))
            try:
                status = bstack1111ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቆ") if rep.outcome.lower() == bstack1111ll1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪቇ") else bstack1111ll1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫቈ")
                reason = bstack1111ll1_opy_ (u"ࠬ࠭቉")
                if (reason != bstack1111ll1_opy_ (u"ࠨࠢቊ")):
                    try:
                        if (threading.current_thread().bstackTestErrorMessages == None):
                            threading.current_thread().bstackTestErrorMessages = []
                    except Exception as e:
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(str(reason))
                if status == bstack1111ll1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧቋ"):
                    reason = rep.longrepr.reprcrash.message
                    if (not threading.current_thread().bstackTestErrorMessages):
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(reason)
                level = bstack1111ll1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ቌ") if status == bstack1111ll1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩቍ") else bstack1111ll1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ቎")
                data = name + bstack1111ll1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭቏") if status == bstack1111ll1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬቐ") else name + bstack1111ll1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩቑ") + reason
                bstack1l11ll1l_opy_ = bstack1l1l11ll_opy_(bstack1111ll1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩቒ"), bstack1111ll1_opy_ (u"ࠨࠩቓ"), bstack1111ll1_opy_ (u"ࠩࠪቔ"), bstack1111ll1_opy_ (u"ࠪࠫቕ"), level, data)
                for driver in bstack1l1l1111_opy_:
                    if bstack1ll1llllll_opy_ == driver.session_id:
                        driver.execute_script(bstack1l11ll1l_opy_)
            except Exception as e:
                logger.debug(bstack1111ll1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨቖ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩ቗").format(str(e)))
    bstack11llll1ll_opy_(item, call, rep)
notset = Notset()
def bstack1lllll1111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lll11l11l_opy_
    if str(name).lower() == bstack1111ll1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ቘ"):
        return bstack1111ll1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨ቙")
    else:
        return bstack1lll11l11l_opy_(self, name, default, skip)
def bstack1l111lll1_opy_(self):
    global CONFIG
    global bstack11lllll1_opy_
    try:
        proxy = bstack1llll11l11_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1111ll1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ቚ")):
                proxies = bstack1ll111l11_opy_(proxy, bstack11l1111ll_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1111ll_opy_ = proxies.popitem()
                    if bstack1111ll1_opy_ (u"ࠤ࠽࠳࠴ࠨቛ") in bstack1l1111ll_opy_:
                        return bstack1l1111ll_opy_
                    else:
                        return bstack1111ll1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦቜ") + bstack1l1111ll_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1111ll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣቝ").format(str(e)))
    return bstack11lllll1_opy_(self)
def bstack1ll111l1_opy_():
    return bstack1111ll1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ቞") in CONFIG or bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ቟") in CONFIG and bstack1ll1l11l1l_opy_() >= version.parse(
        bstack1ll1l1l11l_opy_)
def bstack111llll1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l111l1l1_opy_
    global bstack1llll1ll_opy_
    global bstack1l1l1111l_opy_
    CONFIG[bstack1111ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩበ")] = str(bstack1l1l1111l_opy_) + str(__version__)
    bstack1ll1l1lll_opy_ = 0
    try:
        if bstack1llll1ll_opy_ is True:
            bstack1ll1l1lll_opy_ = int(os.environ.get(bstack1111ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨቡ")))
    except:
        bstack1ll1l1lll_opy_ = 0
    CONFIG[bstack1111ll1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣቢ")] = True
    bstack1111l111_opy_ = bstack1lll111l_opy_(CONFIG, bstack1ll1l1lll_opy_)
    logger.debug(bstack1l11ll111_opy_.format(str(bstack1111l111_opy_)))
    if CONFIG[bstack1111ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧባ")]:
        bstack1l11llll1_opy_(bstack1111l111_opy_, bstack11l1l1ll_opy_)
    if bstack1111ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቤ") in CONFIG and bstack1111ll1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪብ") in CONFIG[bstack1111ll1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩቦ")][bstack1ll1l1lll_opy_]:
        bstack1l111l1l1_opy_ = CONFIG[bstack1111ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪቧ")][bstack1ll1l1lll_opy_][bstack1111ll1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ቨ")]
    import urllib
    import json
    bstack111111ll1_opy_ = bstack1111ll1_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫቩ") + urllib.parse.quote(json.dumps(bstack1111l111_opy_))
    browser = self.connect(bstack111111ll1_opy_)
    return browser
def bstack11ll11l1l_opy_():
    global bstack1lllll1l1_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack111llll1l_opy_
        bstack1lllll1l1_opy_ = True
    except Exception as e:
        pass
def bstack1l111lll1l_opy_():
    global CONFIG
    global bstack1llllll1l_opy_
    global bstack1ll1111l1_opy_
    global bstack11l1l1ll_opy_
    global bstack1llll1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack1111ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩቪ")))
    bstack1llllll1l_opy_ = eval(os.environ.get(bstack1111ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬቫ")))
    bstack1ll1111l1_opy_ = os.environ.get(bstack1111ll1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬቬ"))
    bstack1lll1lll1l_opy_(CONFIG, bstack1llllll1l_opy_)
    bstack11l11ll1l_opy_()
    global bstack1lll1l11ll_opy_
    global bstack11ll1l111_opy_
    global bstack1111ll1l_opy_
    global bstack1111l111l_opy_
    global bstack1ll1lll1l1_opy_
    global bstack1l11lllll_opy_
    global bstack1l111lll_opy_
    global bstack11llllll1_opy_
    global bstack11lllll1_opy_
    global bstack1lll11l11l_opy_
    global bstack111111ll_opy_
    global bstack11llll1ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1lll1l11ll_opy_ = webdriver.Remote.__init__
        bstack11ll1l111_opy_ = WebDriver.quit
        bstack1l111lll_opy_ = WebDriver.close
        bstack11llllll1_opy_ = WebDriver.get
    except Exception as e:
        pass
    if bstack1111ll1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩቭ") in CONFIG or bstack1111ll1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫቮ") in CONFIG:
        if bstack1ll1l11l1l_opy_() < version.parse(bstack1ll1l1l11l_opy_):
            logger.error(bstack1l1ll1l11_opy_.format(bstack1ll1l11l1l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack11lllll1_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1lllllll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1lll11l11l_opy_ = Config.getoption
        from _pytest import runner
        bstack111111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1llllll11_opy_)
    try:
        from pytest_bdd import reporting
        bstack11llll1ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1111ll1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩቯ"))
    bstack11l1l1ll_opy_ = CONFIG.get(bstack1111ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ተ"), {}).get(bstack1111ll1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬቱ"))
    bstack1llll1ll_opy_ = True
    bstack1lll11ll_opy_(bstack1ll1ll11ll_opy_)
if (bstack1l1lll1l1l_opy_()):
    bstack1l111lll1l_opy_()