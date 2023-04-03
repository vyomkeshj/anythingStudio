import { memo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { OutputProps } from './props';

export const MarkdownOutput = memo(({ outputId, useOutputData }: OutputProps) => {
    const { last } = useOutputData<string>(outputId);

    if (!last) {
        return <p>No data available.</p>;
    }

    return (
        <ReactMarkdown
            children={last}
            remarkPlugins={[remarkGfm]}
        />
    );
});
