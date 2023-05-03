import { app } from 'electron';
import log from 'electron-log';
import { readdirSync, rmSync } from 'fs';
import os from 'os';
import path from 'path';
import './i18n';
import { parseArgs } from './arguments';
import { createCli } from './cli/create';
import { runChainInCli } from './cli/run';
import { createGuiApp } from './gui/create';
import { getRootDirSync } from './platform';

const installExtensions = async () => {
    const installer = require('electron-devtools-installer')
    const forceDownload = !!process.env.UPGRADE_EXTENSIONS
    const extensions = [
        'REACT_DEVELOPER_TOOLS',
        'REDUX_DEVTOOLS',
        'DEVTRON'
    ]

    return Promise
        .all(extensions.map(name => installer.default(installer[name], forceDownload)))
        .catch(console.log)
}
const startApp = () => {
    const args = parseArgs(process.argv.slice(app.isPackaged ? 1 : 2));
    if (process.argv.indexOf('--noDevServer') === -1) {
        installExtensions().then(() => {
            console.info("Installed DEV Tools!")
        })
    }
    log.transports.file.resolvePath = (variables) =>
        path.join(getRootDirSync(), 'logs', variables.fileName!);
    log.transports.file.level = 'info';

    process.env.ELECTRON_DISABLE_SECURITY_WARNINGS = 'true';

    app.setPath('userData', getRootDirSync());

    app.on('quit', () => {
        log.info('Cleaning up temp folders...');
        const tempDir = os.tmpdir();
        // find all the folders starting with 'MachinesStudio-'
        const tempFolders = readdirSync(tempDir, { withFileTypes: true })
            .filter((dir) => dir.isDirectory())
            .map((dir) => dir.name)
            .filter((name) => name.includes('MachinesStudio-'));
        tempFolders.forEach((folder) => {
            try {
                rmSync(path.join(tempDir, folder), { force: true, recursive: true });
            } catch (error) {
                log.error(`Error removing temp folder. ${String(error)}`);
            }
        });
    });

    if (args.command === 'open') {
        createGuiApp(args);
    } else {
        createCli(() => runChainInCli(args));
    }
};

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
// eslint-disable-next-line global-require
if (require('electron-squirrel-startup')) {
    app.quit();
} else {
    startApp();
}
