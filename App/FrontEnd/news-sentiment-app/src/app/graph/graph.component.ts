import { Component, OnInit } from '@angular/core';

import ForceGraph3D, { 
  ConfigOptions, 
  ForceGraph3DInstance 
} from "3d-force-graph";

import neo4j, { Transaction, Record } from 'neo4j-driver';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {
  
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
        'MATCH (n)-->(m) RETURN { id: id(n), label:head(labels(n)), value:n.value, abstract:n.abstract } as source, { id: id(m), label:head(labels(m)), value:m.value, abstract:m.abstract } as target LIMIT $limit', 
        {limit: neo4j.int(5000)}
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
      }

      console.log(links.length + " links loaded in " + (new Date().getTime() - start.getTime()) + " ms.");
      const gData = { nodes: Object.values(nodes), links: links};
      const Graph = ForceGraph3D()(document.getElementById('3d-graph') as HTMLElement)
                    .graphData(gData)
                    .nodeAutoColorBy('label')
                    .nodeLabel((obj: object) => {
                      const node = obj as Node;
                      if (node.label === 'Keyword') {
                        return `${node.label}: ${node.value}`;
                      } else {
                        return `${node.label}: ${node.abstract}`;
                      }
                    })
                    .onNodeHover(node => document.body.style.cursor = node ? 'pointer' : 'default');
    } catch (error) {
      console.log(error);
    } finally {
      await session.close();
    }
  }
}
