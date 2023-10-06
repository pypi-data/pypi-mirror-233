import numpy as np
from sklearn.feature_extraction.text import CountVectorizer as cv
from sklearn.metrics.pairwise import cosine_similarity

"""
    This is a very required or nessasary module use in our Advance Personal AI serise: https://youtube.com/playlist?list=PLeoHstZu_JQX66udUtj_XyqH-RMutIv5x&si=d_xSpnq1Iwsb2Kyb
    This module also help in figure out  the most similar text in the given dataset with user given input....
    How to used the this library ?
    Here is a demo:

    >>> from NRandom import FSCosine
    >>> Data=[["What is your name","Your name"],[Your favroite color,What is your fav color]] #Define your data to find user input text similarity.
    >>> # Make sure your dataset must be in 2D array. 
    >>> Text=input("Enter text >>")
    >>> Similar=FSCosine()
    >>> Similar_Text=Similar.Find_similarity(Data,Text)
    >>> print(Similar_Text)
"""
class FSCosine():
    def __init__(self) -> None:
        self.lent=300
    def _preprocess(self,data,text):
        self.New_Data=[]
        for idx,vlu in enumerate(data):
            if type(vlu)==list:
                for substring in vlu:
                    self.New_Data.append((idx,substring))
            else:
                self.New_Data.append((idx,vlu))
        self.New_Data.append((self.New_Data[-1][0]+1,text))
        self.New_Data=np.array(self.New_Data)
    
    def _ToVector(self):
        self.OnlyTextData=self.New_Data[:,1]
        c=cv(max_features=self.lent)
        vactors=c.fit_transform(self.OnlyTextData).toarray()
        return list(vactors)

    def Find_similarity(self,data,text):
        self._preprocess(data,text)
        self.lent=len(self.New_Data)
        vactors=self._ToVector()
        cosine=cosine_similarity(vactors)
        distance=cosine[-1]
        listdata=sorted(list(enumerate(distance)),key=lambda x:x[1],reverse=True)
        for r in listdata:
            title=self.OnlyTextData[r[0]]
            if title!=self.OnlyTextData[-1]:
                T_idx=r[0]
                index=self.New_Data[T_idx][0]
                # text=self.New_Data[T_idx][1]
                return index

 
if __name__=="__main__":     
    Data=[
                    [
                        "what is your name ?",
                        "your name",
                        "what people call you ?",
                        "what did i call you ?"
                    ],
                    [
                        "What is your gender",
                        "what is your sex",
                        "your gender",
                        "are you a male",
                        "are you a female",
                        "Are you male or female"
                    ],
                    [
                        "What is your favorite colour",
                        "what is your fav color",
                        "Your fav color"
                    ]]
    while True:
        text=input("Enter text >>")
        ans=FSCosine().Find_similarity(Data,text)
        print(ans)
            