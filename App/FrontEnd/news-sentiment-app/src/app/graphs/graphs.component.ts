import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpService } from '../services/http.service';
import ForceGraph3D, { ForceGraph3DInstance } from '3d-force-graph';
import * as dat from 'dat.gui';

@Component({
  selector: 'app-graphs',
  templateUrl: './graphs.component.html',
  styleUrls: ['./graphs.component.css'],
})
export class GraphsComponent implements OnInit, OnDestroy {
  private graph!: ForceGraph3DInstance;
  private graphData: { nodes: any[]; links: any[] } = { nodes: [], links: [] };
  private guiControls: dat.GUI | null = null;
  private guiInformation: dat.GUI | null = null;
  private highlightNodes = new Set();
  private highlightLinks = new Set();
  private hoverNode = null;

  constructor(private httpService: HttpService) {}

  ngOnInit(): void {
    this.loadGraphData();
  }

  ngOnDestroy(): void {
    this.cleanup();
  }

  private loadGraphData(): void {
    this.httpService.getCompaniesGraphsData().subscribe((res: any) => {
      this.graphData = { nodes: res.nodes, links: res.links };
      this.launchGraph();
    });
  }

  private async launchGraph() {
    const elem = document.getElementById('3d-graph') as HTMLElement;
    this.graph = ForceGraph3D()(elem)
      .graphData(this.graphData)
      .cameraPosition({ z: 5000 }) // Initial camera position
      .forceEngine('d3')
      .nodeOpacity(1)
      .backgroundColor('#131316')
      .linkWidth(link => this.highlightLinks.has(link) ? 10 : 5)
      .linkDirectionalParticleWidth(link => this.highlightLinks.has(link) ? 10 : 3)
      .linkDirectionalParticles(link => this.highlightLinks.has(link) ? 8 : 3)
      .linkDirectionalParticleSpeed(link => this.highlightLinks.has(link) ? 0.01 : 0.006)
      .linkColor((link: any) => this.getColorBySentiment(link.sentiment))
      .nodeVal((node: any) => this.highlightNodes.has(node) ? this.getNodeVal(node) * 10 : this.getNodeVal(node)) // 
      .nodeColor((node: any) => node.node_type === 'company' ? '#1D57A9' : this.getColorBySentiment(node.sentiment))
      .nodeLabel((node: any) => node.node_type === 'company' ? `${node.short_name}` : `${node.title}`)
      .onNodeClick((node: any) => this.onNodeClick(node))
      .onNodeRightClick(() => this.resetNodeVisibility())
      .onNodeHover(node => this.onNodeHover(node, this.graph));
    
      if (this.graph) {
        const chargeForce = this.graph.d3Force('charge');
        if (chargeForce) {
          // Spread nodes a wider apart
          chargeForce['strength'](-5000);
        }
      }
    this.setupGUI();
  }

  private setupGUI(): void {
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

    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private onNodeClick(node: any): void {
    /**
     * When a node is clicked, the graph will zoom in on the node,
     * display information about the node, and display the node's neighbors.
     */
    const distance = 1000;
    const distRatio = 1.5 + distance / Math.hypot(node.x, node.y, node.z);
    const newPos = {
      x: node.x * distRatio,
      y: node.y * distRatio,
      z: node.z * distRatio,
    };

    this.graph.cameraPosition(newPos, node, 1500);
    this.displayNodeInformation(node);
    this.displayNodeNeighbors(node);
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

  private resetNodeVisibility(): void {
    this.graph.nodeVisibility(() => true);
    this.graph.linkVisibility(() => true);
    const visibilityFolder = this.guiControls!.__folders['Visibility'];
    if (visibilityFolder && visibilityFolder.domElement) {
      visibilityFolder.domElement.style.display = '';
    }
    this.guiControls!.__folders['Visibility'].__controllers.forEach(controller => controller.setValue(true));
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
      this.highlightRelatedCompanies(node);
    } else if (node.node_type === 'company') {
      this.highlightRelatedArticles(node);
    }
  }

  private highlightRelatedCompanies(node: any): void {
    node.companies.forEach((companyId: any) => {
      const companyNode = this.graphData.nodes.find((n: any) => n.id === companyId);
      if (companyNode) this.highlightNodes.add(companyNode);
      const link = this.graphData.links.find((l: any) => l.target.id === companyId && l.source.id === node.id);
      if (link) this.highlightLinks.add(link);
    });
  }

  private highlightRelatedArticles(node: any): void {
    node.articles.forEach((articleId: any) => {
      const articleNode = this.graphData.nodes.find((n: any) => n.id === articleId);
      if (articleNode) this.highlightNodes.add(articleNode);
      const link = this.graphData.links.find((l: any) => l.target.id === node.id && l.source.id === articleId);
      if (link) this.highlightLinks.add(link);
    });
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
        return this.getNeutralColor(sentiment);
      default:
        return 'white';
    }
  }

  private getNeutralColor(sentiment: any): string {
    const alpha = sentiment.negative > sentiment.positive
      ? Number(sentiment.negative) + 0.30
      : Number(sentiment.positive) + 0.30;
    return `rgba(${sentiment.negative > sentiment.positive ? '255, 0, 0' : '0, 128, 0'}, ${alpha})`;
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
    this.graph.numDimensions(3); // Ensure 3D layout
  }

  private updateVisibility(settings: GraphSettings): void {
    /**
    * Updates the visibility of nodes and links in the graph
    * based on the user's settings related to sentiment visibility.
    * Article nodes are shown or hidden based on their sentiment,
    * and company nodes are shown or hidden based on if any of their
    * articles are visible.
    */
    this.graph.nodeVisibility((node: any) => {
      if (node.node_type === 'article') {
        // Construct the key to check in settings based on the article's sentiment
        const key: keyof GraphSettings = `show${node.sentiment.classification}` as keyof GraphSettings;
        // Return true or false based on the settings for showing this sentiment
        return Boolean(settings[key]);
      }
      if (node.node_type === 'company') {
        // Check if any of the company's articles should be visible
        return node.articles.some((articleId: any) => {
          // Find the article node by ID
          const articleNode = this.graphData.nodes.find((n: any) => n.id === articleId);
          if (articleNode) {
            // Construct the key to check in settings based on the article's sentiment
            const key: keyof GraphSettings = `show${articleNode.sentiment.classification}` as keyof GraphSettings;
            // Return true if the article's sentiment is set to be visible
            return Boolean(settings[key]);
          }
          return false;
        });
      }
    });
    
    this.graph.linkVisibility((link: any) => {
      // Construct the key to check in settings based on the source's (article's) sentiment
      const key: keyof GraphSettings = `show${link.source.sentiment.classification}` as keyof GraphSettings;
      // Return true or false based on the settings for showing this sentiment
      return Boolean(settings[key]);
    });
    }

  private displayNodeInformation(node: any): void {
    /**
     * When a node is clicked, this function will display information
     * about the node in the GUI. The GUI will display different information
     * based on the type of node (article or company).
     */

    this.resetGuiInformation();

    if (node.node_type === 'article') {
      this.displayArticleInformation(node);
    } else if (node.node_type === 'company') {
      this.displayCompanyInformation(node);
    }
  }

  private resetGuiInformation(): void {
    /**
     * Resets the GUI information panel to prepare for new information.
     */
    if (this.guiInformation) {
      this.guiInformation.destroy();
    }
    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private displayArticleInformation(node: any): void {
    const articleInfoFolder = this.guiInformation!.addFolder('Article Information');
    this.addArticleFields(articleInfoFolder, node);
    this.addSentimentFields(articleInfoFolder, node.sentiment);
    this.addCompanies(articleInfoFolder, node, node.companies);
  }

  private displayCompanyInformation(node: any): void {
    const companyInfoFolder = this.guiInformation!.addFolder('Company Information');
    this.addCompanyFields(companyInfoFolder, node, node.articles);
    this.addArticles(companyInfoFolder, node);
  }

  private addArticleFields(folder: dat.GUI, node: any): void {
    folder.add({ Title: node.title }, 'Title').name('Title');
    folder.add({ PublishedDate: node.published_date }, 'PublishedDate').name('Published Date');
    folder.add({ Author: node.author }, 'Author').name('Author');
    folder.add({ 'Open URL': () => window.open(node.url, '_blank') }, 'Open URL').name('Open Article');
  }

  private addSentimentFields(folder: dat.GUI, sentiment: any): void {
    /**
     * Adds sentiment fields to the GUI information panel.
     */
    let sentimentFolder; 
  
    if (folder.name === 'Article Information') {
      sentimentFolder = folder.addFolder('Average Sentiment');
    } else{
      sentimentFolder = folder.addFolder('Ticker\'s Sentiment');
    }
  
    // Ensure sentimentFolder is defined before adding fields to it
    if (sentimentFolder) {
      sentimentFolder.add({ Sentiment: sentiment.classification }, 'Sentiment').name('Classification');
      sentimentFolder.add({ Positive: sentiment.positive }, 'Positive').name('Positive');
      sentimentFolder.add({ Neutral: sentiment.neutral }, 'Neutral').name('Neutral');
      sentimentFolder.add({ Negative: sentiment.negative }, 'Negative').name('Negative');
    }
  }

  private addCompanies(folder: dat.GUI, articleNode: any, companies: any[]): void {
    /**
     * Adds company fields to the GUI information panel.
     */
    const companiesFolder = folder.addFolder('Companies');
    companies.forEach(companyId => {
      const companyNode = this.graphData.nodes.find((n: any) => n.id === companyId);
      if (companyNode) {
        this.addCompanyFields(companiesFolder, companyNode, [articleNode.id]);
      }
    });
  }

  private addArticles(folder: dat.GUI, companyNode: any): void {
    const articlesInfoFolder = this.guiInformation!.addFolder('Articles');
    const existingFolderNames = new Set(); // Keep track of folder names to ensure uniqueness some of titles first 50 chars be same
  
    companyNode.articles.forEach((linkId: any) => {
      const articleNode = this.graphData.nodes.find((n: any) => n.id === linkId)
      if (articleNode) {
        const articleLink = this.graphData.links.find((l: any) => l.target.id === companyNode.id && l.source.id === articleNode.id);
        if (articleLink) {
          let folderName = truncateWithEllipsis(articleNode.title);
          // Ensure the folder name is unique
          let uniqueFolderName = folderName;
          let counter = 1;
          while (existingFolderNames.has(uniqueFolderName)) {
            uniqueFolderName = `${folderName} (${counter++})`;
          }
          existingFolderNames.add(uniqueFolderName); 
  
          const articleFolder = articlesInfoFolder.addFolder(uniqueFolderName);
          this.addSentimentFields(articleFolder, articleLink.sentiment);
        }
      }
    });
  }

  private addCompanyFields(folder: dat.GUI, companyNode: any, articles: any): void {
    const companyFolder = folder.addFolder(`${companyNode.short_name}`);
    companyFolder.add({ Ticker: companyNode.ticker}, 'Ticker').name('Ticker');
    companyFolder.add({ 'Open Dashboard': () => window.open(`/company/${companyNode.ticker}/dashboard`, '_blank') }, 'Open Dashboard').name('Open Dashboard');
    companyFolder.add({ 'Open Graph': () => window.open(`/company/${companyNode.ticker}/graph`, '_blank') }, 'Open Graph').name('Open Graph');

    if (folder.name === 'Companies') {
      const sentimentLink = this.graphData.links.find((l: any) => l.source.id === articles[0] && l.target.id === companyNode.id);
      if (sentimentLink) {
        this.addSentimentFields(companyFolder, sentimentLink.sentiment);
      }
    }
  }

  private displayNodeNeighbors(node: any): void {
    if (node.node_type === 'article') {
      const relatedCompanies = node.companies.map((companyId: any) => this.graphData.nodes.find((n: any) => n.id === companyId));
      this.graph.nodeVisibility((n: any) => n === node || relatedCompanies.includes(n));
      this.graph.linkVisibility((link: any) => link.source.id === node.id);
    } else if (node.node_type === 'company') {
      const relatedArticles = node.articles.map((articleId: any) => this.graphData.nodes.find((n: any) => n.id === articleId));
      this.graph.nodeVisibility((n: any) => n === node || relatedArticles.includes(n));
      this.graph.linkVisibility((link: any) => link.target === node);
    }

    const visibilityFolder = this.guiControls!.__folders['Visibility'];
    if (visibilityFolder && visibilityFolder.domElement) {
      visibilityFolder.domElement.style.display = 'none';
    }
  }

  private getNodeVal(node: any): number {
    if (node.node_type === 'article') {
      return this.calculateNodeValue(node.companies);
    } else if (node.node_type === 'company') {
      return this.calculateNodeValue(node.articles);
    } else {
      return 1;
    }
  }

  private calculateNodeValue(relatedEntities: any[]): number {
    const count = relatedEntities.map((entityId: any) => this.graphData.nodes.find((n: any) => n.id === entityId)).filter(entity => entity).length;
    return count > 0 ? count * 5 : 1;
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
  positiveDistance: number = 1500;
  neutralDistance: number = 1500;
  negativeDistance: number = 1500;

  showPOSITIVE: boolean = true;
  showNEUTRAL: boolean = true;
  showNEGATIVE: boolean = true;
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