import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { ActivatedRoute } from '@angular/router';
import { ForceGraph3DInstance } from '3d-force-graph';
import ForceGraph3D from '3d-force-graph';
import * as dat from 'dat.gui';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css'],
})
export class GraphComponent implements OnInit, OnDestroy {
  private graph!: ForceGraph3DInstance;
  private graphData: { nodes: any[], links: any[] } = { nodes: [], links: [] };
  private guiControls: dat.GUI | null = null;
  private guiInformation: dat.GUI | null = null;
  private highlightNodes = new Set();
  private highlightLinks = new Set();
  private hoverNode = null;

  constructor(private httpService: HttpService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.loadGraphData();
  }

  ngOnDestroy(): void {
    this.cleanup();
  }

  private loadGraphData(): void {
    this.route.params.subscribe(params => {
      const ticker = params['ticker'];
      this.httpService.getCompanyGraphData(ticker).subscribe((res: any) => {
        this.graphData = { nodes: res.nodes, links: res.links };
        this.launchGraph();
      });
    });
  }

  private launchGraph(): void {
    const elem = document.getElementById('3d-graph') as HTMLElement;
    this.graph = ForceGraph3D()(elem)
      .graphData(this.graphData)
      .forceEngine('d3')
      .nodeOpacity(1)
      .backgroundColor('#131316')
      .linkWidth(link => this.highlightLinks.has(link) ? 5 : 1)
      .linkDirectionalParticleWidth(link => this.highlightLinks.has(link) ? 5 : 2)
      .linkDirectionalParticles(link => this.highlightLinks.has(link) ? 5 : 2)
      .linkDirectionalParticleSpeed(link => this.highlightLinks.has(link) ? 0.01 : 0.006)
      .linkColor((link: any) => this.getColorBySentiment(link.sentiment))
      .nodeVal(node => this.getNodeValue(node))
      .nodeColor(node => this.getNodeColor(node))
      .nodeLabel(node => this.getNodeLabel(node))
      .onNodeClick(node => this.onNodeClick(node))
      .onNodeHover(node => this.onNodeHover(node, this.graph));

    this.setupGuiControls();
  }

  private getNodeValue(node: any): number {
    if (this.highlightNodes.has(node)) {
      return node === this.hoverNode ? 50 : 25;
    }
    return node.node_type == 'company' ? 2 : 1;
  }

  private getNodeColor(node: any): string {
    return node.node_type === 'company' ? '#1D57A9' : this.getColorBySentiment(node.sentiment);
  }

  private getNodeLabel(node: any): string {
    return node.node_type === 'company' ? node.short_name : node.title;
  }

  private onNodeClick(node: any): void {
    const distance = 250;
    const distRatio = 1 + distance / Math.hypot(node.x, node.y, node.z);
    const newPos = {
      x: node.x * distRatio,
      y: node.y * distRatio,
      z: node.z * distRatio,
    };
    this.graph.cameraPosition(newPos, node, 1500);
    this.displayNodeInformation(node);
  }

  private onNodeHover(node: any, graph: ForceGraph3DInstance): void {
    if (this.isNodeAlreadyHovered(node)) return;

    this.clearHighlights();
    if (node) {
      this.highlightNodeAndRelatedElements(node);
    }
    this.hoverNode = node || null;
    this.updateHighlight();
  }

  private isNodeAlreadyHovered(node: any): boolean {
    return (!node && !this.highlightNodes.size) || (node && this.hoverNode === node);
  }

  private clearHighlights(): void {
    this.highlightNodes.clear();
    this.highlightLinks.clear();
  }

  private highlightNodeAndRelatedElements(node: any): void {
    this.highlightNodes.add(node);
    if (node.node_type === 'article') {
      this.highlightRelatedCompany(node);
    }
  }

  private highlightRelatedCompany(node: any): void {
    const companyId = this.graphData.links[0].target.id;
    const companyNode = this.graphData.nodes.find((n: any) => n.id === companyId);
    if (companyNode) this.highlightNodes.add(companyNode);
    const link = this.graphData.links.find((l: any) => l.target.id === companyId && l.source.id === node.id);
    if (link) this.highlightLinks.add(link);
  }

  private updateHighlight(): void {
    this.graph
      .nodeVal(this.graph.nodeVal())
      .linkWidth(this.graph.linkWidth())
      .linkDirectionalParticles(this.graph.linkDirectionalParticles())
      .linkDirectionalParticleSpeed(this.graph.linkDirectionalParticleSpeed())
      .linkDirectionalParticleWidth(this.graph.linkDirectionalParticleWidth());
  }

  private getColorBySentiment(sentiment: any): string {
    switch (sentiment.classification) {
      case 'NEGATIVE':
        return 'red';
      case 'POSITIVE':
        return 'green';
      case 'NEUTRAL':
        return sentiment.negative > sentiment.positive
          ? `rgba(255, 0, 0, ${Number(sentiment.negative) + 0.30})`
          : `rgba(0, 128, 0, ${Number(sentiment.positive) + 0.30})`;
      default:
        return 'white';
    }
  }

  private setupGuiControls(): void {
    const settings = new GraphSettings();
    this.guiControls = new dat.GUI({ autoPlace: true, width: 250 });
    const distancesFolder = this.guiControls.addFolder('Distances');
    distancesFolder.add(settings, 'positiveDistance', 100, 3000).name('POSITIVE').onChange(() => this.updateLinkDistance(settings));
    distancesFolder.add(settings, 'neutralDistance', 100, 3000).name('NEUTRAL').onChange(() => this.updateLinkDistance(settings));
    distancesFolder.add(settings, 'negativeDistance', 100, 3000).name('NEGATIVE').onChange(() => this.updateLinkDistance(settings));

    const visibilityFolder = this.guiControls.addFolder('Visibility');
    visibilityFolder.add(settings, 'showPOSITIVE').name('POSITIVE').onChange(() => this.updateVisibility(settings));
    visibilityFolder.add(settings, 'showNEUTRAL').name('NEUTRAL').onChange(() => this.updateVisibility(settings));
    visibilityFolder.add(settings, 'showNEGATIVE').name('NEGATIVE').onChange(() => this.updateVisibility(settings));

    this.updateLinkDistance(settings);
    this.updateVisibility(settings);

    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private updateLinkDistance(settings: GraphSettings): void {
    const linkForce = this.graph.d3Force('link');
    if (linkForce) {
      linkForce['distance']((link: any) => {
        switch (link.sentiment.classification) {
          case 'POSITIVE':
            return settings.positiveDistance;
          case 'NEUTRAL':
            return settings.neutralDistance;
          case 'NEGATIVE':
            return settings.negativeDistance;
          default:
            return settings.neutralDistance;
        }
      });
    }
    this.graph.numDimensions(3);
  }

  private updateVisibility(settings: GraphSettings): void {
    this.graph.nodeVisibility((node: any) => {
      if (node.node_type === 'article') {
        const key: keyof GraphSettings = `show${node.sentiment.classification}` as keyof GraphSettings;
        return Boolean(settings[key]);
      }
      return true;
    });

    this.graph.linkVisibility((link: any) => {
      const key: keyof GraphSettings = `show${link.sentiment.classification}` as keyof GraphSettings;
      return Boolean(settings[key]);
    });
  }

  private displayNodeInformation(node: any): void {
    this.resetGuiInformation();
    if (node.node_type === 'article') {
      this.displayArticleInformation(node);
    } else if (node.node_type === 'company') {
      this.displayCompanyInformation(node);
    }
  }

  private resetGuiInformation(): void {
    if (this.guiInformation) {
      this.guiInformation.destroy();
    }
    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private displayArticleInformation(node: any): void {
    const articleInfoFolder = this.guiInformation!.addFolder('Article Information');
    this.addArticleFields(articleInfoFolder, node);
    this.addSentimentFields(articleInfoFolder, node.sentiment);
  }

  private addArticleFields(folder: dat.GUI, node: any): void {
    folder.add({ Title: node.title }, 'Title').name('Title');
    folder.add({ PublishedDate: node.published_date }, 'PublishedDate').name('Published Date');
    folder.add({ Author: node.author }, 'Author').name('Author');
    folder.add({ 'Open URL': () => window.open(node.url, '_blank') }, 'Open URL').name('Open Article');
  }

  private addSentimentFields(folder: dat.GUI, sentiment: any): void {
    const sentimentFolder = folder.name === "Today's Sentiment" ? folder : folder.addFolder('Sentiment');
    sentimentFolder.add({ Sentiment: sentiment.classification }, 'Sentiment').name('Classification');
    sentimentFolder.add({ Positive: sentiment.positive }, 'Positive').name('Positive');
    sentimentFolder.add({ Neutral: sentiment.neutral }, 'Neutral').name('Neutral');
    sentimentFolder.add({ Negative: sentiment.negative }, 'Negative').name('Negative');
  }

  private displayCompanyInformation(node: any): void {
    const companyInfoFolder = this.guiInformation!.addFolder('Company Information');
    this.addCompanyFields(companyInfoFolder, node);
    this.addSentimentFields(companyInfoFolder.addFolder("Today's Sentiment"), node.sentiment);
    this.addArticles(companyInfoFolder, node);
  }

  private addCompanyFields(folder: dat.GUI, companyNode: any): void {
    const companyFolder = folder.addFolder(`${companyNode.short_name}`);
    companyFolder.add({ Ticker: companyNode.ticker}, 'Ticker').name('Ticker');
    companyFolder.add({ 'Open Dashboard': () => window.open(`/company/${companyNode.ticker}/dashboard`, '_blank') }, 'Open Dashboard').name('Open Dashboard');
  }

  private addArticles(folder: dat.GUI, companyNode: any): void {
    const articlesInfoFolder = this.guiInformation!.addFolder('Articles');
  
    this.graphData.links.forEach((link: any) => {
      const articleNode = link.source; 
      if (articleNode) {
        const articleLink = this.graphData.links.find((l: any) => l.target.id === companyNode.id && l.source.id === articleNode.id);
        if (articleLink) {
          
          const articleFolder = articlesInfoFolder.addFolder(truncateWithEllipsis(articleNode.title));
          
          this.addSentimentFields(articleFolder, articleLink.sentiment);
        }
      }
    });
  }

  private cleanup(): void {
    if (this.guiControls) {
      this.guiControls.destroy();
      this.guiControls = null;
    }
    if (this.guiInformation) {
      this.guiInformation.destroy();
      this.guiInformation = null;
    }
    if (this.graph) {
      this.graph._destructor();
    }
  }
}

class GraphSettings {
  positiveDistance = 200;
  neutralDistance = 200;
  negativeDistance = 200;

  showPOSITIVE = true;
  showNEGATIVE = true;
  showNEUTRAL = true;

  [key: string]: any;
}

function truncateWithEllipsis(text: string): string {
  /**
   * Function for truncation long titles.
   */
  const maxLength: number = 50;

  if (text.length > maxLength) {
    return text.substring(0, maxLength - 3) + '...'; 
  } else {
    return text;
  }
}
