export interface PriceData {
    date: string;
    adj_close: number;
  }
  
  export interface SentimentData {
    date: string;
    adj_close: number;
    sentiment: {
      classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
      positive: number;
      neutral: number;
      negative: number;
    };
  }
  
  export interface CompanyChart {
    price_data: PriceData[];
    sentiment_data: SentimentData[];
  }