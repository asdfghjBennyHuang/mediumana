from selenium import webdriver

import pandas as pd
import crawler
import collections
import random
import os
import sys
import time
import pickle

from mlogger import med_logger

exit_flag = False
objective_number = 3000

df = pd.DataFrame( columns=['url', 'length', 'claps', 'claps_people', 'tags'] )

searched_links = set()

if not sys.argv[1]:
    print( 'please provide the number of starting point' )
    sys.exit(1)

if sys.argv[1] == 'load':
    file_name = 'queue_pages_{}.pic'.format( sys.argv[2] )

    with open( file_name, 'rb' ) as fr:
        link_queue = pickle.load( fr )

else:
    link_queue = collections.deque()

    start_url = [ "https://thebolditalic.com/thank-you-for-your-undivided-attention-ad39d713dc4a" ]

    med_logger.info( 'starting points : {}'.format( '\n'.join( start_url ) ) )

    link_queue.append( start_url[ int( sys.argv[1] ) ] )

def main():
    global exit_flag, link_queue, searched_links, df

    counter = 0

    # driver = webdriver.Chrome( 'C:/Program Files (x86)/Google/chromedriver.exe' )
    driver = webdriver.PhantomJS( 'phantomjs-2.1.1/bin/phantomjs.exe', service_args=['--load-images=no'] )
    # driver = webdriver.PhantomJS( 'phantomjs-2.1.1/bin/phantomjs.exe', service_args=['--load-images=no'] )

    try:
        while True:
            if link_queue:
                medium_url = link_queue.popleft()
            else:
                # running out of links
                the_s = 'running out of links'
                print( the_s )
                med_logger.info( the_s )

                exit_flag = True

                break

            try:
                page_data, next_links = crawler.get_data_from_url( driver, medium_url )
            except Exception as err:
                the_s = 'error calling get_data_from_url : {}'.format( err )
                print( the_s )
                med_logger.info( the_s )

            if isinstance( page_data, list ):

                # only add to record when succeed
                searched_links.add( medium_url )

                counter += 1

                inx = df.count()[0]
                df.loc[ inx ] = page_data

                for l in next_links:
                    if l not in searched_links:
                        link_queue.append( l )
            elif isinstance( page_data, str ):
                
                if page_data == 'OSError':
                    break

            else:
                pass

            print( len( searched_links ) )

            if counter >= 60:
                break

            if len( searched_links ) >= objective_number:
                exit_flag = True

                break

    except KeyboardInterrupt:
        pass

    driver.quit()


if __name__ == '__main__':

    while True:
        try:
            main()
        except Exception as err:
            med_logger.error( 'Error in the main loop :\n{}\n{}\n'.format( type(err), err ) )

        if exit_flag:
            file_name = 'pages_{}'.format( int( random.uniform( 0, 1000000 ) ) )
            df.to_csv( file_name + '.csv', index = False )

            with open( 'queue_{}.pic'.format( file_name ), 'wb' ) as fw:
                pickle.dump( link_queue, fw )

            # here we should also store searched_set
            # TODO

            break

