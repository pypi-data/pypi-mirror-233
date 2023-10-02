from cdxg.logging import log
from selenium.common import StaleElementReferenceException
from wfs.utils.common import validate_order
from wfs.utils.assertions import Assertion
# from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import traceback, time, re


def get_type_key(lpage, item, keyitem, gready):
    try:
        if item == 'type':
            lpage.locators_ready(greadyx=gready).clear()
            lpage.locators_ready(greadyx=gready).send_keys(keyitem)
            log.info('Enter data as : ' + str(keyitem))
            return 'Enter data as : ' + str(keyitem)
    except Exception as e:
        return 'Error ' + str(e)


def get_click(lpage, item, gready):
    if item == 'click':
        try:
            # print(lpage.locators_ready())
            lpage.locators_ready(greadyx=gready).click()
            log.info('1. Button or Clickable item get Clicked')
            return 'Button1 clicked'
        except Exception as e:
            getclicked = lpage.clickable_element(gready)
            if getclicked == 'YY':
                log.info('2. Button or Clickable item get Clicked')
                return 'Button2 clicked'
            else:
                return 'Error ' + str(e)


def get_text(lpage, item, felement, aresults, case, testcase, exresults, stepline, gitems, gready,
             testitem, ptname):
    # print(type(aresults))
    # print(aresults)
    try:
        gtt = None
        lref = 'N'
        gettxt = []
        if item == 'text':
            timeout_start = time.time()
            timeout = 2 * 5
            progress_net = None
            while not progress_net:
                delta = time.time() - timeout_start
                if 'Frame_' in gitems:
                    getnavg = lpage.element_in_frames()
                    # print(getnavg)
                else:
                    getnavg = lpage.locators_ready(greadyx=gready)
                if testitem == '***':
                    gttext = aresults
                else:
                    gttext = testitem
                if felement == 'S':
                    if getnavg.is_displayed():
                        gtt = lpage.locators_ready(greadyx=gready, textn=gttext)
                        progress_net = 'Done'
                        # gtt = getnavg.text
                    lref = 'Y'
                else:
                    # for xnavigation in getnavg:
                    for xnavigation in range(0, len(getnavg)):
                        try:
                            if getnavg[xnavigation].is_displayed():
                                # print(getnavg[xnavigation].text, gttext)
                                if getnavg[xnavigation].text == gttext:
                                    gtt = getnavg[xnavigation].text
                                    lref = 'Y'
                                    progress_net = 'Done'
                                    break
                                else:
                                    gettxt.append(getnavg[xnavigation].text)
                                    gtt = gettxt
                                    lref = 'YY'
                                    xnavigation = xnavigation + 1
                                    # print(xnavigation)
                                    if ptname is None:
                                        if xnavigation >= len(getnavg):
                                            progress_net = 'Done'
                                            break
                        except StaleElementReferenceException:
                            progress_net = None
                if progress_net == 'Done':
                    progress_net = 'Success'
                if delta >= timeout:
                    break

            if 'Frame_' in gitems:
                lpage.back_to_default()

            if lref == 'Y':
                log.info('Given Text : ' + str(gtt) + ' displayed on Page')
                if testitem == '***':
                    Assertion().assert_equals_results(case=case, testcase=testcase, gtext=gtt,
                                                      aresults=aresults.rstrip(),
                                                      exresults=exresults, stepline=stepline, gtitems=testitem)
                    return 'YES'
                else:
                    return 'Given Text  ' + str(gtt) + ' displayed on Page'
            else:
                log.info('List of Texts : ' + str(gtt) + ' displayed')
                if type(aresults) is not list:
                    if ',' in aresults:
                        aresults = aresults.split(',')
                        is_valid = validate_order(order_list=gtt, expected_order=aresults)
                        if is_valid:
                            gtt = aresults
                    aresults = [string.rstrip() for string in aresults]
                else:
                    aresults = [string.rstrip() for string in aresults]

                gtt = sorted(str(item) for item in gtt)
                aresults = sorted(str(item) for item in aresults)

            if testitem == '***':
                if gtt == aresults:
                    print('List are Equals....')
                    Assertion().assert_equals_results(case=case, testcase=testcase, gtext=gtt,
                                                      aresults=aresults,
                                                      exresults=exresults, stepline=stepline, gtitems=testitem)
                else:
                    print('List are not Equals....')
                    Assertion().assert_in_results(case=case, testcase=testcase, gtext=gtt, aresults=aresults,
                                                  exresults=exresults, stepline=stepline, gtitems=testitem)
                return 'YES'
            else:
                if ptname:
                    gtt = set(gtt)
                return 'List of Texts  ' + str(gtt) + ' displayed'
    except Exception as e:
        print(traceback.print_exc())
        return 'Error :' + str(e)


def get_link_text(lpage, item, testitem, felement, gready):
    try:
        if item == 'link_text':
            timeout_start = time.time()
            timeout = 2 * 5
            progress_net = None
            while not progress_net:
                delta = time.time() - timeout_start
                getnavigation = lpage.locators_ready(greadyx=gready)
                # print(getnavigation)
                # gttext = gtitems[6]
                if felement == 'S':
                    if getnavigation.is_displayed():
                        if getnavigation.text == testitem:
                            getnavigation.click()
                            progress_net = 'Done'
                            log.info('1.Link_text or Clickable item get Clicked')
                            time.sleep(1)
                else:
                    for xnavigation in getnavigation:
                        if xnavigation.is_displayed():
                            log.info(xnavigation.text)
                            if xnavigation.text == testitem:
                                xnavigation.click()
                                log.info('2.Link_text or Clickable item get Clicked')
                                time.sleep(1)
                                progress_net = 'Done'
                                break
                if progress_net == 'Done':
                    progress_net = 'Success'
                if delta >= timeout:
                    break
            return 'Link Item get Clicked'
    except Exception as e:
        return 'Error ' + str(e)


def get_page_title(lpage, item, case, testcase, aresults, exresults, stepline, gready, gtitems):
    global rTitle
    yx = 'NO'
    try:
        if item == 'title':
            rTitle = lpage.get_title
            yx = 'YES'
        if item == 'row':
            gdx = get_ordering_table(lpage, item, gready)
            rTitle = int(gdx) - 1
            if type(aresults) == list:
                aresults = [int(num) for num in aresults]
            yx = 'YES'

        if item in ['asc', 'desc']:
            aresults, rTitle = get_ordering_table(lpage, item, gready)
            yx = 'YES'

        if yx == 'YES':
            Assertion().assert_equals_results(case, testcase, rTitle, aresults, exresults, stepline, gtitems)
            return 'YES'
    except Exception as e:
        print(traceback.print_exc())
        return 'Error ' + str(e)


def get_select_item(lpage, item, keyitem, gready):
    try:
        if item == 'option':
            opts = lpage.locators_ready(greadyx=gready)
            matched = False
            for opt in opts:
                if keyitem == opt.text:
                    opt.click()
                    matched = True
                    break
            if not matched:
                # raise NoSuchElementException("Could not locate element with visible text: %s" % keyitem)
                return 'Error : ' + str(keyitem) + ' Not Match'
            else:
                return str(keyitem) + ' is Matched'
    except Exception as e:
        return 'Error ' + str(e)


def _get_longest_token(value: str) -> str:
    items = value.split(" ")
    longest = ""
    for item in items:
        if len(item) > len(longest):
            longest = item
    return longest


def get_clickable_selectable(lpage, item, gready):
    try:
        getElement = lpage.gethidden(gready)
        if item == 'click':
            getElement.click()
            return 'Item Clicked'
    except Exception as e:
        return 'Error ' + str(e)


def get_keys_press(lpage, gready, keyitem='ENTER'):
    try:
        element = lpage.locators_ready(greadyx=gready)
        actions = lpage.get_action_chains()
        if keyitem == 'ENTER':
            actions.send_keys_to_element(element, Keys.ENTER)
        actions.perform()
        return 'Key Action Performed ->'+str(keyitem)
    except Exception as e:
        return 'Error  ' + str(e)


def long_press(lpage, gready):
    element = lpage.locators_ready(greadyx=gready)
    actions = lpage.get_touch_actions()
    actions.long_press(element).perform()


def mouse_actions(lpage, item, gready):
    if item == 'hover':
        element = lpage.locators_ready(greadyx=gready)
        actions = lpage.get_action_chains()
        actions.move_to_element(element).click().perform()
        return 'Mouse over to element -> clicked'
    else:
        return scrollpage(lpage, item, gready)


def scrollpage(lpage, item, gready):
    if item == 'scroll':
        element = lpage.locators_ready(greadyx=gready)
        try:
            actions = lpage.get_action_chains()
            # actions.scroll_to_element(element)
            lpage.getscrolled(elementx=element)
            return 'Scrolled the element'
        except Exception as e:
            return 'Error ' + str(e)


def get_common(lpage, item, gready, attriname=None):
    try:
        if item in ['idata']:
            element = lpage.locators_ready(greadyx=gready)
            get_element = lpage.get_inject_data(element, attriname)
            if element:
                return 'Element available'
        else:
            return get_ordering_table(lpage, item, gready)
    except Exception as e:
        return 'Error  ' + str(e)


def get_ordering_table(lpage, item, gready, arst=None):
    # Get all the rows of the table
    global expected_order
    if item == 'row':
        locator_identity, element_identity, action_item, fetchlements = 'tag', 'tr', 'page', 'M'
        gready = locator_identity, element_identity, action_item, fetchlements
        rows = lpage.locators_ready(greadyx=gready)
        return len(rows)

    if item in ['asc', 'desc']:
        extracted_order = []
        cells = lpage.locators_ready(gready)
        extracted_order = [cell.text for cell in cells]
        if item == 'asc':
            expected_order = sorted(extracted_order, key=lambda x: x.lower())
        if item == 'desc':
            expected_order = sorted(extracted_order, key=lambda x: x.lower(), reverse=True)
        return expected_order, extracted_order

    if item == 'text':
        # extracted_order = []
        cells = lpage.locators_ready(gready)  # row.find_elements(By.TAG_NAME, "td")
        extracted_order = [cell.text for cell in cells]
        abc = extracted_order
        getrxt = str(arst).split('>>')[1]
        def_value = getrxt.split(',')  # Example list with additional strings
        is_valid = all(any(element == def_val for def_val in def_value) for element in abc)
        if is_valid:
            return extracted_order
        else:
            return 'No Extracted Data Not Matched'
