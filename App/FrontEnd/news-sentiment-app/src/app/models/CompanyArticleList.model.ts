export interface ArticleSentiment {
  /**
   * Interface for the article sentiment data
   * used in the company article list component.
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
  
interface CompanyArticle {
    /**
     * Interface for the company article data
     * used in the company article list component.
     * 
     * id: The UUID of the article
     * title: The title of the article
     * type: The type of the article
     * section: The section of the article
     * published_date: The published date of the article
     * url: The URL of the article
     * author: The author of the article
     * sentiment: The sentiment data of the article
     */
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
  /**
   * Interface for the company article list data
   * used in the company article list component.
   * 
   * [index: number]: The index of the company article
   * CompanyArticle: The company article data
   */
  [index: number]: CompanyArticle;
}