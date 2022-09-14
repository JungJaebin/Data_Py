import pandas as pd
import numpy as np
import datetime

class Momentum() :

    def __init__(self, df, col) :
    
        self.df = df.loc[:, ['Date', col]]
        self.col = col

        # 년-월 컬럼을 추가
        self.df['STD-YM'] = self.df['Date'].map(lambda x : datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%Y-%m'))
        
        # 비어있는 데이터프레임을 생성
        self.month_last_df = pd.DataFrame()

        # 년-월 컬럼의 유니크 값을 month_list에 삽입
        self.month_list = self.df['STD-YM'].unique()


    def create_df(self) :

        for i in self.month_list :

            self.last_df = self.df[self.df['STD-YM'] == i].tail(1)
            self.month_last_df = pd.concat([self.month_last_df, self.last_df])
            # len(month_last_df) == len(month_list)

        self.month_last_df['BF_1M'] = self.month_last_df.shift(1)[self.col].fillna(0)   
        self.month_last_df['BF_12M'] = self.month_last_df.shift(12)[self.col].fillna(0) 
        
        self.month_last_df.set_index(['Date'], inplace = True)      # loc를 사용할 때 편하게 사용하기 위해서 set.index로 변경
        
        self.df.set_index(['Date'], inplace = True)

        self.df['trade'] = ''
       
        return self.month_last_df


    def add_trade(self) :

        for i in self.month_last_df.index :
            
            self.signal = ''

            self.momentum_index = self.month_last_df.loc[i, 'BF_1M'] / self.month_last_df.loc[i, 'BF_12M'] - 1

            self.flag = True if((self.momentum_index > 0.0) and (self.momentum_index != np.inf) and (self.momentum_index != -np.inf)) else False

            if self.flag :       

                self.signal = 'buy'

            print('날짜: ', i, '모멘텀 인덱스: ', self.momentum_index, 'self.flag: ', self.flag, 'self.signal: ', self.signal)

            self.df.loc[i, 'trade'] = self.signal

        self.df.value_counts('trade')


    def returns(self) :
    
        self.rtn = 1.0
        self.buy = 0.0
        self.sell = 0.0

        self.df['return'] = 1

        for i in self.df.index :

            if self.df.loc[i, 'trade'] == 'buy' and self.df.shift(1).loc[i, 'trade'] == '' :   
                
                self.buy = self.df.loc[i, self.col]

                print('진입일: ', i, '진입 가격: ', self.buy)

            elif self.df.loc[i, 'trade'] == '' and self.df.shift(1).loc[i, 'trade'] == 'buy' :    
                
                self.sell = self.df.loc[i, self.col]
                self.rtn = (self.sell - self.buy) / self.buy + 1        
                self.df.loc[i, 'return'] = self.rtn

                print('청산일: ', i, '진입 가격: ', self.buy, '청산 가격: ', self.sell, '| return: ', round(self.rtn, 4))

            if self.df.loc[i, 'trade'] == '' :         
               
                self.buy = 0.0
                self.sell = 0.0

        self.acc_rtn = 1.0

        for i in self.df.index :
            
            self.rtn = self.df.loc[i, 'return']
            self.acc_rtn = self.acc_rtn * self.rtn
            self.df.loc[i, 'acc_rtn'] = self.acc_rtn

        print('누적수익률: ', round(self.acc_rtn, 4))
        
        return self.df