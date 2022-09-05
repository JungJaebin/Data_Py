import pandas as pd

class Class_4() :
    def __init__(self, _path) :             # _a: a는 입력받은 값이라는 뜻
        self.df = pd.read_csv(_path)
    
    def change(self, _column) :         # '_column' 특정 컬럼 지정
        self.df[_column] = self.df[_column].str.replace(' ', '')    # 공백 제거

        self.df[_column] = self.df[_column].str.upper()             # 대문자 변경
        
        return self.df

    def change_dt(self, _column, _format = '') :
        if _format == '' :
            self.df[_column] = pd.to_datetime(self.df[_column])

        else :
            self.df[_column] = pd.to_datetime(self.df[_column], format = _format)

        return self.df

    def create_date(self, _column) :
        self.df['year'] = self.df[_column].dt.strftime('%Y')
        self.df['month'] = self.df[_column].dt.strftime('%m')
        self.df['day'] = self.df[_column].dt.strftime('%d')

        return self.df

    def review(self) :
        return self.df