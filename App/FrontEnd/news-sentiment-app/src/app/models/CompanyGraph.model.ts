export interface Sentiment {
    classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    positive: number;
    neutral: number;
    negative: number;
  }
  
export interface ArticleNode {
    id: string; // UUID
    node_type: 'article';
    title: string;
    published_date: string; // Date-time format
    url: string; // URI format
    author?: string; // Nullable
    sentiment: Sentiment;
  }
  
export interface CompanyNode {
    id: number;
    node_type: 'company';
    short_name: string;
    ticker: string;
    sentiment: Sentiment;
  }
  
export interface Link {
    source: string; // UUID
    target: number;
    sentiment: Sentiment;
  }
  
export interface CompanyGraph {
    nodes: (ArticleNode | CompanyNode)[];
    links: Link[];
  }