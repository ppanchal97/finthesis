// components/ImpactBox.tsx
import React from 'react';

interface ImpactBoxProps {
    impact: string;
    customStyles?: React.CSSProperties;  // Ensure it accepts React.CSSProperties
}

const getColor = (impact: string) => {
    switch (impact.toLowerCase()) {
        case 'critical':
            return '#FF5050';
        case 'moderate':
            return '#FFAF50';
        case 'positive':
            return '#42D662';
        default:
            return '#CCCCCC';  // Default or unknown impact color
    }
}

const ImpactBox: React.FC<ImpactBoxProps> = ({ impact, customStyles = {} }) => {
    return (
        <div style={{
            height: '17px', // Default height unless overridden
            backgroundColor: getColor(impact),
            borderRadius: '10px',
            flexShrink: 0,
            ...customStyles  // Apply custom styles, if any
        }} />
    );
};

export default ImpactBox;
