import InnerHTML from 'dangerously-set-html-content';
import { memo } from 'react';
import { OutputProps } from './props';

export const HtmlOutput = memo(({ outputId, useOutputData }: OutputProps) => {
    const { last } = useOutputData<string>(outputId);

    if (!last) {
        return <p>No data available.</p>;
    }

    return <InnerHTML html={last} />;
});
