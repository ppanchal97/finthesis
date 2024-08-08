export interface NewsItem {
    id: number;
    timestamp: string;
    title: string;
    description: string;
    fundamentals_impact_text: string;
    thesis_impact_text: string;
    fundamentals_impact: string;
    thesis_impact: string;
    tickers_impacted: string[];
    source: string;
}