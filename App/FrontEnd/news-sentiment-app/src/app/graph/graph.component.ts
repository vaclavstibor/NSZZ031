/* 
Note: Důležité si uvědomit, že pokud má nějaký uzel 3M hran a v query 
nespecifikujeme název hrany, tak je 3M krát pomalejší, než když ji specifikujeme.
*/

import { Component, OnInit } from '@angular/core';

import ForceGraph3D, { 
  ConfigOptions, 
  ForceGraph3DInstance 
} from "3d-force-graph";

import neo4j, { Transaction, Record, graph } from 'neo4j-driver';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  graph: any;

  data: {
    nodes: any;
    links: any[];
  } = {
    nodes: [],
    links: []
  };

  ngOnInit(): void {
    
    const driver = neo4j.driver(
      'bolt://localhost:7687',
      neo4j.auth.basic('neo4j', 'StrongPassword!')
      );

    this.launchGraph(driver);
  }

  async launchGraph(driver: any) {
    const session = driver.session({database: "neo4j"});
    const start = new Date();
    try {
      const result = await session.run(
        // NYT 'MATCH (k:Keyword)-[:IS_MENTIONED_IN]->(a:Article) RETURN { id: id(k), label:head(labels(k)), value:k.value } as source, { id: id(a), label:head(labels(a)), abstract:a.abstract } as target LIMIT $limit', 
        'MATCH (t:Ticker)-[:IS_MENTIONED_IN]->(a:Article) RETURN { id: id(t), label:head(labels(t)), name:t.name } as source, { id: id(a), label:head(labels(a)), title:a.title, abstract:a.abstract } as target LIMIT $limit', 
        {limit: neo4j.int(3000)}
      );
      const nodes: {[key: number]: any} = {};
      const links = result.records.map((r:Record) => { 
        var source = r.get('source');
        source.id = source.id.toNumber();
        nodes[source.id] = source;
        var target = r.get('target');
        target.id = target.id.toNumber();
        nodes[target.id] = target;
        return {source: source.id, target: target.id};
      });
      interface Node {
        id: number;
        label: string;
        caption: string;
        value: number;
        abstract: string;
        name: string;
        title: string;
      }

      console.log(links.length + " links loaded in " + (new Date().getTime() - start.getTime()) + " ms.");
      const gData = { nodes: Object.values(nodes), links: links};
      this.graph = ForceGraph3D()(document.getElementById('3d-graph') as HTMLElement)
                    .graphData(gData)
                    .nodeAutoColorBy('label')
                    .nodeLabel((obj: object) => {
                      const node = obj as Node;
                      if (node.label === 'Ticker') {
                        return `${node.name}`;
                      } else {
                        return `${node.title}`;
                      }
                    })
                    .onNodeHover(node => document.body.style.cursor = node ? 'pointer' : 'default')

    } catch (error) {
      console.log(error);
    } finally {
      await session.close();
    }
  }

  ngOnDestroy(): void {
    this.graph = null;
  }
}
