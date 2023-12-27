export interface Ticker {
    id: number;
    name: string;
    label: string;
    ticker_sentiment_label: string;
    articles: Array<number> // Article IDs
}