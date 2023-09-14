import pycurl

file_name = 'model/client.h5'
file_src = 'http://140.124.182.1:6000/image/client.h5'

with open(file_name, 'wb') as f:
    cl = pycurl.Curl()
    cl.setopt(cl.URL, file_src)
    cl.setopt(cl.WRITEDATA, f)
    cl.perform()
    cl.close()
