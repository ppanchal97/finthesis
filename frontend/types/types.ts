export interface NewsItem {
    id: number;
    timestamp: string;
    title: string;
    description: string;
    full_text: string;
    holding_impact: string;
    portfolio_impact: string;
    holdings_impacted: string[];
    source: string;
}