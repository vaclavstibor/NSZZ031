import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpService } from '../services/http.service';
import ForceGraph3D, { ForceGraph3DInstance } from '3d-force-graph';
import * as dat from 'dat.gui';

import { CompaniesGraphs, Sentiment } from '../models/CompaniesGraphs.model';

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
    /**
     * When the component is initialized, the graph data is loaded.
     * Once the data is loaded, the graph is launched.
     */
    this.loadGraphData();
  }

  ngOnDestroy(): void {
    /**
     * When the component is destroyed, the graph is cleaned up.
     */
    this.cleanup();
  }

  private loadGraphData(): void {
    this.httpService.getCompaniesGraphsData().subscribe((res: CompaniesGraphs) => {
      this.graphData = { nodes: res.nodes, links: res.links };
      this.launchGraph();
    });
  }

  private launchGraph() {
    /**
     * Launches the 3D graph with the loaded data.
     * The graph is set up with the necessary settings and event listeners.
     * The GUI is set up to allow the user to control the graph's settings.
     */
    const elem = document.getElementById('3d-graph') as HTMLElement;
    this.graph = ForceGraph3D()(elem)
      .graphData(this.graphData)
      .cameraPosition({ z: 6000 }) // Initial camera position
      .forceEngine('d3')
      .nodeOpacity(1)
      .backgroundColor('#131316')
      .linkWidth(link => this.highlightLinks.has(link) ? 10 : 5)
      .linkDirectionalParticleWidth(link => this.highlightLinks.has(link) ? 10 : 0)
      .linkDirectionalParticles(link => this.highlightLinks.has(link) ? 8 : 0)
      .linkDirectionalParticleSpeed(link => this.highlightLinks.has(link) ? 0.01 : 0.006)
      .linkColor((link: any) => this.getColorBySentiment(link.sentiment))
      .nodeVal((node: any) => this.highlightNodes.has(node) ? this.getNodeVal(node) * 10 : this.getNodeVal(node))
      .nodeColor((node: any) => node.node_type === 'company' ? '#1D57A9' : this.getColorBySentiment(node.sentiment))
      .nodeLabel((node: any) => node.node_type === 'company' ? `${node.short_name}` : `${node.title}`)
      .onNodeClick((node: any) => this.onNodeClick(node))
      .onNodeRightClick(() => this.resetNodeVisibility())
      .onNodeHover(node => this.onNodeHover(node));
    
      if (this.graph) {
        const chargeForce = this.graph.d3Force('charge');
        if (chargeForce) {
          // Spread nodes a wider apart
          chargeForce['strength'](-5000);
        }
      }
    this.setupGUIControls();
  }

  private setupGUIControls(): void {
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

    this.guiInformation = new dat.GUI({ autoPlace: true, width: 350 });
  }

  private onNodeClick(node: any): void {
    /**
     * When a node is clicked, the graph will zoom in on the node,
     * display information about the node, and display the node's neighbors.
     * The GUI will display different information based on the type of node (article or company).
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

  private onNodeHover(node: any): void {
    /**
     * When a node is hovered over, the node and its related elements will be highlighted.
     */

    if (this.isNodeAlreadyHovered(node)) return;

    this.clearHighlights();
    if (node) {
      this.highlightNodeAndRelatedElements(node);
    }

    this.hoverNode = node || null;
    this.updateHighlight();
  }

  private resetNodeVisibility(): void {
    /**
     * Resets the visibility of the nodes and links in the graph.
     * All nodes and links will be visible. In graphs it is not necessary implement 
     * filtering by colour 
     */
    this.graph.nodeVisibility(() => true);
    this.graph.linkVisibility(() => true);

    // Reset the GUI visibility settings
    const visibilityFolder = this.guiControls!.__folders['Visibility'];
    if (visibilityFolder && visibilityFolder.domElement) {
      visibilityFolder.domElement.style.display = '';
    }
    this.guiControls!.__folders['Visibility'].__controllers.forEach(controller => controller.setValue(true));
  }

  private isNodeAlreadyHovered(node: any): boolean {
    /**
     * Checks if the node is already hovered over.
     */
    return (!node && !this.highlightNodes.size) || (node && this.hoverNode === node);
  }

  private clearHighlights(): void {
    /**
     * Clears the highlights from the graph.
     */
    this.highlightNodes.clear();
    this.highlightLinks.clear();
  }

  private highlightNodeAndRelatedElements(node: any): void {
    /**
     * Highlights the node and its related elements in the graph.
     */
    this.highlightNodes.add(node);

    if (node.node_type === 'article') {
      this.highlightRelatedCompanies(node);
    } else if (node.node_type === 'company') {
      this.highlightRelatedArticles(node);
    }
  }

  private highlightRelatedCompanies(node: any): void {
    /**
     * Highlights the companies related to the article node.
     * The companies are highlighted by adding them to the highlightNodes set.
     */
    node.companies.forEach((companyId: any) => {
      // Find the company node by ID
      const companyNode = this.graphData.nodes.find((n: any) => n.id === companyId);
      // Add the company node to the highlightNodes set
      if (companyNode) this.highlightNodes.add(companyNode);
      // Find the link between the article and the company
      const link = this.graphData.links.find((l: any) => l.target.id === companyId && l.source.id === node.id);
      // Add the link to the highlightLinks set
      if (link) this.highlightLinks.add(link);
    });
  }

  private highlightRelatedArticles(node: any): void {
    /**
     * Highlights the articles related to the company node.
     * The articles are highlighted by adding them to the highlightNodes set.
     */
    node.articles.forEach((articleId: any) => {
      // Find the article node by ID
      const articleNode = this.graphData.nodes.find((n: any) => n.id === articleId);
      // Add the article node to the highlightNodes set
      if (articleNode) this.highlightNodes.add(articleNode);
      // Find the link between the article and the company
      const link = this.graphData.links.find((l: any) => l.target.id === node.id && l.source.id === articleId);
      // Add the link to the highlightLinks set
      if (link) this.highlightLinks.add(link);
    });
  }

  private updateHighlight(): void {
    /**
     * Updates the highlights in the graph based on the current state of the highlights.
     * The node and link colors are updated based on if they are in the highlight sets.
     * The link width and particle settings are also updated based on the highlight sets.
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
     * Returns a color based on the sentiment classification.
     * The color is determined by the classification and the sentiment values.
     */
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

  private getNeutralColor(sentiment: Sentiment): string {
    /**
     * Returns a color for a neutral sentiment based on the positive and negative values.
     * The color is a shade of red or green based on which sentiment is higher.
     * The alpha value is increased to make the color more visible.
     * The color is more red if the negative sentiment is higher, and more green if the positive sentiment is higher.
     */
    const alpha = sentiment.negative > sentiment.positive
      ? Number(sentiment.negative) + 0.30
      : Number(sentiment.positive) + 0.30;
    return `rgba(${sentiment.negative > sentiment.positive ? '255, 0, 0' : '0, 128, 0'}, ${alpha})`;
  }

  private updateLinkDistance(settings: GraphSettings): void {
    /**
     * Updates the link distance in the graph based on the user's settings.
     * The distance is set to the user's specified distance for the link's sentiment classification.
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
    /**
     * Displays article information in the GUI information panel.
     * The article information includes the title, published date, author, and sentiment.
     */
    const articleInfoFolder = this.guiInformation!.addFolder('Article Information');
    this.addArticleFields(articleInfoFolder, node);
    this.addSentimentFields(articleInfoFolder, node.sentiment);
    this.addCompanies(articleInfoFolder, node, node.companies);
  }

  private displayCompanyInformation(node: any): void {
    /**
     * Displays company information in the GUI information panel.
     * The company information includes the short name, ticker, sentiment, and articles.
     */
    const companyInfoFolder = this.guiInformation!.addFolder('Company Information');
    this.addCompanyFields(companyInfoFolder, node, node.articles);
    this.addArticles(companyInfoFolder, node);
  }

  private addArticleFields(folder: dat.GUI, node: any): void {
    /**
     * Adds article fields to the GUI information panel.
     * The article fields include the title, published date, author, and a link to the article.
     */
    folder.add({ Title: node.title }, 'Title').name('Title');
    folder.add({ PublishedDate: node.published_date }, 'PublishedDate').name('Published Date');
    folder.add({ Author: node.author }, 'Author').name('Author');
    folder.add({ 'Open URL': () => window.open(node.url, '_blank') }, 'Open URL').name('Open Article');
  }

  private addSentimentFields(folder: dat.GUI, sentiment: any): void {
    /**
     * Adds sentiment fields to the GUI information panel.
     * The sentiment fields include the classification, positive, neutral, and negative values.
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
     * The company fields include the short name, ticker, sentiment, and a link to the company dashboard.
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
    /**
     * Adds article fields to the GUI information panel.
     * The article fields include the title and sentiment of the articles related to the company.
     * The articles are displayed in folders named after the article titles.
     * The sentiment of the link between the article and the company is used to determine the sentiment of the article.
     * The sentiment of the article is displayed in the GUI information panel.
     * The sentiment of the article is displayed in a folder named after the article title.
     */
    const articlesInfoFolder = this.guiInformation!.addFolder('Articles');
    const existingFolderNames = new Set(); // Keep track of folder names to ensure uniqueness some of titles first 50 chars be same
  
    companyNode.articles.forEach((linkId: any) => {
      // Find the article node by ID
      const articleNode = this.graphData.nodes.find((n: any) => n.id === linkId)
      if (articleNode) {
        // Find the link between the article and the company
        const articleLink = this.graphData.links.find((l: any) => l.target.id === companyNode.id && l.source.id === articleNode.id);
        if (articleLink) {
          // Truncate the folder name to ensure it fits in the GUI
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
    /**
     * Adds company fields to the GUI information panel.
     * The company fields include the short name, ticker, and links to the company dashboard and graph.
     * The sentiment of the link between the article and the company is used to determine the sentiment of the company.
     * The sentiment of the company is displayed in the GUI information panel.
     * The sentiment of the company is displayed in a folder named after the company short name.
     */
    const companyFolder = folder.addFolder(`${companyNode.short_name}`);
    companyFolder.add({ Ticker: companyNode.ticker}, 'Ticker').name('Ticker');
    companyFolder.add({ 'Open Dashboard': () => window.open(`/company/${companyNode.ticker}/dashboard`, '_blank') }, 'Open Dashboard').name('Open Dashboard');
    companyFolder.add({ 'Open Graph': () => window.open(`/company/${companyNode.ticker}/graph`, '_blank') }, 'Open Graph').name('Open Graph');

    if (folder.name === 'Companies') {
      // Find the sentiment link between the article and the company
      const sentimentLink = this.graphData.links.find((l: any) => l.source.id === articles[0] && l.target.id === companyNode.id);
      if (sentimentLink) {
        // Add the sentiment fields to the company folder
        this.addSentimentFields(companyFolder, sentimentLink.sentiment);
      }
    }
  }

  private displayNodeNeighbors(node: any): void {
    /**
     * Displays the neighbors of the node in the graph.
     * The neighbors are the nodes that are directly connected to the node.
     * The neighbors are set to visible in the graph.
     * The neighbors are displayed in the GUI information panel.
     */
    if (node.node_type === 'article') {
      // Map the company IDs to company nodes
      const relatedCompanies = node.companies.map((companyId: any) => this.graphData.nodes.find((n: any) => n.id === companyId));
      // Set the visibility of the nodes in the graph
      this.graph.nodeVisibility((n: any) => n === node || relatedCompanies.includes(n));
      // Set the visibility of the links in the graph
      this.graph.linkVisibility((link: any) => link.source.id === node.id);
    } else if (node.node_type === 'company') {
      // Map the article IDs to article nodes
      const relatedArticles = node.articles.map((articleId: any) => this.graphData.nodes.find((n: any) => n.id === articleId));
      // Set the visibility of the nodes in the graph
      this.graph.nodeVisibility((n: any) => n === node || relatedArticles.includes(n));
      // Set the visibility of the links in the graph
      this.graph.linkVisibility((link: any) => link.target === node);
    }

    // Hide the visibility folder in the GUI controls
    const visibilityFolder = this.guiControls!.__folders['Visibility'];
    if (visibilityFolder && visibilityFolder.domElement) {
      visibilityFolder.domElement.style.display = 'none';
    }
  }

  private getNodeVal(node: any): number {
    /**
     * Returns the value of the node based on the node type.
     * The value of the node is used to determine the size of the node in the graph.
     * The value is calculated based on the number of related entities (articles or companies).
     */
    if (node.node_type === 'article') {
      return this.calculateNodeValue(node.companies);
    } else if (node.node_type === 'company') {
      return this.calculateNodeValue(node.articles);
    } else {
      return 1;
    }
  }

  private calculateNodeValue(relatedNodes: any[]): number {
    /**
     * Calculates the value of the node based on the number of related nodes.
     */
    const count = relatedNodes.map((nodeId: any) => this.graphData.nodes.find((n: any) => n.id === nodeId)).filter(node => node).length;
    return count > 0 ? count * 5 : 1;
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
  
  positiveDistance: number = 1500;
  neutralDistance: number = 1500;
  negativeDistance: number = 1500;

  showPOSITIVE: boolean = true;
  showNEUTRAL: boolean = true;
  showNEGATIVE: boolean = true;
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