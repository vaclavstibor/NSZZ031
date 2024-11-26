export interface PriceData {
    /**
     * Interface for the price data
     * used in the company chart component.
     * 
     * date: The date of the price data
     * adj_close: The adjusted close price
     */
    date: string;
    adj_close: number;
  }
  
  export interface SentimentData {
    /**
     * Interface for the sentiment data
     * used in the company chart component.
     * 
     * date: The date of the sentiment data
     * adj_close: The adjusted close price
     * sentiment: The sentiment data
     * classification: The classification of the sentiment
     * positive: The positive sentiment value
     * neutral: The neutral sentiment value
     * negative: The negative sentiment value
     */
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
    /**
     * Interface for the company chart data
     * used in the dashboard component.
     * 
     * price_data: The price data of the company
      * sentiment_data: The sentiment data of the company
     */
    price_data: PriceData[];
    sentiment_data: SentimentData[];
  }