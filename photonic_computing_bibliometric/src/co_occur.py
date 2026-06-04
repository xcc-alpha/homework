import pandas as pd
def build_co(df,topn):
    kw_ser=df["关键词"].str.split("; ").dropna()
    top_list=kw_ser.explode().value_counts().head(topn).index.tolist()
    mat=pd.DataFrame(0,index=top_list,columns=top_list)
    for item in kw_ser:
        kw=[k for k in item if k in top_list]
        for i in range(len(kw)):
            for j in range(i+1,len(kw)):
                mat.loc[kw[i],kw[j]]+=1
                mat.loc[kw[j],kw[i]]+=1
    return mat,top_list
