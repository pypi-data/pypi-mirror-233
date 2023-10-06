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
import datetime
import inspect
import logging
import os
import sys
import threading
from uuid import uuid4
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11ll1l1l_opy_, bstack1l111l1l_opy_, update, bstack11l111ll_opy_,
                                       bstack111l11l1_opy_, bstack1lll1111ll_opy_, bstack1ll1l1l111_opy_, bstack1l1l1lll1_opy_,
                                       bstack1lll1ll1ll_opy_, bstack1l1l1111_opy_, bstack11111l1ll_opy_, bstack11ll1lll_opy_,
                                       bstack111l111l_opy_)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1ll11l1lll_opy_
from bstack_utils.constants import bstack11l1l111_opy_, bstack1llll111l1_opy_, bstack1l11ll11l_opy_, bstack11ll1ll11_opy_, \
    bstack111l1l1l1_opy_
from bstack_utils.helper import bstack1l1lll111l_opy_, bstack1ll1111l11_opy_, bstack111ll111_opy_, bstack1l1llll111_opy_, \
    bstack1l1ll1ll1l_opy_, bstack1ll111ll1_opy_, bstack1lll1l1111_opy_, bstack1ll11111l1_opy_, bstack1ll11111ll_opy_, Notset, \
    bstack1111llll1_opy_, bstack1ll1111ll1_opy_
from bstack_utils.messages import bstack11lll1111_opy_, bstack111l11lll_opy_, bstack1l1lll1ll_opy_, bstack1l111ll1_opy_, bstack1lll111l_opy_, \
    bstack1l11l1l1_opy_, bstack11l1l1l11_opy_, bstack1lllll1111_opy_, bstack11l1l11ll_opy_, bstack1111ll11l_opy_, \
    bstack1llllll11_opy_, bstack1l11ll111_opy_
from bstack_utils.proxy import bstack1lll11lll_opy_, bstack1lll1lll1l_opy_
from bstack_utils.bstack1l1l11ll11_opy_ import bstack1l1l1l111l_opy_
from bstack_utils.bstack1l1l11l1l1_opy_ import bstack1lllll1ll_opy_, bstack1llllll1ll_opy_, bstack11ll1l11l_opy_
from bstack_utils.bstack1ll111111_opy_ import bstack1l111l1ll_opy_
bstack1111ll1l_opy_ = None
bstack11l11l1ll_opy_ = None
bstack11ll1l1l1_opy_ = None
bstack111l11l11_opy_ = None
bstack11l11lll1_opy_ = None
bstack1ll1lll1_opy_ = None
bstack11l11l11l_opy_ = None
bstack1ll1ll111_opy_ = None
bstack111l1l11l_opy_ = None
bstack111llll1l_opy_ = None
bstack1lllll11l1_opy_ = None
bstack1lll1ll1l_opy_ = None
bstack11ll11l1_opy_ = None
bstack11ll11ll1_opy_ = bstack1_opy_ (u"ࠬ࠭ᄣ")
CONFIG = {}
bstack11111111_opy_ = False
bstack111111l1l_opy_ = bstack1_opy_ (u"࠭ࠧᄤ")
bstack1ll1l111l_opy_ = bstack1_opy_ (u"ࠧࠨᄥ")
bstack1l111111l_opy_ = False
bstack1111ll111_opy_ = []
bstack111l1llll_opy_ = bstack1llll111l1_opy_
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack111l1llll_opy_,
                    format=bstack1_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᄦ"),
                    datefmt=bstack1_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᄧ"),
                    stream=sys.stdout)
def bstack1l1l11ll1_opy_():
    global CONFIG
    global bstack111l1llll_opy_
    if bstack1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᄨ") in CONFIG:
        bstack111l1llll_opy_ = bstack11l1l111_opy_[CONFIG[bstack1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᄩ")]]
        logging.getLogger().setLevel(bstack111l1llll_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111lll1l_opy_ = {}
bstack1l11ll1ll1_opy_ = None
_1l111ll11l_opy_ = {}
def bstack1l1l1l1ll_opy_(page, bstack1lll111l1l_opy_):
    try:
        page.evaluate(bstack1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᄪ"),
                      bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠪᄫ") + json.dumps(
                          bstack1lll111l1l_opy_) + bstack1_opy_ (u"ࠢࡾࡿࠥᄬ"))
    except Exception as e:
        print(bstack1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣࡿࢂࠨᄭ"), e)
def bstack111ll1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᄮ"), bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨᄯ") + json.dumps(
            message) + bstack1_opy_ (u"ࠫ࠱ࠨ࡬ࡦࡸࡨࡰࠧࡀࠧᄰ") + json.dumps(level) + bstack1_opy_ (u"ࠬࢃࡽࠨᄱ"))
    except Exception as e:
        print(bstack1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡤࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠦࡻࡾࠤᄲ"), e)
def bstack11llll1l_opy_(page, status, message=bstack1_opy_ (u"ࠢࠣᄳ")):
    try:
        if (status == bstack1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣᄴ")):
            page.evaluate(bstack1_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᄵ"),
                          bstack1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠫᄶ") + json.dumps(
                              bstack1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࠨᄷ") + str(message)) + bstack1_opy_ (u"ࠬ࠲ࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩᄸ") + json.dumps(status) + bstack1_opy_ (u"ࠨࡽࡾࠤᄹ"))
        else:
            page.evaluate(bstack1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᄺ"),
                          bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡴࡶࡤࡸࡺࡹࠢ࠻ࠩᄻ") + json.dumps(
                              status) + bstack1_opy_ (u"ࠤࢀࢁࠧᄼ"))
    except Exception as e:
        print(bstack1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤࢀࢃࠢᄽ"), e)
def pytest_configure(config):
    config.args = bstack1l111l1ll_opy_.bstack1l11ll1lll_opy_(config.args)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1l111l1l11_opy_ = item.config.getoption(bstack1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᄾ"))
    plugins = item.config.getoption(bstack1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨᄿ"))
    report = outcome.get_result()
    bstack1l11l11ll1_opy_(item, call, report)
    if bstack1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦᅀ") not in plugins or bstack1ll11111ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣᅁ"), None)
    page = getattr(item, bstack1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢᅂ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1l111ll1l1_opy_(item, report, summary, bstack1l111l1l11_opy_)
    if (page is not None):
        bstack1l111lll11_opy_(item, report, summary, bstack1l111l1l11_opy_)
def bstack1l111ll1l1_opy_(item, report, summary, bstack1l111l1l11_opy_):
    if report.when in [bstack1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᅃ"), bstack1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᅄ")]:
        return
    if not bstack1ll1111l11_opy_():
        return
    if (str(bstack1l111l1l11_opy_).lower() != bstack1_opy_ (u"ࠫࡹࡸࡵࡦࠩᅅ")):
        item._driver.execute_script(
            bstack1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᅆ") + json.dumps(
                report.nodeid) + bstack1_opy_ (u"࠭ࡽࡾࠩᅇ"))
    passed = report.passed or (report.failed and hasattr(report, bstack1_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᅈ")))
    bstack11l11111l_opy_ = bstack1_opy_ (u"ࠣࠤᅉ")
    if not passed:
        try:
            bstack11l11111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡪࡦ࡯࡬ࡶࡴࡨࠤࡷ࡫ࡡࡴࡱࡱ࠾ࠥࢁ࠰ࡾࠤᅊ").format(e)
            )
    if (bstack11l11111l_opy_ != bstack1_opy_ (u"ࠥࠦᅋ")):
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11l11111l_opy_))
    try:
        if (passed):
            item._driver.execute_script(
                bstack1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᅌ")
                + json.dumps(bstack1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠦࠨᅍ"))
                + bstack1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᅎ")
            )
        else:
            item._driver.execute_script(
                bstack1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪᅏ")
                + json.dumps(str(bstack11l11111l_opy_))
                + bstack1_opy_ (u"ࠣ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᅐ")
            )
    except Exception as e:
        summary.append(bstack1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡢࡰࡱࡳࡹࡧࡴࡦ࠼ࠣࡿ࠵ࢃࠢᅑ").format(e))
def bstack1l111lll11_opy_(item, report, summary, bstack1l111l1l11_opy_):
    if report.when in [bstack1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᅒ"), bstack1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᅓ")]:
        return
    if (str(bstack1l111l1l11_opy_).lower() != bstack1_opy_ (u"ࠬࡺࡲࡶࡧࠪᅔ")):
        bstack1l1l1l1ll_opy_(item._page, report.nodeid)
    passed = report.passed or (report.failed and hasattr(report, bstack1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᅕ")))
    bstack11l11111l_opy_ = bstack1_opy_ (u"ࠢࠣᅖ")
    if not passed:
        try:
            bstack11l11111l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᅗ").format(e)
            )
    try:
        if passed:
            bstack11llll1l_opy_(item._page, bstack1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤᅘ"))
        else:
            if bstack11l11111l_opy_:
                bstack111ll1l1l_opy_(item._page, str(bstack11l11111l_opy_), bstack1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᅙ"))
                bstack11llll1l_opy_(item._page, bstack1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᅚ"), str(bstack11l11111l_opy_))
            else:
                bstack11llll1l_opy_(item._page, bstack1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᅛ"))
    except Exception as e:
        summary.append(bstack1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻ࠱ࡿࠥᅜ").format(e))
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
    parser.addoption(bstack1_opy_ (u"ࠢ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦᅝ"), default=bstack1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢᅞ"), help=bstack1_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡧࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠣᅟ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1_opy_ (u"ࠥ࠱࠲ࡪࡲࡪࡸࡨࡶࠧᅠ"), action=bstack1_opy_ (u"ࠦࡸࡺ࡯ࡳࡧࠥᅡ"), default=bstack1_opy_ (u"ࠧࡩࡨࡳࡱࡰࡩࠧᅢ"),
                         help=bstack1_opy_ (u"ࠨࡄࡳ࡫ࡹࡩࡷࠦࡴࡰࠢࡵࡹࡳࠦࡴࡦࡵࡷࡷࠧᅣ"))
def bstack1l11l11lll_opy_(log):
    if log[bstack1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅤ")] == bstack1_opy_ (u"ࠨ࡞ࡱࠫᅥ"):
        return
    bstack1l111l1ll_opy_.bstack1l1l111l1l_opy_([{
        bstack1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᅦ"): log[bstack1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᅧ")],
        bstack1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᅨ"): datetime.datetime.utcnow().isoformat() + bstack1_opy_ (u"ࠬࡠࠧᅩ"),
        bstack1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᅪ"): log[bstack1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᅫ")],
        bstack1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᅬ"): bstack1l11ll1ll1_opy_
    }])
bstack1l111llll1_opy_ = bstack1ll11l1lll_opy_(bstack1l11l11lll_opy_)
def pytest_runtest_call(item):
    try:
        if not bstack1l111l1ll_opy_.on():
            return
        global bstack1l11ll1ll1_opy_, bstack1l111llll1_opy_
        bstack1l111llll1_opy_.start()
        bstack1l11l111ll_opy_ = {
            bstack1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᅭ"): uuid4().__str__(),
            bstack1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᅮ"): datetime.datetime.utcnow().isoformat() + bstack1_opy_ (u"ࠫ࡟࠭ᅯ")
        }
        bstack1l11ll1ll1_opy_ = bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠬࡻࡵࡪࡦࠪᅰ")]
        threading.current_thread().bstack1l11ll1ll1_opy_ = bstack1l11ll1ll1_opy_
        _1l111lll1l_opy_[item.nodeid] = {**_1l111lll1l_opy_[item.nodeid], **bstack1l11l111ll_opy_}
        bstack1l111lllll_opy_(item, _1l111lll1l_opy_[item.nodeid], bstack1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᅱ"))
    except Exception as err:
        print(bstack1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩᅲ"), str(err))
def pytest_runtest_setup(item):
    if bstack1ll11111l1_opy_():
        atexit.register(bstack1lll1l1l1l_opy_)
    try:
        if not bstack1l111l1ll_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack1l11l111ll_opy_ = {
            bstack1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᅳ"): uuid,
            bstack1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᅴ"): datetime.datetime.utcnow().isoformat() + bstack1_opy_ (u"ࠪ࡞ࠬᅵ"),
            bstack1_opy_ (u"ࠫࡹࡿࡰࡦࠩᅶ"): bstack1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᅷ"),
            bstack1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᅸ"): bstack1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᅹ")
        }
        threading.current_thread().bstack1l11l11111_opy_ = uuid
        if not _1l111lll1l_opy_.get(item.nodeid, None):
            _1l111lll1l_opy_[item.nodeid] = {bstack1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᅺ"): []}
        _1l111lll1l_opy_[item.nodeid][bstack1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᅻ")].append(bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᅼ")])
        _1l111lll1l_opy_[item.nodeid + bstack1_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫᅽ")] = bstack1l11l111ll_opy_
        bstack1l111ll1ll_opy_(item, bstack1l11l111ll_opy_, bstack1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᅾ"))
    except Exception as err:
        print(bstack1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᅿ"), str(err))
def pytest_runtest_teardown(item):
    try:
        if not bstack1l111l1ll_opy_.on():
            return
        bstack1l11l111ll_opy_ = {
            bstack1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᆀ"): uuid4().__str__(),
            bstack1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᆁ"): datetime.datetime.utcnow().isoformat() + bstack1_opy_ (u"ࠩ࡝ࠫᆂ"),
            bstack1_opy_ (u"ࠪࡸࡾࡶࡥࠨᆃ"): bstack1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᆄ"),
            bstack1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᆅ"): bstack1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᆆ")
        }
        _1l111lll1l_opy_[item.nodeid + bstack1_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᆇ")] = bstack1l11l111ll_opy_
        bstack1l111ll1ll_opy_(item, bstack1l11l111ll_opy_, bstack1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᆈ"))
    except Exception as err:
        print(bstack1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨᆉ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef):
    start_time = datetime.datetime.now()
    outcome = yield
    try:
        if not bstack1l111l1ll_opy_.on():
            return
        bstack1l11l11l1l_opy_ = threading.current_thread().bstack1l11l11111_opy_
        log = {
            bstack1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᆊ"): bstack1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧᆋ"),
            bstack1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᆌ"): fixturedef.argname,
            bstack1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᆍ"): threading.current_thread().bstack1l11l11111_opy_,
            bstack1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᆎ"): bstack111ll111_opy_(),
            bstack1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᆏ"): bstack1l1llll111_opy_(outcome),
            bstack1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᆐ"): (datetime.datetime.now() - start_time).total_seconds() * 1000,
        }
        if log[bstack1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᆑ")] == bstack1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᆒ"):
            log[bstack1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᆓ")] = bstack1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᆔ")
            log[bstack1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᆕ")] = outcome.exception.__str__()
        if not _1l111ll11l_opy_.get(bstack1l11l11l1l_opy_, None):
            _1l111ll11l_opy_[bstack1l11l11l1l_opy_] = []
        _1l111ll11l_opy_[bstack1l11l11l1l_opy_].append(log)
    except Exception as err:
        print(bstack1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠࡵࡨࡸࡺࡶ࠺ࠡࡽࢀࠫᆖ"), str(err))
@bstack1l111l1ll_opy_.bstack1l11l1l111_opy_
def bstack1l11l11ll1_opy_(item, call, report):
    try:
        if report.when == bstack1_opy_ (u"ࠩࡦࡥࡱࡲࠧᆗ"):
            bstack1l111llll1_opy_.reset()
        if report.when == bstack1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᆘ"):
            _1l111lll1l_opy_[item.nodeid][bstack1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᆙ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1_opy_ (u"ࠬࡠࠧᆚ")
            bstack1l111lllll_opy_(item, _1l111lll1l_opy_[item.nodeid], bstack1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᆛ"), report, call)
        elif report.when in [bstack1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᆜ"), bstack1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᆝ")]:
            bstack1l111l1l1l_opy_ = item.nodeid + bstack1_opy_ (u"ࠩ࠰ࠫᆞ") + report.when
            if report.skipped:
                hook_type = bstack1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᆟ") if report.when == bstack1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᆠ") else bstack1_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩᆡ")
                _1l111lll1l_opy_[bstack1l111l1l1l_opy_] = {
                    bstack1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᆢ"): uuid4().__str__(),
                    bstack1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᆣ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1_opy_ (u"ࠨ࡜ࠪᆤ"),
                    bstack1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᆥ"): hook_type
                }
            _1l111lll1l_opy_[bstack1l111l1l1l_opy_][bstack1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᆦ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1_opy_ (u"ࠫ࡟࠭ᆧ")
            if report.when == bstack1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᆨ"):
                bstack1l11l11l1l_opy_ = _1l111lll1l_opy_[bstack1l111l1l1l_opy_][bstack1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᆩ")]
                if _1l111ll11l_opy_.get(bstack1l11l11l1l_opy_, None):
                    bstack1l111l1ll_opy_.bstack1l1l111111_opy_(_1l111ll11l_opy_[bstack1l11l11l1l_opy_])
            bstack1l111ll1ll_opy_(item, _1l111lll1l_opy_[bstack1l111l1l1l_opy_], bstack1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᆪ"), report, call)
            if report.when == bstack1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᆫ"):
                if report.outcome == bstack1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᆬ"):
                    bstack1l11l111ll_opy_ = {
                        bstack1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᆭ"): uuid4().__str__(),
                        bstack1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᆮ"): bstack111ll111_opy_(),
                        bstack1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᆯ"): bstack111ll111_opy_()
                    }
                    _1l111lll1l_opy_[item.nodeid] = {**_1l111lll1l_opy_[item.nodeid], **bstack1l11l111ll_opy_}
                    bstack1l111lllll_opy_(item, _1l111lll1l_opy_[item.nodeid], bstack1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᆰ"))
                    bstack1l111lllll_opy_(item, _1l111lll1l_opy_[item.nodeid], bstack1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᆱ"), report, call)
    except Exception as err:
        print(bstack1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭ᆲ"), str(err))
def bstack1l11l11l11_opy_(test, bstack1l11l111ll_opy_, result=None, call=None, bstack1l1111ll_opy_=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l11l111l1_opy_ = {
        bstack1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᆳ"): bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᆴ")],
        bstack1_opy_ (u"ࠫࡹࡿࡰࡦࠩᆵ"): bstack1_opy_ (u"ࠬࡺࡥࡴࡶࠪᆶ"),
        bstack1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᆷ"): test.name,
        bstack1_opy_ (u"ࠧࡣࡱࡧࡽࠬᆸ"): {
            bstack1_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᆹ"): bstack1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᆺ"),
            bstack1_opy_ (u"ࠪࡧࡴࡪࡥࠨᆻ"): inspect.getsource(test.obj)
        },
        bstack1_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᆼ"): test.name,
        bstack1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᆽ"): test.name,
        bstack1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᆾ"): bstack1l111l1ll_opy_.bstack1l1l1111l1_opy_(test),
        bstack1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᆿ"): file_path,
        bstack1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᇀ"): file_path,
        bstack1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᇁ"): bstack1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᇂ"),
        bstack1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᇃ"): file_path,
        bstack1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᇄ"): bstack1l11l111ll_opy_[bstack1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᇅ")],
        bstack1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᇆ"): bstack1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᇇ"),
        bstack1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᇈ"): {
            bstack1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᇉ"): test.nodeid
        },
        bstack1_opy_ (u"ࠫࡹࡧࡧࡴࠩᇊ"): bstack1l1ll1ll1l_opy_(test.own_markers)
    }
    if bstack1l1111ll_opy_ == bstack1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᇋ"):
        bstack1l11l111l1_opy_[bstack1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᇌ")] = bstack1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᇍ")
        bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᇎ")] = bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᇏ")]
        bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᇐ")] = bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᇑ")]
    if result:
        bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᇒ")] = result.outcome
        bstack1l11l111l1_opy_[bstack1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᇓ")] = result.duration * 1000
        bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᇔ")] = bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᇕ")]
        if result.failed:
            bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᇖ")] = bstack1l111l1ll_opy_.bstack1l1l111l11_opy_(call.excinfo.typename)
            bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᇗ")] = bstack1l111l1ll_opy_.bstack1l11l1lll1_opy_(call.excinfo, result)
        bstack1l11l111l1_opy_[bstack1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᇘ")] = bstack1l11l111ll_opy_[bstack1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᇙ")]
    return bstack1l11l111l1_opy_
def bstack1l111l1lll_opy_(test, bstack1l111l1ll1_opy_, bstack1l1111ll_opy_, result, call):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111l1ll1_opy_[bstack1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᇚ")]
    hook_data = {
        bstack1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᇛ"): bstack1l111l1ll1_opy_[bstack1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᇜ")],
        bstack1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᇝ"): bstack1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᇞ"),
        bstack1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᇟ"): bstack1_opy_ (u"ࠬࢁࡽࠡࡨࡲࡶࠥࢁࡽࠨᇠ").format(bstack1l111l1ll_opy_.bstack1l11ll1111_opy_(hook_type), test.name),
        bstack1_opy_ (u"࠭ࡢࡰࡦࡼࠫᇡ"): {
            bstack1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᇢ"): bstack1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᇣ"),
            bstack1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᇤ"): None
        },
        bstack1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᇥ"): test.name,
        bstack1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᇦ"): bstack1l111l1ll_opy_.bstack1l1l1111l1_opy_(test),
        bstack1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᇧ"): file_path,
        bstack1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᇨ"): file_path,
        bstack1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᇩ"): bstack1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᇪ"),
        bstack1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᇫ"): file_path,
        bstack1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᇬ"): bstack1l111l1ll1_opy_[bstack1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᇭ")],
        bstack1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᇮ"): bstack1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᇯ"),
        bstack1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᇰ"): bstack1l111l1ll1_opy_[bstack1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᇱ")]
    }
    if _1l111lll1l_opy_.get(test.nodeid, None) is not None and _1l111lll1l_opy_[test.nodeid].get(bstack1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᇲ"), None):
        hook_data[bstack1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᇳ")] = _1l111lll1l_opy_[test.nodeid][bstack1_opy_ (u"ࠫࡺࡻࡩࡥࠩᇴ")]
    if result:
        hook_data[bstack1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᇵ")] = result.outcome
        hook_data[bstack1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᇶ")] = result.duration * 1000
        hook_data[bstack1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᇷ")] = bstack1l111l1ll1_opy_[bstack1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᇸ")]
        if result.failed:
            hook_data[bstack1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᇹ")] = bstack1l111l1ll_opy_.bstack1l1l111l11_opy_(call.excinfo.typename)
            hook_data[bstack1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᇺ")] = bstack1l111l1ll_opy_.bstack1l11l1lll1_opy_(call.excinfo, result)
    return hook_data
def bstack1l111lllll_opy_(test, bstack1l11l111ll_opy_, bstack1l1111ll_opy_, result=None, call=None):
    bstack1l11l111l1_opy_ = bstack1l11l11l11_opy_(test, bstack1l11l111ll_opy_, result, call, bstack1l1111ll_opy_)
    driver = getattr(test, bstack1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᇻ"), None)
    if bstack1l1111ll_opy_ == bstack1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᇼ") and driver:
        bstack1l11l111l1_opy_[bstack1_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᇽ")] = bstack1l111l1ll_opy_.bstack1l11l1l1l1_opy_(driver)
    if bstack1l1111ll_opy_ == bstack1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᇾ"):
        bstack1l1111ll_opy_ = bstack1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᇿ")
    bstack1l11l1111l_opy_ = {
        bstack1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ሀ"): bstack1l1111ll_opy_,
        bstack1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬሁ"): bstack1l11l111l1_opy_
    }
    bstack1l111l1ll_opy_.bstack1l11l1llll_opy_(bstack1l11l1111l_opy_)
def bstack1l111ll1ll_opy_(test, bstack1l11l111ll_opy_, bstack1l1111ll_opy_, result=None, call=None):
    hook_data = bstack1l111l1lll_opy_(test, bstack1l11l111ll_opy_, bstack1l1111ll_opy_, result, call)
    bstack1l11l1111l_opy_ = {
        bstack1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨሂ"): bstack1l1111ll_opy_,
        bstack1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧሃ"): hook_data
    }
    bstack1l111l1ll_opy_.bstack1l11l1llll_opy_(bstack1l11l1111l_opy_)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l111l1ll_opy_.on():
            return
        records = caplog.get_records(bstack1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫሄ"))
        bstack1l11llllll_opy_ = []
        for record in records:
            if record.message == bstack1_opy_ (u"ࠧ࡝ࡰࠪህ"):
                continue
            bstack1l11llllll_opy_.append({
                bstack1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫሆ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1_opy_ (u"ࠩ࡝ࠫሇ"),
                bstack1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩለ"): record.levelname,
                bstack1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬሉ"): record.message,
                bstack1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬሊ"): _1l111lll1l_opy_.get(request.node.nodeid).get(bstack1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫላ"))
            })
        bstack1l111l1ll_opy_.bstack1l1l111l1l_opy_(bstack1l11llllll_opy_)
    except Exception as err:
        print(bstack1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫሌ"), str(err))
def bstack1l111l11ll_opy_(driver_command, response):
    if driver_command == bstack1_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬል"):
        bstack1l111l1ll_opy_.bstack1l1l11111l_opy_({
            bstack1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨሎ"): response[bstack1_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩሏ")],
            bstack1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫሐ"): bstack1l11ll1ll1_opy_
        })
@bstack1l111l1ll_opy_.bstack1l11l1l111_opy_
def bstack1l111l11l1_opy_():
    if bstack1l1lll111l_opy_():
        bstack1l1l1l111l_opy_(bstack1l111l11ll_opy_)
bstack1l111l11l1_opy_()
def bstack1lll1l1l1l_opy_():
    global bstack1111ll111_opy_
    bstack1l111l1ll_opy_.bstack1l11lll111_opy_()
    for driver in bstack1111ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11llll_opy_(self, *args, **kwargs):
    bstack1l1l111ll_opy_ = bstack1111ll1l_opy_(self, *args, **kwargs)
    bstack1l111l1ll_opy_.bstack1ll111l11_opy_(self)
    return bstack1l1l111ll_opy_
def bstack11l111l11_opy_(framework_name):
    global bstack11ll11ll1_opy_
    global bstack1llll1111l_opy_
    bstack11ll11ll1_opy_ = framework_name
    logger.info(bstack1l11ll111_opy_.format(bstack11ll11ll1_opy_.split(bstack1_opy_ (u"ࠬ࠳ࠧሑ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll1111l11_opy_():
            Service.start = bstack1ll1l1l111_opy_
            Service.stop = bstack1l1l1lll1_opy_
            webdriver.Remote.__init__ = bstack1l1l1l111_opy_
            webdriver.Remote.get = bstack11ll1l1ll_opy_
            if not isinstance(os.getenv(bstack1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧሒ")), str):
                return
            WebDriver.close = bstack1lll1ll1ll_opy_
            WebDriver.quit = bstack1lll1lll_opy_
        if not bstack1ll1111l11_opy_() and bstack1l111l1ll_opy_.on():
            webdriver.Remote.__init__ = bstack1l11llll_opy_
        bstack1llll1111l_opy_ = True
    except Exception as e:
        pass
    bstack1l1lllll1_opy_()
    if os.environ.get(bstack1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬሓ")):
        bstack1llll1111l_opy_ = eval(os.environ.get(bstack1_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭ሔ")))
    if not bstack1llll1111l_opy_:
        bstack11111l1ll_opy_(bstack1_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦሕ"), bstack1llllll11_opy_)
    if bstack1l11111l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l1l1ll11_opy_
        except Exception as e:
            logger.error(bstack1l11l1l1_opy_.format(str(e)))
    if bstack1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪሖ") in str(framework_name).lower():
        if not bstack1ll1111l11_opy_():
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
def bstack1lll1lll_opy_(self):
    global bstack11ll11ll1_opy_
    global bstack1l11l1ll_opy_
    global bstack11l11l1ll_opy_
    try:
        if bstack1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫሗ") in bstack11ll11ll1_opy_ and self.session_id != None:
            bstack11l1ll1ll_opy_ = bstack1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬመ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሙ")
            bstack11111llll_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪሚ"), bstack1_opy_ (u"ࠨࠩማ"), bstack11l1ll1ll_opy_, bstack1_opy_ (u"ࠩ࠯ࠤࠬሜ").join(
                threading.current_thread().bstackTestErrorMessages), bstack1_opy_ (u"ࠪࠫም"), bstack1_opy_ (u"ࠫࠬሞ"))
            if self != None:
                self.execute_script(bstack11111llll_opy_)
    except Exception as e:
        logger.debug(bstack1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨሟ") + str(e))
    bstack11l11l1ll_opy_(self)
    self.session_id = None
def bstack1l1l1l111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l11l1ll_opy_
    global bstack1l11l1lll_opy_
    global bstack1l111111l_opy_
    global bstack11ll11ll1_opy_
    global bstack1111ll1l_opy_
    global bstack1111ll111_opy_
    global bstack111111l1l_opy_
    global bstack1ll1l111l_opy_
    CONFIG[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨሠ")] = str(bstack11ll11ll1_opy_) + str(__version__)
    command_executor = bstack1lll1l1111_opy_(bstack111111l1l_opy_)
    logger.debug(bstack1l111ll1_opy_.format(command_executor))
    proxy = bstack111l111l_opy_(CONFIG, proxy)
    bstack11l1ll111_opy_ = 0
    try:
        if bstack1l111111l_opy_ is True:
            bstack11l1ll111_opy_ = int(os.environ.get(bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧሡ")))
    except:
        bstack11l1ll111_opy_ = 0
    bstack1l11ll1ll_opy_ = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll111_opy_)
    logger.debug(bstack1lllll1111_opy_.format(str(bstack1l11ll1ll_opy_)))
    if bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬሢ") in CONFIG and CONFIG[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ሣ")]:
        bstack11ll1l11l_opy_(bstack1l11ll1ll_opy_, bstack1ll1l111l_opy_)
    if desired_capabilities:
        bstack1lll1l1ll_opy_ = bstack1l111l1l_opy_(desired_capabilities)
        bstack1lll1l1ll_opy_[bstack1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪሤ")] = bstack1111llll1_opy_(CONFIG)
        bstack1llll1l11l_opy_ = bstack11ll1l1l_opy_(bstack1lll1l1ll_opy_)
        if bstack1llll1l11l_opy_:
            bstack1l11ll1ll_opy_ = update(bstack1llll1l11l_opy_, bstack1l11ll1ll_opy_)
        desired_capabilities = None
    if options:
        bstack1l1l1111_opy_(options, bstack1l11ll1ll_opy_)
    if not options:
        options = bstack11l111ll_opy_(bstack1l11ll1ll_opy_)
    if proxy and bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫሥ")):
        options.proxy(proxy)
    if options and bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫሦ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll111ll1_opy_() < version.parse(bstack1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬሧ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1l11ll1ll_opy_)
    logger.info(bstack1l1lll1ll_opy_)
    if bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧረ")):
        bstack1111ll1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧሩ")):
        bstack1111ll1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩሪ")):
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
        bstack1llll1llll_opy_ = bstack1_opy_ (u"ࠪࠫራ")
        if bstack1ll111ll1_opy_() >= version.parse(bstack1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬሬ")):
            bstack1llll1llll_opy_ = self.caps.get(bstack1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧር"))
        else:
            bstack1llll1llll_opy_ = self.capabilities.get(bstack1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨሮ"))
        if bstack1llll1llll_opy_:
            if bstack1ll111ll1_opy_() <= version.parse(bstack1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧሯ")):
                self.command_executor._url = bstack1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤሰ") + bstack111111l1l_opy_ + bstack1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨሱ")
            else:
                self.command_executor._url = bstack1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧሲ") + bstack1llll1llll_opy_ + bstack1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧሳ")
            logger.debug(bstack111l11lll_opy_.format(bstack1llll1llll_opy_))
        else:
            logger.debug(bstack11lll1111_opy_.format(bstack1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨሴ")))
    except Exception as e:
        logger.debug(bstack11lll1111_opy_.format(e))
    bstack1l11l1ll_opy_ = self.session_id
    if bstack1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ስ") in bstack11ll11ll1_opy_:
        threading.current_thread().bstack1lll11ll_opy_ = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1l111l1ll_opy_.bstack1ll111l11_opy_(self)
    bstack1111ll111_opy_.append(self)
    if bstack1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪሶ") in CONFIG and bstack1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ሷ") in CONFIG[bstack1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬሸ")][bstack11l1ll111_opy_]:
        bstack1l11l1lll_opy_ = CONFIG[bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ሹ")][bstack11l1ll111_opy_][bstack1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩሺ")]
    logger.debug(bstack1111ll11l_opy_.format(bstack1l11l1ll_opy_))
def bstack11ll1l1ll_opy_(self, url):
    global bstack111l1l11l_opy_
    global CONFIG
    try:
        bstack1llllll1ll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l1l11ll_opy_.format(str(err)))
    try:
        bstack111l1l11l_opy_(self, url)
    except Exception as e:
        try:
            bstack111lll111_opy_ = str(e)
            if any(err_msg in bstack111lll111_opy_ for err_msg in bstack11ll1ll11_opy_):
                bstack1llllll1ll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l1l11ll_opy_.format(str(err)))
        raise e
def bstack1l1l11l1l_opy_(item, when):
    global bstack1lll1ll1l_opy_
    try:
        bstack1lll1ll1l_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1lll1l_opy_(item, call, rep):
    global bstack11ll11l1_opy_
    global bstack1111ll111_opy_
    name = bstack1_opy_ (u"ࠬ࠭ሻ")
    try:
        if rep.when == bstack1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫሼ"):
            bstack1l11l1ll_opy_ = threading.current_thread().bstack1lll11ll_opy_
            bstack1l111l1l11_opy_ = item.config.getoption(bstack1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩሽ"))
            try:
                if (str(bstack1l111l1l11_opy_).lower() != bstack1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ሾ")):
                    name = str(rep.nodeid)
                    bstack11111llll_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪሿ"), name, bstack1_opy_ (u"ࠪࠫቀ"), bstack1_opy_ (u"ࠫࠬቁ"), bstack1_opy_ (u"ࠬ࠭ቂ"), bstack1_opy_ (u"࠭ࠧቃ"))
                    for driver in bstack1111ll111_opy_:
                        if bstack1l11l1ll_opy_ == driver.session_id:
                            driver.execute_script(bstack11111llll_opy_)
            except Exception as e:
                logger.debug(bstack1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧቄ").format(str(e)))
            try:
                status = bstack1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨቅ") if rep.outcome.lower() == bstack1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩቆ") else bstack1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪቇ")
                reason = bstack1_opy_ (u"ࠫࠬቈ")
                if (reason != bstack1_opy_ (u"ࠧࠨ቉")):
                    try:
                        if (threading.current_thread().bstackTestErrorMessages == None):
                            threading.current_thread().bstackTestErrorMessages = []
                    except Exception as e:
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(str(reason))
                if status == bstack1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ቊ"):
                    reason = rep.longrepr.reprcrash.message
                    if (not threading.current_thread().bstackTestErrorMessages):
                        threading.current_thread().bstackTestErrorMessages = []
                    threading.current_thread().bstackTestErrorMessages.append(reason)
                level = bstack1_opy_ (u"ࠧࡪࡰࡩࡳࠬቋ") if status == bstack1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨቌ") else bstack1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨቍ")
                data = name + bstack1_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ቎") if status == bstack1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫ቏") else name + bstack1_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨቐ") + reason
                bstack1111ll1l1_opy_ = bstack1lllll1ll_opy_(bstack1_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨቑ"), bstack1_opy_ (u"ࠧࠨቒ"), bstack1_opy_ (u"ࠨࠩቓ"), bstack1_opy_ (u"ࠩࠪቔ"), level, data)
                for driver in bstack1111ll111_opy_:
                    if bstack1l11l1ll_opy_ == driver.session_id:
                        driver.execute_script(bstack1111ll1l1_opy_)
            except Exception as e:
                logger.debug(bstack1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧቕ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨቖ").format(str(e)))
    bstack11ll11l1_opy_(item, call, rep)
notset = Notset()
def bstack111ll1lll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1lllll11l1_opy_
    if str(name).lower() == bstack1_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬ቗"):
        return bstack1_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧቘ")
    else:
        return bstack1lllll11l1_opy_(self, name, default, skip)
def bstack1l1l1ll11_opy_(self):
    global CONFIG
    global bstack11l11l11l_opy_
    try:
        proxy = bstack1lll11lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ቙")):
                proxies = bstack1lll1lll1l_opy_(proxy, bstack1lll1l1111_opy_())
                if len(proxies) > 0:
                    protocol, bstack111l1ll11_opy_ = proxies.popitem()
                    if bstack1_opy_ (u"ࠣ࠼࠲࠳ࠧቚ") in bstack111l1ll11_opy_:
                        return bstack111l1ll11_opy_
                    else:
                        return bstack1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥቛ") + bstack111l1ll11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢቜ").format(str(e)))
    return bstack11l11l11l_opy_(self)
def bstack1l11111l_opy_():
    return bstack1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧቝ") in CONFIG or bstack1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ቞") in CONFIG and bstack1ll111ll1_opy_() >= version.parse(
        bstack1l11ll11l_opy_)
def bstack1ll1ll1l1_opy_(self,
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
    global bstack1l11l1lll_opy_
    global bstack1l111111l_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstack1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ቟")] = str(bstack11ll11ll1_opy_) + str(__version__)
    bstack11l1ll111_opy_ = 0
    try:
        if bstack1l111111l_opy_ is True:
            bstack11l1ll111_opy_ = int(os.environ.get(bstack1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧበ")))
    except:
        bstack11l1ll111_opy_ = 0
    CONFIG[bstack1_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢቡ")] = True
    bstack1l11ll1ll_opy_ = bstack11ll1l1l_opy_(CONFIG, bstack11l1ll111_opy_)
    logger.debug(bstack1lllll1111_opy_.format(str(bstack1l11ll1ll_opy_)))
    if CONFIG[bstack1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ቢ")]:
        bstack11ll1l11l_opy_(bstack1l11ll1ll_opy_, bstack1ll1l111l_opy_)
    if bstack1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ባ") in CONFIG and bstack1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩቤ") in CONFIG[bstack1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨብ")][bstack11l1ll111_opy_]:
        bstack1l11l1lll_opy_ = CONFIG[bstack1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩቦ")][bstack11l1ll111_opy_][bstack1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬቧ")]
    import urllib
    import json
    bstack1l1llll1_opy_ = bstack1_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪቨ") + urllib.parse.quote(json.dumps(bstack1l11ll1ll_opy_))
    browser = self.connect(bstack1l1llll1_opy_)
    return browser
def bstack1l1lllll1_opy_():
    global bstack1llll1111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1ll1l1_opy_
        bstack1llll1111l_opy_ = True
    except Exception as e:
        pass
def bstack1l111ll111_opy_():
    global CONFIG
    global bstack11111111_opy_
    global bstack111111l1l_opy_
    global bstack1ll1l111l_opy_
    global bstack1l111111l_opy_
    CONFIG = json.loads(os.environ.get(bstack1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨቩ")))
    bstack11111111_opy_ = eval(os.environ.get(bstack1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫቪ")))
    bstack111111l1l_opy_ = os.environ.get(bstack1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫቫ"))
    bstack11ll1lll_opy_(CONFIG, bstack11111111_opy_)
    bstack1l1l11ll1_opy_()
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
    if bstack1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨቬ") in CONFIG or bstack1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪቭ") in CONFIG:
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
        logger.debug(bstack1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨቮ"))
    bstack1ll1l111l_opy_ = CONFIG.get(bstack1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬቯ"), {}).get(bstack1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫተ"))
    bstack1l111111l_opy_ = True
    bstack11l111l11_opy_(bstack111l1l1l1_opy_)
if (bstack1ll11111l1_opy_()):
    bstack1l111ll111_opy_()