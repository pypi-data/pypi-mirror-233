from tejapi.connection import Connection
from tejapi.util import Util
from tejapi.message import Message
import pandas as pd
from io import BytesIO
import warnings
import copy

def fastget(datatable_code, **options):
    
    path = 'datatables/%s.parquet' % datatable_code
    
    if 'paginate' in options.keys():
        paginate = options.pop('paginate')
        options["opts.full"]=True
    else:
        paginate = None
        
    if 'opts_filter' in options.keys():
        filters = options.pop('opts_filter')
        options.update(filters)
        
    if 'chinese_column_name' in options.keys():
        chinese_column_name = options.pop('chinese_column_name')
    else:
        chinese_column_name = False
        
        
    params ={}
    params["params"]=options

    updated_options = Util.convert_options(**params)
    
    r = Connection.request('post', path, **updated_options)

    data =  pd.read_parquet(BytesIO(r.content) ,engine="fastparquet")    
        
    if chinese_column_name:
        cname = convert_cname(path, updated_options)
        data.rename(columns=cname,inplace=True)
    else:
        colname={}
        for v in list(data.columns):
            colname[v]=v.replace("TEJAPI_","")
            
        data.rename(columns=colname,inplace=True)

    if paginate is not True:
        warnings.warn(Message.WARN_PAGE_LIMIT_EXCEEDED)
        
    return data


def convert_cname(path, options):
    cname_options = copy.deepcopy(options)
    cname_options["params"]["opts.cname"]=True
    r = Connection.request('post', path, **cname_options)
    metadata = r.json()
    
    cname={}
    for v in list(metadata["datatable"]["columns"]):
        cname["TEJAPI_"+v["name"]]=v["cname"]
        
    return cname