import React, { createContext, useState } from 'react';

interface DataContextType {
    dataPoints: number[];
    labels: string[];
    setDataPoints: React.Dispatch<React.SetStateAction<number[]>>;
    setLabels: React.Dispatch<React.SetStateAction<string[]>>;
}
interface DataProviderProps {
    children: JSX.Element;
}

export const DataContext = createContext<DataContextType>({
    dataPoints: [20,40,50],
    labels: ['20','40','50'],
    setDataPoints: () => {},
    setLabels: () => {},
});

export const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
    const [dataPoints, setDataPoints] = useState<number[]>([]);
    const [labels, setLabels] = useState<string[]>([]);

    return (
        <DataContext.Provider value={{ dataPoints, labels, setDataPoints, setLabels }}>
            {children}
        </DataContext.Provider>
    );
};
