import time
from make_html import *

userRequest = str(raw_input("Album and Artist: "))
st = time.time()
print make_html(userRequest)
print 'That took %.2f seconds' % (time.time() - st)
