import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpService } from '../../services/http.service';
import { ActivatedRoute } from '@angular/router';
import { ForceGraph3DInstance } from '3d-force-graph';
import ForceGraph3D from '3d-force-graph';
import * as dat from 'dat.gui';

import { CompanyGraph, Sentiment } from '../../models/CompanyGraph.model';

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
   /**
     * When the component is initialized, the graph data is loaded.
     * Once the data is loaded, the graph is launched.
     */
    this.loadGraphData();
  }

  ngOnDestroy(): void {
    /**
     * Cleanup when the component is destroyed.
     */
    this.cleanup();
  }

  private loadGraphData(): void {
    /**
     * Load the graph data from the API.
     */
    this.route.params.subscribe(params => {
      const ticker = params['ticker'];
      this.httpService.getCompanyGraphData(ticker).subscribe((res: CompanyGraph) => {
        this.graphData = { nodes: res.nodes, links: res.links };
        this.launchGraph();
      });
    });
  }

  private launchGraph(): void {
    /**
     * Launches the 3D graph with the loaded data.
     * The graph is set up with the necessary settings and event listeners.
     * The GUI is set up to allow the user to control the graph's settings.
     */
    const elem = document.getElementById('3d-graph') as HTMLElement;
    this.graph = ForceGraph3D()(elem)
      .graphData(this.graphData) 
      .forceEngine('d3')
      .nodeOpacity(1)
      .backgroundColor('#131316')
      .linkWidth(link => this.highlightLinks.has(link) ? 5 : 1)
      .linkDirectionalParticleWidth(link => this.highlightLinks.has(link) ? 5 : 0)
      .linkDirectionalParticles(link => this.highlightLinks.has(link) ? 5 : 0)
      .linkDirectionalParticleSpeed(link => this.highlightLinks.has(link) ? 0.01 : 0.006)
      .linkColor((link: any) => this.getColorBySentiment(link.sentiment))
      .nodeVal(node => this.getNodeValue(node))
      .nodeColor(node => this.getNodeColor(node))
      .nodeLabel(node => this.getNodeLabel(node))
      .onNodeClick(node => this.onNodeClick(node))
      .onNodeHover(node => this.onNodeHover(node));

    this.setupGuiControls();
  }

  private getNodeValue(node: any): number {
    /**
     * Node value is used to determine the size of the node.
     */
    if (this.highlightNodes.has(node)) {
      // Increase the size of the node when it is highlighted
      return node === this.hoverNode ? 50 : 25;
    }
    return node.node_type == 'company' ? 2 : 1;
  }

  private getNodeColor(node: any): string {
    /**
     * Node color is used to determine the color of the node.
     * If the node is a company, it will be colored blue. Otherwise, it will be colored based on its sentiment.
     */
    return node.node_type === 'company' ? '#1D57A9' : this.getColorBySentiment(node.sentiment);
  }

  private getNodeLabel(node: any): string {
    /**
     * Node label is used to determine the text displayed on the node.
     * If the node is a company, it will display the company's short name. Otherwise, it will display the article's title.
     */
    return node.node_type === 'company' ? node.short_name : node.title;
  }

  private onNodeClick(node: any): void {
    /**
     * When a node is clicked, the graph will zoom in on the node and display information about the node.
     * If the node is an article, it will display information about the article. 
     * If the node is a company, it will display information about the company.
     */
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

  private onNodeHover(node: any): void {
    /**
     * When a node is hovered over, the graph will highlight the node and related elements.
     * If the node is an article, it will highlight the company related to the article.
     */
    if (this.isNodeAlreadyHovered(node)) return;

    this.clearHighlights();
    if (node) {
      this.highlightNodeAndRelatedElements(node);
    }
    this.hoverNode = node || null;
    this.updateHighlight();
  }

  private isNodeAlreadyHovered(node: any): boolean {
    /**
     * Check if the node is already hovered over.
     */
    return (!node && !this.highlightNodes.size) || (node && this.hoverNode === node);
  }

  private clearHighlights(): void {
    /**
     * Clear all highlights from the graph.
     */
    this.highlightNodes.clear();
    this.highlightLinks.clear();
  }

  private highlightNodeAndRelatedElements(node: any): void {
    /**
     * Highlight the node and related elements in the graph.
     * If the node is an article, it will highlight the company related to the article.
     */
    this.highlightNodes.add(node);
    if (node.node_type === 'article') {
      this.highlightRelatedCompany(node);
    }
  }

  private highlightRelatedCompany(node: any): void {
    /**
     * Highlight the company related to the article.
     */
    const companyId = this.graphData.links[0].target.id;
    const companyNode = this.graphData.nodes.find((n: any) => n.id === companyId);
    if (companyNode) this.highlightNodes.add(companyNode);
    const link = this.graphData.links.find((l: any) => l.target.id === companyId && l.source.id === node.id);
    if (link) this.highlightLinks.add(link);
  }

  private updateHighlight(): void {
    /**
     * Update the graph to reflect the current highlights.
     * This will update the size and color of the nodes, as well as the width and color of the links.
     */
    this.graph
      .nodeVal(this.graph.nodeVal())
      .linkWidth(this.graph.linkWidth())
      .linkDirectionalParticles(this.graph.linkDirectionalParticles())
      .linkDirectionalParticleSpeed(this.graph.linkDirectionalParticleSpeed())
      .linkDirectionalParticleWidth(this.graph.linkDirectionalParticleWidth());
  }

  private getColorBySentiment(sentiment: Sentiment): string {
    /**
     * Determine the color of the node based on its sentiment.
     * If the sentiment is positive, the node will be colored green.
     * If the sentiment is negative, the node will be colored red.
     * If the sentiment is neutral, the node will be colored based on the balance of positive and negative sentiment.
     */
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
    /**
     * Setup the general GUI controls for the graph.
     * This will allow the user to adjust the link distances and visibility of the nodes and links.
     */
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
    /**
     * Updates the link distance in the graph based on the user's settings.
     * The link distance is set based on the sentiment classification of the link.
     * The distance is set to the user's specified distance for the sentiment classification.
     */
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
     * Update the visibility of the nodes and links based on the user settings.
     * This will show or hide nodes and links based on their sentiment classification.
     */
    this.graph.nodeVisibility((node: any) => {
      if (node.node_type === 'article') {
        // Show only the nodes that match the sentiment classification
        const key: keyof GraphSettings = `show${node.sentiment.classification}` as keyof GraphSettings;
        // Return true if the sentiment classification is visible
        return Boolean(settings[key]);
      }
      return true;
    });

    this.graph.linkVisibility((link: any) => {
      // Show only the links that match the sentiment classification
      const key: keyof GraphSettings = `show${link.sentiment.classification}` as keyof GraphSettings;
      // Return true if the sentiment classification is visible
      return Boolean(settings[key]);
    });
  }

  private displayNodeInformation(node: any): void {
    /**
     * Display information about the node in the GUI.
     */
    this.resetGuiInformation();
    if (node.node_type === 'article') {
      // Display article information
      this.displayArticleInformation(node);
    } else if (node.node_type === 'company') {
      // Display company information
      this.displayCompanyInformation(node);
    }
  }

  private resetGuiInformation(): void {
    /**
     * Reset the GUI information panel.
     */

    if (this.guiInformation) {
      this.guiInformation.destroy();
    }
    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private displayArticleInformation(node: any): void {
    /**
     * Display information about the article in the GUI.
     */
    const articleInfoFolder = this.guiInformation!.addFolder('Article Information');
    this.addArticleFields(articleInfoFolder, node);
    this.addSentimentFields(articleInfoFolder, node.sentiment);
  }

  private addArticleFields(folder: dat.GUI, node: any): void {
    /**
     * Add fields for the article information to the GUI.
     */
    folder.add({ Title: node.title }, 'Title').name('Title');
    folder.add({ PublishedDate: node.published_date }, 'PublishedDate').name('Published Date');
    folder.add({ Author: node.author }, 'Author').name('Author');
    folder.add({ 'Open URL': () => window.open(node.url, '_blank') }, 'Open URL').name('Open Article');
  }

  private addSentimentFields(folder: dat.GUI, sentiment: Sentiment): void {
    /**
     * Add fields for the sentiment information to the GUI.
     * If the folder does not exist, it will be created. Otherwise, the fields will be added to the existing folder.
     * It is due to taht depends if we call this function from the company or article information.
     * If we call it from the company information, we will have to create the folder.
     * If we call it from the article information, the folder will already exist. 
     * And we do not provide Today's Sentiment folder in the article information.
     */
    const sentimentFolder = folder.name === "Today's Sentiment" ? folder : folder.addFolder('Sentiment');
    sentimentFolder.add({ Sentiment: sentiment.classification }, 'Sentiment').name('Classification');
    sentimentFolder.add({ Positive: sentiment.positive }, 'Positive').name('Positive');
    sentimentFolder.add({ Neutral: sentiment.neutral }, 'Neutral').name('Neutral');
    sentimentFolder.add({ Negative: sentiment.negative }, 'Negative').name('Negative');
  }

  private displayCompanyInformation(node: any): void {
    /**
     * Display information about the company in the GUI.
     */
    const companyInfoFolder = this.guiInformation!.addFolder('Company Information');
    this.addCompanyFields(companyInfoFolder, node);
    this.addSentimentFields(companyInfoFolder.addFolder("Today's Sentiment"), node.sentiment);
    this.addArticles(companyInfoFolder, node);
  }

  private addCompanyFields(folder: dat.GUI, companyNode: any): void {
    /**
     * Add fields for the company information to the GUI.
     */
    const companyFolder = folder.addFolder(`${companyNode.short_name}`);
    companyFolder.add({ Ticker: companyNode.ticker}, 'Ticker').name('Ticker');
    companyFolder.add({ 'Open Dashboard': () => window.open(`/company/${companyNode.ticker}/dashboard`, '_blank') }, 'Open Dashboard').name('Open Dashboard');
  }

  private addArticles(folder: dat.GUI, companyNode: any): void {
    /**
     * Add fields for the articles related to the company to the GUI.
     * This will display information about the articles related to the company.
     */
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
    /**
     * Cleanup when the component is destroyed.
     * This will destroy the GUI controls and information panels, as well as the graph.
     * It is important to clean up the resources when the component is destroyed to prevent memory leaks.
     */
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
  /**
   * Graph GUI settings for controlling the graph's appearance.
   */

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
   * Truncate the text with an ellipsis if it exceeds the maximum length for GUI fields.
   */

  const maxLength: number = 50;

  if (text.length > maxLength) {
    return text.substring(0, maxLength - 3) + '...'; 
  } else {
    return text;
  }
}
