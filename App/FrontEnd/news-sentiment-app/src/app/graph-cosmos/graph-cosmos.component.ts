import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Graph, GraphConfigInterface } from '@cosmograph/cosmos';
import neo4j, { Transaction, Record, graph } from 'neo4j-driver';

interface Node {
  id: string;
  x?: number;
  y?: number;
}

interface Link {
  source: string;
  target: string;
  time?: string;
}

const config: GraphConfigInterface<Node, Link> = {
  renderLinks: true,
  //linkColor: (link:any) => link.color,
  //nodeColor: (node:any) => node.color,
  events: {
    onClick: (node:any) => { console.log('Clicked node: ', node) },
  },
  backgroundColor: "#151515",
  nodeSize: 2,
  nodeColor: "#4B5BBF",
  nodeGreyoutOpacity: 0.1,
  linkWidth: 0.1,
  linkColor: "#5F74C2",
  linkArrows: false,
  linkGreyoutOpacity: 0,
  renderHoveredNodeRing: true,
  hoveredNodeRingColor: "#4B5BBF",
  simulation: {
    linkDistance: 3,
    linkSpring: 2,
    repulsion: 0.5,
    gravity: 0.5,

  }};

@Component({
  selector: 'app-graph-cosmos',
  template: '<canvas #canvas></canvas>',
  styleUrls: ['./graph-cosmos.component.css']
})
export class GraphCosmosComponent implements OnInit {
  @ViewChild('canvas')
  canvas!: ElementRef;

  graph!: Graph<Node, Link>;

  async ngOnInit() {

    const driver = neo4j.driver(
      'bolt://localhost:7687',
      neo4j.auth.basic('neo4j', 'StrongPassword!')
      );

    const session = driver.session({database: "neo4j"});
    try {
      const result = await session.run(
        'MATCH (k:Keyword)-[:IS_MENTIONED_IN]->(a:Article) RETURN { id: id(k), label:head(labels(k)), value:k.value } as source, { id: id(a), label:head(labels(a)), abstract:a.abstract } as target LIMIT $limit', 
        {limit: neo4j.int(100)}
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

      this.graph = new Graph(this.canvas.nativeElement, config);
      this.graph.setData(Object.values(nodes), links);
    } catch (error) {
      console.log(error);
    } finally {
      await session.close();
    }
  }

  ngOnDestroy() {
    this.graph.destroy();
  }
}