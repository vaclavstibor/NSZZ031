export interface Sentiment {
    classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    positive: number;
    neutral: number;
    negative: number;
}

export interface ArticleNode {
    id: string; // UUID format
    node_type: 'article';
    title: string;
    published_date: string; // Date-time format
    url: string; // URI format
    author?: string; // Nullable
    sentiment: Sentiment;
    companies: number[]; // An array of company IDs
}

export interface CompanyNode {
    id: number;
    node_type: 'company';
    short_name: string;
    ticker: string;
    sentiment: Sentiment;
    articles: string[]; // An array of article UUIDs
}

export interface Link {
    source: string; // UUID format for articles
    target: number; // Numeric ID for companies
    sentiment: Sentiment;
}

export interface CompaniesGraphs {
    nodes: (ArticleNode | CompanyNode)[];
    links: Link[];
}