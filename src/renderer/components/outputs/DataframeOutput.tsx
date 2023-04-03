import { memo } from 'react';
import { OutputProps } from './props';

export const PandasDataFrameOutput = memo(({ outputId, useOutputData }: OutputProps) => {
    const { last } = useOutputData<string>(outputId);

    if (!last) {
        return <p>No data available.</p>;
    }

    return <div dangerouslySetInnerHTML={{ __html: last }} />;
});
