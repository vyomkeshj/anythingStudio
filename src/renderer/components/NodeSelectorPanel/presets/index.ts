import { ParsedSaveData, SaveFile } from '../../../../common/SaveFile';
import basicNcnnUpscale from './PRESET -- basic_ncnn_upscale.json';
import basicOnnxUpscale from './PRESET -- basic_onnx_upscale.json';
import basicPytorchUpscale from './PRESET -- basic_pytorch_upscale.json';
import batchUpscale from './PRESET -- batch_upscale.json';
import captionedMultiUpscaleComparison from './PRESET -- captioned_multi_upscale_comparison.json';
import captionedUpscale from './PRESET -- captioned_upscale.json';
import separatedTransparencyUpscale from './PRESET -- separated_transaprency_upscale.json';

export interface Preset {
    name: string;
    author: string;
    description: string;
    /**
     * The whole chain is guaranteed to be positioned at origin (0,0).
     */
    chain: ParsedSaveData;
}

const fromJson = (json: unknown): ParsedSaveData => {
    const chain = SaveFile.parse(JSON.stringify(json));

    // move the whole chain to origin
    const freeNodes = chain.nodes.filter((n) => !n.parentNode);
    const minX = Math.min(...freeNodes.map((node) => node.position.x));
    const minY = Math.min(...freeNodes.map((node) => node.position.y));
    for (const n of freeNodes) {
        n.position.x -= minX;
        n.position.y -= minY;
    }

    return chain;
};

export const presets = [
    {
        name: 'Basic PyTorch Upscale',
        author: 'MachinesStudio',
        description: 'Upscale an image using a PyTorch model.',
        chain: fromJson(basicPytorchUpscale),
    },
    {
        name: 'Basic NCNN Upscale',
        author: 'MachinesStudio',
        description: 'Upscale an image using an NCNN model.',
        chain: fromJson(basicNcnnUpscale),
    },
    {
        name: 'Basic ONNX Upscale',
        author: 'MachinesStudio',
        description: 'Upscale an image using an ONNX model.',
        chain: fromJson(basicOnnxUpscale),
    },
    {
        name: 'Separated Transparency Upscale',
        author: 'MachinesStudio',
        description: 'A simple way of upscaling the RGB and Alpha channels separately.',
        chain: fromJson(separatedTransparencyUpscale),
    },
    {
        name: 'Batch Upscale',
        author: 'MachinesStudio',
        description: 'A simple example of a batch upscale.',
        chain: fromJson(batchUpscale),
    },
    {
        name: 'Captioned Upscale',
        author: 'MachinesStudio',
        description: 'Upscaling and attaching a caption to the output.',
        chain: fromJson(captionedUpscale),
    },
    {
        name: 'Captioned Multi-Upscale Comparison',
        author: 'MachinesStudio',
        description:
            'Upscaling with multiple models and making a comparison between them, with captions.',
        chain: fromJson(captionedMultiUpscaleComparison),
    },
];
