import os
import pyodbc
import pandas as pd
import numpy as np
import csv
import re

'''
# 删除代码行
def deleteCode(s):
    str1= '{code'
    #如果存在代码行
    if(str1 in s):
      lenth1 = len(s)
      lenth2 = len(str1)
      resultstr= ' '
      indexstr1 = []
      codestr = []
      i = 0
      while str1 in s[i:]:
          indextmp = s.index(str1, i, lenth1)
          indexstr1.append(indextmp)
          i = (indextmp + lenth2)
      for j in range(0,len((indexstr1)),2):
          x1 = indexstr1[j]
          x2 = indexstr1[j+1]
          codestr.append(s[x1:x2+6])
      for k in range(0,len(codestr)):
          resultstr = s.replace(codestr[k] , "")
          s=resultstr
      return resultstr
    else:
        return s
'''
def deleteCode(s):
    str1 = '{code'
    if (str1 in s):
        s=re.sub('\s+', " ", s)
        result = re.sub(r'{code(.+?)code}', "", s)
        return result
    else:
        return  s
    #判断两列是否相等
def function(m, n):
    if m == n:
        return int(1)
    else:
        return int(0)

if __name__ == '__main__':

 # 拼接所有csv文件
 path = r"D:\yanjiusheng\SA-TD\Multi-Programming-Language Commits in OSS\03journal\data\reopenIssueCSV"  # 原始文件路径
 output_path = r"D:\yanjiusheng\SA-TD\Multi-Programming-Language Commits in OSS\03journal\data\reopenIssueEXCEL"  # 输出路径

 dirs = os.listdir(path)
 for dir in dirs:
    if os.path.isdir("%s\\%s" % (path, dir)):
        projectpath = "%s\\%s" % (path, dir)
        filelist = os.listdir(projectpath)
        df = pd.read_csv(path + '\\' + dir + '\\' + filelist[0], low_memory=False)
        dfComment = df[df.columns[pd.Series(df.columns).str.startswith('Comment')]]

        df['DescriptionSize'] = 0
        df['CommentNum'] = 0
        df['CommentSize'] = 0
        df['CommentrNo'] = 0

        #描述大小
        df['DescriptionSize'] = df['Description'].str.len()

        #评论数
        df['CommentNum'] = dfComment.count(axis=1)

        dfComment.fillna('', inplace=True)
        dfComment = dfComment.astype(str)
        dfCommentr = pd.DataFrame(data=None , columns=range(0,dfComment.shape[1]),index=range(0,dfComment.shape[0]))
        #评论字符数
        dfComment = dfComment.applymap(lambda x: deleteCode(x))
        for t in range(0 , dfComment.shape[1]):
            dfs = dfComment.iloc[:, t]
            df['CommentSize'] = df['CommentSize'] + dfs.str.len()
        #评论人员个数
            dfCommentr.iloc[:, t] = dfs.str.extract(';(.+?);')
        dfCommentrStack = pd.DataFrame(dfCommentr.values.T, index=dfCommentr.columns, columns=dfCommentr.index)
        for k in range(0,dfCommentrStack.shape[1]):
            df['CommentrNo'][k] = len(dfCommentrStack.iloc[:, k].unique())-1
        df['DescriptionSize'] = df['DescriptionSize'].astype(str)
        df['CommentNum'] = df['CommentNum'].astype(str)
        df['CommentSize'] = df['CommentSize'].astype(str)
        df['CommentrNo'] = df['CommentrNo'].astype(str)
        df = df[['Project name', 'Issue key', 'Summary', 'Issue Type', 'Status', 'Priority', 'Resolution', 'Assignee',
                 'Reporter', 'Creator', 'Created', 'Last Viewed', 'Updated', 'Resolved', 'DescriptionSize', 'CommentNum','CommentSize','CommentrNo']]
        df.to_csv(output_path + '\\' + dir + '_all.csv', encoding="utf_8_sig", index=False)
        print(path + '\\' + dir + '\\' + filelist[0])
        for i in range(1, len(filelist)):
            if os.path.isfile("%s\\%s\\%s" % (path, dir, filelist[i])):
                df = pd.read_csv(path + '\\' + dir + '\\' + filelist[i], low_memory=False)
                dfComment = df[df.columns[pd.Series(df.columns).str.startswith('Comment')]]
                df['DescriptionSize'] = 0
                df['CommentNum'] = 0
                df['CommentSize'] = 0
                df['CommentrNo'] = 0

                # 描述大小
                df['DescriptionSize'] = df['Description'].str.len()

                # 评论数
                df['CommentNum'] = dfComment.count(axis=1)

                dfComment.fillna('', inplace=True)
                dfComment = dfComment.astype(str)
                dfCommentr = pd.DataFrame(data=None, columns=range(0, dfComment.shape[1]),
                                          index=range(0, dfComment.shape[0]))
                # 评论字符数
                dfComment = dfComment.applymap(lambda x: deleteCode(x))
                for t in range(0, dfComment.shape[1]):
                    dfs = dfComment.iloc[:, t]
                    df['CommentSize'] = df['CommentSize'] + dfs.str.len()
                    # 评论人员个数
                    dfCommentr.iloc[:, t] = dfs.str.extract(';(.+?);')
                dfCommentrStack = pd.DataFrame(dfCommentr.values.T, index=dfCommentr.columns, columns=dfCommentr.index)
                for k in range(0, dfCommentrStack.shape[1]):
                    df['CommentrNo'][k] = len(dfCommentrStack.iloc[:, k].unique()) - 1
                df['DescriptionSize'] = df['DescriptionSize'].astype(str)
                df['CommentNum'] = df['CommentNum'].astype(str)
                df['CommentSize'] = df['CommentSize'].astype(str)
                df['CommentrNo'] = df['CommentrNo'].astype(str)

                df = df[['Project name', 'Issue key', 'Summary', 'Issue Type', 'Status', 'Priority', 'Resolution',
                         'Assignee',
                         'Reporter', 'Creator', 'Created', 'Last Viewed', 'Updated', 'Resolved', 'DescriptionSize',
                         'CommentNum', 'CommentSize', 'CommentrNo']]
            print(path + '\\' + dir + '\\' + filelist[i])
            df.to_csv(output_path + '\\' + dir + '_all.csv', encoding="utf_8_sig", index=False, header=False,
                          mode='a+')

 print("success!")