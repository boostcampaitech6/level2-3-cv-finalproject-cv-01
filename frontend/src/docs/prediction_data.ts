export interface SelectOption {
    readonly value: string;
    readonly label: string;
    // readonly isFixed?: boolean;
    // readonly isDisabled?: boolean;
  }


  export const companyOptions: readonly SelectOption[] = [
    { label: 'Tesla', value: 'Tesla'},
    { label: 'Apple', value: 'AAPL'},
    { label: 'Google', value: 'GOOGL'},
    { label: 'Nvidia', value: 'Tesla'},
    { label: 'Samsung', value: '005930.KS'},
    { label: 'Naver', value: '035420.KS'},
    { label: 'Kakao', value: '035720.KS'},
    { label: 'SK Hynix', value: '000660.KS'},
    { label: 'BTC-USD', value: 'BTC-USD'},
    
  ];


  export const periodOptions: readonly SelectOption[] = [
    { label: '1 Day', value: '1d'},
    { label: '5 Days', value: '5d'},
    { label: '1 Month', value: '1mo'},
    { label: '3 Months', value: '3mo'},
    { label: '6 Months', value: '6mo'},
    { label: '1 Year', value: '1y'},
    { label: '2 Years', value: '2y'},
    { label: '5 Years', value: '5y'},
    { label: '10 Years', value: '10y'},
  ];


  export const intervalOptionsMap = {
    '1d': ['1m', '2m', '5m', '15m', '30m', '60m', '90m'],
    '5d': ['5m', '15m', '30m', '60m', '90m'],
    '1mo': ['30m', '60m', '90m', '1d'],
    '3mo': ['1d', '5d', '1wk', '1mo'],
    '6mo': ['1d', '5d', '1wk', '1mo'],
    '1y': ['1d', '5d', '1wk', '1mo'],
    '2y': ['1d', '5d', '1wk', '1mo'],
    '5y': ['1d', '5d', '1wk', '1mo'],
    '10y': ['1d', '5d', '1wk', '1mo'],
  };