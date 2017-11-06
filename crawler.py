import time
import re

from selenium.common import exceptions

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mlogger import med_logger

claps_reg = re.compile( r'(\d+) claps from (\d+)' )

def get_data_from_url( driver, medium_url ):
    try:
        t_0 = time.time()
        
        # bottleneck due to network IO
        print( 'getting to page' )
        driver.get( medium_url )

        footer = driver.find_element_by_tag_name('footer')
        footer_elem = driver.find_element_by_class_name('js-postActionsFooter')
        driver.execute_script("arguments[0].scrollIntoView()", footer_elem)

        time.sleep( 0.2 )

        footer_buttons = footer_elem.find_elements_by_tag_name('button')
        message_count = footer_buttons[4].text

        # bottleneck due to network IO
        clap_count = footer_buttons[2]
        clap_count.click()

        clap_title = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'overlay-title'))
            )

        # clap_title = driver.find_element_by_class_name('overlay-title')

        tags = driver.find_element_by_class_name('tags--postTags').find_elements_by_tag_name('a')
        tags = [ i.get_attribute('innerHTML') for i in tags ]
        tags = '|'.join( tags )

        clap_text = clap_title.text
        match_obj = claps_reg.search(clap_text)

        driver.find_element_by_class_name('button--close').click()
        
        read_time = driver.find_element_by_class_name( 'readingTime' ).get_attribute('title').split( ' ' )[0]

        next_links = driver.find_elements_by_class_name( 'u-padding8' )
        next_links = [ i.find_element_by_tag_name( 'a' ).get_attribute( 'href' ) for i in next_links ]
        next_links = [ i.split('?')[0] for i in next_links ]

        s = 'takes : {} s'.format( time.time() - t_0 )

        print( s )
        med_logger.debug( s )

        return [ medium_url, read_time, match_obj.group( 1 ), match_obj.group( 2 ), tags ], next_links

    except exceptions.NoSuchElementException:
        print( 'NoSuchElementException, skipping' )
    
    except exceptions.TimeoutException:
        # when the Internet is slow
        print( 'TimeoutException, skipping' )
    
    except exceptions.StaleElementReferenceException:
        # reason unknown
        print( 'StaleElementReferenceException, skipping' )

    except OSError:
        # Medium refuse to connect
        print( 'OSError, restarting driver...' )
        return 'OSError', []
    
    except Exception as err:
        med_logger.error( '{}\n{}\n'.format( type(err), err ) )

    # reach this line due to error
    return None, []
