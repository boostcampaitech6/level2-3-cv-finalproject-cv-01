export interface SelectOption {
    readonly value: string;
    readonly label: string;
    // readonly isFixed?: boolean;
    // readonly isDisabled?: boolean;
  }


  export const companyOptions: readonly SelectOption[] = [
    { label: 'Tesla', value: 'NASDAQ:TSLA'},
    { label: 'Apple', value: 'NASDAQ:AAPL'},
    { label: 'Google', value: 'NASDAQ:GOOGL'},
    { label: 'Nvidia', value: 'NASDAQ:Tesla'},
    // { label: 'Samsung', value: 'KRX:005930'},
    // { label: 'Naver', value: 'KRX:035420'},
    // { label: 'Kakao', value: 'KRX:035720'},
    { label: 'SK Hynix', value: 'KRX:000660'},
    { label: 'BTC-USD', value: 'BINANCE:BTCUSDT'},
    
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
    '1d': ['1m', '3m', '5m', '15m', '30m', '60m'],
    // '1d': ['1m', '2m', '5m', '15m', '30m', '60m', '90m'],
    '5d': ['5m', '15m', '30m', '60m'],
    '1mo': ['30m', '60m','1d'],
    '3mo': ['1d', '5d', '1wk', '1mo'],
    '6mo': ['1d', '5d', '1wk', '1mo'],
    '1y': ['1d', '5d', '1wk', '1mo'],
    '2y': ['1d', '5d', '1wk', '1mo'],
    '5y': ['1d', '5d', '1wk', '1mo'],
    '10y': ['1d', '5d', '1wk', '1mo'],
  };