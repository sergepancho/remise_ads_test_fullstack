import * as React from 'react';

interface VehicleModel {
    id: number;
    name: string;
}

interface CoverageMap {
    [modelName: string]: number[];
}

interface VehicleGridProps {
    makeName: string;
    models: VehicleModel[];
    years: number[];
    coverage: CoverageMap;
    onToggle: (modelId: number, modelName: string, year: number) => void;
}

export const VehicleGrid: React.FC<VehicleGridProps> = ({
    makeName,
    models,
    years,
    coverage,
    onToggle,
}) => {
    const isCovered = (modelName: string, year: number): boolean => {
        const modelYears = coverage[modelName] || [];
        return modelYears.includes(year);
    };

    return (
        <div className="vehicle-grid">
            <div className="grid-row header-row">
                <div className="logo-cell">
                    <svg viewBox="0 0 100 120" className="acura-logo">
                        <circle cx="50" cy="50" r="40" fill="none" stroke="white" strokeWidth="3" />
                        <path d="M50 15 L72 78 L63 78 L56 58 L44 58 L37 78 L28 78 Z" fill="white" />
                        <path d="M46 50 L54 50 L58 58 L42 58 Z" fill="#888" />
                    </svg>
                </div>
                {years.map(year => (
                    <div className="year-header" key={year}>
                        <span>{year}</span>
                    </div>
                ))}
            </div>
            {models.map((model, index) => (
                <div
                    className={`grid-row data-row ${index % 2 === 0 ? 'even' : 'odd'}`}
                    key={model.id}
                >
                    <div className="model-cell">{model.name}</div>
                    {years.map(year => (
                        <div
                            className={`cell ${isCovered(model.name, year) ? 'covered' : 'uncovered'}`}
                            key={`${model.id}-${year}`}
                            onClick={() => onToggle(model.id, model.name, year)}
                            title={`${model.name} ${year}`}
                        />
                    ))}
                </div>
            ))}
        </div>
    );
};
