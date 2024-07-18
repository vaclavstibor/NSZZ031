export interface ArticleSentiment {
    classification: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
    positive: number;
    neutral: number;
    negative: number;
  }
  
interface CompanyArticle {
    id: string;
    title: string;
    type: string;
    section: string;
    published_date: string;
    url: string;
    author?: string; // x-nullable based on endpoint
    sentiment: ArticleSentiment;
  }

export interface CompanyArticleList extends Iterable<CompanyArticle> {
  [index: number]: CompanyArticle;
}