const AdmZip = require('adm-zip');

/** @type {import("@electron-forge/shared-types").ForgeConfig} */
const config = {
    packagerConfig: {
        executableName: 'machines',
        extraResource: './backend/src/',
        icon: './src/public/icons/cross_platform/icon',
    },
    publishers: [
        {
            name: '@electron-forge/publisher-github',
            config: {
                repository: {
                    owner: 'MachinesStudio-org',
                    name: 'MachinesStudio',
                },
            },
            draft: true,
            prerelease: true,
        },
    ],
    makers: [
        {
            name: '@electron-forge/maker-squirrel',
            config: {
                name: 'machines',
                iconUrl:
                    'https://github.com/MachinesStudio-org/MachinesStudio/blob/main/src/public/icons/win/icon.ico',
                setupIcon: './src/public/icons/win/icon.ico',
                loadingGif: './src/public/icons/win/installing_loop.gif',
            },
        },
        {
            name: '@electron-forge/maker-zip',
            platforms: ['darwin', 'linux', 'win32'],
        },
        {
            name: '@electron-forge/maker-dmg',
            config: {
                format: 'ULFO',
                name: 'MachinesStudio',
                icon: './src/public/icons/mac/icon.icns',
            },
        },
        {
            name: '@electron-forge/maker-deb',
            config: {
                name: 'machines',
                options: {
                    icon: './src/public/icons/cross_platform/icon.png',
                },
            },
        },
        {
            name: '@electron-forge/maker-rpm',
            config: {
                name: 'machines',
                options: {
                    icon: './src/public/icons/cross_platform/icon.png',
                },
            },
        },
    ],
    plugins: [
        {
            name: '@electron-forge/plugin-webpack',
            config: {
                mainConfig: './webpack.main.config.js',
                renderer: {
                    config: './webpack.renderer.config.js',
                    nodeIntegration: true,
                    contextIsolation: false,
                    entryPoints: [
                        {
                            html: './src/renderer/index.html',
                            js: './src/renderer/renderer.js',
                            name: 'main_window',
                        },
                        {
                            html: './src/renderer/splash.html',
                            js: './src/renderer/splash_renderer.js',
                            name: 'splash_screen',
                        },
                    ],
                },
                devContentSecurityPolicy: '',
            },
        },
    ],
    hooks: {
        postMake: async (forgeConfig, makeResults) => {
            const justArtifacts = makeResults.map((m) => m.artifacts).reduce((a, b) => a.concat(b));
            const zipArtifact = justArtifacts.find((a) => a.endsWith('.zip'));
            if (zipArtifact) {
                // Add an empty `portable` file to the zip
                const zip = new AdmZip(zipArtifact);
                zip.addFile('portable', Buffer.alloc(0));
                zip.writeZip(zipArtifact);
            }
        },
    },
};

module.exports = config;
