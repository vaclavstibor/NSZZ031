import { Injectable } from '@angular/core';
import neo4j from 'neo4j-driver';


@Injectable({
  providedIn: 'root'
})
export class SearchService {
  constructor() { }

  private driver = neo4j.driver(
    'bolt://localhost:7687',
    neo4j.auth.basic('neo4j', 'StrongPassword!')
  );

  async getTickers() {
    const session = this.driver.session({database: "neo4j"});
    try {
      const result = await session.run(
        'MATCH (t:Ticker) RETURN t LIMIT $limit',
        {limit: neo4j.int(1000)}
      );
      return result.records.map((r: any) => r._fields[0]);
    } catch (error) {
      console.log(error);
      return [error];
    } finally {
      session.close();
    }
  }
}
