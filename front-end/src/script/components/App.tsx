import * as React from 'react';
import { VehicleGrid } from './VehicleGrid';

const API_BASE = 'http://localhost:8080/api';
const MAKE_NAME = 'Acura';
const AUTH_CREDENTIALS = { username: 'admin', password: 'admin123' };

interface VehicleModel {
    id: number;
    name: string;
}

interface CoverageMap {
    [modelName: string]: number[];
}

const authFetch = async (url: string, token: string, options: RequestInit = {}) => {
    return fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
        },
    });
};

export const App: React.FC = () => {
    const [makeId, setMakeId] = React.useState<number | null>(null);
    const [models, setModels] = React.useState<VehicleModel[]>([]);
    const [years, setYears] = React.useState<number[]>([]);
    const [coverage, setCoverage] = React.useState<CoverageMap>({});
    const [makeName, setMakeName] = React.useState<string>('');
    const [loading, setLoading] = React.useState(true);
    const [token, setToken] = React.useState<string | null>(null);
    const [toast, setToast] = React.useState<string | null>(null);
    const toastTimer = React.useRef<number | null>(null);

    const showToast = (message: string) => {
        if (toastTimer.current) clearTimeout(toastTimer.current);
        setToast(message);
        toastTimer.current = window.setTimeout(() => setToast(null), 4000);
    };

    React.useEffect(() => {
        const fetchData = async () => {
            try {
                // Step 1: Authenticate
                const loginRes = await fetch(`${API_BASE}/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(AUTH_CREDENTIALS),
                });

                if (!loginRes.ok) {
                    console.error('Authentication failed');
                    setLoading(false);
                    return;
                }

                const loginData = await loginRes.json();
                const jwt = loginData.token;
                setToken(jwt);

                // Step 2: Resolve make name to ID
                const makesRes = await authFetch(`${API_BASE}/vehicle-makes`, jwt);
                const makesData = await makesRes.json();
                const make = makesData.vehicle_makes.find((m: any) => m.name === MAKE_NAME);

                if (!make) {
                    console.error(`Vehicle make "${MAKE_NAME}" not found`);
                    setLoading(false);
                    return;
                }

                setMakeId(make.id);
                setMakeName(make.name);

                // Step 3: Fetch data using the resolved ID
                const [modelsRes, yearsRes, coverageRes] = await Promise.all([
                    authFetch(`${API_BASE}/vehicle-makes/${make.id}/models`, jwt),
                    authFetch(`${API_BASE}/vehicle-years`, jwt),
                    authFetch(`${API_BASE}/vehicle-makes/${make.id}/coverage`, jwt),
                ]);

                const modelsData = await modelsRes.json();
                const yearsData = await yearsRes.json();
                const coverageData = await coverageRes.json();

                setModels(modelsData.vehicle_models);
                setYears(yearsData.vehicle_years);
                setCoverage(coverageData.coverage);
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch data:', error);
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    const handleToggle = async (modelId: number, modelName: string, year: number) => {
        if (!token) return;

        try {
            const res = await authFetch(`${API_BASE}/vehicle-makes/${makeId}/coverage/toggle`, token, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    vehicle_model_id: modelId,
                    vehicle_year: year,
                }),
            });

            if (!res.ok) {
                showToast(`Failed to update ${modelName} ${year} — server error`);
            } else {
                const data = await res.json();
                setCoverage(prev => ({
                    ...prev,
                    [modelName]: data.state === 1
                        ? [...(prev[modelName] || []).filter(y => y !== year), year]
                        : (prev[modelName] || []).filter(y => y !== year),
                }));
            }
        } catch (error) {
            showToast(`Failed to update ${modelName} ${year} — network error`);
        }
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="app">
            <VehicleGrid
                makeName={makeName}
                models={models}
                years={years}
                coverage={coverage}
                onToggle={handleToggle}
            />
            {toast && (
                <div className="toast">{toast}</div>
            )}
        </div>
    );
};
