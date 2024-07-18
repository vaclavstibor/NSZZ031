interface Sentiment {
    classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    positive: number;
    neutral: number;
    negative: number;
}
  
export interface CompanyInfo {
    shortName: string;
    ticker: string;
    website: string;
    industry: string;
    dayHigh: number;
    dayLow: number;
    volume: number;
    sentiment: Sentiment;
}