#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from time import sleep

import pytest

from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from test.functional.test_helper import wait_for_element

from .helper.test_helper import BaseTestCase, is_ci


class TestMultiAction(BaseTestCase):
    def test_parallel_actions(self) -> None:
        self._move_to_splitting_touches_accros_views()

        els = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.ListView')
        a1 = TouchAction()
        a1.press(els[0]).move_to(x=10, y=0).move_to(x=10, y=-75).move_to(x=10, y=-600).release()

        a2 = TouchAction()
        a2.press(els[1]).move_to(x=10, y=10).move_to(x=10, y=-300).move_to(x=10, y=-600).release()

        ma = MultiAction(self.driver, els[0])
        ma.add(a1, a2)
        ma.perform()

    def test_actions_with_waits(self) -> None:
        self._move_to_splitting_touches_accros_views()

        els = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.ListView')
        a1 = TouchAction()
        a1.press(els[0]).move_to(x=10, y=0).move_to(x=10, y=-75).wait(1000).move_to(x=10, y=-600).release()

        a2 = TouchAction()
        a2.press(els[1]).move_to(x=10, y=10).move_to(x=10, y=-300).wait(500).move_to(x=10, y=-600).release()

        ma = MultiAction(self.driver, els[0])
        ma.add(a1, a2)
        ma.perform()

    def _move_to_splitting_touches_accros_views(self) -> None:
        el1 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Content')
        el2 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Animation')
        self.driver.scroll(el1, el2)

        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Views')
        action = TouchAction(self.driver)
        action.tap(el).perform()

        # simulate a swipe/scroll
        el = wait_for_element(self.driver, AppiumBy.ACCESSIBILITY_ID, 'Expandable Lists')
        action.press(el).move_to(x=100, y=-1000).release().perform()
        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Layouts')
        action.press(el).move_to(x=100, y=-1000).release().perform()

        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Splitting Touches across Views')
        action.tap(el).perform()

        wait_for_element(self.driver, AppiumBy.ID, 'io.appium.android.apis:id/list1')

    @pytest.mark.skipif(condition=is_ci(), reason='Skip since the test must be watched to check if it works')
    def test_driver_multi_tap(self) -> None:
        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Graphics')
        action = TouchAction(self.driver)
        action.tap(el).perform()

        wait_for_element(self.driver, AppiumBy.CLASS_NAME, 'android.widget.TextView')
        els = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
        self.driver.scroll(els[len(els) - 1], els[0])

        els = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
        if els[len(els) - 1].get_attribute('name') != 'Xfermodes':
            self.driver.scroll(els[len(els) - 1], els[0])

        el = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Touch Paint')
        action.tap(el).perform()

        positions = [(100, 200), (100, 400)]

        # makes two dots in the paint program
        # THE TEST MUST BE WATCHED TO CHECK IF IT WORKS
        self.driver.tap(positions)
        sleep(10)
