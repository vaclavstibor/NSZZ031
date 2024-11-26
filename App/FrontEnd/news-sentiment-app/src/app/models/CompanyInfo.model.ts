interface Sentiment {
    /**
     * Interface for the sentiment data
     * used in the company info component.
     * 
     * classification: The classification of the sentiment
     * positive: The positive sentiment value
     * neutral: The neutral sentiment value
     * negative: The negative sentiment value
     */
    classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    positive: number;
    neutral: number;
    negative: number;
}
  
export interface CompanyInfo {
    /**
     * Interface for the company info data
     * used in the dashboard component.
     * 
     * shortName: The name of the company
     * ticker: The ticker of the company
     * website: The website of the company
     * industry: The industry of the company
     * dayHigh: The highest price of the day
     * dayLow: The lowest price of the day
     * volume: The volume of the company
     * sentiment: The sentiment data of the company
     */
    shortName: string;
    ticker: string;
    website: string;
    industry: string;
    dayHigh: number;
    dayLow: number;
    volume: number;
    sentiment: Sentiment;
}