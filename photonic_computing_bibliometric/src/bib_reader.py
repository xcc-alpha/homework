import os,pandas as pd
def read_wos(path):
    res=[]
    for f in os.listdir(path):
        if f.endswith(".txt"):
            rec={}
            with open(os.path.join(path,f),"r",encoding="utf-8",errors="ignore") as fp:
                for line in fp.readlines():
                    line=line.strip()
                    if len(line)<3:continue
                    fd=line[:2]
                    val=line[3:].strip()
                    if fd=="PT":
                        if rec:res.append(rec)
                        rec={}
                    if fd in ["TI","AU","SO","DE","PY","C1"]:
                        rec[fd]=rec.get(fd,"")+("; "+val if fd in rec else val)
            if rec:res.append(rec)
    df=pd.DataFrame(res)
    df.columns=["标题","作者","期刊","关键词","年份","机构"]
    return df
