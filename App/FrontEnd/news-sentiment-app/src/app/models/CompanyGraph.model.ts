export interface Sentiment {
    /**
     * Interface for the sentiment data
     * used in the company chart component.
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
  
export interface ArticleNode {
    /**
     * Interface for the article node data
     * used in the company graph component.
     * 
     * id: The UUID of the article
     * node_type: The type of the node
     * title: The title of the article
     * published_date: The published date of the article
     * url: The URL of the article
     * author: The author of the article
     * sentiment: The sentiment data of the article
     */
    id: string; // UUID
    node_type: 'article';
    title: string;
    published_date: string; // Date-time format
    url: string; // URI format
    author?: string; // Nullable
    sentiment: Sentiment;
  }
  
export interface CompanyNode {
    /**
     * Interface for the company node data
     * used in the company graph component.
     * 
     * id: The ID of the company
     * node_type: The type of the node
     * short_name: The short name of the company
     * ticker: The ticker of the company
     * sentiment: The sentiment data of the company
     */
    id: number;
    node_type: 'company';
    short_name: string;
    ticker: string;
    sentiment: Sentiment;
  }
  
export interface Link {
    /**
     * Interface for the link data
     * used in the company graph component.
     * 
     * source: The source of the link
     * target: The target of the link
     * sentiment: The sentiment data of the link
     */
    source: string; // UUID
    target: number;
    sentiment: Sentiment;
  }
  
export interface CompanyGraph {
    /**
     * Interface for the company graph data
     * used in the company graph component.
     * 
     * nodes: The nodes of the graph
     * links: The links of the graph
     */
    nodes: (ArticleNode | CompanyNode)[];
    links: Link[];
  }