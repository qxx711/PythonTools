import os
import pyodbc
import pandas as pd
import numpy as np

#将整合的csv文件转成excel格式

path = r"D:\yanjiusheng\SA-TD\Multi-Programming-Language Commits in OSS\03journal\data\reopenIssueEXCEL"#整合后的csv文件路径
output_path = r"D:\yanjiusheng\SA-TD\Multi-Programming-Language Commits in OSS\03journal\data\excel"#excel文件输出路径
filelist = os.listdir(path)

for file in filelist:
    if os.path.isfile(path+'\\'+file):
        print(path+'\\'+file)
        df = pd.read_csv(path+'\\'+file)
        # print(df.shape)
        df['Created'] = pd.to_datetime(df['Created'], errors='coerce')
        df['Last Viewed'] = pd.to_datetime(df['Last Viewed'], errors='coerce')
        df['Updated'] = pd.to_datetime(df['Updated'], errors='coerce')
        df['Resolved'] = pd.to_datetime(df['Resolved'], errors='coerce')
        print(df.shape)
        with pd.ExcelWriter(output_path+'\\'+file.split('.')[0]+'.xlsx',datetime_format='YYYY-MM-DD HH:MM:SS',options={'strings_to_urls': False}) as writer:
            df.to_excel(writer, index=False)
print("success!")