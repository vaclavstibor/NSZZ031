import { Component, OnInit } from '@angular/core';
import { HttpService } from '../services/http.service';
import { Router, ActivatedRoute } from '@angular/router';
import { Ticker } from '../models/Ticker';
import ForceGraph3D from '3d-force-graph';

const d3 = require('d3-force-3d');

@Component({
  selector: 'app-ticker-graph',
  templateUrl: './ticker-graph.component.html',
  styleUrls: ['./ticker-graph.component.css']
})
export class TickerGraphComponent implements OnInit {
  data: Ticker = {} as Ticker;
  name: string = "";

  constructor(
    private httpService: HttpService,
    private route: ActivatedRoute,
    ) {
      this.route.params.subscribe(params => {
        this.name = params['name'];
      });
     }

  ngOnInit(): void {
    this.httpService.getTickerByName(this.name).subscribe((res: Ticker) => {
      this.data = res;
      console.log(res);
    
      this.launchGraph(this.data);
    });
  }

  async launchGraph(data: Ticker) {
    const start = new Date();
    const nodes: {[key: number]: any} = {};
    const links: any[] = [];

    try {
      // Create a node for the ticker
      nodes[data.id] = { id: data.id, label: data.label, name: data.name, ticker_sentiment_label: data.ticker_sentiment_label };
  
      // Loop through each article mentioned by the ticker
      data.articles.forEach((article: any) => {
        // Create a node for the article
        nodes[article.id] = { id: article.id, label: article.label, title: article.title, article_sentiment_label: article.article_sentiment_label };
  
        // Create a link between the ticker and the article
        //links.push({ source: data.id, target: article.id, ticker_sentiment_label: article.ticker_sentiment_label });
        console.log(links);
      });

      console.log(links.length + " links loaded in " + (new Date().getTime() - start.getTime()) + " ms.");
    

      
      const graphData = { nodes: Object.values(nodes), links: links };
      let graph = ForceGraph3D()(document.getElementById('3d-graph') as HTMLElement)
        .graphData(graphData)
        //.forceEngine('d3')
        //.d3AlphaDecay(0.01)
        .d3VelocityDecay(0.1)
        .d3Force('charge', null!) // Deactivate existing charge
        .d3Force('radial', d3.forceRadial((d: any) => d.label === 'Ticker' ? 0 : 400))
        .d3Force('collide', d3.forceCollide(16))
        .d3Force('link', d3.forceLink().id((d: any) => d.id).distance(400).strength(1))
        //.warmupTicks(100)
        //.cooldownTicks(0)  
        //.nodeAutoColorBy('label')
        //.nodeOpacity(1)
        //.linkWidth(0.5)
        //.linkDirectionalParticles(2)
        //.linkDirectionalParticleWidth(1)
        //.linkDirectionalParticleSpeed(0.006)
        //.dagMode('td')
        //.dagLevelDistance(200)
        .nodeVal((node: any) => Math.pow((node.label == 'Ticker' ? 3 : 1), 3))
        .nodeColor((node: any) => {
          if (node.label === 'Ticker') {
            return '#176696' // default blue by nodeAutoColorBy('label')
          } else {
            return this.getColorBySentimentLabel(node.article_sentiment_label)  
          }
        })
        .linkColor((link: any) => {     
          return this.getColorBySentimentLabel(link.ticker_sentiment_label)    
        })
        .nodeLabel((obj: object) => {
          const node = obj as any;
          if (node.label === 'Ticker') {
            return `${node.name}`;
          } else {
            return `${node.title}`;
          }
        })
        .onNodeClick((node:any) => {
          // Aim at node from outside it
          const distance = 40;
          const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);

          const newPos = node.x || node.y || node.z
            ? { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }
            : { x: 0, y: 0, z: distance }; // special case if node is in (0,0,0)

          graph.cameraPosition(
            newPos, // new position
            node, // lookAt ({ x, y, z })
            3000  // ms transition duration
          )})
        .onNodeHover(node => document.body.style.cursor = node ? 'pointer' : 'default')   
      } catch (error) {
      console.error(error);
    }    
  }
  
  getColorBySentimentLabel(sentimentLabel: any): string {
    switch (sentimentLabel) {
      case 'Bearish':
        return '#BC2023'; // Red
      case 'Somewhat-Bearish ':
        return '#Eb442C'; // Orange
      case 'Neutral':
        return '#F8B324'; // Yellow
      case 'Somewhat-Bullish':
        return '#0B6E4F'; // Dark Green 0C6B37
      case 'Bullish':
        return '#4AB535'; // Light Green
      default:
        return 'white';
    }
  }
}
